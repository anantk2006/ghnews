"use client";
import Navbar from "./components/navbar";
import Footer from "./sections/footer";
import Hero from "./sections/hero";
import { NewsMarquee } from "./sections/news-marquee";
import Pricing from "./sections/pricing";
import { useState } from "react";
import Headlines from "./sections/headlines";

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
      <Navbar openModal={openModal} home={true} />
      <Hero
        isModalOpen={isModalOpen}
        closeModal={closeModal}
        openModal={openModal}
      />
      <NewsMarquee />
      <Pricing openModal={openModal} />

      <Footer />
    </div>
  );
}

