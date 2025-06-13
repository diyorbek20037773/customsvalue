import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_import_data():
    """1000 ta sintetik import ma'lumotlarini yaratish"""
    
    # Random seed
    np.random.seed(42)
    random.seed(42)
    
    # Davlatlar ro'yxati (G34)
    countries = [
        'USA', 'CHN', 'DEU', 'TUR', 'RUS', 'KOR', 'JPN', 'IND', 
        'GBR', 'FRA', 'ITA', 'ESP', 'NLD', 'BEL', 'AUT', 'CHE',
        'POL', 'CZE', 'HUN', 'SVK', 'SVN', 'BGR', 'ROU', 'HRV',
        'FIN', 'SWE', 'DNK', 'NOR', 'ISL', 'EST', 'LVA', 'LTU',
        'UKR', 'BLR', 'MDA', 'GEO', 'ARM', 'AZE', 'KAZ', 'UZB',
        'TJK', 'KGZ', 'TKM', 'AFG', 'PAK', 'BGD', 'LKA', 'NPL'
    ]
    
    # HS kodlari ro'yxati (G33) - Real import mahsulotlari
    hs_codes = [
        # Elektronika va texnika
        '8517', '8471', '8473', '8528', '8544', '8536', '8537', '8542',
        # Avtomobil va qismlari
        '8703', '8708', '8407', '8409', '8413', '8414', '8415', '8418',
        # Neft mahsulotlari
        '2710', '2711', '2712', '2713', '2714', '2715', '2716', '2717',
        # Metall va metallurgiya
        '7208', '7209', '7210', '7211', '7212', '7213', '7214', '7215',
        # Tekstil va kiyim
        '6203', '6204', '6205', '6206', '6207', '6208', '6209', '6210',
        # Oziq-ovqat mahsulotlari
        '0901', '0902', '0903', '0904', '0905', '0906', '0907', '0908',
        # G'alla mahsulotlari
        '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008',
        # Dori va kimyo
        '3004', '3005', '3006', '3002', '3003', '3001', '2941', '2942',
        # Plastik va polimer
        '3901', '3902', '3903', '3904', '3905', '3906', '3907', '3908',
        # Mebel va yog'och
        '9403', '9401', '9402', '4409', '4407', '4408', '4410', '4411'
    ]
    
    # Ma'lumotlar ro'yxati
    data = []
    
    # Sana diapazoni (2024 yil)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days
    
    print("📊 1000 ta sintetik import ma'lumoti yaratilmoqda...")
    
    for i in range(1000):
        # Random sana
        random_days = random.randint(0, date_range)
        date = start_date + timedelta(days=random_days)
        
        # Random vaqt qo'shish
        random_hour = random.randint(8, 18)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)
        date = date.replace(hour=random_hour, minute=random_minute, second=random_second)
        
        # Random davlat va HS kod
        country = random.choice(countries)
        hs_code = random.choice(hs_codes)
        
        # Og'irlik (G38) - 10 kg dan 10000 kg gacha
        # Exponential distribution bilan real ko'rinishdagi qiymatlar
        weight = np.random.exponential(scale=300) + 10
        if weight > 10000:
            weight = np.random.uniform(100, 10000)
        weight = round(weight, 2)
        
        # Asosiy narx (PRICE) - Real import narxlari
        # Lognormal distribution bilan real narx taqsimoti
        base_price = np.random.lognormal(mean=3.8, sigma=1.0)
        if base_price < 5:
            base_price = np.random.uniform(5, 50)
        elif base_price > 1000:
            base_price = np.random.uniform(100, 1000)
        base_price = round(base_price, 2)
        
        # OHLC ma'lumotlari (Candlestick uchun)
        # OPEN narxi (ochilish)
        open_price = base_price * np.random.uniform(0.95, 1.05)
        
        # HIGH narxi (eng yuqori)
        high_multiplier = np.random.uniform(1.02, 1.15)
        high_price = open_price * high_multiplier
        
        # LOW narxi (eng past)
        low_multiplier = np.random.uniform(0.85, 0.98)
        low_price = open_price * low_multiplier
        
        # CLOSE narxi (yopilish) - High va Low orasida
        close_price = np.random.uniform(low_price, high_price)
        
        # Barcha narxlarni yaxlitlash
        open_price = round(open_price, 2)
        high_price = round(high_price, 2)
        low_price = round(low_price, 2)
        close_price = round(close_price, 2)
        
        # Sana va vaqtni formatlash (dd.mm.yyyy hh:mm:ss)
        formatted_date = date.strftime('%d.%m.%Y %H:%M:%S')
        
        # Ma'lumot qo'shish
        record = {
            'G34': country,                    # Davlat kodi
            'G33': hs_code,                   # HS kodi
            'G38': weight,                    # Og'irlik (kg)
            'PRICE': base_price,              # Asosiy narx ($)
            'OPEN': open_price,               # Ochilish narxi ($)
            'HIGH': high_price,               # Eng yuqori narx ($)
            'LOW': low_price,                 # Eng past narx ($)
            'CLOSE': close_price,             # Yopilish narxi ($)
            'INSTIME': formatted_date         # Sana va vaqt
        }
        
        data.append(record)
        
        # Progress ko'rsatish
        if (i + 1) % 100 == 0:
            print(f"✅ {i + 1}/1000 ma'lumot yaratildi...")
    
    # DataFrame yaratish
    df = pd.DataFrame(data)
    
    # Statistikalar
    print("\n📈 Yaratilgan ma'lumotlar statistikasi:")
    print(f"📋 Jami qatorlar: {len(df)}")
    print(f"🏳️ Davlatlar soni: {df['G34'].nunique()}")
    print(f"📦 HS kodlari soni: {df['G33'].nunique()}")
    print(f"💰 Narx diapazoni: ${df['PRICE'].min():.2f} - ${df['PRICE'].max():.2f}")
    print(f"⚖️ Og'irlik diapazoni: {df['G38'].min():.2f}kg - {df['G38'].max():.2f}kg")
    print(f"📅 Sana diapazoni: {df['INSTIME'].min()} - {df['INSTIME'].max()}")
    
    # CSV faylga saqlash
    filename = "import_analytics_data_1000.csv"
    df.to_csv(filename, index=False, encoding='utf-8')
    
    print(f"\n✅ Ma'lumotlar '{filename}' faylga saqlandi!")
    print(f"📂 Fayl hajmi: {len(df)} qator x {len(df.columns)} ustun")
    
    # Birinchi 10 ta yozuvni ko'rsatish
    print("\n📊 Birinchi 10 ta yozuv:")
    print(df.head(10).to_string(index=False))
    
    # Eng ko'p import qiluvchi davlatlar
    print(f"\n🌍 Eng ko'p import qiluvchi davlatlar:")
    country_stats = df['G34'].value_counts().head(10)
    for country, count in country_stats.items():
        print(f"• {country}: {count} ta import")
    
    # Eng ko'p import qilinadigan mahsulotlar
    print(f"\n📦 Eng ko'p import qilinadigan mahsulotlar (HS kodlari):")
    hs_stats = df['G33'].value_counts().head(10)
    for hs, count in hs_stats.items():
        print(f"• HS {hs}: {count} ta import")
    
    # Oylik statistika
    df['INSTIME_parsed'] = pd.to_datetime(df['INSTIME'], format='%d.%m.%Y %H:%M:%S')
    monthly_stats = df.groupby(df['INSTIME_parsed'].dt.month).size()
    print(f"\n📅 Oylik import statistikasi:")
    months = ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyun', 'Iyul', 'Avg', 'Sen', 'Okt', 'Noy', 'Dek']
    for month, count in monthly_stats.items():
        print(f"• {months[month-1]}: {count} ta import")
    
    return df

# Funksiyani ishga tushirish
if __name__ == "__main__":
    df = generate_synthetic_import_data()
    print(f"\n🎉 Sintetik ma'lumotlar tayyor!")
    print(f"💡 Bu ma'lumotlarni MVP dashboardingizda ishlatishingiz mumkin.")
    print(f"📁 Fayl nomi: import_analytics_data_1000.csv")
    
    # Ustunlar haqida ma'lumot
    print(f"\n📋 Ustunlar tafsiloti:")
    print(f"• G34: Davlat kodi ({df['G34'].nunique()} ta davlat)")
    print(f"• G33: HS kodi ({df['G33'].nunique()} ta mahsulot kodi)")
    print(f"• G38: Og'irlik kilogram da")
    print(f"• PRICE: Asosiy narx dollar da")
    print(f"• OPEN: Ochilish narxi dollar da (Candlestick)")
    print(f"• HIGH: Eng yuqori narx dollar da (Candlestick)")
    print(f"• LOW: Eng past narx dollar da (Candlestick)")
    print(f"• CLOSE: Yopilish narxi dollar da (Candlestick)")
    print(f"• INSTIME: Sana va vaqt (dd.mm.yyyy hh:mm:ss)")