import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Header.css";
import AuthModal from "./AuthModal";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [closeTimer, setCloseTimer] = useState(null);
  const menuRef = useRef(null);
  const navigate = useNavigate();

  const authToken = localStorage.getItem("auth_token");
  const isLoggedIn = Boolean(authToken); // Проверка, вошёл ли пользователь
  const userName = isLoggedIn ? localStorage.getItem("username") || "Меню" : "Войти";

  useEffect(() => {
    const hasTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    setIsTouchDevice(hasTouch);
    return () => clearTimeout(closeTimer);
  }, []);

  const handleMouseEnter = () => {
    if (!isTouchDevice && isLoggedIn) {
      clearTimeout(closeTimer);
      setIsMenuOpen(true);
    }
  };

  const handleMouseLeave = () => {
    if (!isTouchDevice && isLoggedIn) {
      setCloseTimer(setTimeout(() => setIsMenuOpen(false), 300));
    }
  };

  const handleMenuClick = (path) => {
    setIsMenuOpen(false);
    if (path === "/profile") {
      if (!isLoggedIn) {
        setIsAuthModalOpen(true);
      } else {
        navigate(path);
      }
    } else {
      navigate(path);
    }
  };

  const handleContainerClick = (e) => {
    if (!isLoggedIn) {
      setIsAuthModalOpen(true); // Если не вошёл — показываем окно входа
      return;
    }

    if (isTouchDevice) {
      if (menuRef.current && menuRef.current.contains(e.target)) {
        return;
      }
      setIsMenuOpen((prev) => !prev);
    }
  };

  const handleTitleClick = () => {
    navigate("/");
  };

  return (
    <>
      <header className="header">
        <h1 className="title" onClick={handleTitleClick} style={{ cursor: "pointer" }}>
          Debugg™
        </h1>
        <div
          className="profile-container"
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          onClick={handleContainerClick}
        >
          <span className="user-name">{userName}</span>
          <div className="profile-icon">
            <img src="/images/account_logo.png" className="icon" alt="профиль" />
            {isLoggedIn && (
              <div
                ref={menuRef}
                className={`dropdown-menu ${isMenuOpen ? "open" : ""}`}
              >
                <button className="menu-item" onClick={() => handleMenuClick("/profile")}>
                  Профиль
                </button>
                <button className="menu-item" onClick={() => handleMenuClick("/upload-resume")}>
                  Загрузить резюме
                </button>
                <button className="menu-item" onClick={() => handleMenuClick("/payment")}>
                  Оплата
                </button>
              </div>
            )}
          </div>
        </div>
      </header>
      {isAuthModalOpen && (
        <AuthModal onClose={() => setIsAuthModalOpen(false)} />
      )}
    </>
  );
}
