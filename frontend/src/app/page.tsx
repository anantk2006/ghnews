"use client";
import Navbar from "./components/navbar";
import Footer from "./sections/footer";
import Hero from "./sections/hero";
import Pricing from "./sections/pricing";
import { useState } from "react";
import CheckoutForm from "./components/checkoutform";

export default function Home() {
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const openModal = () => {
        console.log("Opening modal");
        setIsModalOpen(true);
    }
    const closeModal = () => setIsModalOpen(false);
  return (
    <div>
      <Navbar openModal={openModal} />
      <Hero />
      <Pricing />
      <Footer />
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
