import { ArrowRightIcon } from "lucide-react";

import { cn } from "@/lib/utils";

import { InteractiveGridPattern } from "../components/magic-background-grid";
import { AnimatedShinyText } from "../components/magic-shiny-text";
import Link from "next/link";

export default function Hero() {
  return (
    <div className="flex items-center justify-center h-screen relative overflow-hidden">
      <div className="absolute inset-0 w-screen h-screen flex items-center justify-center">
        <InteractiveGridPattern
          className="opacity-30 w-screen [mask-image:radial-gradient(ellipse_at_center,_black_0%,_black_25%,_rgba(0,0,0,0.5)_40%,_transparent_75%)]"
          width={40}
          height={40}
          squares={[48, 32]}
          squaresClassName="hover:fill-purple-500"
        />
      </div>
      <div className="flex flex-col items-center justify-center px-44 gap-2 z-[99]">
        <div
          className={cn(
            "group rounded-full border border-black/10 text-base bg-white text-black transition-all ease-in hover:cursor-pointer hover:bg-neutral-200 dark:border-white/5 dark:bg-neutral-900 dark:hover:bg-neutral-800 mb-4",
          )}
        >
          <AnimatedShinyText className="inline-flex font-hanken items-center justify-center px-4 py-1 transition ease-out">
            <span>✨ Sign up for a free 14 day trial</span>
            <ArrowRightIcon className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
          </AnimatedShinyText>
        </div>
        <h1 className="text-7xl font-oddlini text-center leading-[1.25]">
          The tech news you need, <br /> made{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-violet-500 to-pink-500">
            simple.
          </span>
        </h1>
        <p className="text-xl font-hanken text-center text-neutral-600 w-3/4">
          The modern standard for staying up-to-date with everything tech.{" "}
          <br />
          Simple, personalized, and uniquely yours.
        </p>
        <div className="flex items-center justify-center mt-5">
          <Link
            href="/signup"
            className="text-sm font-medium bg-foreground text-background px-4 py-2 pt-2.5 rounded-lg flex items-center justify-center font-oddlini hover:bg-foreground/80"
          >
            Get Started for Free
            <ArrowRightIcon className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
