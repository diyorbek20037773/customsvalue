import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Sahifa konfiguratsiyasi - dastur sozlamalari
st.set_page_config(
    page_title="Customs Value Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stillar - interfeys dizayni
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
    
    /* Sidebar tugmalari uchun effekt */
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
    
    /* Filtr konteynerlar */
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

# Ma'lumotlarni yuklash funksiyasi - fayl o'qish va tayyorlash
@st.cache_data
def load_data(file):
    """Fayl yuklash va ma'lumotlarni tayyorlash"""
    try:
        # Fayl turini aniqlash va o'qish
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Sana ustunini to'g'ri formatga o'girish
        if 'С графа' in df.columns:
            # Turli sana formatlarini sinab ko'rish
            df['С графа'] = pd.to_datetime(df['С графа'], errors='coerce', dayfirst=True)
        
        # Raqamli ustunlarni tekshirish va o'girish
        if 'За.ед. из.$' in df.columns:
            # Agar string bo'lsa, raqamga o'girish
            df['За.ед. из.$'] = pd.to_numeric(df['За.ед. из.$'], errors='coerce')
        
        if 'Нетто' in df.columns:
            df['Нетто'] = pd.to_numeric(df['Нетто'], errors='coerce')
        
        # Jami bojxona qiymatini hisoblash (Birlik narx * Og'irlik)
        if 'За.ед. из.$' in df.columns and 'Нетто' in df.columns:
            df['Bojxona_Qiymati'] = df['За.ед. из.$'] * df['Нетто']
        
        # Country code'larni string'ga o'girish
        if '31-Страна происхождения' in df.columns:
            df['31-Страна происхождения'] = df['31-Страна происхождения'].astype(str)
        
        if 'ТИФ ТН КОДИ' in df.columns:
            df['ТИФ ТН КОДИ'] = df['ТИФ ТН КОДИ'].astype(str)
        
        # Bo'sh qiymatlarni tozalash
        required_columns = ['Страна отправления', '31-Страна происхождения', 'ТИФ ТН КОДИ', 'С графа']
        existing_required = [col for col in required_columns if col in df.columns]
        if existing_required:
            df = df.dropna(subset=existing_required)
        
        return df
    except Exception as e:
        st.error(f"Fayl yuklashda xatolik: {str(e)}")
        return None

# O'rtacha qiymat hisoblagich funksiyasi
def calculate_weighted_average_price(df):
    """Bojxona qiymatining o'rtacha qiymatini hisoblash"""
    if 'Bojxona_Qiymati' in df.columns and 'Нетто' in df.columns:
        total_value = df['Bojxona_Qiymati'].sum()  # Jami qiymat
        total_weight = df['Нетто'].sum()  # Jami og'irlik
        
        if total_weight > 0:
            # Formula: SUMM(bojxona qiymati) / SUMM(og'irlik)
            weighted_avg = total_value / total_weight
            return weighted_avg
        else:
            return 0
    else:
        return 0

# Excel yuklab olish funksiyasi - tahlil natijalarini Excel formatda saqlash
@st.cache_data
def create_excel_download(df, section_name):
    """Tahlil qilingan ma'lumotlarni Excel formatda tayyorlash"""
    try:
        from io import BytesIO
        
        # BytesIO buffer yaratish
        output = BytesIO()
        
        # Excel writer yaratish
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Asosiy ma'lumotlar varaqasi
            df.to_excel(writer, sheet_name='Asosiy_Malumotlar', index=False)
            
            # Statistikalar varaqasi
            if 'За.ед. из.$' in df.columns:
                avg_price = calculate_weighted_average_price(df)
                stats_df = pd.DataFrame({
                    'Ko\'rsatkich': [
                        'Jami yozuvlar', 
                        'O\'rtacha qiymat', 
                        'Maksimal birlik narx', 
                        'Minimal birlik narx', 
                        'Jami og\'irlik',
                        'Jami bojxona qiymati'
                    ],
                    'Qiymat': [
                        len(df),
                        f"${avg_price:.2f}/kg" if avg_price > 0 else "N/A",
                        f"${df['За.ед. из.$'].max():.2f}/kg" if df['За.ед. из.$'].notna().any() else "N/A",
                        f"${df['За.ед. из.$'].min():.2f}/kg" if df['За.ед. из.$'].notna().any() else "N/A",
                        f"{df['Нетто'].sum():.2f} kg" if 'Нетто' in df.columns and df['Нетто'].notna().any() else "N/A",
                        f"${df['Bojxona_Qiymati'].sum():.2f}" if 'Bojxona_Qiymati' in df.columns else "N/A"
                    ]
                })
                stats_df.to_excel(writer, sheet_name='Statistikalar', index=False)
            
            # Davlatlar bo'yicha tahlil
            if '31-Страна происхождения' in df.columns and 'За.ед. из.$' in df.columns:
                country_analysis = df.groupby('31-Страна происхождения').agg({
                    'За.ед. из.$': 'count',
                    'Нетто': 'sum' if 'Нетто' in df.columns else 'count',
                    'Bojxona_Qiymati': 'sum' if 'Bojxona_Qiymati' in df.columns else 'count'
                }).round(2)
                country_analysis.columns = ['Import_Soni', 'Jami_Ogirlik', 'Jami_Bojxona_Qiymati']
                country_analysis.to_excel(writer, sheet_name='Davlatlar_Tahlili')
            
            # HS kodlar bo'yicha tahlil
            if 'ТИФ ТН КОДИ' in df.columns and 'За.ед. из.$' in df.columns:
                hs_analysis = df.groupby('ТИФ ТН КОДИ').agg({
                    'За.ед. из.$': 'count',
                    'Нетто': 'sum' if 'Нетто' in df.columns else 'count',
                    'Bojxona_Qiymati': 'sum' if 'Bojxona_Qiymati' in df.columns else 'count'
                }).round(2)
                hs_analysis.columns = ['Import_Soni', 'Jami_Ogirlik', 'Jami_Bojxona_Qiymati']
                hs_analysis.to_excel(writer, sheet_name='HS_Kodlar_Tahlili')
        
        # Buffer'ni qayta o'qish uchun boshiga o'tkazish
        output.seek(0)
        return output.getvalue()
    
    except Exception as e:
        st.error(f"Excel fayl yaratishda xatolik: {str(e)}")
        return None

# Demo ma'lumotlar yaratish funksiyasi - test uchun
def create_demo_data():
    """Test uchun demo ma'lumotlar yaratish"""
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Real country codes va names
    countries_dispatch = ['ГЕРМАНИЯ', 'КИТАЙ', 'ТУРЦИЯ', 'РОССИЯ', 'КОРЕЯ', 'ЯПОНИЯ', 'ИНДИЯ', 'США']
    countries_origin_codes = [276, 156, 792, 643, 410, 392, 356, 840]  # ISO country codes
    hs_codes = [8517120000, 8471300000, 8473301100, 8528591000, 8544421000, 
                8536500000, 8537109000, 8542310000]
    methods = ['1-metod', '2-metod', '3-metod', '4-metod', '5-metod', '6-metod']
    
    data = []
    for _ in range(1000):
        date = np.random.choice(dates)
        country_dispatch = np.random.choice(countries_dispatch)
        country_origin = np.random.choice(countries_origin_codes)
        hs_code = np.random.choice(hs_codes)
        method = np.random.choice(methods)
        
        # Realistik ma'lumotlar
        weight = np.random.uniform(10, 1000)  # kg
        unit_price = np.random.uniform(1, 50)  # $ per kg
        
        data.append({
            'Страна отправления': country_dispatch,
            '31-Страна происхождения': country_origin,
            'ТИФ ТН КОДИ': hs_code,
            'За.ед. из.$': unit_price,
            'Нетто': weight,
            'metod': method,
            'С графа': date
        })
    
    df = pd.DataFrame(data)
    # Bojxona qiymatini hisoblash
    df['Bojxona_Qiymati'] = df['За.ед. из.$'] * df['Нетто']
    return df

# Progressive filtering funksiyasi - filtrlarni ketma-ket qo'llash
def get_available_options(df, column, selected_filters):
    """Selected filtrlar asosida mavjud bo'lgan optionlarni qaytaradi"""
    if df is None or len(df) == 0:
        return ['Hammasi']
    
    # Oldingi filtrlarni qo'llash
    filtered_df = df.copy()
    
    for filter_col, filter_val in selected_filters.items():
        if filter_val != 'Hammasi' and filter_col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[filter_col] == filter_val]
    
    if column in filtered_df.columns:
        unique_values = sorted(filtered_df[column].dropna().unique().tolist())
        return ['Hammasi'] + [str(x) for x in unique_values]
    else:
        return ['Hammasi']

