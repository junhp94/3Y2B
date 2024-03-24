import React, { useState, useEffect } from 'react';
import './App.css';
import SpeechToText from './SpeechToText';

function App() {
  const [members, setMembers] = useState([]);
  const [username, setUsername] = useState('');

  const fetchMembers = () => {
    fetch('http://127.0.0.1:5000/member')
      .then(response => response.json())
      .then(data => {
        setMembers(data.members);
      })
      .catch(error => console.error('Error fetching data:', error));
  };

  useEffect(() => {
    fetchMembers(); // Fetch members initially
    const interval = setInterval(fetchMembers, 5000); // Poll every 5 seconds
    return () => clearInterval(interval); // Clean up interval on component unmount
  }, []);

  const handleInputChange = (event) => {
    setUsername(event.target.value);
  };

  const handleSubmit = () => {
    // Send the username to the backend
    fetch('http://127.0.0.1:5000/add_member', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username }),
    })
      .then(response => response.json())
      .then(data => {
        // Assuming the backend responds with updated list of members
        setMembers(data.members);
        setUsername(''); // Clear the input field after adding member
      })
      .catch(error => console.error('Error adding member:', error));
  };

  return (
    <div className="App">
      <h1>Members:</h1>
      <ul>
        {members.map((member, index) => (
          <li key={index}>{member}</li>
        ))}
      </ul>
      <input
        type="text"
        value={username}
        onChange={handleInputChange}
        placeholder="Enter username"
      />
      <button onClick={handleSubmit}>Add Member</button>

      <SpeechToText />
    </div>
  );
}

export default App;
