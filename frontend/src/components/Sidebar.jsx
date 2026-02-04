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
                        className={`sidebar-item ${topic.id === currentTopicId ? 'active' : ''}`}
                    >
                        <Link to={`/topic/${topic.id}`} className="sidebar-link">
                            <span className="sidebar-icon">
                                {topic.is_completed ? '✓' : '📖'}
                            </span>
                            <span className="sidebar-text">
                                {index + 1}. {topic.title}
                            </span>
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;