import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Header from './components/Header'; // Импортируем Header
import Footer from './components/Footer'; // Импортируем Footer
import LoginPage from './pages/LoginPage'; // Страница входа
import RegisterPage from './pages/RegisterPage'; // Страница регистрации

const App = () => {
  const isAuthenticated = !!localStorage.getItem('jwtToken');

  return (
    <Router>
      <div className="App">
        <Header /> {/* Добавляем Header */}
        <Routes>
          <Route
            path="/"
            element={isAuthenticated ? <Navigate to="/home" /> : <LoginPage />}
          />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          {/* Перенаправление для незарегистрированных пользователей */}
          <Route path="/home" element={isAuthenticated ? <h1>Welcome Home!</h1> : <Navigate to="/login" />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
