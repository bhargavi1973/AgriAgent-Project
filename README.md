# AgriAgent-Project 🌱

AgriAgent is a full-stack web application designed to help farmers in the Jhansi region get instant information about their crops, local weather, and current market prices.

## ✨ Features
-   **Crop Advisory:** Ask questions about crop diseases, fertilizers, and best practices.
-   **Weather Forecast:** Get up-to-date weather information for your location.
-   **Market Prices:** Check the latest prices for various crops in local markets (mandis).

## 🛠️ Tech Stack
-   **Frontend:** React, Vite
-   **Backend:** Python, FastAPI
-   **Database:** ChromaDB (for vector store)

## 🚀 How to Run Locally

To run this project, you need to start both the backend and frontend servers.

### 1. Run the Backend
Open a terminal and navigate to the `backend` directory, then run:
```bash
uvicorn main:app --reload