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
      <Hero isModalOpen={isModalOpen} closeModal={closeModal} />
      <Pricing />
      <Footer />
    </div>

  );
}
