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

Open a terminal and navigate to the `backend` directory, then run:
```bash
uvicorn main:app --reload
The backend will be running on http://localhost:8000.

### 2. Run the Frontend
Open a second terminal and navigate to the frontend directory, then run:
```bash 
npm run dev
The frontend will be running on http://localhost:5173.

###3. View the App 
Open your browser and go to http://localhost:5173.

#### 3. Push the New File to GitHub
Now, save the `README.md` file and run these commands in your terminal (from the main `AgriAgent` folder) to add it to your GitHub repository.

```bash
git add README.md
git commit -m "Add project README"
git push

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/AgriAgent-Project.git](https://github.com/your-username/AgriAgent-Project.git)
    cd AgriAgent-Project
    ```

2.  **Set up the Backend:**
    ```bash
    cd backend
    pip install -r requirements.txt
    cd ..
    ```

3.  **Set up the Frontend:**
    ```bash
    cd frontend
    npm install
    cd ..
    ```

    ## 📂 Project Structure

The project is organized into two main directories:

<pre>
AgriAgent-Project/
├── backend/         # Contains the Python, FastAPI server logic
│   ├── main.py
│   └── requirements.txt
│
├── frontend/        # Contains the React, Vite user interface
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatInterface.jsx
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── index.html
│   └── package.json
│
└── .gitignore       # Specifies files for Git to ignore
</pre>
