import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Smart Wearable", page_icon="⌚", layout="wide")

# ==========================================
# كود الـ HTML والـ JavaScript الكامل
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
    
    /* ----- Watch ----- */
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
        align-items: center; padding-top: 20px; position: relative; overflow: hidden;
    }
    .watch-crown { position: absolute; right: -12px; top: 70px; width: 8px; height: 45px; background: #555; border-radius: 5px; }
    
    .watch-time { color: #888; font-size: 12px; margin-bottom: 5px; }
    .watch-hr { font-size: 55px; font-weight: 800; color: #ff3b30; line-height: 1; margin: 0; text-shadow: 0 0 15px rgba(255,59,48,0.4); transition: 0.2s; }
    .watch-hr-label { font-size: 10px; color: #ff3b30; letter-spacing: 2px; font-weight: bold; margin-bottom: 15px; }
    .watch-spo2 { font-size: 24px; font-weight: bold; color: #32ade6; margin-bottom: 10px; transition: 0.2s;}
    
    /* Sliders inside Watch */
    .control-group { width: 80%; text-align: left; margin-bottom: 10px; }
    .control-label { font-size: 10px; color: #aaa; margin-bottom: 2px; display: flex; justify-content: space-between;}
    input[type=range] { -webkit-appearance: none; width: 100%; background: transparent; }
    input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; height: 15px; width: 15px; border-radius: 50%; background: #fff; cursor: pointer; margin-top: -5px; box-shadow: 0 0 10px rgba(255,255,255,0.5); }
    input[type=range]::-webkit-slider-runnable-track { width: 100%; height: 5px; cursor: pointer; background: #333; border-radius: 5px; }
    .fall-btn { background: #ff3b30; color: white; border: none; padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; cursor: pointer; margin-top: 5px; box-shadow: 0 0 10px rgba(255,59,48,0.5); }

    /* ----- Phone ----- */
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
    
    /* WhatsApp Button inside Phone */
    .wa-btn {
        display: none; background: #25D366; color: white; padding: 12px; border-radius: 12px; 
        text-decoration: none; font-weight: bold; text-align: center; margin-top: 10px;
        font-size: 14px; box-shadow: 0 4px 15px rgba(37,211,102,0.4); animation: pulse 1.5s infinite;
    }
    
    .nav-bar { position: absolute; bottom: 0; width: 100%; height: 70px; background: rgba(28,28,30,0.9); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #333; font-size: 20px; }

    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
</style>
</head>
<body>

    <!-- Watch -->
    <div class="watch-wrapper">
        <div class="strap top"></div>
        <div class="watch-body">
            <div class="watch-crown"></div>
            <div class="watch-screen">
                <div class="watch-time">09:41</div>
                <div class="watch-hr" id="display-hr">75</div>
                <div class="watch-hr-label">HEART RATE</div>
                <div class="watch-spo2" id="display-spo2">SpO2 98%</div>
                
                <div class="control-group">
                    <div class="control-label"><span>Heart Rate</span><span id="val-hr">75</span></div>
                    <input type="range" id="slider-hr" min="40" max="160" value="75" oninput="updateData()">
                </div>
                <div class="control-group">
                    <div class="control-label"><span>SpO2</span><span id="val-spo2">98</span></div>
                    <input type="range" id="slider-spo2" min="80" max="100" value="98" oninput="updateData()">
                </div>
                <button class="fall-btn" id="fall-btn" onclick="toggleFall()">Simulate Fall</button>
            </div>
        </div>
        <div class="strap bottom"></div>
    </div>

    <!-- Phone -->
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

            <!-- AI & WhatsApp inside the App -->
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
        let isFall = false;

        function toggleFall() {
            isFall = !isFall;
            const btn = document.getElementById('fall-btn');
            if(isFall) {
                btn.style.background = '#880000';
                btn.innerText = 'RESET FALL';
                document.getElementById('slider-hr').value = 140;
                document.getElementById('slider-spo2').value = 85;
            } else {
                btn.style.background = '#ff3b30';
                btn.innerText = 'Simulate Fall';
                document.getElementById('slider-hr').value = 75;
                document.getElementById('slider-spo2').value = 98;
            }
            updateData();
        }

        function updateData() {
            let hr = parseInt(document.getElementById('slider-hr').value);
            let spo2 = parseInt(document.getElementById('slider-spo2').value);

            // Update Watch UI
            document.getElementById('display-hr').innerText = hr;
            document.getElementById('display-spo2').innerText = 'SpO2 ' + spo2 + '%';
            document.getElementById('val-hr').innerText = hr;
            document.getElementById('val-spo2').innerText = spo2;

            // Update Phone UI
            document.getElementById('phone-hr').innerHTML = hr + ' <span class="card-unit">BPM</span>';
            document.getElementById('phone-spo2').innerHTML = spo2 + ' <span class="card-unit">%</span>';

            // Get DOM Elements for AI & State
            let phoneBody = document.getElementById('phone-body');
            let aiCard = document.getElementById('ai-card');
            let aiMsg = document.getElementById('phone-ai-msg');
            let waBtn = document.getElementById('wa-link');

            // Logic
            if (isFall || hr > 120 || spo2 < 90) {
                // EMERGENCY STATE
                document.getElementById('phone-status').innerText = "EMERGENCY";
                document.getElementById('phone-badge').style.background = "#ff3b30";
                
                // Make phone glow red
                phoneBody.classList.add('emergency');
                
                // AI Card update
                aiCard.classList.add('danger');
                aiMsg.innerHTML = "<strong style='color:#ff3b30;'>🚨 CRITICAL EMERGENCY!</strong><br>Fall detected or vitals are critical. Immediate assistance required.";
                
                // Show WhatsApp Button
                waBtn.style.display = 'block';
                let msg = encodeURIComponent("🚨 EMERGENCY! Patient vitals critical. HR: " + hr + " BPM, SpO2: " + spo2 + "%. Fall Detected: " + isFall);
                waBtn.href = "https://wa.me/201283605279?text=" + msg; // رقمك هنا
                
            } else if (hr > 100) {
                // HIGH STRESS
                document.getElementById('phone-status').innerText = "HIGH STRESS";
                document.getElementById('phone-badge').style.background = "#ff9f0a";
                phoneBody.classList.remove('emergency');
                
                aiCard.classList.remove('danger');
                aiMsg.innerText = "⚠️ Elevated heart rate detected. You seem stressed. Please take a deep breath.";
                waBtn.style.display = 'none';
                
            } else {
                // NORMAL STATE
                document.getElementById('phone-status').innerText = "NORMAL";
                document.getElementById('phone-badge').style.background = "#32d74b";
                phoneBody.classList.remove('emergency');
                
                aiCard.classList.remove('danger');
                aiMsg.innerText = "✅ All vitals are stable. You are good to go!";
                waBtn.style.display = 'none';
            }
        }

        // Initialize
        updateData();
    </script>
</body>
</html>
"""

# عرض الكود في المتصفح
components.html(html_code, height=750)
