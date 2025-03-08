import React, { useState, useEffect } from "react";
import "./App.css";
import RegistrationPage from "./RegistrationPage";
import LoginPage from "./LoginPage";

const App = () => {
  const [isLoginPage, setIsLoginPage] = useState(true);
  const [stars, setStars] = useState([]);

  const togglePage = () => {
    setIsLoginPage(!isLoginPage);
  };

  useEffect(() => {
    const newStars = [];
    for (let i = 0; i < 100; i++) {
      newStars.push({
        left: `${Math.random() * 100}vw`,
        top: `${Math.random() * 100}vh`,
        size: `${Math.random() * 3 + 1}px`,
        opacity: Math.random() * 0.7 + 0.3,
        animationDuration: `${Math.random() * 2 + 1}s`,
        animationDelay: `${Math.random() * 2}s`,
      });
    }
    setStars(newStars);
  }, []);

  return (
    <div className="app">
      <div className="stars">
        {stars.map((star, index) => (
          <div
            key={index}
            className="star"
            style={{
              left: star.left,
              top: star.top,
              width: star.size,
              height: star.size,
              opacity: star.opacity,
              animationDuration: star.animationDuration,
              animationDelay: star.animationDelay,
            }}
          />
        ))}
      </div>

      <div className="content-wrapper">
        <header className="header">
          <h1>Добро пожаловать</h1>
          <p>Войдите в систему или зарегистрируйтесь</p>
        </header>

        <div className="auth-container">
          <h2>{isLoginPage ? "Вход" : "Регистрация"}</h2>
          {isLoginPage ? <LoginPage /> : <RegistrationPage />}
          <div className="auth-footer">
            <span>
              {isLoginPage ? (
                <>
                  Нет аккаунта?{" "}
                  <a href="#" className="register-link" onClick={togglePage}>
                    Зарегистрироваться
                  </a>
                </>
              ) : (
                <>
                  Есть аккаунт?{" "}
                  <a href="#" className="register-link" onClick={togglePage}>
                    Войти
                  </a>
                </>
              )}
            </span>
          </div>
        </div>
      </div>

      <footer className="footer">
        <p>&copy; 2025 Все права защищены</p>
      </footer>
    </div>
  );
};

export default App;
