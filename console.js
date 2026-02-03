const http = require('http');
const fs = require('fs');

http.createServer((req, res) => {
    if (req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            const cmd = new URLSearchParams(body).get('cmd');
            // This sends the command to the Minecraft pipe we made in main.yml
            fs.appendFileSync('server_input', cmd + '\n');
            res.end('Command Sent: ' + cmd);
        });
    } else {
        // Simple HTML Interface
        res.end(`
            <form method="POST">
                <input name="cmd" placeholder="Enter command..." autofocus>
                <button>Send</button>
            </form>
            <script>if(window.history.replaceState){window.history.replaceState(null,null,window.location.href);}</script>
        `);
    }
}).listen(8080);
