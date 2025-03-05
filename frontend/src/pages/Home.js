import React, { useState } from "react";
import "../styles/Home.css";
import Header from "../components/Header";

export default function Home() {
  const [setIsSidebarOpen] = useState(false);

  return (
    <div className="container">
      {/* Шапка */}
      <Header setIsSidebarOpen={setIsSidebarOpen} />

      {/* Основной блок */}
      <main className="main">
        <h2 className="subtitle">Вставьте ваше резюме</h2>
        <textarea className="resume-input" placeholder="Введите текст резюме..."></textarea>
      </main>
    </div>
  );
}
