export default function AdminDashboard() {
    return(
        <div style={{"color" : "white"}}>
            <h1>Admin Dashboard</h1>
            <p>
                The backend fully implements admin capabilities — flight CRUD, airport CRUD, automatic seat generation — all protected by role-based JWT authentication (see api/flights.py, api/airports.py, and the get_current_admin dependency). This was a deliberate architectural decision made before frontend development began: the primary engineering value of this project is in the customer booking flow — Redis-based concurrent seat locking, dynamic pricing, a weighted recommendation engine, and a retry-safe payment state machine. Building a full admin UI on top of an already-complete admin API would have added development time without adding new backend complexity to demonstrate. The admin dashboard route exists and is protected by role, but currently shows a placeholder rather than functional screens.
            </p>
        </div>
    )
}