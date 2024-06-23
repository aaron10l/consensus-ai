import React, { useState, useEffect, useRef } from 'react';
import './TextBox.css';

const TextBox = ({ chatHistory, setChatHistory }) => {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');
    const chatHistoryRef = useRef(null);

    useEffect(() => {
        if (chatHistoryRef.current) {
            chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
        }
    }, [chatHistory]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await fetch('http://localhost:5000/get-responses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });
        const data = await res.json();
        const newResponse = `${data.response}`;

        setChatHistory([...chatHistory, { role: 'user', content: prompt }, { role: 'assistant', content: newResponse }]);
        setResponse(newResponse);
        setPrompt('');
    };

    return (
        <div className="textbox-container">
            <div className="chat-history" ref={chatHistoryRef}>
                {chatHistory.map((message, index) => (
                    <div key={index} className={`message ${message.role}`}>
                        <p>{message.content}</p>
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit} className="textbox-form">
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Enter your prompt"
                    className="textbox-input"
                />
                <button type="submit" className="textbox-button">Submit</button>
            </form>
        </div>
    );
};

export default TextBox;