# Header va logo - sahifa yuqori qismi
col1, col2, col3 = st.columns([2, 3, 1])

with col1:
    st.markdown("")  # Bo'sh joy

with col2:
    st.markdown('<div class="main-header">📊 Customs Value Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #666; margin-top: -0.5rem;">Bojxona auditi boshqarmasi</div>', unsafe_allow_html=True)

with col3:
    # Bojxona logosi
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

# Sidebar - TAHLIL TURLARI
st.sidebar.header("📊 TAHLIL TURLARI")
st.sidebar.markdown("---")

# Session state uchun sahifa holati
if 'selected_section' not in st.session_state:
    st.session_state.selected_section = "CANDLESTICK"

# Sidebar tugmalari - tahlil turlarini tanlash
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

# Fayl yuklash maydoni
uploaded_file = st.file_uploader(
    "Faylni yuklash:",
    type=['csv', 'xlsx', 'xls'],
    help="Kerakli ustunlar: Страна отправления, 31-Страна происхождения, ТИФ ТН КОДИ, За.ед. из.$, Нетто, metod, С графа",
    key="main_file_uploader"
)

# Ma'lumotlarni olish (yuklangan fayl yoki demo)
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

# Session state uchun filtrlar - har bir filtr uchun holatni saqlash
filter_keys = ['15-GRAFA', '34-GRAFA', '33-GRAFA', 'METOD']
for key in filter_keys:
    if f'filter_{key}' not in st.session_state:
        st.session_state[f'filter_{key}'] = 'Hammasi'

