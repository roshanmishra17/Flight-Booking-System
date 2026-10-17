export function formatTime(isoString) {
    return new Date(isoString).toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
    });
}

export function formatDuration(minutes) {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return `${h}h ${m}m`;
}

export function formatCurrency(amount) {
    return `₹${Number(amount).toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
}

export function formatDate(isoString) {
    return new Date(isoString).toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

export function isSameDay(a, b) {
    return new Date(a).toDateString() === new Date(b).toDateString();
}