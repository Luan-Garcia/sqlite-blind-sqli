from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'flag{Blind_SQLi_Is_Fun_123}')")
    c.execute("INSERT INTO users (username, password) VALUES ('guest', 'guest123')")
    conn.commit()
    return conn

db = init_db()

@app.route('/', methods=['GET', 'POST'])
def search():
    result = ""
    if request.method == 'POST':
        username = request.form.get('username')
        
        query = f"SELECT * FROM users WHERE username = '{username}'"
        
        try:
            cursor = db.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            
            if data:
                result = "<p style='color:green'>[+] Usuário encontrado no banco de dados.</p>"
            else:
                result = "<p style='color:red'>[-] Usuário não encontrado.</p>"
                
        except Exception as e:
            print(f"ERRO SQL: {e}")
            result = "<p style='color:gray'>Erro interno (Query falhou).</p>"

    html = """
    <h1>Pesquisa de Usuários (Interno)</h1>
    <form method="POST">
        Username: <input type="text" name="username">
        <button type="submit">Verificar</button>
    </form>
    {{ result|safe }}
    """
    return render_template_string(html, result=result)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.15.9', port=5000)
