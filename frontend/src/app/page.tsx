import Navbar from "./components/navbar";
import Footer from "./sections/footer";
import Hero from "./sections/hero";
import Pricing from "./sections/pricing";

export default function Home() {
  return (
    <div>
      <Navbar />
      <Hero />
      <Pricing />
      <Footer />
    </div>
  );
}
