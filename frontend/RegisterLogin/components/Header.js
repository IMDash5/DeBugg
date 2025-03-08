import React from 'react';
import { Link } from 'react-router-dom'; // Для навигации, если нужно
import '../styles/Header.css'; // Путь к стилям

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">
        <h1>
          DeBugg<sup>&#8482;</sup> {/* Символ ™ для товарного знака */}
        </h1>
      </div>
      <nav className="header-nav">
        {/* Навигационные ссылки можно оставить пустыми, если они не нужны */}
      </nav>
    </header>
  );
};

export default Header;
