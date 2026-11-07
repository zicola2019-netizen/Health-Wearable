import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Smart Wearable", page_icon="⌚", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smartwatch OS</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* إعدادات الصفحة الأساسية */
    body {
        background-color: #0d1117; color: white; font-family: 'Inter', sans-serif;
        margin: 0; padding: 0; height: 100vh; overflow: hidden;
    }

    /* الحاوية الرئيسية - هنثبتها في نص الشاشة بالظبط */
    .app-container {
        display: flex; justify-content: center; align-items: flex-start; gap: 40px;
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%); /* سر التوسيط */
        transform-origin: center center;
        transition: transform 0.3s ease;
    }
    
    /* ----- Watch ----- */
    .watch-wrapper { display: flex; flex-direction: column; align-items: center; }
    .strap { width: 100px; height: 80px; background: #222; border-radius: 20px; border: 2px solid #333; }
    .strap.top { margin-bottom: -10px; }
    .strap.bottom { margin-top: -10px; }
    .watch-body {
        width: 250px; height: 310px; background: #000; border-radius: 60px; border: 4px solid #333;
        position: relative; padding: 10px; z-index: 10; box-shadow: 0 0 30px rgba(0,255,204,0.1); transition: 0.3s;
    }
    .watch-body.emergency { border-color: #ff3b30; box-shadow: 0 0 40px rgba(255,59,48,0.4); }
    .watch-screen {
        width: 100%; height: 100%; background: #000; border-radius: 50px; display: flex; flex-direction: column;
        align-items: center; position: relative; overflow: hidden; transition: background 0.3s;
    }
    .watch-screen.emergency-bg { background: #2a0000; }
    .watch-time { color: #888; font-size: 11px; margin-top: 15px; margin-bottom: 5px; font-weight: 600;}
    .watch-hr-container { display: flex; align-items: center; justify-content: center; gap: 5px; }
    .watch-hr { font-size: 55px; font-weight: 800; color: #ff3b30; line-height: 1; margin: 0; text-shadow: 0 0 10px rgba(255,59,48,0.3); }
    .heart-icon { font-size: 20px; color: #ff3b30; animation: beat 1s infinite; }
    .watch-hr-label { font-size: 10px; color: #ff3b30; letter-spacing: 2px; font-weight: bold; margin-bottom: 10px; }
    .watch-spo2 { font-size: 22px; font-weight: bold; color: #32ade6; margin-bottom: 15px; }
    
    .watch-nav { position: absolute; bottom: 15px; display: flex; gap: 10px; }
    .nav-btn {
        width: 32px; height: 32px; border-radius: 50%; background: #1c1c1e; border: 1px solid #333;
        display: flex; justify-content: center; align-items: center; font-size: 14px; cursor: pointer;
        transition: 0.2s; opacity: 0.6;
    }
    .nav-btn.active { opacity: 1; border-color: #0a84ff; background: rgba(10,132,255,0.2); box-shadow: 0 0 10px rgba(10,132,255,0.5);}
    @keyframes beat { 0% { transform: scale(1); } 15% { transform: scale(1.3); } 30% { transform: scale(1); } 45% { transform: scale(1.3); } 60% { transform: scale(1); } }

    /* ----- Phone ----- */
    .phone-body {
        width: 320px; height: 650px; background: #000; border-radius: 45px; border: 6px solid #333;
        padding: 10px; position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.9); transition: 0.3s;
    }
    .phone-body.emergency { border-color: #ff3b30; box-shadow: 0 0 40px rgba(255,59,48,0.4); }
    .phone-screen {
        width: 100%; height: 100%; background: #000; border-radius: 35px; position: relative; overflow: hidden;
        display: flex; flex-direction: column;
    }
    .notch { width: 120px; height: 25px; background: #000; position: absolute; top: 0; left: 50%; transform: translateX(-50%); border-radius: 0 0 15px 15px; z-index: 10; border: 1px solid #111;}
    .status-bar { display: flex; justify-content: space-between; padding: 15px 20px 5px; font-size: 11px; font-weight: bold; color: #fff; }
    
    .view { display: none; flex-direction: column; height: 100%; padding: 10px 15px; }
    .view.active { display: flex; animation: fadeIn 0.3s; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    .app-title { text-align: center; font-size: 20px; font-weight: 800; margin: 5px 0 15px; }
    .card { background: #1c1c1e; margin-bottom: 12px; padding: 15px; border-radius: 15px; }
    .card-title { font-size: 11px; color: #8e8e93; text-transform: uppercase; letter-spacing: 1px; }
    .card-value { font-size: 28px; font-weight: bold; }
    .card-unit { font-size: 14px; color: #8e8e93; }
    .status-badge { padding: 4px 8px; border-radius: 8px; display: inline-block; font-size: 10px; font-weight: bold; margin-top: 5px; color: white; }
    
    .ai-card { background: linear-gradient(135deg, #1e1e1e, #111); border: 1px solid #333; transition: 0.3s; }
    .ai-card.danger { border-color: #ff3b30; background: rgba(255,59,48,0.1); }
    .ai-msg { font-size: 13px; margin-top: 8px; color: #ddd; line-height: 1.4; }
    .wa-btn {
        display: none; background: #25D366; color: white; padding: 12px; border-radius: 12px; 
        text-decoration: none; font-weight: bold; text-align: center; margin-top: 10px;
        font-size: 14px; box-shadow: 0 4px 15px rgba(37,211,102,0.4); animation: pulse 1.5s infinite;
    }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    
    .chart-container { position: relative; height: 250px; width: 100%; margin-top: 10px; background: #1c1c1e; border-radius: 15px; padding: 10px;}

    .nav-bar { position: absolute; bottom: 0; width: 100%; height: 65px; background: #111; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #333; }
    .nav-item { font-size: 22px; cursor: pointer; opacity: 0.5; transition: 0.2s; }
    .nav-item.active { opacity: 1; transform: scale(1.1); }

    /* ----- الحل النهائي للموبايل ----- */
    @media (max-width: 800px) {
        .app-container {
            transform: translate(-50%, -50%) scale(0.45); /* تصغير + توسيط في نفس الوقت */
            gap: 20px;
        }
    }
</style>
</head>
<body>

    <div class="app-container">
        <!-- Watch -->
        <div class="watch-wrapper">
            <div class="strap top"></div>
            <div class="watch-body" id="watch-body">
                <div class="watch-screen" id="watch-screen">
                    <div class="watch-time">09:41</div>
                    <div class="watch-hr-container">
                        <div class="watch-hr" id="watch-hr">75</div>
                        <div class="heart-icon" id="heart-icon">❤️</div>
                    </div>
                    <div class="watch-hr-label">HEART RATE</div>
                    <div class="watch-spo2" id="watch-spo2">SpO2 98%</div>
                    
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

        <!-- Phone -->
        <div class="phone-body" id="phone-body">
            <div class="notch"></div>
            <div class="phone-screen">
                <div class="status-bar"><span>09:41</span><span>📶 🔋 100%</span></div>
                
                <div class="view active" id="view-home">
                    <div class="app-title">Health App</div>
                    <div class="card">
                        <div class="card-title">Heart Rate</div>
                        <div class="card-value" id="phone-hr">75 <span class="card-unit">BPM</span></div>
                    </div>
                    <div class="card">
                        <div class="card-title">Blood Oxygen</div>
                        <div class="card-value" id="phone-spo2">98 <span class="card-unit">%</span></div>
                    </div>
                    <div class="card">
                        <div class="card-title">Status</div>
                        <div class="card-value" id="phone-status" style="font-size: 18px;">NORMAL</div>
                        <div class="status-badge" id="phone-badge" style="background:#32d74b;">MONITORING</div>
                    </div>
                    <div class="card ai-card" id="ai-card">
                        <div class="card-title">🧠 AI Assistant</div>
                        <div class="ai-msg" id="phone-ai-msg">All vitals are stable. You are good to go!</div>
                        <a href="#" class="wa-btn" id="wa-link" target="_blank">📲 Send WhatsApp SOS</a>
                    </div>
                </div>

                <div class="view" id="view-heart">
                    <div class="app-title">Heart Rate</div>
                    <div class="chart-container"><canvas id="hrChart"></canvas></div>
                    <div style="text-align: center; margin-top: 10px; color:#888; font-size: 12px;">Last 1 Hour (Live)</div>
                </div>

                <div class="view" id="view-chart">
                    <div class="app-title">Health Trends</div>
                    <div class="chart-container"><canvas id="combinedChart"></canvas></div>
                    <div style="text-align: center; margin-top: 10px; color:#888; font-size: 12px;">HR & SpO2 (Last 1 Hour)</div>
                </div>

                <div class="nav-bar">
                    <div class="nav-item active" id="nav-home" onclick="switchView('home')">🏠</div>
                    <div class="nav-item" id="nav-heart" onclick="switchView('heart')">❤️</div>
                    <div class="nav-item" id="nav-chart" onclick="switchView('chart')">📊</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentMode = 'normal';
        let currentHR = 75;
        let currentSpO2 = 98;

        const modes = {
            normal: { hr: 75, spo2: 98, status: "NORMAL", color: "#32d74b", danger: false, ai: "✅ All vitals are stable. You are good to go! Keep up the good work and stay hydrated." },
            sleep:  { hr: 55, spo2: 96, status: "SLEEPING", color: "#32ade6", danger: false, ai: "😴 Sleep mode active. Ensure you are in a comfortable position and relax. Sweet dreams!" },
            stress: { hr: 115, spo2: 97, status: "HIGH STRESS", color: "#ff9f0a", danger: false, ai: "⚠️ Elevated heart rate detected. Please take a deep breath, sit down, drink a glass of water, and try to relax for 5 minutes." },
            fall:   { hr: 145, spo2: 85, status: "EMERGENCY", color: "#ff3b30", danger: true, ai: "🚨 CRITICAL EMERGENCY! Fall detected. If you are conscious, please stay still, take slow deep breaths to stabilize your heart rate, and seek help immediately. SOS sent." }
        };

        let labels = Array.from({length: 60}, (_, i) => `${60-i}m ago`);
        let hrData = Array.from({length: 60}, () => 75 + Math.random() * 10);
        let spo2Data = Array.from({length: 60}, () => 97 + Math.random() * 2);

        const ctxHR = document.getElementById('hrChart').getContext('2d');
        const hrChart = new Chart(ctxHR, {
            type: 'line',
            data: { labels: labels, datasets: [{ label: 'Heart Rate', data: hrData, borderColor: '#ff3b30', backgroundColor: 'rgba(255, 59, 48, 0.1)', borderWidth: 2, fill: true, tension: 0.4, pointRadius: 0 }] },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { display: true, textColor: '#888', grid: { color: '#333' } } } }
        });

        const ctxCombined = document.getElementById('combinedChart').getContext('2d');
        const combinedChart = new Chart(ctxCombined, {
            type: 'line',
            data: { 
                labels: labels, 
                datasets: [
                    { label: 'Heart Rate', data: hrData, borderColor: '#ff3b30', borderWidth: 2, tension: 0.4, pointRadius: 0, yAxisID: 'y' },
                    { label: 'SpO2', data: spo2Data, borderColor: '#32ade6', borderWidth: 2, tension: 0.4, pointRadius: 0, yAxisID: 'y1' }
                ] 
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: true, labels: {color: '#fff'} } }, scales: { x: { display: false }, y: { type: 'linear', display: true, position: 'left', textColor: '#ff3b30', grid: { color: '#333' } }, y1: { type: 'linear', display: true, position: 'right', textColor: '#32ade6', grid: { drawOnChartArea: false } } } }
        });

        function switchView(viewName) {
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('view-' + viewName).classList.add('active');
            document.getElementById('nav-' + viewName).classList.add('active');
            if(viewName === 'heart') hrChart.update();
            if(viewName === 'chart') combinedChart.update();
        }

        function setMode(modeName) {
            currentMode = modeName;
            const mode = modes[modeName];
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('btn-' + modeName).classList.add('active');
            document.getElementById('watch-hr').innerText = mode.hr;
            document.getElementById('watch-spo2').innerText = 'SpO2 ' + mode.spo2 + '%';
            document.getElementById('phone-hr').innerHTML = mode.hr + ' <span class="card-unit">BPM</span>';
            document.getElementById('phone-spo2').innerHTML = mode.spo2 + ' <span class="card-unit">%</span>';
            document.getElementById('phone-status').innerText = mode.status;
            document.getElementById('phone-badge').style.background = mode.color;
            document.getElementById('phone-ai-msg').innerText = mode.ai;
            
            const phoneBody = document.getElementById('phone-body');
            const watchBody = document.getElementById('watch-body');
            const aiCard = document.getElementById('ai-card');
            const waBtn = document.getElementById('wa-link');

            if (mode.danger) {
                phoneBody.classList.add('emergency');
                watchBody.classList.add('emergency');
                aiCard.classList.add('danger');
                waBtn.style.display = 'block';
                let msg = encodeURIComponent("🚨 EMERGENCY! Patient vitals critical. HR: " + mode.hr + " BPM, SpO2: " + mode.spo2 + "%. Fall Detected.");
                waBtn.href = "https://wa.me/201283605279?text=" + msg;
            } else {
                phoneBody.classList.remove('emergency');
                watchBody.classList.remove('emergency');
                aiCard.classList.remove('danger');
                waBtn.style.display = 'none';
            }
            currentHR = mode.hr;
            currentSpO2 = mode.spo2;
            updateHeartbeat(mode.hr);
        }

        function updateHeartbeat(hr) {
            document.getElementById('heart-icon').style.animationDuration = (60 / hr) + 's';
        }

        setInterval(() => {
            let newHR = currentHR + Math.round(Math.random() * 4 - 2);
            let newSpO2 = currentSpO2 + Math.round(Math.random() * 2 - 1);
            
            if (currentMode === 'normal' || currentMode === 'sleep') {
                if (newHR < 50) newHR = 50;
                if (newHR > 100) newHR = 100;
                if (newSpO2 > 100) newSpO2 = 100;
                if (newSpO2 < 95) newSpO2 = 95;
            } else {
                newHR = currentHR + Math.round(Math.random() * 6 - 3);
                newSpO2 = currentSpO2 + Math.round(Math.random() * 2 - 1);
            }

            currentHR = newHR;
            currentSpO2 = newSpO2;

            document.getElementById('watch-hr').innerText = newHR;
            document.getElementById('watch-spo2').innerText = 'SpO2 ' + newSpO2 + '%';
            updateHeartbeat(newHR);

            document.getElementById('phone-hr').innerHTML = newHR + ' <span class="card-unit">BPM</span>';
            document.getElementById('phone-spo2').innerHTML = newSpO2 + ' <span class="card-unit">%</span>';

            hrData.push(newHR); hrData.shift();
            spo2Data.push(newSpO2); spo2Data.shift();
            hrChart.update();
            combinedChart.update();
        }, 3000);

        setMode('normal');
    </script>
</body>
</html>
"""

# قللنا الـ height لـ 400 عشان المساحة السودة تختفي تماماً
components.html(html_code, height=400)
