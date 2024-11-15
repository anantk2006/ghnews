// MyComponent.js
import React from 'react';
import { useLocation } from 'react-router-dom';

function Register() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const paramValue = queryParams.get('code'); // This will get 'sgdgdes'

  return (
    <div>
      <h1>Query Parameter Value</h1>
      <p>param = {paramValue}</p>
    </div>
  );
}

export default Register;
