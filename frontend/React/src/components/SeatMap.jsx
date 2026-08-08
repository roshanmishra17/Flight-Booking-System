import "../CSS/SeatMap.css";

export default function SeatMap({
    seats,
    selectedSeatId,
    onSelect,
}) {

    const groupedByClass = {
        business: {},
        economy: {},
    };

    seats.forEach((seat) => {
        const row = parseInt(
            seat.seat_number.match(/\d+/)?.[0] ?? "0",
            10
        );

        const seatClass = seat.seat_class.toLowerCase();

        if (!groupedByClass[seatClass][row]) {
            groupedByClass[seatClass][row] = [];
        }

        groupedByClass[seatClass][row].push(seat);
    });

    return (
        <div className="seat-map">

            <div className="aircraft-front">
                ✈ FRONT
            </div>

            <Legend />


            <div className="seat-map-scrollable">

                <SeatSection
                    title="Business Class"
                    rows={groupedByClass.business}
                    selectedSeatId={selectedSeatId}
                    onSelect={onSelect}
                />

                <SeatSection
                    title="Economy Class"
                    rows={groupedByClass.economy}
                    selectedSeatId={selectedSeatId}
                    onSelect={onSelect}
                />
                
            </div>

        </div>
    );
}

function SeatSection({
    title,
    rows,
    selectedSeatId,
    onSelect,
}) {

    const rowNumbers = Object.keys(rows)
        .map(Number)
        .sort((a, b) => a - b);

    if (rowNumbers.length === 0) return null;

    return (
        <div className="seat-section">

            <h3>{title}</h3>

            {rowNumbers.map((row) => {

                const rowSeats = [...rows[row]].sort((a, b) =>
                    a.seat_number.localeCompare(b.seat_number)
                );

                const mid = Math.ceil(rowSeats.length / 2);
                const leftSeats = rowSeats.slice(0, mid);
                const rightSeats = rowSeats.slice(mid);

                return (

                    <div
                        key={row}
                        className="seat-row"
                    >

                        <span className="row-number">
                            {row}
                        </span>

                        <div className="seat-group">

                            {leftSeats.map((seat) => (
                                <SeatButton
                                    key={seat.id}
                                    seat={seat}
                                    selected={
                                        seat.id === selectedSeatId
                                    }
                                    onSelect={onSelect}
                                />
                            ))}

                        </div>

                        <div className="aircraft-aisle" />

                        <div className="seat-group">

                            {rightSeats.map((seat) => (
                                <SeatButton
                                    key={seat.id}
                                    seat={seat}
                                    selected={
                                        seat.id === selectedSeatId
                                    }
                                    onSelect={onSelect}
                                />
                            ))}

                        </div>

                    </div>

                );
            })}
        </div>
    );
}

function SeatButton({
    seat,
    selected,
    onSelect,
}) {

    const unavailable =
        seat.availability !== "available";

    const classes = [
        "seat",
        `seat-${seat.seat_class}`,
        unavailable
            ? "seat-booked"
            : selected
                ? "seat-selected"
                : "seat-available",
    ].join(" ");

    return (

        <button
            className={classes}
            disabled={unavailable}
            onClick={() => onSelect(seat)}
            title={
                `${seat.seat_number}
                ${seat.seat_position}
                ${seat.seat_class}
                x${seat.price_multiplier}`
            }
        >

            {seat.seat_number.replace(/^\d+/, "")}

        </button>

    );
}

function Legend() {

    return (

        <div className="seat-legend">

            <LegendItem
                color="seat-available"
                label="Available"
            />

            <LegendItem
                color="seat-selected"
                label="Selected"
            />

            <LegendItem
                color="seat-booked"
                label="Booked"
            />

        </div>

    );
}

function LegendItem({
    color,
    label,
}) {

    return (

        <div className="legend-item">

            <span
                className={`legend-box ${color}`}
            />

            {label}

        </div>

    );
}