const http = require('http');
const fs = require('fs');
const path = require('path');
const suggestions = ["stop", "save-all", "op ", "deop ", "tp ", "gamemode creative", "gamemode survival", "kick ", "ban ", "pardon ", "whitelist add ", "whitelist remove", "list", "tps", "authme reload", "luckperms"];

http.createServer((req, res) => {
  if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      const params = new URLSearchParams(body);
      const cmd = params.get('cmd');
      if (cmd) { fs.appendFileSync('server_input', cmd + '\n'); }
      res.writeHead(302, {'Location': '/'});
      res.end();
    });
  } else if (req.url === '/fetch_logs') {
    const logPath = path.join(__dirname, 'logs', 'latest.log');
    if (fs.existsSync(logPath)) {
      const content = fs.readFileSync(logPath, 'utf8');
      const lines = content.split('\n').slice(-100).join('\n');
      res.end(lines);
    } else { res.end("Server starting..."); }
  } else {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(`<html><head><style>
      *{box-sizing:border-box;}
      body{background:#0c0c0c;color:#00ff41;font-family:monospace;margin:0;padding:20px;display:flex;flex-direction:column;height:100vh;overflow:hidden;}
      #log-win{background:#000;border:1px solid #333;padding:15px;flex-grow:1;overflow-y:auto;white-space:pre-wrap;margin-bottom:15px;font-size:13px;color:#00ff41;word-break:break-all;}
      .cmd-bar{display:flex;gap:10px;flex-shrink:0;padding-bottom:10px;}
      input{flex-grow:1;background:#1a1a1a;border:1px solid #444;color:white;padding:12px;border-radius:4px;outline:none;}
      button{background:#00ff41;color:black;border:none;padding:0 30px;border-radius:4px;cursor:pointer;font-weight:bold;}
    </style></head><body>
      <h3 style="color:white;margin:0 0 10px 0;">🛡️ Remote Terminal</h3>
      <div id="log-win">Loading Stream...</div>
      <form class="cmd-bar" method="POST">
        <input id="cmd-input" name="cmd" list="suggestions" placeholder="Type / to see commands..." autofocus autocomplete="off">
        <datalist id="suggestions">
          ${suggestions.map(s => `<option value="${s}">`).join('')}
          ${suggestions.map(s => `<option value="/${s}">`).join('')}
        </datalist>
        <button>RUN</button>
      </form>
      <script>
        const input = document.getElementById('cmd-input');
        input.addEventListener('input', (e) => {
          if (e.target.value === '/') {
            input.setAttribute('list', 'suggestions');
          }
        });
        let us=false; const w=document.getElementById('log-win');
        w.onscroll=()=>{us=w.scrollHeight-w.clientHeight>w.scrollTop+50};
        setInterval(()=>{fetch('/fetch_logs').then(r=>r.text()).then(d=>{w.innerText=d;if(!us)w.scrollTop=w.scrollHeight;})},2000);
      </script>
    </body></html>`);
  }
}).listen(8080);
