import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home = () => {
    const { isAuthenticated } = useAuth();

    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <h1 className="hero-title">
                        Learn Python <span className="highlight">Step by Step</span>
                    </h1>
                    <p className="hero-subtitle">
                        Master Python programming with interactive theory and practice questions.
                        Perfect for beginners who want to learn coding from scratch.
                    </p>
                    
                    {isAuthenticated ? (
                        <Link to="/dashboard" className="hero-button primary">
                            Go to Dashboard
                        </Link>
                    ) : (
                        <div className="hero-buttons">
                            <Link to="/register" className="hero-button primary">
                                Get Started Free
                            </Link>
                            <Link to="/login" className="hero-button secondary">
                                Login
                            </Link>
                        </div>
                    )}
                </div>
                <div className="hero-image">
                    <div className="code-preview">
                        <div className="code-header">
                            <span className="dot red"></span>
                            <span className="dot yellow"></span>
                            <span className="dot green"></span>
                        </div>
                        <pre className="code-body">
{`# Welcome to Python!
print("Hello, World!")

# Variables
name = "PyLearn"
print(f"Welcome to {name}")

# Let's learn together! 🐍`}
                        </pre>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features">
                <h2 className="section-title">Why Learn With Us?</h2>
                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon">📚</div>
                        <h3>Theory First</h3>
                        <p>Read clear explanations before solving problems. Understand concepts deeply.</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">💻</div>
                        <h3>Practice Questions</h3>
                        <p>Solve coding questions directly in your browser. Get instant feedback.</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">🔓</div>
                        <h3>Unlock Topics</h3>
                        <p>Complete questions to unlock new topics. Track your learning progress.</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">🎯</div>
                        <h3>Step by Step</h3>
                        <p>Follow a structured path from basics to advanced concepts.</p>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="how-it-works">
                <h2 className="section-title">How It Works</h2>
                <div className="steps">
                    <div className="step">
                        <div className="step-number">1</div>
                        <h3>Sign Up</h3>
                        <p>Create your free account in seconds</p>
                    </div>
                    <div className="step-arrow">→</div>
                    <div className="step">
                        <div className="step-number">2</div>
                        <h3>Read Theory</h3>
                        <p>Learn concepts with clear explanations</p>
                    </div>
                    <div className="step-arrow">→</div>
                    <div className="step">
                        <div className="step-number">3</div>
                        <h3>Solve Questions</h3>
                        <p>Practice with coding exercises</p>
                    </div>
                    <div className="step-arrow">→</div>
                    <div className="step">
                        <div className="step-number">4</div>
                        <h3>Unlock More</h3>
                        <p>Progress to new topics</p>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta">
                <h2>Ready to Start Learning?</h2>
                <p>Join now and begin your Python journey today!</p>
                {!isAuthenticated && (
                    <Link to="/register" className="cta-button">
                        Start Learning Free
                    </Link>
                )}
            </section>

            {/* Footer */}
            <footer className="footer">
                <p>© 2024 PyLearn - Python Learning Platform</p>
            </footer>
        </div>
    );
};

export default Home;