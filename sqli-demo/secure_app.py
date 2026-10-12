"""
ҚОРҒАЛҒАН НҰСҚА
Параметрленген сұраныс (placeholder ?) қолданылады.
Енгізілген мәтін SQL команда ретінде емес, жай деректер ретінде өтеді.
Сол себепті ' OR 1=1-- деген шабуыл енді өтпейді.
"""
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="kk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Қорғалған нұсқа</title>
<style>
  :root { --accent:#1f6e52; --bg:#edf3ef; --card:#ffffff; --ink:#1b2a22; --mut:#6f8a7b; --line:#cfe0d5; }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:var(--bg); color:var(--ink); font:16px/1.5 system-ui, -apple-system, Segoe UI, sans-serif; padding:32px; }
  .card { width:100%; max-width:440px; background:var(--card); border:1px solid var(--line); border-radius:12px; padding:36px; }
  .tag { display:inline-block; font-size:13px; font-weight:600; color:var(--accent); background:#e2f0e8;
         padding:4px 10px; border-radius:6px; margin-bottom:14px; }
  h1 { font-size:22px; margin:0 0 24px; }
  label { display:block; font-size:14px; color:var(--mut); margin:16px 0 6px; }
  input { width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:8px; font-size:15px; }
  input:focus { outline:2px solid var(--accent); outline-offset:1px; }
  button { margin-top:22px; width:100%; padding:11px; border:none; border-radius:8px; background:var(--accent);
           color:#fff; font-size:15px; font-weight:600; cursor:pointer; }
  .panel { margin-top:22px; padding:16px; border-radius:8px; font-size:14px; }
  .panel.sql { background:#15231b; color:#cfe8da; font-family:Consolas, monospace; overflow-wrap:anywhere; }
  .panel.ok { background:#e2f0e8; color:#1f5c42; }
  .panel.err { background:#f3e8e0; color:#7a5230; }
</style>
</head>
<body>
<div class="card">
  <span class="tag">ҚОРҒАЛҒАН НҰСҚА</span>
  <h1>Кіру формасы</h1>
  <form method="post">
    <label>Email</label>
    <input name="email" autocomplete="off">
    <label>Password</label>
    <input name="password" type="password">
    <button type="submit">Кіру</button>
  </form>
  {% if query %}<div class="panel sql"><b>SQL:</b><br>{{ query }}<br><br><b>параметрлер:</b> {{ params }}</div>{% endif %}
  {% if result %}<div class="panel ok"><b>Нәтиже:</b> {{ result }}</div>{% endif %}
  {% if error %}<div class="panel err"><b>Қате:</b> {{ error }}</div>{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    query = params = result = error = None
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        # Дұрыс әдіс: "?" орынбасарлар, деректер бөлек беріледі.
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        params = (email, password)

        db = sqlite3.connect("users.db")
        try:
            row = db.execute(query, params).fetchone()
            if row:
                result = f"Кірдіңіз! id={row[0]}, email={row[1]}, is_admin={row[3]}"
            else:
                error = "Email немесе пароль қате."
        except sqlite3.Error as e:
            error = f"SQL қатесі: {e}"
        db.close()

    return render_template_string(TEMPLATE, query=query, params=params, result=result, error=error)

if __name__ == "__main__":
    app.run(port=5002, debug=False)
