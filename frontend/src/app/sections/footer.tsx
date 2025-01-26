import { Copyright } from "lucide-react";

export default function Footer() {
  return (
    <div className="h-10 bg-white flex items-center justify-center py-16">
      <p className="text-sm font-hanken flex items-center gap-1 font-semibold">
        <Copyright className="size-3" /> {new Date().getFullYear()} Virsitile.
        All rights reserved.
      </p>
    </div>
  );
}
