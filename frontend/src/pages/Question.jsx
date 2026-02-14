import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getQuestion, runCode, submitCode, getTopics } from '../services/api';
import CodeEditor from '../components/CodeEditor';
import Sidebar from '../components/Sidebar';

const Question = () => {
    const { questionId } = useParams();
    const navigate = useNavigate();
    
    const [question, setQuestion] = useState(null);
    const [allTopics, setAllTopics] = useState([]);
    const [code, setCode] = useState('');
    const [output, setOutput] = useState('');
    const [loading, setLoading] = useState(true);
    const [running, setRunning] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchData();
    }, [questionId]);

    const fetchData = async () => {
        setLoading(true);
        setError('');
        setResult(null);
        setOutput('');
        try {
            const [questionData, topicsData] = await Promise.all([
                getQuestion(questionId),
                getTopics()
            ]);
            setQuestion(questionData);
            setAllTopics(topicsData);
            
            // Load saved code if exists, otherwise use default
            if (questionData.submitted_code && questionData.submitted_code.trim()) {
                setCode(questionData.submitted_code);
            } else {
                setCode('# Write your Python code here\n\n');
            }
        } catch (err) {
            if (err.response?.status === 403) {
                setError('This topic is locked. Complete previous topics first.');
            } else if (err.response?.status === 404) {
                setError('Question not found.');
            } else {
                setError('Failed to load question. Please try again.');
            }
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleRun = async () => {
        if (!code.trim() || code.trim() === '# Write your Python code here') {
            setOutput('Error: Please write some code first.');
            return;
        }

        setRunning(true);
        setOutput('');
        setResult(null);

        try {
            const response = await runCode(code);
            if (response.error) {
                setOutput(`Error:\n${response.error}`);
            } else {
                setOutput(response.output || '(No output)');
            }
        } catch (err) {
            setOutput('Error: Failed to run code. Please check your connection and try again.');
            console.error('Run code error:', err);
        } finally {
            setRunning(false);
        }
    };

    const handleSubmit = async () => {
        if (!code.trim() || code.trim() === '# Write your Python code here') {
            setOutput('Error: Please write some code first.');
            return;
        }

        setSubmitting(true);
        setOutput('');
        setResult(null);

        try {
            const response = await submitCode(questionId, code);
            setResult(response);
            setOutput(response.output || '(No output)');
            
            // Refresh question data to update attempts count
            if (response.passed) {
                const updatedQuestion = await getQuestion(questionId);
                setQuestion(updatedQuestion);
            }
        } catch (err) {
            setOutput('Error: Failed to submit code. Please check your connection and try again.');
            console.error('Submit error:', err);
        } finally {
            setSubmitting(false);
        }
    };

    const handleNextQuestion = () => {
        // Navigate to the topic page
        navigate(`/topic/${question.topic}`);
    };

    const handleReset = () => {
        setCode('# Write your Python code here\n\n');
        setOutput('');
        setResult(null);
    };

    if (loading) {
        return (
            <div className="question-loading">
                <p>Loading question...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="question-error">
                <div className="error-box">
                    <h2>🔒 Topic Locked</h2>
                    <p>{error}</p>
                    <Link to="/dashboard" className="back-button">
                        Back to Dashboard
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="question-page">
            {/* Sidebar */}
            <Sidebar topics={allTopics} />

            {/* Main Content */}
            <div className="question-content">
                {/* Question Header */}
                <div className="question-header">
                    <Link to={`/topic/${question.topic}`} className="breadcrumb">
                        ← Back to {question.topic_title}
                    </Link>
                    <h1 className="question-title">{question.title}</h1>
                    <div className="question-meta">
                        {question.is_completed && (
                            <span className="completed-badge">✓ Completed</span>
                        )}
                        {question.attempts > 0 && (
                            <span className="attempts-badge">
                                Attempts: {question.attempts}
                            </span>
                        )}
                    </div>
                </div>

                {/* Question Description */}
                <div className="question-description">
                    <h2>📋 Problem Description</h2>
                    <div 
                        className="description-content"
                        dangerouslySetInnerHTML={{ __html: question.description }}
                    />
                </div>

                {/* Hint if available */}
                {question.hint && (
                    <div className="hint-box">
                        <h3>💡 Hint</h3>
                        <p>{question.hint}</p>
                    </div>
                )}

                {/* Expected Output */}
                <div className="expected-output-hint">
                    <h3>Expected Output:</h3>
                    <pre>{question.expected_output}</pre>
                </div>

                {/* Code Editor */}
                <div className="editor-section">
                    <div className="editor-header">
                        <h2>💻 Your Code</h2>
                        <button 
                            className="reset-button"
                            onClick={handleReset}
                            disabled={running || submitting}
                        >
                            🔄 Reset Code
                        </button>
                    </div>
                    <CodeEditor 
                        value={code} 
                        onChange={setCode}
                        disabled={running || submitting}
                    />

                    {/* Buttons */}
                    <div className="editor-buttons">
                        <button 
                            className="run-button"
                            onClick={handleRun}
                            disabled={running || submitting}
                        >
                            {running ? '⏳ Running...' : '▶ Run Code'}
                        </button>
                        <button 
                            className="submit-button"
                            onClick={handleSubmit}
                            disabled={running || submitting}
                        >
                            {submitting ? '⏳ Checking...' : '✓ Submit'}
                        </button>
                    </div>
                </div>

                {/* Output Section */}
                <div className="output-section">
                    <h2>📤 Output</h2>
                    <div className="output-box">
                        {output ? (
                            <pre>{output}</pre>
                        ) : (
                            <p className="output-placeholder">
                                Run your code to see the output here...
                            </p>
                        )}
                    </div>
                </div>

                {/* Result Section */}
                {result && (
                    <div className={`result-section ${result.passed ? 'passed' : 'failed'}`}>
                        <div className="result-icon">
                            {result.passed ? '🎉' : '❌'}
                        </div>
                        <div className="result-content">
                            <h3>{result.passed ? 'Correct! Well Done!' : 'Not Quite Right'}</h3>
                            <p>{result.message}</p>
                            
                            {result.missing_keywords && result.missing_keywords.length > 0 && (
                                <div className="missing-keywords-warning">
                                    <p>⚠️ Your code must use these keywords:</p>
                                    <ul>
                                        {result.missing_keywords.map((kw, index) => (
                                            <li key={index}><code>{kw}</code></li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                            
                            {result.topic_completed && (
                                <p className="topic-unlock-message">
                                    🎊 Topic Completed! Next topic has been unlocked!
                                </p>
                            )}
                            
                            {!result.passed && !result.missing_keywords && (
                                <div className="result-comparison">
                                    <div className="comparison-item">
                                        <strong>Your Output:</strong>
                                        <pre>{result.output || '(empty)'}</pre>
                                    </div>
                                    <div className="comparison-item">
                                        <strong>Expected Output:</strong>
                                        <pre>{result.expected}</pre>
                                    </div>
                                </div>
                            )}

                            {result.passed && (
                                <button 
                                    className="next-button"
                                    onClick={handleNextQuestion}
                                >
                                    Continue to Topic →
                                </button>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Question;