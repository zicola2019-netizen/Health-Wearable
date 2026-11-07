import streamlit as st
import time
import random
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Wearable Ecosystem", page_icon="⌚", layout="wide")

# 2. تصميم الـ CSS (شكل الساعة والموبايل)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* شكل الساعة الذكية */
    .smartwatch {
        width: 280px; height: 320px;
        background: #111; border-radius: 40px;
        border: 4px solid #333;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
        margin: auto; padding: 20px; text-align: center;
        position: relative;
    }
    .watch-screen {
        background: #000; height: 100%; border-radius: 25px;
        padding: 15px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .watch-hr { font-size: 40px; font-weight: bold; color: #ff4b4b; margin: 0; }
    .watch-spo2 { font-size: 30px; font-weight: bold; color: #00f3ff; margin: 0; }
    .watch-label { font-size: 12px; color: #888; letter-spacing: 2px; }
    
    /* شكل الموبايل */
    .phone {
        width: 300px; height: 550px;
        background: #111; border-radius: 40px;
        border: 6px solid #222;
        box-shadow: 0 0 30px rgba(0, 243, 255, 0.15);
        margin: auto; padding: 15px;
    }
    .phone-screen {
        background: #0a0a0a; height: 100%; border-radius: 30px;
        padding: 20px; display: flex; flex-direction: column;
    }
    
    /* التنبيهات */
    .alert-danger { background: rgba(255,0,0,0.2); border: 1px solid red; color: red; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-top: 10px;}
    .alert-safe { background: rgba(0,255,0,0.1); border: 1px solid green; color: #00ff00; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("⌚ Smart Wearable Health Ecosystem")
st.markdown("### Live Demo: Real-time Health Telemetry & Fall Detection")

# 3. محاكاة البيانات (Data Simulation)
# في الواقع، دي هتكون جاية من ESP32، لكن هنا بنعملها بـ Python عشان الديمو
if 'hr' not in st.session_state: st.session_state.hr = 75
if 'spo2' not in st.session_state: st.session_state.spo2 = 98
if 'status' not in st.session_state: st.session_state.status = "Normal"
if 'fall' not in st.session_state: st.session_state.fall = False

# 4. أزرار التحكم (عشان تعرض السيناريوهات للدكتور)
st.sidebar.header("🎮 Simulation Controls")
st.sidebar.write("استخدم الأزرار دي عشان تحاكي الحالات للدكتور")
if st.sidebar.button("🟢 Normal State (حالة طبيعية)"):
    st.session_state.hr = random.randint(70, 80)
    st.session_state.spo2 = random.randint(97, 99)
    st.session_state.fall = False
    st.session_state.status = "Normal"
if st.sidebar.button("🚨 Fall Detected (سقوط)"):
    st.session_state.hr = 130
    st.session_state.spo2 = 88
    st.session_state.fall = True
    st.session_state.status = "Emergency"
if st.sidebar.button("😴 Sleeping (نوم)"):
    st.session_state.hr = 55
    st.session_state.spo2 = 96
    st.session_state.fall = False
    st.session_state.status = "Sleeping"
if st.sidebar.button("😰 High Stress (توتر)"):
    st.session_state.hr = 115
    st.session_state.spo2 = 97
    st.session_state.fall = False
    st.session_state.status = "Stressed"

# 5. تحديث تلقائي للبيانات كل ثانيتين
hr = st.session_state.hr + random.randint(-2, 2)
spo2 = st.session_state.spo2 + random.randint(-1, 1)

# 6. عرض الواجهة (الساعة والموبايل)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(f"""
    <div class="smartwatch">
        <div class="watch-screen">
            <div>
                <div class="watch-label">HEART RATE</div>
                <div class="watch-hr">{hr} <span style="font-size:16px;color:white;">BPM</span></div>
            </div>
            <div>
                <div class="watch-label">OXYGEN</div>
                <div class="watch-spo2">{spo2}<span style="font-size:16px;color:white;">%</span></div>
            </div>
            <div style="color: #888; font-size: 12px;">{time.strftime("%H:%M:%S")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="phone">
        <div class="phone-screen">
            <h4 style="color: #00f3ff; text-align: center;">Health App</h4>
            <div style="background: #222; padding: 15px; border-radius: 15px; margin-top: 10px;">
                <p style="margin:0; color:#888;">Current State:</p>
                <h3 style="margin:0; color:white;">{st.session_state.status}</h3>
            </div>
            
            <div style="background: #222; padding: 15px; border-radius: 15px; margin-top: 15px;">
                <p style="margin:0; color:#888;">Fall Detection:</p>
                <h3 style="margin:0; color:{'red' if st.session_state.fall else 'green'};">
                    {'🚨 FALL DETECTED!' if st.session_state.fall else '✅ Secure'}
                </h3>
            </div>
            
            <div style="margin-top:auto; text-align:center; padding-bottom:10px;">
                <div style="width:40px; height:40px; border-radius:50%; background:#333; margin:auto;"></div>
                <p style="color:#555; font-size:10px;">Swipe up to unlock</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("### 🧠 AI Analysis & Alerts")
    
    # التحليل الذكي
    if st.session_state.fall or hr > 120 or spo2 < 90:
        st.markdown('<div class="alert-danger">🚨 CRITICAL EMERGENCY DETECTED!<br>Patient needs immediate attention.</div>', unsafe_allow_html=True)
        
        # زرار الواتساب
        phone = "201283605279" # <--- حط رقمك هنا
        msg = f"🚨 EMERGENCY! Fall detected. HR: {hr}, SpO2: {spo2}%"
        wa_url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <a href="{wa_url}" target="_blank">
                <button style="background-color: #ff4b4b; color: white; padding: 15px; border: none; border-radius: 10px; width: 100%; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 20px;">
                    📲 SEND WHATSAPP SOS
                </button>
            </a>
        ''', unsafe_allow_html=True)
        
    elif st.session_state.status == "Stressed":
        st.markdown('<div class="alert-safe" style="background:rgba(255,165,0,0.2); border-color:orange; color:orange;">⚠️ High Stress Detected.<br>Recommend taking a deep breath.</div>', unsafe_allow_html=True)
    elif st.session_state.status == "Sleeping":
        st.markdown('<div class="alert-safe" style="color:#00f3ff; border-color:#00f3ff; background:rgba(0,243,255,0.1);">😴 Sleep Mode Active.<br>Monitoring sleep quality...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-safe">✅ All vitals are normal.<br>Patient is safe and healthy.</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("🔄 Refresh Live Data"):
    st.rerun()
