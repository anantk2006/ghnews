import React from 'react';
import './index.css';
import { useState } from 'react';
import CheckoutForm from './Payment';
import './modal.css'

function Landing() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);


    return (
        <div className="landing-page">
            <header className="hero-section">
                <h1>Virsitile</h1>
                <p>Making sure your tech knowledge remains state-of-the-art in a fast world.</p>
                <button onClick={openModal} className="github-button">
                    <img src="/github-logo.svg" alt="GitHub Logo" className="github-logo" />
                    <p>Subscribe to the newsletter</p>
                </button>
            </header>
            {isModalOpen && (
                <div className="modal-overlay" onClick={closeModal}>
                <div
                    className="modal-content"
                    onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside modal
                >
                    <button className="close-modal-button" onClick={closeModal}>
                    &times;
                    </button>
                    <CheckoutForm />
                </div>
                </div>
            )}
        </div>
    );
}

export default Landing;
