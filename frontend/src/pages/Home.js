import React, { useState } from "react";
import "../styles/Home.css";
import Header from "../components/Header";

export default function Home() {
  const [setIsSidebarOpen] = useState(false);
  const [resumeText, setResumeText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isResultVisible, setIsResultVisible] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    
    // Имитация запроса к бэкенду (2 секунды ожидания)
    setTimeout(() => {
      setIsLoading(false);
      setIsResultVisible(true);
    }, 2000);
  };

  return (
    <div className="container">
      {/* Шапка */}
      <Header setIsSidebarOpen={setIsSidebarOpen} />

      {/* Блок с результатом (выезжающий слева) */}
      <div className={`result-panel ${isResultVisible ? "open" : ""}`}></div>

      {/* Основной блок */}
      <main className={`main ${isResultVisible ? "shifted" : ""}`}>
        <h2 className="subtitle">Вставьте ваше резюме</h2>
        <textarea 
          className="resume-input" 
          placeholder="Введите текст резюме..."
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
        ></textarea>
        <button className="submit-button" onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? "Загрузка..." : "Отправить"}
        </button>
      </main>
    </div>
  );
}