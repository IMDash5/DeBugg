// src/pages/LoginPage.js

import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/LoginPage.css';  // Подключаем стили для LoginPage

const LoginPage = () => {
  return (
    <div className="auth-wrapper">
      <h2 className="auth-header">Вход</h2>
      <form className="auth-form">
        <input type="email" className="auth-input" placeholder="Электронная почта" />
        <input type="password" className="auth-input" placeholder="Пароль" />
        <button type="submit" className="auth-button">Войти</button>
      </form>
      <p>
        <Link to="/register" className="auth-link-light">Нет аккаунта? Зарегистрироваться</Link>
      </p>
    </div>
  );
};

export default LoginPage;
