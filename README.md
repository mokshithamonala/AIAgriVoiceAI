# 🌱 AgriVoice AI – Multilingual Voice-Based Agricultural Assistant

AgriVoice AI is a multilingual, voice-first agricultural guidance application that helps farmers interact with an agricultural assistant using voice or text in their preferred language.

## 🔗 Project Links

- 🚀 **Live Demo (Vercel):** [Open AgriVoice AI](YOUR_VERCEL_DEPLOYMENT_URL)
- 💻 **GitHub Repository:** [AgriVoice AI](https://github.com/mokshithamonala/AIAgriVoiceAI)

---

## ✨ Features

- **Multilingual Support:** Supports Telugu, Hindi, Tamil, Kannada, and English.
- **Voice Input:** Converts spoken queries into text using Gnani Prisma v3.0.
- **Voice Output:** Converts assistant responses into speech using Gnani Timbre.
- **Text-Based Queries:** Allows farmers to submit agricultural questions through text.
- **Agricultural Guidance:** Provides general guidance through a rule-based starter knowledge engine.
- **Responsive Interface:** Offers a simple, user-friendly experience.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Frontend | React |
| Backend | Python, FastAPI |
| Speech-to-Text | Gnani Prisma v3.0 |
| Text-to-Speech | Gnani Timbre |
| API Communication | REST APIs |

## 🔄 How It Works

1. The farmer enters a query using voice or text.
2. Gnani Prisma converts voice input into text.
3. The FastAPI backend processes the query.
4. The agricultural guidance engine generates a general response.
5. Gnani Timbre converts the response into speech.
6. The farmer receives the guidance in the selected language.

## 📁 Project Structure

```text
AgriVoice-AI/
│
├── backend/
│   ├── main.py
│   ├── farming_service.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Node.js 20 or later
- Gnani API key

### 1. Clone the Repository

```bash
git clone https://github.com/mokshithamonala/AIAgriVoiceAI.git
cd AIAgriVoiceAI
```

### 2. Backend Setup

Navigate to the backend directory:

```powershell
cd backend
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create the environment file:

```powershell
Copy-Item .env.example .env
```

Add your Gnani API key to `backend/.env`:

```env
GNANI_API_KEY=your_api_key
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local development URL displayed in your terminal.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GNANI_API_KEY` | Authenticates requests to Gnani APIs |
| `VITE_API_URL` | Backend API URL, if configured in the frontend |

**Security:** Keep API keys private. Never commit `.env` files or expose secret keys in frontend code.

## ☁️ Deployment

The frontend can be deployed using Vercel, while the FastAPI backend must be hosted separately.

Deployment configuration:

- **Frontend Hosting:** Vercel
- **Backend:** FastAPI hosting platform
- **Frontend API Configuration:** Set `VITE_API_URL` to the deployed backend URL.
- **Backend CORS:** Allow requests from the deployed frontend domain.

### Live Application

🚀 **[Visit AgriVoice AI](https://ai-agri-voice-ai-t6tk.vercel.app/)**

## ⚠️ Implementation Note

The current `farming_service.py` implementation uses a rule-based starter knowledge engine. It provides general guidance for a limited set of agricultural queries. It is not a generative AI model or an expert crop-diagnosis system.

## 🔮 Future Enhancements

- Expand the agricultural knowledge base using verified agricultural resources.
- Support additional regional languages.
- Improve crop-specific recommendations.
- Integrate a verified RAG-based agricultural knowledge system.
- Enhance accessibility and mobile usability.

## 🙌 Acknowledgements

- [Gnani AI](https://www.gnani.ai/)
- [Gnani Prisma Documentation](https://www.gnani.ai/resources/prisma-v3)
- [Gnani Text-to-Speech API](https://www.gnani.ai/text-to-speech-api)
- [Gnani Developer Documentation](https://docs.gnani.ai/)

---

**Built to make agricultural guidance more accessible through multilingual voice technology.**
