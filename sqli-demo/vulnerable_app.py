"""
ОСАЛ НҰСҚА (тек оқу мақсатында!)
SQL сұранысы пайдаланушы енгізген мәтінмен тікелей құрастырылады.
Login формасына:  email = ' OR 1=1--   паролі = кез келген
деп жазсаңыз, парольсіз-ақ admin ретінде кіресіз.
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
<title>Осал нұсқа</title>
<style>
  :root { --accent:#b3463a; --bg:#f6efed; --card:#ffffff; --ink:#2a1e1c; --mut:#8a716c; --line:#e3d2ce; }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:var(--bg); color:var(--ink); font:16px/1.5 system-ui, -apple-system, Segoe UI, sans-serif; padding:32px; }
  .card { width:100%; max-width:440px; background:var(--card); border:1px solid var(--line); border-radius:12px; padding:36px; }
  .tag { display:inline-block; font-size:13px; font-weight:600; color:var(--accent); background:#f6e4e1;
         padding:4px 10px; border-radius:6px; margin-bottom:14px; }
  h1 { font-size:22px; margin:0 0 24px; }
  label { display:block; font-size:14px; color:var(--mut); margin:16px 0 6px; }
  input { width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:8px; font-size:15px; }
  input:focus { outline:2px solid var(--accent); outline-offset:1px; }
  button { margin-top:22px; width:100%; padding:11px; border:none; border-radius:8px; background:var(--accent);
           color:#fff; font-size:15px; font-weight:600; cursor:pointer; }
  .panel { margin-top:22px; padding:16px; border-radius:8px; font-size:14px; }
  .panel.sql { background:#241a18; color:#e9d3cf; font-family:Consolas, monospace; overflow-wrap:anywhere; }
  .panel.ok { background:#eaf3ea; color:#2f5c33; }
  .panel.err { background:#f6e4e1; color:#7c3329; }
</style>
</head>
<body>
<div class="card">
  <span class="tag">ОСАЛ НҰСҚА</span>
  <h1>Кіру формасы</h1>
  <form method="post">
    <label>Email</label>
    <input name="email" autocomplete="off">
    <label>Password</label>
    <input name="password" type="password">
    <button type="submit">Кіру</button>
  </form>
  {% if query %}<div class="panel sql"><b>SQL:</b><br>{{ query }}</div>{% endif %}
  {% if result %}<div class="panel ok"><b>Нәтиже:</b> {{ result }}</div>{% endif %}
  {% if error %}<div class="panel err"><b>Қате:</b> {{ error }}</div>{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    query = result = error = None
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        # ЕСКЕРТУ: мәтінді тікелей сұранысқа қосу — SQL Injection-ға ашық!
        query = (f"SELECT * FROM users WHERE email = '{email}' "
                 f"AND password = '{password}'")

        db = sqlite3.connect("users.db")
        try:
            row = db.execute(query).fetchone()
            if row:
                result = f"Кірдіңіз! id={row[0]}, email={row[1]}, is_admin={row[3]}"
            else:
                error = "Email немесе пароль қате."
        except sqlite3.Error as e:
            error = f"SQL қатесі: {e}"
        db.close()

    return render_template_string(TEMPLATE, query=query, result=result, error=error)

if __name__ == "__main__":
    app.run(port=5001, debug=False)
