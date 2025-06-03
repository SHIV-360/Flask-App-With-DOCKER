from flask import Flask, request, redirect, render_template_string
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        port='5432',
        database='mydb',
        user='postgres',
        password='pass123'
    )

def ensure_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        create table if not exists users (
            id serial primary key,
            name varchar(50),
            age int
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cur.execute("insert into users (name, age) values (%s, %s)", (name, age))
        conn.commit()
        return redirect('/')

    cur.execute('select * from users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>USER DATABASE</title>
      <style>
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: #121212;
          color: #eee;
          margin: 0;
          padding: 2rem;
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        h1 {
          color: #ff4081;
          margin-bottom: 1rem;
        }
        form {
          background: #1f1f1f;
          padding: 1rem 2rem;
          border-radius: 10px;
          margin-bottom: 2rem;
          box-shadow: 0 0 10px #ff4081aa;
          display: flex;
          gap: 1rem;
          align-items: center;
        }
        input[type="text"],
        input[type="number"] {
          padding: 0.5rem 1rem;
          border-radius: 5px;
          border: none;
          outline: none;
          font-size: 1rem;
          width: 150px;
          background: #333;
          color: #eee;
        }
        input[type="submit"] {
          background: #ff4081;
          border: none;
          padding: 0.6rem 1.2rem;
          color: white;
          font-weight: bold;
          border-radius: 5px;
          cursor: pointer;
          transition: background-color 0.3s ease;
        }
        input[type="submit"]:hover {
          background: #e73370;
        }
        table {
          border-collapse: collapse;
          width: 70vw;
          max-width: 600px;
          box-shadow: 0 0 10px #ff4081aa;
          background: #1f1f1f;
          border-radius: 10px;
          overflow: hidden;
        }
        th, td {
          padding: 1rem;
          text-align: center;
          border-bottom: 1px solid #333;
        }
        th {
          background: #ff4081;
          color: white;
          font-weight: 600;
          text-transform: uppercase;
        }
        tr:hover {
          background: #2c2c2c;
        }
        @media (max-width: 600px) {
          table {
            width: 100vw;
          }
          form {
            flex-direction: column;
            gap: 0.5rem;
          }
          input[type="text"],
          input[type="number"] {
            width: 100%;
          }
        }
      </style>
    </head>
    <body>
      <h1>USER DATABASE</h1>
      <form method="post" autocomplete="off">
        <input name="name" type="text" placeholder="name" required />
        <input name="age" type="number" placeholder="age" min="1" max="150" required />
        <input type="submit" value="add" />
      </form>
      <table>
        <tr><th>id</th><th>name</th><th>age</th></tr>
        {% for u in users %}
          <tr><td>{{ u[0] }}</td><td>{{ u[1] }}</td><td>{{ u[2] }}</td></tr>
        {% endfor %}
      </table>
    </body>
    </html>
    ''', users=users)

if __name__ == '__main__':
    ensure_table()
    app.run(debug=True)
