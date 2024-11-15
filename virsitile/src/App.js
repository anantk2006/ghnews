import './App.css';
import { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './Register';

function App() {
    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://apis.google.com/js/platform.js';
        script.async = true;
        document.body.appendChild(script);
    }, []);

    const handleGithubLogin = () => {
        window.location.href = 'https://github.com/login/oauth/authorize?client_id=Iv23liyZsfVUeLCoHC5L&scope=user';
    };

    return (
        <Router>
            <Routes>
                <Route path="/register/" element={<Register />} />
                <Route
                    path="/"
                    element={
                        <button onClick={handleGithubLogin} style={{ border: 'none', background: 'none' }}>
                            <img src="/github-logo.svg" alt="GitHub Logo" style={{ width: '50px', height: '50px' }} />
                        </button>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
