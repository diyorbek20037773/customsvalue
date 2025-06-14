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
        df['G38'] = pd.to_numeric(df['G38'], errors='coerce')
        df['PRICE'] = pd.to_numeric(df['PRICE'], errors='coerce')
        
        # NaN qiymatlarni tozalash
        df = df.dropna(subset=['G34', 'G33', 'PRICE', 'INSTIME'])
        
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
            
            # Statistikalar
            stats_df = pd.DataFrame({
                'Ko\'rsatkich': ['Jami yozuvlar', 'O\'rtacha narx', 'Maksimal narx', 'Minimal narx', 'Standart og\'ish'],
                'Qiymat': [
                    len(df),
                    f"${df['PRICE'].mean():.2f}",
                    f"${df['PRICE'].max():.2f}",
                    f"${df['PRICE'].min():.2f}",
                    f"${df['PRICE'].std():.2f}"
                ]
            })
            stats_df.to_excel(writer, sheet_name='Statistikalar', index=False)
            
            # Davlatlar bo'yicha tahlil
            country_analysis = df.groupby('G34').agg({
                'PRICE': ['count', 'mean', 'sum'],
                'G38': 'sum'
            }).round(2)
            country_analysis.columns = ['Import_Soni', 'Ortacha_Narx', 'Jami_Qiymat', 'Jami_Ogirlik']
            country_analysis.to_excel(writer, sheet_name='Davlatlar_Tahlili')
            
            # HS kodlar bo'yicha tahlil
            hs_analysis = df.groupby('G33').agg({
                'PRICE': ['count', 'mean', 'sum'],
                'G38': 'sum'
            }).round(2)
            hs_analysis.columns = ['Import_Soni', 'Ortacha_Narx', 'Jami_Qiymat', 'Jami_Ogirlik']
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
    
    countries = ['USA', 'CHN', 'DEU', 'TUR', 'RUS', 'KOR', 'JPN', 'IND']
    hs_codes = ['8517', '8471', '8473', '8528', '8544', '8536', '8537', '8542']
    
    data = []
    for _ in range(1000):
        date = np.random.choice(dates)
        country = np.random.choice(countries)
        hs_code = np.random.choice(hs_codes)
        weight = np.random.uniform(10, 1000)
        price = np.random.uniform(5, 100)
        
        # Candlestick uchun OHLC ma'lumotlari
        open_price = price
        high_price = price * np.random.uniform(1.0, 1.1)
        low_price = price * np.random.uniform(0.9, 1.0)
        close_price = np.random.uniform(low_price, high_price)
        
        data.append({
            'G34': country,
            'G33': hs_code,
            'G38': weight,
            'PRICE': price,
            'OPEN': open_price,
            'HIGH': high_price,
            'LOW': low_price,
            'CLOSE': close_price,
            'INSTIME': date
        })
    
    return pd.DataFrame(data)

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
    
    if st.button("📈 YIELD CURVES"):
        st.session_state.selected_section = "YIELD CURVES"
    
    if st.button("📊 GRAFIK"):
        st.session_state.selected_section = "GRAFIK"
    
    if st.button("📋 USTUNLI DIAGRAMMA"):
        st.session_state.selected_section = "USTUNLI DIAGRAMMA"
    
    if st.button("📉 HISTOGRAM"):
        st.session_state.selected_section = "HISTOGRAM"
    
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
st.markdown("### 📁 Fayl yuklash va filtrlar")

