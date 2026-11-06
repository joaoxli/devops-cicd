import os
import time

import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "app"),
    "password": os.getenv("DB_PASSWORD", "app"),
    "database": os.getenv("DB_NAME", "devops"),
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def get_conn(retries=15, delay=2):
    """Conecta no MySQL, tentando de novo enquanto o banco sobe."""
    for tentativa in range(1, retries + 1):
        try:
            return pymysql.connect(**DB_CONFIG)
        except pymysql.MySQLError as e:
            print(f"[db] tentativa {tentativa}/{retries} falhou: {e}", flush=True)
            time.sleep(delay)
    raise RuntimeError("Não foi possível conectar ao MySQL")


def init_db():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS recados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                autor VARCHAR(80) NOT NULL,
                mensagem VARCHAR(255) NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.get("/")
def index():
    return jsonify(
        projeto="CI/CD com Containers",
        status="rodando",
        endpoints=["GET /health", "GET /recados", "POST /recados"],
    )


@app.get("/health")
def health():
    try:
        with get_conn(retries=1) as conn, conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            cur.fetchone()
        return jsonify(api="ok", db="ok")
    except Exception as e:
        return jsonify(api="ok", db="erro", detalhe=str(e)), 503


@app.get("/recados")
def listar():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, autor, mensagem, criado_em FROM recados ORDER BY id DESC LIMIT 50")
        rows = cur.fetchall()
    for r in rows:
        r["criado_em"] = r["criado_em"].isoformat()
    return jsonify(rows)


@app.post("/recados")
def criar():
    dados = request.get_json(silent=True) or {}
    autor = str(dados.get("autor", "")).strip()[:80]
    mensagem = str(dados.get("mensagem", "")).strip()[:255]
    if not autor or not mensagem:
        return jsonify(erro="Informe 'autor' e 'mensagem'"), 400
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO recados (autor, mensagem) VALUES (%s, %s)", (autor, mensagem))
        novo_id = cur.lastrowid
    return jsonify(id=novo_id, autor=autor, mensagem=mensagem), 201


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
