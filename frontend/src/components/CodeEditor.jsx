const CodeEditor = ({ value, onChange, disabled }) => {
    const handleKeyDown = (e) => {
        // Handle Tab key for indentation
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = e.target.selectionStart;
            const end = e.target.selectionEnd;
            const newValue = value.substring(0, start) + '    ' + value.substring(end);
            onChange(newValue);
            // Set cursor position after the tab
            setTimeout(() => {
                e.target.selectionStart = e.target.selectionEnd = start + 4;
            }, 0);
        }
    };

    return (
        <div className="code-editor">
            <div className="code-editor-header">
                <span className="editor-dot red"></span>
                <span className="editor-dot yellow"></span>
                <span className="editor-dot green"></span>
                <span className="editor-title">Python Code</span>
            </div>
            <div className="code-editor-body">
                <div className="line-numbers">
                    {value.split('\n').map((_, index) => (
                        <span key={index}>{index + 1}</span>
                    ))}
                </div>
                <textarea
                    className="code-textarea"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="# Write your Python code here..."
                    spellCheck="false"
                    disabled={disabled}
                />
            </div>
        </div>
    );
};

export default CodeEditor;