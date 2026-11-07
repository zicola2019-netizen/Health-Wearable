import streamlit as st
import time
import random
import urllib.parse

st.set_page_config(page_title="Wearable Health Demo", page_icon="⌚", layout="wide")

# ==========================================
# 1. التصميم الاحترافي (CSS + HTML)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

/* إعدادات عامة */
.stApp { background-color: #0d1117; color: white; font-family: 'Inter', sans-serif; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

/* ----- تصميم الساعة ----- */
.watch-container {
    display: flex; flex-direction: column; align-items: center;
    margin-top: 20px; margin-bottom: 20px;
}
.watch-strap {
    width: 120px; height: 100px; background: #1a1a1a;
    border-radius: 20px 20px 0 0; margin-bottom: -10px;
    border: 2px solid #333;
}
.watch-body {
    width: 260px; height: 300px;
    background: linear-gradient(145deg, #2a2a2a, #111);
    border-radius: 60px; padding: 10px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8), inset 0 0 10px rgba(255,255,255,0.1);
    position: relative; z-index: 10;
    border: 3px solid #444;
}
.watch-screen {
    width: 100%; height: 100%; background: #000;
    border-radius: 50px; overflow: hidden; position: relative;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.watch-strap-bottom {
    width: 120px; height: 100px; background: #1a1a1a;
    border-radius: 0 0 20px 20px; margin-top: -10px;
    border: 2px solid #333;
}
.watch-crown {
    position: absolute; right: -8px; top: 70px;
    width: 8px; height: 40px; background: #555;
    border-radius: 5px; border: 1px solid #222;
}

/* شاشة الساعة (البيانات) */
.watch-time { color: #888; font-size: 12px; position: absolute; top: 15px; }
.watch-hr { color: #ff3b30; font-size: 64px; font-weight: 800; margin: 0; line-height: 1; text-shadow: 0 0 20px rgba(255,59,48,0.4); }
.watch-hr-label { color: #ff3b30; font-size: 12px; font-weight: 600; letter-spacing: 2px; margin-top: 5px;}
.watch-spo2 { color: #32ade6; font-size: 28px; font-weight: 600; margin-top: 15px; }
.watch-icon { font-size: 20px; margin-top: 10px; }

/* ----- تصميم الموبايل ----- */
.phone-container {
    display: flex; justify-content: center; margin-top: 20px;
}
.phone-body {
    width: 320px; height: 650px;
    background: #111; border-radius: 50px; padding: 12px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8), inset 0 0 5px rgba(255,255,255,0.2);
    border: 4px solid #333; position: relative;
}
.phone-screen {
    width: 100%; height: 100%; background: #000;
    border-radius: 40px; overflow: hidden; position: relative;
    display: flex; flex-direction: column;
}
.phone-notch {
    width: 120px; height: 25px; background: #111;
    position: absolute; top: 0; left: 50%; transform: translateX(-50%);
    border-radius: 0 0 15px 15px; z-index: 20;
}
.phone-header {
    padding: 40px 20px 10px; display: flex; justify-content: space-between; align-items: center;
    color: white; font-size: 12px; font-weight: 600;
}
.phone-app-title {
    text-align: center; color: #fff; font-size: 22px; font-weight: 800; margin-top: 10px;
}
.phone-card {
    background: #1c1c1e; border-radius: 20px; padding: 15px; margin: 15px 20px 0;
}
.phone-card-title { color: #8e8e93; font-size: 12px; font-weight: 600; text-transform: uppercase; }
.phone-card-value { color: #fff; font-size: 24px; font-weight: 800; margin-top: 5px; }
.phone-card-status { color: #32d74b; font-size: 14px; margin-top: 5px; font-weight: 600; }
.phone-card-status.danger { color: #ff3b30; }
.phone-nav {
    position: absolute; bottom: 0; width: 100%; height: 80px;
    background: rgba(28,28,30,0.9); backdrop-filter: blur(10px);
    display: flex; justify-content: space-around; align-items: center;
    border-top: 1px solid #333;
}
.phone-nav-icon { color: #8e8e93; font-size: 24px; }
.phone-nav-icon.active { color: #0a84ff; }

/* ----- التنبيهات ----- */
.ai-alert { padding: 15px; border-radius: 15px; text-align: center; font-weight: 700; margin-bottom: 15px; font-size: 16px;}
.alert-red { background: rgba(255,59,48,0.15); color: #ff3b30; border: 1px solid #ff3b30; box-shadow: 0 0 15px rgba(255,59,48,0.3);}
.alert-green { background: rgba(50,215,75,0.15); color: #32d74b; border: 1px solid #32d74b;}
.alert-orange { background: rgba(255,159,10,0.15); color: #ff9f0a; border: 1px solid #ff9f0a;}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. التحكم في البيانات (Simulation)
# ==========================================
if 'hr' not in st.session_state: st.session_state.hr = 72
if 'spo2' not in st.session_state: st.session_state.spo2 = 98
if 'status' not in st.session_state: st.session_state.status = "Normal"
if 'fall' not in st.session_state: st.session_state.fall = False

# أزرار التحكم في الـ Sidebar
with st.sidebar:
    st.markdown("## 🎮 Demo Controls")
    st.markdown("Use these buttons to simulate scenarios:")
    if st.button("🟢 Normal State", use_container_width=True):
        st.session_state.hr, st.session_state.spo2, st.session_state.fall, st.session_state.status = 75, 98, False, "Normal"
    if st.button("🏃‍♂️ Working Out", use_container_width=True):
        st.session_state.hr, st.session_state.spo2, st.session_state.fall, st.session_state.status = 130, 96, False, "Active"
    if st.button("😴 Sleeping", use_container_width=True):
        st.session_state.hr, st.session_state.spo2, st.session_state.fall, st.session_state.status = 52, 97, False, "Sleeping"
    if st.button("🚨 Fall Detected!", use_container_width=True):
        st.session_state.hr, st.session_state.spo2, st.session_state.fall, st.session_state.status = 135, 88, True, "Emergency"

# محاكاة التغير الطبيعي في القراءات
hr = st.session_state.hr + random.randint(-1, 1)
spo2 = st.session_state.spo2 + random.randint(0, 1)
current_time = time.strftime("%I:%M %p")

# ==========================================
# 3. عرض الواجهة (Layout)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #fff; margin-bottom: 30px;'>⌚ Smart Wearable Ecosystem</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1, 1])

# --- الساعة الذكية ---
with col1:
    watch_html = f"""
    <div class="watch-container">
        <div class="watch-strap"></div>
        <div class="watch-body">
            <div class="watch-crown"></div>
            <div class="watch-screen">
                <div class="watch-time">{current_time}</div>
                <div class="watch-hr">{hr}</div>
                <div class="watch-hr-label">HEART RATE</div>
                <div class="watch-spo2">SpO2 {spo2}%</div>
                <div class="watch-icon" style="color: {'red' if st.session_state.fall else '#32d74b'};">
                    {'🚨' if st.session_state.fall else '❤️'}
                </div>
            </div>
        </div>
        <div class="watch-strap-bottom"></div>
    </div>
    """
    st.markdown(watch_html, unsafe_allow_html=True)

# --- الموبايل ---
with col2:
    status_color = "danger" if st.session_state.fall else ""
    status_text = "EMERGENCY" if st.session_state.fall else st.session_state.status.upper()
    
    phone_html = f"""
    <div class="phone-container">
        <div class="phone-body">
            <div class="phone-notch"></div>
            <div class="phone-screen">
                <div class="phone-header">
                    <span>{current_time}</span>
                    <span>📶 🔋 100%</span>
                </div>
                <div class="phone-app-title">Health</div>
                
                <div class="phone-card">
                    <div class="phone-card-title">Heart Rate</div>
                    <div class="phone-card-value">{hr} <span style="font-size:14px; color:#888;">BPM</span></div>
                </div>
                
                <div class="phone-card">
                    <div class="phone-card-title">Blood Oxygen</div>
                    <div class="phone-card-value">{spo2} <span style="font-size:14px; color:#888;">%</span></div>
                </div>
                
                <div class="phone-card">
                    <div class="phone-card-title">Current State</div>
                    <div class="phone-card-value" style="font-size:18px;">{st.session_state.status}</div>
                    <div class="phone-card-status {status_color}">{status_text}</div>
                </div>
                
                <div class="phone-nav">
                    <div class="phone-nav-icon active">🏠</div>
                    <div class="phone-nav-icon">❤️</div>
                    <div class="phone-nav-icon">📊</div>
                    <div class="phone-nav-icon">⚙️</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(phone_html, unsafe_allow_html=True)

# --- تحليل الـ AI والتنبيهات ---
with col3:
    st.markdown("### 🧠 AI Analysis")
    
    if st.session_state.fall or hr > 120 or spo2 < 90:
        st.markdown('<div class="ai-alert alert-red">🚨 CRITICAL EMERGENCY<br>Fall Detected / Abnormal Vitals</div>', unsafe_allow_html=True)
        
        phone_num = "201283605279" # غير الرقم هنا
        msg = f"🚨 EMERGENCY! Patient needs help. HR: {hr}, SpO2: {spo2}%"
        wa_url = f"https://wa.me/{phone_num}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <a href="{wa_url}" target="_blank">
                <button style="background: #ff3b30; color: white; padding: 15px; border: none; border-radius: 15px; width: 100%; font-size: 16px; font-weight: 800; cursor: pointer; box-shadow: 0 0 20px rgba(255,59,48,0.5);">
                    📲 SEND WHATSAPP SOS
                </button>
            </a>
        ''', unsafe_allow_html=True)
    elif st.session_state.status == "Active":
        st.markdown('<div class="ai-alert alert-orange">🏃‍♂️ High Activity Detected.<br>Heart rate is elevated (Normal for exercise).</div>', unsafe_allow_html=True)
    elif st.session_state.status == "Sleeping":
        st.markdown('<div class="ai-alert alert-green" style="color:#32ade6; border-color:#32ade6; background:rgba(50,173,230,0.1);">😴 Sleep Mode Active.<br>Tracking sleep cycles...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ai-alert alert-green">✅ All Vitals Normal.<br>Patient is safe.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
