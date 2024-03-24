import React, { useState, useEffect, useRef } from 'react';

const VoiceInputClient = () => {
    const [streaming, setStreaming] = useState(false);
    const [playerId, setPlayerId] = useState('');
    const recognition = useRef(null); // Use useRef for persistence across renders

    const [currentUsers, setCurrentUsers] = useState([]);

    useEffect(() => {
        fetchCurrentUsers();
    }, [currentUsers]);

    const fetchCurrentUsers = () => {
        fetch('http://207.23.187.236:5555/current_users')
            .then(response => response.json())
            .then(data => {
                setCurrentUsers(data.current_users);
            })
            .catch(error => console.error('Error:', error));
    };

    

    useEffect(() => {
        recognition.current = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
        recognition.current.lang = 'en-US';
        recognition.current.continuous = true;
        recognition.current.interimResults = false;

        recognition.current.onresult = event => {
            const transcript = event.results[event.results.length - 1][0].transcript;
            console.log('Player ID:', playerId);
            console.log('Transcript:', transcript);
            sendVoiceInput(playerId, transcript);
        };

        recognition.current.onerror = event => {
            console.error('Speech recognition error:', event.error);
        };

        return () => {
            if (recognition.current) {
                recognition.current.stop();
            }
        };
    }, [playerId]);

    const startRecording = () => {
        if (!streaming && recognition.current) {
            recognition.current.start();
            setStreaming(true);
            console.log('Recording started');
        }
    };

    const stopRecording = () => {
        if (streaming && recognition.current) {
            recognition.current.stop();
            setStreaming(false);
            console.log('Recording stopped');
        }
    };

    const handlePlayerIdChange = event => {
        setPlayerId(event.target.value.trim());
    };

    const sendVoiceInput = (playerId, voiceInput) => {
        fetch('http://207.23.187.236:5555', {
            method: 'POST',
            body: JSON.stringify({ playerId, voiceInput }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => console.error('Error:', error));
    };

    return (
        <div>
            <input 
                type="text" 
                id="playerId"
                placeholder="Enter Player ID or Name" 
                value={playerId} 
                onChange={handlePlayerIdChange} 
            />
            <button onClick={startRecording}>Start Recording</button>
            <button onClick={stopRecording}>Stop Recording</button>


            <div>
                <h2>Current Users:</h2>
                <ul>
                    {currentUsers.map((user, index) => (
                        <li key={index}>{user}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default VoiceInputClient;