# Faqat fayl yuklash
st.markdown("**Faylni yuklash:**")
uploaded_file = st.file_uploader(
    "",
    type=['csv', 'xlsx', 'xls'],
    help="G34, G33, G38, PRICE, INSTIME ustunlari bo'lishi kerak",
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

# FILTRLAR bo'limi - katta buttonlar yonma-yon
st.markdown("### 🔍 FILTRLAR")

# Filtr buttonlari uchun 3 ustun
col1, col2, col3 = st.columns(3)

with col1:
    countries = ['Hammasi'] + sorted(df['G34'].unique().tolist())
    selected_country = st.selectbox(
        "34-GRAFA",
        countries,
        key="country_filter",
        help="Kelib chiqish davlati"
    )

with col2:
    hs_codes = ['Hammasi'] + sorted(df['G33'].unique().tolist())
    selected_hs = st.selectbox(
        "33-GRAFA", 
        hs_codes,
        key="hs_filter",
        help="HS kodi"
    )

with col3:
    # Qo'shimcha filtr - Vaqt oralig'i
    date_range = st.selectbox(
        "VAQT ORALIG'I",
        ["Hammasi", "So'nggi 30 kun", "So'nggi 90 kun", "So'nggi yil"],
        key="date_filter"
    )

# Ma'lumotlarni filtrlash
filtered_df = df.copy()
if selected_country != 'Hammasi':
    filtered_df = filtered_df[filtered_df['G34'] == selected_country]
if selected_hs != 'Hammasi':
    filtered_df = filtered_df[filtered_df['G33'] == selected_hs]

# Vaqt filtri
if date_range != "Hammasi":
    today = datetime.now()
    if date_range == "So'nggi 30 kun":
        start_date = today - timedelta(days=30)
    elif date_range == "So'nggi 90 kun":
        start_date = today - timedelta(days=90)
    else:  # So'nggi yil
        start_date = today - timedelta(days=365)
    
    filtered_df = filtered_df[filtered_df['INSTIME'] >= start_date]

st.markdown("---")

# Asosiy ko'rsatkichlar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Jami yozuvlar", len(filtered_df))
with col2:
    st.metric("O'rtacha narx", f"${filtered_df['PRICE'].mean():.2f}")
with col3:
    st.metric("Eng yuqori narx", f"${filtered_df['PRICE'].max():.2f}")
with col4:
    st.metric("Eng past narx", f"${filtered_df['PRICE'].min():.2f}")

# CANDLESTICK BO'LIMI
if selected_section == "CANDLESTICK":
    st.markdown('<div class="section-header">🕯️ CANDLESTICK - Professional Bojxona Qiymatlari Tahlili</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
        # Ma'lumot haqida qisqacha info
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            current_price = filtered_df['PRICE'].iloc[-1]
            st.metric("Joriy narx", f"${current_price:.2f}")
        with col2:
            price_change = filtered_df['PRICE'].iloc[-1] - filtered_df['PRICE'].iloc[-2] if len(filtered_df) > 1 else 0
            st.metric("O'zgarish", f"${price_change:.2f}", f"{price_change:.2f}")
        with col3:
            st.metric("Hajm", f"{filtered_df['G38'].sum():.0f}")
        with col4:
            st.metric("Kun maksimumi", f"${filtered_df['PRICE'].max():.2f}")
        with col5:
            st.metric("Kun minimumi", f"${filtered_df['PRICE'].min():.2f}")
        
        # Kunlik ma'lumotlarni agregatsiya qilish
        if 'OPEN' in filtered_df.columns:
            daily_agg = filtered_df.groupby(filtered_df['INSTIME'].dt.date).agg({
                'OPEN': 'first',
                'HIGH': 'max', 
                'LOW': 'min',
                'CLOSE': 'last',
                'G38': 'sum'  # Hajm uchun
            }).reset_index()
            daily_agg['INSTIME'] = pd.to_datetime(daily_agg['INSTIME'])
            daily_agg = daily_agg.sort_values('INSTIME')
        else:
            # PRICE dan OHLC yaratish
            daily_agg = filtered_df.groupby(filtered_df['INSTIME'].dt.date).agg({
                'PRICE': ['first', 'max', 'min', 'last'],
                'G38': 'sum'
            }).reset_index()
            daily_agg.columns = ['INSTIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'G38']
            daily_agg['INSTIME'] = pd.to_datetime(daily_agg['INSTIME'])
            daily_agg = daily_agg.sort_values('INSTIME')
        
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
                increasing_line_color='#00ff00',  # Yashil
                decreasing_line_color='#ff0000',  # Qizil
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
        
        if len(daily_agg) >= 50:
            daily_agg['MA50'] = daily_agg['CLOSE'].rolling(window=50).mean()
            fig.add_trace(
                go.Scatter(
                    x=daily_agg['INSTIME'],
                    y=daily_agg['MA50'],
                    mode='lines',
                    name='MA50',
                    line=dict(color='orange', width=1)
                ),
                row=1, col=1
            )
        
        # Volume bars
        colors = ['green' if daily_agg['CLOSE'].iloc[i] >= daily_agg['OPEN'].iloc[i] else 'red' 
                  for i in range(len(daily_agg))]
        
        fig.add_trace(
            go.Bar(
                x=daily_agg['INSTIME'],
                y=daily_agg['G38'],
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
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#333',
            zeroline=False,
            color='white',
            row=1, col=1
        )
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#333',
            zeroline=False,
            color='white',
            title_text="Sana",
            row=2, col=1
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#333',
            zeroline=False,
            color='white',
            title_text="Narx ($)",
            tickformat='$,.0f',
            row=1, col=1
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#333',
            zeroline=False,
            color='white',
            title_text="Hajm",
            tickformat=',.0f',
            row=2, col=1
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Technical indicators
        st.subheader("📈 Texnik Ko'rsatkichlar")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # RSI calculation (simplified)
            if len(daily_agg) >= 14:
                price_diff = daily_agg['CLOSE'].diff()
                gain = price_diff.where(price_diff > 0, 0).rolling(window=14).mean()
                loss = (-price_diff.where(price_diff < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                current_rsi = rsi.iloc[-1]
                st.metric("RSI (14)", f"{current_rsi:.1f}")
                
                if current_rsi > 70:
                    st.error("🔴 Overbought (Sotish signali)")
                elif current_rsi < 30:
                    st.success("🟢 Oversold (Sotib olish signali)")
                else:
                    st.info("🟡 Neytral zona")
        
        with col2:
            # Bollinger Bands
            if len(daily_agg) >= 20:
                ma20 = daily_agg['CLOSE'].rolling(window=20).mean()
                std20 = daily_agg['CLOSE'].rolling(window=20).std()
                upper_band = ma20 + (std20 * 2)
                lower_band = ma20 - (std20 * 2)
                
                current_price = daily_agg['CLOSE'].iloc[-1]
                current_upper = upper_band.iloc[-1]
                current_lower = lower_band.iloc[-1]
                
                st.metric("Bollinger Yuqori", f"${current_upper:.2f}")
                st.metric("Bollinger Pastki", f"${current_lower:.2f}")
                
                if current_price > current_upper:
                    st.error("🔴 Yuqori band ustida")
                elif current_price < current_lower:
                    st.success("🟢 Pastki band ostida")
                else:
                    st.info("🟡 Bandlar orasida")
        
        with col3:
            # Volume analysis
            avg_volume = daily_agg['G38'].mean()
            current_volume = daily_agg['G38'].iloc[-1]
            volume_ratio = current_volume / avg_volume
            
            st.metric("O'rtacha hajm", f"{avg_volume:.0f}")
            st.metric("Joriy hajm", f"{current_volume:.0f}")
            st.metric("Hajm nisbati", f"{volume_ratio:.1f}x")
            
            if volume_ratio > 1.5:
                st.success("🟢 Yuqori hajm")
            elif volume_ratio < 0.5:
                st.warning("🟡 Past hajm")
            else:
                st.info("🔵 Normal hajm")
        
        # Price levels table
        st.subheader("📊 Narx Darajalari")
        price_levels = pd.DataFrame({
            'Daraja': ['Joriy narx', 'Bugungi maksimum', 'Bugungi minimum', 'MA20', 'MA50'],
            'Qiymat': [
                f"${current_price:.2f}",
                f"${daily_agg['HIGH'].iloc[-1]:.2f}",
                f"${daily_agg['LOW'].iloc[-1]:.2f}",
                f"${daily_agg['MA20'].iloc[-1]:.2f}" if 'MA20' in daily_agg.columns else "N/A",
                f"${daily_agg['MA50'].iloc[-1]:.2f}" if 'MA50' in daily_agg.columns else "N/A"
            ]
        })
        st.dataframe(price_levels, use_container_width=True)
        
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
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi")

# YIELD CURVES BO'LIMI
elif selected_section == "YIELD CURVES":
    st.markdown('<div class="section-header">📈 YIELD CURVES - Narx Egri Chiziqlari Tahlili</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
        # Ma'lumot haqida qisqacha info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            max_price = filtered_df['PRICE'].max()
            st.metric("Maksimal narx", f"${max_price:.2f}", "🟢")
        with col2:
            avg_price = filtered_df['PRICE'].mean()
            st.metric("O'rtacha narx", f"${avg_price:.2f}", "🟡")
        with col3:
            min_price = filtered_df['PRICE'].min()
            st.metric("Minimal narx", f"${min_price:.2f}", "🔵")
        with col4:
            price_range = max_price - min_price
            st.metric("Narx diapazoni", f"${price_range:.2f}")
        
        # Vaqt davrlari bo'yicha ma'lumotlarni tayyorlash
        periods = ['1M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y']
        
        # Uch xil sana uchun ma'lumot yaratish
        end_date = filtered_df['INSTIME'].max()
        dates = [
            end_date,
            end_date - timedelta(days=30),
            end_date - timedelta(days=365)
        ]
        
        fig = go.Figure()
        
        # Har bir sana uchun yield curve yaratish
        colors = ['#00ff00', '#ffa500', '#00bfff']  # Yashil, Sariq, Ko'k
        curve_names = ['Maksimal', 'O\'rtacha', 'Minimal']
        
        for i, (date, color, name) in enumerate(zip(dates, colors, curve_names)):
            # Har bir period uchun narxlarni hisoblash
            if name == 'Maksimal':
                base_price = max_price
                multipliers = [0.95, 0.96, 0.97, 0.98, 0.99, 1.0, 1.01, 1.02, 1.03, 1.04]
            elif name == 'O\'rtacha':
                base_price = avg_price
                multipliers = [0.98, 0.99, 0.995, 1.0, 1.005, 1.01, 1.015, 1.02, 1.025, 1.03]
            else:  # Minimal
                base_price = min_price
                multipliers = [1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97, 0.96]
            
            prices = [base_price * mult for mult in multipliers]
            
            fig.add_trace(go.Scatter(
                x=periods,
                y=prices,
                mode='lines+markers',
                name=f'{name} - {date.strftime("%b %d, %Y")}',
                line=dict(color=color, width=3),
                marker=dict(size=8, color=color)
            ))
        
        # Layout sozlamalari
        fig.update_layout(
            title={
                'text': "Narx Egri Chiziqlari - Vaqt Davrlari Bo'yicha Tahlil",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'color': 'white', 'size': 18}
            },
            height=600,
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font=dict(color='white', size=12),
            xaxis=dict(
                title="Vaqt Davri",
                showgrid=True,
                gridcolor='#333',
                color='white'
            ),
            yaxis=dict(
                title="Narx ($)",
                showgrid=True,
                gridcolor='#333',
                color='white',
                tickformat='$,.2f'
            ),
            legend=dict(
                bgcolor='rgba(0,0,0,0.5)',
                font=dict(color='white')
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Excel yuklab olish buttoni
        st.markdown("---")
        excel_data = create_excel_download(filtered_df, "YIELD_CURVES")
        if excel_data:
            st.download_button(
                label="📊 Excel formatda yuklab olish",
                data=excel_data,
                file_name=f"yield_curves_tahlil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi")

# GRAFIK BO'LIMI
elif selected_section == "GRAFIK":
    st.markdown('<div class="section-header">📈 GRAFIK - Vaqt bo\'yicha narx monitoring</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
        # Vaqt bo'yicha saralash
        filtered_df_sorted = filtered_df.sort_values('INSTIME')
        
        fig = go.Figure()
        
        # Real narxlar
        fig.add_trace(go.Scatter(
            x=filtered_df_sorted['INSTIME'],
            y=filtered_df_sorted['PRICE'],
            mode='markers+lines',
            name='Real narxlar',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        
        # Statistik chiziqlar
        max_price = filtered_df['PRICE'].max()
        min_price = filtered_df['PRICE'].min()
        mean_price = filtered_df['PRICE'].mean()
        
        # Eng yuqori narx
        fig.add_hline(y=max_price, line_dash="dash", line_color="green", 
                     annotation_text=f"Eng yuqori: ${max_price:.2f}")
        
        # Eng past narx
        fig.add_hline(y=min_price, line_dash="dash", line_color="red",
                     annotation_text=f"Eng past: ${min_price:.2f}")
        
        # O'rtacha narx
        fig.add_hline(y=mean_price, line_dash="dash", line_color="orange",
                     annotation_text=f"O'rtacha: ${mean_price:.2f}")
        
        fig.update_layout(
            title="Bojxona qiymatlari vaqt bo'yicha",
            xaxis_title="Vaqt",
            yaxis_title="Narx ($)",
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
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi")

# USTUNLI DIAGRAMMA BO'LIMI
elif selected_section == "USTUNLI DIAGRAMMA":
    st.markdown('<div class="section-header">📊 USTUNLI DIAGRAMMA - HS kodlar bo\'yicha o\'rtacha narx</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
        # HS kodlar bo'yicha o'rtacha narx
        hs_price_avg = filtered_df.groupby('G33')['PRICE'].mean().reset_index()
        hs_price_avg = hs_price_avg.sort_values('PRICE', ascending=False)
        
        fig = px.bar(
            hs_price_avg,
            x='G33',
            y='PRICE',
            title="HS kodlar bo'yicha o'rtacha bojxona qiymati",
            labels={'G33': 'HS Kod', 'PRICE': 'O\'rtacha narx ($)'},
            color='PRICE',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            height=600,
            yaxis=dict(tickformat='$,.2f')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Jadval ko'rinishi
        st.subheader("📋 Batafsil ma'lumot")
        st.dataframe(hs_price_avg.round(2))
        
        # Excel yuklab olish buttoni
        st.markdown("---")
        excel_data = create_excel_download(filtered_df, "USTUNLI_DIAGRAMMA")
        if excel_data:
            st.download_button(
                label="📊 Excel formatda yuklab olish",
                data=excel_data,
                file_name=f"ustunli_diagramma_tahlil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi")

# HISTOGRAM BO'LIMI
elif selected_section == "HISTOGRAM":
    st.markdown('<div class="section-header">📉 HISTOGRAM - Narx taqsimoti</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
        fig = px.histogram(
            filtered_df,
            x='PRICE',
            nbins=30,
            title="Bojxona qiymatlarining taqsimoti",
            labels={'PRICE': 'Narx ($)', 'count': 'Soni'},
            color_discrete_sequence=['#1f77b4']
        )
        
        # Statistik ma'lumotlar qo'shish
        fig.add_vline(x=filtered_df['PRICE'].mean(), line_dash="dash", line_color="red",
                     annotation_text=f"O'rtacha: ${filtered_df['PRICE'].mean():.2f}")
        fig.add_vline(x=filtered_df['PRICE'].median(), line_dash="dash", line_color="green",
                     annotation_text=f"Mediana: ${filtered_df['PRICE'].median():.2f}")
        
        fig.update_layout(
            height=600,
            xaxis=dict(tickformat='$,.2f')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistik ma'lumotlar
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Standart og'ish", f"${filtered_df['PRICE'].std():.2f}")
        with col2:
            st.metric("Mediana", f"${filtered_df['PRICE'].median():.2f}")
        with col3:
            st.metric("Mod", f"${filtered_df['PRICE'].mode().iloc[0]:.2f}" if not filtered_df['PRICE'].mode().empty else "N/A")
        
        # Excel yuklab olish buttoni
        st.markdown("---")
        excel_data = create_excel_download(filtered_df, "HISTOGRAM")
        if excel_data:
            st.download_button(
                label="📊 Excel formatda yuklab olish",
                data=excel_data,
                file_name=f"histogram_tahlil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi")

# SUNBURST BO'LIMI
elif selected_section == "SUNBURST":
    st.markdown('<div class="section-header">🌍 SUNBURST - Davlat va HS kodlar bo\'yicha ulush</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
        # Davlat va HS kodlar bo'yicha yig'indi qiymat
        sunburst_data = filtered_df.groupby(['G34', 'G33'])['PRICE'].sum().reset_index()
        
        fig = px.sunburst(
            sunburst_data,
            path=['G34', 'G33'],
            values='PRICE',
            title="Davlat va HS kodlar bo'yicha bojxona qiymatlari ulushi"
        )
        
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
        
        # Treemap alternativasi
        st.subheader("📦 Treemap ko'rinishi")
        fig2 = px.treemap(
            sunburst_data,
            path=['G34', 'G33'],
            values='PRICE',
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
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi")

# TIME GROUP BO'LIMI
elif selected_section == "TIME GROUP":
    st.markdown('<div class="section-header">🕒 TIME GROUP - Vaqtga asoslangan analiz</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0:
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
            'PRICE': ['mean', 'count', 'sum', 'min', 'max']
        }).round(2)
        
        time_stats.columns = ['O\'rtacha narx', 'Soni', 'Jami qiymat', 'Min narx', 'Max narx']
        time_stats = time_stats.reset_index()
        
        # Chiziqli grafik
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("O'rtacha narx o'zgarishi", "Rasmiylashtirish soni"),
            vertical_spacing=0.1
        )
        
        # O'rtacha narx
        fig.add_trace(
            go.Scatter(
                x=time_stats['time_group'],
                y=time_stats['O\'rtacha narx'],
                mode='lines+markers',
                name='O\'rtacha narx',
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
        fig.update_yaxes(title_text="Narx ($)", tickformat='$,.2f', row=1, col=1)
        fig.update_yaxes(title_text="Soni", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Jadval
        st.subheader("📊 Vaqt bo'yicha statistika")
        st.dataframe(time_stats)
        
        # Trend tahlili
        if len(time_stats) > 1:
            price_trend = time_stats['O\'rtacha narx'].iloc[-1] - time_stats['O\'rtacha narx'].iloc[0]
            count_trend = time_stats['Soni'].iloc[-1] - time_stats['Soni'].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                trend_color = "green" if price_trend > 0 else "red"
                st.markdown(f"**Narx trendi:** <span style='color:{trend_color}'>{price_trend:+.2f}$</span>", unsafe_allow_html=True)
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
        st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi")

# Import Analytics Dashboard footer
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Customs Value Analytics**")
st.sidebar.markdown("Tashkent, 2025")
st.sidebar.markdown("Real vaqtda monitoring va tahlil")