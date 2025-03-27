import React, { useState } from 'react';
import { Link } from 'react-router-dom';  // Добавляем импорт Link
import '../styles/LoginPage.css'; // Путь к стилям для страницы

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Логика для входа
  };

  return (
    <div className="login-container">
      <h2>Вход</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Имя пользователя" 
          value={username}
          onChange={(e) => setUsername(e.target.value)} 
        />
        <input 
          type="password" 
          placeholder="Пароль" 
          value={password}
          onChange={(e) => setPassword(e.target.value)} 
        />
        <button type="submit">Войти</button>
      </form>
      <p className="register-text">Нет аккаунта? <Link to="/register" className="register-link">Зарегистрироваться</Link></p>
    </div>
  );
};

export default LoginPage;
