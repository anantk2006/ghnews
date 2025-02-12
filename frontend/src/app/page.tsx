"use client";
import Navbar from "./components/navbar";
import Footer from "./sections/footer";
import Hero from "./sections/hero";
import Pricing from "./sections/pricing";
import { useState } from "react";

export const useModal = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
  
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);
  
    return { isModalOpen, openModal, closeModal };
  };

export default function Home() {
    const { isModalOpen, openModal, closeModal } = useModal();
  return (
    <div>
      <Navbar openModal={openModal} />
      <Hero isModalOpen={isModalOpen} closeModal={closeModal} openModal={openModal} />
      <Pricing openModal={openModal} />
      <Footer />
    </div>

  );
}



