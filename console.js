const http = require('http');
const fs = require('fs');
const path = require('path');
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
      res.end(content.split('\n').slice(-100).join('\n'));
    } else { res.end("Server starting..."); }
  } else {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(`<html><body style="background:#000;color:#0f0;font-family:monospace;"><h3>🛡️ Console</h3><pre id="l"></pre><form method="POST"><input name="cmd" autofocus><button>SEND</button></form><script>setInterval(()=>{fetch('/fetch_logs').then(r=>r.text()).then(d=>document.getElementById('l').innerText=d)},2000)</script></body></html>`);
  }
}).listen(8080);
