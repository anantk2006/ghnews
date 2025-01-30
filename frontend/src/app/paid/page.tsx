"use client"; // Required for using hooks in the App Router

import { useSearchParams } from 'next/navigation';
import { useState } from 'react';
import Navbar from '../components/navbar';
import Footer from '../sections/footer';
import { ArrowRightIcon } from 'lucide-react';
import { AnimatedShinyText } from '../components/magic-shiny-text';
import { InteractiveGridPattern } from '../components/magic-background-grid';
import { motion } from 'framer-motion';

export default function PaidPage() {
  const searchParams = useSearchParams();
  const session_id = searchParams.get('session_id'); // Access the `session_id` query parameter
  const nullMethod = () => null;
  const [email, setEmail] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (session_id && email) {
      window.location.href = `/some-link?email=${email}&session_id=${session_id}`;
    }
  };

  return (
    <div className='px-44'>
        <Navbar openModal={nullMethod} />
        <div className="flex flex-col items-center justify-center h-screen gap-2 z-[99]">
  <AnimatedShinyText className="flex flex-row font-hanken items-center justify-center px-4 py-1 transition ease-in-out mb-4">
    <span className='text-lg'>Enter your email to continue</span>
    <ArrowRightIcon className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
  </AnimatedShinyText>
  <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="flex items-center justify-center mt-5"
          >
  <form onSubmit={handleSubmit} className="flex flex-col items-center">
    <input
      type="email"
      id="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      required
      className="mb-4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
    <button
      type="submit"
      className="text-sm font-medium bg-foreground text-background px-4 py-2 pt-2.5 rounded-lg flex items-center justify-center font-oddlini hover:bg-foreground/80"
    >
      Subscribe with GitHub
    </button>
  </form>
</motion.div>
</div>
<Footer />
<div className="absolute inset-0 w-screen h-screen flex items-center justify-center">
        <InteractiveGridPattern
          className="opacity-30 w-screen [mask-image:radial-gradient(ellipse_at_center,_black_0%,_black_25%,_rgba(0,0,0,0.5)_40%,_transparent_75%)]"
          width={40}
          height={40}
          squares={[48, 32]}
          squaresClassName="hover:fill-purple-500"
        />
      </div>
    </div>
  );
}