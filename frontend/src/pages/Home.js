import React, { useEffect } from "react";
import "../styles/Home.css";

export default function Home() {
  useEffect(() => {
    document.title = "О нас";
  }, []);

  return (
    <div className="container">
      <main className="main">
        <h2 className="subtitle">О нас</h2>
        <p className="about-text">
          Debugg™ — это инновационный проект, который использует нейронные сети для автоматического анализа резюме. 
          Мы стремимся упростить процесс составления резюме, помочь в поиске ключевых ошибок и предложить рекомендации 
          для соискателей. Наша цель — сделать поиск работы проще и эффективнее.
        </p>
      </main>
    </div>
  );
}