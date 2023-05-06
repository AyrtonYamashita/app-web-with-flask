from flask import Flask, render_template, request
import psycopg2
import time

app = Flask(__name__)

DATABASE_HOST = "db"
DATABASE_PORT = "5432"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "postgres"
app.config["DATABASE_URL"] = "postgresql://postgres:postgres@db:5432/mydb"


def connect():
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
    )
    return conn


def wait_for_db(max_attempts=5, interval=5):
    attempts = 0
    while attempts < max_attempts:
        try:
            conn = psycopg2.connect()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"Não foi possível conectar ao banco de dados: {e}")
            attempts += 1
            time.sleep(interval)
        return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    conn = connect()
    cur = conn.cursor()
    item = request.form["item"]
    cur.execute(
        "CREATE TABLE IF NOT EXISTS itens (id SERIAL PRIMARY KEY,\
        name VARCHAR(255) NOT NULL)"
    )
    cur.execute("INSERT INTO itens (name) VALUES (%s)", (item,))
    conn.commit()
    cur.close()
    conn.close()
    return render_template("index.html")


@app.route("/view")
def view():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM itens")
    itens = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("view.html", itens=itens)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
