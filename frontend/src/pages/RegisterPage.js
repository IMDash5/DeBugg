import React, { useState } from 'react';
import '../styles/RegisterPage.css'; // Путь к стилям для страницы регистрации

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Логика для регистрации
  };

  return (
    <div className="register-container">
      <h2>Регистрация</h2>
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
        <input 
          type="email" 
          placeholder="Электронная почта" 
          value={email}
          onChange={(e) => setEmail(e.target.value)} 
        />
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
};

export default RegisterPage;
