import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Account.css';

export default function Account() {
  const navigate = useNavigate();
  const username = localStorage.getItem("username");
  const email = localStorage.getItem("email");
  const phone = localStorage.getItem("phone");
  const token = localStorage.getItem("auth_token");

  useEffect(() => {
    if (!token) {
      navigate("/login"); // Переадресация на регистрацию
    }
  }, [token, navigate]);

  const handleLogout = () => {
    localStorage.clear(); // Очищение данных пользователя
    navigate("/login"); // Переадресация на регистрацию
  };

  return (
    <div className="account-container">
      <div className="account-sidebar">
        <img
          src="/images/account_logo.png"
          alt="avatar"
          className="account-avatar"
        />
        <h2 className="account-name">{username || "Неизвестный пользователь"}</h2>
        <p className="account-role">Пользователь</p>
      </div>

      <div className="account-info">
        <h3 className="account-section-title">Информация</h3>
        <div className="account-info-row">
          <div>
            <p className="account-label">Email</p>
            <p>{email || "Не указано"}</p>
          </div>
          <div>
            <p className="account-label">Телефон</p>
            <p>{phone || "Не указано"}</p>
          </div>
        </div>
        <button className="logout-button" onClick={handleLogout}>
          Выйти из профиля
        </button>
      </div>
    </div>
  );
}
