from flask import Flask, render_template_string, jsonify, request
import time

app = Flask(__name__)

# O HTML_BASE contém agora a estrutura de Abas e todo o JavaScript dos jogos
HTML_BASE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>NeuroWorkspace Professional v2.0</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --primary: #2563eb; --bg: #f1f5f9; --surface: #ffffff;
            --text: #0f172a; --border: #e2e8f0; --success: #10b981;
        }
        body { margin: 0; font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); display: flex; height: 100vh; }
        
        /* Sidebar */
        .sidebar { width: 260px; background: #1e293b; color: white; padding: 20px; flex-shrink: 0; }
        .sidebar h2 { color: #38bdf8; font-size: 1.2rem; margin-bottom: 30px; }
        .nav-item { 
            padding: 12px; border-radius: 8px; cursor: pointer; margin-bottom: 10px;
            transition: 0.2s; display: flex; align-items: center; gap: 10px;
        }
        .nav-item:hover { background: #334155; }
        .nav-item.active { background: var(--primary); }

        /* Main Content */
        .main { flex-grow: 1; padding: 30px; overflow-y: auto; }
        .card { background: var(--surface); border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid var(--border); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* UI de Jogos */
        .question-box { background: #f8fafc; padding: 30px; border-radius: 12px; font-size: 1.8rem; text-align: center; margin: 20px 0; border: 2px solid var(--border); }
        .grid-options { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; }
        .btn-game { padding: 15px; border: 1px solid var(--border); border-radius: 8px; background: white; cursor: pointer; font-weight: bold; transition: 0.2s; }
        .btn-game:hover { border-color: var(--primary); background: #eff6ff; }
        
        /* Frações */
        .fractions-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; }
        .slice { fill: #fff; stroke: #333; cursor: pointer; stroke-width: 1; }
        .slice.selected { fill: var(--primary); }
    </style>
</head>
<body>

<div class="sidebar">
    <h2>🧠 NeuroWorkspace</h2>
    <div class="nav-item active" onclick="switchTab('tab-neuro')">🎮 Neuro Game</div>
    <div class="nav-item" onclick="switchTab('tab-frac')">🍕 Frações</div>
    <div class="nav-item" onclick="switchTab('tab-ang')">📐 Ângulos</div>
</div>

<div class="main">
    <div id="tab-neuro" class="tab-content active">
        <div class="card">
            <div id="neuro-area" style="font-weight: bold; color: var(--primary);">ÁREA: ÁLGEBRA</div>
            <div id="neuro-q" class="question-box">Carregando pergunta...</div>
            <div id="neuro-opts" class="grid-options"></div>
            <div style="margin-top: 20px;">
                <p>Pontuação: <span id="neuro-score">0</span></p>
            </div>
        </div>
    </div>

    <div id="tab-frac" class="tab-content">
        <div class="card">
            <h3>Pinte a Fração solicitada</h3>
            <div id="frac-grid" class="fractions-container"></div>
        </div>
    </div>

    <div id="tab-ang" class="tab-content">
        <div class="card" style="text-align: center;">
            <h3>Identifique o Ângulo</h3>
            <div id="ang-svg"></div>
            <div id="ang-opts" class="grid-options" style="max-width: 400px; margin: 20px auto;"></div>
        </div>
    </div>
</div>

<script>
    // --- GERENCIADOR DE ABAS ---
    function switchTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        event.currentTarget.classList.add('active');
    }

    // --- MÓDULO NEURO GAME ---
    let neuroScore = 0;
    function loadNeuro() {
        const q = { txt: "Se 2x + 4 = 12, quanto vale x?", ans: 4, opts: [2, 4, 6, 8] };
        document.getElementById('neuro-q').innerText = q.txt;
        const div = document.getElementById('neuro-opts');
        div.innerHTML = '';
        q.opts.forEach(o => {
            const b = document.createElement('button');
            b.className = 'btn-game';
            b.innerText = o;
            b.onclick = () => {
                if(o === q.ans) { 
                    confetti(); neuroScore += 10; 
                    document.getElementById('neuro-score').innerText = neuroScore;
                    loadNeuro();
                } else { alert("Tente novamente!"); }
            };
            div.appendChild(b);
        });
    }

    // --- MÓDULO FRAÇÕES ---
    function initFractions() {
        const grid = document.getElementById('frac-grid');
        grid.innerHTML = '';
        const desafios = [{n:2, d:4}, {n:3, d:8}, {n:1, d:3}];
        
        desafios.forEach((des, idx) => {
            const box = document.createElement('div');
            box.innerHTML = `<b>${des.n}/${des.d}</b><br>`;
            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttribute("viewBox", "0 0 100 100");
            svg.setAttribute("width", "100");

            for(let i=0; i<des.d; i++) {
                const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
                const startAngle = (i * 360) / des.d;
                const endAngle = ((i + 1) * 360) / des.d;
                p.setAttribute("d", drawSlice(50, 50, 40, startAngle, endAngle));
                p.className.baseVal = "slice";
                p.onclick = () => { 
                    p.classList.toggle('selected');
                    checkFrac(box, des.n);
                };
                svg.appendChild(p);
            }
            box.appendChild(svg);
            grid.appendChild(box);
        });
    }

    function drawSlice(x, y, r, start, end) {
        const s = polarToCart(x, y, r, end);
        const e = polarToCart(x, y, r, start);
        const arc = end - start <= 180 ? "0" : "1";
        return `M ${x} ${y} L ${s.x} ${s.y} A ${r} ${r} 0 ${arc} 0 ${e.x} ${e.y} Z`;
    }
    function polarToCart(cx, cy, r, ang) {
        const rad = (ang - 90) * Math.PI / 180.0;
        return { x: cx + (r * Math.cos(rad)), y: cy + (r * Math.sin(rad)) };
    }
    function checkFrac(box, n) {
        if(box.querySelectorAll('.selected').length === n) confetti();
    }

    // --- MÓDULO ÂNGULOS ---
    function initAngles() {
        const ang = 45;
        const svg = document.getElementById('ang-svg');
        svg.innerHTML = `
            <svg width="200" height="150">
                <line x1="50" y1="120" x2="150" y2="120" stroke="black" stroke-width="4"/>
                <line x1="50" y1="120" x2="130" y2="40" stroke="black" stroke-width="4"/>
            </svg>
        `;
        const opts = [30, 45, 90];
        const div = document.getElementById('ang-opts');
        div.innerHTML = '';
        opts.forEach(o => {
            const b = document.createElement('button');
            b.className = 'btn-game';
            b.innerText = o + '°';
            b.onclick = () => { if(o === 45) confetti(); };
            div.appendChild(b);
        });
    }

    // Inicialização Geral
    loadNeuro();
    initFractions();
    initAngles();

</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_BASE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)