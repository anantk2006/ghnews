"use client"; // Required for using hooks in the App Router

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Navbar from "../components/navbar";
import Footer from "../sections/footer";
import { GridPattern } from "../components/magic-static-grid";
import "./loader.css";
import { div } from "framer-motion/client";

export default function ConnectPage() {
  const searchParams = useSearchParams();
  const session_id = searchParams.get("state"); // Access the `session_id` query parameter
  const code = searchParams.get("code"); // Access the `code` query parameter
  const nullMethod = () => null;
  const response = fetch("http://localhost:8000/api/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify({ code: code, session_id: session_id }),
  });
    const [isResponseReceived, setIsResponseReceived] = useState(false);

    useEffect(() => {
        response
            .then(() => setIsResponseReceived(true))
            .catch(() => setIsResponseReceived(false));
    }, [response]);

  return (
    <div className="px-44 w-full relative">
      <Navbar openModal={nullMethod} />
      <div className="flex flex-col items-center justify-center h-screen gap-2 z-[99]">
    {!isResponseReceived ? (
        <div>
            <div className="loader"></div>
            <p className="text-2xl font-oddlini mt-10 bg-clip-text text-black">This may take some time.</p>
        </div>
    ) : (
        <p className="text-2xl font-oddlini text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-violet-500 to-pink-500">
            You have connected your GitHub account!
        </p>
    )}
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
