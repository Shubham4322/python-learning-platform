import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getDashboard } from '../services/api';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const data = await getDashboard();
            setDashboardData(data);
        } catch (err) {
            setError('Failed to load dashboard. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="dashboard-loading">
                <p>Loading your dashboard...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="dashboard-error">
                <p>{error}</p>
                <button onClick={fetchDashboard} className="retry-button">
                    Try Again
                </button>
            </div>
        );
    }

    const { user, progress, topics } = dashboardData;

    return (
        <div className="dashboard-page">
            <div className="dashboard-container">
                {/* Welcome Section */}
                <section className="welcome-section">
                    <h1>Welcome back, {user.username}! 👋</h1>
                    <p>Continue your Python learning journey</p>
                </section>

                {/* Progress Section */}
                <section className="progress-section">
                    <h2>Your Progress</h2>
                    <div className="progress-cards">
                        <div className="progress-card">
                            <div className="progress-number">
                                {progress.completed_topics}/{progress.total_topics}
                            </div>
                            <div className="progress-label">Topics Completed</div>
                        </div>
                        <div className="progress-card">
                            <div className="progress-number">
                                {progress.completed_questions}/{progress.total_questions}
                            </div>
                            <div className="progress-label">Questions Solved</div>
                        </div>
                        <div className="progress-card">
                            <div className="progress-number">
                                {progress.total_questions > 0 
                                    ? Math.round((progress.completed_questions / progress.total_questions) * 100)
                                    : 0}%
                            </div>
                            <div className="progress-label">Overall Progress</div>
                        </div>
                    </div>
                </section>

                {/* Topics Section */}
                <section className="topics-section">
                    <div className="topics-header">
                        <h2>Learning Topics</h2>
                        {topics.length > 0 && topics[0].is_unlocked && (
                            <Link to={`/topic/${topics[0].id}`} className="start-learning-btn">
                                Start Learning
                            </Link>
                        )}
                    </div>

                    <div className="topics-list">
                        {topics.map((topic, index) => (
                            <div 
                                key={topic.id} 
                                className={`topic-card ${topic.is_unlocked ? 'unlocked' : 'locked'} ${topic.is_completed ? 'completed' : ''}`}
                            >
                                <div className="topic-status">
                                    {topic.is_completed ? (
                                        <span className="status-icon completed">✓</span>
                                    ) : topic.is_unlocked ? (
                                        <span className="status-icon unlocked">📖</span>
                                    ) : (
                                        <span className="status-icon locked">🔒</span>
                                    )}
                                </div>

                                <div className="topic-info">
                                    <h3 className="topic-title">
                                        Topic {index + 1}: {topic.title}
                                    </h3>
                                    <p className="topic-description">{topic.description}</p>
                                    <div className="topic-progress">
                                        <span>{topic.completed_count}/{topic.questions_count} questions</span>
                                    </div>
                                </div>

                                <div className="topic-action">
                                    {topic.is_unlocked ? (
                                        <Link to={`/topic/${topic.id}`} className="topic-button">
                                            {topic.is_completed ? 'Review' : 'Continue'}
                                        </Link>
                                    ) : (
                                        <span className="topic-locked-text">Locked</span>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>

                    {topics.length === 0 && (
                        <div className="no-topics">
                            <p>No topics available yet. Check back soon!</p>
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
};

export default Dashboard;