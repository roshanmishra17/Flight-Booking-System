import { useState, useRef, useEffect } from "react";
import "../CSS/AirportSelect.css";

export default function AirportSelect({ label, airports, value, onChange, excludeCode }) {
    const [query, setQuery] = useState("");
    const [open, setOpen] = useState(false);
    const wrapRef = useRef(null);

    useEffect(() => {
        function handleClickOutside(e) {
            if (wrapRef.current && !wrapRef.current.contains(e.target)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const filtered = airports.filter((a) => {
        if (a.iata_code === excludeCode) return false;
        const q = query.toLowerCase();
        return (
            a.iata_code.toLowerCase().includes(q) ||
            a.city.toLowerCase().includes(q) ||
            a.name.toLowerCase().includes(q)
        );
    });

    const selected = airports.find((a) => a.iata_code === value);

    function handleSelect(airport) {
        onChange(airport.iata_code);
        setQuery("");
        setOpen(false);
    }

    return (
        <div className="airport-select" ref={wrapRef}>
            <label>{label}</label>
            <button
                type="button"
                className="airport-select-trigger"
                onClick={() => setOpen((o) => !o)}
            >
                {selected ? (
                    <span>
                        <strong>{selected.iata_code}</strong> — {selected.city}
                    </span>
                ) : (
                    <span className="airport-select-placeholder">Select airport</span>
                )}
            </button>

            {open && (
                <div className="airport-select-panel">
                    <input
                        autoFocus
                        type="text"
                        placeholder="Search city or airport code..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="airport-select-search"
                    />
                    <div className="airport-select-list">
                        {filtered.length === 0 && (
                            <p className="airport-select-empty">No airports found</p>
                        )}
                        {filtered.map((a) => (
                            <button
                                type="button"
                                key={a.id}
                                className="airport-select-option"
                                onClick={() => handleSelect(a)}
                            >
                                <span className="airport-select-code">{a.iata_code}</span>
                                <span className="airport-select-city">{a.city}</span>
                                <span className="airport-select-name">{a.name}</span>
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}