import React from 'react';
import './NavBar.css';
const NavBar = ({ modal }) => {
    return (
        <nav className="navbar">
            <div className="navbar-logo">
                <img src="logo.png" alt="Logo" />
            </div>
            <h2>Virsitile</h2>
            <div className="navbar-links">
                <button onClick={modal} className="github-button-nav">
                    <img src="/github-logo.svg" alt="GitHub Logo" className="github-logo" />
                    <p>Subscribe</p>
                </button>
            </div>
        </nav>
    );
};

export default NavBar;