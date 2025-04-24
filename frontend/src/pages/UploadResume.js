
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
    }, 5000);
  };

  return (
    <div className="container">
      {/* Блок с результатом (выезжающий слева) */}
      <div className={`result-panel ${isResultVisible ? "open" : ""}`}></div>
      <main className={`main ${isResultVisible ? "shifted" : ""}`}>
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
      </main>
    </div>
  );
}


