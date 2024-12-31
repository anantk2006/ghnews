import React, { useState } from 'react';
import { CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

function PaymentForm() {
    const stripe = useStripe();
    const elements = useElements();
    const [paymentSucceeded, setPaymentSucceeded] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!stripe || !elements) return;

        const cardElement = elements.getElement(CardElement);

        // Call the backend to create a PaymentIntent
        const response = await fetch('/api/pay', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: 500, currency: 'usd' }) // Adjust amount and currency
        });

        const { clientSecret } = await response.json();

        // Confirm the payment with the client secret
        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: 'Cardholder Name',
                },
            },
        });

        if (result.error) {
            setError(result.error.message);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                setPaymentSucceeded(true);
            }
        }
    };

    return (
            <div style={{ maxWidth: '400px', margin: 'auto' }}>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    <label style={{ fontSize: '16px', fontWeight: 'bold' }}>Card Details</label>
                    <CardElement
                        options={{
                            style: {
                                base: {
                                    fontSize: '16px',
                                    color: '#424770',
                                    letterSpacing: '0.025em',
                                    fontFamily: 'Source Code Pro, monospace, sans-serif',
                                    '::placeholder': {
                                        color: '#aab7c4',
                                    },
                                },
                                invalid: {
                                    color: '#9e2146',
                                },
                            },
                        }}
                    />
                    <button
                        type="submit"
                        style={{
                            padding: '10px 20px',
                            fontSize: '16px',
                            color: 'white',
                            backgroundColor: '#5469d4',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                        }}
                        disabled={!stripe}
                    >
                        Pay
                    </button>
                    {error && <div style={{ color: 'red' }}>{error}</div>}
                    {paymentSucceeded && <div style={{ color: 'green' }}>Payment Successful!</div>}
                </form>
            </div>
        
    );

}

export default PaymentForm;
