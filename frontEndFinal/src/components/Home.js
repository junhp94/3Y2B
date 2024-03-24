import React, { useState, useEffect } from "react";

export const Home = () => {
    const [playerId, setPlayerId] = useState('');

    const handlePlayerIdChange = event => {
        setPlayerId(event.target.value.trim());
    };

    const sendPlayerId = () => {
        // Check if playerId is not empty before sending
        if (playerId.trim() !== '') {
            fetch('http://207.23.187.236:5555/adduser', {
                method: 'POST',
                body: JSON.stringify({ playerId }), // Corrected to playerId instead of username
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Server response:', data);
            })
            .catch(error => console.error('Error:', error));
        } else {
            console.error('Player ID is required');
        }
    };

    // useEffect(() => {
    //     sendPlayerId();
    // }, [playerId]);

    return (
        <div>
            <input 
                type="text" 
                id="playerId"
                placeholder="Enter Player ID or Name" 
                value={playerId} 
                onChange={handlePlayerIdChange} 
            />
            <button onClick={sendPlayerId}>Register</button>
        </div>
    );
};
