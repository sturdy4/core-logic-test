#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import os
import json
import time

PASSWORD = "admin123"  # CHANGE THIS!
SERVER_DIR = os.path.expanduser("~/mc-server-1.21.10")
COMMAND_PIPE = os.path.join(SERVER_DIR, "console.pipe")

class MinecraftHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check password
        if f"?pass={PASSWORD}" not in self.path:
            self.send_error(403, "Access Denied")
            return
        
        # Routes
        if self.path.startswith(f"/?pass={PASSWORD}"):
            self.serve_dashboard()
        elif "/cmd/" in self.path:
            self.handle_command()
        elif "/status" in self.path:
            self.get_status()
        elif "/logs" in self.path:
            self.get_logs()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Minecraft Server Control</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * { box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    max-width: 1000px; 
                    margin: 0 auto; 
                    padding: 20px; 
                    background: #1a1a1a; 
                    color: #fff; 
                }
                .header { 
                    background: linear-gradient(90deg, #007bff, #6610f2); 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin-bottom: 20px; 
                    text-align: center; 
                }
                .btn-group { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                    gap: 10px; 
                    margin-bottom: 20px; 
                }
                .btn { 
                    padding: 15px; 
                    border: none; 
                    border-radius: 5px; 
                    cursor: pointer; 
                    font-size: 16px; 
                    font-weight: bold; 
                    transition: 0.3s; 
                }
                .btn:hover { transform: translateY(-2px); opacity: 0.9; }
                .btn-start { background: #28a745; color: white; }
                .btn-stop { background: #dc3545; color: white; }
                .btn-restart { background: #ffc107; color: black; }
                .btn-cmd { background: #17a2b8; color: white; }
                .btn-save { background: #6f42c1; color: white; }
                .status { 
                    background: #2d2d2d; 
                    padding: 15px; 
                    border-radius: 5px; 
                    margin: 15px 0; 
                    border-left: 5px solid #007bff; 
                }
                .status-online { border-color: #28a745; }
                .status-offline { border-color: #dc3545; }
                .command-box { 
                    margin: 20px 0; 
                    display: flex; 
                    gap: 10px; 
                }
                #customCmd { 
                    flex: 1; 
                    padding: 12px; 
                    border: 2px solid #007bff; 
                    border-radius: 5px; 
                    background: #2d2d2d; 
                    color: white; 
                    font-size: 16px; 
                }
                .logs { 
                    background: #000; 
                    color: #0f0; 
                    padding: 15px; 
                    border-radius: 5px; 
                    font-family: 'Courier New', monospace; 
                    max-height: 300px; 
                    overflow-y: auto; 
                    white-space: pre-wrap; 
                    margin-top: 20px; 
                }
                .quick-cmds { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 10px; 
                    margin: 20px 0; 
                }
                .quick-btn { 
                    background: #495057; 
                    color: white; 
                    padding: 10px; 
                    border: none; 
                    border-radius: 5px; 
                    cursor: pointer; 
                }
                h3 { color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎮 Minecraft Server Control Panel</h1>
                <p>Manage your server from the browser</p>
            </div>
            
            <div class="status" id="statusBox">Checking server status...</div>
            
            <div class="btn-group">
                <button class="btn btn-start" onclick="sendCmd('start')">▶ Start Server</button>
                <button class="btn btn-stop" onclick="sendCmd('stop')">⏹ Stop Server</button>
                <button class="btn btn-restart" onclick="sendCmd('restart')">🔄 Restart</button>
                <button class="btn btn-save" onclick="sendCmd('save-all')">💾 Save World</button>
            </div>
            
            <h3>⚡ Quick Commands</h3>
            <div class="quick-cmds">
                <button class="quick-btn" onclick="sendCmd('op Binwalk')">👑 OP Binwalk</button>
                <button class="quick-btn" onclick="sendCmd('gamemode creative Binwalk')">✨ Creative Mode</button>
                <button class="quick-btn" onclick="sendCmd('time set day')">☀️ Time to Day</button>
                <button class="quick-btn" onclick="sendCmd('time set night')">🌙 Time to Night</button>
                <button class="quick-btn" onclick="sendCmd('weather clear')">☀️ Clear Weather</button>
                <button class="quick-btn" onclick="sendCmd('weather rain')">🌧️ Make it Rain</button>
                <button class="quick-btn" onclick="sendCmd('difficulty peaceful')">🕊️ Peaceful Mode</button>
                <button class="quick-btn" onclick="sendCmd('whitelist reload')">📋 Reload Whitelist</button>
            </div>
            
            <h3>🎯 Custom Command</h3>
            <div class="command-box">
                <input type="text" id="customCmd" placeholder="Enter server command (e.g., 'give Binwalk diamond 64')">
                <button class="btn btn-cmd" onclick="sendCustomCmd()">Send Command</button>
            </div>
            
            <h3>📊 Server Logs (Last 10 lines)</h3>
            <div class="logs" id="serverLogs">Loading logs...</div>
            
            <script>
            function sendCmd(cmd) {
                fetch('/cmd/' + encodeURIComponent(cmd) + '?pass=""" + PASSWORD + """')
                    .then(r => r.text())
                    .then(t => {
                        alert('Command executed: ' + t);
                        updateStatus();
                        updateLogs();
                    });
            }
            
            function sendCustomCmd() {
                let cmd = document.getElementById('customCmd').value;
                if(cmd.trim()) {
                    sendCmd(cmd);
                    document.getElementById('customCmd').value = '';
                }
            }
            
            function updateStatus() {
                fetch('/status?pass=""" + PASSWORD + """')
                    .then(r => r.text())
                    .then(t => {
                        let box = document.getElementById('statusBox');
                        box.innerHTML = t;
                        box.className = t.includes('ONLINE') ? 'status status-online' : 'status status-offline';
                    });
            }
            
            function updateLogs() {
                fetch('/logs?pass=""" + PASSWORD + """')
                    .then(r => r.text())
                    .then(t => {
                        document.getElementById('serverLogs').innerText = t;
                    });
            }
            
            // Enter key for custom command
            document.getElementById('customCmd').addEventListener('keypress', function(e) {
                if(e.key === 'Enter') sendCustomCmd();
            });
            
            // Auto-update every 10 seconds
            setInterval(updateStatus, 10000);
            setInterval(updateLogs, 5000);
            
            // Initial load
            updateStatus();
            updateLogs();
            </script>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_command(self):
        cmd = self.path.split("/cmd/")[1].split("?")[0]
        cmd = cmd.replace("%20", " ").replace("%2F", "/")
        
        result = ""
        if cmd == "start":
            subprocess.Popen(["./start.sh"], cwd=SERVER_DIR, shell=True)
            result = "✅ Server starting..."
        elif cmd == "stop":
            self.send_to_console("stop")
            result = "✅ Stop command sent"
        elif cmd == "restart":
            self.send_to_console("stop")
            time.sleep(3)
            subprocess.Popen(["./start.sh"], cwd=SERVER_DIR, shell=True)
            result = "✅ Server restarting..."
        else:
            self.send_to_console(cmd)
            result = f"✅ Command sent: {cmd}"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(result.encode())
    
    def get_status(self):
        # Check if server is running
        check = subprocess.run(["pgrep", "-f", "server.jar"], capture_output=True)
        if check.returncode == 0:
            status = "🟢 SERVER IS ONLINE\nPort: 25565 (Java) | 19132 (Bedrock)"
        else:
            status = "🔴 SERVER IS OFFLINE"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(status.encode())
    
    def get_logs(self):
        log_file = os.path.join(SERVER_DIR, "logs", "latest.log")
        if os.path.exists(log_file):
            # Get last 20 lines
            result = subprocess.run(["tail", "-20", log_file], capture_output=True, text=True)
            logs = result.stdout
        else:
            logs = "No log file found"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(logs.encode())
    
    def send_to_console(self, command):
        """Send command to server console via pipe"""
        # Create command pipe if it doesn't exist
        if not os.path.exists(COMMAND_PIPE):
            os.mkfifo(COMMAND_PIPE)
        
        # Write command to pipe
        with open(COMMAND_PIPE, "w") as pipe:
            pipe.write(command + "\\n")

print("🎮 Minecraft Dashboard running at: http://127.0.0.1:8080/?pass=""" + PASSWORD + """")
print("🔒 Password: " + PASSWORD)
print("📁 Server directory: " + SERVER_DIR)
print("Press Ctrl+C to stop")
HTTPServer(('127.0.0.1', 8080), MinecraftHandler).serve_forever()
