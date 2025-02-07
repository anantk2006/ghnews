"use client"; // Required for using hooks in the App Router

import { useSearchParams } from "next/navigation";
import { useState } from "react";
import Navbar from "../components/navbar";
import Footer from "../sections/footer";
import { ArrowRightIcon } from "lucide-react";
import { AnimatedShinyText } from "../components/magic-shiny-text";
import { InteractiveGridPattern } from "../components/magic-background-grid";
import { motion } from "framer-motion";
import { GridPattern } from "../components/magic-static-grid";
import { useModal } from "../page";
export default function PaidPage() {
    const searchParams = useSearchParams();
    const article_id = searchParams.get("id"); // Access the `id` query parameter
    const { isModalOpen, openModal, closeModal } = useModal();
    const article = fetch(`http://localhost:8000/api/article?id=${article_id}`);
    console.log(article);
    return (
        <div className="px-44 w-full relative">
            <Navbar openModal={openModal} />
            <div className="flex flex-col items-center justify-center h-screen gap-2 z-[99]">
                <AnimatedShinyText className="flex flex-row font-hanken items-center justify-center px-4 py-1 transition ease-in-out mb-1 bg-white">
                    <span className="text-3xl">Test</span>
                    <ArrowRightIcon className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
                </AnimatedShinyText>
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.5 }}
                    className="group bg-white border-black/10 text-base text-black transition-all ease-in hover:cursor-pointer mb-4"
                >
                
                </motion.div>
            </div>
            <Footer />
            <div className="pointer-events-none absolute inset-0 w-screen h-screen flex items-center justify-center">
                <GridPattern
                    className="opacity-30 w-screen [mask-image:radial-gradient(ellipse_at_center,_black_0%,_black_25%,_rgba(0,0,0,0.5)_40%,_transparent_75%)]"
                    width={40}
                    height={40}
                    squares={[[48, 32]]}
                />
            </div>
        </div>
    );
}
