import React, { useState } from "react";
import { Link } from "react-router-dom";
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
        <div 
          className="profile-icon" 
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <img src="/images/account_logo.png" className="icon" alt="профиль"/>
          <div className={`dropdown-menu ${isMenuOpen ? "open" : ""}`}>
            <Link to="/profile" className="menu-item">Профиль</Link>
            <Link to="/home" className="menu-item">Загрузить резюме</Link>
            <Link to="/payment" className="menu-item">Оплата</Link>
            <button className="menu-item logout-button" onClick={() => alert("Выход")}>Выход</button>
          </div>
        </div>
      </div>
    </header>
  );
}
