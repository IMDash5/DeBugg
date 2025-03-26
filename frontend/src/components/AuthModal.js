import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/AuthModal.css";

export default function AuthModal({ onClose }) {
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    phone: "",
    password: "",
  });
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = () => {
    if (isRegister) {
      // Мохраняем данные в локалтное хранилище
      localStorage.setItem("username", formData.username);
      localStorage.setItem("email", formData.email);
      localStorage.setItem("phone", formData.phone);
      localStorage.setItem("auth_token", "dummy_token"); 
    } else {
      // Симуляция входа пользователя
      localStorage.setItem("auth_token", "dummy_token");
    }
    onClose();
    navigate("/profile"); 
  };

  return (
    <div className="auth-modal">
      <div className="auth-modal-content">
        <button className="close-icon" onClick={onClose}>
          &times;
        </button>
        <h2>{isRegister ? "Регистрация" : "Вход"}</h2>
        {isRegister && (
          <>
            <input
              type="text"
              name="username"
              placeholder="Логин"
              value={formData.username}
              onChange={handleInputChange}
            />
            <input
              type="email"
              name="email"
              placeholder="Почта"
              value={formData.email}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="phone"
              placeholder="Номер телефона"
              value={formData.phone}
              onChange={handleInputChange}
            />
          </>
        )}
        <input
          type="password"
          name="password"
          placeholder="Пароль"
          value={formData.password}
          onChange={handleInputChange}
        />
        <button onClick={handleSubmit}>
          {isRegister ? "Зарегистрироваться" : "Войти"}
        </button>
        <button onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? "Уже есть аккаунт?" : "Нет аккаунта?"}
        </button>
      </div>
    </div>
  );
}