# Progressive filtrlar (birinchi 4 ta filtr)
col1, col2, col3, col4 = st.columns(4)

# 1. 15-GRAFA (Jonatilgan mamlakat)
with col1:
    current_filters = {}
    dispatch_countries = get_available_options(df, 'Страна отправления', current_filters)
    selected_dispatch = st.selectbox(
        "15-GRAFA",
        dispatch_countries,
        key="dispatch_filter",
        help="Tovar jonatilgan mamlakat"
    )
    st.session_state['filter_15-GRAFA'] = selected_dispatch

# 2. 34-GRAFA (Ishlab chiqarilgan mamlakat)
with col2:
    current_filters = {'Страна отправления': selected_dispatch}
    origin_countries = get_available_options(df, '31-Страна происхождения', current_filters)
    selected_origin = st.selectbox(
        "34-GRAFA",
        origin_countries,
        key="origin_filter", 
        help="Tovar ishlab chiqarilgan mamlakat"
    )
    st.session_state['filter_34-GRAFA'] = selected_origin

# 3. 33-GRAFA (HS kodi)
with col3:
    current_filters = {
        'Страна отправления': selected_dispatch,
        '31-Страна происхождения': selected_origin
    }
    hs_codes = get_available_options(df, 'ТИФ ТН КОДИ', current_filters)
    selected_hs = st.selectbox(
        "33-GRAFA",
        hs_codes,
        key="hs_filter",
        help="Tovar HS kodi"
    )
    st.session_state['filter_33-GRAFA'] = selected_hs

# 4. METOD (Qiymat aniqlash metodi)
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

st.markdown('</div>', unsafe_allow_html=True)

