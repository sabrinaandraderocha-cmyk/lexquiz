from flask import Flask, render_template, request, redirect, url_for, session, flash
from whitenoise import WhiteNoise
import random
import secrets
import os

# =========================================================
# APP
# =========================================================
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

# WhiteNoise para servir /static no Render (css/imagens)
# root precisa apontar para a pasta "static" do projeto
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.wsgi_app = WhiteNoise(app.wsgi_app, root=STATIC_DIR, prefix="static/")

# Sessão: use uma chave fixa via env no Render (recomendado)
# No Render: Settings -> Environment -> SECRET_KEY = (uma string grande)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(24)

# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================
APP_NAME = "LexQuiz"

AREAS = [
    "Direito Civil",
    "Direito Penal",
    "Direito Constitucional",
    "Processo Civil",
    "Processo Penal",
    "Ética"
]

# =========================================================
# BANCO DE QUESTÕES
# (mantive o seu conteúdo como estava; pode continuar colando abaixo)
# =========================================================
QUESTIONS = [
    # -------------------- DIREITO CIVIL (Geral) --------------------
    {"id": 1, "area": "Direito Civil", "q": "A personalidade civil da pessoa começa, em regra:", "options": ["na concepção", "no nascimento com vida", "aos 18 anos", "no registro civil"], "answer": 1, "explain": "Em regra, a personalidade civil começa com o nascimento com vida."},
    {"id": 2, "area": "Direito Civil", "q": "Capacidade de direito é:", "options": ["aptidão para ser titular de direitos e deveres", "aptidão para praticar atos sozinho", "poder de representar alguém", "condição exclusiva de maiores de idade"], "answer": 0, "explain": "Capacidade de direito é a aptidão genérica para ter direitos e deveres."},
    {"id": 3, "area": "Direito Civil", "q": "Em regra, a maioridade civil ocorre aos:", "options": ["16 anos", "18 anos", "21 anos", "14 anos"], "answer": 1, "explain": "A regra geral é 18 anos para a maioridade civil."},
    {"id": 4, "area": "Direito Civil", "q": "Domicílio da pessoa natural, em regra, é:", "options": ["onde nasceu", "onde trabalha", "onde estabelece residência com ânimo definitivo", "onde tem família"], "answer": 2, "explain": "Domicílio, em regra, é a residência com intenção de permanência."},
    {"id": 5, "area": "Direito Civil", "q": "Pessoa jurídica é:", "options": ["qualquer pessoa maior de idade", "ente criado pela lei, com personalidade própria", "apenas órgão público", "apenas empresa com lucro"], "answer": 1, "explain": "Pessoa jurídica tem personalidade própria, distinta das pessoas que a compõem."},
    {"id": 6, "area": "Direito Civil", "q": "Bens móveis são, em regra:", "options": ["os que não podem ser transportados", "os que podem ser transportados sem alteração substancial", "somente imóveis", "somente dinheiro"], "answer": 1, "explain": "Bens móveis podem ser transportados sem alteração da substância."},
    {"id": 7, "area": "Direito Civil", "q": "Negócio jurídico é, em geral:", "options": ["qualquer conversa", "manifestação de vontade que produz efeitos jurídicos", "qualquer ato ilícito", "somente contrato escrito"], "answer": 1, "explain": "Negócio jurídico é manifestação de vontade com efeitos no mundo jurídico."},
    {"id": 8, "area": "Direito Civil", "q": "Um contrato, em regra, exige:", "options": ["acordo de vontades", "apenas assinatura em cartório", "sempre duas testemunhas", "sempre forma pública"], "answer": 0, "explain": "O essencial é o acordo de vontades, respeitada a forma exigida em casos específicos."},
    {"id": 9, "area": "Direito Civil", "q": "A boa-fé objetiva se relaciona a:", "options": ["um sentimento interno", "padrão de conduta leal e cooperativo", "direito penal", "apenas promessa verbal"], "answer": 1, "explain": "Boa-fé objetiva é padrão de conduta esperado nas relações jurídicas."},
    {"id": 10, "area": "Direito Civil", "q": "Responsabilidade civil, em regra, visa:", "options": ["punir com prisão", "reparar dano causado", "anular qualquer contrato", "criar imposto"], "answer": 1, "explain": "A responsabilidade civil tem foco na reparação do dano."},

    # ... (COLE O RESTO DAS SUAS QUESTÕES AQUI, sem mudar a estrutura)
]

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def get_questions_by_area(area: str):
    return [q for q in QUESTIONS if q.get("area") == area]

def q_by_id(qid: int):
    for q in QUESTIONS:
        if q.get("id") == qid:
            return q
    return None

