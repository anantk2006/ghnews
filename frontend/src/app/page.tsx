import Navbar from "./components/navbar";

export default function Home() {
  return (
    <div>
      <Navbar />
      <div className="flex items-center justify-center h-screen">
        <div className="flex flex-col items-center justify-center px-44">
          <h1 className="text-7xl font-oddlini text-center leading-[1.35]">
            The tech news you need, <br /> made{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-violet-500 to-pink-500">
              simple.
            </span>
          </h1>
        </div>
      </div>
    </div>
  );
}
