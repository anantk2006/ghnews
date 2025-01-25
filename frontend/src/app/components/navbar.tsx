"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export default function Navbar() {
  return (
    <motion.div
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8 }}
      className="flex h-16 items-center justify-between px-6 border-b"
    >
      <div className="flex items-center gap-6 font-oddlini justify-center mt-0.5">
        <Link href="/" className="text-2xl font-semibold font-oddlini">
          Virsitile
        </Link>
      </div>
      <div className="flex items-center gap-6 justify-center">
        <Link
          href="/login"
          className="text-sm font-medium hover:text-foreground/8 flex items-center justify-center font-oddlini mt-0.5 hover:text-foreground/90"
        >
          Login
        </Link>
        <Link
          href="/signup"
          className="text-sm font-medium bg-foreground text-background px-4 py-2 pt-2.5 rounded-lg flex items-center justify-center font-oddlini hover:bg-foreground/80"
        >
          Sign up
        </Link>
      </div>
    </motion.div>
  );
}
