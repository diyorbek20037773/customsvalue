# 📊 Customs Value Analytics

**Professional Bojxona Qiymatlari Tahlil Tizimi**

Real-time bojxona ma'lumotlarini visualization qilish va tahlil qilish uchun mo'ljallangan professional dashboard.

![Dashboard Preview](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Customs+Value+Analytics+Dashboard)

## 🚀 **Asosiy Imkoniyatlar**

### 📈 **4 xil Professional Tahlil:**
- **🕯️ CANDLESTICK** - Moliyaviy bozorlar uslubida OHLC grafiklar
- **📊 GRAFIK** - Vaqt bo'yicha birlik narx monitoring
- **🌍 SUNBURST** - Davlat va HS kodlar bo'yicha ulush diagrammasi  
- **🕒 TIME GROUP** - Kunlik/Haftalik/Oylik guruhlangan tahlil

### 🔍 **Progressive Filtering:**
- **15-GRAFA** - Jonatilgan mamlakat
- **34-GRAFA** - Ishlab chiqarilgan mamlakat
- **33-GRAFA** - HS kod
- **METOD** - Qiymat aniqlash metodi
- **VAQT** - DAN / GACHA sana oralig'i

### 📊 **Smart Metrics:**
- **O'RTACHA QIYMAT** - Og'irlikka asoslangan weighted average
- **Jami og'irlik** - Real kg hisobi
- **Jami bojxona qiymati** - To'liq moliyaviy hisobot

## 🛠️ **Texnik Talablar**

### **Python versiyasi:**
```
Python 3.8+ (tavsiya etiladi: 3.10+)
```

### **Kerakli kutubxonalar:**
```bash
pip install streamlit pandas plotly numpy openpyxl
```

## 📦 **O'rnatish va Ishga Tushirish**

### 1. **Repository'ni klonlash:**
```bash
git clone https://github.com/username/customs-value-analytics.git
cd customs-value-analytics
```

### 2. **Virtual environment yaratish:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

### 3. **Dependencieslarni o'rnatish:**
```bash
pip install -r requirements.txt
```

### 4. **Dasturni ishga tushirish:**
```bash
streamlit run app.py
```

### 5. **Brauzerda ochish:**
```
http://localhost:8501
```

## 🔐 **Kirish Ma'lumotlari**

```
Parol: admin123
Maxfiy kod: 2025
```

## 📂 **Qo'llab-quvvatlanadigan Fayl Formatlari**

| Format | Tavsif |
|--------|--------|
| `.csv` | Comma-separated values |
| `.xlsx` | Excel workbook |
| `.xls` | Legacy Excel format |

## 📋 **Kerakli Data Ustunlari**

```python
# Majburiy ustunlar:
"Страна отправления"     # Jonatilgan mamlakat
"31-Страна происхождения" # Ishlab chiqarilgan mamlakat  
"ТИФ ТН КОДИ"            # HS kod
"За.ед. из.$"            # Birlik narx ($/kg)
"Нетто"                  # Og'irlik (kg)
"metod"                  # Qiymat aniqlash metodi
"С графа"                # Sana (dd.mm.yyyy)
```

## 🧮 **O'rtacha Qiymat Algoritmi**

```python
# Weighted Average Formula:
def calculate_weighted_average_price(df):
    total_value = df['Bojxona_Qiymati'].sum()   # SUMM(За.ед. из.$ × Нетто)
    total_weight = df['Нетто'].sum()            # SUMM(og'irlik)
    return total_value / total_weight           # Weighted average
```

**Nima uchun weighted average?**
- Real bojxona amaliyotida standart
- Og'ir partiyalar ko'proq ta'sir qiladi
- Moliyaviy hisobotlarda aniq natija

## 📊 **Data Visualization Turlari**

### **1. CANDLESTICK:**
- Professional moliyaviy grafiklar
- OHLC (Open, High, Low, Close) ma'lumotlar
- Moving averages (MA20)
- Volume analysis
- To'g'ri ketma-ketlik (close → next open)

### **2. GRAFIK:**
- Real-time line charts
- Statistik chiziqlar (max, min, average)
- Interactive markers
- Time-series analysis

### **3. SUNBURST:**
- Hierarhik ma'lumotlar ko'rinishi
- Davlat → HS kod drill-down
- Interactive hover effects
- Treemap alternativasi

### **4. TIME GROUP:**
- Kunlik/Haftalik/Oylik guruhlash
- Trend analysis
- Multi-level charts
- Statistical summaries

## 🔄 **Progressive Filtering Logic**

```python
# Filtrlar ketma-ket qo'llanadi:
1. 15-GRAFA tanlandi → 34-GRAFA faqat shu davlatdagi variantlar
2. 34-GRAFA tanlandi → 33-GRAFA faqat qolgan variantlar  
3. 33-GRAFA tanlandi → METOD faqat qolgan variantlar
4. VAQT filtri oxirida qo'llanadi
```

## 📤 **Export Imkoniyatlari**

- **Excel format** - barcha tahlil turlari uchun
- **Multi-sheet workbook:**
  - Asosiy ma'lumotlar
  - Statistikalar  
  - Davlatlar tahlili
  - HS kodlar tahlili

## 🎨 **UI/UX Features**

### **Professional Design:**
- Dark theme support
- Responsive layout
- Animated buttons
- Loading states
- Error handling

### **User Experience:**
- Session state management
- Cache optimization  
- Real-time filtering
- Interactive tooltips
- Progress indicators

## 🔧 **Troubleshooting**

### **Umumiy muammolar:**

**1. Port band bo'lsa:**
```bash
streamlit run app.py --server.port 8502
```

**2. Memory error (katta fayllar):**
```bash
# Fayl hajmini kamaytiring yoki server quvvatini oshiring
```

**3. Date parsing errors:**
```python
# С графа ustunida turli sana formatlarini tekshiring
```

### **Performance Optimization:**

```python
# Katta datasetlar uchun:
@st.cache_data  # Automatic caching
def load_data(file):
    # Data loading optimized
```

## 📈 **Real Use Cases**

### **Bojxona Auditi:**
- Import qiymatlari monitoring
- Suspicious pricing detection
- Trend analysis
- Country comparison

### **Trade Analytics:**
- Market intelligence
- Price benchmarking  
- Seasonal patterns
- Risk assessment

### **Compliance Monitoring:**
- WTO requirements
- Transfer pricing
- Documentation audit
- Statistical reporting

## 🤝 **Contributing**

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 **License**

Bu loyiha MIT License ostida tarqatiladi. Batafsil ma'lumot uchun `LICENSE` faylini ko'ring.

## 👨‍💻 **Developer**

**Customs Value Analytics Team**
- 📧 Email: diyorbek20037377@gmail.com
- 📍 Location: Tashkent, Uzbekistan

## 🏢 **Organization**

**O'zbekiston Respublikasi Davlat Bojxona Xizmati**
- Bojxona Auditi Boshqarmasi
-Bojxona instituti

---

### **🎯 Professional Dashboard for Customs Value Analysis**
