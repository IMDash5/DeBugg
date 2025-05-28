import React, { useEffect } from "react";
import "../styles/Home.css";

export default function Home() {
  useEffect(() => {
    document.title = "О нас";
  }, []);

  return (
    <div
      className="container"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        width: "100vw",
        boxSizing: "border-box",
      }}
    >
      <main
        className="main"
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          maxWidth: 800,
          margin: "0 auto",
          minHeight: "300px",
        }}
      >
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