import './App.css';
import { HomePage } from './pages/HomePage';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Lobby } from './pages/Lobby';

function App() {
  return (
    <div className="App">
    <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/lobby" element={<Lobby />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
