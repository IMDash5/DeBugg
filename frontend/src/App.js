import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home.js";
import Payment from "./pages/Payment.js";
import Header from "./components/Header.js";
import Footer from "./components/Footer.js";

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/payment" element={<Payment />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}
