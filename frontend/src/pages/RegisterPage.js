// src/pages/RegisterPage.js

import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/RegisterPage.css';  // Подключаем стили для RegisterPage

const RegisterPage = () => {
  return (
    <div className="auth-wrapper">
      <h2 className="auth-header">Регистрация</h2>
      <form className="auth-form">
        <input type="text" className="auth-input" placeholder="Имя" />
        <input type="text" className="auth-input" placeholder="Фамилия" />
        <input type="tel" className="auth-input" placeholder="Номер телефона" />
        <input type="email" className="auth-input" placeholder="Электронная почта" />
        <input type="password" className="auth-input" placeholder="Пароль" />
        <button type="submit" className="auth-button">Зарегистрироваться</button>
      </form>
      <p>
        <Link to="/login" className="auth-link-light">Есть аккаунт? Войти</Link>
      </p>
    </div>
  );
};

export default RegisterPage;
