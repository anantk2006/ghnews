"use client";

import { ArrowRightIcon } from "lucide-react";

import { cn } from "@/lib/utils";

import { InteractiveGridPattern } from "../components/magic-background-grid";
import { AnimatedShinyText } from "../components/magic-shiny-text";
import Link from "next/link";
import { motion } from "framer-motion";
import CheckoutForm from "../components/checkoutform";

import "./modal.css";

export default function Hero({
  isModalOpen,
  closeModal,
  openModal,
}: {
  isModalOpen: boolean;
  closeModal: () => void;
  openModal: () => void;
}) {
  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      <div className="flex items-center justify-center h-screen">
        <div className="flex flex-col items-center justify-center px-44 gap-2 z-[99]">
          <motion.div
            initial={{ opacity: 0, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className={cn(
              "group rounded-full border bg-white border-black/10 text-base text-black transition-all ease-in hover:cursor-pointer hover:bg-neutral-200 dark:border-white/5 dark:bg-neutral-900 dark:hover:bg-neutral-800 mb-4",
            )}
          >
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
            
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="text-7xl font-oddlini text-center leading-[1.25]"
          >
            The tech news you need, <br /> made{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-violet-500 to-pink-500">
              simple.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="text-xl font-hanken text-center text-neutral-600 w-3/4"
          >
            The modern standard for staying up-to-date with everything tech.{" "}
            <br />
            Simple, personalized, and uniquely yours.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="flex items-center justify-center mt-5"
          >
            <button
              onClick={openModal}
              className="text-sm font-medium bg-foreground text-background px-4 py-2 pt-2.5 rounded-lg flex items-center justify-center font-oddlini hover:bg-foreground/80"
            >
              Get Started for Free
              <ArrowRightIcon className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
            </button>
          </motion.div>
        </div>
      </div>

      {/* Arc background */}
      
    </div>
  );
}
