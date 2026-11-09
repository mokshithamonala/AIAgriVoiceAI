import React, { useEffect, useRef, useState } from "react";
import {
  Sprout,
  Mic,
  Send,
  Volume2,
  VolumeX,
  Languages,
  Leaf,
  ShieldCheck,
  CloudRain,
  RotateCcw,
  LoaderCircle,
  MessageSquare,
  Info,
  Upload,
  CheckCircle2,
  AlertTriangle,
  Menu,
  X,
  ArrowRight,
  Sparkles,
  Bug,
  Droplets,
  Sun,
  Compass,
  Smartphone,
  Headphones,
  BookOpen,
  HeartHandshake,
  ChevronRight,
  Square,
  MapPin,
  Camera,
  TrendingUp,
  Award,
  Users,
  User,
  Calendar,
  PhoneCall,
  Search,
  Plus,
  ThumbsUp,
  Activity,
  ExternalLink,
} from "lucide-react";
import SmartFarmMap from "./SmartFarmMap";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const LANGUAGES = [
  {
    code: "te-IN",
    label: "తెలుగు",
    english: "Telugu",
    sampleQuery: "నా టమాటా ఆకులు ఎందుకు పసుపు రంగులోకి మారుతున్నాయి?",
    greeting:
      "నమస్కారం! AgriVoice AI కి స్వాగతం. ఈరోజు మీ వ్యవసాయం లేదా పంటల గురించి నేను ఎలా సహాయం చేయగలను?",
    placeholder: "మీ వ్యవసాయ ప్రశ్నను ఇక్కడ టైప్ చేయండి లేదా మైక్రోఫోన్ నొక్కండి...",
  },
  {
    code: "hi-IN",
    label: "हिन्दी",
    english: "Hindi",
    sampleQuery: "मेरे टमाटर के पत्ते पीले क्यों पड़ रहे हैं?",
    greeting:
      "नमस्ते! AgriVoice AI में आपका स्वागत है। आज मैं आपके खेत और फसलों के लिए कैसे मदद कर सकता हूँ?",
    placeholder: "अपना कृषि प्रश्न यहाँ लिखें या माइक्रोफ़ोन दबाकर बोलें...",
  },
  {
    code: "ta-IN",
    label: "தமிழ்",
    english: "Tamil",
    sampleQuery: "என் தக்காளி இலைகள் ஏன் மஞ்சளாக மாறுகின்றன?",
    greeting:
      "வணக்கம்! AgriVoice AI-க்கு வரவேற்கிறோம். இன்று உங்கள் பண்ணை மற்றும் பயிர்களுக்கு நான் எப்படி உதவ முடியும்?",
    placeholder: "உங்கள் விவசாயக் கேள்வியை இங்கே தட்டச்சு செய்யவும்...",
  },
  {
    code: "kn-IN",
    label: "ಕನ್ನಡ",
    english: "Kannada",
    sampleQuery: "ನನ್ನ ಟೊಮೆಟೊ ಎಲೆಗಳು ಏಕೆ ಹಳದಿಯಾಗುತ್ತಿವೆ?",
    greeting:
      "ನಮಸ್ಕಾರ! AgriVoice AI ಗೆ ಸ್ವಾಗತ. ಇಂದು ನಿಮ್ಮ ಕೃಷಿ ಮತ್ತು ಬೆಳೆಗಳ ಬಗ್ಗೆ ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
    placeholder: "ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...",
  },
  {
    code: "ml-IN",
    label: "മലയാളം",
    english: "Malayalam",
    sampleQuery: "എന്റെ തക്കാളി ഇലകൾ മഞ്ഞനിറമാകുന്നത് എന്തുകൊണ്ട്?",
    greeting:
      "നമസ്കാരം! AgriVoice AI-ലേക്ക് സ്വാഗതം. ഇന്ന് നിങ്ങളുടെ കൃഷിയുമായി ബന്ധപ്പെട്ട് എനിക്ക് എങ്ങനെ സഹായിക്കാനാകും?",
    placeholder: "നിങ്ങളുടെ കാർഷിക ചോദ്യം ഇവിടെ ടൈപ്പ് ചെയ്യുക...",
  },
  {
    code: "en-IN",
    label: "English",
    english: "English",
    sampleQuery: "Why are my tomato leaves turning yellow?",
    greeting:
      "Namaste! Welcome to AgriVoice AI. How can I help you with your farm today?",
    placeholder: "Ask a farming question (e.g., Why are my tomato leaves turning yellow?)...",
  },
];

const SUGGESTED_QUESTIONS_BY_LANG = {
  "te-IN": [
    "నా టమాటా ఆకులు ఎందుకు పసుపు రంగులోకి మారుతున్నాయి? (Tomato yellowing)",
    "వరి పొలానికి ఎప్పుడు నీరు పెట్టాలి? (Paddy irrigation schedule)",
    "మిర్చిలో ఆకు ముడత మరియు తామర పురుగుల నివారణ ఎలా? (Chilli pest control)",
    "నా నేలకు ఏ ఎరువులు వేయాలి? (Balanced fertilizer schedule)",
    "మా ప్రాంతంలో వర్షం పడే అవకాశం ఉందా? (Weather & rain precautions)",
    "ఈ సీజన్‌లో ఏ పంట వేస్తే మంచి దిగుబడి వస్తుంది? (Best seasonal crops)",
  ],
  "hi-IN": [
    "मेरे टमाटर के पत्ते पीले क्यों पड़ रहे हैं? (Tomato leaf yellowing)",
    "धान के खेत में सिंचाई कब करनी चाहिए? (Paddy irrigation)",
    "मिर्च में पत्ती मरोड़ और थ्रिप्स की रोकथाम कैसे करें? (Chilli pest control)",
    "मेरी मिट्टी के लिए कौन सा उर्वरक उपयुक्त है? (Soil fertilizer guide)",
    "क्या मेरे क्षेत्र में बारिश होने की संभावना है? (Weather precautions)",
    "इस सीजन के लिए कौन सी फसल सबसे उपयुक्त है? (Seasonal crop selection)",
  ],
  "ta-IN": [
    "என் தக்காளி இலைகள் ஏன் மஞ்சளாக மாறுகின்றன? (Tomato leaf yellowing)",
    "நெல் வயலுக்கு எப்போது நீர் பாய்ச்ச வேண்டும்? (Paddy irrigation)",
    "மிளகாய் இலை சுருள் மற்றும் பூச்சி கட்டுப்பாடு எப்படி? (Chilli pest control)",
    "என் மண்ணுக்கு எந்த உரம் சிறந்தது? (Balanced fertilizer)",
    "மழை முன்னறிவிப்பு மற்றும் பயிர் பாதுகாப்பு என்ன? (Weather precautions)",
    "இந்த பருவத்திற்கு ஏற்ற பயிர் எது? (Best seasonal crop)",
  ],
  "kn-IN": [
    "ನನ್ನ ಟೊಮೆಟೊ ಎಲೆಗಳು ಏಕೆ ಹಳದಿಯಾಗುತ್ತಿವೆ? (Tomato leaf yellowing)",
    "ಭತ್ತದ ಗದ್ದೆಗೆ ಯಾವಾಗ ನೀರು ಹಾಯಿಸಬೇಕು? (Paddy irrigation)",
    "ಮೆಣಸಿನಕಾಯಿ ಎಲೆ ಮುడుచు ಮತ್ತು ಕೀಟ ನಿಯಂತ್ರಣ ಹೇಗೆ? (Chilli pest control)",
    "ನನ್ನ ಮಣ್ಣಿಗೆ ಯಾವ ಗೊಬ್ಬರ ಸೂಕ್ತವಾಗಿದೆ? (Fertilizer schedule)",
    "ಮಳೆ ಮುನ್ಸೂಚನೆ ಮತ್ತು ಬೆಳೆ ರಕ್ಷಣೆ ಹೇಗೆ? (Weather precautions)",
    "ಈ ಹಂಗಾಮಿಗೆ ಯಾವ ಬೆಳೆ ಸೂಕ್ತವಾಗಿದೆ? (Seasonal crop selection)",
  ],
  "ml-IN": [
    "എന്റെ തക്കാളി ഇലകൾ മഞ്ഞനിറമാകുന്നത് എന്തുകൊണ്ട്? (Tomato yellowing)",
    "നെൽവയലിൽ എപ്പോൾ വെള്ളം നനയ്ക്കണം? (Paddy irrigation)",
    "മുളകിലെ ഇലച്ചുരുളലും കീട നിയന്ത്രണവും എങ്ങനെ? (Chilli pest control)",
    "എന്റെ മണ്ണിന് അനുയോജ്യമായ വളം ഏതാണ്? (Soil fertilizer guide)",
    "മഴ മുന്നറിയിപ്പും വിള സംരക്ഷണവും എങ്ങനെ? (Weather precautions)",
    "ഈ സീസണിന് അനുയോജ്യമായ വിള ഏതാണ്? (Best seasonal crop)",
  ],
  "en-IN": [
    "Why are my tomato leaves turning yellow?",
    "When should I irrigate my paddy field?",
    "How can I control leaf curl and thrips in chilli?",
    "What fertilizer schedule is suitable for my soil?",
    "Will it rain in my farming area and what precautions should I take?",
    "Which crop is suitable for this season?",
  ],
};

/**
 * Converts a browser-recorded audio Blob (e.g. WebM/Opus) into a standard
 * 16kHz 16-bit mono PCM WAV Blob so Gnani Prisma V3.0 accepts it natively.
 */
async function convertBlobToWav(blob) {
  try {
    const arrayBuffer = await blob.arrayBuffer();
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) {
      return { blob, fileName: "farmer-recording.wav" };
    }

    const audioCtx = new AudioCtx();
    const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
    await audioCtx.close().catch(() => {});

    const targetSampleRate = 16000;
    const frameCount = Math.max(1, Math.ceil(audioBuffer.duration * targetSampleRate));
    const offlineCtx = new OfflineAudioContext(1, frameCount, targetSampleRate);

    const source = offlineCtx.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(offlineCtx.destination);
    source.start(0);

    const renderedBuffer = await offlineCtx.startRendering();
    const samples = renderedBuffer.getChannelData(0);

    const wavBuffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(wavBuffer);

    function writeAscii(offset, text) {
      for (let i = 0; i < text.length; i++) {
        view.setUint8(offset + i, text.charCodeAt(i));
      }
    }

    writeAscii(0, "RIFF");
    view.setUint32(4, 36 + samples.length * 2, true);
    writeAscii(8, "WAVE");
    writeAscii(12, "fmt ");
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, targetSampleRate, true);
    view.setUint32(28, targetSampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeAscii(36, "data");
    view.setUint32(40, samples.length * 2, true);

    let offset = 44;
    for (let i = 0; i < samples.length; i++, offset += 2) {
      const clamped = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, clamped < 0 ? clamped * 0x8000 : clamped * 0x7fff, true);
    }

    return {
      blob: new Blob([wavBuffer], { type: "audio/wav" }),
      fileName: "farmer-recording.wav",
    };
  } catch {
    return { blob, fileName: "farmer-recording.wav" };
  }
}

function createWelcomeMessage(langCode = "te-IN") {
  const langObj = LANGUAGES.find((l) => l.code === langCode) || LANGUAGES[0];
  const baseWelcome =
    "Namaste! Welcome to AgriVoice AI. How can I help you with your farm today?";
  const text =
    langObj.code === "en-IN"
      ? baseWelcome
      : `${baseWelcome}\n\n${langObj.greeting}`;

  return {
    id: "welcome-msg",
    role: "assistant",
    text,
    language_code: langObj.code,
    time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    isWelcome: true,
  };
}

