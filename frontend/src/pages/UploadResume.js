import React, { useState, useEffect } from "react";
import "../styles/Home.css";

export default function UploadResume() {
  const [resumeText, setResumeText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isResultVisible, setIsResultVisible] = useState(false);
  const [fileError, setFileError] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [isFileSelected, setIsFileSelected] = useState(false);
  const [showGif, setShowGif] = useState(false); // Новое состояние для отображения GIF
  const [resultText, setResultText] = useState(""); // Новый стейт для результата

  useEffect(() => {
    document.title = "Загрузить резюме";
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
      setFileError("");
      setIsFileSelected(true);
    } else {
      setFileError("Пожалуйста, выберите PDF файл.");
      setSelectedFile(null);
      setIsFileSelected(false);
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setFileError("Пожалуйста, прикрепите PDF файл.");
      return;
    }

    setIsLoading(true);
    setShowGif(true);

    // таймер для скрытия GIF через 5 секунд
    setTimeout(() => {
      setShowGif(false); 
      setIsLoading(false);
      setIsResultVisible(true);
      // Здесь имитация результата, замените на реальный fetch к API
      setResultText(
        "Пример результата анализа резюме: \n\n- Ключевые навыки: Python, ML\n- Опыт работы: 3 года\n- Рекомендации: добавить проекты"
      );
    }, 5000);
  };

  return (
    <div className="container">
      <main className="main">
        <h2 className="subtitle">Вставьте ваше резюме</h2>
        <textarea
          className="resume-input"
          placeholder="Введите текст запроса..."
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
        ></textarea>
        <div className="button-container">
          <label
            className={`file-upload-button ${isFileSelected ? "file-selected" : ""}`}
            style={{
              width: "150px",
              height: "40px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            Выбрать файл
            <input
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </label>
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <button
              className="submit-button"
              onClick={handleSubmit}
              disabled={isLoading}
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              {isLoading ? "Загрузка..." : "Отправить"}
            </button>
            {showGif && (
              <img
                src="/images/rocket-for-waiting.gif"
                alt="Загрузка"
                style={{ width: "60px", height: "60px" }}
              />
            )}
          </div>
        </div>
        {fileError && <p className="error-message">{fileError}</p>}

        {isResultVisible && (
          <div style={{
            marginTop: "32px",
            width: "100%",
            background: "#23272f",
            borderRadius: "10px",
            padding: "20px",
            color: "#fff",
            boxShadow: "0 2px 8px rgba(0,0,0,0.12)"
          }}>
            <h3 style={{marginTop: 0}}>Результат анализа</h3>
            <pre style={{
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              background: "none",
              color: "#d1fae5",
              fontSize: "1rem"
            }}>
              {resultText}
            </pre>
          </div>
        )}
      </main>
    </div>
  );
}


