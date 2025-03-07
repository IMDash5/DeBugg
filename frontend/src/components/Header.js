import React, { useState } from "react";
import "../styles/Header.css";

export default function Header({ setIsSidebarOpen }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const userName = "Иванов Иван";

  return (
    <header className="header">
      <h1 className="title">Debugg™</h1>

      <div 
        className="profile-container" 
        onMouseEnter={() => setIsMenuOpen(true)} 
        onMouseLeave={() => setIsMenuOpen(false)}
      >
        <span className="user-name">{userName}</span>
        <div className="profile-icon">
          <img src="/images/account_logo.png" className="icon" alt="профиль"/>
          <div className={`dropdown-menu ${isMenuOpen ? "open" : ""}`}>
            <a href="#" className="menu-item">Профиль</a>
            <a href="#" className="menu-item">Оплата</a>
            <a href="#" className="menu-item">Выход</a>
          </div>
        </div>
      </div>
    </header>
  );
}
