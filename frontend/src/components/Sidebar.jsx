import { Link, useParams } from 'react-router-dom';

const Sidebar = ({ topics }) => {
    const { topicId } = useParams();
    const currentTopicId = parseInt(topicId);

    return (
        <div className="sidebar">
            <h3 className="sidebar-title">All Topics</h3>
            <ul className="sidebar-list">
                {topics.map((topic, index) => (
                    <li 
                        key={topic.id} 
                        className={`sidebar-item ${topic.id === currentTopicId ? 'active' : ''} ${!topic.is_unlocked ? 'locked' : ''}`}
                    >
                        {topic.is_unlocked ? (
                            <Link to={`/topic/${topic.id}`} className="sidebar-link">
                                <span className="sidebar-icon">
                                    {topic.is_completed ? '✓' : topic.id === currentTopicId ? '📖' : '○'}
                                </span>
                                <span className="sidebar-text">
                                    {index + 1}. {topic.title}
                                </span>
                            </Link>
                        ) : (
                            <div className="sidebar-link disabled">
                                <span className="sidebar-icon">🔒</span>
                                <span className="sidebar-text">
                                    {index + 1}. {topic.title}
                                </span>
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;