import React, { useState, useEffect, useRef } from 'react';
import './TextBox.css';

const TextBox = ({ chatHistory, setChatHistory }) => {
    const [prompt, setPrompt] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const chatHistoryRef = useRef(null);

    useEffect(() => {
        if (chatHistoryRef.current) {
            chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
        }
    }, [chatHistory]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!prompt.trim() || isLoading) return;
        
        setIsLoading(true);
        try {
            const res = await fetch('http://localhost:5000/get-responses', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });
            const data = await res.json();
            setChatHistory([
                ...chatHistory, 
                { role: 'user', content: prompt }, 
                { role: 'assistant', content: data.response, winner: data.winner }
            ]);
            setPrompt('');
        } catch (error) {
            console.error('Error:', error);
            // Optionally, you can add error handling here
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <div className="textbox-container">
            <div className="chat-history" ref={chatHistoryRef}>
                {chatHistory.length === 0 ? (
                    <div className="message system">
                        <p>What consensus can we draw today?</p>
                    </div>
                ) : (
                    chatHistory.map((message, index) => (
                        <div key={index} className={`message ${message.role}`}>
                            {message.role === 'assistant' && (
                                <div className="winner-model">{message.winner}</div>
                            )}
                            <p>{message.content}</p>
                        </div>
                    ))
                )}
            </div>
            <form onSubmit={handleSubmit} className="textbox-form">
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Message consensus.ai"
                    className="textbox-input"
                    disabled={isLoading}
                />
                <button type="submit" className="textbox-button" disabled={isLoading}>
                    {isLoading ? (
                        <>
                            <div className="loading-circle"></div>
                        </>
                    ) : (
                        'Submit'
                    )}
                </button>
            </form>
        </div>
    );
};

export default TextBox;




