import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const { isAuthenticated, user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    🐍 PyLearn
                </Link>

                <div className="navbar-links">
                    <Link to="/" className="nav-link">Home</Link>
                    
                    {isAuthenticated ? (
                        <>
                            <Link to="/dashboard" className="nav-link">Dashboard</Link>
                            <span className="nav-user">Hello, {user?.username}</span>
                            <button onClick={handleLogout} className="nav-button logout-btn">
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="nav-link">Login</Link>
                            <Link to="/register" className="nav-button">Register</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;