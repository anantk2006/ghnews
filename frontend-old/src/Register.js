// MyComponent.js
import React from 'react';
import { useLocation } from 'react-router-dom';
import './index.css';

function Register() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const paramValue = queryParams.get('code');
  const session_id = queryParams.get('state');
  const [data, setData] = React.useState(null);
    React.useEffect(() => {
        const abortController = new AbortController();
        const fetchData = async () => {
        
            fetch('http://localhost:8000/api/register', {
                method: 'POST',
                body: JSON.stringify({ code: paramValue, session_id: session_id}),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                setData("Connected!");
            })
            .catch((error) => {
                console.error('Error:', error);
                setData("Error!");
            });         
        }
        fetchData();
        return () => abortController.abort();
    }, [paramValue, session_id]);
  return (
    <div className="landing-page">
    <header className="hero-section">
        <h1>{data}</h1>

    </header>
    </div>
  );
}

export default Register;
