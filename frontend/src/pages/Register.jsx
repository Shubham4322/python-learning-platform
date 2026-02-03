import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { registerUser } from '../services/api';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        password2: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
        if (error) setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        if (!formData.username || !formData.email || !formData.password || !formData.password2) {
            setError('Please fill in all fields');
            setLoading(false);
            return;
        }

        if (formData.password !== formData.password2) {
            setError('Passwords do not match');
            setLoading(false);
            return;
        }

        if (formData.password.length < 6) {
            setError('Password must be at least 6 characters');
            setLoading(false);
            return;
        }

        try {
            const response = await registerUser({
                username: formData.username,
                email: formData.email,
                password: formData.password,
                password2: formData.password2,
            });

            login(response.user, response.tokens);
            navigate('/dashboard');
        } catch (err) {
            if (err.response?.data) {
                const errors = err.response.data;
                if (errors.username) {
                    setError(errors.username[0]);
                } else if (errors.email) {
                    setError(errors.email[0]);
                } else if (errors.password) {
                    setError(errors.password[0]);
                } else {
                    setError('Registration failed. Please try again.');
                }
            } else {
                setError('Something went wrong. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-container">
                <div className="auth-box">
                    <h1 className="auth-title">Create Account</h1>
                    <p className="auth-subtitle">Join PyLearn and start your Python journey</p>

                    {error && <div className="auth-error">{error}</div>}

                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label htmlFor="username">Username</label>
                            <input
                                type="text"
                                id="username"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                placeholder="Choose a username"
                                disabled={loading}
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="Enter your email"
                                disabled={loading}
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Create a password (min 6 characters)"
                                disabled={loading}
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password2">Confirm Password</label>
                            <input
                                type="password"
                                id="password2"
                                name="password2"
                                value={formData.password2}
                                onChange={handleChange}
                                placeholder="Confirm your password"
                                disabled={loading}
                            />
                        </div>

                        <button 
                            type="submit" 
                            className="auth-button"
                            disabled={loading}
                        >
                            {loading ? 'Creating Account...' : 'Create Account'}
                        </button>
                    </form>

                    <p className="auth-footer">
                        Already have an account?{' '}
                        <Link to="/login" className="auth-link">
                            Login here
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Register;