import React from 'react';
import './index.css';
import { useState } from 'react';
import CheckoutForm from './Payment';
import './modal.css'
import NavBar from './NavBar';

function Landing() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);


    return (
        <div>
            <NavBar modal={openModal}/>
        <div className="landing-page">
            
            <header className="hero-section">

                
                <div>
                    <div>
                    <p>
                        There has never been more demand for tech knowledge. New frameworks, languages, models, and APIs are released every day. Additionally, employers in this labor market are looking for candidates with a wide range of skills that can instantly be applied to their projects. This includes everything from the latest AI models, cloud services, and fintech platforms. 
                    </p>
                    <p>
                        Virsitile is a learning platform and newsletter that will send you a. recent tech news and b. the latest important papers in the field. It is just 1.99$ a month--going entirely to the cost of tokens and search APIs (tokens aren't cheap!).
                    </p>

                    </div>


                </div>
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
        </div>
    );
}

export default Landing;
