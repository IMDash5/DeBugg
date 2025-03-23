import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Header.css";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  const navigate = useNavigate();
  const userName = "Иванов Иван";

  useEffect(() => {
    // Определяем, есть ли touch
    const hasTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    setIsTouchDevice(hasTouch);
  }, []);

  const handleMenuClick = (path) => {
    setIsMenuOpen(false);
    navigate(path);
  };

  const handleContainerClick = () => {
    if (isTouchDevice) {
      setIsMenuOpen((prev) => !prev);
    }
  };

  return (
    <header className="header">
      <h1 className="title">Debugg™</h1>
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
              onClick={() => handleMenuClick("/home")}
            >
              Загрузить резюме
            </button>
            <button
              className="menu-item"
              onClick={() => handleMenuClick("/payment")}
            >
              Оплата
            </button>
            <button
              className="menu-item logout-button"
              onClick={() => {
                setIsMenuOpen(false);
                alert("Выход");
              }}
            >
              Выход
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
