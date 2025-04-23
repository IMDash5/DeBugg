import React, { useState } from "react";
import "../styles/AuthModal.css";

export default function AuthModal({ onClose }) {
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
  });
  const [passwordError, setPasswordError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({}); // Track errors for each field

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setFieldErrors({ ...fieldErrors, [name]: false }); // Reset field error on change
  };

  const handleSubmit = () => {
    const errors = {};
    if (!formData.username) errors.username = true; // Ensure username is required for both login and registration
    if (isRegister) {
      if (!formData.email || !formData.email.includes("@")) errors.email = true;
      if (!formData.phone) errors.phone = true;
      if (!formData.password) errors.password = true;
      if (formData.password !== formData.confirmPassword) {
        errors.confirmPassword = true;
        setPasswordError("Пароли не совпадают.");
      } else {
        setPasswordError("");
      }
    }

    setFieldErrors(errors);

    if (Object.keys(errors).length > 0) return; // Stop if there are errors

    if (isRegister) {
      localStorage.setItem("username", formData.username);
      localStorage.setItem("email", formData.email);
      localStorage.setItem("phone", formData.phone);
      localStorage.setItem("auth_token", "dummy_token");
    } else {
      localStorage.setItem("username", formData.username); // Save username during login
      localStorage.setItem("auth_token", "dummy_token");
    }
    onClose();
  };

  const getInputStyle = (field) => {
    if (fieldErrors[field]) return { border: "2px solid red" };
    if (formData[field]) return { border: "2px solid green" };
    return {};
  };

  return (
    <div className="auth-modal">
      <div className="auth-modal-content">
        <button className="close-icon" onClick={onClose}>
          &times;
        </button>
        <h2>{isRegister ? "Регистрация" : "Вход"}</h2>
        <input
          type="text"
          name="username"
          placeholder="Логин"
          value={formData.username}
          onChange={handleInputChange}
          style={getInputStyle("username")}
        />
        {isRegister && (
          <>
            <input
              type="email"
              name="email"
              placeholder="Почта"
              value={formData.email}
              onChange={handleInputChange}
              style={getInputStyle("email")}
            />
            <input
              type="text"
              name="phone"
              placeholder="Номер телефона"
              value={formData.phone}
              onChange={handleInputChange}
              style={getInputStyle("phone")}
            />
          </>
        )}
        <input
          type="password"
          name="password"
          placeholder="Пароль"
          value={formData.password}
          onChange={handleInputChange}
          style={getInputStyle("password")}
        />
        {isRegister && (
          <input
            type="password"
            name="confirmPassword"
            placeholder="Повторите пароль"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            style={getInputStyle("confirmPassword")}
          />
        )}
        {passwordError && <p className="error-message">{passwordError}</p>}
        <div className="button-container">
          <button onClick={handleSubmit}>
            {isRegister ? "Зарегистрироваться" : "Войти"}
          </button>
          <button onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? "Уже есть аккаунт?" : "Нет аккаунта?"}
          </button>
        </div>
      </div>
    </div>
  );
}
