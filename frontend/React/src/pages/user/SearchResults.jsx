import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";

import { searchFlights, searchFlightsRanked, searchAlternativeRoutes } from "../../api/flightApi";
import FlightCard from "../../components/FlightCard";
import AlternativeRouteCard from "../../components/AlternativeRouteCard";
import "../../CSS/SearchResults.css";

export default function SearchResults() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    const origin = searchParams.get("origin");
    const destination = searchParams.get("destination");
    const departureDate = searchParams.get("departure_date");
    const travelClass = searchParams.get("travel_class");
    const mode = searchParams.get("mode");

    const [flights, setFlights] = useState(null);
    const [recommendations, setRecommendations] = useState(null);
    const [alternatives, setAlternatives] = useState(null);
    const [altLoading, setAltLoading] = useState(false);
    const [altLoaded, setAltLoaded] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!origin || !destination || !departureDate) {
            navigate("/");
            return;
        }

        const params = { origin, destination, departureDate, travelClass, mode };

        setLoading(true);
        setError(null);

        Promise.all([searchFlights(params), searchFlightsRanked(params)])
            .then(([flightsData, rankedData]) => {
                setFlights(flightsData);
                setRecommendations(rankedData);
            })
            .catch(() => setError("Couldn't load results. Please try again."))
            .finally(() => setLoading(false));
    }, [origin, destination, departureDate, travelClass, mode]);

    function loadAlternatives() {
        if (altLoaded || altLoading) return;
        setAltLoading(true);
        searchAlternativeRoutes({ origin, destination, departureDate })
            .then(setAlternatives)
            .catch(() => setAlternatives([]))
            .finally(() => {
                setAltLoading(false);
                setAltLoaded(true);
            });
    }

    if (!origin || !destination) return null;

    return (
        <div className="results-page">
            <div className="results-header">
                <h1>{origin} <span>→</span> {destination}</h1>
                <p>{departureDate}</p>
            </div>

            {loading && <p className="results-status">Loading…</p>}
            {error && <p className="results-status results-error">{error}</p>}

            {!loading && !error && (
                <>
                    <section className="results-section">
                        <h2>⭐ Recommended for you</h2>
                        {recommendations?.length === 0 && <p className="results-empty">No recommendations found.</p>}
                        {recommendations?.map((r) => (
                            <FlightCard
                                key={r.flight.id}
                                flight={r.flight}
                                badge={`#${r.rank_position} · Score ${r.computed_score.toFixed(2)}`}
                            />
                        ))}
                    </section>

                    <section className="results-section">
                        <h2>Direct Flights</h2>
                        {flights?.length === 0 && <p className="results-empty">No direct flights found for this route.</p>}
                        {flights?.map((flight) => <FlightCard key={flight.id} flight={flight} />)}
                    </section>

                    <section className="results-section">
                        <div className="results-section-header">
                            <h2>Alternative Routes</h2>
                            {!altLoaded && !altLoading && (
                                <button className="results-show-alt" onClick={loadAlternatives}>
                                    Show connecting flights
                                </button>
                            )}
                        </div>
                        {altLoading && <p className="results-status">Searching for connections…</p>}
                        {altLoaded && alternatives?.length === 0 && (
                            <p className="results-empty">No connecting routes found.</p>
                        )}
                        {alternatives?.map((route, i) => <AlternativeRouteCard key={i} route={route} />)}
                    </section>
                </>
            )}
        </div>
    );
}