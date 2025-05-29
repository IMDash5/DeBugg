import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home.js";
import UploadResume from "./pages/UploadResume.js"; 
import Header from "./components/Header.js";
import Footer from "./components/Footer.js";
import Account from "./pages/Account.js";

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/profile" element={<Account />} />
        <Route path="/" element={<Home />} />
        <Route path="/upload-resume" element={<UploadResume />} /> {/* New route */}
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}
