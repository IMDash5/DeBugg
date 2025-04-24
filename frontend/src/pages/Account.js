import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Account.css";

export default function Account() {
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState(localStorage.getItem("firstName") || "");
  const [lastName, setLastName] = useState(localStorage.getItem("lastName") || "");
  const [email, setEmail] = useState(localStorage.getItem("email") || "Не указано");
  const [phone, setPhone] = useState(localStorage.getItem("phone") || "Не указано");
  const [isEditing, setIsEditing] = useState(false);
  const token = localStorage.getItem("auth_token");

  useEffect(() => {
    if (!token) {
      navigate("/login"); // Переадресация на регистрацию
    }
  }, [token, navigate]);

  const handleSave = () => {
    localStorage.setItem("firstName", firstName);
    localStorage.setItem("lastName", lastName);
    setIsEditing(false);
    alert("Данные профиля обновлены!");
  };

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
        <h2 className="account-name">
          {firstName && lastName
            ? `${firstName} ${lastName}`
            : "Неизвестный пользователь"}
        </h2>
      </div>

      <div className="account-info">
        <h3 className="account-section-title">Информация</h3>
        <div className="account-info-row">
          <div>
            <p className="account-label">Имя</p>
            <p>{firstName || "Не указано"}</p>
          </div>
          <div>
            <p className="account-label">Фамилия</p>
            <p>{lastName || "Не указано"}</p>
          </div>
        </div>
        <div className="account-info-row">
          <div>
            <p className="account-label">Почта</p>
            <p>{email}</p>
          </div>
          <div>
            <p className="account-label">Номер телефона</p>
            <p>{phone}</p>
          </div>
        </div>
        {!isEditing ? (
          <div className="button-container">
            <button
              className="edit-button"
              onClick={() => setIsEditing(true)}
            >
              Редактировать профиль
            </button>
            <button className="logout-button" onClick={handleLogout}>
              Выйти из профиля
            </button>
          </div>
        ) : (
          <>
            <input
              type="text"
              placeholder="Имя"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="account-input"
            />
            <input
              type="text"
              placeholder="Фамилия"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="account-input"
            />
            <button className="save-button" onClick={handleSave}>
              Сохранить
            </button>
          </>
        )}
      </div>
    </div>
  );
}