def build_quiz(area: str, mode: str, n: int):
    pool = get_questions_by_area(area)

    # protege: não pede mais do que existe
    n = min(n, len(pool))

    # seleciona SEM repetição
    selected = random.sample(pool, k=n) if n > 0 else []

    return {
        "area": area,
        "mode": mode,
        "n": n,
        "items": [q["id"] for q in selected],
        "pos": 0,
        "score": 0,
        "answers": [],
    }

# =========================================================
# ROTAS
# =========================================================
@app.get("/")
def index():
    counts = {a: 0 for a in AREAS}
    for q in QUESTIONS:
        a = q.get("area")
        if a in counts:
            counts[a] += 1

    return render_template(
        "index.html",
        app_name=APP_NAME,
        areas=AREAS,
        total_questions=len(QUESTIONS),
        counts=counts
    )

@app.post("/start")
def start():
    area = request.form.get("area", "")
    mode = request.form.get("mode", "treino")
    n_raw = request.form.get("n", "10")

    if area not in AREAS:
        flash("Escolha uma área válida.")
        return redirect(url_for("index"))

    try:
        n = int(n_raw)
        n = max(5, min(20, n))
    except ValueError:
        n = 10

    quiz = build_quiz(area, mode, n)

    if not quiz["items"]:
        flash(f"Ainda não há perguntas cadastradas para {area}.")
        return redirect(url_for("index"))

    session["quiz"] = quiz
    session.pop("last_feedback", None)
    return redirect(url_for("question"))

@app.get("/q")
def question():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("index"))

    pos = quiz["pos"]
    if pos >= quiz["n"]:
        return redirect(url_for("result"))

    qid = quiz["items"][pos]
    q = q_by_id(qid)
    if not q:
        flash("Erro ao carregar pergunta.")
        return redirect(url_for("index"))

    time_limit = 20 if quiz["mode"] == "prova" else None

    return render_template(
        "quiz.html",
        app_name=APP_NAME,
        quiz=quiz,
        q=q,
        pos=pos,
        time_limit=time_limit
    )

@app.post("/answer")
def answer():
    quiz = session.get("quiz")
    if not quiz:
        flash("Sessão expirada. Inicie novo quiz.")
        return redirect(url_for("index"))

    pos = quiz["pos"]
    if pos >= quiz["n"]:
        return redirect(url_for("result"))

    qid = quiz["items"][pos]
    q = q_by_id(qid)
    if not q:
        flash("Pergunta inválida.")
        return redirect(url_for("index"))

    chosen_raw = request.form.get("choice", "")
    try:
        chosen = int(chosen_raw)
    except ValueError:
        chosen = -1

    correct = q["answer"]
    is_correct = (chosen == correct)

    if is_correct:
        quiz["score"] += 1

    quiz["answers"].append({
        "id": qid,
        "chosen": chosen,
        "correct": correct,
        "is_correct": is_correct
    })

    quiz["pos"] += 1
    session["quiz"] = quiz

    if quiz["mode"] == "treino":
        session["last_feedback"] = {
            "qid": qid,
            "is_correct": is_correct,
            "explain": q.get("explain", "")
        }
    else:
        session.pop("last_feedback", None)

    return redirect(url_for("question"))

@app.get("/result")
def result():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("index"))

    details = []
    for a in quiz["answers"]:
        q = q_by_id(a["id"])
        if not q:
            continue

        q_data = {
            "area": q["area"],
            "q": q["q"],
            "options": q["options"],
            "chosen": a["chosen"],
            "correct": a["correct"],
            "is_correct": a["is_correct"],
            "explain": q.get("explain", ""),
        }
        if "difficulty" in q:
            q_data["difficulty"] = q["difficulty"]

        details.append(q_data)

    wrong_ids = [a["id"] for a in quiz["answers"] if not a.get("is_correct")]
    session["wrong_ids"] = wrong_ids

    per_area = {}
    for d in details:
        area = d["area"]
        if area not in per_area:
            per_area[area] = {"total": 0, "correct": 0}
        per_area[area]["total"] += 1
        if d["is_correct"]:
            per_area[area]["correct"] += 1

    session["last_per_area"] = per_area

    return render_template(
        "result.html",
        app_name=APP_NAME,
        quiz=quiz,
        details=details,
        per_area=per_area
    )

@app.get("/review")
def review():
    wrong_ids = session.get("wrong_ids", [])
    if not wrong_ids:
        flash("Você não tem erros para revisar ainda.")
        return redirect(url_for("index"))

    n_review = min(20, len(wrong_ids))

    quiz = {
        "area": "Revisão de Erros",
        "mode": "treino",
        "n": n_review,
        "items": wrong_ids[:n_review],
        "pos": 0,
        "score": 0,
        "answers": [],
    }

    session["quiz"] = quiz
    session.pop("last_feedback", None)
    return redirect(url_for("question"))

@app.get("/reset")
def reset():
    session.pop("quiz", None)
    session.pop("last_feedback", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
