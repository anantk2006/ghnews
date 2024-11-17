import './App.css';
import { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './Register';
import Landing from './Landing';

function App() {
    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://apis.google.com/js/platform.js';
        script.async = true;
        document.body.appendChild(script);
    }, []);



    return (
        <Router>
            <Routes>
                <Route path="/register/" element={<Register />} />
                <Route
                    path="/"
                    element={
                        <Landing/>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
