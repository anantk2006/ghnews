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

export default function PaidPage() {
  const searchParams = useSearchParams();
  const session_id = searchParams.get("session_id"); // Access the `session_id` query parameter
  const nullMethod = () => null;
  const [email, setEmail] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submitting email to GitHub OAuth");
    if (session_id && email) {
      console.log("Redirecting to GitHub OAuth");
      window.location.href = `https://github.com/login/oauth/authorize?client_id=Iv23liyZsfVUeLCoHC5L&scope=repo&state=${session_id}ABCHASH${email}`;
    }
  };

  return (
    <div className="px-44 w-full relative">
      <Navbar openModal={nullMethod} />
      <div className="flex flex-col items-center justify-center h-screen gap-2 z-[99]">
        <AnimatedShinyText className="flex flex-row font-hanken items-center justify-center px-4 py-1 transition ease-in-out mb-1 bg-white">
          <span className="text-lg">Enter your email to continue</span>
          <ArrowRightIcon className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
        </AnimatedShinyText>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="group bg-white border-black/10 text-base text-black transition-all ease-in hover:cursor-pointer mb-4"
        >
          <form
            className="flex flex-col items-center z-[99]"
            onSubmit={handleSubmit}
          >
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-1 focus:ring-purple-500 z-[99] mb-4 hover:ring-1 hover:ring-purple-400"
            />
            <button
              type="submit"
              className="text-sm font-medium bg-foreground text-background px-4 py-2 pt-2.5 rounded-lg flex items-center justify-center font-oddlini"
            >
              Subscribe with GitHub
            </button>
          </form>
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
