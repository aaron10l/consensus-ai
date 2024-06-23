import React, { useState } from 'react';
import './TextBox.css'; // Import the CSS file for styling

const TextBox = () => {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');

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
        setResponse(`Winner: ${data.winner}\nResponse: ${data.response}`);
    };

    return (
        <div className="textbox-container">
            <form onSubmit={handleSubmit}>
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Enter your prompt"
                    className="textbox-input"
                />
                <button type="submit" className="textbox-button">Submit</button>
            </form>
            <div className="response-container">
                <h2>Response:</h2>
                <p>{response}</p>
            </div>
        </div>
    );
};

export default TextBox;
