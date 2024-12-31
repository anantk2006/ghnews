import React, { useCallback } from "react";
import {loadStripe} from '@stripe/stripe-js';
import {
  EmbeddedCheckoutProvider,
  EmbeddedCheckout
} from '@stripe/react-stripe-js';

// Make sure to call `loadStripe` outside of a component’s render to avoid
// recreating the `Stripe` object on every render.
// This is your test secret API key.
const stripePromise = loadStripe("pk_test_51QbcO9RpVERX1hynTcbOUJQb8UK5GxRH0s4SzE6iDShTf5QCa9854Ib7AitqA41E8C1KpVAEC9geokdmYWZok0Ox007b80AoTa");

const CheckoutForm = () => {
  const fetchClientSecret = useCallback(async () => {
    // Create a Checkout Session
    var ret = await fetch("http://localhost:8000/api/pay", {
      method: "POST",      
    })
    .then(response => response.json())
    console.log(ret);
    return ret;
      
  }, []);

  const options = {fetchClientSecret};

  return (
    <div id="checkout">
        <meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-inline';"></meta>
      <EmbeddedCheckoutProvider
        stripe={stripePromise}
        options={options}
      >
        <EmbeddedCheckout />
      </EmbeddedCheckoutProvider>
    </div>
  )
}

export default CheckoutForm;