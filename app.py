import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Sahifa konfiguratsiyasi
st.set_page_config(
    page_title="Customs Value Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stillar
st.markdown("""
<style>
    * {
        font-family: Verdana, Geneva, Tahoma, sans-serif !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1rem 0;
        padding: 0.5rem;
        background-color: #ecf0f1;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #f1f3f4;
    }
    .login-container {
        max-width: 450px;
        margin: 3rem auto;
        padding: 3rem;
        background: #0e1117;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        color: white;
        text-align: center;
        border: 1px solid #333;
    }
    .login-title {
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1f77b4;
    }
    .login-subtitle {
        font-size: 1.2rem;
        margin-bottom: 0rem !important;
        opacity: 0.8;
        color: #ccc;
    }
    .login-form {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-top: 1rem;
    }
    
    /* Login tugmasi - yashil #08FF08 - KUCHLI SELECTOR */
    .login-button button,
    button[key="login_button"],
    div[data-testid="stButton"] button:contains("Tizimga kirish"),
    div[data-testid="stButton"] button:contains("🚀") {
        background: #08FF08 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    .login-button button:hover,
    button[key="login_button"]:hover,
    div[data-testid="stButton"] button:contains("Tizimga kirish"):hover,
    div[data-testid="stButton"] button:contains("🚀"):hover {
        background: #06CC06 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(8, 255, 8, 0.3) !important;
    }
    
    /* TIZIMGA KIRISH buttoni uchun maxsus stil */
    button[key="login_button"] {
        background: #08FF08 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    button[key="login_button"]:hover {
        background: #06CC06 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(8, 255, 8, 0.3) !important;
    }
    
    /* Input maydonlari */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px !important;
        color: #333 !important;
        font-size: 16px !important;
    }
    
    /* Sidebar Button Styles - Professional Glowing Effect */
    .stButton > button {
        width: 90% !important;
        height: 60px !important;
        border: none !important;
        outline: none !important;
        color: #fff !important;
        background: #111 !important;
        cursor: pointer !important;
        position: relative !important;
        z-index: 0 !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        margin: 0.5rem 0 !important;
        transition: all 0.3s ease !important;
    }

    .stButton::before {
        content: '' !important;
        background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000) !important;
        position: absolute !important;
        top: -2px !important;
        left: -2px !important;
        background-size: 400% !important;
        z-index: -1 !important;
        filter: blur(5px) !important;
        width: calc(95% + 4px) !important;
        height: calc(100% + 7px) !important;
        animation: glowing 20s linear infinite !important;
        opacity: 0 !important;
        transition: opacity .3s ease-in-out !important;
        border-radius: 10px !important;
    }

    .stButton:hover::before {
        opacity: 1 !important;
    }

    .stButton::after {
        z-index: -1 !important;
        content: '' !important;
        position: absolute !important;
        width: 93% !important;
        height: 100% !important;
        background: #111 !important;
        left: 0 !important;
        top: 0 !important;
        border-radius: 10px !important;
    }

    @keyframes glowing {
        0% { background-position: 0 0; }
        50% { background-position: 400% 0; }
        100% { background-position: 0 0; }
    }
    
    /* Chiqish tugmasi - qizil #FE0808 - KUCHLI SELECTOR */
    .logout-btn button,
    button[key="logout_btn"],
    div[data-testid="stButton"] button:contains("Chiqish"),
    div[data-testid="stButton"] button:contains("🚪") {
        background: #FE0808 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .logout-btn button:hover,
    button[key="logout_btn"]:hover,
    div[data-testid="stButton"] button:contains("Chiqish"):hover,
    div[data-testid="stButton"] button:contains("🚪"):hover {
        background: #CC0606 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(254, 8, 8, 0.3) !important;
    }
    
    /* CHIQISH buttoni uchun maxsus stil */
    button[key="logout_btn"] {
        background: #FE0808 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    button[key="logout_btn"]:hover {
        background: #CC0606 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(254, 8, 8, 0.3) !important;
    }
    
    /* Filter containers */
    .filter-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
    
    /* Streamlit elementlarini yashirish */
    .stDeployButton {display:none !important;}
    footer {visibility: hidden !important;}
    .stDecoration {display:none !important;}
    .stToolbar {display:none !important;}
    .stApp > header {display:none !important;}
    .stMainMenu {display:none !important;}
    header[data-testid="stHeader"] {display:none !important;}
    div[data-testid="stToolbar"] {display:none !important;}
    div[data-testid="stDecoration"] {display:none !important;}
    div[data-testid="stStatusWidget"] {display:none !important;}
    button[data-testid="baseButton-header"] {display:none !important;}
    .css-14xtw13.e8zbici0 {display:none !important;}
    .css-h5rgaw.egzxvld1 {display:none !important;}
    .reportview-container .sidebar-content {background-color: #f1f3f4;}
    
    /* Ortiqcha bo'shliqlarni yo'qotish */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Login sahifasidagi ortiqcha bo'shliqni yo'qotish */
    .login-subtitle + div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Barcha bo'sh div'larni yashirish */
    div:empty {
        display: none !important;
    }
    
    /* Container'lar orasidagi ortiqcha bo'shliqni kamaytirish */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Parol tekshirish funksiyasi
def check_password():
    """Parol va kod bilan kirish sistemasi"""
    
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Login form
    st.markdown("""
    <div class="login-container">
        <div class="login-title">📊 Customs Value Analytics</div>
        <div class="login-subtitle">Bojxona auditi boshqarmasi</div>
        <div class="login-form">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("#### 🔐 Xavfsiz kirish")
        st.markdown("**Tizimga kirish uchun ma'lumotlarni kiriting:**")
        
        # Parol kiritish
        password = st.text_input(
            "Parol", 
            type="password", 
            placeholder="Parolni kiriting...",
            key="password_input"
        )
        
        # Maxfiy kod kiritish
        secret_code = st.text_input(
            "Maxfiy kod",
            type="password",
            placeholder="Maxfiy kodni kiriting...",
            key="code_input"
        )
        
        # Login button container
        st.markdown('<div class="login-button">', unsafe_allow_html=True)
        if st.button("🚀 Tizimga kirish", key="login_button", use_container_width=True):
            if password == "admin123" and secret_code == "2025":
                st.session_state["password_correct"] = True
                st.success("✅ Muvaffaqiyatli kirildi!")
                st.rerun()
            else:
                st.error("❌ Parol yoki maxfiy kod noto'g'ri!")
                st.warning("💡 To'g'ri ma'lumotlarni kiriting")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    return False

# Agar parol noto'g'ri bo'lsa, dashboardni ko'rsatmaslik
if not check_password():
    st.stop()

# Ma'lumotlarni yuklash funksiyasi
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Sana ustunini o'zgartirish
        df['INSTIME'] = pd.to_datetime(df['INSTIME'], format='%d.%m.%Y %H:%M:%S', errors='coerce')
        
        # Raqamli ustunlarni tekshirish
        numeric_columns = ['Нетто', 'За.ед. из.$', 'Там.стоим $', 
                          'Минимал диапазон БК$ ХБТда', 'Ўрта диапазон БК$ ХБТда', 
                          'Максимал диапазон БК$ ХБТда']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # NaN qiymatlarni tozalash (asosiy ustunlar uchun)
        required_columns = ['31-Страна происхождения', 'Страна отправления', 'ТИФ ТН КОДИ', 'INSTIME']
        existing_required = [col for col in required_columns if col in df.columns]
        if existing_required:
            df = df.dropna(subset=existing_required)
        
        return df
    except Exception as e:
        st.error(f"Fayl yuklashda xatolik: {str(e)}")
        return None

# Excel yuklab olish funksiyasi
@st.cache_data
def create_excel_download(df, section_name):
    """Tahlil qilingan ma'lumotlarni Excel formatda tayyorlash"""
    try:
        from io import BytesIO
        
        # BytesIO buffer yaratish
        output = BytesIO()
        
        # Excel writer yaratish
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Asosiy ma'lumotlar
            df.to_excel(writer, sheet_name='Asosiy_Malumotlar', index=False)
            
            # Statistikalar (agar mavjud bo'lsa)
            if 'Там.стоим $' in df.columns:
                stats_df = pd.DataFrame({
                    'Ko\'rsatkich': ['Jami yozuvlar', 'O\'rtacha qiymat', 'Maksimal qiymat', 'Minimal qiymat', 'Standart og\'ish'],
                    'Qiymat': [
                        len(df),
                        f"${df['Там.стоим $'].mean():.2f}" if df['Там.стоим $'].notna().any() else "N/A",
                        f"${df['Там.стоим $'].max():.2f}" if df['Там.стоим $'].notna().any() else "N/A",
                        f"${df['Там.стоим $'].min():.2f}" if df['Там.стоим $'].notna().any() else "N/A",
                        f"${df['Там.стоим $'].std():.2f}" if df['Там.стоим $'].notna().any() else "N/A"
                    ]
                })
                stats_df.to_excel(writer, sheet_name='Statistikalar', index=False)
            
            # Davlatlar bo'yicha tahlil
            if '31-Страна происхождения' in df.columns and 'Там.стоим $' in df.columns:
                country_analysis = df.groupby('31-Страна происхождения').agg({
                    'Там.стоим $': ['count', 'mean', 'sum'],
                    'Нетто': 'sum' if 'Нетто' in df.columns else 'count'
                }).round(2)
                country_analysis.columns = ['Import_Soni', 'Ortacha_Qiymat', 'Jami_Qiymat', 'Jami_Ogirlik']
                country_analysis.to_excel(writer, sheet_name='Davlatlar_Tahlili')
            
            # HS kodlar bo'yicha tahlil
            if 'ТИФ ТН КОДИ' in df.columns and 'Там.стоим $' in df.columns:
                hs_analysis = df.groupby('ТИФ ТН КОДИ').agg({
                    'Там.стоим $': ['count', 'mean', 'sum'],
                    'Нетто': 'sum' if 'Нетто' in df.columns else 'count'
                }).round(2)
                hs_analysis.columns = ['Import_Soni', 'Ortacha_Qiymat', 'Jami_Qiymat', 'Jami_Ogirlik']
                hs_analysis.to_excel(writer, sheet_name='HS_Kodlar_Tahlili')
        
        # Buffer'ni qayta o'qish uchun boshiga o'tkazish
        output.seek(0)
        return output.getvalue()
    
    except Exception as e:
        st.error(f"Excel fayl yaratishda xatolik: {str(e)}")
        return None

# Demo ma'lumotlar yaratish
def create_demo_data():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    countries_origin = ['USA', 'CHN', 'DEU', 'TUR', 'RUS', 'KOR', 'JPN', 'IND']
    countries_dispatch = ['USA', 'CHN', 'DEU', 'TUR', 'RUS', 'KOR', 'JPN', 'IND', 'ARE', 'FRA']
    hs_codes = ['8517120000', '8471300000', '8473301100', '8528591000', '8544421000', 
                '8536500000', '8537109000', '8542310000']
    regimes = ['40', '10', '02', '51', '61']
    methods = ['1-metod', '2-metod', '3-metod', '4-metod', '5-metod', '6-metod']
    
    data = []
    for _ in range(1000):
        date = np.random.choice(dates)
        country_origin = np.random.choice(countries_origin)
        country_dispatch = np.random.choice(countries_dispatch)
        hs_code = np.random.choice(hs_codes)
        regime = np.random.choice(regimes)
        method = np.random.choice(methods)
        
        weight = np.random.uniform(10, 1000)
        unit_price = np.random.uniform(5, 100)
        customs_value = weight * unit_price * np.random.uniform(0.9, 1.1)
        
        min_range = customs_value * np.random.uniform(0.8, 0.9)
        avg_range = customs_value * np.random.uniform(0.95, 1.05)
        max_range = customs_value * np.random.uniform(1.1, 1.2)
        
        # Candlestick uchun OHLC ma'lumotlari
        open_price = unit_price
        high_price = unit_price * np.random.uniform(1.0, 1.1)
        low_price = unit_price * np.random.uniform(0.9, 1.0)
        close_price = np.random.uniform(low_price, high_price)
        
        data.append({
            '31-Страна происхождения': country_origin,
            'Страна отправления': country_dispatch,
            'ТИФ ТН КОДИ': hs_code,
            'Режим': regime,
            'metod': method,
            'Нетто': weight,
            'За.ед. из.$': unit_price,
            'Там.стоим $': customs_value,
            'Минимал диапазон БК$ ХБТда': min_range,
            'Ўрта диапазон БК$ ХБТда': avg_range,
            'Максимал диапазон БК$ ХБТда': max_range,
            'OPEN': open_price,
            'HIGH': high_price,
            'LOW': low_price,
            'CLOSE': close_price,
            'INSTIME': date
        })
    
    return pd.DataFrame(data)

# Progressive filtering funksiyasi
def get_available_options(df, column, selected_filters):
    """Selected filtrlar asosida mavjud bo'lgan optionlarni qaytaradi"""
    if df is None or len(df) == 0:
        return ['Hammasi']
    
    # Oldingi filtrlarni qo'llash
    filtered_df = df.copy()
    
    for filter_col, filter_val in selected_filters.items():
        if filter_val != 'Hammasi' and filter_col in filtered_df.columns:
            if filter_col == 'VAQT':
                # Vaqt filtri uchun alohida logika
                today = datetime.now()
                if filter_val == "So'nggi 30 kun":
                    start_date = today - timedelta(days=30)
                elif filter_val == "So'nggi 90 kun":
                    start_date = today - timedelta(days=90)
                elif filter_val == "So'nggi yil":
                    start_date = today - timedelta(days=365)
                else:
                    continue
                filtered_df = filtered_df[filtered_df['INSTIME'] >= start_date]
            else:
                filtered_df = filtered_df[filtered_df[filter_col] == filter_val]
    
    if column in filtered_df.columns:
        unique_values = sorted(filtered_df[column].dropna().unique().tolist())
        return ['Hammasi'] + unique_values
    else:
        return ['Hammasi']

# Header va logo
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    st.markdown("")  # Bo'sh joy

with col2:
    st.markdown('<div class="main-header">📊 Customs Value Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #666; margin-top: -0.5rem;">Bojxona auditi boshqarmasi</div>', unsafe_allow_html=True)

with col3:
    # Bojxona logosi - loyihadagi st.image.png faylini ishlatish
    try:
        st.image("st.image.png", width=120)
    except:
        # Agar fayl topilmasa, SVG logoni ko'rsatish
        st.markdown("""
        <div style="text-align: right; margin-top: 0.5rem;">
            <svg width="90" height="90" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                <!-- Tashqi yulduz (8 qirrali) -->
                <polygon points="60,10 70,45 105,45 78,68 88,103 60,85 32,103 42,68 15,45 50,45" 
                         fill="#C8C8C8" stroke="#A0A0A0" stroke-width="2"/>
                
                <!-- Ichki doira - yashil -->
                <circle cx="60" cy="60" r="32" fill="#4A7C59" stroke="#2F4F2F" stroke-width="2"/>
                
                <!-- Oq ichki doira -->
                <circle cx="60" cy="60" r="28" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
                
                <!-- Dunyoning konturi -->
                <g transform="translate(60,60)">
                    <!-- Kontinentlar -->
                    <path d="M-20,-5 Q-15,-10 -10,-8 Q-5,-12 0,-10 Q5,-15 10,-12 Q15,-8 20,-5" 
                          fill="#8B4513" opacity="0.7"/>
                    <path d="M-18,5 Q-10,8 -5,5 Q0,8 5,5 Q10,3 18,8" 
                          fill="#8B4513" opacity="0.7"/>
                    <path d="M-15,15 Q-8,18 0,15 Q8,18 15,15" 
                          fill="#8B4513" opacity="0.7"/>
                </g>
                
                <!-- Tibbiy belgi (Caduceus) markazi -->
                <g transform="translate(60,60)">
                    <!-- Asosiy tayoq -->
                    <line x1="0" y1="-20" x2="0" y2="20" stroke="#FFD700" stroke-width="3"/>
                    
                    <!-- Qanotlar -->
                    <path d="M-12,-15 Q-20,-18 -15,-10 Q-8,-5 0,-12" fill="#FFD700" opacity="0.9"/>
                    <path d="M12,-15 Q20,-18 15,-10 Q8,-5 0,-12" fill="#FFD700" opacity="0.9"/>
                    
                    <!-- Chap ilon -->
                    <path d="M-4,-15 Q-10,-8 -4,0 Q2,8 -4,15" 
                          fill="none" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round"/>
                    
                    <!-- O'ng ilon -->
                    <path d="M4,-15 Q10,-8 4,0 Q-2,8 4,15" 
                          fill="none" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round"/>
                    
                    <!-- Ustki to'p -->
                    <circle cx="0" cy="-20" r="3" fill="#FFD700"/>
                    
                    <!-- Ilon boshlari -->
                    <circle cx="-4" cy="-15" r="1.5" fill="#FFD700"/>
                    <circle cx="4" cy="-15" r="1.5" fill="#FFD700"/>
                </g>
                
                <!-- Atrofdagi matn -->
                <path id="top-curve" d="M 20 60 A 40 40 0 0 1 100 60" fill="none"/>
                <text font-family="Arial" font-size="9" font-weight="bold" fill="#4A7C59">
                    <textPath href="#top-curve" startOffset="5%">
                        O'ZBEKISTON RESPUBLIKASI
                    </textPath>
                </text>
                
                <path id="bottom-curve" d="M 100 60 A 40 40 0 0 1 20 60" fill="none"/>
                <text font-family="Arial" font-size="9" font-weight="bold" fill="#4A7C59">
                    <textPath href="#bottom-curve" startOffset="5%">
                        DAVLAT BOJXONA XIZMATI
                    </textPath>
                </text>
            </svg>
        </div>
        """, unsafe_allow_html=True)

# Logout button
col1, col2, col3 = st.columns([5, 1, 1])
with col3:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 Chiqish", key="logout_btn"):
        st.session_state["password_correct"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar - TAHLIL TURLARI
st.sidebar.header("📊 TAHLIL TURLARI")
st.sidebar.markdown("---")

# Session state uchun sahifa holati
if 'selected_section' not in st.session_state:
    st.session_state.selected_section = "CANDLESTICK"

# Sidebar buttons
with st.sidebar:
    st.markdown('<div class="sidebar-buttons">', unsafe_allow_html=True)
    
    if st.button("🕯️ CANDLESTICK"):
        st.session_state.selected_section = "CANDLESTICK"
    
    if st.button("📊 GRAFIK"):
        st.session_state.selected_section = "GRAFIK"
    
    if st.button("🌍 SUNBURST"):
        st.session_state.selected_section = "SUNBURST"
    
    if st.button("🕒 TIME GROUP"):
        st.session_state.selected_section = "TIME GROUP"
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tanlangan bo'limni olish
selected_section = st.session_state.selected_section

# Ma'lumotlarni olish
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Markaziy qism - Fayl yuklash va filtrlar
st.markdown("### 📁 Fayl yuklash")

# Faqat fayl yuklash
uploaded_file = st.file_uploader(
    "Faylni yuklash:",
    type=['csv', 'xlsx', 'xls'],
    help="Kerakli ustunlar: 31-Страна происхождения, Страна отправления, ТИФ ТН КОДИ, metod, INSTIME, Там.стоим $",
    key="main_file_uploader"
)

# Ma'lumotlarni olish
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is None:
        st.stop()
else:
    st.info("Demo ma'lumotlar ishlatilmoqda")
    df = create_demo_data()

# PROGRESSIVE FILTRLAR bo'limi
st.markdown("---")
st.markdown("### 🔍 FILTRLAR")
st.markdown('<div class="filter-container">', unsafe_allow_html=True)

# Session state uchun filtrlar
filter_keys = ['15-GRAFA', '34-GRAFA', 'ТИФ ТН КОДИ', 'METOD', 'VAQT']
for key in filter_keys:
    if f'filter_{key}' not in st.session_state:
        st.session_state[f'filter_{key}'] = 'Hammasi'

# Filtr ustunlari uchun mapping
filter_mapping = {
    '15-GRAFA': 'Страна отправления',
    '34-GRAFA': '31-Страна происхождения', 
    'ТИФ ТН КОДИ': 'ТИФ ТН КОДИ',
    'METOD': 'metod',
    'VAQT': 'INSTIME'
}

# Progressive filtrlar
col1, col2, col3, col4, col5 = st.columns(5)

# 1. 15-GRAFA (Страна отправления)
with col1:
    current_filters = {}
    countries_dispatch = get_available_options(df, 'Страна отправления', current_filters)
    selected_dispatch = st.selectbox(
        "15-GRAFA",
        countries_dispatch,
        key="dispatch_filter",
        help="Tovar yuborilgan mamlakat"
    )
    st.session_state['filter_15-GRAFA'] = selected_dispatch

# 2. 34-GRAFA (31-Страна происхождения)
with col2:
    current_filters = {'Страна отправления': selected_dispatch}
    countries_origin = get_available_options(df, '31-Страна происхождения', current_filters)
    selected_origin = st.selectbox(
        "34-GRAFA",
        countries_origin,
        key="origin_filter", 
        help="Tovar kelib chiqish mamlakati"
    )
    st.session_state['filter_34-GRAFA'] = selected_origin

# 3. ТИФ ТН КОДИ
with col3:
    current_filters = {
        'Страна отправления': selected_dispatch,
        '31-Страна происхождения': selected_origin
    }
    hs_codes = get_available_options(df, 'ТИФ ТН КОДИ', current_filters)
    selected_hs = st.selectbox(
        "ТИФ ТН КОДИ",
        hs_codes,
        key="hs_filter",
        help="Tovar HS kodi"
    )
    st.session_state['filter_ТИФ ТН КОДИ'] = selected_hs

# 4. METOD
with col4:
    current_filters = {
        'Страна отправления': selected_dispatch,
        '31-Страна происхождения': selected_origin,
        'ТИФ ТН КОДИ': selected_hs
    }
    methods = get_available_options(df, 'metod', current_filters)
    selected_method = st.selectbox(
        "METOD",
        methods,
        key="method_filter",
        help="Bojxona qiymatining aniqlash metodi"
    )
    st.session_state['filter_METOD'] = selected_method

# 5. VAQT
with col5:
    date_options = ["Hammasi", "So'nggi 30 kun", "So'nggi 90 kun", "So'nggi yil"]
    selected_date = st.selectbox(
        "VAQT",
        date_options,
        key="date_filter",
        help="Vaqt oralig'i"
    )
    st.session_state['filter_VAQT'] = selected_date

st.markdown('</div>', unsafe_allow_html=True)

# Ma'lumotlarni filtrlash
filtered_df = df.copy()

# Har bir filtrni qo'llash
if selected_dispatch != 'Hammasi':
    filtered_df = filtered_df[filtered_df['Страна отправления'] == selected_dispatch]

if selected_origin != 'Hammasi':
    filtered_df = filtered_df[filtered_df['31-Страна происхождения'] == selected_origin]

if selected_hs != 'Hammasi':
    filtered_df = filtered_df[filtered_df['ТИФ ТН КОДИ'] == selected_hs]

if selected_method != 'Hammasi':
    filtered_df = filtered_df[filtered_df['metod'] == selected_method]

# Vaqt filtri
if selected_date != "Hammasi":
    today = datetime.now()
    if selected_date == "So'nggi 30 kun":
        start_date = today - timedelta(days=30)
    elif selected_date == "So'nggi 90 kun":
        start_date = today - timedelta(days=90)
    else:  # So'nggi yil
        start_date = today - timedelta(days=365)
    
    filtered_df = filtered_df[filtered_df['INSTIME'] >= start_date]

st.markdown("---")

# Asosiy ko'rsatkichlar
if 'Там.стоим $' in filtered_df.columns and len(filtered_df) > 0:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jami yozuvlar", len(filtered_df))
    with col2:
        avg_value = filtered_df['Там.стоим $'].mean()
        st.metric("O'rtacha qiymat", f"${avg_value:.2f}" if not pd.isna(avg_value) else "N/A")
    with col3:
        max_value = filtered_df['Там.стоим $'].max()
        st.metric("Eng yuqori qiymat", f"${max_value:.2f}" if not pd.isna(max_value) else "N/A")
    with col4:
        min_value = filtered_df['Там.стоим $'].min()
        st.metric("Eng past qiymat", f"${min_value:.2f}" if not pd.isna(min_value) else "N/A")
else:
    st.metric("Jami yozuvlar", len(filtered_df))

# CANDLESTICK BO'LIMI
if selected_section == "CANDLESTICK":
    st.markdown('<div class="section-header">🕯️ CANDLESTICK - Professional Bojxona Qiymatlari Tahlili</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'За.ед. из.$' in filtered_df.columns:
        # Ma'lumot haqida qisqacha info
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            current_price = filtered_df['За.ед. из.$'].iloc[-1]
            st.metric("Joriy narx", f"${current_price:.2f}")
        with col2:
            price_change = filtered_df['За.ед. из.$'].iloc[-1] - filtered_df['За.ед. из.$'].iloc[-2] if len(filtered_df) > 1 else 0
            st.metric("O'zgarish", f"${price_change:.2f}", f"{price_change:.2f}")
        with col3:
            if 'Нетто' in filtered_df.columns:
                st.metric("Hajm", f"{filtered_df['Нетто'].sum():.0f}")
            else:
                st.metric("Hajm", "N/A")
        with col4:
            st.metric("Kun maksimumi", f"${filtered_df['За.ед. из.$'].max():.2f}")
        with col5:
            st.metric("Kun minimumi", f"${filtered_df['За.ед. из.$'].min():.2f}")
        
        # Kunlik ma'lumotlarni agregatsiya qilish - TO'G'RI KETMA-KETLIK BILAN
        if 'OPEN' in filtered_df.columns:
            daily_agg = filtered_df.groupby(filtered_df['INSTIME'].dt.date).agg({
                'OPEN': 'first',
                'HIGH': 'max', 
                'LOW': 'min',
                'CLOSE': 'last',
                'Нетто': 'sum' if 'Нетто' in filtered_df.columns else 'count'
            }).reset_index()
            daily_agg['INSTIME'] = pd.to_datetime(daily_agg['INSTIME'])
            daily_agg = daily_agg.sort_values('INSTIME')
        else:
            # За.ед. из.$ dan TO'G'RI OHLC yaratish
            filtered_df_sorted = filtered_df.sort_values('INSTIME')
            daily_groups = filtered_df_sorted.groupby(filtered_df_sorted['INSTIME'].dt.date)
            
            daily_data = []
            prev_close = None
            
            for date, group in daily_groups:
                group_sorted = group.sort_values('INSTIME')
                
                # Agar oldingi kun mavjud bo'lsa, uning close qiymatidan boshlaymiz
                if prev_close is not None:
                    open_price = prev_close
                else:
                    open_price = group_sorted['За.ед. из.$'].iloc[0]
                
                high_price = group_sorted['За.ед. из.$'].max()
                low_price = group_sorted['За.ед. из.$'].min()
                close_price = group_sorted['За.ед. из.$'].iloc[-1]
                volume = group_sorted['Нетто'].sum() if 'Нетто' in group_sorted.columns else len(group_sorted)
                
                daily_data.append({
                    'INSTIME': pd.to_datetime(date),
                    'OPEN': open_price,
                    'HIGH': high_price,
                    'LOW': low_price,
                    'CLOSE': close_price,
                    'Volume': volume
                })
                
                # Keyingi kun uchun close qiymatini saqlash
                prev_close = close_price
            
            daily_agg = pd.DataFrame(daily_data)
            daily_agg = daily_agg.sort_values('INSTIME')
        
        if len(daily_agg) > 0:
            # Professional Candlestick Chart
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                row_heights=[0.7, 0.3],
                subplot_titles=('Bojxona Qiymatlari (OHLC)', 'Hajm')
            )
            
            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=daily_agg['INSTIME'],
                    open=daily_agg['OPEN'],
                    high=daily_agg['HIGH'],
                    low=daily_agg['LOW'],
                    close=daily_agg['CLOSE'],
                    name="OHLC",
                    increasing_line_color='#00ff00',
                    decreasing_line_color='#ff0000',
                    increasing_fillcolor='rgba(0,255,0,0.7)',
                    decreasing_fillcolor='rgba(255,0,0,0.7)'
                ),
                row=1, col=1
            )
            
            # Moving averages qo'shish
            if len(daily_agg) >= 20:
                daily_agg['MA20'] = daily_agg['CLOSE'].rolling(window=20).mean()
                fig.add_trace(
                    go.Scatter(
                        x=daily_agg['INSTIME'],
                        y=daily_agg['MA20'],
                        mode='lines',
                        name='MA20',
                        line=dict(color='blue', width=1)
                    ),
                    row=1, col=1
                )
            
            # Volume bars
            volume_col = 'Нетто' if 'Нетто' in daily_agg.columns else 'Volume'
            if volume_col in daily_agg.columns:
                colors = ['green' if daily_agg['CLOSE'].iloc[i] >= daily_agg['OPEN'].iloc[i] else 'red' 
                          for i in range(len(daily_agg))]
                
                fig.add_trace(
                    go.Bar(
                        x=daily_agg['INSTIME'],
                        y=daily_agg[volume_col],
                        name="Hajm",
                        marker_color=colors,
                        opacity=0.7
                    ),
                    row=2, col=1
                )
            
            # Layout sozlamalari
            fig.update_layout(
                title={
                    'text': f"Bojxona Qiymatlari Professional Tahlil - Joriy: ${current_price:.2f}",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'color': 'white', 'size': 16}
                },
                height=800,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                plot_bgcolor='#0e1117',
                paper_bgcolor='#0e1117',
                font=dict(color='white'),
                legend=dict(
                    font=dict(color='white'),
                    bgcolor='rgba(0,0,0,0)'
                )
            )
            
            # X va Y o'qlarini sozlash
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#333', zeroline=False, color='white', row=1, col=1)
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#333', zeroline=False, color='white', title_text="Sana", row=2, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333', zeroline=False, color='white', title_text="Narx ($)", tickformat='$,.0f', row=1, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333', zeroline=False, color='white', title_text="Hajm", tickformat=',.0f', row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Excel yuklab olish buttoni
        st.markdown("---")
        excel_data = create_excel_download(filtered_df, "CANDLESTICK")
        if excel_data:
            st.download_button(
                label="📊 Excel formatda yuklab olish",
                data=excel_data,
                file_name=f"candlestick_tahlil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
    else:
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi yoki kerakli ustunlar mavjud emas")

# GRAFIK BO'LIMI  
elif selected_section == "GRAFIK":
    st.markdown('<div class="section-header">📈 GRAFIK - Vaqt bo\'yicha qiymat monitoring</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'За.ед. из.$' in filtered_df.columns:
        # Vaqt bo'yicha saralash
        filtered_df_sorted = filtered_df.sort_values('INSTIME')
        
        fig = go.Figure()
        
        # Real narxlar
        fig.add_trace(go.Scatter(
            x=filtered_df_sorted['INSTIME'],
            y=filtered_df_sorted['За.ед. из.$'],
            mode='markers+lines',
            name='Real qiymatlar',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        
        # Statistik chiziqlar
        max_price = filtered_df['За.ед. из.$'].max()
        min_price = filtered_df['За.ед. из.$'].min()
        mean_price = filtered_df['За.ед. из.$'].mean()
        
        # Eng yuqori qiymat
        fig.add_hline(y=max_price, line_dash="dash", line_color="green", 
                     annotation_text=f"Eng yuqori: ${max_price:.2f}")
        
        # Eng past qiymat
        fig.add_hline(y=min_price, line_dash="dash", line_color="red",
                     annotation_text=f"Eng past: ${min_price:.2f}")
        
        # O'rtacha qiymat
        fig.add_hline(y=mean_price, line_dash="dash", line_color="orange",
                     annotation_text=f"O'rtacha: ${mean_price:.2f}")
        
        fig.update_layout(
            title="Bojxona qiymatlari vaqt bo'yicha",
            xaxis_title="Vaqt",
            yaxis_title="Qiymat ($)",
            height=600,
            showlegend=True,
            yaxis=dict(tickformat='$,.2f')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Excel yuklab olish buttoni
        st.markdown("---")
        excel_data = create_excel_download(filtered_df, "GRAFIK")
        if excel_data:
            st.download_button(
                label="📊 Excel formatda yuklab olish",
                data=excel_data,
                file_name=f"grafik_tahlil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi yoki kerakli ustunlar mavjud emas")

# SUNBURST BO'LIMI
elif selected_section == "SUNBURST":
    st.markdown('<div class="section-header">🌍 SUNBURST - Davlat va HS kodlar bo\'yicha ulush</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'Там.стоим $' in filtered_df.columns and '31-Страна происхождения' in filtered_df.columns:
        # Davlat va HS kodlar bo'yicha yig'indi qiymat
        sunburst_data = filtered_df.groupby(['31-Страна происхождения', 'ТИФ ТН КОДИ'])['Там.стоим $'].sum().reset_index()
        
        fig = px.sunburst(
            sunburst_data,
            path=['31-Страна происхождения', 'ТИФ ТН КОДИ'],
            values='Там.стоим $',
            title="Davlat va HS kodlar bo'yicha bojxona qiymatlari ulushi"
        )
        
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
        
        # Treemap alternativasi
        st.subheader("📦 Treemap ko'rinishi")
        fig2 = px.treemap(
            sunburst_data,
            path=['31-Страна происхождения', 'ТИФ ТН КОДИ'],
            values='Там.стоим $',
            title="Treemap - Davlat va HS kodlar bo'yicha ulush"
        )
        fig2.update_layout(height=600)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Excel yuklab olish buttoni
        st.markdown("---")
        excel_data = create_excel_download(filtered_df, "SUNBURST")
        if excel_data:
            st.download_button(
                label="📊 Excel formatda yuklab olish",
                data=excel_data,
                file_name=f"sunburst_tahlil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi yoki kerakli ustunlar mavjud emas")

# TIME GROUP BO'LIMI
elif selected_section == "TIME GROUP":
    st.markdown('<div class="section-header">🕒 TIME GROUP - Vaqtga asoslangan analiz</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'За.ед. из.$' in filtered_df.columns:
        # Vaqt gruppalarini tanlash
        time_group = st.selectbox("Vaqt guruhi", ["Kunlik", "Haftalik", "Oylik"])
        
        if time_group == "Kunlik":
            filtered_df['time_group'] = filtered_df['INSTIME'].dt.date
        elif time_group == "Haftalik":
            filtered_df['time_group'] = filtered_df['INSTIME'].dt.to_period('W').dt.start_time
        else:  # Oylik
            filtered_df['time_group'] = filtered_df['INSTIME'].dt.to_period('M').dt.start_time
        
        # Vaqt bo'yicha statistikalar
        time_stats = filtered_df.groupby('time_group').agg({
            'За.ед. из.$': ['mean', 'count', 'sum', 'min', 'max']
        }).round(2)
        
        time_stats.columns = ['O\'rtacha qiymat', 'Soni', 'Jami qiymat', 'Min qiymat', 'Max qiymat']
        time_stats = time_stats.reset_index()
        
        # Chiziqli grafik
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("O'rtacha qiymat o'zgarishi", "Rasmiylashtirish soni"),
            vertical_spacing=0.1
        )
        
        # O'rtacha qiymat
        fig.add_trace(
            go.Scatter(
                x=time_stats['time_group'],
                y=time_stats['O\'rtacha qiymat'],
                mode='lines+markers',
                name='O\'rtacha qiymat',
                line=dict(color='blue', width=3)
            ),
            row=1, col=1
        )
        
        # Rasmiylashtirish soni
        fig.add_trace(
            go.Bar(
                x=time_stats['time_group'],
                y=time_stats['Soni'],
                name='Rasmiylashtirish soni',
                marker_color='lightblue'
            ),
            row=2, col=1
        )
        
        fig.update_layout(height=800, showlegend=True)
        fig.update_xaxes(title_text="Vaqt", row=2, col=1)
        fig.update_yaxes(title_text="Qiymat ($)", tickformat='$,.2f', row=1, col=1)
        fig.update_yaxes(title_text="Soni", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Jadval
        st.subheader("📊 Vaqt bo'yicha statistika")
        st.dataframe(time_stats)
        
        # Trend tahlili
        if len(time_stats) > 1:
            price_trend = time_stats['O\'rtacha qiymat'].iloc[-1] - time_stats['O\'rtacha qiymat'].iloc[0]
            count_trend = time_stats['Soni'].iloc[-1] - time_stats['Soni'].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                trend_color = "green" if price_trend > 0 else "red"
                st.markdown(f"**Qiymat trendi:** <span style='color:{trend_color}'>{price_trend:+.2f}$</span>", unsafe_allow_html=True)
            with col2:
                trend_color = "green" if count_trend > 0 else "red"
                st.markdown(f"**Hajm trendi:** <span style='color:{trend_color}'>{count_trend:+}</span>", unsafe_allow_html=True)
        
        # Excel yuklab olish buttoni
        st.markdown("---")
        excel_data = create_excel_download(filtered_df, "TIME_GROUP")
        if excel_data:
            st.download_button(
                label="📊 Excel formatda yuklab olish",
                data=excel_data,
                file_name=f"time_group_tahlil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi yoki kerakli ustunlar mavjud emas")

# Import Analytics Dashboard footer
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Customs Value Analytics**")
st.sidebar.markdown("Tashkent, 2025")
st.sidebar.markdown("Real vaqtda monitoring va tahlil")
