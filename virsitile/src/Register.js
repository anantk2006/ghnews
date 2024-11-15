// MyComponent.js
import React from 'react';
import { useLocation } from 'react-router-dom';
import './index.css';

function Register() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const paramValue = queryParams.get('code');
    React.useEffect(() => {
        if (paramValue) {
            fetch('http://localhost:3000/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
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
