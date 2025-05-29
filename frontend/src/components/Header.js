import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Header.css";
import AuthModal from "./AuthModal";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false); 
  const [theme, setTheme] = useState("dark");
  const navigate = useNavigate();
  const userName = localStorage.getItem("username") || "Меню";

  // Определяем предпочтение клиента
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute("data-theme", savedTheme);
    } else {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const detectedTheme = prefersDark ? "dark" : "light";
      setTheme(detectedTheme);
      document.documentElement.setAttribute("data-theme", detectedTheme);
    }
  }, []);

  // Сохраняем тему и применяем к html
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const handleThemeToggle = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

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
          onMouseEnter={() => !isTouchDevice && setIsMenuOpen(true)}
          onMouseLeave={() => !isTouchDevice && setIsMenuOpen(false)}
          onClick={handleContainerClick}
        >
          <span className="user-name">{userName}</span>
          {/* Меню в строку для больших экранов */}
          <nav className="header-nav">
            <div className="theme-toggle-container" style={{marginRight: 12}}>
              <label className="theme-switch">
                <input
                  type="checkbox"
                  checked={theme === "light"}
                  onChange={handleThemeToggle}
                  aria-label="Переключить тему"
                />
                <span className="slider"></span>
                <span className="theme-label">{theme === "light" ? "Светлая" : "Тёмная"}</span>
              </label>
            </div>
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
          </nav>
          {/* Иконка всегда видна, выпадающее меню только на маленьких экранах */}
          <div className="profile-icon">
            <img src="/images/account_logo.png" className="icon" alt="профиль" />
            <div className={`dropdown-menu ${isMenuOpen ? "open" : ""}`}>
              <div className="theme-toggle-container" style={{margin: "0 0 8px 0"}}>
                <label className="theme-switch">
                  <input
                    type="checkbox"
                    checked={theme === "light"}
                    onChange={handleThemeToggle}
                    aria-label="Переключить тему"
                  />
                  <span className="slider"></span>
                  <span className="theme-label">{theme === "light" ? "Светлая" : "Тёмная"}</span>
                </label>
              </div>
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
