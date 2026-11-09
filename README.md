# AgriVoice AI

A multilingual, voice-first agricultural guidance demo built with React, FastAPI, Gnani Prisma v3.0 (speech-to-text), and Gnani Timbre (text-to-speech).

## Important honesty note
The included `farming_service.py` is a small **rule-based starter knowledge engine**, not a generative LLM and not an expert crop-diagnosis system. It returns cautious general guidance for a few symptom categories in Telugu, Hindi, Tamil, Kannada, and English. Expand it with locally verified agricultural sources or connect a vetted LLM/RAG service before describing it as expert AI advice.

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Node.js 20 or newer
- Gnani API key from https://app.gnani.ai/

## 1. Extract and open
Extract `AgriVoice-AI.zip`. Open the `AgriVoice-AI` folder in VS Code.

## 2. Configure the backend
Open a terminal in VS Code:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `backend/.env` and replace `PASTE_YOUR_GNANI_API_KEY_HERE` with your API key. Do not share the key or commit `.env`.

If PowerShell blocks activation, run this once in that terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Start the backend:
```powershell
uvicorn main:app --reload --port 8000
```

Check:
- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/api/health

## 3. Configure the frontend
Open a **second** VS Code terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL Vite prints, normally http://localhost:5173.

## 4. Test in this order
1. Type: `Why are my crop leaves turning yellow?` and submit. This tests the local starter knowledge engine.
2. Select Telugu and try a short typed question.
3. Click **Speak to AgriVoice**, allow microphone access, speak a short question, then click **Stop recording**. This tests the Prisma REST endpoint.
4. Click **Listen** under an assistant response. This tests the Timbre endpoint.

## 5. Gnani API details
Prisma REST endpoint:
`https://api.vachana.ai/stt/v3`

The request sends multipart fields `audio_file`, `language_code`, `preferred_language`, `format=transcribe`, and `itn_native_numerals=true`, with header `X-API-Key-ID`.

Timbre endpoint used by this demo:
`https://api.vachana.ai/api/v1/tts/sse`

The request uses the public example model `vachana-voice-v3`, voice `Karan`, and an MP3 audio configuration. The exact model/voice entitlement may vary by account. If your Gnani dashboard or current API docs show different values, update `TIMBRE_MODEL` and `TIMBRE_VOICE` in `.env`. The code expects SSE `data:` events containing base64 audio chunks; confirm the response shape against your account's API response if this endpoint changes.

Official references:
- https://www.gnani.ai/resources/prisma-v3
- https://www.gnani.ai/text-to-speech-api
- https://docs.gnani.ai/
- https://app.gnani.ai/

## 6. Troubleshooting
- **503 API key missing:** check `backend/.env`, ensure the variable is `GNANI_API_KEY=...`, then restart FastAPI.
- **401/403 from Gnani:** verify the key is an API key created in the Gnani dashboard and that your account has access to the selected model.
- **Prisma file/format error:** try a short audio file from the dashboard's supported upload flow. Browser audio MIME formats can vary; if your account rejects WebM, use the upload-audio button with a WAV/MP3 file or add audio conversion with FFmpeg.
- **Timbre returns no audio chunks:** check your account's current Timbre model, voice, endpoint, and response shape in Gnani API Docs. The public page example is `vachana-voice-v3` and voice `Karan`.
- **Microphone blocked:** use localhost in Chrome/Edge and allow microphone permission.
- **CORS:** when deployed, set `FRONTEND_ORIGINS` in the backend environment to your exact frontend URL.

## 7. Before public deployment
- Do not publish `.env`.
- Set `GNANI_API_KEY` as a secret environment variable in your backend hosting service.
- Set frontend `VITE_API_URL` to your deployed backend URL before building.
- Set backend `FRONTEND_ORIGINS` to your deployed frontend URL.
- Test every endpoint on the deployed site.
- Add a privacy notice before collecting real farmer recordings. Do not store recordings in this starter app.
- Do not present the rule-based guidance as a medical/agronomic diagnosis. Ask local agricultural experts to review crop-specific recommendations.

## 8. Submission preparation
- Record a real end-to-end demo showing a Gnani Prisma transcription and a Gnani Timbre spoken answer.
- Show the project working, not just screenshots.
- Publish a demo video on LinkedIn or X, tag Gnani AI, and use:
  - `#GnaniAI`
  - `#GreatIndianAIInternshipChallenge`
- Submit the public project/demo links through the official submission form before the deadline stated in your registration email.
