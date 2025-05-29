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
  const [resultText, setResultText] = useState(""); 

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
  if (!resumeText.trim()) {
    setFileError("Пожалуйста, введите текст запроса.");
    return;
  }

  setIsLoading(true);
  setShowGif(true);
  setFileError("");
  setIsResultVisible(false);

  try {
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("query", resumeText);

    const response = await fetch("/analyze-resume", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Ошибка сервера: ${response.statusText}`);
    }

    const data = await response.json();
    setResultText(data.result || "Результат пустой");
    setIsResultVisible(true);
  } catch (error) {
    setFileError(`Ошибка при запросе: ${error.message}`);
  } finally {
    setIsLoading(false);
    setShowGif(false);
  }
  };

  // Функция для скачивания результата в txt-файл
  const handleDownloadTXT = () => {
    const txtBlob = new Blob([resultText], { type: "text/plain;charset=utf-8" });
    const txtUrl = URL.createObjectURL(txtBlob);
    const link = document.createElement("a");
    link.href = txtUrl;
    link.download = "resume_analysis.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(txtUrl);
  };

  return (
    <div
      className="container"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
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
          margin: "100px auto 0 auto", 
          minHeight: "300px",
        }}
      >
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
              minWidth: "150px",
              minHeight: "40px",
              maxWidth: "150px",
              maxHeight: "40px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              whiteSpace: "nowrap", 
              overflow: "hidden",
              textOverflow: "ellipsis",
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
          <div style={{ display: "flex", alignItems: "center", gap: "10px", position: "relative", minWidth: "150px" }}>
            <button
              className="submit-button"
              onClick={handleSubmit}
              disabled={isLoading}
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "40px",
                minHeight: "40px",
                maxHeight: "40px",
                width: "150px",
                minWidth: "150px",
                maxWidth: "150px",
                position: "relative",
                zIndex: 1,
              }}
            >
              {isLoading ? "Загрузка..." : "Отправить"}
            </button>
            {showGif && (
              <img
                src="/images/rocket-for-waiting.gif"
                alt="Загрузка"
                style={{
                  width: "60px",
                  height: "60px",
                  position: "absolute",
                  left: "calc(100% + 10px)",
                  top: "50%",
                  transform: "translateY(-50%)"
                }}
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
            boxShadow: "0 2px 8px rgba(0,0,0,0.12)",
            maxWidth: "100vw",
            overflowX: "auto"
          }}>
            <h3 style={{marginTop: 0, fontSize: "1.1rem"}}>Результат анализа</h3>
            <pre style={{
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              background: "none",
              color: "#d1fae5",
              fontSize: "1rem"
            }}>
              {resultText}
            </pre>
            <button
              className="submit-button"
              style={{ width: "100%", maxWidth: "180px", height: "45px", marginTop: "16px" }}
              onClick={handleDownloadTXT}
            >
              Скачать TXT
            </button>
          </div>
        )}
      </main>
    </div>
  );
}