export default function App() {
  const [language, setLanguage] = useState("te-IN");
  const [activeNav, setActiveNav] = useState("home");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Farmer Profile / Auth Modal
  const [farmerProfile, setFarmerProfile] = useState(() => {
    try {
      const saved = localStorage.getItem("agrivoice_farmer_profile");
      if (saved) return JSON.parse(saved);
    } catch {}
    return {
      name: "Srinivas Rao",
      phone: "9876543210",
      state: "Andhra Pradesh",
      district: "Guntur",
      farm_size_acres: 4.5,
      primary_crops: "Paddy, Tomato, Chilli",
    };
  });
  const [showProfileModal, setShowProfileModal] = useState(false);

  // Voice Assistant State
  const [messages, setMessages] = useState(() => [createWelcomeMessage("te-IN")]);
  const [question, setQuestion] = useState("");
  const [micState, setMicState] = useState("Ready");
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [livePreviewTranscript, setLivePreviewTranscript] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  // Backend & API Health
  const [backendStatus, setBackendStatus] = useState({
    checked: false,
    online: false,
    gnaniConfigured: false,
    visionConfigured: false,
  });

  // Audio Playback & Credit-Conserving Cache
  const [speakingMsgId, setSpeakingMsgId] = useState(null);
  const [playingMsgId, setPlayingMsgId] = useState(null);
  const audioCacheRef = useRef({});
  const currentAudioRef = useRef(null);

  // Smart Farm Digital Twin, Map & Timeline State
  const [farmZones, setFarmZones] = useState([]);
  const [nearbyResources, setNearbyResources] = useState([]);
  const [selectedZoneId, setSelectedZoneId] = useState("zone-a");
  const [explainData, setExplainData] = useState(null);
  const [explainLoading, setExplainLoading] = useState(false);
  const [timeline, setTimeline] = useState([]);
  const [dailyPlan, setDailyPlan] = useState([]);
  const [newActivity, setNewActivity] = useState({
    title: "",
    category: "Crop inspection",
    zone_name: "Zone A – North Plot",
    scheduled_date: new Date().toISOString().slice(0, 10),
  });

  // Weather Intelligence State
  const [weather, setWeather] = useState(null);

  // Smart Irrigation & What-If Simulator State
  const [irrigationForm, setIrrigationForm] = useState({
    crop_type: "Tomato",
    field_size_acres: 1.5,
    soil_type: "Red Sandy Loam",
    irrigation_method: "Drip Irrigation",
    current_moisture_pct: 54,
  });
  const [irrigationResult, setIrrigationResult] = useState(null);
  const [simulatorScenario, setSimulatorScenario] = useState("rainfall_decrease");
  const [simulatorCrop, setSimulatorCrop] = useState("Tomato");
  const [simulatorResult, setSimulatorResult] = useState(null);

  // AI Crop Doctor State
  const [doctorCrop, setDoctorCrop] = useState("Tomato");
  const [doctorNotes, setDoctorNotes] = useState(
    "Lower leaves turning yellow with small dark brown spots after recent humidity."
  );
  const [doctorImageFile, setDoctorImageFile] = useState(null);
  const [doctorImagePreview, setDoctorImagePreview] = useState("");
  const [doctorLoading, setDoctorLoading] = useState(false);
  const [doctorResult, setDoctorResult] = useState(null);
  const [doctorHistory, setDoctorHistory] = useState([]);

  // Market Insights State
  const [marketPrices, setMarketPrices] = useState([]);
  const [marketSearch, setMarketSearch] = useState("");
  const [marketStateFilter, setMarketStateFilter] = useState("All");
  const [marketDecisionCrop, setMarketDecisionCrop] = useState("Paddy");
  const [marketDecisionResult, setMarketDecisionResult] = useState(null);

  // Knowledge Hub & Government Schemes State
  const [guides, setGuides] = useState([]);
  const [guideCategory, setGuideCategory] = useState("All");
  const [guideSearch, setGuideSearch] = useState("");
  const [schemes, setSchemes] = useState([]);
  const [schemeCategory, setSchemeCategory] = useState("All");
  const [eligForm, setEligForm] = useState({
    land_acres: 2.5,
    has_land_record: true,
    needs_irrigation: true,
    wants_insurance: true,
  });
  const [eligResult, setEligResult] = useState(null);

  // Farmer Community State
  const [communityPosts, setCommunityPosts] = useState([]);
  const [communityCategory, setCommunityCategory] = useState("All");
  const [newPost, setNewPost] = useState({
    title: "",
    category: "Crop Diseases",
    crop_tag: "Tomato",
    content: "",
  });
  const [commentInputs, setCommentInputs] = useState({});

  // Refs
  const recorderRef = useRef(null);
  const speechRecRef = useRef(null);
  const browserTranscriptRef = useRef("");
  const chunksRef = useRef([]);
  const streamRef = useRef(null);
  const timerRef = useRef(null);
  const chatContainerRef = useRef(null);
  const fileInputRef = useRef(null);
  const doctorInputRef = useRef(null);
  const questionInputRef = useRef(null);

  const selectedLanguage =
    LANGUAGES.find((item) => item.code === language) || LANGUAGES[0];

  // Initial Data Load from FastAPI Backend (0 Gnani Credits Used)
  useEffect(() => {
    async function loadPlatformData() {
      try {
        const [
          healthRes,
          zonesRes,
          timelineRes,
          weatherRes,
          marketRes,
          guidesRes,
          schemesRes,
          postsRes,
          historyRes,
          irrRes,
          simRes,
          mktDecRes,
        ] = await Promise.all([
          fetch(`${API_BASE}/api/health`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/farm/zones`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/farm/timeline`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/weather`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/market/prices`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/guides`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/schemes`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/community/posts`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/crop-doctor/history`).then((r) => r.json()).catch(() => null),
          fetch(`${API_BASE}/api/irrigation/plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(irrigationForm),
          })
            .then((r) => r.json())
            .catch(() => null),
          fetch(`${API_BASE}/api/simulator/what-if`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              scenario: "rainfall_decrease",
              crop_type: "Tomato",
              area_acres: 2.0,
            }),
          })
            .then((r) => r.json())
            .catch(() => null),
          fetch(`${API_BASE}/api/market/assistant`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ crop: "Paddy" }),
          })
            .then((r) => r.json())
            .catch(() => null),
        ]);

        if (healthRes) {
          setBackendStatus({
            checked: true,
            online: healthRes.status === "ok",
            gnaniConfigured: Boolean(healthRes.gnani_key_configured),
            visionConfigured: Boolean(healthRes.vision_key_configured),
          });
        }
        if (zonesRes?.zones) {
          setFarmZones(zonesRes.zones);
          setNearbyResources(zonesRes.nearby_resources || []);
          setDailyPlan(zonesRes.daily_action_plan || []);
        }
        if (timelineRes?.timeline) {
          setTimeline(timelineRes.timeline);
        }
        if (weatherRes) {
          setWeather(weatherRes);
        }
        if (marketRes?.prices) {
          setMarketPrices(marketRes.prices);
        }
        if (guidesRes?.guides) {
          setGuides(guidesRes.guides);
        }
        if (schemesRes?.schemes) {
          setSchemes(schemesRes.schemes);
        }
        if (postsRes?.posts) {
          setCommunityPosts(postsRes.posts);
        }
        if (historyRes?.history) {
          setDoctorHistory(historyRes.history);
        }
        if (irrRes) {
          setIrrigationResult(irrRes);
        }
        if (simRes) {
          setSimulatorResult(simRes);
        }
        if (mktDecRes) {
          setMarketDecisionResult(mktDecRes);
        }
      } catch {}
    }
    loadPlatformData();
  }, []);

  // Scroll chat container smoothly when messages change
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, busy]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      streamRef.current?.getTracks().forEach((track) => track.stop());
      if (timerRef.current) clearInterval(timerRef.current);
      if (currentAudioRef.current) currentAudioRef.current.pause();
      Object.values(audioCacheRef.current).forEach((url) => {
        if (url) URL.revokeObjectURL(url);
      });
    };
  }, []);

  function navigateToSection(sectionId) {
    setActiveNav(sectionId);
    setMobileMenuOpen(false);
    const el = document.getElementById(sectionId);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function handleLanguageChange(newLangCode) {
    setLanguage(newLangCode);
    setError("");
    setMessages((prev) => {
      if (prev.length === 1 && prev[0].isWelcome) {
        return [createWelcomeMessage(newLangCode)];
      }
      return prev;
    });
  }

  function addMessage(role, text, extra = {}) {
    const id = `msg-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
    setMessages((prev) => [
      ...prev,
      {
        id,
        role,
        text,
        language_code: language,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        ...extra,
      },
    ]);
    return id;
  }

  // ============================================================================
  // VOICE RECORDING, GNANI PRISMA STT & ADVISOR
  // ============================================================================
  async function transcribeAudio(
    blob,
    fileName = "farmer-recording.wav",
    fallbackTranscript = ""
  ) {
    setBusy(true);
    setError("");
    setMicState("Transcribing");

    try {
      const form = new FormData();
      form.append("audio_file", blob, fileName);
      form.append("language_code", language);

      const response = await fetch(`${API_BASE}/api/transcribe`, {
        method: "POST",
        body: form,
      });
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Speech recognition could not process the audio. You can also type your farming question below."
        );
      }

      const transcriptText = (data.transcript || "").trim();
      if (!transcriptText) {
        throw new Error("No clear speech was detected in the recording.");
      }

      setQuestion(transcriptText);
      setLivePreviewTranscript("");
      addMessage("user", transcriptText, {
        kind: "voice",
        provider: data.provider || "Gnani Prisma V3.0",
      });

      await getAdvice(transcriptText, false);
    } catch (err) {
      const cleanFallback = (fallbackTranscript || "").trim();
      if (cleanFallback) {
        setQuestion(cleanFallback);
        setLivePreviewTranscript("");
        addMessage("user", cleanFallback, {
          kind: "voice",
          provider: "Live Browser Speech Recognition",
        });
        await getAdvice(cleanFallback, false);
        return;
      }

      const friendlyMsg =
        err.message === "Failed to fetch"
          ? "Unable to connect to the AgriVoice server at http://localhost:8000."
          : err.message;
      setError(friendlyMsg);
      setMicState("Error");
    } finally {
      setBusy(false);
    }
  }

  async function startRecording() {
    setError("");
    setLivePreviewTranscript("");
    if (busy) return;

    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) {
      setError(
        "Microphone recording is not supported in this browser. Please use Chrome/Edge or upload an audio file."
      );
      setMicState("Error");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      browserTranscriptRef.current = "";

      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRec) {
        try {
          const recognition = new SpeechRec();
          recognition.lang = language;
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.onresult = (event) => {
            let combined = "";
            for (let i = 0; i < event.results.length; i++) {
              combined += event.results[i][0].transcript + " ";
            }
            if (combined.trim()) {
              browserTranscriptRef.current = combined.trim();
              setLivePreviewTranscript(combined.trim());
            }
          };
          recognition.onerror = () => {};
          recognition.start();
          speechRecRef.current = recognition;
        } catch {
          speechRecRef.current = null;
        }
      }

      const preferred = [
        "audio/webm;codecs=opus",
        "audio/webm",
        "audio/ogg",
        "audio/mp4",
      ].find((type) => MediaRecorder.isTypeSupported(type));

      const recorder = preferred
        ? new MediaRecorder(stream, { mimeType: preferred })
        : new MediaRecorder(stream);

      recorderRef.current = recorder;
      chunksRef.current = [];
      setRecordingSeconds(0);

      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        if (timerRef.current) {
          clearInterval(timerRef.current);
          timerRef.current = null;
        }
        if (speechRecRef.current) {
          try {
            speechRecRef.current.stop();
          } catch {}
          speechRecRef.current = null;
        }
        const mimeType = recorder.mimeType || "audio/webm";
        const rawBlob = new Blob(chunksRef.current, { type: mimeType });
        stream.getTracks().forEach((track) => track.stop());
        streamRef.current = null;

        const capturedFallback = browserTranscriptRef.current;

        if (rawBlob.size > 0) {
          setMicState("Processing");
          const { blob: wavBlob, fileName } = await convertBlobToWav(rawBlob);
          await transcribeAudio(wavBlob, fileName, capturedFallback);
        } else if (capturedFallback) {
          addMessage("user", capturedFallback, {
            kind: "voice",
            provider: "Live Browser Speech Recognition",
          });
          await getAdvice(capturedFallback, false);
        } else {
          setMicState("Error");
          setError("The recorded audio clip was empty. Please try speaking again.");
        }
      };

      recorder.start();
      setMicState("Recording");

      timerRef.current = setInterval(() => {
        setRecordingSeconds((prev) => {
          if (prev >= 27) {
            stopRecording();
            return 28;
          }
          return prev + 1;
        });
      }, 1000);
    } catch {
      setMicState("Error");
      setError(
        "Microphone permission is required. Please allow microphone access in your browser settings."
      );
    }
  }

  function stopRecording() {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    if (speechRecRef.current) {
      try {
        speechRecRef.current.stop();
      } catch {}
    }
    if (recorderRef.current && recorderRef.current.state !== "inactive") {
      setMicState("Processing");
      recorderRef.current.stop();
    }
  }

  async function uploadAudio(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    event.target.value = "";

    if (file.size === 0 || file.size > 12 * 1024 * 1024) {
      setError("Please select a valid audio file under 12 MB.");
      return;
    }
    setMicState("Processing");
    if (file.type.includes("webm") || file.name.toLowerCase().endsWith(".webm")) {
      const { blob: wavBlob, fileName } = await convertBlobToWav(file);
      await transcribeAudio(wavBlob, fileName);
    } else {
      await transcribeAudio(file, file.name);
    }
  }

  function buildOfflineStructuredAdvice(cleanText, langCode) {
    const q = cleanText.toLowerCase();
    const isTelugu = langCode === "te-IN";
    const isHindi = langCode === "hi-IN";
    const isIrr =
      q.includes("irrigat") || q.includes("water") || q.includes("నీరు") || q.includes("తడి") || q.includes("पानी") || q.includes("सिंचाई");
    const isPest =
      q.includes("pest") || q.includes("curl") || q.includes("thrips") || q.includes("పురుగు") || q.includes("ముడత") || q.includes("कीट");
    const isFert =
      q.includes("fertiliz") || q.includes("soil") || q.includes("urea") || q.includes("ఎరువు") || q.includes("నేల") || q.includes("खाद");
    const isRain =
      q.includes("rain") || q.includes("weather") || q.includes("వర్షం") || q.includes("వాతావరణం") || q.includes("बारिश");

    if (isTelugu) {
      const sections = [
        {
          key: "problem",
          title: "1. గుర్తించిన సమస్య / వ్యవసాయ అంశం (Problem / Topic Identified)",
          body: isIrr
            ? "పంటకు సరైన నీటి యాజమాన్యం, తడి పెట్టే సమయం మరియు వేరు మండల తేమ రక్షణ."
            : isPest
            ? "ఆకు ముడత, రసం పీల్చే పురుగులు (తెల్లదోమ, తామర పురుగులు) మరియు సమగ్ర సస్యరక్షణ."
            : isFert
            ? "భూసార ఆధారిత సమతుల్య ఎరువుల యాజమాన్యం (NPK + సూక్ష్మ పోషకాలు)."
            : isRain
            ? "వాతావరణ సూచన ఆధారిత పంట రక్షణ మరియు మురుగునీటి కాలువల యాజమాన్యం."
            : "పంట ఆకుల ఆరోగ్యం, పోషకాల లోపం నివారణ మరియు సమగ్ర పంట యాజమాన్యం.",
        },
        {
          key: "causes",
          title: "2. ప్రధాన కారణాలు & పంట పరిస్థితులు (Possible Causes & Factors)",
          body: "నేలలో తేమ హెచ్చుతగ్గులు, నత్రజని/జింక్/మెగ్నీషియం వంటి పోషకాల అసమతుల్యత లేదా ఆకుల అడుగున రసం పీల్చే పురుగుల ఉనికి.",
        },
        {
          key: "steps",
          title: "3. రైతులు తీసుకోవాల్సిన తదుపరి చర్యలు (Recommended Next Steps)",
          body: "1. ఉదయం పూట 5–10 మొక్కల ఆకుల అడుగు భాగాన్ని మరియు 5–8 సెం.మీ లోతులో మట్టి తేమను పరిశీలించండి.\n2. ఎకరాకు 10 పసుపు/నీలం జిగురు అట్టలు పెట్టి 5% వేప గింజల కషాయం (NSKE) పిచికారీ చేయండి.\n3. ఎరువులను ఒకేసారి కాకుండా తేమ ఉన్నప్పుడు విడతల వారీగా వేర్ల దగ్గర అందించండి.",
        },
        {
          key: "precautions",
          title: "4. పాటించాల్సిన జాగ్రత్తలు (Precautions)",
          body: "సమస్యను నిర్ధారించుకోకుండా రకరకాల రసాయన మందులను కలిపి వాడవద్దు మరియు వర్షం/బలమైన గాలి ఉన్నప్పుడు పిచికారీ చేయవద్దు.",
        },
        {
          key: "expert",
          title: "5. స్థానిక వ్యవసాయ నిపుణుడిని ఎప్పుడు సంప్రదించాలి (When to Consult an Expert)",
          body: "లక్షణాలు తీవ్రంగా ఉంటే ఆకు నమూనాతో స్థానిక వ్యవసాయ అధికారి (AO) లేదా కృషి విజ్ఞాన కేంద్రం (KVK టోల్-ఫ్రీ: 1800-180-1551) ని సంప్రదించండి.",
        },
      ];
      return {
        answer: sections.map((s) => `${s.title}:\n${s.body}`).join("\n\n"),
        sections,
        notice:
          "గమనిక: ఇది ఆచరణాత్మక వ్యవసాయ అవగాహన సమాచారం. మందుల మోతాదు కోసం స్థానిక వ్యవసాయ అధికారి లేదా KVK (1800-180-1551) ని సంప్రదించండి.",
      };
    }

    if (isHindi) {
      const sections = [
        {
          key: "problem",
          title: "1. पहचानी गई कृषि समस्या / विषय (Topic Identified)",
          body: "फसल स्वास्थ्य, सिंचाई समय-सारणी, पोषण और एकीकृत कीट प्रबंधन मार्गदर्शन।",
        },
        {
          key: "causes",
          title: "2. प्रमुख कारण और कृषि कारक (Key Factors & Causes)",
          body: "मिट्टी की नमी में उतार-चढ़ाव, सूक्ष्म पोषक तत्वों (जिंक/आयरन/नाइट्रोजन) की कमी या पत्तियों के नीचे रस चूसक कीट।",
        },
        {
          key: "steps",
          title: "3. सुझाए गए व्यावहारिक कदम (Recommended Next Steps)",
          body: "1. सुबह 5–10 पौधों की पत्तियों के निचले हिस्से और 5–8 सेमी मिट्टी की नमी जांचें।\n2. प्रति एकड़ 10 पीले/नीले चिपचिपे ट्रैप लगाएं और 5% नीम अर्क का छिड़काव करें।\n3. मृदा स्वास्थ्य कार्ड के अनुसार किस्तों में संतुलित खाद दें।",
        },
        {
          key: "precautions",
          title: "4. आवश्यक सावधानियां (Precautions)",
          body: "बिना पहचान के कई रासायनिक दवाएं आपस में न मिलाएं और बारिश या तेज हवा के समय छिड़काव न करें।",
        },
        {
          key: "expert",
          title: "5. स्थानीय कृषि विशेषज्ञ से कब संपर्क करें (When to Consult an Expert)",
          body: "लक्षण बढ़ने पर प्रभावित पत्ती लेकर नजदीकी कृषि विज्ञान केंद्र (KVK हेल्पलाइन: 1800-180-1551) से संपर्क करें।",
        },
      ];
      return {
        answer: sections.map((s) => `${s.title}:\n${s.body}`).join("\n\n"),
        sections,
        notice:
          "नोट: किसी भी रसायन के उपयोग से पहले स्थानीय कृषि अधिकारी या KVK (1800-180-1551) से सलाह लें।",
      };
    }

    const sections = [
      {
        key: "problem",
        title: "1. Problem / Topic Identified",
        body: `Targeted Agronomic Guidance for: "${cleanText}"`,
      },
      {
        key: "causes",
        title: "2. Key Agronomic Factors & Causes",
        body: "Crop performance and visible leaf symptoms are driven by root-zone moisture (5–8 cm depth), balanced NPK + micronutrient availability (Zinc, Boron, Magnesium), and early sucking/chewing pest activity.",
      },
      {
        key: "steps",
        title: "3. Recommended Actionable Next Steps",
        body: "1. Inspect 5–10 plants early morning (6:30–8:30 AM), checking both upper and lower leaf surfaces.\n2. Check soil moisture 5–8 cm deep before irrigating; water during cool morning hours.\n3. Install 10 yellow/blue sticky traps per acre and use 5% Neem Seed Kernel Extract (NSKE) as preventive IPM.\n4. Apply split doses of balanced nutrients along with decomposed organic manure.",
      },
      {
        key: "precautions",
        title: "4. Field Precautions",
        body: "Avoid mixing multiple chemical pesticides blindly, and never spray right before expected rain or during strong winds.",
      },
      {
        key: "expert",
        title: "5. When to Consult a Local Agricultural Expert",
        body: "If symptoms spread across multiple rows, take a sample leaf to your local Agricultural Officer or call the KVK Toll-Free Helpline at 1800-180-1551.",
      },
    ];
    return {
      answer: sections.map((s) => `${s.title}:\n${s.body}`).join("\n\n"),
      sections,
      notice:
        "Educational agronomic guidance. Confirm chemical dosages with your local Agricultural Officer or KVK (1800-180-1551).",
    };
  }

  async function getAdvice(text, showUserMessage = true) {
    const cleanText = text.trim();
    if (!cleanText) return;

    setBusy(true);
    setError("");
    setMicState("Generating response");

    if (showUserMessage) {
      addMessage("user", cleanText, { kind: "text" });
    }

    try {
      const response = await fetch(`${API_BASE}/api/advice`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: cleanText,
          language_code: language,
        }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Unable to generate farming guidance.");
      }

      setBackendStatus((prev) => ({ ...prev, checked: true, online: true }));

      addMessage("assistant", data.answer, {
        source: data.source,
        notice: data.notice,
        sections: data.sections,
        category: data.category,
        language_code: data.language_code || language,
      });

      setQuestion("");
      setMicState("Completed");
    } catch {
      const fallbackData = buildOfflineStructuredAdvice(cleanText, language);
      addMessage("assistant", fallbackData.answer, {
        source: "AgriVoice Built-In Agronomic Engine",
        notice: fallbackData.notice,
        sections: fallbackData.sections,
        category: "crop_guidance",
        language_code: language,
      });
      setQuestion("");
      setMicState("Completed");
    } finally {
      setBusy(false);
    }
  }

  async function submitQuestion(e) {
    e.preventDefault();
    if (!question.trim() || busy) return;
    await getAdvice(question, true);
  }

  function stopAudioPlayback() {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current.currentTime = 0;
      currentAudioRef.current = null;
    }
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setPlayingMsgId(null);
  }

  async function speakResponse(message) {
    setError("");
    if (playingMsgId === message.id) {
      stopAudioPlayback();
      return;
    }
    stopAudioPlayback();

    const cacheKey = `${message.language_code || language}:${message.text}`;
    if (audioCacheRef.current[cacheKey]) {
      try {
        const cachedPlayer = new Audio(audioCacheRef.current[cacheKey]);
        currentAudioRef.current = cachedPlayer;
        setPlayingMsgId(message.id);
        cachedPlayer.onended = () => setPlayingMsgId(null);
        await cachedPlayer.play();
        return;
      } catch {
        setPlayingMsgId(null);
      }
    }

    setSpeakingMsgId(message.id);
    try {
      const response = await fetch(`${API_BASE}/api/speak`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: message.text,
          language_code: message.language_code || language,
        }),
      });
      if (!response.ok) throw new Error("Timbre voice unavailable");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      audioCacheRef.current[cacheKey] = url;

      const player = new Audio(url);
      currentAudioRef.current = player;
      setPlayingMsgId(message.id);
      player.onended = () => setPlayingMsgId(null);
      await player.play();
    } catch {
      if ("speechSynthesis" in window) {
        speakPlainText(message.text, message.language_code || language, message.id);
      }
    } finally {
      setSpeakingMsgId(null);
    }
  }

  function speakPlainText(text, langCode = language, msgId = "quick-tts") {
    if (!("speechSynthesis" in window)) return;
    stopAudioPlayback();
    try {
      window.speechSynthesis.resume();
    } catch {}
    const utterance = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices?.() || [];
    const langPrefix = (langCode || "en-IN").split("-")[0].toLowerCase();
    const matchedVoice =
      voices.find((v) => v.lang?.toLowerCase() === langCode.toLowerCase()) ||
      voices.find((v) => v.lang?.toLowerCase().startsWith(langPrefix)) ||
      voices.find((v) => v.lang?.toLowerCase().includes("in")) ||
      voices[0];
    if (matchedVoice) {
      utterance.voice = matchedVoice;
      utterance.lang = matchedVoice.lang || langCode;
    } else {
      utterance.lang = langCode;
    }
    utterance.rate = 0.96;
    utterance.onend = () => setPlayingMsgId(null);
    utterance.onerror = () => setPlayingMsgId(null);
    setPlayingMsgId(msgId);
    window.speechSynthesis.speak(utterance);
  }

  function clearChat() {
    stopAudioPlayback();
    setMessages([createWelcomeMessage(language)]);
    setQuestion("");
    setError("");
    setMicState("Ready");
  }

  function handleAskFromAnywhere(promptText) {
    setQuestion(promptText);
    navigateToSection("assistant");
    getAdvice(promptText, true);
  }

  // ============================================================================
  // HANDLERS FOR DIGITAL TWIN, TIMELINE, IRRIGATION, SIMULATOR, CROP DOCTOR, ETC.
  // ============================================================================
  async function handleAddZone(zonePayload) {
    try {
      const res = await fetch(`${API_BASE}/api/farm/zones`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(zonePayload),
      });
      const data = await res.json();
      if (data.zones) {
        setFarmZones(data.zones);
        if (data.zone?.id) setSelectedZoneId(data.zone.id);
      }
    } catch {}
  }

  async function handleDeleteZone(zoneId) {
    try {
      const res = await fetch(`${API_BASE}/api/farm/zones/${zoneId}`, {
        method: "DELETE",
      });
      const data = await res.json();
      if (data.zones) {
        setFarmZones(data.zones);
        if (data.zones[0]) setSelectedZoneId(data.zones[0].id);
      }
    } catch {}
  }

  async function handleExplainZone(zoneId) {
    setExplainLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/farm/explain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zone_id: zoneId }),
      });
      const data = await res.json();
      setExplainData(data);
    } catch {} finally {
      setExplainLoading(false);
    }
  }

  async function handleAddTimeline(e) {
    e.preventDefault();
    if (!newActivity.title.trim()) return;
    try {
      const res = await fetch(`${API_BASE}/api/farm/timeline`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newActivity),
      });
      const data = await res.json();
      if (data.timeline) {
        setTimeline(data.timeline);
        setNewActivity({ ...newActivity, title: "" });
      }
    } catch {}
  }

  async function handleToggleTimeline(itemId) {
    try {
      const res = await fetch(`${API_BASE}/api/farm/timeline/${itemId}`, {
        method: "PATCH",
      });
      const data = await res.json();
      if (data.timeline) setTimeline(data.timeline);
    } catch {}
  }

  async function handleCalculateIrrigation(e) {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/api/irrigation/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(irrigationForm),
      });
      const data = await res.json();
      setIrrigationResult(data);
    } catch {}
  }

  async function handleRunSimulator(scenarioKey, cropVal = simulatorCrop) {
    setSimulatorScenario(scenarioKey);
    try {
      const res = await fetch(`${API_BASE}/api/simulator/what-if`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          scenario: scenarioKey,
          crop_type: cropVal,
          area_acres: farmerProfile.farm_size_acres || 2.0,
        }),
      });
      const data = await res.json();
      setSimulatorResult(data);
    } catch {}
  }

  function handleDoctorImageChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setDoctorImageFile(file);
    const reader = new FileReader();
    reader.onload = () => setDoctorImagePreview(String(reader.result || ""));
    reader.readAsDataURL(file);
  }

  async function handleAnalyzeCropDoctor(e) {
    e.preventDefault();
    setDoctorLoading(true);
    try {
      const form = new FormData();
      form.append("crop_name", doctorCrop);
      form.append("symptom_notes", doctorNotes);
      if (doctorImageFile) {
        form.append("image_file", doctorImageFile);
      }
      const res = await fetch(`${API_BASE}/api/crop-doctor/analyze`, {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (data.analysis) setDoctorResult(data.analysis);
      if (data.history) setDoctorHistory(data.history);
    } catch {} finally {
      setDoctorLoading(false);
    }
  }

  async function handleMarketDecision(cropName) {
    setMarketDecisionCrop(cropName);
    try {
      const res = await fetch(`${API_BASE}/api/market/assistant`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ crop: cropName }),
      });
      const data = await res.json();
      setMarketDecisionResult(data);
    } catch {}
  }

  async function handleCheckEligibility(e) {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/api/schemes/eligibility`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eligForm),
      });
      const data = await res.json();
      setEligResult(data);
    } catch {}
  }

  async function handleCreatePost(e) {
    e.preventDefault();
    if (!newPost.title.trim() || !newPost.content.trim()) return;
    try {
      const res = await fetch(`${API_BASE}/api/community/posts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...newPost,
          author_name: farmerProfile.name,
          author_location: `${farmerProfile.district}, ${farmerProfile.state}`,
        }),
      });
      const data = await res.json();
      if (data.posts) {
        setCommunityPosts(data.posts);
        setNewPost({ ...newPost, title: "", content: "" });
      }
    } catch {}
  }

  async function handleLikePost(postId) {
    try {
      const res = await fetch(`${API_BASE}/api/community/posts/${postId}/like`, {
        method: "POST",
      });
      const data = await res.json();
      if (data.posts) setCommunityPosts(data.posts);
    } catch {}
  }

  async function handleCommentPost(postId) {
    const text = (commentInputs[postId] || "").trim();
    if (!text) return;
    try {
      const res = await fetch(`${API_BASE}/api/community/posts/${postId}/comment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ author: farmerProfile.name, text }),
      });
      const data = await res.json();
      if (data.posts) {
        setCommunityPosts(data.posts);
        setCommentInputs({ ...commentInputs, [postId]: "" });
      }
    } catch {}
  }

  async function handleSaveProfile(e) {
    e.preventDefault();
    localStorage.setItem("agrivoice_farmer_profile", JSON.stringify(farmerProfile));
    try {
      await fetch(`${API_BASE}/api/auth/profile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...farmerProfile, language_code: language }),
      });
    } catch {}
    setShowProfileModal(false);
  }

  // Filtered Market, Guides, Schemes, Community
  const filteredMarkets = marketPrices.filter((m) => {
    const matchState =
      marketStateFilter === "All" ||
      m.state.toLowerCase() === marketStateFilter.toLowerCase();
    const matchSearch =
      !marketSearch ||
      m.crop.toLowerCase().includes(marketSearch.toLowerCase()) ||
      m.mandi.toLowerCase().includes(marketSearch.toLowerCase()) ||
      m.district.toLowerCase().includes(marketSearch.toLowerCase());
    return matchState && matchSearch;
  });

  const filteredGuides = guides.filter((g) => {
    const matchCat =
      guideCategory === "All" ||
      g.category.toLowerCase() === guideCategory.toLowerCase();
    const matchSearch =
      !guideSearch ||
      g.title.toLowerCase().includes(guideSearch.toLowerCase()) ||
      g.crops.toLowerCase().includes(guideSearch.toLowerCase()) ||
      g.summary.toLowerCase().includes(guideSearch.toLowerCase());
    return matchCat && matchSearch;
  });

  const filteredSchemes = schemes.filter(
    (s) =>
      schemeCategory === "All" ||
      s.category.toLowerCase() === schemeCategory.toLowerCase() ||
      s.level.toLowerCase() === schemeCategory.toLowerCase()
  );

  const filteredPosts = communityPosts.filter(
    (p) => communityCategory === "All" || p.category === communityCategory
  );

  return (
    <div className="site-wrapper">
      {/* ====================================================================
          MAIN NAVIGATION BAR (TWO-TIER ORDERED EXECUTIVE HEADER)
         ==================================================================== */}
      <header className="navbar">
        <div className="navbar-top-row">
          <div className="container navbar-top-inner">
            <div className="nav-brand-cluster">
              <a
                href="#home"
                className="nav-brand"
                onClick={(e) => {
                  e.preventDefault();
                  navigateToSection("home");
                }}
              >
                <div className="brand-mark">
                  <Sprout size={22} />
                </div>
                <div className="brand-text">
                  <span className="brand-name">
                    AGRIVOICE <em>AI</em>
                  </span>
                  <span className="brand-sub">SMART AGRICULTURE PLATFORM</span>
                </div>
              </a>
              <span className="nav-live-badge">
                <span className="nav-live-dot" />6 Indian Languages · Voice &amp; Digital Twin
              </span>
            </div>

            <div className="nav-actions">
              <label className="nav-lang-picker" aria-label="Select Language">
                <Languages size={15} />
                <select
                  value={language}
                  onChange={(e) => handleLanguageChange(e.target.value)}
                >
                  {LANGUAGES.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.label} ({lang.english})
                    </option>
                  ))}
                </select>
              </label>

              <button
                type="button"
                className="btn-profile-pill"
                onClick={() => setShowProfileModal(true)}
                title="Farmer Profile & Login"
              >
                <User size={15} />
                <span>{farmerProfile.name.split(" ")[0]}</span>
              </button>

              <button
                type="button"
                className="btn btn-primary nav-cta"
                onClick={() => {
                  navigateToSection("assistant");
                  setTimeout(() => questionInputRef.current?.focus(), 300);
                }}
              >
                <Mic size={16} />
                <span>Ask AgriVoice</span>
              </button>

              <button
                type="button"
                className="mobile-menu-toggle"
                aria-label="Toggle Menu"
                onClick={() => setMobileMenuOpen((v) => !v)}
              >
                {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
              </button>
            </div>
          </div>
        </div>

        <div className="navbar-menu-row">
          <div className="container">
            <nav className="nav-links" aria-label="Main Platform Navigation">
              {[
                { id: "home", label: "Home" },
                { id: "assistant", label: "01 · AI Assistant" },
                { id: "my-farm", label: "02 · My Farm" },
                { id: "smart-map", label: "03 · Smart Map" },
                { id: "crop-doctor", label: "04 · Crop Doctor" },
                { id: "weather", label: "05 · Weather" },
                { id: "market", label: "06 · Markets" },
                { id: "guides", label: "07 · Farming Guide" },
                { id: "schemes", label: "08 · Schemes" },
                { id: "community", label: "09 · Community" },
                { id: "about", label: "10 · About" },
              ].map((item) => (
                <a
                  key={item.id}
                  href={`#${item.id}`}
                  className={activeNav === item.id ? "active-nav-link" : ""}
                  onClick={(e) => {
                    e.preventDefault();
                    navigateToSection(item.id);
                  }}
                >
                  {item.label}
                </a>
              ))}
            </nav>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="mobile-nav-drawer">
            <div className="container mobile-nav-inner">
              {[
                { id: "home", label: "Home" },
                { id: "assistant", label: "AI Voice Assistant" },
                { id: "my-farm", label: "My Farm & Digital Twin" },
                { id: "smart-map", label: "Smart Farm Map" },
                { id: "crop-doctor", label: "AI Crop Doctor" },
                { id: "weather", label: "Weather Intelligence" },
                { id: "market", label: "Market Insights" },
                { id: "guides", label: "Farming Guide" },
                { id: "schemes", label: "Government Schemes" },
                { id: "community", label: "Farmer Community" },
                { id: "about", label: "About & Emergency Help" },
              ].map((item) => (
                <a
                  key={item.id}
                  href={`#${item.id}`}
                  onClick={(e) => {
                    e.preventDefault();
                    navigateToSection(item.id);
                  }}
                >
                  {item.label}
                </a>
              ))}
              <div className="mobile-nav-footer">
                <button
                  type="button"
                  className="btn btn-secondary full-width"
                  onClick={() => {
                    setMobileMenuOpen(false);
                    setShowProfileModal(true);
                  }}
                >
                  <User size={16} /> Farmer Login / Profile ({farmerProfile.name})
                </button>
                <button
                  type="button"
                  className="btn btn-primary full-width"
                  onClick={() => navigateToSection("assistant")}
                >
                  <Mic size={16} /> Talk to AgriVoice
                </button>
              </div>
            </div>
          </div>
        )}
      </header>

      <main>
        {/* ====================================================================
            SECTION 1: PREMIUM FULL-WIDTH AGRICULTURAL HERO
           ==================================================================== */}
        <section id="home" className="hero-banner-section">
          <div className="container hero-grid">
            <div className="hero-content">
              <div className="product-pill-dark">
                <Sparkles size={14} />
                <span>Empowering Every Farmer with the Intelligence of AI</span>
              </div>

              <h1 className="hero-title-light">
                Reviving the Future of <span>Farming with AI.</span>
              </h1>

              <p className="hero-subtitle-light">
                Your Farm. Your Language. Your AI Agricultural Companion — built for crop
                health, weather insights, soil intelligence, market opportunities, and
                multilingual voice guidance.
              </p>

              <div className="hero-cta-group">
                <button
                  type="button"
                  className="btn btn-leaf btn-lg"
                  onClick={() => {
                    navigateToSection("assistant");
                    setTimeout(() => questionInputRef.current?.focus(), 350);
                  }}
                >
                  <Mic size={19} />
                  <span>Talk to AgriVoice</span>
                </button>

                <button
                  type="button"
                  className="btn btn-glass btn-lg"
                  onClick={() => navigateToSection("my-farm")}
                >
                  <Sprout size={18} />
                  <span>Explore My Farm</span>
                </button>

                <a
                  href="#smart-map"
                  className="hero-secondary-link"
                  onClick={(e) => {
                    e.preventDefault();
                    navigateToSection("smart-map");
                  }}
                >
                  Discover Smart Farming <ArrowRight size={16} />
                </a>
              </div>

              {/* Floating Live & Labeled Telemetry Cards */}
              <div className="hero-floating-telemetry">
                <div className="telemetry-chip">
                  <ShieldCheck size={16} className="icon-leaf" />
                  <div>
                    <small>Crop Health (Demo Twin)</small>
                    <strong>3 Healthy · 1 Check</strong>
                  </div>
                </div>
                <div className="telemetry-chip">
                  <CloudRain size={16} className="icon-amber" />
                  <div>
                    <small>
                      Weather ({weather?.is_live ? "Live Feed" : "Agromet"})
                    </small>
                    <strong>
                      {weather
                        ? `${weather.current.temperature_c}°C · ${weather.current.rain_probability_pct}% Rain`
                        : "30.5°C · Rain Watch"}
                    </strong>
                  </div>
                </div>
                <div className="telemetry-chip">
                  <Droplets size={16} className="icon-leaf" />
                  <div>
                    <small>Avg Soil Moisture (Est.)</small>
                    <strong>65% Optimal</strong>
                  </div>
                </div>
                <div className="telemetry-chip">
                  <Sparkles size={16} className="icon-leaf" />
                  <div>
                    <small>AI Recommendation</small>
                    <strong>Irrigate Zone B Today</strong>
                  </div>
                </div>
              </div>
            </div>

            {/* Hero Right Visual Card */}
            <div className="hero-visual">
              <div className="hero-showcase-card">
                <div className="showcase-top-banner">
                  <div className="showcase-badge-row">
                    <span className="live-voice-pill">
                      <Mic size={13} /> Gnani Prisma V3.0 + Timbre
                    </span>
                    <span className="lang-count-pill">6 Indian Languages</span>
                  </div>
                  <h3>Your Farm at Your Command — By Voice or Touch</h3>
                  <p>
                    Speak naturally in Telugu, Hindi, Tamil, Kannada, Malayalam, or
                    English.
                  </p>
                </div>

                <div className="showcase-body">
                  <div className="showcase-voice-wave-box">
                    <div className="wave-bars" aria-hidden="true">
                      <span />
                      <span />
                      <span />
                      <span />
                      <span />
                      <span />
                      <span />
                    </div>
                    <div className="wave-copy">
                      <small>Farmer Voice Query ({selectedLanguage.english})</small>
                      <strong>“{selectedLanguage.sampleQuery}”</strong>
                    </div>
                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={() =>
                        handleAskFromAnywhere(selectedLanguage.sampleQuery)
                      }
                    >
                      Try Now
                    </button>
                  </div>

                  <div className="showcase-mini-grid">
                    <button
                      type="button"
                      className="showcase-mini-tile"
                      onClick={() => navigateToSection("smart-map")}
                    >
                      <MapPin size={18} />
                      <div>
                        <strong>Smart Farm Map</strong>
                        <small>Interactive Leaflet &amp; Digital Twin</small>
                      </div>
                    </button>
                    <button
                      type="button"
                      className="showcase-mini-tile"
                      onClick={() => navigateToSection("crop-doctor")}
                    >
                      <Camera size={18} />
                      <div>
                        <strong>AI Crop Doctor</strong>
                        <small>Upload Leaf Photo &amp; Track Health</small>
                      </div>
                    </button>
                    <button
                      type="button"
                      className="showcase-mini-tile"
                      onClick={() => navigateToSection("weather")}
                    >
                      <CloudRain size={18} />
                      <div>
                        <strong>Weather-to-Action</strong>
                        <small>Live Forecast &amp; Spraying Alerts</small>
                      </div>
                    </button>
                    <button
                      type="button"
                      className="showcase-mini-tile"
                      onClick={() => navigateToSection("market")}
                    >
                      <TrendingUp size={18} />
                      <div>
                        <strong>Mandi Insights</strong>
                        <small>Compare Modal Prices &amp; Trends</small>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Trusted Agricultural Intelligence Strip */}
          <div className="container">
            <div className="trusted-strip">
              {[
                { icon: Mic, label: "Multilingual AI Assistance", target: "assistant" },
                { icon: MapPin, label: "Smart Farm Mapping", target: "smart-map" },
                { icon: Camera, label: "Crop Disease Detection", target: "crop-doctor" },
                { icon: CloudRain, label: "Weather Intelligence", target: "weather" },
                { icon: TrendingUp, label: "Market Insights", target: "market" },
                { icon: Award, label: "Government Support", target: "schemes" },
              ].map((item, i) => {
                const StripIcon = item.icon;
                return (
                  <button
                    key={i}
                    type="button"
                    className="trusted-strip-item"
                    onClick={() => navigateToSection(item.target)}
                  >
                    <StripIcon size={18} />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 6 (PRIORITY): AI VOICE ASSISTANT — THE HEART OF AGRIVOICE AI
           ==================================================================== */}
        <section id="assistant" className="assistant-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <Mic size={14} /> MULTILINGUAL AI VOICE ASSISTANT
                </span>
                <h2>Speak in Your Language. Receive Actionable Crop Guidance.</h2>
                <p>
                  Powered by Gnani Prisma V3.0 (Speech-to-Text) and Gnani Timbre
                  (Text-to-Speech) with automatic 16kHz WAV conversion and structured
                  agronomic answers.
                </p>
              </div>

              <div className="assistant-status-cluster">
                <div
                  className={`api-status-pill ${
                    backendStatus.online ? "online" : "offline"
                  }`}
                >
                  <span className="status-dot" />
                  {backendStatus.online
                    ? backendStatus.gnaniConfigured
                      ? "FastAPI & Gnani Voice API Ready"
                      : "FastAPI Online · Text & Local Voice Ready"
                    : "Backend Offline — Check Port 8000"}
                </div>
                <div className="credit-saver-pill">
                  <ShieldCheck size={14} />
                  <span>Credit-Safe On-Demand Mode</span>
                </div>
              </div>
            </div>

            <div className="assistant-workspace-grid">
              {/* Main Voice & Chat Console */}
              <div className="assistant-console-card">
                <div className="console-header">
                  <div className="console-identity">
                    <div className="console-avatar">
                      <Sprout size={22} />
                    </div>
                    <div>
                      <h3>AgriVoice AI Agricultural Expert</h3>
                      <span className="console-sub">
                        Active Language: <strong>{selectedLanguage.label}</strong> (
                        {selectedLanguage.english}) · Farmer: {farmerProfile.name}
                      </span>
                    </div>
                  </div>

                  <button
                    type="button"
                    className="btn-clear-chat"
                    onClick={clearChat}
                  >
                    <RotateCcw size={14} />
                    <span>Reset Chat</span>
                  </button>
                </div>

                {/* Language Selector Bar */}
                <div className="console-language-bar">
                  <span className="lang-bar-label">
                    <Languages size={15} /> Select Language:
                  </span>
                  <div className="lang-pill-group">
                    {LANGUAGES.map((lang) => (
                      <button
                        key={lang.code}
                        type="button"
                        className={`lang-select-pill ${
                          language === lang.code ? "selected" : ""
                        }`}
                        onClick={() => handleLanguageChange(lang.code)}
                      >
                        <span className="native-name">{lang.label}</span>
                        <span className="eng-name">{lang.english}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Conversation History */}
                <div
                  className="conversation-viewport"
                  ref={chatContainerRef}
                  aria-live="polite"
                >
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`chat-message-row ${
                        msg.role === "user" ? "user-row" : "assistant-row"
                      }`}
                    >
                      {msg.role === "assistant" && (
                        <div className="msg-avatar">
                          <Sprout size={18} />
                        </div>
                      )}

                      <div className="msg-bubble-wrapper">
                        <div className={`msg-bubble ${msg.role}-bubble`}>
                          {msg.role === "user" && msg.kind === "voice" && (
                            <div className="voice-transcript-badge">
                              <Mic size={12} />
                              <span>
                                Transcribed via {msg.provider || "Gnani Prisma V3.0"}
                              </span>
                            </div>
                          )}

                          {msg.sections && Array.isArray(msg.sections) ? (
                            <div className="structured-guidance">
                              <div className="guidance-sections-grid">
                                {msg.sections.map((sec) => (
                                  <div
                                    key={sec.key}
                                    className={`guidance-section-block sec-${sec.key}`}
                                  >
                                    <h4>{sec.title}</h4>
                                    <p>{sec.body}</p>
                                  </div>
                                ))}
                              </div>
                            </div>
                          ) : (
                            <div className="msg-plain-text">{msg.text}</div>
                          )}
                        </div>

                        <div className="msg-footer-meta">
                          <span className="msg-timestamp">{msg.time}</span>
                          {msg.role === "assistant" && (
                            <div className="msg-audio-actions">
                              <button
                                type="button"
                                className={`btn-listen-response ${
                                  playingMsgId === msg.id ? "playing" : ""
                                }`}
                                onClick={() => speakResponse(msg)}
                                disabled={speakingMsgId === msg.id}
                              >
                                {speakingMsgId === msg.id ? (
                                  <>
                                    <LoaderCircle size={14} className="spin" />
                                    <span>Generating Voice...</span>
                                  </>
                                ) : playingMsgId === msg.id ? (
                                  <>
                                    <VolumeX size={14} />
                                    <span>Stop Audio</span>
                                  </>
                                ) : (
                                  <>
                                    <Volume2 size={14} />
                                    <span>Listen to Response</span>
                                  </>
                                )}
                              </button>

                              {"speechSynthesis" in window && (
                                <button
                                  type="button"
                                  className="btn-browser-tts"
                                  onClick={() =>
                                    speakPlainText(
                                      msg.text,
                                      msg.language_code || language,
                                      msg.id
                                    )
                                  }
                                >
                                  <Headphones size={13} />
                                  <span>Read Aloud (Free)</span>
                                </button>
                              )}
                            </div>
                          )}
                        </div>

                        {msg.notice && (
                          <div className="msg-safety-notice">
                            <Info size={14} />
                            <span>{msg.notice}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}

                  {busy && (
                    <div className="chat-message-row assistant-row">
                      <div className="msg-avatar">
                        <Sprout size={18} />
                      </div>
                      <div className="msg-bubble assistant-bubble loading-bubble">
                        <LoaderCircle size={18} className="spin" />
                        <span>
                          {micState === "Transcribing"
                            ? "Converting speech to text..."
                            : "Analyzing crop question and preparing structured recommendations..."}
                        </span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Live Recording Waveform Banner */}
                {micState === "Recording" && (
                  <div className="live-recording-banner">
                    <div className="wave-bars active-wave">
                      <span />
                      <span />
                      <span />
                      <span />
                      <span />
                    </div>
                    <div className="live-recording-text">
                      <strong>
                        Listening in {selectedLanguage.english} ({recordingSeconds}s)...
                      </strong>
                      <span>
                        {livePreviewTranscript ||
                          "Speak clearly about your crop, soil, irrigation, or weather question."}
                      </span>
                    </div>
                    <button
                      type="button"
                      className="btn btn-danger btn-sm"
                      onClick={stopRecording}
                    >
                      <Square size={14} /> Stop &amp; Send
                    </button>
                  </div>
                )}

                {error && (
                  <div className="assistant-error-banner" role="alert">
                    <AlertTriangle size={18} />
                    <div className="error-banner-text">
                      <strong>Notice:</strong> {error}
                    </div>
                    <button
                      type="button"
                      className="error-dismiss-btn"
                      onClick={() => setError("")}
                    >
                      <X size={16} />
                    </button>
                  </div>
                )}

                {/* Voice & Text Input Composer */}
                <div className="console-composer">
                  <div className="voice-control-panel">
                    <div className="voice-button-group">
                      <button
                        type="button"
                        className={`btn-microphone state-${micState
                          .toLowerCase()
                          .replace(/\s+/g, "-")}`}
                        onClick={
                          micState === "Recording" ? stopRecording : startRecording
                        }
                        disabled={busy && micState !== "Recording"}
                      >
                        {micState === "Recording" ? (
                          <>
                            <span className="recording-pulse-dot" />
                            <Square size={17} />
                            <span>Stop Recording ({recordingSeconds}s)</span>
                          </>
                        ) : (
                          <>
                            <Mic size={19} />
                            <span>Speak in {selectedLanguage.english}</span>
                          </>
                        )}
                      </button>

                      <button
                        type="button"
                        className="btn-upload-audio"
                        onClick={() => fileInputRef.current?.click()}
                        disabled={busy || micState === "Recording"}
                      >
                        <Upload size={16} />
                        <span>Upload Audio</span>
                      </button>
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept="audio/*"
                        hidden
                        onChange={uploadAudio}
                      />
                    </div>

                    <div className="mic-state-indicator">
                      <span className="state-label">Status:</span>
                      <span
                        className={`state-badge badge-${micState
                          .toLowerCase()
                          .replace(/\s+/g, "-")}`}
                      >
                        {micState}
                      </span>
                    </div>
                  </div>

                  <form className="question-form" onSubmit={submitQuestion}>
                    <input
                      ref={questionInputRef}
                      type="text"
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      placeholder={selectedLanguage.placeholder}
                      disabled={busy || micState === "Recording"}
                    />
                    <button
                      type="submit"
                      className="btn-send-question"
                      disabled={!question.trim() || busy || micState === "Recording"}
                    >
                      <span>Send</span>
                      <Send size={17} />
                    </button>
                  </form>
                </div>
              </div>

              {/* Right Side Panel: Suggested Questions & How AgriVoice Works */}
              <aside className="assistant-side-panel">
                <div className="side-card">
                  <div className="side-card-head">
                    <MessageSquare size={18} />
                    <h3>Suggested Farmer Questions</h3>
                  </div>
                  <p className="side-card-desc">
                    Tap any question to ask AgriVoice AI immediately:
                  </p>
                  <div className="example-questions-list">
                    {(
                      SUGGESTED_QUESTIONS_BY_LANG[language] ||
                      SUGGESTED_QUESTIONS_BY_LANG["en-IN"]
                    ).map((qText, idx) => (
                      <button
                        key={idx}
                        type="button"
                        className="example-question-btn"
                        onClick={() => getAdvice(qText, true)}
                        disabled={busy}
                      >
                        <span>{qText}</span>
                        <ChevronRight size={16} />
                      </button>
                    ))}
                  </div>
                </div>

                <div className="side-card how-mini-card">
                  <div className="side-card-head">
                    <Compass size={18} />
                    <h3>How AgriVoice Works</h3>
                  </div>
                  <ol className="how-mini-steps">
                    <li>
                      <strong>1. Ask:</strong> Speak or type your question in Telugu,
                      Hindi, Tamil, Kannada, Malayalam, or English.
                    </li>
                    <li>
                      <strong>2. Understand:</strong> AI transcribes your speech and
                      evaluates crop symptoms, weather, and soil context.
                    </li>
                    <li>
                      <strong>3. Guide:</strong> Receive 5-step practical guidance and
                      listen aloud at the tap of a button.
                    </li>
                  </ol>
                </div>
              </aside>
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 15 & 10 & 16: MY FARM DASHBOARD, TIMELINE, IRRIGATION & SIMULATOR
           ==================================================================== */}
        <section id="my-farm" className="my-farm-section">
          <div className="container">
            <div className="dashboard-welcome-banner">
              <div>
                <span className="section-eyebrow">
                  <Activity size={14} /> PERSONALIZED FARMER DASHBOARD
                </span>
                <h2>Good Morning, {farmerProfile.name}! Welcome Back to Your Farm.</h2>
                <p>
                  📍 {farmerProfile.district}, {farmerProfile.state} ·{" "}
                  {farmerProfile.farm_size_acres} Acres Registered · Primary Crops:{" "}
                  {farmerProfile.primary_crops}
                </p>
              </div>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setShowProfileModal(true)}
              >
                <User size={16} /> Edit Farmer Profile
              </button>
            </div>

            {/* 6 Summary Cards */}
            <div className="summary-cards-grid">
              <div className="summary-stat-card">
                <small>My Farm Zones</small>
                <strong>{farmZones.length} Active Plots</strong>
                <span>{farmerProfile.farm_size_acres} Total Acres</span>
              </div>
              <div className="summary-stat-card">
                <small>Active Crops</small>
                <strong>Paddy, Tomato, Chilli</strong>
                <span>Kharif / Rabi Transition</span>
              </div>
              <div className="summary-stat-card">
                <small>Weather Status</small>
                <strong>
                  {weather ? `${weather.current.temperature_c}°C` : "30.5°C"}
                </strong>
                <span>
                  {weather
                    ? `${weather.current.condition} (${weather.current.rain_probability_pct}% Rain)`
                    : "Partly Cloudy"}
                </span>
              </div>
              <div className="summary-stat-card">
                <small>Crop Health Status</small>
                <strong>
                  {farmZones.filter((z) => z.health_status === "Healthy").length} /{" "}
                  {farmZones.length} Healthy
                </strong>
                <span>Zone B needs moisture check</span>
              </div>
              <div className="summary-stat-card">
                <small>Pending Activities</small>
                <strong>
                  {timeline.filter((t) => t.status !== "Completed").length} Tasks
                </strong>
                <span>In My Farm Timeline</span>
              </div>
              <div className="summary-stat-card highlight-stat">
                <small>Today's AI Priority</small>
                <strong>Drip Check · Zone B</strong>
                <span>Inspect lower tomato leaves</span>
              </div>
            </div>

            {/* Today's AI Farm Action Planner + My Farm Timeline */}
            <div className="farm-management-grid">
              {/* AI Daily Farm Action Planner */}
              <div className="panel-card">
                <div className="panel-card-header">
                  <div>
                    <span className="section-eyebrow">AI FARM ACTION PLANNER</span>
                    <h3>Today's Farm Plan</h3>
                  </div>
                  <button
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={() =>
                      speakPlainText(
                        dailyPlan.map((p) => `${p.time_slot}: ${p.title}. ${p.detail}`).join(" ")
                      )
                    }
                  >
                    <Volume2 size={14} /> Listen to Plan
                  </button>
                </div>

                <div className="daily-plan-list">
                  {dailyPlan.map((item, i) => (
                    <div key={i} className="daily-plan-item">
                      <div className="plan-time-row">
                        <span className="plan-time">{item.time_slot}</span>
                        <span className={`priority-tag prio-${item.priority.toLowerCase()}`}>
                          {item.priority} Priority
                        </span>
                      </div>
                      <h4>{item.title}</h4>
                      <p>{item.detail}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* My Farm Timeline & Calendar */}
              <div className="panel-card">
                <div className="panel-card-header">
                  <div>
                    <span className="section-eyebrow">PERSONALIZED FARMING CALENDAR</span>
                    <h3>My Farm Timeline</h3>
                  </div>
                  <span className="badge-subtle">Click task to mark complete</span>
                </div>

                <div className="timeline-list">
                  {timeline.map((item) => {
                    const done = item.status === "Completed";
                    return (
                      <div
                        key={item.id}
                        className={`timeline-row ${done ? "done" : ""}`}
                        onClick={() => handleToggleTimeline(item.id)}
                      >
                        <button
                          type="button"
                          className="timeline-check-btn"
                          aria-label="Toggle task completion"
                        >
                          <CheckCircle2 size={18} />
                        </button>
                        <div className="timeline-info">
                          <div className="timeline-top-line">
                            <strong>{item.title}</strong>
                            <span className="timeline-date">{item.scheduled_date}</span>
                          </div>
                          <small>
                            {item.category} · {item.zone_name} ·{" "}
                            <b>{item.status}</b>
                          </small>
                        </div>
                      </div>
                    );
                  })}
                </div>

                <form className="timeline-add-form" onSubmit={handleAddTimeline}>
                  <input
                    type="text"
                    placeholder="Add new farm activity (e.g., Neem oil spray in Zone B)..."
                    value={newActivity.title}
                    onChange={(e) =>
                      setNewActivity({ ...newActivity, title: e.target.value })
                    }
                    required
                  />
                  <select
                    value={newActivity.category}
                    onChange={(e) =>
                      setNewActivity({ ...newActivity, category: e.target.value })
                    }
                  >
                    <option>Crop inspection</option>
                    <option>Irrigation</option>
                    <option>Fertilizer application</option>
                    <option>Pest management</option>
                    <option>Sowing</option>
                    <option>Harvesting</option>
                  </select>
                  <button type="submit" className="btn btn-primary btn-sm">
                    <Plus size={15} /> Add Task
                  </button>
                </form>
              </div>
            </div>

            {/* Smart Irrigation & Soil Intelligence + What-If Simulator */}
            <div className="farm-management-grid" style={{ marginTop: "24px" }}>
              {/* Smart Irrigation & Soil Planner */}
              <div className="panel-card">
                <div className="panel-card-header">
                  <div>
                    <span className="section-eyebrow">
                      <Droplets size={14} /> SOIL &amp; IRRIGATION INTELLIGENCE
                    </span>
                    <h3>Smart Irrigation Planner</h3>
                  </div>
                  <span className="badge-subtle">Farmer-Entered Estimate</span>
                </div>

                <form className="planner-form-grid" onSubmit={handleCalculateIrrigation}>
                  <label>
                    <span>Crop Type</span>
                    <select
                      value={irrigationForm.crop_type}
                      onChange={(e) =>
                        setIrrigationForm({ ...irrigationForm, crop_type: e.target.value })
                      }
                    >
                      <option>Tomato</option>
                      <option>Paddy</option>
                      <option>Chilli</option>
                      <option>Cotton</option>
                      <option>Maize</option>
                      <option>Vegetables</option>
                    </select>
                  </label>
                  <label>
                    <span>Field Size (Acres)</span>
                    <input
                      type="number"
                      step="0.1"
                      min="0.2"
                      value={irrigationForm.field_size_acres}
                      onChange={(e) =>
                        setIrrigationForm({
                          ...irrigationForm,
                          field_size_acres: parseFloat(e.target.value) || 1.0,
                        })
                      }
                    />
                  </label>
                  <label>
                    <span>Soil Type</span>
                    <select
                      value={irrigationForm.soil_type}
                      onChange={(e) =>
                        setIrrigationForm({ ...irrigationForm, soil_type: e.target.value })
                      }
                    >
                      <option>Red Sandy Loam</option>
                      <option>Black Cotton Soil</option>
                      <option>Alluvial Clay Loam</option>
                    </select>
                  </label>
                  <label>
                    <span>Irrigation Method</span>
                    <select
                      value={irrigationForm.irrigation_method}
                      onChange={(e) =>
                        setIrrigationForm({
                          ...irrigationForm,
                          irrigation_method: e.target.value,
                        })
                      }
                    >
                      <option>Drip Irrigation</option>
                      <option>Sprinkler</option>
                      <option>Furrow / Ridge</option>
                      <option>Flood Irrigation</option>
                    </select>
                  </label>
                  <label>
                    <span>Current Moisture (%)</span>
                    <input
                      type="number"
                      min="15"
                      max="90"
                      value={irrigationForm.current_moisture_pct}
                      onChange={(e) =>
                        setIrrigationForm({
                          ...irrigationForm,
                          current_moisture_pct: parseInt(e.target.value, 10) || 50,
                        })
                      }
                    />
                  </label>
                  <div className="planner-submit-cell">
                    <button type="submit" className="btn btn-primary full-width">
                      Calculate Water Schedule
                    </button>
                  </div>
                </form>

                {irrigationResult && (
                  <div className="planner-result-box">
                    <div className="planner-highlight-row">
                      <div>
                        <small>Estimated Water Requirement</small>
                        <strong>
                          {irrigationResult.estimated_water_liters.toLocaleString()} Liters /
                          Cycle
                        </strong>
                      </div>
                      <div>
                        <small>Recommended Timing</small>
                        <strong>6:00 AM – 8:30 AM</strong>
                      </div>
                    </div>
                    <p className="planner-schedule-text">
                      <strong>Schedule:</strong> {irrigationResult.recommended_schedule}
                    </p>
                    <small className="planner-disclaimer">
                      ℹ️ {irrigationResult.disclaimer}
                    </small>
                  </div>
                )}
              </div>

              {/* What-If Farming Simulator */}
              <div className="panel-card">
                <div className="panel-card-header">
                  <div>
                    <span className="section-eyebrow">
                      <Sparkles size={14} /> HYPOTHETICAL SCENARIO PLANNER
                    </span>
                    <h3>What-If Farming Simulator</h3>
                  </div>
                </div>

                <p className="panel-intro-text">
                  Explore how weather shifts, irrigation changes, or crop rotation impact
                  your field before making decisions:
                </p>

                <div className="simulator-buttons-grid">
                  {[
                    {
                      id: "rainfall_decrease",
                      label: "What if rainfall decreases by 30%?",
                    },
                    {
                      id: "irrigation_reduced",
                      label: "What if I switch to Drip + Mulching (-25% water)?",
                    },
                    {
                      id: "crop_switch_pulses",
                      label: "What if I rotate with Pulses next season?",
                    },
                    {
                      id: "fertilizer_delayed",
                      label: "What if fertilizer application is delayed 15 days?",
                    },
                  ].map((sc) => (
                    <button
                      key={sc.id}
                      type="button"
                      className={`sim-option-btn ${
                        simulatorScenario === sc.id ? "active" : ""
                      }`}
                      onClick={() => handleRunSimulator(sc.id)}
                    >
                      {sc.label}
                    </button>
                  ))}
                </div>

                {simulatorResult && (
                  <div className="simulator-output-box">
                    <h4>{simulatorResult.title}</h4>
                    <div className="sim-badges-row">
                      <span className="sim-badge">{simulatorResult.moisture_impact}</span>
                      <span className="sim-badge warn">{simulatorResult.risk_level}</span>
                    </div>
                    <p>{simulatorResult.estimated_effect}</p>
                    <ul className="sim-steps-list">
                      {simulatorResult.mitigation_steps?.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                    <small className="planner-disclaimer">
                      ℹ️ {simulatorResult.disclaimer}
                    </small>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 7: SMART FARM MAP & DIGITAL TWIN (INTERACTIVE LEAFLET)
           ==================================================================== */}
        <section id="smart-map" className="smart-map-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <MapPin size={14} /> GEOSPATIAL FIELD INTELLIGENCE &amp; DIGITAL TWIN
                </span>
                <h2>See Your Farm and Crop Conditions on the Interactive Map</h2>
                <p>
                  Inspect field zones, switch between OpenStreetMap and Satellite imagery,
                  locate nearby KVKs and Mandis, or ask AI to explain any zone on your farm.
                </p>
              </div>
            </div>

            <SmartFarmMap
              zones={farmZones}
              nearbyResources={nearbyResources}
              selectedZoneId={selectedZoneId}
              onSelectZone={setSelectedZoneId}
              onAddZone={handleAddZone}
              onDeleteZone={handleDeleteZone}
              onExplainZone={handleExplainZone}
              explainData={explainData}
              explainLoading={explainLoading}
              onAskAssistant={handleAskFromAnywhere}
              onSpeakText={(txt) => speakPlainText(txt, language)}
            />
          </div>
        </section>

        {/* ====================================================================
            SECTION 8: AI CROP DOCTOR & CROP HEALTH PASSPORT
           ==================================================================== */}
        <section id="crop-doctor" className="crop-doctor-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <Camera size={14} /> AI CROP DOCTOR &amp; HEALTH PASSPORT
                </span>
                <h2>Upload Crop Leaf Photos &amp; Diagnose Plant Stress</h2>
                <p>
                  Upload or capture a photograph of affected leaves, stems, or fruits and
                  describe visible symptoms for structured diagnostic guidance and history
                  tracking.
                </p>
              </div>
              <div className="api-status-pill">
                <Info size={14} />
                <span>
                  {backendStatus.visionConfigured
                    ? "Vision AI Model Configured"
                    : "Symptom-Assisted Mode (Set VISION_API_KEY in backend/.env for Auto Vision AI)"}
                </span>
              </div>
            </div>

            <div className="crop-doctor-grid">
              {/* Upload & Symptom Input Form */}
              <form className="panel-card" onSubmit={handleAnalyzeCropDoctor}>
                <h3>1. Upload Crop Photograph &amp; Describe Symptoms</h3>

                <div
                  className="photo-dropzone"
                  onClick={() => doctorInputRef.current?.click()}
                >
                  {doctorImagePreview ? (
                    <div className="photo-preview-box">
                      <img
                        src={doctorImagePreview}
                        alt="Uploaded crop leaf preview"
                      />
                      <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setDoctorImageFile(null);
                          setDoctorImagePreview("");
                        }}
                      >
                        Remove Photo
                      </button>
                    </div>
                  ) : (
                    <div className="dropzone-placeholder">
                      <Camera size={32} />
                      <strong>Click to Upload Leaf / Plant Photo or Capture from Camera</strong>
                      <small>Supports JPG, PNG, WebP up to 10 MB</small>
                    </div>
                  )}
                  <input
                    ref={doctorInputRef}
                    type="file"
                    accept="image/*"
                    capture="environment"
                    hidden
                    onChange={handleDoctorImageChange}
                  />
                </div>

                <div className="doctor-form-fields">
                  <label>
                    <span>Select Crop</span>
                    <select
                      value={doctorCrop}
                      onChange={(e) => setDoctorCrop(e.target.value)}
                    >
                      <option>Tomato</option>
                      <option>Paddy (Rice)</option>
                      <option>Chilli</option>
                      <option>Cotton</option>
                      <option>Brinjal / Vegetables</option>
                      <option>Groundnut / Pulses</option>
                    </select>
                  </label>

                  <label>
                    <span>Observed Symptoms on Leaves / Stems / Fruits</span>
                    <input
                      type="text"
                      value={doctorNotes}
                      onChange={(e) => setDoctorNotes(e.target.value)}
                      placeholder="e.g., Yellowing on lower leaves, brown concentric spots, or upward leaf curl..."
                      required
                    />
                  </label>

                  <button
                    type="submit"
                    className="btn btn-primary full-width"
                    disabled={doctorLoading}
                  >
                    {doctorLoading ? (
                      <>
                        <LoaderCircle size={17} className="spin" />
                        <span>Analyzing Crop Condition...</span>
                      </>
                    ) : (
                      <>
                        <Sparkles size={17} />
                        <span>Run Crop Doctor Assessment &amp; Save to Passport</span>
                      </>
                    )}
                  </button>
                </div>
              </form>

              {/* Diagnostic Output & Crop Health History Passport */}
              <div className="panel-card">
                <h3>2. Diagnostic Guidance &amp; Crop Health Passport</h3>

                {doctorResult ? (
                  <div className="doctor-result-card">
                    <div className="doctor-result-head">
                      <div>
                        <small>{doctorResult.crop_name} · {doctorResult.created_at}</small>
                        <h4>{doctorResult.suspected_issue}</h4>
                      </div>
                      <span className="severity-badge">{doctorResult.severity}</span>
                    </div>

                    <div className="doctor-detail-block">
                      <strong>Visual Symptoms &amp; Possible Causes:</strong>
                      <p>{doctorResult.causes}</p>
                    </div>

                    <div className="doctor-detail-block">
                      <strong>Recommended Next Steps:</strong>
                      <p style={{ whiteSpace: "pre-line" }}>{doctorResult.next_steps}</p>
                    </div>

                    <div className="doctor-detail-block">
                      <strong>Prevention &amp; Expert Consultation:</strong>
                      <p>{doctorResult.prevention}</p>
                    </div>

                    <div className="doctor-mode-note">
                      ℹ️ <b>Analysis Mode:</b> {doctorResult.analysis_mode}
                    </div>
                  </div>
                ) : (
                  <div className="empty-doctor-state">
                    <Leaf size={28} />
                    <p>
                      Select your crop, upload a leaf photo (optional), and click{" "}
                      <strong>Run Crop Doctor Assessment</strong> to view structured
                      recommendations.
                    </p>
                  </div>
                )}

                {doctorHistory.length > 0 && (
                  <div className="doctor-history-section">
                    <h4>Recent Crop Health Passport Records ({doctorHistory.length})</h4>
                    <div className="doctor-history-list">
                      {doctorHistory.slice(0, 4).map((item) => (
                        <div
                          key={item.id}
                          className="history-item-row"
                          onClick={() => setDoctorResult(item)}
                        >
                          <div>
                            <strong>
                              {item.crop_name}: {item.suspected_issue}
                            </strong>
                            <small>{item.symptom_notes}</small>
                          </div>
                          <span>{item.created_at}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 9: WEATHER INTELLIGENCE & WEATHER-TO-ACTION AI
           ==================================================================== */}
        <section id="weather" className="weather-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <CloudRain size={14} /> HYPERLOCAL AGROMET FORECAST
                </span>
                <h2>Weather Intelligence &amp; Weather-to-Action AI</h2>
                <p>
                  Real-time meteorological parameters translated into clear irrigation,
                  spraying, and drainage decisions for your farm.
                </p>
              </div>
              {weather && (
                <span className="api-status-pill online">
                  <span className="status-dot" />
                  {weather.source}
                </span>
              )}
            </div>

            {weather && (
              <>
                <div className="weather-top-grid">
                  {/* Current Weather Card */}
                  <div className="weather-current-card">
                    <div className="weather-current-main">
                      <div>
                        <span className="weather-loc-badge">
                          📍 {farmerProfile.district}, {farmerProfile.state}
                        </span>
                        <div className="temp-giant">
                          {weather.current.temperature_c}°C
                        </div>
                        <p className="weather-cond-label">
                          {weather.current.condition} · Feels like{" "}
                          {weather.current.feels_like_c}°C
                        </p>
                      </div>
                      <Sun size={54} className="weather-sun-icon" />
                    </div>

                    <div className="weather-metrics-strip">
                      <div>
                        <small>Humidity</small>
                        <strong>{weather.current.humidity_pct}%</strong>
                      </div>
                      <div>
                        <small>Rain Probability</small>
                        <strong>{weather.current.rain_probability_pct}%</strong>
                      </div>
                      <div>
                        <small>Wind Speed</small>
                        <strong>{weather.current.wind_speed_kmh} km/h</strong>
                      </div>
                      <div>
                        <small>Sunrise / Sunset</small>
                        <strong>
                          {weather.current.sunrise} / {weather.current.sunset}
                        </strong>
                      </div>
                    </div>
                  </div>

                  {/* Weather-to-Action AI Card */}
                  <div className="weather-action-card">
                    <div className="panel-card-header">
                      <div>
                        <span className="section-eyebrow">WEATHER-TO-ACTION AI</span>
                        <h3>What Today's Weather Means for Your Farm</h3>
                      </div>
                      <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        onClick={() =>
                          speakPlainText(weather.weather_to_action.join(" "), language)
                        }
                      >
                        <Volume2 size={14} /> Listen
                      </button>
                    </div>

                    <ul className="weather-action-list">
                      {weather.weather_to_action.map((act, i) => (
                        <li key={i}>
                          <CheckCircle2 size={16} />
                          <span>{act}</span>
                        </li>
                      ))}
                    </ul>

                    {weather.alerts?.length > 0 && (
                      <div className="weather-alerts-stack">
                        {weather.alerts.map((al, idx) => (
                          <div key={idx} className="agromet-alert-box">
                            <AlertTriangle size={16} />
                            <div>
                              <strong>{al.title}:</strong> {al.message}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* 7-Day Forecast Strip */}
                <div className="forecast-7day-grid">
                  {weather.daily_forecast?.map((day, idx) => (
                    <div key={idx} className="forecast-day-card">
                      <span className="f-date">
                        {idx === 0 ? "Today" : idx === 1 ? "Tomorrow" : day.date.slice(5)}
                      </span>
                      <strong className="f-cond">{day.condition}</strong>
                      <div className="f-temps">
                        <span className="t-max">{day.temp_max}°</span> /{" "}
                        <span className="t-min">{day.temp_min}°</span>
                      </div>
                      <span className="f-rain">💧 {day.rain_prob}% Rain</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </section>

        {/* ====================================================================
            SECTION 11: MARKET INTELLIGENCE & MANDI DECISION ASSISTANT
           ==================================================================== */}
        <section id="market" className="market-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <TrendingUp size={14} /> AGRICULTURAL MARKET INTELLIGENCE
                </span>
                <h2>Mandi Prices, Historical Trends &amp; Selling Assistant</h2>
                <p>
                  Compare modal, minimum, and maximum prices per quintal across regional
                  regulated markets.
                </p>
              </div>
            </div>

            {/* Market Decision Assistant Banner */}
            <div className="market-assistant-banner">
              <div className="market-assistant-left">
                <span className="section-eyebrow">MARKET DECISION ASSISTANT</span>
                <h3>“Where can I find the best available price for my crop?”</h3>
                <div className="market-crop-pills">
                  {["Paddy", "Tomato", "Chilli", "Cotton", "Turmeric", "Onion"].map(
                    (c) => (
                      <button
                        key={c}
                        type="button"
                        className={`lang-select-pill ${
                          marketDecisionCrop === c ? "selected" : ""
                        }`}
                        onClick={() => handleMarketDecision(c)}
                      >
                        {c}
                      </button>
                    )
                  )}
                </div>
              </div>

              {marketDecisionResult && (
                <div className="market-assistant-right">
                  <div className="best-mandi-head">
                    <strong>Best Reference Mandi: {marketDecisionResult.best_mandi}</strong>
                    <span className="modal-price-tag">
                      ₹{marketDecisionResult.modal_price} / Quintal
                    </span>
                  </div>
                  <p>{marketDecisionResult.recommendation}</p>
                </div>
              )}
            </div>

            {/* Search & State Filter */}
            <div className="filter-toolbar">
              <div className="search-input-box">
                <Search size={16} />
                <input
                  type="text"
                  placeholder="Search crop, mandi, or district (e.g., Guntur, Tomato, Paddy)..."
                  value={marketSearch}
                  onChange={(e) => setMarketSearch(e.target.value)}
                />
              </div>
              <div className="state-pills">
                {[
                  "All",
                  "Andhra Pradesh",
                  "Telangana",
                  "Karnataka",
                  "Tamil Nadu",
                  "Maharashtra",
                ].map((st) => (
                  <button
                    key={st}
                    type="button"
                    className={`filter-pill ${marketStateFilter === st ? "active" : ""}`}
                    onClick={() => setMarketStateFilter(st)}
                  >
                    {st}
                  </button>
                ))}
              </div>
            </div>

            <div className="market-cards-grid">
              {filteredMarkets.map((m) => (
                <div key={m.id} className="market-card">
                  <div className="market-card-top">
                    <div>
                      <span className="market-state-tag">
                        {m.district}, {m.state}
                      </span>
                      <h3>{m.crop}</h3>
                      <small>{m.mandi}</small>
                    </div>
                    <span className="market-trend-badge">{m.trend}</span>
                  </div>

                  <div className="market-price-row">
                    <div>
                      <small>Min Price</small>
                      <strong>₹{m.min_price}</strong>
                    </div>
                    <div className="modal-highlight">
                      <small>Modal Price</small>
                      <strong>₹{m.modal_price}</strong>
                    </div>
                    <div>
                      <small>Max Price</small>
                      <strong>₹{m.max_price}</strong>
                    </div>
                  </div>

                  {/* Mini Trend Bar Visualization */}
                  <div className="mini-trend-bars" title="Recent 6-period price trend">
                    {m.history?.map((val, i) => {
                      const pct = Math.max(
                        35,
                        Math.min(100, Math.round((val / m.max_price) * 100))
                      );
                      return (
                        <div key={i} className="trend-bar-col">
                          <div
                            className="trend-bar-fill"
                            style={{ height: `${pct}%` }}
                          />
                        </div>
                      );
                    })}
                  </div>

                  <div className="market-card-foot">
                    <span>Source: {m.source}</span>
                    <span>Updated: {m.updated_at}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 12: FARMING KNOWLEDGE HUB (WITH AUDIO READ-ALOUD)
           ==================================================================== */}
        <section id="guides" className="guides-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <BookOpen size={14} /> FARMING KNOWLEDGE HUB
                </span>
                <h2>Step-by-Step Practical Farming Guides</h2>
                <p>
                  Accessible field guides with step-by-step instructions, precautions,
                  and one-tap voice read-aloud for every farmer.
                </p>
              </div>
            </div>

            <div className="filter-toolbar">
              <div className="search-input-box">
                <Search size={16} />
                <input
                  type="text"
                  placeholder="Search guides by crop or topic (e.g., SRI Paddy, Drip, Vermicompost)..."
                  value={guideSearch}
                  onChange={(e) => setGuideSearch(e.target.value)}
                />
              </div>
              <div className="state-pills">
                {[
                  "All",
                  "Crop cultivation",
                  "Soil management",
                  "Pest management",
                  "Irrigation",
                  "Organic farming",
                  "Fertilizers",
                ].map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    className={`filter-pill ${guideCategory === cat ? "active" : ""}`}
                    onClick={() => setGuideCategory(cat)}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="guides-grid">
              {filteredGuides.map((g) => (
                <article key={g.id} className="guide-card">
                  <div className="guide-card-top">
                    <span className="guide-cat-badge">{g.category}</span>
                    <span className="guide-crop-tag">🌱 {g.crops}</span>
                  </div>
                  <h3>{g.title}</h3>
                  <p className="guide-summary">{g.summary}</p>
                  <ol className="guide-steps">
                    {g.steps.map((st, idx) => (
                      <li key={idx}>{st}</li>
                    ))}
                  </ol>
                  <div className="guide-precaution">
                    <strong>⚠️ Precaution:</strong> {g.precautions}
                  </div>
                  <div className="guide-actions">
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={() =>
                        speakPlainText(
                          `${g.title}. ${g.summary}. Steps: ${g.steps.join(" ")}`,
                          language
                        )
                      }
                    >
                      <Volume2 size={14} /> Listen to Article
                    </button>
                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={() =>
                        handleAskFromAnywhere(`Tell me more about ${g.title}`)
                      }
                    >
                      Ask AI Assistant
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 13: GOVERNMENT SCHEMES & ELIGIBILITY ASSISTANT
           ==================================================================== */}
        <section id="schemes" className="schemes-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <Award size={14} /> GOVERNMENT SCHEMES &amp; FARMER SUPPORT
                </span>
                <h2>Verified Agricultural Subsidies, Insurance &amp; Credit Schemes</h2>
                <p>
                  Explore Central and State welfare schemes with required documents,
                  application processes, and official portal links.
                </p>
              </div>
            </div>

            {/* Scheme Eligibility Assistant */}
            <div className="eligibility-assistant-card">
              <div className="elig-left">
                <span className="section-eyebrow">SCHEME ELIGIBILITY ASSISTANT</span>
                <h3>Find Relevant Government Schemes for Your Farm</h3>
                <form className="elig-form" onSubmit={handleCheckEligibility}>
                  <label>
                    <span>Cultivable Land (Acres)</span>
                    <input
                      type="number"
                      step="0.5"
                      min="0.5"
                      value={eligForm.land_acres}
                      onChange={(e) =>
                        setEligForm({
                          ...eligForm,
                          land_acres: parseFloat(e.target.value) || 2.0,
                        })
                      }
                    />
                  </label>
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={eligForm.has_land_record}
                      onChange={(e) =>
                        setEligForm({ ...eligForm, has_land_record: e.target.checked })
                      }
                    />
                    <span>I hold Land RoR / Pattadar Passbook</span>
                  </label>
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={eligForm.needs_irrigation}
                      onChange={(e) =>
                        setEligForm({ ...eligForm, needs_irrigation: e.target.checked })
                      }
                    />
                    <span>Interested in Drip / Sprinkler Subsidy</span>
                  </label>
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={eligForm.wants_insurance}
                      onChange={(e) =>
                        setEligForm({ ...eligForm, wants_insurance: e.target.checked })
                      }
                    />
                    <span>Looking for Crop Insurance (PMFBY)</span>
                  </label>
                  <button type="submit" className="btn btn-primary">
                    Check Matching Schemes
                  </button>
                </form>
              </div>

              {eligResult && (
                <div className="elig-right">
                  <strong>
                    Category: {eligResult.farmer_category} ({eligResult.matched_count}{" "}
                    Relevant Schemes Found)
                  </strong>
                  <div className="elig-matched-pills">
                    {eligResult.matched_schemes?.map((s) => (
                      <span key={s.id} className="elig-match-tag">
                        ✓ {s.name}
                      </span>
                    ))}
                  </div>
                  <small>{eligResult.disclaimer}</small>
                </div>
              )}
            </div>

            {/* Category Filter */}
            <div className="state-pills" style={{ marginBottom: "20px" }}>
              {[
                "All",
                "Central government",
                "State government",
                "Financial assistance",
                "Crop insurance",
                "Equipment subsidies",
                "Farmer welfare",
              ].map((cat) => (
                <button
                  key={cat}
                  type="button"
                  className={`filter-pill ${schemeCategory === cat ? "active" : ""}`}
                  onClick={() => setSchemeCategory(cat)}
                >
                  {cat}
                </button>
              ))}
            </div>

            <div className="schemes-grid">
              {filteredSchemes.map((s) => (
                <div key={s.id} className="scheme-card">
                  <div className="scheme-top">
                    <span className="scheme-level-badge">{s.level}</span>
                    <span className="scheme-cat-badge">{s.category}</span>
                  </div>
                  <h3>{s.name}</h3>
                  <p className="scheme-desc">{s.description}</p>
                  <div className="scheme-meta-box">
                    <p>
                      <strong>Benefits:</strong> {s.benefits}
                    </p>
                    <p>
                      <strong>Eligibility:</strong> {s.eligibility}
                    </p>
                    <p>
                      <strong>Required Documents:</strong> {s.documents.join(", ")}
                    </p>
                    <p>
                      <strong>How to Apply:</strong> {s.application_process}
                    </p>
                  </div>
                  <div className="scheme-footer">
                    <a
                      href={s.official_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-primary btn-sm"
                    >
                      <span>Official Portal</span>
                      <ExternalLink size={14} />
                    </a>
                    <small>Verified: {s.verified_date}</small>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 14: FARMER COMMUNITY ECOSYSTEM
           ==================================================================== */}
        <section id="community" className="community-section">
          <div className="container">
            <div className="section-header-bar">
              <div>
                <span className="section-eyebrow">
                  <Users size={14} /> PEER-TO-PEER FARMER ECOSYSTEM
                </span>
                <h2>Farmer Community &amp; Field Discussions</h2>
                <p>
                  Share real crop experiences, ask fellow farmers, and learn proven
                  practices across districts.
                </p>
              </div>
            </div>

            <div className="community-layout">
              {/* Left: Posts Feed */}
              <div className="community-feed">
                <div className="state-pills" style={{ marginBottom: "16px" }}>
                  {[
                    "All",
                    "Crop Diseases",
                    "Paddy Farming",
                    "Vegetable Farming",
                    "Organic Farming",
                    "Irrigation",
                  ].map((cat) => (
                    <button
                      key={cat}
                      type="button"
                      className={`filter-pill ${
                        communityCategory === cat ? "active" : ""
                      }`}
                      onClick={() => setCommunityCategory(cat)}
                    >
                      {cat}
                    </button>
                  ))}
                </div>

                <div className="posts-stack">
                  {filteredPosts.map((post) => (
                    <div key={post.id} className="community-post-card">
                      <div className="post-header">
                        <div className="post-author-badge">
                          <User size={16} />
                          <div>
                            <strong>{post.author_name}</strong>
                            <small>
                              📍 {post.author_location} · {post.created_at}
                            </small>
                          </div>
                        </div>
                        <div className="post-tags">
                          <span className="post-tag">{post.category}</span>
                          <span className="post-tag crop">{post.crop_tag}</span>
                        </div>
                      </div>

                      <h4>{post.title}</h4>
                      <p>{post.content}</p>

                      <div className="post-actions-bar">
                        <button
                          type="button"
                          className="btn-like-post"
                          onClick={() => handleLikePost(post.id)}
                        >
                          <ThumbsUp size={14} />
                          <span>Helpful ({post.likes})</span>
                        </button>
                        <span className="comment-count">
                          💬 {post.comments?.length || 0} Responses
                        </span>
                      </div>

                      {post.comments?.length > 0 && (
                        <div className="post-comments-list">
                          {post.comments.map((c, idx) => (
                            <div key={idx} className="post-comment-item">
                              <strong>{c.author}:</strong> {c.text}
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="post-comment-box">
                        <input
                          type="text"
                          placeholder="Write a helpful reply..."
                          value={commentInputs[post.id] || ""}
                          onChange={(e) =>
                            setCommentInputs({
                              ...commentInputs,
                              [post.id]: e.target.value,
                            })
                          }
                        />
                        <button
                          type="button"
                          className="btn btn-secondary btn-sm"
                          onClick={() => handleCommentPost(post.id)}
                        >
                          Reply
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Right: Create New Community Post */}
              <aside className="panel-card">
                <h3>Share a Question or Field Experience</h3>
                <p className="side-card-desc">
                  Posting as <strong>{farmerProfile.name}</strong> (
                  {farmerProfile.district}, {farmerProfile.state})
                </p>
                <form className="doctor-form-fields" onSubmit={handleCreatePost}>
                  <label>
                    <span>Topic Category</span>
                    <select
                      value={newPost.category}
                      onChange={(e) =>
                        setNewPost({ ...newPost, category: e.target.value })
                      }
                    >
                      <option>Crop Diseases</option>
                      <option>Paddy Farming</option>
                      <option>Vegetable Farming</option>
                      <option>Organic Farming</option>
                      <option>Irrigation</option>
                    </select>
                  </label>
                  <label>
                    <span>Crop Name</span>
                    <input
                      type="text"
                      value={newPost.crop_tag}
                      onChange={(e) =>
                        setNewPost({ ...newPost, crop_tag: e.target.value })
                      }
                      placeholder="e.g., Tomato, Paddy, Chilli"
                      required
                    />
                  </label>
                  <label>
                    <span>Post Title</span>
                    <input
                      type="text"
                      value={newPost.title}
                      onChange={(e) =>
                        setNewPost({ ...newPost, title: e.target.value })
                      }
                      placeholder="Summarize your question or experience..."
                      required
                    />
                  </label>
                  <label>
                    <span>Details</span>
                    <input
                      type="text"
                      value={newPost.content}
                      onChange={(e) =>
                        setNewPost({ ...newPost, content: e.target.value })
                      }
                      placeholder="Describe crop stage, symptoms, or what worked for you..."
                      required
                    />
                  </label>
                  <button type="submit" className="btn btn-primary full-width">
                    Publish to Farmer Community
                  </button>
                </form>
              </aside>
            </div>
          </div>
        </section>

        {/* ====================================================================
            SECTION 6, 7 & 16 (ABOUT, BENEFITS, EMERGENCY SUPPORT & FINAL CTA)
           ==================================================================== */}
        <section id="about" className="about-section">
          <div className="container">
            <div className="about-grid">
              <div className="about-copy">
                <span className="section-eyebrow">
                  <ShieldCheck size={14} /> FARMER-FOCUSED BENEFITS &amp; EMERGENCY SUPPORT
                </span>
                <h2>Designed for Ordinary Farmers, Built to Competition Standards</h2>
                <p>
                  AgriVoice AI combines voice-first Indian language interaction with
                  geospatial field mapping, weather-to-action intelligence, and KVK-aligned
                  crop safety guidance.
                </p>

                <div className="about-highlights">
                  <div className="about-highlight-row">
                    <CheckCircle2 size={18} />
                    <span>
                      <strong>Understand Crop Problems Earlier:</strong> Structured
                      5-part answers and Crop Health Passport records help spot stress
                      before it spreads.
                    </span>
                  </div>
                  <div className="about-highlight-row">
                    <CheckCircle2 size={18} />
                    <span>
                      <strong>Reduce Unnecessary Water &amp; Input Usage:</strong> Smart
                      Irrigation Planner and Weather-to-Action alerts prevent watering right
                      before rain.
                    </span>
                  </div>
                  <div className="about-highlight-row">
                    <CheckCircle2 size={18} />
                    <span>
                      <strong>Zero-Jargon Regional Language Access:</strong> Speak and
                      listen in Telugu, Hindi, Tamil, Kannada, Malayalam, and English.
                    </span>
                  </div>
                </div>
              </div>

              {/* Farmer Emergency Assistance Card */}
              <div className="emergency-assistance-card">
                <div className="emergency-head">
                  <PhoneCall size={24} />
                  <div>
                    <span className="section-eyebrow">FARMER EMERGENCY ASSISTANCE</span>
                    <h3>Urgent Crop, Pest or Weather Helplines</h3>
                  </div>
                </div>
                <p>
                  For severe pest outbreaks, cyclone/flood crop damage, or urgent on-field
                  inspection, contact official government agricultural helplines:
                </p>
                <div className="helpline-boxes">
                  <div className="helpline-item">
                    <strong>Kisan Call Centre (Toll-Free India)</strong>
                    <span>📞 1800-180-1551 (6:00 AM – 10:00 PM, 22 Languages)</span>
                  </div>
                  <div className="helpline-item">
                    <strong>PMFBY Crop Insurance Claim Intimation</strong>
                    <span>📞 14447 (Notify within 72 hours of weather crop loss)</span>
                  </div>
                  <div className="helpline-item">
                    <strong>e-NAM National Market Helpline</strong>
                    <span>📞 1800-270-0224</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Final CTA Banner */}
            <div className="final-cta-banner">
              <div>
                <h2>Your Next Farming Decision Starts Here.</h2>
                <p>
                  Empowering Every Farmer with the Intelligence of AI — Speak in your
                  language today.
                </p>
              </div>
              <div className="final-cta-buttons">
                <button
                  type="button"
                  className="btn btn-leaf btn-lg"
                  onClick={() => navigateToSection("assistant")}
                >
                  <Mic size={18} /> Start with AgriVoice
                </button>
                <button
                  type="button"
                  className="btn btn-glass btn-lg"
                  onClick={() => navigateToSection("smart-map")}
                >
                  Explore Smart Farming
                </button>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* ====================================================================
          FOOTER
         ==================================================================== */}
      <footer className="site-footer">
        <div className="container footer-inner">
          <div className="footer-brand-col">
            <div className="nav-brand">
              <div className="brand-mark">
                <Sprout size={20} />
              </div>
              <div className="brand-text">
                <span className="brand-name">
                  AGRIVOICE <em>AI</em>
                </span>
                <span className="brand-sub">SMART AGRICULTURE PLATFORM</span>
              </div>
            </div>
            <p className="footer-mission">
              Empowering Every Farmer with the Intelligence of AI. Your Farm. Your
              Language. Your AI Agricultural Companion.
            </p>
          </div>

          <div className="footer-links-col">
            <h4>Platform Modules</h4>
            <ul>
              <li>
                <a href="#assistant" onClick={() => navigateToSection("assistant")}>
                  Multilingual Voice Assistant
                </a>
              </li>
              <li>
                <a href="#my-farm" onClick={() => navigateToSection("my-farm")}>
                  My Farm &amp; Digital Twin
                </a>
              </li>
              <li>
                <a href="#smart-map" onClick={() => navigateToSection("smart-map")}>
                  Interactive Smart Farm Map
                </a>
              </li>
              <li>
                <a href="#crop-doctor" onClick={() => navigateToSection("crop-doctor")}>
                  AI Crop Doctor
                </a>
              </li>
              <li>
                <a href="#weather" onClick={() => navigateToSection("weather")}>
                  Weather-to-Action AI
                </a>
              </li>
            </ul>
          </div>

          <div className="footer-links-col">
            <h4>Farmer Ecosystem</h4>
            <ul>
              <li>
                <a href="#market" onClick={() => navigateToSection("market")}>
                  Market &amp; Mandi Insights
                </a>
              </li>
              <li>
                <a href="#guides" onClick={() => navigateToSection("guides")}>
                  Farming Knowledge Hub
                </a>
              </li>
              <li>
                <a href="#schemes" onClick={() => navigateToSection("schemes")}>
                  Government Schemes
                </a>
              </li>
              <li>
                <a href="#community" onClick={() => navigateToSection("community")}>
                  Farmer Community
                </a>
              </li>
              <li>Kisan Call Centre: 1800-180-1551</li>
            </ul>
          </div>
        </div>

        <div className="container footer-bottom">
          <span>© {new Date().getFullYear()} AgriVoice AI. All rights reserved.</span>
          <span className="footer-disclaimer">
            Educational agronomic decision support — Always consult your local Agricultural
            Officer or Krishi Vigyan Kendra (KVK) before applying chemical crop treatments.
          </span>
        </div>
      </footer>

      {/* ====================================================================
          MOBILE-FIRST BOTTOM NAVIGATION BAR
         ==================================================================== */}
      <nav className="mobile-bottom-nav" aria-label="Mobile Bottom Navigation">
        <button
          type="button"
          className={activeNav === "home" ? "active" : ""}
          onClick={() => navigateToSection("home")}
        >
          <Sprout size={19} />
          <span>Home</span>
        </button>
        <button
          type="button"
          className={`voice-fab-tab ${activeNav === "assistant" ? "active" : ""}`}
          onClick={() => navigateToSection("assistant")}
        >
          <Mic size={20} />
          <span>Ask AI</span>
        </button>
        <button
          type="button"
          className={activeNav === "my-farm" ? "active" : ""}
          onClick={() => navigateToSection("my-farm")}
        >
          <Activity size={19} />
          <span>My Farm</span>
        </button>
        <button
          type="button"
          className={activeNav === "smart-map" ? "active" : ""}
          onClick={() => navigateToSection("smart-map")}
        >
          <MapPin size={19} />
          <span>Map</span>
        </button>
        <button
          type="button"
          onClick={() => setShowProfileModal(true)}
        >
          <User size={19} />
          <span>Profile</span>
        </button>
      </nav>

      {/* ====================================================================
          FARMER LOGIN / REGISTER / PROFILE MODAL
         ==================================================================== */}
      {showProfileModal && (
        <div
          className="modal-backdrop"
          onClick={() => setShowProfileModal(false)}
        >
          <div
            className="profile-modal-card"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <div>
                <span className="section-eyebrow">FARMER ACCOUNT &amp; FARM PROFILE</span>
                <h3>Personalize Your AgriVoice AI Farm</h3>
              </div>
              <button
                type="button"
                className="error-dismiss-btn"
                onClick={() => setShowProfileModal(false)}
              >
                <X size={20} />
              </button>
            </div>

            <form className="doctor-form-fields" onSubmit={handleSaveProfile}>
              <label>
                <span>Farmer Full Name</span>
                <input
                  type="text"
                  value={farmerProfile.name}
                  onChange={(e) =>
                    setFarmerProfile({ ...farmerProfile, name: e.target.value })
                  }
                  required
                />
              </label>
              <label>
                <span>Mobile Number</span>
                <input
                  type="tel"
                  value={farmerProfile.phone}
                  onChange={(e) =>
                    setFarmerProfile({ ...farmerProfile, phone: e.target.value })
                  }
                  required
                />
              </label>
              <div className="two-col-inputs">
                <label>
                  <span>State</span>
                  <input
                    type="text"
                    value={farmerProfile.state}
                    onChange={(e) =>
                      setFarmerProfile({ ...farmerProfile, state: e.target.value })
                    }
                    required
                  />
                </label>
                <label>
                  <span>District</span>
                  <input
                    type="text"
                    value={farmerProfile.district}
                    onChange={(e) =>
                      setFarmerProfile({ ...farmerProfile, district: e.target.value })
                    }
                    required
                  />
                </label>
              </div>
              <div className="two-col-inputs">
                <label>
                  <span>Farm Size (Acres)</span>
                  <input
                    type="number"
                    step="0.5"
                    min="0.5"
                    value={farmerProfile.farm_size_acres}
                    onChange={(e) =>
                      setFarmerProfile({
                        ...farmerProfile,
                        farm_size_acres: parseFloat(e.target.value) || 2.0,
                      })
                    }
                  />
                </label>
                <label>
                  <span>Primary Crops</span>
                  <input
                    type="text"
                    value={farmerProfile.primary_crops}
                    onChange={(e) =>
                      setFarmerProfile({
                        ...farmerProfile,
                        primary_crops: e.target.value,
                      })
                    }
                  />
                </label>
              </div>
              <button type="submit" className="btn btn-primary full-width">
                Save Farmer Profile
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
