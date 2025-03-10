import React, { useCallback } from "react";
import { loadStripe, Stripe } from "@stripe/stripe-js";
import{
  EmbeddedCheckoutProvider,
  EmbeddedCheckout,
} from "@stripe/react-stripe-js"; 
import "../globals.css"

// Make sure to call `loadStripe` outside of a component’s render to avoid
// recreating the `Stripe` object on every render.
// Replace this with your actual Stripe public key.
const stripePromise: Promise<Stripe | null> = loadStripe("pk_test_51QbcO9RpVERX1hynTcbOUJQb8UK5GxRH0s4SzE6iDShTf5QCa9854Ib7AitqA41E8C1KpVAEC9geokdmYWZok0Ox007b80AoTa");

const CheckoutForm: React.FC = () => {
    console.log("CheckoutForm");
  const fetchClientSecret = useCallback(async (): Promise<string> => {
    try {
      const response = await fetch("https://api.virsitile.dev/api/pay", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      return data; // Assuming your server returns `{ clientSecret: string }`
    } catch (error) {
      console.error("Error fetching client secret:", error);
      throw error;
    }
  }, []);

    const options = { fetchClientSecret };

  return (
    <div id="checkout" className="embed-checkout">
      <EmbeddedCheckoutProvider stripe={stripePromise} options={options}>
        <EmbeddedCheckout />
      </EmbeddedCheckoutProvider>
    </div>
  );
};

export default CheckoutForm;
