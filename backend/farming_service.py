"""
AgriVoice AI — Comprehensive Multilingual Agricultural Guidance Knowledge Engine.
Provides crop-specific, context-aware, 5-part structured agricultural guidance across
10 core agronomic domains and 12+ major Indian crops in Telugu, Hindi, Tamil,
Kannada, Malayalam, and English.
"""

from typing import Any, Dict, List, Optional, Tuple

# ==============================================================================
# CROP DETECTION DICTIONARY (6 INDIAN LANGUAGES)
# ==============================================================================
CROP_KEYWORDS: Dict[str, List[str]] = {
    "paddy": [
        "paddy", "rice", "sri ", "sri method", "bpt", "sona masuri", "ir64", "transplanting", "tillering", "panicle",
        "వరి", "ధాన్యం", "బియ్యం", "నాట్లు", "దుబ్బు",
        "धान", "चावल", "रोपाई", "कल्ले",
        "நெல்", "அரிசி", "நாற்று", "தூர்",
        "ಭತ್ತ", "ಅಕ್ಕಿ", "ನಾಟಿ",
        "നെല്ല്", "അരി", "ഞാറ്",
    ],
    "tomato": [
        "tomato", "tomatoes", "arka rakshak", "lycopersicon",
        "టమాటా", "టొమాటో", "టమాట",
        "टमाटर",
        "தக்காளி",
        "ಟೊಮೆಟೊ", "ಟೊಮ್ಯಾಟೊ",
        "തക്കാളി",
    ],
    "chilli": [
        "chilli", "chili", "chillies", "mirchi", "teja", "guntur chilli", "capsicum",
        "మిర్చి", "మిరప", "మిరపకాయ",
        "मिर्च", "मिर्ची", "शिमला मिर्च",
        "மிளகாய்",
        "ಮೆಣಸಿನಕಾಯಿ", "ಮೆಣಸು",
        "മുളക്", "പച്ചമുളക്",
    ],
    "cotton": [
        "cotton", "bt cotton", "bollworm", "pink bollworm", "lint", "boll",
        "పత్తి", "గులాబీ రంగు పురుగు", "కాయ తొలిచే",
        "कपास", "नरमा", "गुलाबी सुंडी",
        "பருத்தி", "காய்ப்புழு",
        "ಹತ್ತಿ", "ಗುಲಾಬಿ ಕಾಯಿ ಕೊರಕ",
        "പരുത്തി",
    ],
    "groundnut": [
        "groundnut", "peanut", "tikka", "pegging", "pod",
        "వేరుశనగ", "పల్లీ", "ఆకుమచ్చ",
        "मूंगफली", "टिक्का",
        "நிலக்கடலை", "வேர்க்கடலை",
        "ಶೇಂಗಾ", "ನೆಲಗಡಲೆ",
        "നിലക്കടല",
    ],
    "maize": [
        "maize", "corn", "fall armyworm", "cob", "silking",
        "మొక్కజొన్న", "జొన్న", "కత్తెర పురుగు",
        "मक्का", "भुट्टा", "फॉल आर्मीवर्म",
        "மக்காச்சோளம்", "சோளம்", "படைப்புழு",
        "ಮೆಕ್ಕೆಜೋಳ", "ಜೋಳ", "ಸೈನಿಕ ಹುಳು",
        "ചോളം",
    ],
    "turmeric": [
        "turmeric", "rhizome", "curcumin",
        "పసుపు పంట", "దుంప కుళ్ళు", "కొమ్ము",
        "हल्दी", "कंद",
        "மஞ்சள் பயிர்", "கிழங்கு",
        "ಅರಿಶಿನ", "ಗೆಡ್ಡೆ",
        "മഞ്ഞൾ",
    ],
    "onion": [
        "onion", "garlic", "purple blotch", "bulb",
        "ఉల్లి", "ఉల్లిపాయ", "వెల్లుల్లి",
        "प्याज", "लहसुन",
        "வெங்காயம்", "பூண்டு",
        "ಈರುಳ್ಳಿ", "ಬೆಳ್ಳುಳ್ಳಿ",
        "ഉള്ളി", "സവാള",
    ],
    "pulses": [
        "pulse", "pulses", "redgram", "pigeonpea", "tur", "arhar", "blackgram", "urad",
        "greengram", "moong", "chickpea", "bengal gram", "chana", "lentil", "legume",
        "పప్పు", "కంది", "మినుము", "పెసర", "శనగ", "అపరాలు",
        "दाल", "दलहन", "अरहर", "तूर", "चना", "मूंग", "उड़द",
        "பயறு", "துவரை", "உளுந்து", "பாசிப்பயறு", "கடலை",
        "ಬೇಳೆ", "ತೊಗರಿ", "ಉದ್ದು", "ಹೆಸರು", "ಕಡಲೆ",
        "പയർ", "ഉഴുന്ന്", "ചെറുപയർ", "കടല",
    ],
    "vegetables": [
        "vegetable", "vegetables", "brinjal", "eggplant", "okra", "bhindi", "ladyfinger",
        "gourd", "bitter gourd", "bottle gourd", "ridge gourd", "cucumber", "cabbage", "cauliflower",
        "కూరగాయ", "కూరగాయలు", "వంకాయ", "బెండ", "బెండకాయ", "కాకర", "సొరకాయ", "బీరకాయ",
        "सब्जी", "सब्जियां", "बैंगन", "भिंडी", "लौकी", "करेला", "गोभी", "खीरा",
        "காய்கறி", "கத்திரிக்காய்", "வெண்டைக்காய்", "பாகற்காய்", "சுரைக்காய்",
        "ತರಕಾರಿ", "ಬದನೆಕಾಯಿ", "ಬೆಂಡೆಕಾಯಿ", "ಹಾಗಲಕಾಯಿ",
        "പച്ചക്കറി", "വഴുതന", "വെണ്ടയ്ക്ക", "പാവയ്ക്ക",
    ],
    "sugarcane": [
        "sugarcane", "cane", "ratoon", "red rot",
        "చెరకు", "గెడ",
        "गन्ना", "पेड़ी",
        "கரும்பு",
        "ಕಬ್ಬು",
        "കരിമ്പ്",
    ],
    "fruits": [
        "mango", "banana", "papaya", "citrus", "lemon", "sweet orange", "guava", "pomegranate",
        "మామిడి", "అరటి", "బొప్పాయి", "నిమ్మ", "బత్తాయి", "జామ", "దానిమ్మ",
        "आम", "केला", "पपीता", "नींबू", "अमरूद", "अनार",
        "மாம்பழம்", "வாழை", "பப்பாளி", "எலுமிச்சை", "கொய்யா",
        "ಮಾವು", "ಬಾಳೆ", "ಪಪ್ಪಾಯಿ", "ನಿಂಬೆ", "ಸೀಬೆ",
        "മാവ്", "വാഴ", "പപ്പായ", "നാരങ്ങ", "പേരയ്ക്ക",
    ],
}

CROP_DISPLAY_NAMES: Dict[str, Dict[str, str]] = {
    "paddy": {
        "en-IN": "Paddy (Rice)",
        "hi-IN": "धान (Paddy)",
        "te-IN": "వరి (Paddy)",
        "ta-IN": "நெல் (Paddy)",
        "kn-IN": "ಭತ್ತ (Paddy)",
        "ml-IN": "നെല്ല് (Paddy)",
    },
    "tomato": {
        "en-IN": "Tomato",
        "hi-IN": "टमाटर (Tomato)",
        "te-IN": "టమాటా (Tomato)",
        "ta-IN": "தக்காளி (Tomato)",
        "kn-IN": "ಟೊಮೆಟೊ (Tomato)",
        "ml-IN": "തക്കാളി (Tomato)",
    },
    "chilli": {
        "en-IN": "Chilli",
        "hi-IN": "मिर्च (Chilli)",
        "te-IN": "మిర్చి (Chilli)",
        "ta-IN": "மிளகாய் (Chilli)",
        "kn-IN": "ಮೆಣಸಿನಕಾಯಿ (Chilli)",
        "ml-IN": "മുളക് (Chilli)",
    },
    "cotton": {
        "en-IN": "Cotton",
        "hi-IN": "कपास (Cotton)",
        "te-IN": "పత్తి (Cotton)",
        "ta-IN": "பருத்தி (Cotton)",
        "kn-IN": "ಹತ್ತಿ (Cotton)",
        "ml-IN": "പരുത്തി (Cotton)",
    },
    "groundnut": {
        "en-IN": "Groundnut",
        "hi-IN": "मूंगफली (Groundnut)",
        "te-IN": "వేరుశనగ (Groundnut)",
        "ta-IN": "நிலக்கடலை (Groundnut)",
        "kn-IN": "ಶೇಂಗಾ (Groundnut)",
        "ml-IN": "നിലക്കടല (Groundnut)",
    },
    "maize": {
        "en-IN": "Maize (Corn)",
        "hi-IN": "मक्का (Maize)",
        "te-IN": "మొక్కజొన్న (Maize)",
        "ta-IN": "மக்காச்சோளம் (Maize)",
        "kn-IN": "ಮೆಕ್ಕೆಜೋಳ (Maize)",
        "ml-IN": "ചോളം (Maize)",
    },
    "turmeric": {
        "en-IN": "Turmeric",
        "hi-IN": "हल्दी (Turmeric)",
        "te-IN": "పసుపు పంట (Turmeric)",
        "ta-IN": "மஞ்சள் (Turmeric)",
        "kn-IN": "ಅರಿಶಿನ (Turmeric)",
        "ml-IN": "മഞ്ഞൾ (Turmeric)",
    },
    "onion": {
        "en-IN": "Onion",
        "hi-IN": "प्याज (Onion)",
        "te-IN": "ఉల్లి (Onion)",
        "ta-IN": "வெங்காயம் (Onion)",
        "kn-IN": "ಈರುಳ್ಳಿ (Onion)",
        "ml-IN": "ഉള്ളി (Onion)",
    },
    "pulses": {
        "en-IN": "Pulses (Redgram / Blackgram / Greengram)",
        "hi-IN": "दलहनी फसलें (Pulses)",
        "te-IN": "పప్పుధాన్యాలు — కంది/మినుము/పెసర (Pulses)",
        "ta-IN": "பயறு வகைப் பயிர்கள் (Pulses)",
        "kn-IN": "ದ್ವಿದಳ ಧಾನ್ಯಗಳು (Pulses)",
        "ml-IN": "പയറുവർഗ്ഗങ്ങൾ (Pulses)",
    },
    "vegetables": {
        "en-IN": "Vegetable Crops",
        "hi-IN": "सब्जी फसलें (Vegetables)",
        "te-IN": "కూరగాయ పంటలు (Vegetables)",
        "ta-IN": "காய்கறிப் பயிர்கள் (Vegetables)",
        "kn-IN": "ತರಕಾರಿ ಬೆಳೆಗಳು (Vegetables)",
        "ml-IN": "പച്ചക്കറി വിളകൾ (Vegetables)",
    },
    "sugarcane": {
        "en-IN": "Sugarcane",
        "hi-IN": "गन्ना (Sugarcane)",
        "te-IN": "చెరకు (Sugarcane)",
        "ta-IN": "கரும்பு (Sugarcane)",
        "kn-IN": "ಕಬ್ಬು (Sugarcane)",
        "ml-IN": "കരിമ്പ് (Sugarcane)",
    },
    "fruits": {
        "en-IN": "Orchard & Fruit Crops",
        "hi-IN": "फल एवं बागवानी फसलें (Fruits)",
        "te-IN": "పండ్ల తోటలు — మామిడి/అరటి/నిమ్మ (Fruits)",
        "ta-IN": "பழப்பயிர்கள் (Fruits)",
        "kn-IN": "ಹಣ್ಣಿನ ಬೆಳೆಗಳು (Fruits)",
        "ml-IN": "പഴവർഗ്ഗ വിളകൾ (Fruits)",
    },
}

# ==============================================================================
# TOPIC KEYWORDS (10 CORE AGRONOMIC CATEGORIES)
# ==============================================================================
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "irrigation": [
        "irrigate", "irrigating", "irrigation", "water", "watering", "drip", "sprinkler",
        "moisture", "dry", "canal", "borewell", "schedule", "furrow", "flood irrigation",
        "when should i irrigate", "how much water",
        "నీరు", "నీళ్ల", "నీళ్ళు", "తడి", "సాగునీరు", "డ్రిప్", "బోరు", "కాలువ", "ఎప్పుడు నీరు",
        "पानी", "सिंचाई", "नमी", "ड्रिप", "फव्वारा", "सूखा", "कब पानी",
        "தண்ணீர்", "நீர்", "பாசனம்", "சொட்டு நீர்", "ஈரப்பதம்",
        "ನೀರು", "ನೀರಾವರಿ", "ತೇವಾಂಶ", "ಹನಿ ನೀರಾವರಿ",
        "വെള്ളം", "ജലസേചനം", "ഈർപ്പം", "തുള്ളിനന",
    ],
    "crop_health": [
        "yellow", "yellowing", "pale", "curl", "curling", "stunted", "weak", "wilting",
        "drooping", "leaf drop", "flower drop", "tomato leaves", "crop health", "turning yellow",
        "scorching", "drying", "reddening", "deficiency",
        "పసుపు", "ఆకులు", "ముడత", "పెరుగుదల", "వాడిపో", "పూత రాల", "ఎర్రబడ",
        "पीले", "पीला", "सिकुड़ना", "मुरझाना", "पत्ते", "फूल झड़ना", "बढ़वार",
        "மஞ்சள்", "இலை", "சுருள்", "வளர்ச்சி", "வாடுதல்", "பூ உதிர்தல்",
        "ಹಳದಿ", "ಎಲೆ", "ಮುడుచు", "ಬೆಳವಣಿಗೆ", "ಬಾಡುವುದು", "ಹೂವು ಉದುರುವುದು",
        "മഞ്ഞ", "ഇല", "വാട്ടം", "വളർച്ച", "ചുരുളൽ",
    ],
    "pest_management": [
        "pest", "insect", "worm", "caterpillar", "aphid", "borer", "stem borer", "bollworm",
        "whitefly", "thrips", "mite", "hopper", "bph", "bug", "larva", "armyworm", "mealybug",
        "trap", "pheromone", "sticky trap", "sucking pest",
        "పురుగు", "పురుగులు", "కీటక", "దోమ", "గొంగళి", "పేనుబంక", "తామర", "తెల్లదోమ", "కాండం తొలిచే",
        "कीट", "कीड़ा", "सुंडी", "माहू", "तना छेदक", "सफेद मक्खी", "थ्रिप्स", "मच्छर", "इल्ली",
        "பூச்சி", "புழு", "அசுவினி", "தண்டு துளைப்பான்", "வெள்ளை ஈ", "இலைப்பேன்",
        "ಕೀಟ", "ಹುಳು", "ನುಸಿ", "ಕಾಂಡ ಕೊರೆಯುವ", "ಬಿಳಿ ನೊಣ", "ಥ್ರಿಪ್ಸ್",
        "കീടം", "പുഴു", "പ്രാണി", "തണ്ടുതുരപ്പൻ", "വെള്ളീച്ച",
    ],
    "disease_prevention": [
        "fungus", "fungal", "mildew", "spots", "spot", "blight", "early blight", "late blight",
        "rot", "root rot", "collar rot", "rust", "wilt", "mosaic", "canker", "disease",
        "infection", "blast", "sheath blight", "tikka", "anthracnose", "identify a crop disease",
        "బూజు", "మచ్చ", "మచ్చలు", "కుళ్ళు", "వేరు కుళ్ళు", "తెగులు", "అగ్గి తెగులు", "ఆకుమచ్చ",
        "फफूंद", "धब्बे", "झुलसा", "सड़न", "जड़ सड़न", "रोग", "बीमारी", "ब्लास्ट", "उकठा",
        "பூஞ்சை", "புள்ளி", "புள்ளிகள்", "அழுகல்", "வேர் அழுகல்", "நோய்", "கருகல்",
        "ಶಿಲೀಂಧ್ರ", "ಕಲೆ", "ಕೊಳೆ", "ಬೇರು ಕೊಳೆ", "ರೋಗ", "ಅಂಗಮಾರಿ",
        "കുമിൾ", "പുള്ളി", "ചീയൽ", "വേരുചീയൽ", "രോഗം",
    ],
    "fertilizer_guidance": [
        "fertilizer", "fertiliser", "manure", "urea", "dap", "npk", "potash", "mop", "ssp",
        "phosphorus", "nitrogen", "vermicompost", "micronutrient", "zinc", "boron", "magnesium",
        "nutrient", "feeding", "top dressing", "basal",
        "ఎరువు", "ఎరువులు", "పోషకాలు", "యూరియా", "డిఎపి", "పొటాష్", "జింక్", "వర్మీకంపోస్ట్",
        "खाद", "उर्वरक", "पोषक", "गोबर", "वर्मीकम्पोस्ट", "यूरिया", "डीएपी", "पोटाश", "जिंक",
        "உரம்", "உரங்கள்", "ஊட்டச்சத்து", "தொழு உரம்", "யூரியா", "மண்புழு உரம்",
        "ಗೊಬ್ಬರ", "ಪೋಷಕಾಂಶ", "ಸಾವಯವ ಗೊಬ್ಬರ", "ಯೂರಿಯಾ", "ಡಿಎಪಿ", "ಎರೆಹುಳು ಗೊಬ್ಬರ",
        "വളം", "വളങ്ങൾ", "പോഷകങ്ങൾ", "ജൈവവളം", "യൂറിയ", "മണ്ണിര കമ്പോസ്റ്റ്",
    ],
    "soil_health": [
        "soil", "ph", "organic matter", "compost", "earthworm", "fertility", "salinity",
        "alkaline", "acidic", "structure", "topsoil", "soil test", "soil health card", "gypsum",
        "నేల", "మట్టి", "భూమి", "సారం", "భూసార", "చౌడు", "జిప్సం",
        "मिट्टी", "मृदा", "उर्वरता", "जीवांश", "जांच", "मृदा स्वास्थ्य", "जिप्सम",
        "மண்", "மண் வளம்", "பரிசோதனை", "ஜிப்சம்",
        "ಮಣ್ಣು", "ಮಣ್ಣಿನ", "ಫಲವತ್ತತೆ", "ಮಣ್ಣು ಪರೀಕ್ಷೆ",
        "മണ്ണ്", "മണ്ണിന്റെ", "ഫലഭൂയിഷ്ഠത", "മണ്ണ് പരിശോധന",
    ],
    "weather_precautions": [
        "weather", "rain", "rainfall", "heavy rain", "flood", "waterlogging", "storm", "wind",
        "heat", "heatwave", "drought", "frost", "monsoon", "cyclone", "forecast", "will it rain",
        "వర్షం", "వాతావరణం", "వరద", "గాలి", "ఎండ", "తుఫాను", "వాన",
        "बारिश", "वर्षा", "मौसम", "बाढ़", "लू", "सूखा", "तेज हवा", "तूफान",
        "மழை", "வானிலை", "வெள்ளம்", "காற்று", "வெயில்", "புயல்",
        "ಮಳೆ", "ಹವಾಮಾನ", "ಪ್ರವಾಹ", "ಗಾಳಿ", "ಬಿಸಿಲು",
        "മഴ", "കാലാവസ്ഥ", "വെള്ളപ്പൊക്കം", "കാറ്റ്", "ചൂട്",
    ],
    "crop_selection_season": [
        "season", "suitable", "which crop", "kharif", "rabi", "zaid", "summer crop", "sow",
        "sowing", "seed", "seeds", "variety", "varieties", "spacing", "nursery", "sri ",
        "cultivate", "cultivation", "grow", "growing", "yield", "harvest", "tell me more about",
        "సీజన్", "ఏ పంట", "విత్తనాలు", "విత్తనం", "ఖరీఫ్", "రబీ", "సాగు", "దిగుబడి", "రకాలు", "కోత",
        "सीजन", "मौसम में कौन", "कौन सी फसल", "खरीफ", "रबी", "जायद", "बीज", "बुवाई", "किस्म", "पैदावार", "खेती",
        "பருவம்", "எந்த பயிர்", "விதை", "விதைப்பு", "சாகுபடி", "மகசூல்", "ரகம்",
        "ಹಂಗಾಮು", "ಯಾವ ಬೆಳೆ", "ಬಿತ್ತನೆ", "ಬೀಜ", "ಮುಂಗಾರು", "ಹಿಂಗಾರು", "ಇಳುವರಿ", "ಬೇಸಾಯ",
        "സീസൺ", "ഏത് വിള", "വിത്ത്", "കൃഷി", "വിളവ്", "നടീൽ",
    ],
    "market_schemes": [
        "market", "mandi", "price", "prices", "rate", "sell", "selling", "msp", "e-nam",
        "scheme", "schemes", "subsidy", "pm-kisan", "pmfby", "insurance", "loan", "kcc", "credit",
        "మార్కెట్", "ధర", "ధరలు", "మండి", "అమ్మకం", "మద్దతు ధర", "పథకం", "పథకాలు", "సబ్సిడీ", "భీమా", "రుణం",
        "बाजार", "मंडी", "भाव", "कीमत", "एमएसपी", "योजना", "सब्सिडी", "बीमा", "किसान सम्मान", "ऋण",
        "சந்தை", "விலை", "மண்டி", "திட்டம்", "மானியம்", "காப்பீடு",
        "ಮಾರುಕಟ್ಟೆ", "ಬೆಲೆ", "ಮಂಡಿ", "ಯೋಜನೆ", "ಸಬ್ಸಿಡಿ", "ವಿಮೆ",
        "വിപണി", "വില", "പദ്ധതി", "സബ്സിഡി", "ഇൻഷുറൻസ്",
    ],
    "sustainable_farming": [
        "sustainable", "organic", "rotation", "crop rotation", "mulch", "mulching", "intercrop",
        "intercropping", "natural", "bio", "trap crop", "neem", "eco", "weed", "weeding", "jeevamrutham",
        "ప్రకృతి", "సేంద్రీయ", "సేంద్రియ", "పంట మార్పిడి", "మల్చింగ్", "అంతర పంట", "వేప", "కలుపు",
        "जैविक", "टिकाऊ", "फसल चक्र", "मल्चिंग", "प्राकृतिक", "नीम", "खरपतवार", "सहफसली",
        "இயற்கை", "பயிர் சுழற்சி", "மூடாக்கு", "ஊடுபயிர்", "வேப்ப", "களை",
        "ಸಾವಯವ", "ಬೆಳೆ ಪರಿವರ್ತನೆ", "ಹೊದಿಕೆ", "ಮಿಶ್ರ ಬೆಳೆ", "ಬೇವು", "ಕಳೆ",
        "ജൈവകൃഷി", "വിളപരിവർത്തനം", "പുതയിടൽ", "ഇടവിള", "വേപ്പെണ്ണ", "കള",
    ],
}

