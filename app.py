import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Smart Wearable", page_icon="⌚", layout="wide")

# ==========================================
# كود الـ HTML والـ JavaScript الكامل (Smartwatch OS)
# ==========================================
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smartwatch Control</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    body {
        background-color: #0d1117; color: white; font-family: 'Inter', sans-serif;
        display: flex; justify-content: center; align-items: flex-start; gap: 50px; min-height: 100vh; margin: 0; padding: 20px; flex-wrap: wrap;
    }
    
    /* ----- Watch Design ----- */
    .watch-wrapper { display: flex; flex-direction: column; align-items: center; }
    .strap { width: 100px; height: 80px; background: #222; border-radius: 20px; border: 2px solid #444; }
    .strap.top { margin-bottom: -10px; }
    .strap.bottom { margin-top: -10px; }
    .watch-body {
        width: 260px; height: 320px; background: #111; border-radius: 60px; border: 4px solid #444;
        position: relative; padding: 10px; z-index: 10; box-shadow: 0 10px 40px rgba(0,0,0,0.9);
    }
    .watch-screen {
        width: 100%; height: 100%; background: #000; border-radius: 50px; display: flex; flex-direction: column;
        align-items: center; position: relative; overflow: hidden; transition: background 0.5s;
    }
    .watch-screen.emergency-bg { background: #2a0000; }
    .watch-crown { position: absolute; right: -12px; top: 70px; width: 8px; height: 45px; background: #555; border-radius: 5px; }
    
    /* Watch UI Elements */
    .watch-time { color: #888; font-size: 11px; margin-top: 15px; margin-bottom: 5px; font-weight: 600;}
    .watch-hr-container { display: flex; align-items: center; justify-content: center; gap: 5px; }
    .watch-hr { font-size: 55px; font-weight: 800; color: #ff3b30; line-height: 1; margin: 0; transition: 0.3s; }
    .heart-icon { font-size: 24px; color: #ff3b30; animation: beat 1s infinite; }
    
    .watch-hr-label { font-size: 10px; color: #ff3b30; letter-spacing: 2px; font-weight: bold; margin-bottom: 10px; }
    .watch-spo2 { font-size: 22px; font-weight: bold; color: #32ade6; margin-bottom: 15px; transition: 0.3s;}
    
    /* Nav Buttons (Bottom of Watch) */
    .watch-nav { position: absolute; bottom: 15px; display: flex; gap: 12px; }
    .nav-btn {
        width: 30px; height: 30px; border-radius: 50%; background: #1c1c1e; border: 1px solid #333;
        display: flex; justify-content: center; align-items: center; font-size: 14px; cursor: pointer;
        transition: 0.2s; opacity: 0.6;
    }
    .nav-btn:hover { opacity: 1; }
    .nav-btn.active { opacity: 1; border-color: #0a84ff; background: rgba(10,132,255,0.2); box-shadow: 0 0 10px rgba(10,132,255,0.5);}

    @keyframes beat {
        0% { transform: scale(1); }
        15% { transform: scale(1.3); }
        30% { transform: scale(1); }
        45% { transform: scale(1.3); }
        60% { transform: scale(1); }
    }

    /* ----- Phone Design ----- */
    .phone-body {
        width: 320px; height: 650px; background: #111; border-radius: 45px; border: 6px solid #333;
        padding: 12px; position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.9); transition: 0.3s;
    }
    .phone-body.emergency { border-color: #ff3b30; box-shadow: 0 0 40px rgba(255,59,48,0.4); }
    .phone-screen {
        width: 100%; height: 100%; background: #000; border-radius: 35px; position: relative; overflow: hidden;
        display: flex; flex-direction: column;
    }
    .notch { width: 120px; height: 25px; background: #111; position: absolute; top: 0; left: 50%; transform: translateX(-50%); border-radius: 0 0 15px 15px; z-index: 10; }
    .status-bar { display: flex; justify-content: space-between; padding: 15px 20px 5px; font-size: 11px; font-weight: bold; }
    .app-title { text-align: center; font-size: 22px; font-weight: 800; margin: 10px 0 15px; }
    
    .card { background: #1c1c1e; margin: 0 15px 12px; padding: 15px; border-radius: 15px; transition: 0.3s; }
    .card-title { font-size: 11px; color: #8e8e93; text-transform: uppercase; letter-spacing: 1px; }
    .card-value { font-size: 28px; font-weight: bold; }
    .card-unit { font-size: 14px; color: #8e8e93; }
    .status-badge { padding: 5px 10px; border-radius: 10px; display: inline-block; font-size: 12px; font-weight: bold; margin-top: 5px; color: white; }
    
    /* AI Assistant Card */
    .ai-card { background: linear-gradient(135deg, #1e1e1e, #111); border: 1px solid #333; }
    .ai-card.danger { border-color: #ff3b30; background: rgba(255,59,48,0.1); }
    .ai-msg { font-size: 13px; margin-top: 8px; color: #ddd; line-height: 1.4; }
    
    .wa-btn {
        display: none; background: #25D366; color: white; padding: 12px; border-radius: 12px; 
        text-decoration: none; font-weight: bold; text-align: center; margin-top: 10px;
        font-size: 14px; box-shadow: 0 4px 15px rgba(37,211,102,0.4); animation: pulse 1.5s infinite;
    }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    
    .nav-bar { position: absolute; bottom: 0; width: 100%; height: 70px; background: rgba(28,28,30,0.9); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #333; font-size: 20px; }
</style>
</head>
<body>

    <!-- Smartwatch -->
    <div class="watch-wrapper">
        <div class="strap top"></div>
        <div class="watch-body">
            <div class="watch-crown"></div>
            <div class="watch-screen" id="watch-screen">
                <div class="watch-time" id="watch-time">09:41</div>
                <div class="watch-hr-container">
                    <div class="watch-hr" id="display-hr">75</div>
                    <div class="heart-icon" id="heart-icon">❤️</div>
                </div>
                <div class="watch-hr-label">HEART RATE</div>
                <div class="watch-spo2" id="display-spo2">SpO2 98%</div>
                
                <!-- Watch Navigation (Simulating swipe pages) -->
                <div class="watch-nav">
                    <div class="nav-btn active" id="btn-normal" onclick="setMode('normal')" title="Normal">🟢</div>
                    <div class="nav-btn" id="btn-sleep" onclick="setMode('sleep')" title="Sleep">😴</div>
                    <div class="nav-btn" id="btn-stress" onclick="setMode('stress')" title="Stress">🔥</div>
                    <div class="nav-btn" id="btn-fall" onclick="setMode('fall')" title="Fall">🚨</div>
                </div>
            </div>
        </div>
        <div class="strap bottom"></div>
    </div>

    <!-- Smartphone -->
    <div class="phone-body" id="phone-body">
        <div class="notch"></div>
        <div class="phone-screen">
            <div class="status-bar"><span>09:41</span><span>📶 🔋 100%</span></div>
            <div class="app-title">Health</div>
            
            <div class="card">
                <div class="card-title">Heart Rate</div>
                <div class="card-value" id="phone-hr">75 <span class="card-unit">BPM</span></div>
            </div>
            
            <div class="card">
                <div class="card-title">Blood Oxygen</div>
                <div class="card-value" id="phone-spo2">98 <span class="card-unit">%</span></div>
            </div>

            <div class="card">
                <div class="card-title">Current Status</div>
                <div class="card-value" id="phone-status" style="font-size: 20px;">NORMAL</div>
                <div class="status-badge" id="phone-badge" style="background:#32d74b;">MONITORING</div>
            </div>

            <div class="card ai-card" id="ai-card">
                <div class="card-title">🧠 AI Assistant</div>
                <div class="ai-msg" id="phone-ai-msg">All vitals are stable. You are good to go!</div>
                <a href="#" class="wa-btn" id="wa-link" target="_blank">📲 Send WhatsApp SOS</a>
            </div>

            <div class="nav-bar">
                <span style="color:#0a84ff;">🏠</span>
                <span style="color:#8e8e93;">❤️</span>
                <span style="color:#8e8e93;">📊</span>
                <span style="color:#8e8e93;">⚙️</span>
            </div>
        </div>
    </div>

    <script>
        // Data for all modes
        const modes = {
            normal: { hr: 75, spo2: 98, status: "NORMAL", color: "#32d74b", ai: "✅ All vitals are stable. You are good to go!", danger: false },
            sleep:  { hr: 55, spo2: 96, status: "SLEEPING", color: "#32ade6", ai: "😴 Sleep mode active. Tracking sleep cycles...", danger: false },
            stress: { hr: 115, spo2: 97, status: "HIGH STRESS", color: "#ff9f0a", ai: "⚠️ Elevated heart rate detected. You seem stressed. Please take a deep breath.", danger: false },
            fall:   { hr: 145, spo2: 85, status: "EMERGENCY", color: "#ff3b30", ai: "🚨 CRITICAL EMERGENCY! Fall detected and SpO2 is dropping. Immediate assistance required.", danger: true }
        };

        function setMode(modeName) {
            const mode = modes[modeName];

            // 1. Update Active Button UI
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('btn-' + modeName).classList.add('active');

            // 2. Update Watch UI
            document.getElementById('display-hr').innerText = mode.hr;
            document.getElementById('display-spo2').innerText = 'SpO2 ' + mode.spo2 + '%';
            
            // Adjust Heartbeat Animation Speed
            const heartIcon = document.getElementById('heart-icon');
            let beatDuration = 60 / mode.hr; // 60 seconds / BPM
            heartIcon.style.animationDuration = beatDuration + 's';

            // 3. Update Phone UI
            document.getElementById('phone-hr').innerHTML = mode.hr + ' <span class="card-unit">BPM</span>';
            document.getElementById('phone-spo2').innerHTML = mode.spo2 + ' <span class="card-unit">%</span>';
            document.getElementById('phone-status').innerText = mode.status;
            document.getElementById('phone-badge').style.background = mode.color;

            // 4. Handle Danger/WhatsApp State
            const phoneBody = document.getElementById('phone-body');
            const watchScreen = document.getElementById('watch-screen');
            const aiCard = document.getElementById('ai-card');
            const waBtn = document.getElementById('wa-link');
            const aiMsg = document.getElementById('phone-ai-msg');

            aiMsg.innerText = mode.ai;

            if (mode.danger) {
                phoneBody.classList.add('emergency');
                watchScreen.classList.add('emergency-bg');
                aiCard.classList.add('danger');
                waBtn.style.display = 'block';
                
                let msg = encodeURIComponent("🚨 EMERGENCY! Patient vitals critical. HR: " + mode.hr + " BPM, SpO2: " + mode.spo2 + "%. Fall Detected.");
                waBtn.href = "https://wa.me/201283605279?text=" + msg; // ضع رقمك هنا
            } else {
                phoneBody.classList.remove('emergency');
                watchScreen.classList.remove('emergency-bg');
                aiCard.classList.remove('danger');
                waBtn.style.display = 'none';
            }
        }

        // Set initial state on load
        setMode('normal');
    </script>
</body>
</html>
"""

# عرض الكود في المتصفح
components.html(html_code, height=750)
