import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import localFont from "next/font/local";
import "./globals.css";

const oddlini = localFont({
  src: "../fonts/oddlini-bold.ttf",
  variable: "--font-oddlini",
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Virsitile",
  description:
    "Virsitile is an innovative platform designed to help developers stay ahead in the fast-paced world of technology, startups, and artificial intelligence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${oddlini.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
