import React, { useState, useEffect } from "react";
import "../styles/Payment.css";

export default function Payment() {
  const [cardNumber, setCardNumber] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [cvv, setCvv] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  
  useEffect(() => {
    document.title = "Оплата";
  }, []);

  const handlePayment = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      alert("Оплата успешно выполнена!");
    }, 2000);
  };

  return (
    <div className="container">
      <div className="payment-wrapper">
        <h2 className="subtitle">Оплата</h2>
        <div className="payment-form">
          <input
            type="text"
            className="payment-input"
            placeholder="Номер карты"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value)}
          />
          <input
            type="text"
            className="payment-input"
            placeholder="Срок действия (MM/YY)"
            value={expiryDate}
            onChange={(e) => setExpiryDate(e.target.value)}
          />
          <input
            type="text"
            className="payment-input"
            placeholder="CVV"
            value={cvv}
            onChange={(e) => setCvv(e.target.value)}
          />
          <button className="submit-button" onClick={handlePayment} disabled={isProcessing}>
            {isProcessing ? "Обработка..." : "Оплатить"}
          </button>
        </div>
      </div>
    </div>
  );
}