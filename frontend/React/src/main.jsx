import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AuthContext } from './context/AuthContext'

createRoot(document.getElementById('root')).render(
    <BrowserRouter>

        <AuthProvider>

            <App />

        </AuthProvider>

    </BrowserRouter>
)
