import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Account.css";

export default function Account() {
  const navigate = useNavigate();
  const [name, setname] = useState(localStorage.getItem("name") || "");
  const [surname, setsurname] = useState(localStorage.getItem("surname") || "");
  const [email, setEmail] = useState(localStorage.getItem("email") || "Не указано");
  const [phone] = useState(localStorage.getItem("phone") || "Не указано");
  const [isEditing, setIsEditing] = useState(false);
  const [avatar, setAvatar] = useState(localStorage.getItem("avatar") || "/images/account_logo.png");
  const [isAvatarModalOpen, setIsAvatarModalOpen] = useState(false);
  const token = localStorage.getItem("auth_token");

  useEffect(() => {
    if (!token) {
      navigate("/login");
    } else {
      const fetchUserData = async () => {
        try {
          const response = await fetch("/get_user_info_by_token", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            const data = await response.json();
            // Предположим, что бэкенд возвращает { name, surname, email }
            setname(data.name || "");
            setsurname(data.surname || "");
            setEmail(data.email || "");

            // Сохраним в localStorage, если нужно
            localStorage.setItem("name", data.name || "");
            localStorage.setItem("surname", data.surname || "");
            localStorage.setItem("email", data.email || "");
          } else {
            console.error("Ошибка загрузки данных пользователя:", response.status);
          }
        } catch (error) {
          console.error("Ошибка загрузки данных пользователя:", error);
        }
      };

      fetchUserData();
    }
    }, [token, navigate]);

const handleSave = async () => {
  try {
    const response = await fetch("/account/name", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: name,
        surname: surname,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      // Обнови localStorage, если нужно
      localStorage.setItem("name", name);
      localStorage.setItem("surname", surname);
      alert("Данные профиля успешно обновлены!");
      setIsEditing(false);
    } else {
      const errorData = await response.json();
      alert(`Ошибка: ${errorData.message || "Не удалось обновить профиль"}`);
    }
  } catch (error) {
    console.error("Ошибка обновления профиля:", error);
    alert("Произошла ошибка при обновлении профиля. Попробуйте еще раз.");
  }
  };

  const handleLogout = async () => {
  try {
    const response = await fetch("/account/logout", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (response.ok) {
      localStorage.clear();
      navigate("/login");
    } else {
      const errorData = await response.json();
      alert(`Ошибка: ${errorData.message || "Не удалось выйти"}`);
    }
  } catch (error) {
    console.error("Ошибка при логауте:", error);
    alert("Произошла ошибка при выходе. Попробуйте ещё раз.");
    }
  };

  const handleAvatarClick = () => {
    setIsAvatarModalOpen(true);
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith("image/")) {
      // Ограничение размера файла (до 10 МБ)
      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        alert("Размер аватарки не должен превышать 10 МБ.");
        return;
      }
      const reader = new FileReader();
      reader.onload = (ev) => {
        try {
          setAvatar(ev.target.result);
          localStorage.setItem("avatar", ev.target.result);
          setIsAvatarModalOpen(false);
        } catch (err) {
          alert("Ошибка: не удалось сохранить аватарку. Файл слишком большой или недостаточно места.");
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCloseAvatarModal = () => {
    setIsAvatarModalOpen(false);
  };

  return (
    <div className="account-container">
      <div className="account-sidebar">
        <img
          src={avatar}
          alt="avatar"
          className="account-avatar"
          style={{ cursor: "pointer" }}
          onClick={handleAvatarClick}
        />
        <h2 className="account-name">
          {name && surname
            ? `${name} ${surname}`
            : "Неизвестный пользователь"}
        </h2>
      </div>

      <div className="account-info">
        <h3 className="account-section-title">Информация</h3>
        <div className="account-info-row">
          <div>
            <p className="account-label">Имя</p>
            <p>{name || "Не указано"}</p>
          </div>
          <div>
            <p className="account-label">Фамилия</p>
            <p>{surname || "Не указано"}</p>
          </div>
        </div>
        <div className="account-info-row">
          <div>
            <p className="account-label">Почта</p>
            <p>{email}</p>
          </div>
          <div>
            <p className="account-label">Логин</p>
            <p>{login}</p>
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
              value={name}
              onChange={(e) => setname(e.target.value)}
              className="account-input"
            />
            <input
              type="text"
              placeholder="Фамилия"
              value={surname}
              onChange={(e) => setsurname(e.target.value)}
              className="account-input"
            />
            <button className="save-button" onClick={handleSave}>
              Сохранить
            </button>
          </>
        )}
      </div>

      {/* Модальное окно для просмотра и замены аватарки */}
      {isAvatarModalOpen && (
        <div
          style={{
            position: "fixed",
            zIndex: 1001,
            left: 0,
            top: 0,
            width: "100vw",
            height: "100vh",
            background: "rgba(0,0,0,0.7)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
          }}
          onClick={handleCloseAvatarModal}
        >
          <div
            style={{
              background: "#23272f",
              borderRadius: "16px",
              padding: "32px 24px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              position: "relative",
              width: "90vw",
              maxWidth: 340,
              minWidth: 0,
            }}
            onClick={e => e.stopPropagation()}
          >
            <button
              style={{
                position: "absolute",
                top: 10,
                right: 16,
                background: "transparent",
                border: "none",
                color: "#fff",
                fontSize: 28,
                cursor: "pointer"
              }}
              onClick={handleCloseAvatarModal}
              aria-label="Закрыть"
            >
              &times;
            </button>
            <img
              src={avatar}
              alt="avatar-large"
              style={{
                width: 120,
                height: 120,
                borderRadius: "50%",
                marginBottom: 24,
                objectFit: "cover",
                border: "3px solid #fff"
              }}
            />
            <label
              style={{
                background: "#2563eb",
                color: "#fff",
                padding: "10px 18px",
                borderRadius: "8px",
                cursor: "pointer",
                fontSize: "1rem"
              }}
            >
              Заменить аватарку
              <input
                type="file"
                accept="image/*"
                style={{ display: "none" }}
                onChange={handleAvatarChange}
              />
            </label>
          </div>
        </div>
      )}
    </div>
  );
}