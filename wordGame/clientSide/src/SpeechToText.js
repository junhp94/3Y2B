import React, { useState } from 'react';
import axios from 'axios';

const SpeechToText = () => {
  const [listening, setListening] = useState(false);
  const [firstWord, setFirstWord] = useState('');
  const [spokenWords, setSpokenWords] = useState([]);

  const startListening = () => {
    setListening(true);
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = (event) => {
      const spokenWord = event.results[0][0].transcript.trim();
      const words = spokenWord.split(' ');
      if (words.length > 0) {
        const first = words[0];
        setFirstWord(first);
        setSpokenWords(prevSpokenWords => [...prevSpokenWords, first]);
        sendWordToBackend(first); // Send the word to backend
        setListening(false); 
        recognition.stop();
      }
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setListening(false);
    };
  };

  const sendWordToBackend = async (word) => {
    try {
      await axios.post('http://127.0.0.1:5000/add_member', { username: word });
      console.log('Word sent to backend:', word);
    } catch (error) {
      console.error('Error sending word to backend:', error);
    }
  };

  return (
    <div>
      <h1>Speech to Text</h1>
      <button onClick={startListening} disabled={listening}>
        {listening ? 'Listening...' : 'Start Speaking (3 seconds)'}
      </button>
      <h2>First Word:</h2>
      <p>{firstWord !== '' ? firstWord : 'No word spoken yet'}</p>
      <h2>Spoken Words:</h2>
      <ul>
        {spokenWords.map((word, index) => (
          <li key={index}>{word}</li>
        ))}
      </ul>
    </div>
  );
};

export default SpeechToText;
