from flask import Flask
import redis
import os # Importamos a biblioteca do sistema

app = Flask(__name__)

# Agora o Python pergunta ao Docker quem é o Redis, em vez de adivinhar
redis_host = os.environ.get('REDIS_HOST', 'redis')
cache = redis.Redis(host=redis_host, port=6379)

@app.route('/')
def hello():
    count = cache.incr('visitas')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Status da API</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #0f172a;
                color: #f8fafc;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background-color: #1e293b;
                padding: 2.5rem 4rem;
                border-radius: 16px;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
                text-align: center;
                border: 1px solid #334155;
            }}
            h1 {{
                margin-top: 0;
                color: #38bdf8;
                font-size: 1.5rem;
            }}
            .count-box {{
                background-color: #0f172a;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1.5rem 0;
                border: 1px solid #38bdf8;
            }}
            .count-number {{
                font-size: 4rem;
                font-weight: bold;
                color: #e2e8f0;
                margin: 0;
                line-height: 1;
            }}
            .badge {{
                background: #10b981;
                color: white;
                padding: 4px 12px;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Projeto DevOps - T02</h1>
            <span class="badge">API Online</span>
            
            <div class="count-box">
                <p style="margin: 0 0 10px 0; color: #94a3b8; font-size: 0.9rem;">Total de Visitas Registadas</p>
                <p class="count-number">{count}</p>
            </div>
            
            <p style="margin: 0; color: #64748b; font-size: 0.85rem;">Dados guardados num volume Redis</p>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)