import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Header.css";
import AuthModal from "./AuthModal";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false); 
  const navigate = useNavigate();
  const userName = localStorage.getItem("username") || "Меню"; // Достаем имя пользователя из локального хранилища

  useEffect(() => {
    const hasTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    setIsTouchDevice(hasTouch);
  }, []);

  const handleMenuClick = (path) => {
    setIsMenuOpen(false);
    if (path === "/profile") {
      const token = localStorage.getItem("auth_token");
      if (!token) {
        setIsAuthModalOpen(true); 
      } else {
        navigate(path); 
      }
    } else {
      navigate(path); 
    }
  };

  const handleContainerClick = () => {
    if (isTouchDevice) {
      setIsMenuOpen((prev) => !prev);
    }
  };

  const handleTitleClick = () => {
    navigate("/home"); 
  };

  return (
    <>
      <header className="header">
        <h1 className="title" onClick={handleTitleClick} style={{ cursor: "pointer" }}>
          Debugg™
        </h1>
        <div
          className="profile-container"
          onMouseEnter={() => !isTouchDevice && setIsMenuOpen(true)}
          onMouseLeave={() => !isTouchDevice && setIsMenuOpen(false)}
          onClick={handleContainerClick}
        >
          <span className="user-name">{userName}</span>
          <div className="profile-icon">
            <img src="/images/account_logo.png" className="icon" alt="профиль" />
            <div className={`dropdown-menu ${isMenuOpen ? "open" : ""}`}>
              <button
                className="menu-item"
                onClick={() => handleMenuClick("/profile")}
              >
                Профиль
              </button>
              <button
                className="menu-item"
                onClick={() => handleMenuClick("/upload-resume")}
              >
                Загрузить резюме
              </button>
              <button
                className="menu-item"
                onClick={() => handleMenuClick("/payment")}
              >
                Оплата
              </button>
            </div>
          </div>
        </div>
      </header>
      {isAuthModalOpen && (
        <AuthModal onClose={() => setIsAuthModalOpen(false)} /> 
      )}
    </>
  );
}
