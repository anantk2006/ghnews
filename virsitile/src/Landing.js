import React from 'react';
import './index.css';

function Landing() {
    const handleGithubLogin = () => {
        window.location.href = 'https://github.com/login/oauth/authorize?client_id=Iv23liyZsfVUeLCoHC5L&scope=repo';
    };

    return (
        <div className="landing-page">
            <header className="hero-section">
                <h1>Virsitile</h1>
                <p>Making sure your tech stack remains state-of-the-art in a fast world.</p>
                <button onClick={handleGithubLogin} className="github-button">
                    <img src="/github-logo.svg" alt="GitHub Logo" className="github-logo" />
                    <p>Link your GitHub</p>
                </button>
            </header>
        </div>
    );
}

export default Landing;
