import React, { useState } from "react";
import "../styles/AuthModal.css";

export default function AuthModal({ onClose }) {
  const [isRegister, setIsRegister] = useState(false);
  const [isVerification, setIsVerification] = useState(false); 
  const [formData, setFormData] = useState({
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
  });
  const [verificationCode, setVerificationCode] = useState(""); 
  const [passwordError, setPasswordError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setFieldErrors({ ...fieldErrors, [name]: false });
  };

  const handleVerificationChange = (e) => {
    setVerificationCode(e.target.value);
  };

  const handleSubmit = () => {
    const errors = {};
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

    if (Object.keys(errors).length > 0) return;

    if (isRegister) {
      localStorage.setItem("email", formData.email);
      localStorage.setItem("phone", formData.phone);
      localStorage.setItem("auth_token", "dummy_token");
      setIsVerification(true); 
    } else {
      localStorage.setItem("auth_token", "dummy_token");
      onClose();
    }
  };

  const handleVerificationSubmit = () => {
    if (verificationCode === "123456") { 
      alert("Почта успешно подтверждена!");
      onClose();
    } else {
      alert("Неверный код. Попробуйте снова.");
    }
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
        {!isVerification ? (
  <>
    <h2>{isRegister ? "Регистрация" : "Вход"}</h2>
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
            {!isRegister && (
              <input
                type="email"
                name="email"
                placeholder="Почта"
                value={formData.email}
                onChange={handleInputChange}
                style={getInputStyle("email")}
              />
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
              {!isRegister && (
                <button
                  className="recover-button"
                  onClick={() => alert("Функция восстановления аккаунта пока не реализована.")}
                >
                  Восстановить
                </button>
              )}
            </div>
          </>
        ) : (
          <>
            <h2>Подтверждение почты</h2>
            <p>Введите шестизначный код, отправленный на вашу почту.</p>
            <input
              type="text"
              placeholder="Код подтверждения"
              value={verificationCode}
              onChange={handleVerificationChange}
            />
            <div className="button-container">
              <button onClick={handleVerificationSubmit}>Подтвердить</button>
              <button onClick={() => alert("Код отправлен повторно!")}>
                Не пришел код
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}