# VAQT FILTRLAR - 2 ta alohida sana filtri
st.markdown("### 📅 VAQT FILTRLARI")
st.markdown('<div class="filter-container">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Sana filtrlar uchun default qiymatlar
default_start_date = datetime.now() - timedelta(days=365)  # 1 yil oldin
default_end_date = datetime.now()  # Bugun

with col1:
    # "DAN" sana filtri
    start_date = st.date_input(
        "DAN",
        value=default_start_date,
        help="Boshlanish sanasi (dd.mm.yyyy)",
        key="start_date_filter"
    )

with col2:
    # "GACHA" sana filtri  
    end_date = st.date_input(
        "GACHA",
        value=default_end_date,
        help="Tugash sanasi (dd.mm.yyyy)",
        key="end_date_filter"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Ma'lumotlarni filtrlash - barcha filtrlarni ketma-ket qo'llash
filtered_df = df.copy()

# Asosiy filtrlar
if selected_dispatch != 'Hammasi':
    filtered_df = filtered_df[filtered_df['Страна отправления'] == selected_dispatch]

if selected_origin != 'Hammasi':
    filtered_df = filtered_df[filtered_df['31-Страна происхождения'].astype(str) == str(selected_origin)]

if selected_hs != 'Hammasi':
    filtered_df = filtered_df[filtered_df['ТИФ ТН КОДИ'].astype(str) == str(selected_hs)]

if selected_method != 'Hammasi':
    filtered_df = filtered_df[filtered_df['metod'] == selected_method]

# Vaqt filtri - start_date dan end_date gacha
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date) + timedelta(days=1)  # Kun oxirigacha

filtered_df = filtered_df[
    (filtered_df['С графа'] >= start_datetime) & 
    (filtered_df['С графа'] < end_datetime)
]

st.markdown("---")

# Asosiy ko'rsatkichlar - weighted average formula bilan
if len(filtered_df) > 0:
    average_price = calculate_weighted_average_price(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jami yozuvlar", f"{len(filtered_df):,}")
    with col2:
        st.metric("O'RTACHA QIYMAT", f"${average_price:.2f}/kg")
    with col3:
        if 'Нетто' in filtered_df.columns:
            total_weight = filtered_df['Нетто'].sum()
            st.metric("Jami og'irlik", f"{total_weight:,.0f} kg")
        else:
            st.metric("Jami og'irlik", "N/A")
    with col4:
        if 'Bojxona_Qiymati' in filtered_df.columns:
            total_value = filtered_df['Bojxona_Qiymati'].sum()
            st.metric("Jami bojxona qiymati", f"${total_value:,.0f}")
        else:
            st.metric("Jami bojxona qiymati", "N/A")
else:
    st.warning("Tanlangan filtrlar bo'yicha ma'lumot topilmadi!")

# CANDLESTICK BO'LIMI - moliyaviy grafiklar
if selected_section == "CANDLESTICK":
    st.markdown('<div class="section-header">🕯️ CANDLESTICK - Professional Bojxona Qiymatlari Tahlili</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'За.ед. из.$' in filtered_df.columns and 'С графа' in filtered_df.columns:
        # Qisqacha ma'lumot ko'rsatkichlari
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            current_price = filtered_df['За.ед. из.$'].iloc[-1]
            st.metric("Joriy birlik narx", f"${current_price:.2f}/kg")
        with col2:
            price_change = filtered_df['За.ед. из.$'].iloc[-1] - filtered_df['За.ед. из.$'].iloc[-2] if len(filtered_df) > 1 else 0
            st.metric("O'zgarish", f"${price_change:.2f}", f"{price_change:.2f}")
        with col3:
            if 'Нетто' in filtered_df.columns:
                st.metric("Jami hajm", f"{filtered_df['Нетто'].sum():.0f} kg")
            else:
                st.metric("Jami hajm", "N/A")
        with col4:
            st.metric("Maksimal narx", f"${filtered_df['За.ед. из.$'].max():.2f}/kg")
        with col5:
            st.metric("Minimal narx", f"${filtered_df['За.ед. из.$'].min():.2f}/kg")
        
        # Kunlik ma'lumotlarni agregatsiya qilish - TO'G'RI KETMA-KETLIK BILAN
        filtered_df_sorted = filtered_df.sort_values('С графа')
        daily_groups = filtered_df_sorted.groupby(filtered_df_sorted['С графа'].dt.date)
        
        daily_data = []
        prev_close = None
        
        # Har bir kun uchun OHLC (Open, High, Low, Close) ma'lumotlarini yaratish
        for date, group in daily_groups:
            group_sorted = group.sort_values('С графа')
            
            # Agar oldingi kun mavjud bo'lsa, uning close qiymatidan boshlaymiz
            if prev_close is not None:
                open_price = prev_close
            else:
                open_price = group_sorted['За.ед. из.$'].iloc[0]
            
            high_price = group_sorted['За.ед. из.$'].max()  # Kunlik maksimum
            low_price = group_sorted['За.ед. из.$'].min()   # Kunlik minimum
            close_price = group_sorted['За.ед. из.$'].iloc[-1]  # Kunlik yopilish
            volume = group_sorted['Нетто'].sum() if 'Нетто' in group_sorted.columns else len(group_sorted)
            
            daily_data.append({
                'Date': pd.to_datetime(date),
                'OPEN': open_price,
                'HIGH': high_price,
                'LOW': low_price,
                'CLOSE': close_price,
                'Volume': volume
            })
            
            # Keyingi kun uchun close qiymatini saqlash
            prev_close = close_price
        
        daily_agg = pd.DataFrame(daily_data)
        daily_agg = daily_agg.sort_values('Date')
        
        if len(daily_agg) > 0:
            # Professional Candlestick Chart yaratish
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                row_heights=[0.7, 0.3],
                subplot_titles=('Bojxona Birlik Narxlari (OHLC)', 'Kunlik Hajm')
            )
            
            # Candlestick chart qo'shish
            fig.add_trace(
                go.Candlestick(
                    x=daily_agg['Date'],
                    open=daily_agg['OPEN'],
                    high=daily_agg['HIGH'],
                    low=daily_agg['LOW'],
                    close=daily_agg['CLOSE'],
                    name="OHLC",
                    increasing_line_color='#00ff00',  # Yashil - narx oshgan
                    decreasing_line_color='#ff0000',  # Qizil - narx tushgan
                    increasing_fillcolor='rgba(0,255,0,0.7)',
                    decreasing_fillcolor='rgba(255,0,0,0.7)'
                ),
                row=1, col=1
            )
            
            # Moving averages qo'shish (20 kunlik o'rtacha)
            if len(daily_agg) >= 20:
                daily_agg['MA20'] = daily_agg['CLOSE'].rolling(window=20).mean()
                fig.add_trace(
                    go.Scatter(
                        x=daily_agg['Date'],
                        y=daily_agg['MA20'],
                        mode='lines',
                        name='MA20',
                        line=dict(color='blue', width=1)
                    ),
                    row=1, col=1
                )
            
            # Volume bars qo'shish
            colors = ['green' if daily_agg['CLOSE'].iloc[i] >= daily_agg['OPEN'].iloc[i] else 'red' 
                      for i in range(len(daily_agg))]
            
            fig.add_trace(
                go.Bar(
                    x=daily_agg['Date'],
                    y=daily_agg['Volume'],
                    name="Hajm (kg)",
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            # Layout sozlamalari
            fig.update_layout(
                title={
                    'text': f"Bojxona Birlik Narxlari Professional Tahlil - Joriy: ${current_price:.2f}/kg",
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
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333', zeroline=False, color='white', title_text="Narx ($/kg)", tickformat='$,.2f', row=1, col=1)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333', zeroline=False, color='white', title_text="Hajm (kg)", tickformat=',.0f', row=2, col=1)
            
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

# GRAFIK BO'LIMI - chiziqli grafiklar
elif selected_section == "GRAFIK":
    st.markdown('<div class="section-header">📈 GRAFIK - Vaqt bo\'yicha birlik narx monitoring</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'За.ед. из.$' in filtered_df.columns and 'С графа' in filtered_df.columns:
        # Vaqt bo'yicha saralash
        filtered_df_sorted = filtered_df.sort_values('С графа')
        
        fig = go.Figure()
        
        # Real narxlar chiziq grafigi
        fig.add_trace(go.Scatter(
            x=filtered_df_sorted['С графа'],
            y=filtered_df_sorted['За.ед. из.$'],
            mode='markers+lines',
            name='Birlik narxlar',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        
        # Statistik chiziqlar qo'shish
        max_price = filtered_df['За.ед. из.$'].max()
        min_price = filtered_df['За.ед. из.$'].min()
        average_price = calculate_weighted_average_price(filtered_df)
        
        # Maksimal qiymat chizig'i
        fig.add_hline(y=max_price, line_dash="dash", line_color="green", 
                     annotation_text=f"Maksimal: ${max_price:.2f}/kg")
        
        # Minimal qiymat chizig'i
        fig.add_hline(y=min_price, line_dash="dash", line_color="red",
                     annotation_text=f"Minimal: ${min_price:.2f}/kg")
        
        # O'rtacha qiymat chizig'i
        fig.add_hline(y=average_price, line_dash="dash", line_color="blue",
                     annotation_text=f"O'rtacha qiymat: ${average_price:.2f}/kg")
        
        fig.update_layout(
            title="Bojxona birlik narxlari vaqt bo'yicha",
            xaxis_title="Sana",
            yaxis_title="Birlik narx ($/kg)",
            height=600,
            showlegend=True,
            yaxis=dict(tickformat='$,.2f')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Excel yuklab olish
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

# SUNBURST BO'LIMI - doira shaklida ulush diagrammasi
elif selected_section == "SUNBURST":
    st.markdown('<div class="section-header">🌍 SUNBURST - Davlat va HS kodlar bo\'yicha ulush</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'Bojxona_Qiymati' in filtered_df.columns and '31-Страна происхождения' in filtered_df.columns:
        # Davlat va HS kodlar bo'yicha jami qiymatni guruhlash
        sunburst_data = filtered_df.groupby(['31-Страна происхождения', 'ТИФ ТН КОДИ'])['Bojxona_Qiymati'].sum().reset_index()
        
        # Sunburst diagramma
        fig = px.sunburst(
            sunburst_data,
            path=['31-Страна происхождения', 'ТИФ ТН КОДИ'],
            values='Bojxona_Qiymati',
            title="Davlat va HS kodlar bo'yicha bojxona qiymati ulushi"
        )
        
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
        
        # Treemap alternativasi
        st.subheader("📦 Treemap ko'rinishi")
        fig2 = px.treemap(
            sunburst_data,
            path=['31-Страна происхождения', 'ТИФ ТН КОДИ'],
            values='Bojxona_Qiymati',
            title="Treemap - Davlat va HS kodlar bo'yicha ulush"
        )
        fig2.update_layout(height=600)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Excel yuklab olish
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

# TIME GROUP BO'LIMI - vaqt bo'yicha guruhlangan tahlil
elif selected_section == "TIME GROUP":
    st.markdown('<div class="section-header">🕒 TIME GROUP - Vaqtga asoslangan analiz</div>', unsafe_allow_html=True)
    
    if len(filtered_df) > 0 and 'За.ед. из.$' in filtered_df.columns and 'С графа' in filtered_df.columns:
        # Vaqt gruppalarini tanlash
        time_group = st.selectbox("Vaqt guruhi", ["Kunlik", "Haftalik", "Oylik"])
        
        # Vaqt gruppalarini yaratish
        if time_group == "Kunlik":
            filtered_df['time_group'] = filtered_df['С графа'].dt.date
        elif time_group == "Haftalik":
            filtered_df['time_group'] = filtered_df['С графа'].dt.to_period('W').dt.start_time
        else:  # Oylik
            filtered_df['time_group'] = filtered_df['С графа'].dt.to_period('M').dt.start_time
        
        # Vaqt bo'yicha statistikalarni hisoblash
        time_stats = filtered_df.groupby('time_group').agg({
            'За.ед. из.$': ['count', 'min', 'max'],
            'Нетто': 'sum',
            'Bojxona_Qiymati': 'sum' if 'Bojxona_Qiymati' in filtered_df.columns else 'count'
        }).round(2)
        
        time_stats.columns = ['Rasmiylashtirishlar_Soni', 'Min_Birlik_Narx', 'Max_Birlik_Narx', 'Jami_Ogirlik', 'Jami_Bojxona_Qiymati']
        time_stats = time_stats.reset_index()
        
        # Har bir vaqt davri uchun o'rtacha qiymat hisoblash
        average_prices = []
        for _, group in filtered_df.groupby('time_group'):
            avg_price = calculate_weighted_average_price(group)
            average_prices.append(avg_price)
        
        time_stats['Ortacha_Qiymat'] = average_prices
        
        # 3 qatorli grafik yaratish
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=("O'rtacha qiymat o'zgarishi", "Rasmiylashtirish soni", "Jami bojxona qiymati"),
            vertical_spacing=0.08
        )
        
        # 1. O'rtacha qiymat
        fig.add_trace(
            go.Scatter(
                x=time_stats['time_group'],
                y=time_stats['Ortacha_Qiymat'],
                mode='lines+markers',
                name='O\'rtacha qiymat',
                line=dict(color='blue', width=3)
            ),
            row=1, col=1
        )
        
        # 2. Rasmiylashtirish soni
        fig.add_trace(
            go.Bar(
                x=time_stats['time_group'],
                y=time_stats['Rasmiylashtirishlar_Soni'],
                name='Rasmiylashtirish soni',
                marker_color='lightblue'
            ),
            row=2, col=1
        )
        
        # 3. Jami bojxona qiymati
        fig.add_trace(
            go.Bar(
                x=time_stats['time_group'],
                y=time_stats['Jami_Bojxona_Qiymati'],
                name='Jami bojxona qiymati',
                marker_color='lightgreen'
            ),
            row=3, col=1
        )
        
        fig.update_layout(height=900, showlegend=True)
        fig.update_xaxes(title_text="Vaqt", row=3, col=1)
        fig.update_yaxes(title_text="O'rtacha qiymat ($/kg)", tickformat='$,.2f', row=1, col=1)
        fig.update_yaxes(title_text="Soni", row=2, col=1)
        fig.update_yaxes(title_text="Qiymat ($)", tickformat='$,.0f', row=3, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Jadval ko'rsatish
        st.subheader("📊 Vaqt bo'yicha batafsil statistika")
        st.dataframe(time_stats, use_container_width=True)
        
        # Trend tahlili
        if len(time_stats) > 1:
            price_trend = time_stats['Ortacha_Qiymat'].iloc[-1] - time_stats['Ortacha_Qiymat'].iloc[0]
            count_trend = time_stats['Rasmiylashtirishlar_Soni'].iloc[-1] - time_stats['Rasmiylashtirishlar_Soni'].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                trend_color = "green" if price_trend > 0 else "red"
                st.markdown(f"**O'rtacha qiymat trendi:** <span style='color:{trend_color}'>{price_trend:+.2f}$/kg</span>", unsafe_allow_html=True)
            with col2:
                trend_color = "green" if count_trend > 0 else "red"
                st.markdown(f"**Import hajmi trendi:** <span style='color:{trend_color}'>{count_trend:+}</span>", unsafe_allow_html=True)
        
        # Excel yuklab olish
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

# Sahifa pastki qismi - dastur ma'lumotlari
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Customs Value Analytics**")
st.sidebar.markdown("Tashkent, 2025")
st.sidebar.markdown("Real vaqtda monitoring va tahlil")
