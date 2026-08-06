import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

import { getAirports } from "../../api/airportApi";
import { useAuth } from "../../hooks/useAuth";
import AirportSelect from "../../components/AirportSelect";
import "../../CSS/Home.css";

const today = new Date().toISOString().split("T")[0];

export default function Home() {
    const [airports, setAirports] = useState([]);
    const [origin, setOrigin] = useState("");
    const [destination, setDestination] = useState("");
    const [departureDate, setDepartureDate] = useState("");
    const [travelClass, setTravelClass] = useState("economy");
    const [mode, setMode] = useState("balanced");
    const [error, setError] = useState(null);

    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const KNOWN_PAIRS = [
        ["BOM", "MNN"], ["NMI", "BLR"], ["BOM", "BLR"],
        ["DEL", "HYD"], ["BOM", "GOI"], ["BLR", "MNN"],
    ];

    const popularRoutes = KNOWN_PAIRS
        .map(([from, to]) => {
            const fromA = airports.find((a) => a.iata_code === from);
            const toA = airports.find((a) => a.iata_code === to);
            if (!fromA || !toA) return null;
            return { from, to, fromCity: fromA.city, toCity: toA.city };
        })
        .filter(Boolean)
        .slice(0, 6);

    useEffect(() => {
        getAirports().then(setAirports).catch(() => setAirports([]));
    }, []);

    useEffect(() => {
        const preserved = location.state?.searchParams;
        if (preserved) {
            setOrigin(preserved.origin || "");
            setDestination(preserved.destination || "");
            setDepartureDate(preserved.departureDate || "");
            setTravelClass(preserved.travelClass || "economy");
            setMode(preserved.mode || "balanced");
        }
    }, [location.state]);

    function handleSearch(e) {
        e.preventDefault();
        setError(null);

        if (!origin || !destination) {
            setError("Please select both origin and destination.");
            return;
        }
        if (origin === destination) {
            setError("Origin and destination must be different.");
            return;
        }
        if (!departureDate) {
            setError("Please select a departure date.");
            return;
        }

        const query = new URLSearchParams({
            origin,
            destination,
            departure_date: departureDate,
            travel_class: travelClass,
            mode,
        }).toString();

        if (!isAuthenticated) {
            navigate("/login", { state: { redirectTo: `/search-results?${query}` } });
            return;
        }

        navigate(`/search-results?${query}`);
    }

    return (
        <div className="home-page">
            <div className="home-hero">
                <h1>Fly anywhere in India.</h1>
                <p>Search, compare, and book domestic flights in seconds.</p>
            </div>

            <form className="home-search-card" onSubmit={handleSearch}>
                <div className="home-search-row">
                    <AirportSelect
                        label="From"
                        airports={airports}
                        value={origin}
                        onChange={setOrigin}
                        excludeCode={destination}
                    />
                    <AirportSelect
                        label="To"
                        airports={airports}
                        value={destination}
                        onChange={setDestination}
                        excludeCode={origin}
                    />
                </div>

                <div className="home-search-row">
                    <div className="home-field">
                        <label>Departure date</label>
                        <input
                            type="date"
                            min={today}
                            value={departureDate}
                            onChange={(e) => setDepartureDate(e.target.value)}
                        />
                    </div>

                    <div className="home-field">
                        <label>Travel class</label>
                        <select value={travelClass} onChange={(e) => setTravelClass(e.target.value)}>
                            <option value="economy">Economy</option>
                            <option value="business">Business</option>
                            <option value="first">First</option>
                        </select>
                    </div>

                    <div className="home-field">
                        <label>Sort by</label>
                        <select value={mode} onChange={(e) => setMode(e.target.value)}>
                            <option value="cheapest">Cheapest</option>
                            <option value="fastest">Fastest</option>
                            <option value="balanced">Balanced</option>
                        </select>
                    </div>
                </div>

                {error && <p className="home-search-error">{error}</p>}

                <button type="submit" className="home-search-submit">
                    Search flights
                </button>
            </form>
            <div className="home-features">
                <div className="home-feature">
                    <span className="home-feature-icon">📈</span>
                    <h3>Dynamic pricing</h3>
                    <p>Fares update live based on seat demand and how close you're booking to departure.</p>
                </div>
                <div className="home-feature">
                    <span className="home-feature-icon">🧭</span>
                    <h3>Smart recommendations</h3>
                    <p>Sort by cheapest, fastest, or a balanced mix — scored and ranked for you.</p>
                </div>
                <div className="home-feature">
                    <span className="home-feature-icon">🔒</span>
                    <h3>Real seat availability</h3>
                    <p>Every seat you see is checked live — no overbooking, no surprises at payment.</p>
                </div>
            </div>

            {popularRoutes.length > 0 && (
                <div className="home-popular">
                    <h2>Popular routes</h2>
                    <div className="home-popular-grid">
                        {popularRoutes.map((route) => (
                            <button
                                type="button"
                                key={`${route.from}-${route.to}`}
                                className="home-popular-card"
                                onClick={() => {
                                    setOrigin(route.from);
                                    setDestination(route.to);
                                }}
                            >
                                <span className="home-popular-cities">
                                    {route.fromCity} <span className="home-popular-arrow">→</span> {route.toCity}
                                </span>
                                <span className="home-popular-codes">
                                    {route.from} · {route.to}
                                </span>
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}