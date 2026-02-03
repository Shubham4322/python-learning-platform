import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getTopic, getTopics } from '../services/api';
import Sidebar from '../components/Sidebar';

const Topic = () => {
    const { topicId } = useParams();
    const [topic, setTopic] = useState(null);
    const [allTopics, setAllTopics] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchData();
    }, [topicId]);

    const fetchData = async () => {
        setLoading(true);
        setError('');
        try {
            // Fetch current topic and all topics
            const [topicData, topicsData] = await Promise.all([
                getTopic(topicId),
                getTopics()
            ]);
            setTopic(topicData);
            setAllTopics(topicsData);
        } catch (err) {
            if (err.response?.status === 403) {
                setError('This topic is locked. Complete previous topics first.');
            } else if (err.response?.status === 404) {
                setError('Topic not found.');
            } else {
                setError('Failed to load topic. Please try again.');
            }
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="topic-loading">
                <p>Loading topic...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="topic-error">
                <div className="error-box">
                    <h2>⚠️ Oops!</h2>
                    <p>{error}</p>
                    <Link to="/dashboard" className="back-button">
                        Back to Dashboard
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="topic-page">
            {/* Sidebar */}
            <Sidebar topics={allTopics} />

            {/* Main Content */}
            <div className="topic-content">
                {/* Topic Header */}
                <div className="topic-header">
                    <Link to="/dashboard" className="breadcrumb">
                        ← Back to Dashboard
                    </Link>
                    <h1 className="topic-title">{topic.title}</h1>
                    <p className="topic-description">{topic.description}</p>
                </div>

                {/* Theory Section */}
                <div className="theory-section">
                    <h2>📚 Theory</h2>
                    <div className="theory-content">
                        {topic.theory.split('\n').map((paragraph, index) => (
                            <p key={index}>{paragraph}</p>
                        ))}
                    </div>
                </div>

                {/* Instructions */}
                <div className="instructions">
                    <p>📝 Read the theory above, then solve the questions below to complete this topic.</p>
                </div>

                {/* Questions Section */}
                <div className="questions-section">
                    <h2>💻 Practice Questions</h2>
                    
                    {topic.questions.length > 0 ? (
                        <div className="questions-list">
                            {topic.questions.map((question, index) => (
                                <div 
                                    key={question.id} 
                                    className={`question-card ${question.is_completed ? 'completed' : ''}`}
                                >
                                    <div className="question-status">
                                        {question.is_completed ? (
                                            <span className="status-badge completed">✓ Solved</span>
                                        ) : (
                                            <span className="status-badge pending">Pending</span>
                                        )}
                                    </div>
                                    <div className="question-info">
                                        <h3>Question {index + 1}: {question.title}</h3>
                                        <p>{question.description}</p>
                                    </div>
                                    <div className="question-action">
                                        <Link 
                                            to={`/question/${question.id}`} 
                                            className={`solve-button ${question.is_completed ? 'review' : ''}`}
                                        >
                                            {question.is_completed ? 'Review' : 'Solve'}
                                        </Link>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="no-questions">
                            <p>No questions available for this topic yet.</p>
                        </div>
                    )}
                </div>

                {/* Topic Progress */}
                <div className="topic-footer">
                    <div className="topic-progress-bar">
                        <div className="progress-info">
                            <span>Progress: {topic.questions.filter(q => q.is_completed).length}/{topic.questions.length} questions completed</span>
                        </div>
                        <div className="progress-bar-bg">
                            <div 
                                className="progress-bar-fill" 
                                style={{ 
                                    width: `${topic.questions.length > 0 
                                        ? (topic.questions.filter(q => q.is_completed).length / topic.questions.length) * 100 
                                        : 0}%` 
                                }}
                            ></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Topic;