SECTION_LABELS: Dict[str, Dict[str, str]] = {
    "en-IN": {
        "problem": "1. Problem / Topic Identified",
        "causes": "2. Key Agronomic Factors & Causes",
        "steps": "3. Recommended Actionable Next Steps",
        "precautions": "4. Field Precautions",
        "expert": "5. When to Consult a Local Agricultural Expert",
        "notice": "Educational agronomic guidance. Confirm chemical dosages and local recommendations with your Agricultural Officer or Krishi Vigyan Kendra (KVK — Toll-Free 1800-180-1551).",
    },
    "hi-IN": {
        "problem": "1. पहचानी गई कृषि समस्या / विषय (Topic Identified)",
        "causes": "2. प्रमुख कारण और कृषि कारक (Key Factors & Causes)",
        "steps": "3. सुझाए गए व्यावहारिक कदम (Recommended Next Steps)",
        "precautions": "4. आवश्यक सावधानियां (Precautions)",
        "expert": "5. स्थानीय कृषि विशेषज्ञ से कब संपर्क करें (When to Consult an Expert)",
        "notice": "नोट: यह शैक्षिक कृषि मार्गदर्शन है। किसी भी रसायन या उपचार से पहले अपने स्थानीय कृषि अधिकारी या कृषि विज्ञान केंद्र (KVK हेल्पलाइन: 1800-180-1551) से सलाह लें।",
    },
    "te-IN": {
        "problem": "1. గుర్తించిన సమస్య / వ్యవసాయ అంశం (Problem / Topic Identified)",
        "causes": "2. ప్రధాన కారణాలు & పంట పరిస్థితులు (Possible Causes & Factors)",
        "steps": "3. రైతులు తీసుకోవాల్సిన తదుపరి చర్యలు (Recommended Next Steps)",
        "precautions": "4. పాటించాల్సిన జాగ్రత్తలు (Precautions)",
        "expert": "5. స్థానిక వ్యవసాయ నిపుణుడిని ఎప్పుడు సంప్రదించాలి (When to Consult an Expert)",
        "notice": "గమనిక: ఇది ఆచరణాత్మక వ్యవసాయ అవగాహన సమాచారం. మందుల మోతాదు కోసం స్థానిక వ్యవసాయ అధికారి (AO) లేదా కృషి విజ్ఞాన కేంద్రం (KVK టోల్-ఫ్రీ: 1800-180-1551) ని సంప్రదించండి.",
    },
    "ta-IN": {
        "problem": "1. கண்டறியப்பட்ட வேளாண் பிரச்சினை / தலைப்பு (Problem Identified)",
        "causes": "2. முக்கிய காரணங்கள் மற்றும் காரணிகள் (Possible Causes)",
        "steps": "3. பரிந்துரைக்கப்படும் அடுத்த கட்ட நடவடிக்கைகள் (Recommended Next Steps)",
        "precautions": "4. முன்னெச்சரிக்கைகள் (Precautions)",
        "expert": "5. உள்ளூர் வேளாண் நிபுணரை எப்போது அணுக வேண்டும் (When to Consult an Expert)",
        "notice": "குறிப்பு: இது கல்வி வழிகாட்டுதல் மட்டுமே. மருந்து அல்லது உரங்களைப் பயன்படுத்துவதற்கு முன் உள்ளூர் வேளாண் அதிகாரி அல்லது KVK (1800-180-1551)-ஐ அணுகவும்.",
    },
    "kn-IN": {
        "problem": "1. ಗುರುತಿಸಲಾದ ಕೃಷಿ ಸಮಸ್ಯೆ / ವಿಷಯ (Problem Identified)",
        "causes": "2. ಪ್ರಮುಖ ಕಾರಣಗಳು ಮತ್ತು ಅಂಶಗಳು (Possible Causes)",
        "steps": "3. ಮುಂದಿನ ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮಗಳು (Recommended Next Steps)",
        "precautions": "4. ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು (Precautions)",
        "expert": "5. ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರನ್ನು ಯಾವಾಗ ಸಂಪರ್ಕಿಸಬೇಕು (When to Consult an Expert)",
        "notice": "ಗಮನಿಸಿ: ಇದು ಶೈಕ್ಷಣಿಕ ಕೃಷಿ ಮಾಹಿತಿ. ಯಾವುದೇ ರಾಸಾಯನಿಕ ಬಳಸುವ ಮೊದಲು ಸ್ಥಳೀಯ ಕೃಷಿ ಅಧಿಕಾರಿ ಅಥವಾ KVK (1800-180-1551) ಅನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    },
    "ml-IN": {
        "problem": "1. തിരിച്ചറിഞ്ഞ കാർഷിക പ്രശ്നം / വിഷയം (Problem Identified)",
        "causes": "2. സാധ്യമായ കാരണങ്ങളും ഘടകങ്ങളും (Possible Causes)",
        "steps": "3. ശുപാർശ ചെയ്യുന്ന അടുത്ത നടപടികൾ (Recommended Next Steps)",
        "precautions": "4. മുൻകരുതലുകൾ (Precautions)",
        "expert": "5. പ്രാദേശിക കൃഷി വിദഗ്ദ്ധനെ എപ്പോൾ സമീപിക്കണം (When to Consult an Expert)",
        "notice": "ശ്രദ്ധിക്കുക: ഇത് വിദ്യാഭ്യാസപരമായ കാർഷിക വിവരമാണ്. വളങ്ങളോ കീടനാശിനികളോ ഉപയോഗിക്കുന്നതിന് മുമ്പ് കൃഷിഭവനുമായോ KVK (1800-180-1551)-യുമായോ ബന്ധപ്പെടുക.",
    },
}

# ==============================================================================
# CROP-SPECIFIC QUICK NOTES (APPENDED TO STEPS FOR EXTRA PRECISION)
# ==============================================================================
CROP_SPECIFIC_NOTES: Dict[str, Dict[str, str]] = {
    "paddy": {
        "en-IN": "For Paddy (Rice): Maintain 2–3 cm shallow water during active tillering (alternate wetting and drying saves 25% water), monitor stem borer and brown planthopper (BPH) at the base of hills, and apply Zinc Sulphate if rusty brown spots appear on lower leaves.",
        "hi-IN": "धान (Paddy) विशेष सलाह: कल्ले निकलते समय खेत में 2–3 सेमी पानी रखें (बारी-बारी से गीला और सूखा रखने से 25% पानी बचता है), तना छेदक व भूरे फुदके (BPH) की निगरानी करें और जिंक की कमी दिखने पर जिंक सल्फेट का उपयोग करें।",
        "te-IN": "వరి పంట ప్రత్యేక సూచన: దుబ్బు చేసే దశలో 2–3 సెం.మీ మాత్రమే నీరు ఉంచండి (మార్చి మార్చి తడి పెట్టడం వల్ల 25% నీరు ఆదా అవుతుంది). దుబ్బుల అడుగు భాగంలో దోమపోటు (BPH) మరియు కాండం తొలిచే పురుగులను గమనించండి. జింక్ లోపం ఉంటే జింక్ సల్ఫేట్ వాడండి.",
        "ta-IN": "நெல் பயிர் சிறப்பு ஆலோசனை: தூர் கட்டும் பருவத்தில் 2–3 செ.மீ நீர் மட்டும் பராமரிக்கவும் (காய்ச்சலும் பாய்ச்சலும் முறை 25% நீரைச் சேமிக்கும்). தண்டு துளைப்பான் மற்றும் புகையான் (BPH) தாக்குதலைக் கண்காணிக்கவும்.",
        "kn-IN": "ಭತ್ತದ ಬೆಳೆ ವಿಶೇಷ ಸಲಹೆ: ತೆನೆ ಕಟ್ಟುವ ಮತ್ತು ಕವಲು ಒಡೆಯುವ ಹಂತದಲ್ಲಿ 2–3 ಸೆಂ.ಮೀ ನೀರು ಮಾತ್ರ ಇರಲಿ. ಕಾಂಡ ಕೊರೆಯುವ ಹುಳು ಮತ್ತು ಕಂದು ಜಿಗಿಹುಳು (BPH) ಬಗ್ಗೆ ನಿಗಾ ಇರಿಸಿ.",
        "ml-IN": "നെൽകൃഷി പ്രത്യേക നിർദ്ദേശം: ചിനപ്പുപൊട്ടുന്ന സമയത്ത് 2–3 സെ.മീ വെള്ളം മാത്രം ക്രമീകരിക്കുക. തണ്ടുതുരപ്പൻ, മുഞ്ഞ (BPH) എന്നിവയുടെ സാന്നിധ്യം ചുവട്ടിൽ പരിശോധിക്കുക.",
    },
    "tomato": {
        "en-IN": "For Tomato: Stake plants off the wet ground using bamboo/trellis twine, irrigate consistently via drip to prevent blossom-end rot (calcium deficiency) and fruit cracking, and install 10 yellow sticky traps per acre against whitefly-transmitted leaf curl virus.",
        "hi-IN": "टमाटर (Tomato) विशेष सलाह: पौधों को बांस और सुतली से सहारा (Staking) दें ताकि पत्तियां गीली मिट्टी के संपर्क में न आएं, ड्रिप से नियमित नमी बनाए रखें और सफेद मक्खी (पत्ती मोड़क वायरस) की रोकथाम के लिए पीले चिपचिपे ट्रैप लगाएं।",
        "te-IN": "టమాటా పంట ప్రత్యేక సూచన: మొక్కలు నేలకు తగలకుండా కర్రలతో ఊతం (Staking) ఇవ్వండి. కాయలు పగలకుండా మరియు కాల్షియం లోపం రాకుండా డ్రిప్ ద్వారా సమానంగా తడి ఇవ్వండి. తెల్లదోమ మరియు ఆకుముడత వైరస్ నివారణకు ఎకరాకు 10 పసుపు జిగురు అట్టలు పెట్టండి.",
        "ta-IN": "தக்காளி சிறப்பு ஆலோசனை: செடிகள் தரையில் படாமல் குச்சிகள் கட்டித் தாங்கவும் (Staking). சொட்டு நீர்ப்பாசனம் மூலம் சீரான ஈரப்பதம் அளித்து, வெள்ளை ஈக்களைக் கட்டுப்படுத்த மஞ்சள் ஒட்டும் அட்டைகளை வைக்கவும்.",
        "kn-IN": "ಟೊಮೆಟೊ ವಿಶೇಷ ಸಲಹೆ: ಗಿಡಗಳು ನೆಲಕ್ಕೆ ತಾಗದಂತೆ ಕಡ್ಡಿಗಳ ಆಧಾರ (Staking) ನೀಡಿ. ಹನಿ ನೀರಾವರಿ ಮೂಲಕ ಸಮಾನ ತೇವಾಂಶ ಕಾಪಾಡಿ ಮತ್ತು ಬಿಳಿ ನೊಣ ನಿಯಂತ್ರಣಕ್ಕೆ ಹಳದಿ ಅಂಟು ಪಟ್ಟಿಗಳನ್ನು ಅಳವಡಿಸಿ.",
        "ml-IN": "തക്കാളി പ്രത്യേക നിർദ്ദേശം: ചെടികൾ മണ്ണിൽ മുട്ടാതിരിക്കാൻ താങ്ങ് (Staking) നൽകുക. വെള്ളീച്ചയെയും ഇലച്ചുരുളൽ രോഗത്തെയും തടയാൻ മഞ്ഞ കെണികൾ സ്ഥാപിക്കുക.",
    },
    "chilli": {
        "en-IN": "For Chilli: Avoid standing water in the root zone (chilli roots are highly sensitive to collar wilt), install blue sticky traps for thrips (upward leaf curl) and yellow traps for mites (downward leaf curl), and spray 5% Neem Seed Kernel Extract (NSKE) early.",
        "hi-IN": "मिर्च (Chilli) विशेष सलाह: मिर्च की जड़ों के पास पानी बिल्कुल जमा न होने दें (उकठा रोग का खतरा रहता है)। थ्रिप्स (ऊपर की ओर पत्ती मुड़ना) के लिए नीले ट्रैप और माइट्स के लिए पीले ट्रैप लगाएं तथा नीम तेल का छिड़काव करें।",
        "te-IN": "మిర్చి పంట ప్రత్యేక సూచన: మిర్చి వేర్ల దగ్గర నీరు అసలు నిల్వ ఉండనివ్వకండి (వేరు కుళ్ళు వస్తుంది). తామర పురుగులు (ఆకులు పైకి ముడత) కోసం నీలం జిగురు అట్టలు, నల్లి (ఆకులు కిందికి ముడత) కోసం పసుపు అట్టలు పెట్టి వేప నూనె పిచికారీ చేయండి.",
        "ta-IN": "மிளகாய் சிறப்பு ஆலோசனை: வேர்ப்பகுதியில் நீர் தேங்க விடாதீர்கள். இலைப்பேன் (இலை மேல்நோக்கி சுருளுதல்) கட்டுப்படுத்த நீல ஒட்டும் அட்டைகள் மற்றும் வேப்பெண்ணெய் கரைசலைப் பயன்படுத்தவும்.",
        "kn-IN": "ಮೆಣಸಿನಕಾಯಿ ವಿಶೇಷ ಸಲಹೆ: ಬೇರುಗಳ ಬಳಿ ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ. ಥ್ರಿಪ್ಸ್ ಮತ್ತು ನುಸಿ ನಿಯಂತ್ರಣಕ್ಕಾಗಿ ನೀಲಿ/ಹಳದಿ ಅಂಟು ಪಟ್ಟಿಗಳನ್ನು ಮತ್ತು ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಣೆಯನ್ನು ಬಳಸಿ.",
        "ml-IN": "മുളക് കൃഷി പ്രത്യേക നിർദ്ദേശം: ചുവട്ടിൽ വെള്ളം കെട്ടിനിൽക്കാൻ അനുവദിക്കരുത്. ഇലപ്പേൻ നിയന്ത്രിക്കാൻ നീല കെണികളും വേപ്പെണ്ണ മിശ്രിതവും ഉപയോഗിക്കുക.",
    },
    "cotton": {
        "en-IN": "For Cotton: Install 4–5 pheromone traps per acre at 45 days after sowing to monitor Pink Bollworm moths, remove rosette flowers promptly, and spray 2% KNO3 or 1% MgSO4 during boll development to prevent leaf reddening.",
        "hi-IN": "कपास (Cotton) विशेष सलाह: गुलाबी सुंडी की निगरानी हेतु बुवाई के 45 दिन बाद प्रति एकड़ 4–5 फेरोमोन ट्रैप लगाएं, खराब फूलों (Rosette flowers) को नष्ट करें और पत्तों का लाल होना रोकने के लिए मैग्नीशियम सल्फेट का पर्ण छिड़काव करें।",
        "te-IN": "పత్తి పంట ప్రత్యేక సూచన: గులాబీ రంగు పురుగు ఉనికిని గుర్తించేందుకు విత్తిన 45 రోజులకు ఎకరాకు 4–5 లింగాకర్షక బుట్టలు పెట్టండి. గుడ్డి పూలను (Rosette flowers) ఏరి నాశనం చేయండి. ఆకులు ఎర్రబడకుండా మెగ్నీషియం సల్ఫేట్ పిచికారీ చేయండి.",
        "ta-IN": "பருத்தி சிறப்பு ஆலோசனை: இளஞ்சிவப்பு காய்ப்புழுவைக் கண்காணிக்க ஏக்கருக்கு 5 இனக்கவர்ச்சிப் பொறிகள் வைக்கவும். இலை சிவப்பாவதைத் தடுக்க மெக்னீசியம் சல்பேட் தெளிக்கவும்.",
        "kn-IN": "ಹತ್ತಿ ಬೆಳೆ ವಿಶೇಷ ಸಲಹೆ: ಗುಲಾಬಿ ಕಾಯಿ ಕೊರಕದ ನಿಗಾ ವಹಿಸಲು ಎಕರೆಗೆ 4–5 ಮೋಹಕ ಬಲೆಗಳನ್ನು ಅಳವಡಿಸಿ ಮತ್ತು ಎಲೆ ಕೆಂಪಾಗುವುದನ್ನು ತಡೆಯಲು ಮೆಗ್ನೀಸಿಯಮ್ ಸಲ್ಫೇಟ್ ಸಿಂಪಡಿಸಿ.",
        "ml-IN": "പരുത്തി പ്രത്യേക നിർദ്ദേശം: പിങ്ക് ബോൾവേം നിരീക്ഷിക്കാൻ ഫെറമോൺ കെണികൾ സ്ഥാപിക്കുകയും മഗ്നീഷ്യം സൾഫേറ്റ് തളിക്കുകയും ചെയ്യുക.",
    },
}

# ==============================================================================
# MULTILINGUAL KNOWLEDGE BASE ACROSS ALL 10 CATEGORIES
# ==============================================================================
KNOWLEDGE_BASE: Dict[str, Dict[str, Dict[str, str]]] = {
    "en-IN": {
        "crop_health": {
            "problem": "Visible crop stress such as yellowing leaves, leaf curling, flower drop, or slowed plant growth.",
            "causes": "Nutrient deficiency (Nitrogen causes older bottom leaves to turn yellow; Iron/Zinc affects new top leaves), root-zone over-watering or poor drainage, sap-sucking insects (whiteflies, thrips, aphids) under leaves, or sudden moisture stress.",
            "steps": "1. Check whether yellowing starts on older lower leaves or young top shoots.\n2. Turn over 5–10 leaves early in the morning to check for tiny whiteflies, thrips, or mites.\n3. Check soil moisture 5–8 cm deep before watering.\n4. Apply balanced foliar micronutrient or decomposed organic compost based on symptom location.",
            "precautions": "Do not spray strong chemical pesticides or heavy urea blindly before confirming whether the cause is water stress, nutrient deficiency, or insects.",
            "expert": "If yellowing or wilting spreads across multiple rows despite normal soil moisture, take 2–3 affected leaves to your local Agricultural Officer or KVK (1800-180-1551).",
        },
        "pest_management": {
            "problem": "Insect or pest damage on leaves, stems, flowers, or developing pods/fruits.",
            "causes": "Chewing pests (stem borers, caterpillars, bollworms, fall armyworm) or sucking pests (aphids, whiteflies, thrips, hoppers) favored by warm humid weather, dense canopy, or excess nitrogen.",
            "steps": "1. Scout upper and lower leaf surfaces between 6:30 AM and 8:30 AM.\n2. Install 10 yellow/blue sticky traps and 4–5 pheromone traps per acre.\n3. Remove and destroy heavily infested shoots or egg masses.\n4. Use 5% Neem Seed Kernel Extract (NSKE) or Neem Oil (10,000 ppm @ 2 ml/L) as the first line of Integrated Pest Management (IPM).",
            "precautions": "Avoid mixing multiple chemical insecticides together, and never spray during peak honeybee foraging hours (9 AM – 3 PM).",
            "expert": "Show clear close-up photos of the insect or damaged stem to your local KVK or plant clinic for targeted, stage-safe IPM recommendations.",
        },
        "disease_prevention": {
            "problem": "Fungal, bacterial, or viral disease symptoms such as leaf spots, blight, powdery mildew, wilt, or root/fruit rot.",
            "causes": "High humidity (>80%), morning dew or overhead watering wetting foliage, poor field drainage, crowded spacing, or seed/soil-borne pathogens.",
            "steps": "1. Prune and safely dispose of severely spotted lower leaves outside the field.\n2. Water strictly at the root zone (drip/furrow) rather than splashing foliage.\n3. Improve field drainage and plant airflow.\n4. Treat seeds/roots with Trichoderma viride or Pseudomonas fluorescens as a preventive bio-fungicide.",
            "precautions": "Never throw diseased plant debris into irrigation channels or compost pits, and wash tools after inspecting infected rows.",
            "expert": "Consult your local KVK plant protection specialist before buying fungicides so fungal vs. bacterial vs. viral symptoms are accurately distinguished.",
        },
        "irrigation": {
            "problem": "Crop irrigation scheduling, water requirement planning, and moisture stress / waterlogging prevention.",
            "causes": "Irregular watering intervals, high daytime evaporation, uneven land leveling, or heavy clay soils holding standing water around sensitive roots.",
            "steps": "1. Perform the 5–8 cm soil feel test near the root zone before starting the pump.\n2. Irrigate during cool morning (6:00–8:30 AM) or evening hours to reduce evaporation loss by 25–30%.\n3. For Paddy, maintain 2–3 cm shallow water during tillering (Alternate Wetting & Drying) and 5 cm during flowering.\n4. For Tomato, Chilli, and Vegetables, use drip irrigation with mulching and keep drainage channels open.",
            "precautions": "Never allow standing water for more than 12 hours in vegetable, pulse, or cotton fields, as root asphyxiation rapidly triggers wilt and collar rot.",
            "expert": "Contact your mandal horticultural/agricultural officer for PMKSY 'Per Drop More Crop' drip & sprinkler irrigation subsidies (55%–90% support).",
        },
        "fertilizer_guidance": {
            "problem": "Balanced crop nutrition, basal and top-dressing fertilizer schedule, and deficiency correction.",
            "causes": "Applying only Urea without Phosphorus, Potash, and micronutrients (Zinc, Boron, Magnesium), or applying fertilizers on dry/waterlogged soil.",
            "steps": "1. Follow your Soil Health Card NPK prescription rather than blanket applications.\n2. Incorporate 4–5 tonnes/acre of well-decomposed Farmyard Manure (FYM) or 1 tonne Vermicompost before sowing.\n3. Split Nitrogen (Neem-coated Urea) into 3 equal doses (Basal, Vegetative/Tillering, and Flowering/Panicle initiation).\n4. Apply Potash during flowering/fruiting to improve grain weight, fruit shine, and disease resistance.",
            "precautions": "Ensure adequate soil moisture before broadcasting or fertigating, and avoid excess nitrogen which causes lush, weak growth that attracts sucking pests.",
            "expert": "Visit your nearest Soil Testing Laboratory or KVK with a composite soil sample to get a customized district fertilizer schedule.",
        },
        "soil_health": {
            "problem": "Improving soil fertility, organic carbon, pH balance, and water-holding capacity.",
            "causes": "Continuous monocropping without legumes, low organic manure input, soil compaction, or saline/alkaline/acidic soil pH imbalance (ideal range: pH 6.5–7.2).",
            "steps": "1. Collect soil samples from 8–10 spots in a zig-zag pattern (15 cm depth) for a Soil Health Card test.\n2. Grow green manure crops (Dhaincha / Sunnhemp) and incorporate at 45 days before main crop sowing.\n3. Rotate cereal or commercial crops with short-duration pulses (Greengram / Blackgram).\n4. Apply Gypsum for alkaline/sodic soils or agricultural lime for acidic soils as per lab report.",
            "precautions": "Never burn crop stubble or residue in the field — burning destroys beneficial nitrogen-fixing microbes and earthworms.",
            "expert": "Review your Soil Health Card report with your local KVK soil scientist before the Kharif or Rabi sowing window.",
        },
        "weather_precautions": {
            "problem": "Protecting crops from forecasted rainfall, thunderstorms, heatwaves, or high humidity.",
            "causes": "Sudden heavy showers causing waterlogging and spray wash-off, strong winds causing lodging in tall crops, or heatwaves (>38°C) causing flower and fruit drop.",
            "steps": "1. Open field drainage furrows immediately when rainfall probability exceeds 50%.\n2. Postpone chemical or foliar spraying if rain is expected within the next 6 hours or wind speed exceeds 15 km/h.\n3. Earthing-up and stake tall crops (Banana, Sugarcane, Tomato, Maize) against wind lodging.\n4. During dry heat spells, apply organic mulch and give light evening irrigation.",
            "precautions": "Do not broadcast urea or spray pesticides immediately before rain, as runoff wastes money and pollutes water bodies.",
            "expert": "Follow daily IMD / Meghdoot agromet bulletins and call PMFBY helpline 14447 within 72 hours if severe weather damages insured crops.",
        },
        "crop_selection_season": {
            "problem": "Seasonal crop selection, high-yield variety planning, seed treatment, and sowing practices.",
            "causes": "Matching crop duration and water requirement to the current season (Kharif / Rabi / Summer), soil type (Black clay vs. Red loamy), and local market demand.",
            "steps": "1. Kharif (June–Oct): Paddy (BPT-5204, MTU-1010), Cotton, Redgram, Chilli, Maize, Groundnut.\n2. Rabi (Nov–March): Blackgram, Greengram, Chickpea, Rabi Maize, Tomato, Onion, Groundnut, Mustard.\n3. Summer / Zaid (March–May): Short-duration pulses, Watermelon, Gourds, Sesame, Fodder crops, or Green Manure.\n4. Always use certified, disease-resistant seeds and treat seeds with Trichoderma / Rhizobium before sowing.",
            "precautions": "Avoid sowing the exact same crop family in the same plot every season, and verify water availability for the full crop duration before sowing.",
            "expert": "Consult your local KVK or Rythu Bharosa Kendra / Raitha Samparka Kendra for district-approved high-yielding seed varieties.",
        },
        "market_schemes": {
            "problem": "Agricultural mandi price comparison, selling strategy, and government scheme / subsidy support.",
            "causes": "Price fluctuations across local mandis during peak harvest and lack of awareness about direct benefit transfers, crop insurance, and equipment subsidies.",
            "steps": "1. Compare modal prices across nearby regulated mandis and e-NAM before harvesting and transporting produce.\n2. Grade, clean, and dry grains/chillies to standard moisture levels (12%–14%) to secure top maximum mandi rates.\n3. Check eligibility for PM-KISAN (₹6,000/yr), PMFBY Crop Insurance (1.5%–2% premium), Kisan Credit Card (4% interest loan), and PMKSY Drip Subsidy.\n4. Keep Aadhaar, Land RoR/Pattadar Passbook, and linked bank account ready for portal applications.",
            "precautions": "Never share OTPs or pay unauthorized middlemen for government schemes — apply only on official .gov.in portals or CSC/MeeSeva centers.",
            "expert": "Call e-NAM Helpline (1800-270-0224) for market linkage or Kisan Call Centre (1800-180-1551) for scheme enrollment support.",
        },
        "sustainable_farming": {
            "problem": "Eco-friendly, low-cost sustainable farming, organic inputs, mulching, and weed management.",
            "causes": "Rising chemical input costs, weed competition during the first 30–40 days of crop growth, and declining soil microbial activity.",
            "steps": "1. Apply 25–30 micron silver-black polythene mulch or paddy-straw organic mulch to cut weed growth by 80% and save 35% irrigation water.\n2. Intercrop main crops with Marigold or Cowpea as trap/beneficial crops.\n3. Use bio-fertilizers (Azospirillum, PSB, Potash Mobilizing Bacteria) and Jeevamrutham / Vermicompost.\n4. Perform timely inter-cultivation / weeding at 20 and 40 days after sowing.",
            "precautions": "Test any new bio-formulation or organic practice on a 0.5-acre plot first while tracking crop vigor.",
            "expert": "Connect with your local Farmer Producer Organization (FPO) or KVK for training on natural farming and organic certification.",
        },
        "general": {
            "problem": "Comprehensive Integrated Crop & Field Management Guidance for Your Farm.",
            "causes": "Healthy crop yield depends on synchronized management of 4 pillars: root-zone soil moisture, balanced NPK + micronutrient nutrition, early morning pest/disease scouting, and weather-safe timing.",
            "steps": "1. Field Scouting: Walk your plot in an 'M' pattern early morning; inspect 10 plants (top leaves, underside of lower leaves, stem base).\n2. Moisture Check: Check soil 5–8 cm deep before irrigating; keep drainage channels clear.\n3. Balanced Nutrition: Combine organic manure/vermicompost with split fertilizers based on crop stage.\n4. Preventive Protection: Use yellow/blue sticky traps (10/acre) and neem oil sprays early before pests cross threshold levels.",
            "precautions": "Never mix unverified chemical pesticides and fertilizers together, and avoid spraying during strong wind or expected rain.",
            "expert": "You can ask me about any specific crop (Paddy, Tomato, Chilli, Cotton, Groundnut, Maize, Pulses), or call the toll-free Kisan Call Centre at 1800-180-1551.",
        },
    },
    "te-IN": {
        "crop_health": {
            "problem": "పంట ఆకులు పసుపు రంగులోకి మారడం, ఆకు ముడత, పూత రాలడం లేదా మొక్క పెరుగుదల తగ్గడం.",
            "causes": "పోషకాల లోపం (నత్రజని లోపం వల్ల కింది పాత ఆకులు పసుపు అవుతాయి; జింక్/ఇనుము లోపం వల్ల కొత్త చిగుర్లు పసుపు అవుతాయి), వేర్ల దగ్గర అధిక తేమ లేదా మురుగునీరు నిలవడం, ఆకుల అడుగున రసం పీల్చే పురుగులు (తెల్లదోమ, తామర పురుగులు) ఉండటం.",
            "steps": "1. ముందుగా మొక్క కింది ఆకులు పసుపు అవుతున్నాయా లేక పై చిగుర్లు పసుపు అవుతున్నాయో గమనించండి.\n2. ఉదయం పూట 5–10 ఆకుల అడుగు భాగాన్ని తిప్పి తెల్లదోమ, తామర పురుగులు లేదా పేనుబంక ఉన్నాయేమో చూడండి.\n3. 5–8 సెం.మీ లోతులో మట్టి తేమను పరిశీలించి మాత్రమే నీరు పెట్టండి.\n4. పోషకాల లోపం అయితే లీటరు నీటికి 2 గ్రాముల జింక్ సల్ఫేట్ లేదా 5 గ్రాముల 19-19-19/సూక్ష్మ పోషకాల మిశ్రమాన్ని ఆకులపై పిచికారీ చేయండి.",
            "precautions": "సమస్య నీటి లోపమా, పోషకాల లోపమా లేక పురుగుల దాడా అని నిర్ధారించుకోకుండా ఘాటైన రసాయన మందులు పిచికారీ చేయవద్దు.",
            "expert": "పసుపు రంగు లేదా వాడిపోయే లక్షణాలు వేగంగా వ్యాపిస్తుంటే, దెబ్బతిన్న ఆకు నమూనాతో స్థానిక వ్యవసాయ అధికారి (AO) లేదా KVK (1800-180-1551) ని సంప్రదించండి.",
        },
        "pest_management": {
            "problem": "ఆకులు, కాండం, పూత లేదా కాయలపై పురుగులు మరియు రసం పీల్చే కీటకాల దాడి.",
            "causes": "వాతావరణంలో తేమ మరియు వేడి ఎక్కువగా ఉన్నప్పుడు ఆకులు తినే గొంగళి పురుగులు, కాండం తొలిచే పురుగులు, కాయ తొలిచే పురుగులు లేదా రసం పీల్చే తెల్లదోమ, తామర పురుగులు, దోమపోటు (BPH) పెరగడం.",
            "steps": "1. ఉదయం 6:30 నుండి 8:30 మధ్య పొలంలో తిరిగి ఆకుల అడుగు భాగాన్ని, మొక్క మొదళ్లను పరిశీలించండి.\n2. రసం పీల్చే పురుగుల నివారణకు ఎకరాకు 10 పసుపు మరియు నీలం జిగురు అట్టలు (Sticky traps) కట్టండి.\n3. కాండం/కాయ తొలిచే పురుగుల ఉనికిని గుర్తించేందుకు ఎకరాకు 4–5 లింగాకర్షక బుట్టలు (Pheromone traps) ఏర్పాటు చేయండి.\n4. ప్రాథమిక దశలో వేప గింజల కషాయం (5% NSKE) లేదా వేప నూనె (10,000 ppm @ 2 మి.లీ/లీటరు నీటికి) పిచికారీ చేయండి.",
            "precautions": "నిపుణుల సలహా లేకుండా 2–3 రకాల పురుగుమందులను కలిపి కొట్టవద్దు. తేనెటీగలు తిరిగే సమయంలో (ఉదయం 9 నుండి మధ్యాహ్నం 3 వరకు) ఘాటైన మందులు వాడకండి.",
            "expert": "పురుగు ఉధృతి ఎక్కువగా ఉంటే పురుగు ఫోటో లేదా దెబ్బతిన్న మొక్క భాగాన్ని స్థానిక KVK లేదా రైతు సేవా కేంద్రానికి చూపించి తగిన మందును ఎంచుకోండి.",
        },
        "disease_prevention": {
            "problem": "పంటపై ఆకుమచ్చ తెగులు, అగ్గి తెగులు, బూడిద తెగులు, వేరు కుళ్ళు లేదా కాయ కుళ్ళు లక్షణాలు.",
            "causes": "గాలిలో అధిక తేమ (>80%), ఆకులపై నీరు నిలవడం, మొక్కలు ఒత్తుగా ఉండటం, మురుగునీటి పారుదల లేకపోవడం లేదా విత్తన/నేల ద్వారా వ్యాపించే శిలీంద్రాలు.",
            "steps": "1. బాగా మచ్చలు పడిన కింది ఆకులను కత్తిరించి పొలం బయట గొయ్యి తీసి పాతిపెట్టండి.\n2. ఆకులు తడవకుండా కేవలం మొక్కల వేర్ల దగ్గర మాత్రమే (డ్రిప్ లేదా కాలువల ద్వారా) నీరు పెట్టండి.\n3. పొలంలో నీరు నిల్వ ఉండకుండా మురుగు కాలువలు శుభ్రం చేయండి.\n4. వేరు కుళ్ళు నివారణకు ట్రైకోడెర్మా విరిడి (Trichoderma viride) ను పశువుల ఎరువుతో కలిపి వేర్ల దగ్గర వేయండి.",
            "precautions": "తెగులు సోకిన మొక్కలను కాలువల్లో లేదా ఎరువుల గుంతలో వేయవద్దు; దీనివల్ల తెగులు ఆరోగ్యకరమైన మొక్కలకు వ్యాపిస్తుంది.",
            "expert": "శిలీంద్ర నాశిని (Fungicide) కొనే ముందు స్థానిక వ్యవసాయ అధికారికి ఆకు మచ్చలను చూపించి అది బూజు తెగులా లేక బాక్టీరియా తెగులా అని నిర్ధారించుకోండి.",
        },
        "irrigation": {
            "problem": "పంటకు సరైన నీటి యాజమాన్యం, తడి పెట్టే సమయం మరియు నీటి ఎద్దడి / నీటి నిల్వ నివారణ.",
            "causes": "పంట దశను బట్టి నీరు పెట్టకపోవడం, ఎండ తీవ్రతకు తేమ ఆవిరైపోవడం లేదా పొలంలో నీరు నిలిచిపోయి వేర్లు కుళ్ళిపోవడం.",
            "steps": "1. నీరు పెట్టే ముందు మొక్క మొదలు వద్ద 5–8 సెం.మీ లోతులో మట్టిని చేతితో పట్టుకొని తేమను పరిశీలించండి.\n2. ఉదయం (6:00–8:30) లేదా సాయంత్రం చల్లని వేళల్లో మాత్రమే నీరు పెట్టండి; దీనివల్ల 25–30% నీరు ఆదా అవుతుంది.\n3. వరి పొలంలో దుబ్బు చేసే దశలో 2–3 సెం.మీ నీరు మాత్రమే ఉంచండి (మార్చి మార్చి తడి పెట్టే AWD పద్ధతి ఉత్తమం); పొట్ట దశలో 5 సెం.మీ నీరు ఉంచండి.\n4. టమాటా, మిర్చి, కూరగాయ పంటలకు డ్రిప్ ఇరిగేషన్ మరియు మల్చింగ్ వాడుతూ మురుగు కాలువలు తెరిచి ఉంచండి.",
            "precautions": "మిర్చి, టమాటా, పత్తి, పప్పుధాన్య పంటల్లో 12 గంటల కంటే ఎక్కువ సేపు నీరు నిల్వ ఉండనివ్వకండి — వేరు కుళ్ళు వెంటనే ఆశిస్తుంది.",
            "expert": "డ్రిప్ మరియు స్ప్రింక్లర్ రాయితీ (55% నుండి 90% సబ్సిడీ) కోసం మీ మండల ఉద్యానవన / వ్యవసాయ అధికారిని సంప్రదించండి.",
        },
        "fertilizer_guidance": {
            "problem": "పంటకు సమతుల్య ఎరువుల యాజమాన్యం (NPK + సూక్ష్మ పోషకాలు) మరియు వేయాల్సిన సమయం.",
            "causes": "భూసార పరీక్ష లేకుండా కేవలం యూరియా మాత్రమే అధికంగా వేయడం లేదా తగినంత తేమ లేని నేలలో ఎరువులు చల్లడం.",
            "steps": "1. భూసార పరీక్ష (Soil Health Card) ఆధారంగా నత్రజని, భాస్వరం, పొటాష్ (NPK) ఎరువులను సమతుల్యంగా వాడండి.\n2. ఆఖరి దుక్కిలో ఎకరాకు 4–5 టన్నుల బాగా చివికిన పశువుల ఎరువు లేదా 1 టన్ను వర్మీకంపోస్ట్ వేయండి.\n3. నత్రజని (వేప పూత పూసిన యూరియా) ని ఒకేసారి కాకుండా 3 విడతలుగా (విత్తేటప్పుడు, ఎదుగుదల దశలో, పూత/పొట్ట దశలో) వేయండి.\n4. పూత మరియు కాయ ఊరే దశలో పొటాష్ మరియు సూక్ష్మ పోషకాలు (జింక్, బోరాన్, మెగ్నీషియం) అందిస్తే దిగుబడి, నాణ్యత పెరుగుతాయి.",
            "precautions": "నేలలో తగినంత తేమ ఉన్నప్పుడు మాత్రమే ఎరువులు వేయండి. నత్రజని (యూరియా) ఎక్కువగా వేస్తే మొక్కలు ఏపుగా పెరిగి పురుగులు, తెగుళ్లు ఎక్కువగా ఆశిస్తాయి.",
            "expert": "మీ పొలం మట్టి నమూనాను సమీప భూసార పరీక్షా కేంద్రానికి లేదా KVK కి తీసుకెళ్లి పంట వారీగా ఎరువుల మోతాదు తెలుసుకోండి.",
        },
        "soil_health": {
            "problem": "నేల సారం, సేంద్రియ కర్బనం, భూమి pH సమతుల్యత మరియు నీటి నిల్వ సామర్థ్యాన్ని పెంచడం.",
            "causes": "వరుసగా ఒకే పంట సాగు చేయడం, సేంద్రియ ఎరువులు తగ్గడం, చౌడు/క్షార లేదా ఆమ్ల నేల సమస్యలు (ఉత్తమ నేల pH: 6.5 నుండి 7.2).",
            "steps": "1. పంట వేసే ముందు పొలంలో 8–10 చోట్ల మట్టిని సేకరించి భూసార పరీక్ష (Soil Health Card) చేయించుకోండి.\n2. ప్రధాన పంటకు ముందు జీలుగ, జనుము లేదా పిల్లిపెసర వంటి పచ్చిరొట్ట పైర్లను పెంచి 45 రోజులకు భూమిలో కలియదున్నండి.\n3. వరి లేదా వాణిజ్య పంటల తర్వాత కంది, మినుము, పెసర వంటి పప్పుధాన్య పంటలతో పంట మార్పిడి చేయండి.\n4. చౌడు నేలల సవరణకు భూసార పరీక్ష ప్రకారం జిప్సం (Gypsum) వాడండి.",
            "precautions": "పంట కోసిన తర్వాత కొయ్యకాళ్లను లేదా గడ్డిని పొలంలో కాల్చవద్దు — దీనివల్ల నేలలోని మిత్ర సూక్ష్మజీవులు, వానపాములు నశిస్తాయి.",
            "expert": "సీజన్ ప్రారంభానికి ముందు మీ భూసార పరీక్ష కార్డును స్థానిక వ్యవసాయ అధికారికి చూపించి నేల సవరణ చర్యలు చేపట్టండి.",
        },
        "weather_precautions": {
            "problem": "వర్ష సూచన, ఈదురు గాలులు, అధిక తేమ లేదా ఎండ తీవ్రత నుండి పంటలను రక్షించుకోవడం.",
            "causes": "భారీ వర్షాల వల్ల పొలంలో నీరు నిలవడం, మందులు కొట్టుకుపోవడం, గాలికి మొక్కలు పడిపోవడం లేదా అధిక ఎండకు పూత రాలడం.",
            "steps": "1. వర్ష సూచన (50% కంటే ఎక్కువ) ఉన్నప్పుడు పొలం చుట్టూ మురుగు కాలువలు తెరిచి అదనపు నీరు బయటకు వెళ్లేలా చేయండి.\n2. రాబోయే 6 గంటల్లో వర్షం పడే అవకాశం ఉన్నా లేదా గాలి వేగం ఎక్కువగా ఉన్నా పురుగుమందులు/ఎరువులు పిచికారీ చేయవద్దు.\n3. అరటి, చెరకు, టమాటా, మొక్కజొన్న వంటి పంటలకు మట్టి ఎగదోసి కర్రలతో ఊతం ఇవ్వండి.\n4. ఎండ తీవ్రత ఎక్కువగా ఉన్నప్పుడు మల్చింగ్ వేసి సాయంత్రం వేళ తేలికపాటి తడి ఇవ్వండి.",
            "precautions": "వర్షం పడే ముందు యూరియా చల్లడం లేదా మందులు కొట్టడం వల్ల ఖర్చు వృథా అవుతుంది.",
            "expert": "ప్రకృతి వైపరీత్యాల వల్ల పంట నష్టం జరిగితే 72 గంటల్లోపు PMFBY పంట భీమా హెల్ప్‌లైన్ 14447 లేదా కిసాన్ కాల్ సెంటర్ 1800-180-1551 కు తెలియజేయండి.",
        },
        "crop_selection_season": {
            "problem": "సీజన్‌కు అనుకూలమైన పంటల ఎంపిక, అధిక దిగుబడినిచ్చే రకాలు మరియు విత్తన శుద్ధి.",
            "causes": "ప్రస్తుత సీజన్ (ఖరీఫ్ / రబీ / వేసవి), నేల రకం (నల్లరేగడి / ఎర్ర నేల), నీటి లభ్యత మరియు మార్కెట్ డిమాండ్‌కు తగిన పంటను ఎంచుకోవడం.",
            "steps": "1. ఖరీఫ్ సీజన్ (జూన్–అక్టోబర్): వరి (BPT-5204, MTU-1010, RNR-15048), పత్తి, మిర్చి, కంది, మొక్కజొన్న, వేరుశనగ అనుకూలం.\n2. రబీ సీజన్ (నవంబర్–మార్చి): మినుము, పెసర, శనగ, రబీ మొక్కజొన్న, టమాటా, ఉల్లి, వేరుశనగ, కూరగాయలు అత్యంత అనుకూలం.\n3. వేసవి / జైద్ (మార్చి–మే): తక్కువ కాలపరిమితి గల పెసర, నువ్వులు, పుచ్చకాయ, కూరగాయలు లేదా జీలుగ/జనుము పచ్చిరొట్ట పంటలు వేయండి.\n4. విత్తే ముందు విత్తనాలను ట్రైకోడెర్మా విరిడి లేదా రైజోబియం కల్చర్‌తో విత్తన శుద్ధి చేయండి.",
            "precautions": "ప్రతి సీజన్‌లో ఒకే పొలంలో ఒకే రకమైన పంట వేయకుండా పంట మార్పిడి పాటించండి; ధృవీకరించిన (Certified) విత్తనాలనే వాడండి.",
            "expert": "మీ మండలానికి అనుకూలమైన మేలైన విత్తన రకాల కోసం స్థానిక కృషి విజ్ఞాన కేంద్రం (KVK) లేదా రైతు భరోసా/సేవా కేంద్రాన్ని సంప్రదించండి.",
        },
        "market_schemes": {
            "problem": "వ్యవసాయ మార్కెట్ (మండి) ధరల పోలిక, పంట అమ్మకం మరియు ప్రభుత్వ పథకాలు / సబ్సిడీల సమాచారం.",
            "causes": "వివిధ మార్కెట్లలో ధరల వ్యత్యాసం మరియు కేంద్ర/రాష్ట్ర ప్రభుత్వ రాయితీ పథకాలపై సరైన సమాచారం అవసరమవడం.",
            "steps": "1. పంటను మార్కెట్‌కు తీసుకెళ్లే ముందు సమీప మండిలలో మరియు e-NAM పోర్టల్‌లో మోడల్ ధరలను (Modal Prices) సరిపోల్చుకోండి.\n2. ధాన్యం/మిర్చిని శుభ్రంగా గ్రేడింగ్ చేసి, సరైన తేమ శాతం (12%–14%) ఉండేలా ఆరబెడితే గరిష్ట ధర లభిస్తుంది.\n3. PM-KISAN (ఏటా ₹6,000), PMFBY పంట భీమా, కిసాన్ క్రెడిట్ కార్డ్ (4% వడ్డీకే పంట రుణం), మరియు డ్రిప్ ఇరిగేషన్ సబ్సిడీ పథకాలకు దరఖాస్తు చేసుకోండి.\n4. ఆధార్ కార్డు, పట్టాదారు పాస్‌బుక్ (RoR), మరియు బ్యాంక్ ఖాతా వివరాలను సిద్ధంగా ఉంచుకోండి.",
            "precautions": "ప్రభుత్వ పథకాల కోసం మధ్యవర్తులకు డబ్బులు ఇవ్వకండి లేదా OTP లు చెప్పకండి — అధికారిక .gov.in పోర్టల్స్ లేదా రైతు సేవా కేంద్రాల ద్వారానే దరఖాస్తు చేయండి.",
            "expert": "మార్కెట్ సమాచారం కోసం e-NAM హెల్ప్‌లైన్ (1800-270-0224) లేదా పథకాల సహాయం కోసం కిసాన్ కాల్ సెంటర్ (1800-180-1551) కి కాల్ చేయండి.",
        },
        "sustainable_farming": {
            "problem": "తక్కువ ఖర్చుతో సుస్థిర వ్యవసాయం, సేంద్రియ ఎరువులు, మల్చింగ్ మరియు కలుపు నివారణ.",
            "causes": "పెరుగుతున్న రసాయన ఎరువులు/మందుల ఖర్చులు, పంట మొదటి 30–40 రోజుల్లో కలుపు సమస్య మరియు నేలలో సేంద్రియ కర్బనం తగ్గడం.",
            "steps": "1. కూరగాయలు, మిర్చి, టమాటా పంటల్లో మల్చింగ్ షీట్ లేదా ఎండుగడ్డి మల్చింగ్ వేయడం వల్ల 80% కలుపు తగ్గి 35% నీరు ఆదా అవుతుంది.\n2. ప్రధాన పంట చుట్టూ బంతి (Marigold) లేదా అలసందను ఎర పంటగా (Trap crop) సాగు చేయండి.\n3. అజోస్పైరిల్లమ్, ఫాస్ఫోబాక్టీరియా వంటి జీవ ఎరువులు మరియు జీవామృతం / వర్మీకంపోస్ట్ వాడండి.\n4. విత్తిన 20 మరియు 40 రోజులకు అంతర కృషి చేసి కలుపు తొలగించండి.",
            "precautions": "కొత్త సేంద్రియ లేదా జీవ ఎరువులను రసాయన పురుగుమందులతో కలిపి వాడవద్దు.",
            "expert": "ప్రకృతి వ్యవసాయం మరియు సేంద్రియ ధృవీకరణ శిక్షణ కోసం స్థానిక KVK లేదా FPO (రైతు ఉత్పత్తిదారుల సంఘం) ని సంప్రదించండి.",
        },
        "general": {
            "problem": "సమగ్ర పంట యాజమాన్యం మరియు ఆచరణాత్మక వ్యవసాయ సూచనలు (Integrated Crop Advisory).",
            "causes": "పంట ఆరోగ్యంగా పెరిగి అధిక దిగుబడి రావడానికి నేల తేమ, సమతుల్య పోషకాలు, సకాలంలో సస్యరక్షణ మరియు వాతావరణ అనుకూలత ప్రధాన పాత్ర పోషిస్తాయి.",
            "steps": "1. పంట పరిశీలన: ఉదయం వేళ పొలంలో నడుస్తూ 10 మొక్కల పై ఆకులు, కింది ఆకుల అడుగు భాగం మరియు కాండం మొదలును పరిశీలించండి.\n2. నీటి యాజమాన్యం: 5–8 సెం.మీ లోతులో మట్టి తేమను చూసి ఉదయం లేదా సాయంత్రం మాత్రమే తడి పెట్టండి; మురుగు కాలువలు శుభ్రంగా ఉంచండి.\n3. సమతుల్య పోషణ: పశువుల ఎరువు/వర్మీకంపోస్ట్‌తో పాటు పంట దశను బట్టి విడతల వారీగా ఎరువులు అందించండి.\n4. ముందస్తు సస్యరక్షణ: ఎకరాకు 10 పసుపు/నీలం జిగురు అట్టలు పెట్టి, పురుగుల తొలి దశలో 5% వేప గింజల కషాయం పిచికారీ చేయండి.",
            "precautions": "సమస్యను నిర్ధారించుకోకుండా రకరకాల రసాయన మందులను కలిపి వాడవద్దు మరియు వర్షం/బలమైన గాలి ఉన్నప్పుడు పిచికారీ చేయవద్దు.",
            "expert": "మీరు వరి, టమాటా, మిర్చి, పత్తి, వేరుశనగ, మొక్కజొన్న, ఎరువులు, నీటి యాజమాన్యం లేదా మార్కెట్ ధరల గురించి ఏ ప్రశ్ననైనా అడగవచ్చు, లేదా ఉచిత కిసాన్ కాల్ సెంటర్ 1800-180-1551 కు కాల్ చేయవచ్చు.",
        },
    },
    "hi-IN": {
        "crop_health": {
            "problem": "फसल की पत्तियों का पीला पड़ना, मुड़ना, फूल झड़ना या पौधों की बढ़वार रुकना।",
            "causes": "पोषक तत्वों की कमी (नाइट्रोजन की कमी से निचली पुरानी पत्तियां पीली होती हैं; जिंक/आयरन की कमी से नई ऊपरी पत्तियां पीली होती हैं), अधिक पानी या जल निकासी न होना, या पत्तियों के नीचे रस चूसने वाले कीट (सफेद मक्खी, थ्रिप्स)।",
            "steps": "1. जांचें कि पीलापन पुरानी निचली पत्तियों पर है या नई ऊपरी पत्तियों पर।\n2. सुबह के समय 5–10 पत्तियों को पलटकर सफेद मक्खी, माहू या थ्रिप्स की जांच करें।\n3. सिंचाई से पहले 5–8 सेमी गहराई पर मिट्टी की नमी जांचें।\n4. पोषक तत्वों की कमी होने पर जिंक सल्फेट या संतुलित सूक्ष्म पोषक तत्वों का पर्ण छिड़काव करें।",
            "precautions": "सही कारण जाने बिना तेज रासायनिक कीटनाशक या अत्यधिक यूरिया का प्रयोग न करें।",
            "expert": "यदि पीलापन या मुरझाना तेजी से फैल रहा हो, तो प्रभावित पत्ती लेकर स्थानीय कृषि अधिकारी या KVK (1800-180-1551) से संपर्क करें।",
        },
        "pest_management": {
            "problem": "पत्तियों, तनों, फूलों या फलों पर कीटों, सुंडियों और रस चूसक कीड़ों का प्रकोप।",
            "causes": "गर्म और आर्द्र मौसम में तना छेदक, फल छेदक, गुलाबी सुंडी या रस चूसने वाले कीट (सफेद मक्खी, थ्रिप्स, माहू, BPH) का तेजी से बढ़ना।",
            "steps": "1. सुबह 6:30 से 8:30 बजे के बीच पत्तियों के निचले हिस्से और तने के आधार की जांच करें।\n2. रस चूसने वाले कीटों के लिए प्रति एकड़ 10 पीले/नीले चिपचिपे ट्रैप (Sticky traps) लगाएं।\n3. सुंडियों की निगरानी हेतु प्रति एकड़ 4–5 फेरोमोन ट्रैप लगाएं।\n4. शुरुआती अवस्था में 5% नीम निंबोली अर्क (NSKE) या नीम तेल (2 मिली/लीटर) का छिड़काव करें।",
            "precautions": "बिना विशेषज्ञ सलाह के 2–3 रासायनिक दवाओं को आपस में न मिलाएं और मधुमक्खियों के सक्रिय समय में छिड़काव न करें।",
            "expert": "अधिक प्रकोप होने पर कीट की फोटो अपने नजदीकी कृषि विज्ञान केंद्र (KVK) को दिखाकर सुरक्षित IPM सलाह लें।",
        },
        "disease_prevention": {
            "problem": "पत्तियों पर धब्बे, झुलसा रोग (Blight), फफूंद, उकठा (Wilt) या जड़/फल सड़न के लक्षण।",
            "causes": "अधिक नमी (>80%), पत्तियों पर पानी रुकना, खेत में जलभराव या बीज/मिट्टी जनित फफूंद व जीवाणु संक्रमण।",
            "steps": "1. गंभीर रूप से प्रभावित निचली पत्तियों को तोड़कर खेत से बाहर मिट्टी में दबा दें।\n2. पत्तियों को भिगोने के बजाय केवल जड़ों के पास (ड्रिप या नाली से) पानी दें।\n3. खेत में जल निकासी और हवा का प्रवाह बेहतर बनाएं।\n4. जड़ सड़न की रोकथाम के लिए ट्राइकोडर्मा विरिडी को गोबर की खाद में मिलाकर प्रयोग करें।",
            "precautions": "रोगग्रस्त पौधों के अवशेषों को सिंचाई नाली या कम्पोस्ट गड्ढे में न डालें।",
            "expert": "कोई भी फफूंदनाशक खरीदने से पहले स्थानीय कृषि अधिकारी या KVK से रोग की सही पहचान कराएं।",
        },
        "irrigation": {
            "problem": "फसल में सिंचाई समय-सारणी, पानी की सही मात्रा और जलभराव / सूखे से बचाव।",
            "causes": "असमान सिंचाई अंतराल, दोपहर में अधिक वाष्पीकरण, या भारी मिट्टी में पानी जमा होने से जड़ों को नुकसान।",
            "steps": "1. सिंचाई शुरू करने से पहले जड़ क्षेत्र में 5–8 सेमी गहराई पर मिट्टी की नमी जांचें।\n2. हमेशा सुबह (6:00–8:30 बजे) या शाम के ठंडे समय में सिंचाई करें, इससे 25–30% पानी बचता है।\n3. धान में कल्ले निकलते समय केवल 2–3 सेमी पानी रखें (AWD विधि) और फूल आते समय 5 सेमी पानी रखें।\n4. टमाटर, मिर्च और सब्जियों में ड्रिप सिंचाई व मल्चिंग अपनाएं तथा जल निकासी नालियां खुली रखें।",
            "precautions": "सब्जी, दलहन और कपास की फसलों में 12 घंटे से अधिक पानी जमा न होने दें, अन्यथा उकठा और जड़ सड़न रोग फैलता है।",
            "expert": "ड्रिप और स्प्रिंकलर सिंचाई पर 55%–90% सरकारी सब्सिडी (PMKSY) के लिए अपने ब्लॉक कृषि अधिकारी से संपर्क करें।",
        },
        "fertilizer_guidance": {
            "problem": "फसल के लिए संतुलित उर्वरक प्रबंधन (NPK + सूक्ष्म पोषक तत्व) और खाद देने का सही समय।",
            "causes": "बिना मिट्टी जांच के केवल यूरिया का अधिक उपयोग करना या सूखी मिट्टी में खाद डालना।",
            "steps": "1. मृदा स्वास्थ्य कार्ड (Soil Health Card) की सिफारिश के अनुसार NPK और सूक्ष्म पोषक तत्व दें।\n2. बुवाई से पहले प्रति एकड़ 4–5 टन सड़ी हुई गोबर की खाद या 1 टन वर्मीकम्पोस्ट मिलाएं।\n3. नाइट्रोजन (नीम लेपित यूरिया) को 3 बराबर किस्तों में (बुवाई, वानस्पतिक वृद्धि और फूल आने पर) दें।\n4. फूल और फल बनते समय पोटाश व जिंक/बोरॉन की पूर्ति करें जिससे दाने चमकदार और वजनदार बनें।",
            "precautions": "सूखी मिट्टी में उर्वरक न डालें और अत्यधिक यूरिया से बचें क्योंकि इससे कीटों और रोगों का आक्रमण बढ़ता है।",
            "expert": "अपनी फसल और मिट्टी के अनुसार सटीक उर्वरक तालिका के लिए नजदीकी मृदा परीक्षण प्रयोगशाला या KVK से संपर्क करें।",
        },
        "soil_health": {
            "problem": "मिट्टी की उर्वरता, जैविक कार्बन, pH संतुलन और जल धारण क्षमता में सुधार।",
            "causes": "लगातार एक ही फसल उगाना, जैविक खाद की कमी, या मिट्टी का क्षारीय/अम्लीय होना (आदर्श pH: 6.5–7.2)।",
            "steps": "1. बुवाई से पहले खेत के 8–10 स्थानों से मिट्टी का नमूना लेकर Soil Health Card जांच कराएं।\n2. मुख्य फसल से पहले ढैंचा या सनई की हरी खाद उगाएं और 45 दिन पर मिट्टी में मिला दें।\n3. अनाज फसलों के बाद दलहनी फसलों (मूंग, उड़द, चना, अरहर) का फसल चक्र अपनाएं।\n4. क्षारीय मिट्टी के सुधार हेतु जिप्सम और अम्लीय मिट्टी के लिए चूने का प्रयोग जांच रिपोर्ट के अनुसार करें।",
            "precautions": "खेत में पराली या फसल अवशेष कभी न जलाएं — इससे मित्र जीवाणु और केंचुए नष्ट हो जाते हैं।",
            "expert": "सीजन से पहले अपनी मिट्टी जांच रिपोर्ट स्थानीय KVK वैज्ञानिक को दिखाकर सुधार करें।",
        },
        "weather_precautions": {
            "problem": "भारी बारिश, आंधी-तूफान, जलभराव या लू (Heatwave) से खड़ी फसल की सुरक्षा।",
            "causes": "अचानक भारी वर्षा से जलभराव व दवा का धुल जाना, तेज हवा से फसल गिरना, या अधिक तापमान से फूल झड़ना।",
            "steps": "1. बारिश की संभावना (>50%) होने पर खेत की जल निकासी नालियां तुरंत साफ करें।\n2. अगले 6 घंटों में बारिश या तेज हवा की संभावना होने पर किसी भी कीटनाशक/खाद का छिड़काव न करें।\n3. गन्ना, केला, टमाटर और मक्का जैसी फसलों में मिट्टी चढ़ाएं और सहारा दें।\n4. तेज गर्मी के दौरान नमी बचाने के लिए मल्चिंग करें और शाम को हल्की सिंचाई दें।",
            "precautions": "बारिश से ठीक पहले यूरिया या कीटनाशक का प्रयोग न करें।",
            "expert": "मौसम से फसल नुकसान होने पर 72 घंटे के भीतर प्रधानमंत्री फसल बीमा योजना (PMFBY) हेल्पलाइन 14447 या किसान कॉल सेंटर 1800-180-1551 पर सूचित करें।",
        },
        "crop_selection_season": {
            "problem": "मौसम के अनुसार उपयुक्त फसल का चुनाव, उन्नत किस्में और बीज उपचार।",
            "causes": "वर्तमान सीजन (खरीफ / रबी / जायद), मिट्टी के प्रकार और पानी की उपलब्धता के अनुसार सही फसल चुनना।",
            "steps": "1. खरीफ सीजन (जून–अक्टूबर): धान, कपास, मिर्च, अरहर, मक्का, मूंगफली और सोयाबीन उपयुक्त हैं।\n2. रबी सीजन (नवंबर–मार्च): चना, गेहूं, सरसों, उड़द, मूंग, रबी मक्का, टमाटर और प्याज की खेती करें।\n3. जायद / ग्रीष्म (मार्च–मई): मूंग, तिल, तरबूज, लौकी/करेला जैसी सब्जियां या हरी खाद उगाएं।\n4. हमेशा प्रमाणित बीज चुनें और बुवाई से पहले ट्राइकोडर्मा व राइजोबियम से बीज उपचार करें।",
            "precautions": "हर सीजन में एक ही खेत में एक ही परिवार की फसल न उगाएं; फसल चक्र अवश्य अपनाएं।",
            "expert": "अपने जिले के लिए अनुशंसित उन्नत किस्मों की जानकारी हेतु स्थानीय KVK या कृषि विभाग से संपर्क करें।",
        },
        "market_schemes": {
            "problem": "मंडी भाव की तुलना, फसल बिक्री रणनीति और सरकारी कृषि योजनाओं / सब्सिडी की जानकारी।",
            "causes": "विभिन्न मंडियों में भाव का अंतर और सरकारी सहायता योजनाओं की सही प्रक्रिया जानना।",
            "steps": "1. फसल बेचने से पहले नजदीकी मंडियों और e-NAM पोर्टल पर मॉडल भाव (Modal Price) की तुलना करें।\n2. उपज को साफ करके और नमी 12%–14% तक सुखाकर मंडी ले जाएं ताकि अधिकतम भाव मिले।\n3. PM-KISAN (₹6,000/वर्ष), PMFBY फसल बीमा, किसान क्रेडिट कार्ड (KCC — 4% ब्याज ऋण) और ड्रिप सब्सिडी का लाभ लें।\n4. आवेदन के लिए आधार, भूमि खतौनी/पट्टा और बैंक पासबुक तैयार रखें।",
            "precautions": "किसी भी सरकारी योजना के लिए बिचौलियों को पैसे न दें और केवल आधिकारिक .gov.in पोर्टल या CSC केंद्र का उपयोग करें।",
            "expert": "मंडी जानकारी के लिए e-NAM हेल्पलाइन (1800-270-0224) और योजनाओं के लिए किसान कॉल सेंटर (1800-180-1551) पर कॉल करें।",
        },
        "sustainable_farming": {
            "problem": "कम लागत वाली टिकाऊ और जैविक खेती, मल्चिंग तथा खरपतवार नियंत्रण।",
            "causes": "बढ़ती रासायनिक लागत, शुरुआती 30–40 दिनों में खरपतवार की समस्या और मिट्टी में जीवांश की कमी।",
            "steps": "1. सब्जियों और मिर्च/टमाटर में मल्चिंग शीट या पुआल मल्चिंग लगाएं जिससे 80% खरपतवार रुकते हैं और 35% पानी बचता है।\n2. मुख्य फसल के चारों ओर गेंदा (Marigold) या लोबिया ट्रैप क्रॉप के रूप में लगाएं।\n3. जैव उर्वरक (एजोस्पिरिलम, PSB) और जीवामृत / वर्मीकम्पोस्ट का उपयोग करें।\n4. बुवाई के 20 और 40 दिन बाद समय पर निराई-गुड़ाई करें।",
            "precautions": "जैव उर्वरकों को रासायनिक कीटनाशकों या फफूंदनाशकों के साथ मिलाकर प्रयोग न करें।",
            "expert": "प्राकृतिक खेती और जैविक प्रमाणीकरण प्रशिक्षण के लिए अपने जिले के KVK या FPO से जुड़ें।",
        },
        "general": {
            "problem": "समग्र फसल प्रबंधन और व्यावहारिक कृषि मार्गदर्शन (Integrated Crop Advisory)।",
            "causes": "अच्छी पैदावार के लिए मिट्टी की सही नमी, संतुलित पोषण, समय पर कीट-रोग निगरानी और मौसम आधारित निर्णय आवश्यक हैं।",
            "steps": "1. खेत निरीक्षण: सुबह खेत में घूमकर 10 पौधों की ऊपरी व निचली पत्तियों और तने की जांच करें।\n2. सिंचाई प्रबंधन: 5–8 सेमी गहराई पर नमी देखकर सुबह या शाम सिंचाई करें और जल निकासी साफ रखें।\n3. संतुलित पोषण: गोबर की खाद/वर्मीकम्पोस्ट के साथ फसल अवस्था के अनुसार किस्तों में उर्वरक दें।\n4. सुरक्षा: प्रति एकड़ 10 पीले/नीले चिपचिपे ट्रैप लगाएं और शुरुआती कीट नियंत्रण हेतु नीम तेल का छिड़काव करें।",
            "precautions": "बिना पहचान के कई रासायनिक दवाएं न मिलाएं और तेज हवा या बारिश से पहले छिड़काव न करें।",
            "expert": "आप धान, टमाटर, मिर्च, कपास, मूंगफली, मक्का, सिंचाई, खाद या मंडी भाव के बारे में कोई भी प्रश्न पूछ सकते हैं, या टोल-फ्री किसान कॉल सेंटर 1800-180-1551 पर कॉल कर सकते हैं।",
        },
    },
    "ta-IN": {
        "crop_health": {
            "problem": "பயிர் இலைகள் மஞ்சளாக மாறுதல், இலை சுருளுதல், பூ உதிர்தல் அல்லது வளர்ச்சி குறைதல்.",
            "causes": "ஊட்டச்சத்து குறைபாடு (நைட்ரஜன், துத்தநாகம், இரும்பு), அதிக நீர் தேக்கம் அல்லது இலைகளின் அடியில் சாறு உறிஞ்சும் பூச்சிகள் (வெள்ளை ஈ, இலைப்பேன்).",
            "steps": "1. பழைய கீழ் இலைகளா அல்லது புதிய மேல் இலைகளா மஞ்சளாகின்றன என்பதைக் கவனிக்கவும்.\n2. காலை வேளையில் 5–10 இலைகளின் அடிப்பகுதியில் பூச்சிகள் உள்ளதா எனப் பார்க்கவும்.\n3. 5–8 செ.மீ ஆழத்தில் மண்ணின் ஈரப்பதத்தைச் சரிபார்க்கவும்.\n4. நுண்ணூட்டச்சத்து குறைபாடு இருந்தால் துத்தநாக சல்பேட் அல்லது நுண்ணூட்டக் கலவையைத் தெளிக்கவும்.",
            "precautions": "காரணத்தை உறுதிப்படுத்தாமல் கடுமையான இரசாயன பூச்சிக்கொல்லிகளைத் தெளிக்க வேண்டாம்.",
            "expert": "மஞ்சள் நிறம் வேகமாகப் பரவினால் பாதிக்கப்பட்ட இலையுடன் உள்ளூர் வேளாண் அதிகாரி அல்லது KVK (1800-180-1551)-ஐ அணுகவும்.",
        },
        "pest_management": {
            "problem": "இலைகள், தண்டு மற்றும் காய்களில் பூச்சி மற்றும் புழுக்களின் தாக்குதல்.",
            "causes": "தண்டு துளைப்பான், காய்ப்புழு அல்லது சாறு உறிஞ்சும் பூச்சிகளின் (வெள்ளை ஈ, இலைப்பேன், புகையான்) பெருக்கம்.",
            "steps": "1. காலை வேளையில் இலைகளின் மேல் மற்றும் கீழ்ப் பகுதியை ஆய்வு செய்யவும்.\n2. ஏக்கருக்கு 10 மஞ்சள்/நீல ஒட்டும் அட்டைகள் மற்றும் 5 இனக்கவர்ச்சிப் பொறிகளை அமைக்கவும்.\n3. 5% வேப்பங்கொட்டைச் சாறு (NSKE) அல்லது வேப்பெண்ணெய் (2 மி.லி/லிட்டர்) தெளிக்கவும்.",
            "precautions": "நன்மை செய்யும் பூச்சிகளை அழிக்கும் இரசாயனங்களைத் தவிர்க்கவும்; பல மருந்துகளைக் கலக்க வேண்டாம்.",
            "expert": "ஒருங்கிணைந்த பூச்சி மேலாண்மை (IPM) ஆலோசனைக்கு உள்ளூர் வேளாண் அதிகாரியை அணுகவும்.",
        },
        "disease_prevention": {
            "problem": "இலைப் புள்ளிகள், கருகல் நோய், சாம்பல் நோய் அல்லது வேர் அழுகல் அறிகுறிகள்.",
            "causes": "அதிக ஈரப்பதம், இலைகள் மீது நீர் தேங்குதல் அல்லது பூஞ்சை/பாக்டீரியா தொற்று.",
            "steps": "1. பாதிக்கப்பட்ட இலைகளை அகற்றி வயலுக்கு வெளியே அழிக்கவும்.\n2. வேர்ப்பகுதியில் மட்டும் நீர் பாய்ச்சவும் மற்றும் வடிகால் வசதியை மேம்படுத்தவும்.\n3. டிரைக்கோடெர்மா விரிடி (Trichoderma viride) உயிர் பூஞ்சாணக் கொல்லியை தொழு உரத்துடன் கலந்து இடவும்.",
            "precautions": "நோய் தாக்கிய செடிகளை உரக்குழியில் அல்லது வாய்க்காலில் போட வேண்டாம்.",
            "expert": "மருந்து வாங்கும் முன் உள்ளூர் KVK-இல் காண்பித்து நோயை உறுதிப்படுத்தவும்.",
        },
        "irrigation": {
            "problem": "பயிர் நீர்ப்பாசன திட்டமிடல் மற்றும் நீர் தேக்கம் / வறட்சி தடுப்பு.",
            "causes": "சீரற்ற நீர்ப்பாசனம் அல்லது வயலில் வடிகால் வசதி இல்லாமை.",
            "steps": "1. நீர் பாய்ச்சும் முன் 5–8 செ.மீ ஆழத்தில் மண்ணின் ஈரப்பதத்தைச் சரிபார்க்கவும்.\n2. காலை (6:00–8:30) அல்லது மாலை வேளையில் நீர் பாய்ச்சுவதன் மூலம் 30% நீரைச் சேமிக்கலாம்.\n3. நெல்லில் காய்ச்சலும் பாய்ச்சலும் (AWD) முறையில் 2–3 செ.மீ நீர் பராமரிக்கவும்.\n4. காய்கறி மற்றும் மிளகாய் பயிர்களுக்கு சொட்டு நீர்ப்பாசனம் மற்றும் மூடாக்கு பயன்படுத்தவும்.",
            "precautions": "மிளகாய், தக்காளி மற்றும் பயறு வகைகளின் வேர்ப்பகுதியில் நீர் தேங்க விடாதீர்கள்.",
            "expert": "சொட்டு நீர்ப்பாசன மானியம் (PMKSY) பெற உங்கள் வட்டார வேளாண்/தோட்டக்கலை அதிகாரியை அணுகவும்.",
        },
        "fertilizer_guidance": {
            "problem": "சரிவிகித ஊட்டச்சத்து மற்றும் உர மேலாண்மை (NPK + நுண்ணூட்டச்சத்துக்கள்).",
            "causes": "மண் பரிசோதனை இன்றி யூரியாவை மட்டும் அதிகம் பயன்படுத்துதல்.",
            "steps": "1. மண் வள அட்டை (Soil Health Card) பரிந்துரைப்படி உரமிடவும்.\n2. விதைப்புக்கு முன் ஏக்கருக்கு 4–5 டன் மக்கிய தொழு உரம் அல்லது மண்புழு உரம் இடவும்.\n3. தழைச்சத்தை (வேப்பம் புண்ணாக்கு கலந்த யூரியா) 3 பிரிவுகளாகப் பிரித்து வழங்கவும்.",
            "precautions": "மண்ணில் ஈரப்பதம் இல்லாதபோது உரமிட வேண்டாம்.",
            "expert": "உங்கள் பயிர் மற்றும் மண்ணுக்கு ஏற்ற உர அளவுகளை அறிய உள்ளூர் KVK-ஐ அணுகவும்.",
        },
        "soil_health": {
            "problem": "மண் வளம், கரிமச் சத்து மற்றும் pH சமநிலையை மேம்படுத்துதல்.",
            "causes": "தொடர்ந்து ஒரே பயிரைச் சாகுபடி செய்தல் மற்றும் இயற்கை உரங்கள் குறைதல்.",
            "steps": "1. மண் பரிசோதனை செய்து மண் வள அட்டை பெறவும்.\n2. சணப்பு அல்லது தக்கைப்பூண்டு போன்ற பசுந்தாள் உரப் பயிர்களை வளர்த்து மண்ணில் மடக்கி உழவும்.\n3. பயறு வகைப் பயிர்களுடன் பயிர் சுழற்சி செய்யவும்.",
            "precautions": "வயலில் பயிர் கழிவுகளை எரிக்க வேண்டாம்.",
            "expert": "விதைப்புக்கு முன் அருகிலுள்ள மண் பரிசோதனை நிலையம் அல்லது KVK-ஐ அணுகவும்.",
        },
        "weather_precautions": {
            "problem": "கனமழை, பலத்த காற்று அல்லது கடும் வெயிலில் இருந்து பயிரைப் பாதுகாத்தல்.",
            "causes": "மழையால் நீர் தேங்குதல், காற்றினால் பயிர் சாய்தல் அல்லது வெயிலால் பூக்கள் உதிர்தல்.",
            "steps": "1. மழை முன்னறிவிப்பு இருக்கும்போது வடிகால் வாய்க்கால்களைத் திறந்து விடவும்.\n2. மழை அல்லது பலத்த காற்று நேரத்தில் பூச்சிக்கொல்லி/உரம் தெளிக்க வேண்டாம்.\n3. வாழை, கரும்பு, தக்காளி பயிர்களுக்கு முட்டுக் கொடுத்துத் தாங்கவும்.",
            "precautions": "மழைக்கு சற்று முன்பு உரம் அல்லது மருந்து தெளிப்பதைத் தவிர்க்கவும்.",
            "expert": "பயிர் சேதம் ஏற்பட்டால் 72 மணி நேரத்திற்குள் PMFBY காப்பீட்டு உதவி எண் 14447 அல்லது 1800-180-1551-ஐ அழைக்கவும்.",
        },
        "crop_selection_season": {
            "problem": "பருவத்திற்கு ஏற்ற பயிர் தேர்வு, உயர் விளைச்சல் ரகங்கள் மற்றும் விதை நேர்த்தி.",
            "causes": "பருவம் (காரீப் / ரபி / கோடை), மண் வகை மற்றும் நீர் ஆதாரத்திற்கு ஏற்ப பயிர் சாகுபடி.",
            "steps": "1. காரீப் / குறுவை & சம்பா: நெல், பருத்தி, மிளகாய், மக்காச்சோளம், துவரை, நிலக்கடலை.\n2. ரபி / நவரை: உளுந்து, பாசிப்பயறு, கடலை, தக்காளி, வெங்காயம், நிலக்கடலை.\n3. விதைப்புக்கு முன் டிரைக்கோடெர்மா மற்றும் ரைசோபியம் கொண்டு விதை நேர்த்தி செய்யவும்.",
            "precautions": "சான்றளிக்கப்பட்ட விதைகளை மட்டுமே பயன்படுத்தவும் மற்றும் பயிர் சுழற்சியைப் பின்பற்றவும்.",
            "expert": "உங்கள் மாவட்டத்திற்கு ஏற்ற விதை ரகங்களுக்கு உள்ளூர் KVK-ஐ அணுகவும்.",
        },
        "market_schemes": {
            "problem": "சந்தை (மண்டி) விலை ஒப்பீடு மற்றும் அரசு வேளாண் திட்டங்கள் / மானியங்கள்.",
            "causes": "சந்தை விலை நிலவரம் மற்றும் அரசு நலத்திட்டங்களை அறிந்து கொள்ளுதல்.",
            "steps": "1. விளைபொருளை விற்பனைக்குக் கொண்டு செல்லும் முன் அருகிலுள்ள மண்டி மற்றும் e-NAM விலைகளை ஒப்பிடவும்.\n2. PM-KISAN (ஆண்டுக்கு ₹6,000), PMFBY பயிர் காப்பீடு, KCC கடன் மற்றும் சொட்டு நீர்ப்பாசன மானியத்திற்கு விண்ணப்பிக்கவும்.",
            "precautions": "அதிகாரப்பூர்வ .gov.in இணையதளங்கள் அல்லது வேளாண் அலுவலகம் மூலமாக மட்டுமே விண்ணப்பிக்கவும்.",
            "expert": "e-NAM உதவி எண் 1800-270-0224 அல்லது கிசான் கால் சென்டர் 1800-180-1551-ஐ தொடர்பு கொள்ளவும்.",
        },
        "sustainable_farming": {
            "problem": "குறைந்த செலவில் இயற்கை மற்றும் நிலைத்த வேளாண்மை, மூடாக்கு மற்றும் களை கட்டுப்பாடு.",
            "causes": "அதிகரிக்கும் சாகுபடி செலவு மற்றும் களைப் பிரச்சினை.",
            "steps": "1. மூடாக்கு (Mulching) அமைப்பதன் மூலம் 80% களைகளைக் கட்டுப்படுத்தி 35% நீரைச் சேமிக்கலாம்.\n2. உயிர் உரங்கள், மண்புழு உரம் மற்றும் வேப்ப எண்ணெய் கரைசலைப் பயன்படுத்தவும்.",
            "precautions": "உயிர் உரங்களை இரசாயன மருந்துகளுடன் கலக்க வேண்டாம்.",
            "expert": "இயற்கை விவசாயப் பயிற்சிகளுக்கு உங்கள் மாவட்ட KVK அல்லது FPO-உடன் இணையுங்கள்.",
        },
        "general": {
            "problem": "ஒருங்கிணைந்த பயிர் மற்றும் பண்ணை மேலாண்மை வழிகாட்டுதல் (Integrated Crop Advisory).",
            "causes": "சிறந்த மகசூலுக்கு மண்ணின் ஈரப்பதம், சரிவிகித உரம், பூச்சி கண்காணிப்பு மற்றும் வானிலை முன்னெச்சரிக்கை அவசியம்.",
            "steps": "1. காலை வேளையில் வயலில் 10 செடிகளின் இலைகள் மற்றும் தண்டுப் பகுதியை ஆய்வு செய்யவும்.\n2. 5–8 செ.மீ ஆழத்தில் ஈரப்பதம் பார்த்து நீர் பாய்ச்சவும்.\n3. தொழு உரம் மற்றும் பிரித்து இடப்படும் உரங்களைப் பயன்படுத்தவும்.\n4. மஞ்சள்/நீல ஒட்டும் அட்டைகள் மற்றும் வேப்பெண்ணெய் கரைசலைத் தடுப்பு முறையாகப் பயன்படுத்தவும்.",
            "precautions": "காரணம் தெரியாமல் இரசாயன மருந்துகளைக் கலந்து தெளிக்க வேண்டாம்.",
            "expert": "நெல், தக்காளி, மிளகாய், பருத்தி, நீர்ப்பாசனம் அல்லது சந்தை விலை குறித்து எதை வேண்டுமானாலும் கேளுங்கள், அல்லது 1800-180-1551 என்ற எண்ணை அழைக்கவும்.",
        },
    },
    "kn-IN": {
        "crop_health": {
            "problem": "ಬೆಳೆಯ ಎಲೆಗಳು ಹಳದಿಯಾಗುವುದು, ಮುడుಚಿಕೊಳ್ಳುವುದು, ಹೂವು ಉದುರುವುದು ಅಥವಾ ಬೆಳವಣಿಗೆ ಕುಂಠಿತವಾಗುವುದು.",
            "causes": "ಪೋಷಕಾಂಶಗಳ ಕೊರತೆ (ಸಾರಜನಕ, ಸತು/ಜಿಂಕ್, ಕಬ್ಬಿಣ), ಹೆಚ್ಚುವರಿ ನೀರು ಅಥವಾ ಎಲೆಗಳ ಕೆಳಗೆ ರಸ ಹೀರುವ ಕೀಟಗಳು (ಬಿಳಿ ನೊಣ, ಥ್ರಿಪ್ಸ್).",
            "steps": "1. ಹಳೆಯ ಕೆಳಗಿನ ಎಲೆಗಳೇ ಅಥವಾ ಹೊಸ ಮೇಲಿನ ಎಲೆಗಳೇ ಹಳದಿಯಾಗುತ್ತಿವೆ ಎಂದು ಗಮನಿಸಿ.\n2. ಬೆಳಿಗ್ಗೆ 5–10 ಎಲೆಗಳ ಕೆಳಭಾಗವನ್ನು ತಿರುಗಿಸಿ ಕೀಟಗಳಿಗಾಗಿ ಪರಿಶೀಲಿಸಿ.\n3. 5–8 ಸೆಂ.ಮೀ ಆಳದಲ್ಲಿ ಮಣ್ಣಿನ ತೇವಾಂಶ ನೋಡಿ ನೀರು ಕೊಡಿ.\n4. ಲಘು ಪೋಷಕಾಂಶಗಳ ಕೊರತೆಯಿದ್ದರೆ ಜಿಂಕ್ ಸಲ್ಫೇಟ್ ಅಥವಾ ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶಗಳ ಮಿಶ್ರಣ ಸಿಂಪಡಿಸಿ.",
            "precautions": "ನಿಖರ ಕಾರಣ ತಿಳಿಯದೆ ರಾಸಾಯನಿಕ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ.",
            "expert": "ಹಳದಿ ಬಣ್ಣ ವೇಗವಾಗಿ ಹರಡುತ್ತಿದ್ದರೆ ಎಲೆಯ ಮಾದರಿಯೊಂದಿಗೆ ಸ್ಥಳೀಯ ಕೃಷಿ ಅಧಿಕಾರಿ ಅಥವಾ KVK (1800-180-1551) ಅನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        },
        "pest_management": {
            "problem": "ಎಲೆಗಳು, ಕಾಂಡ ಮತ್ತು ಕಾಯಿಗಳ ಮೇಲೆ ಕೀಟ ಮತ್ತು ಹುಳುಗಳ ದಾಳಿ.",
            "causes": "ಕಾಂಡ ಕೊರೆಯುವ ಹುಳು, ಕಾಯಿ ಕೊರಕ ಅಥವಾ ರಸ ಹೀರುವ ಕೀಟಗಳ (ಬಿಳಿ ನೊಣ, ಥ್ರಿಪ್ಸ್, ಜಿಗಿಹುಳು) ಹೆಚ್ಚಳ.",
            "steps": "1. ಬೆಳಿಗ್ಗೆ ಎಲೆಗಳ ಮೇಲ್ಭಾಗ ಮತ್ತು ಕೆಳಭಾಗವನ್ನು ಪರಿಶೀಲಿಸಿ.\n2. ಎಕರೆಗೆ 10 ಹಳದಿ/ನೀಲಿ ಅಂಟು ಪಟ್ಟಿಗಳನ್ನು ಮತ್ತು 4–5 ಮೋಹಕ ಬಲೆಗಳನ್ನು (Pheromone traps) ಅಳವಡಿಸಿ.\n3. ಶೇ. 5ರ ಬೇವಿನ ಬೀಜದ ಕಷಾಯ (NSKE) ಅಥವಾ ಬೇವಿನ ಎಣ್ಣೆ (2 ಮಿ.ಲೀ/ಲೀಟರ್) ಸಿಂಪಡಿಸಿ.",
            "precautions": "ಉಪಯುಕ್ತ ಕೀಟಗಳಿಗೆ ಹಾನಿ ಮಾಡುವ ತೀವ್ರ ರಾಸಾಯನಿಕಗಳನ್ನು ತಪ್ಪಿಸಿ.",
            "expert": "ಸಮಗ್ರ ಕೀಟ ನಿರ್ವಹಣೆ (IPM) ಸಲಹೆಗಾಗಿ ಸ್ಥಳೀಯ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        },
        "disease_prevention": {
            "problem": "ಎಲೆ ಚುಕ್ಕೆ ರೋಗ, ಅಂಗಮಾರಿ ರೋಗ, ಬೂದಿ ರೋಗ ಅಥವಾ ಬೇರು/ಕಾಯಿ ಕೊಳೆ ರೋಗದ ಲಕ್ಷಣಗಳು.",
            "causes": "ಹೆಚ್ಚಿನ ತೇವಾಂಶ, ಎಲೆಗಳ ಮೇಲೆ ನೀರು ನಿಲ್ಲುವುದು ಅಥವಾ ಶಿಲೀಂಧ್ರ/ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು.",
            "steps": "1. ತೀವ್ರವಾಗಿ ಬಾಧಿತವಾದ ಎಲೆಗಳನ್ನು ತೆಗೆದು ಹೊಲದಿಂದ ಹೊರಗೆ ನಾಶಪಡಿಸಿ.\n2. ಬೇರುಗಳ ಬಳಿ ಮಾತ್ರ ನೀರು ಹಾಕಿ ಮತ್ತು ಬಸಿಗಾಲುವೆಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.\n3. ಟ್ರೈಕೋಡರ್ಮಾ ವಿರಿಡಿ (Trichoderma viride) ಜೈವಿಕ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರದೊಂದಿಗೆ ಬಳಸಿ.",
            "precautions": "ರೋಗಗ್ರಸ್ತ ಸಸ್ಯದ ಭಾಗಗಳನ್ನು ಕಾಂಪೋಸ್ಟ್ ಗುಂಡಿಗೆ ಹಾಕಬೇಡಿ.",
            "expert": "ಯಾವುದೇ ಶಿಲೀಂಧ್ರನಾಶಕ ಬಳಸುವ ಮೊದಲು ಸ್ಥಳೀಯ KVK ತಜ್ಞರಿಗೆ ತೋರಿಸಿ ರೋಗವನ್ನು ದೃಢಪಡಿಸಿಕೊಳ್ಳಿ.",
        },
        "irrigation": {
            "problem": "ಬೆಳೆಗೆ ಸಮರ್ಪಕ ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿ ಮತ್ತು ನೀರು ನಿಲ್ಲುವುದನ್ನು / ಒಣಗುವುದನ್ನು ತಡೆಯುವುದು.",
            "causes": "ಅನಿಯಮಿತ ನೀರಾವರಿ ಅಥವಾ ಹೊಲದಲ್ಲಿ ಹೆಚ್ಚುವರಿ ನೀರು ಸರಿಯಾಗಿ ಹರಿದು ಹೋಗದಿರುವುದು.",
            "steps": "1. ನೀರು ಹಾಕುವ ಮೊದಲು 5–8 ಸೆಂ.ಮೀ ಆಳದಲ್ಲಿ ಮಣ್ಣಿನ ತೇವಾಂಶ ಪರಿಶೀಲಿಸಿ.\n2. ಬೆಳಿಗ್ಗೆ (6:00–8:30) ಅಥವಾ ಸಂಜೆ ವೇಳೆ ನೀರು ಹಾಯಿಸುವುದರಿಂದ ಶೇ. 30ರಷ್ಟು ನೀರು ಉಳಿತಾಯವಾಗುತ್ತದೆ.\n3. ಭತ್ತದಲ್ಲಿ ಕವಲು ಒಡೆಯುವ ಹಂತದಲ್ಲಿ 2–3 ಸೆಂ.ಮೀ ನೀರು ಮಾತ್ರ ಇರಲಿ.\n4. ಟೊಮೆಟೊ, ಮೆಣಸಿನಕಾಯಿ ಮತ್ತು ತರಕಾರಿಗಳಿಗೆ ಹನಿ ನೀರಾವರಿ ಹಾಗೂ ಮಲ್ಚಿಂಗ್ ಬಳಸಿ.",
            "precautions": "ತರಕಾರಿ, ಮೆಣಸಿನಕಾಯಿ ಮತ್ತು ದ್ವಿದಳ ಧಾನ್ಯಗಳ ಬೇರುಗಳ ಸುತ್ತ ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.",
            "expert": "ಹನಿ ನೀರಾವರಿ ಸಬ್ಸಿಡಿಗಾಗಿ (PMKSY) ನಿಮ್ಮ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರವನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        },
        "fertilizer_guidance": {
            "problem": "ಬೆಳೆಗೆ ಸಮತೋಲಿತ ಪೋಷಕಾಂಶ ಮತ್ತು ಗೊಬ್ಬರದ ಸರಿಯಾದ ನಿರ್ವಹಣೆ (NPK + ಲಘು ಪೋಷಕಾಂಶಗಳು).",
            "causes": "ಮಣ್ಣು ಪರೀಕ್ಷೆ ಇಲ್ಲದೆ ಯೂರಿಯಾವನ್ನು ಮಾತ್ರ ಹೆಚ್ಚು ಬಳಸುವುದು.",
            "steps": "1. ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಕಾರ್ಡ್ (Soil Health Card) ವರದಿಯಂತೆ ಗೊಬ್ಬರ ನೀಡಿ.\n2. ಬಿತ್ತನೆಗೆ ಮುನ್ನ ಎಕರೆಗೆ 4–5 ಟನ್ ಕೊಳೆತ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಅಥವಾ ಎರೆಹುಳು ಗೊಬ್ಬರ ಸೇರಿಸಿ.\n3. ಸಾರಜನಕವನ್ನು (ಬೇವಿನ ಲೇಪಿತ ಯೂರಿಯಾ) 3 ಕಂತುಗಳಲ್ಲಿ ವಿಭಜಿಸಿ ನೀಡಿ.",
            "precautions": "ಮಣ್ಣಿನಲ್ಲಿ ತೇವಾಂಶ ಇಲ್ಲದಿರುವಾಗ ಗೊಬ್ಬರ ಹಾಕಬೇಡಿ.",
            "expert": "ನಿಮ್ಮ ಬೆಳೆ ಮತ್ತು ಮಣ್ಣಿಗೆ ಸೂಕ್ತವಾದ ಗೊಬ್ಬರದ ಪ್ರಮಾಣ ತಿಳಿಯಲು ಸ್ಥಳೀಯ KVK ಅನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        },
        "soil_health": {
            "problem": "ಮಣ್ಣಿನ ಫಲವತ್ತತೆ, ಸಾವಯವ ಇಂಗಾಲ ಮತ್ತು pH ಸಮತೋಲನ ಸುಧಾರಣೆ.",
            "causes": "ನಿರಂತರವಾಗಿ ಒಂದೇ ಬೆಳೆ ಬೆಳೆಯುವುದು ಮತ್ತು ಸಾವಯವ ಗೊಬ್ಬರದ ಕೊರತೆ.",
            "steps": "1. ಮಣ್ಣು ಪರೀಕ್ಷೆ (Soil Health Card) ಮಾಡಿಸಿ.\n2. ಸೆಣಬು ಅಥವಾ ಡೈಂಚಾ ಹಸಿರೆಲೆ ಗೊಬ್ಬರ ಬೆಳೆದು ಮಣ್ಣಿಗೆ ಸೇರಿಸಿ.\n3. ದ್ವಿದಳ ಧಾನ್ಯಗಳೊಂದಿಗೆ (ತೊಗರಿ, ಉದ್ದು, ಹೆಸರು, ಕಡಲೆ) ಬೆಳೆ ಪರಿವರ್ತನೆ ಮಾಡಿ.",
            "precautions": "ಹೊಲದಲ್ಲಿ ಬೆಳೆ ಅವಶೇಷಗಳನ್ನು ಸುಡಬೇಡಿ.",
            "expert": "ಬಿತ್ತನೆಗೂ ಮುನ್ನ ಮಣ್ಣಿನ ಮಾದರಿಯನ್ನು ಹತ್ತಿರದ ಮಣ್ಣು ಪರೀಕ್ಷಾ ಕೇಂದ್ರ ಅಥವಾ KVK ಗೆ ಕೊಂಡೊಯ್ಯಿರಿ.",
        },
        "weather_precautions": {
            "problem": "ಭಾರೀ ಮಳೆ, ಗಾಳಿ ಅಥವಾ ತೀವ್ರ ಬಿಸಿಲಿನಿಂದ ಬೆಳೆಯ ರಕ್ಷಣೆ.",
            "causes": "ಮಳೆಯಿಂದ ನೀರು ನಿಲ್ಲುವುದು, ಗಾಳಿಗೆ ಬೆಳೆ ಬೀಳುವುದು ಅಥವಾ ಬಿಸಿಲಿನಿಂದ ಹೂವು ಉದುರುವುದು.",
            "steps": "1. ಭಾರೀ ಮಳೆ ಮುನ್ಸೂಚನೆ ಇದ್ದಾಗ ಹೆಚ್ಚುವರಿ ನೀರು ಹೊರಹೋಗಲು ಬಸಿಗಾಲುವೆಗಳನ್ನು ತೆರೆಯಿರಿ.\n2. ಮಳೆ ಬರುವ ಮುನ್ನ ಅಥವಾ ಜೋರು ಗಾಳಿ ಬೀಸುವಾಗ ಯಾವುದೇ ಸಿಂಪಡಣೆ ಮಾಡಬೇಡಿ.\n3. ಬಾಳೆ, ಕಬ್ಬು, ಟೊಮೆಟೊ ಬೆಳೆಗಳಿಗೆ ಆಧಾರ ನೀಡಿ.",
            "precautions": "ಮಳೆಗೆ ಮುನ್ನ ಗೊಬ್ಬರ ಅಥವಾ ಔಷಧ ಸಿಂಪಡಿಸಬೇಡಿ.",
            "expert": "ಬೆಳೆ ಹಾನಿಯಾದರೆ 72 ಗಂಟೆಗಳೊಳಗೆ PMFBY ಸಹಾಯವಾಣಿ 14447 ಅಥವಾ 1800-180-1551 ಗೆ ಕರೆ ಮಾಡಿ.",
        },
        "crop_selection_season": {
            "problem": "ಹಂಗಾಮಿಗೆ ಸೂಕ್ತವಾದ ಬೆಳೆ ಆಯ್ಕೆ, ಅಧಿಕ ಇಳುವರಿ ತಳಿಗಳು ಮತ್ತು ಬೀಜೋಪಚಾರ.",
            "causes": "ಪ್ರಸ್ತುತ ಹಂಗಾಮು (ಮುಂಗಾರು / ಹಿಂಗಾರು / ಬೇಸಿಗೆ), ಮಣ್ಣಿನ ಗುಣ ಮತ್ತು ನೀರಿನ ಲಭ್ಯತೆ.",
            "steps": "1. ಮುಂಗಾರು (Kharif): ಭತ್ತ, ಹತ್ತಿ, ಮೆಣಸಿನಕಾಯಿ, ತೊಗರಿ, ಮೆಕ್ಕೆಜೋಳ, ಶೇಂಗಾ.\n2. ಹಿಂಗಾರು (Rabi): ಕಡಲೆ, ಉದ್ದು, ಹೆಸರು, ಜೋಳ, ಟೊಮೆಟೊ, ಈರುಳ್ಳಿ, ಶೇಂಗಾ.\n3. ಬಿತ್ತನೆಗೆ ಮುನ್ನ ಟ್ರೈಕೋಡರ್ಮಾ ಮತ್ತು ರೈಜೋಬಿಯಂನಿಂದ ಬೀಜೋಪಚಾರ ಮಾಡಿ.",
            "precautions": "ಪ್ರಮಾಣೀಕೃತ ಬೀಜಗಳನ್ನೇ ಬಳಸಿ ಮತ್ತು ಬೆಳೆ ಪರಿವರ್ತನೆ ಅನುಸರಿಸಿ.",
            "expert": "ನಿಮ್ಮ ಜಿಲ್ಲೆಗೆ ಶಿಫಾರಸು ಮಾಡಿದ ತಳಿಗಳಿಗಾಗಿ ಸ್ಥಳೀಯ KVK ಅಥವಾ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರವನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        },
        "market_schemes": {
            "problem": "ಮಾರುಕಟ್ಟೆ (ಮಂಡಿ) ಬೆಲೆ ಹೋಲಿಕೆ ಮತ್ತು ಸರ್ಕಾರಿ ಕೃಷಿ ಯೋಜನೆಗಳು / ಸಬ್ಸಿಡಿಗಳು.",
            "causes": "ಮಾರುಕಟ್ಟೆ ಧಾರಣೆ ತಿಳಿಯುವುದು ಮತ್ತು ಸರ್ಕಾರಿ ಸೌಲಭ್ಯಗಳ ಸದುಪಯೋಗ.",
            "steps": "1. ಉತ್ಪನ್ನ ಮಾರಾಟಕ್ಕೆ ಮುನ್ನ ಹತ್ತಿರದ ಮಂಡಿ ಮತ್ತು e-NAM ಬೆಲೆಗಳನ್ನು ಹೋಲಿಸಿ.\n2. PM-KISAN (ವರ್ಷಕ್ಕೆ ₹6,000), PMFBY ಬೆಳೆ ವಿಮೆ, KCC ಸಾಲ ಮತ್ತು ಹನಿ ನೀರಾವರಿ ಸಬ್ಸಿಡಿಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
            "precautions": "ಅಧಿಕೃತ .gov.in ಪೋರ್ಟಲ್ ಅಥವಾ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರದ ಮೂಲಕವೇ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
            "expert": "e-NAM ಸಹಾಯವಾಣಿ 1800-270-0224 ಅಥವಾ ಕಿಸಾನ್ ಕಾಲ್ ಸೆಂಟರ್ 1800-180-1551 ಗೆ ಕರೆ ಮಾಡಿ.",
        },
        "sustainable_farming": {
            "problem": "ಕಡಿಮೆ ವೆಚ್ಚದ ಸುಸ್ಥಿರ ಮತ್ತು ಸಾವಯವ ಕೃಷಿ, ಮಲ್ಚಿಂಗ್ ಹಾಗೂ ಕಳೆ ನಿಯಂತ್ರಣ.",
            "causes": "ಹೆಚ್ಚುತ್ತಿರುವ ಕೃಷಿ ವೆಚ್ಚ ಮತ್ತು ಕಳೆಗಳ ಸಮಸ್ಯೆ.",
            "steps": "1. ಮಲ್ಚಿಂಗ್ (ಹೊದಿಕೆ) ಅಳವಡಿಸುವುದರಿಂದ ಶೇ. 80ರಷ್ಟು ಕಳೆ ತಡೆದು ಶೇ. 35ರಷ್ಟು ನೀರು ಉಳಿಸಬಹುದು.\n2. ಜೈವಿಕ ಗೊಬ್ಬರಗಳು, ಎರೆಹುಳು ಗೊಬ್ಬರ ಮತ್ತು ಬೇವಿನ ಎಣ್ಣೆ ಬಳಸಿ.",
            "precautions": "ಜೈವಿಕ ಗೊಬ್ಬರಗಳನ್ನು ರಾಸಾಯನಿಕ ಔಷಧಗಳೊಂದಿಗೆ ಬೆರೆಸಬೇಡಿ.",
            "expert": "ಸಾವಯವ ಕೃಷಿ ತರಬೇತಿಗಾಗಿ ಸ್ಥಳೀಯ KVK ಅಥವಾ FPO ಸಂಪರ್ಕಿಸಿ.",
        },
        "general": {
            "problem": "ಸಮಗ್ರ ಬೆಳೆ ಮತ್ತು ಕೃಷಿ ನಿರ್ವಹಣಾ ಮಾರ್ಗದರ್ಶನ (Integrated Crop Advisory).",
            "causes": "ಉತ್ತಮ ಇಳುವರಿಗಾಗಿ ಮಣ್ಣಿನ ತೇವಾಂಶ, ಸಮತೋಲಿತ ಪೋಷಕಾಂಶ, ಕೀಟ ನಿಗಾ ಮತ್ತು ಹವಾಮಾನ ಆಧಾರಿತ ನಿರ್ಧಾರಗಳು ಮುಖ್ಯ.",
            "steps": "1. ಬೆಳಿಗ್ಗೆ ಹೊಲದಲ್ಲಿ 10 ಗಿಡಗಳ ಎಲೆ ಮತ್ತು ಕಾಂಡವನ್ನು ಪರಿಶೀಲಿಸಿ.\n2. 5–8 ಸೆಂ.ಮೀ ಆಳದಲ್ಲಿ ತೇವಾಂಶ ನೋಡಿ ನೀರು ಹಾಯಿಸಿ.\n3. ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರದೊಂದಿಗೆ ಕಂತುಗಳಲ್ಲಿ ಪೋಷಕಾಂಶ ನೀಡಿ.\n4. ಹಳದಿ/ನೀಲಿ ಅಂಟು ಪಟ್ಟಿಗಳು ಮತ್ತು ಬೇವಿನ ಎಣ್ಣೆಯನ್ನು ಮುನ್ನೆಚ್ಚರಿಕೆಯಾಗಿ ಬಳಸಿ.",
            "precautions": "ಕಾರಣ ತಿಳಿಯದೆ ರಾಸಾಯನಿಕ ಔಷಧಗಳನ್ನು ಬೆರೆಸಿ ಸಿಂಪಡಿಸಬೇಡಿ.",
            "expert": "ಭತ್ತ, ಟೊಮೆಟೊ, ಮೆಣಸಿನಕಾಯಿ, ಹತ್ತಿ, ನೀರಾವರಿ ಅಥವಾ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಬಗ್ಗೆ ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಿ, ಅಥವಾ 1800-180-1551 ಗೆ ಕರೆ ಮಾಡಿ.",
        },
    },
    "ml-IN": {
        "crop_health": {
            "problem": "വിളകളുടെ ഇലകൾ മഞ്ഞനിറമാകുക, ചുരുളുക, പൂക്കൾ കൊഴിയുക അല്ലെങ്കിൽ വളർച്ച കുറയുക.",
            "causes": "പോഷകക്കുറവ് (നൈട്രജൻ, സിങ്ക്, ഇരുമ്പ്), അമിതമായ വെള്ളം അല്ലെങ്കിൽ ഇലകളുടെ അടിയിൽ നീരൂറ്റിക്കുടിക്കുന്ന കീടങ്ങൾ (വെള്ളീച്ച, ഇലപ്പേൻ).",
            "steps": "1. പഴയ ഇലകളാണോ പുതിയ ഇലകളാണോ മഞ്ഞനിറമാകുന്നതെന്ന് പരിശോധിക്കുക.\n2. രാവിലെ 5–10 ഇലകളുടെ അടിവശം പരിശോധിച്ച് കീടങ്ങളുണ്ടോ എന്ന് നോക്കുക.\n3. 5–8 സെ.മീ ആഴത്തിൽ മണ്ണിലെ ഈർപ്പം പരിശോധിച്ച ശേഷം മാത്രം നനയ്ക്കുക.\n4. സൂക്ഷ്മ മൂലകങ്ങളുടെ കുറവുണ്ടെങ്കിൽ സിങ്ക് സൾഫേറ്റ് അല്ലെങ്കിൽ മൈക്രോന്യൂട്രിയന്റ് മിശ്രിതം തളിക്കുക.",
            "precautions": "കാരണം വ്യക്തമാകാതെ രാസകീടനാശിനികൾ പ്രയോഗിക്കരുത്.",
            "expert": "മഞ്ഞനിറം വേഗത്തിൽ പടരുന്നുണ്ടെങ്കിൽ കൃഷിഭവനുമായോ KVK (1800-180-1551)-യുമായോ ബന്ധപ്പെടുക.",
        },
        "pest_management": {
            "problem": "ഇലകളിലും തണ്ടുകളിലും കായ്കളിലും കീടങ്ങളുടെയും പുഴുക്കളുടെയും ആക്രമണം.",
            "causes": "തണ്ടുതുരപ്പൻ, കായ്തുരപ്പൻ അല്ലെങ്കിൽ നീരൂറ്റിക്കുടിക്കുന്ന കീടങ്ങളുടെ (വെള്ളീച്ച, ഇലപ്പേൻ, മുഞ്ഞ) വർദ്ധനവ്.",
            "steps": "1. രാവിലെ ഇലകളുടെ മുകൾഭാഗവും അടിഭാഗവും പരിശോധിക്കുക.\n2. ഏക്കറിന് 10 മഞ്ഞ/നീല ഒട്ടിപ്പിടിക്കുന്ന കെണികളും ഫെറമോൺ കെണികളും സ്ഥാപിക്കുക.\n3. വേപ്പിൻകുരു സത്ത് (5% NSKE) അല്ലെങ്കിൽ വേപ്പെണ്ണ (2 മില്ലി/ലിറ്റർ) തളിക്കുക.",
            "precautions": "മിത്രകീടങ്ങളെ നശിപ്പിക്കുന്ന വീര്യം കൂടിയ രാസകീടനാശിനികൾ ഒഴിവാക്കുക.",
            "expert": "സംയോജിത കീട നിയന്ത്രണ (IPM) മാർഗ്ഗങ്ങൾക്കായി കൃഷി ഓഫീസറുടെ ഉപദേശം തേടുക.",
        },
        "disease_prevention": {
            "problem": "ഇലപ്പുള്ളികൾ, കുമിൾ ബാധ, വാട്ടരോഗം അല്ലെങ്കിൽ വേരുചീയൽ രോഗലക്ഷണങ്ങൾ.",
            "causes": "അമിതമായ ഈർപ്പം, ഇലകളിൽ വെള്ളം തങ്ങിനിൽക്കുന്നത് അല്ലെങ്കിൽ കുമിൾ/ബാക്ടീരിയൽ അണുബാധ.",
            "steps": "1. രോഗം ബാധിച്ച ഇലകൾ മുറിച്ചുമാറ്റി കൃഷിയിടത്തിന് പുറത്ത് നശിപ്പിക്കുക.\n2. ചെടികളുടെ ചുവട്ടിൽ മാത്രം നനയ്ക്കുകയും നീർവാർച്ച ഉറപ്പാക്കുകയും ചെയ്യുക.\n3. ട്രൈക്കോഡെർമ സമ്പുഷ്ടീകരിച്ച ചാണകം ചുവട്ടിൽ ചേർക്കുക.",
            "precautions": "രോഗം ബാധിച്ച സസ്യഭാഗങ്ങൾ കമ്പോസ്റ്റ് കുഴിയിൽ ഇടരുത്.",
            "expert": "കുമിൾനാശിനി ഉപയോഗിക്കുന്നതിന് മുമ്പ് കൃഷിഭവനിലോ KVK-യിലോ കാണിച്ച് രോഗം സ്ഥിരീകരിക്കുക.",
        },
        "irrigation": {
            "problem": "ശരിയായ ജലസേചന ക്രമീകരണവും വെള്ളക്കെട്ട് / വരൾച്ച ഒഴിവാക്കലും.",
            "causes": "ക്രമരഹിതമായ നനയ്ക്കൽ അല്ലെങ്കിൽ കൃഷിയിടത്തിലെ നീർവാർച്ചക്കുറവ്.",
            "steps": "1. നനയ്ക്കുന്നതിന് മുമ്പ് 5–8 സെ.മീ ആഴത്തിൽ മണ്ണിലെ ഈർപ്പം പരിശോധിക്കുക.\n2. രാവിലെ (6:00–8:30) അല്ലെങ്കിൽ വൈകുന്നേരം നനയ്ക്കുന്നത് വഴി 30% വെള്ളം ലാഭിക്കാം.\n3. പച്ചക്കറികൾക്ക് തുള്ളിനനയും (Drip irrigation) പുതയിടലും സ്വീകരിക്കുക.",
            "precautions": "വേരുകൾക്ക് ചുറ്റും വെള്ളം കെട്ടിനിൽക്കാൻ അനുവദിക്കരുത്; ഇത് വേരുചീയലിന് കാരണമാകും.",
            "expert": "തുള്ളിനന സബ്സിഡിക്കായി (PMKSY) കൃഷി ഓഫീസറെ സമീപിക്കുക.",
        },
        "fertilizer_guidance": {
            "problem": "വിളകൾക്ക് സന്തുലിതമായ പോഷകങ്ങളും ശരിയായ വളപ്രയോഗവും (NPK + സൂക്ഷ്മ മൂലകങ്ങൾ).",
            "causes": "മണ്ണ് പരിശോധന കൂടാതെ യൂറിയ മാത്രം അമിതമായി ഉപയോഗിക്കുന്നത്.",
            "steps": "1. മണ്ണ് പരിശോധനാ റിപ്പോർട്ട് (Soil Health Card) പ്രകാരം വളം നൽകുക.\n2. നടീലിന് മുമ്പ് ചാണകമോ മണ്ണിര കമ്പോസ്റ്റോ ചേർക്കുക.\n3. നൈട്രജൻ വളങ്ങൾ 3 തവണകളായി വിഭജിച്ച് നൽകുക.",
            "precautions": "മണ്ണിൽ ഈർപ്പമില്ലാത്തപ്പോൾ രാസവളങ്ങൾ ഇടരുത്.",
            "expert": "നിങ്ങളുടെ വിളയ്ക്കും മണ്ണിനും അനുയോജ്യമായ വളപ്രയോഗത്തിന് കൃഷിഭവനുമായി ബന്ധപ്പെടുക.",
        },
        "soil_health": {
            "problem": "മണ്ണിന്റെ ഫലഭൂയിഷ്ഠതയും pH സന്തുലിതാവസ്ഥയും മെച്ചപ്പെടുത്തൽ.",
            "causes": "തുടർച്ചയായി ഒരേ വിള കൃഷി ചെയ്യുന്നതും ജൈവവളങ്ങളുടെ കുറവും.",
            "steps": "1. മണ്ണ് പരിശോധന (Soil Health Card) നടത്തുക.\n2. പയറുവർഗ്ഗങ്ങളുമായി വിളപരിവർത്തനം നടത്തുകയും പച്ചിലവളങ്ങൾ ചേർക്കുകയും ചെയ്യുക.",
            "precautions": "കൃഷിയിടത്തിൽ വിള അവശിഷ്ടങ്ങൾ കത്തിക്കരുത്.",
            "expert": "കൃഷി തുടങ്ങുന്നതിന് മുമ്പ് മണ്ണ് സാമ്പിൾ അടുത്തുള്ള മണ്ണ് പരിശോധനാ കേന്ദ്രത്തിൽ എത്തിക്കുക.",
        },
        "weather_precautions": {
            "problem": "കനത്ത മഴ, കാറ്റ് അല്ലെങ്കിൽ കടുത്ത ചൂടിൽ നിന്ന് വിളകളെ സംരക്ഷിക്കൽ.",
            "causes": "മഴമൂലമുള്ള വെള്ളക്കെട്ട്, കാറ്റിൽ ചെടികൾ ഒടിയുന്നത് അല്ലെങ്കിൽ ചൂടിൽ പൂക്കൾ കൊഴിയുന്നത്.",
            "steps": "1. കനത്ത മഴയ്ക്ക് മുമ്പ് വെള്ളം ഒഴുകിപ്പോകാൻ ചാലുകൾ വൃത്തിയാക്കുക.\n2. മഴയ്ക്ക് തൊട്ടുമുമ്പോ ശക്തമായ കാറ്റുള്ളപ്പോഴോ മരുന്നുകൾ തളിക്കരുത്.\n3. വാഴ, തക്കാളി തുടങ്ങിയ വിളകൾക്ക് താങ്ങ് നൽകുക.",
            "precautions": "മഴയ്ക്ക് തൊട്ടുമുമ്പ് വളമോ കീടനാശിനിയോ പ്രയോഗിക്കരുത്.",
            "expert": "കൃഷിനാശം ഉണ്ടായാൽ 72 മണിക്കൂറിനുള്ളിൽ PMFBY ഹെൽപ്പ്‌ലൈൻ 14447 അല്ലെങ്കിൽ 1800-180-1551-ൽ അറിയിക്കുക.",
        },
        "crop_selection_season": {
            "problem": "സീസണിന് അനുയോജ്യമായ വിള തിരഞ്ഞെടുക്കൽ, മികച്ചയിനം വിത്തുകൾ, വിത്ത് പരിചരണം.",
            "causes": "നിലവിലെ സീസൺ (ഖാരിഫ് / റാബി / വേനൽ), മണ്ണിന്റെ സ്വഭാവം, ജലലഭ്യത.",
            "steps": "1. സീസണിനും മണ്ണിനും അനുയോജ്യമായ സർട്ടിഫൈഡ് വിത്തുകൾ തിരഞ്ഞെടുക്കുക.\n2. നടീലിന് മുമ്പ് ട്രൈക്കോഡെർമ / റൈസോബിയം ഉപയോഗിച്ച് വിത്ത് പരിചരണം നടത്തുക.",
            "precautions": "എല്ലാ സീസണിലും ഒരേ വിള തന്നെ തുടർച്ചയായി കൃഷി ചെയ്യരുത്.",
            "expert": "നിങ്ങളുടെ പ്രദേശത്തിന് അനുയോജ്യമായ വിത്തിനങ്ങൾക്ക് KVK അല്ലെങ്കിൽ കൃഷിഭവനുമായി ബന്ധപ്പെടുക.",
        },
        "market_schemes": {
            "problem": "വിപണി (മണ്ഡി) വില താരതമ്യവും സർക്കാർ കാർഷിക പദ്ധതികളും / സബ്സിഡികളും.",
            "causes": "വിപണി വില നിലവാരവും സർക്കാർ ആനുകൂല്യങ്ങളും മനസ്സിലാക്കൽ.",
            "steps": "1. വിളകൾ വിൽക്കുന്നതിന് മുമ്പ് അടുത്തുള്ള വിപണികളിലെയും e-NAM പോർട്ടലിലെയും വിലകൾ താരതമ്യം ചെയ്യുക.\n2. PM-KISAN (പ്രതിവർഷം ₹6,000), PMFBY വിള ഇൻഷുറൻസ്, KCC വായ്പ, ഡ്രിപ്പ് സബ്സിഡി എന്നിവയ്ക്കായി അപേക്ഷിക്കുക.",
            "precautions": "ഔദ്യോഗിക .gov.in പോർട്ടലുകൾ വഴിയോ കൃഷിഭവൻ വഴിയോ മാത്രം അപേക്ഷിക്കുക.",
            "expert": "e-NAM ഹെൽപ്പ്‌ലൈൻ 1800-270-0224 അല്ലെങ്കിൽ കിസാൻ കോൾ സെന്റർ 1800-180-1551-ൽ വിളിക്കുക.",
        },
        "sustainable_farming": {
            "problem": "കുറഞ്ഞ ചിലവിൽ സുസ്ഥിര ജൈവകൃഷി, പുതയിടൽ, കള നിയന്ത്രണം.",
            "causes": "വർദ്ധിച്ചുവരുന്ന കൃഷി ചിലവുകളും കളകളുടെ പ്രശ്നവും.",
            "steps": "1. പുതയിടൽ (Mulching) വഴി 80% കളകളെ തടയാനും 35% വെള്ളം ലാഭിക്കാനും സാധിക്കും.\n2. ജീവാണുവളങ്ങൾ, മണ്ണിര കമ്പോസ്റ്റ്, വേപ്പെണ്ണ എന്നിവ ഉപയോഗിക്കുക.",
            "precautions": "ജീവാണുവളങ്ങൾ രാസകീടനാശിനികളുമായി കലർത്തരുത്.",
            "expert": "ജൈവകൃഷി പരിശീലനത്തിനായി അടുത്തുള്ള KVK അല്ലെങ്കിൽ FPO-യുമായി ബന്ധപ്പെടുക.",
        },
        "general": {
            "problem": "സംയോജിത വിള-കൃഷിയിട പരിപാലന മാർഗ്ഗനിർദ്ദേശങ്ങൾ (Integrated Crop Advisory).",
            "causes": "മികച്ച വിളവിന് മണ്ണിലെ ഈർപ്പം, സന്തുലിത വളപ്രയോഗം, കീട നിരീക്ഷണം, കാലാവസ്ഥാധിഷ്ഠിത തീരുമാനങ്ങൾ എന്നിവ ആവശ്യമാണ്.",
            "steps": "1. രാവിലെ കൃഷിയിടത്തിൽ 10 ചെടികളുടെ ഇലകളും തണ്ടും പരിശോധിക്കുക.\n2. 5–8 സെ.മീ ആഴത്തിൽ ഈർപ്പം പരിശോധിച്ച് നനയ്ക്കുക.\n3. ജൈവവളങ്ങൾക്കൊപ്പം ഘട്ടംഘട്ടമായി പോഷകങ്ങൾ നൽകുക.\n4. മഞ്ഞ/നീല കെണികളും വേപ്പെണ്ണയും പ്രതിരോധത്തിനായി ഉപയോഗിക്കുക.",
            "precautions": "കാരണം ഉറപ്പാക്കാതെ രാസകീടനാശിനികൾ കലർത്തി തളിക്കരുത്.",
            "expert": "നെല്ല്, തക്കാളി, മുളക്, ജലസേചനം, വളപ്രയോഗം അല്ലെങ്കിൽ വിപണി വിലയെക്കുറിച്ച് ഏത് ചോദ്യവും ചോദിക്കാം, അല്ലെങ്കിൽ 1800-180-1551-ൽ വിളിക്കുക.",
        },
    },
}


def detect_crop_and_category(question: str, category_hint: str = "") -> Tuple[Optional[str], str]:
    q = question.lower()

    # 1. Detect specific crop if mentioned
    detected_crop: Optional[str] = None
    for crop_key, crop_words in CROP_KEYWORDS.items():
        if any(w in q for w in crop_words):
            detected_crop = crop_key
            break

    # 2. Detect agronomic category (score-based so multi-keyword matches win)
    if category_hint and category_hint in CATEGORY_KEYWORDS:
        return detected_crop, category_hint

    best_category = "general"
    best_score = 0
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for word in keywords if word in q)
        if score > best_score:
            best_score = score
            best_category = category

    # 3. If a crop was mentioned without a specific symptom keyword, default to crop_selection_season or crop_health
    if best_category == "general" and detected_crop:
        best_category = "crop_selection_season"

    return detected_crop, best_category


def get_structured_farming_advice(
    question: str, language_code: str, category_hint: str = ""
) -> Dict[str, Any]:
    detected_crop, topic = detect_crop_and_category(question, category_hint)
    lang = language_code if language_code in KNOWLEDGE_BASE else "en-IN"
    labels = SECTION_LABELS.get(lang, SECTION_LABELS["en-IN"])
    base_content = KNOWLEDGE_BASE[lang].get(topic, KNOWLEDGE_BASE[lang]["general"])

    # Create a copy so we can enrich with crop-specific context
    content = dict(base_content)

    if detected_crop:
        crop_display = CROP_DISPLAY_NAMES.get(detected_crop, {}).get(
            lang, detected_crop.capitalize()
        )
        content["problem"] = f"[{crop_display}] {content['problem']}"
        crop_note = CROP_SPECIFIC_NOTES.get(detected_crop, {}).get(lang)
        if crop_note:
            content["steps"] = f"{content['steps']}\n• {crop_note}"

    formatted_answer = (
        f"{labels['problem']}:\n{content['problem']}\n\n"
        f"{labels['causes']}:\n{content['causes']}\n\n"
        f"{labels['steps']}:\n{content['steps']}\n\n"
        f"{labels['precautions']}:\n{content['precautions']}\n\n"
        f"{labels['expert']}:\n{content['expert']}\n\n"
        f"{labels['notice']}"
    )

    sections = [
        {"key": "problem", "title": labels["problem"], "body": content["problem"]},
        {"key": "causes", "title": labels["causes"], "body": content["causes"]},
        {"key": "steps", "title": labels["steps"], "body": content["steps"]},
        {"key": "precautions", "title": labels["precautions"], "body": content["precautions"]},
        {"key": "expert", "title": labels["expert"], "body": content["expert"]},
    ]

    return {
        "answer": formatted_answer,
        "category": topic,
        "crop": detected_crop,
        "sections": sections,
        "notice": labels["notice"],
    }


def get_farming_advice(question: str, language_code: str) -> str:
    """
    Backward-compatible string return for get_farming_advice.
    """
    result = get_structured_farming_advice(question, language_code)
    return result["answer"]
