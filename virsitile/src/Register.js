// MyComponent.js
import React from 'react';
import { useLocation } from 'react-router-dom';
import './index.css';

function Register() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const paramValue = queryParams.get('code');
    React.useEffect(() => {
        const abortController = new AbortController();
        const fetchData = async () => {
        
            fetch('http://localhost:8000/api/register', {
                method: 'POST',
                body: JSON.stringify({ code: paramValue }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });         
        }
        fetchData();
        return () => abortController.abort();
    }, [paramValue]);
  return (
    <div className="landing-page">
    <header className="hero-section">
        <h1>Connected!</h1>

    </header>
    </div>
  );
}

export default Register;
