import React from 'react';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import PaymentForm from './PaymentForm';

// Replace with your Stripe Publishable Key
const stripePromise = loadStripe("pk_test_51QbcO9RpVERX1hynTcbOUJQb8UK5GxRH0s4SzE6iDShTf5QCa9854Ib7AitqA41E8C1KpVAEC9geokdmYWZok0Ox007b80AoTa");

function Form() {
    return (
        <Elements stripe={stripePromise}>
            <PaymentForm />
        </Elements>
    );
}

export default Form;