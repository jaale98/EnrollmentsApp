from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'user_data.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              first_name TEXT NOT NULL,
              last_name TEXT NOT NULL,
              date_of_birth TEXT NOT NULL,
              insurance_plan TEXT NOT NULL,
              insurance_tier TEXT
            )
        ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        insurance_plan = request.form.get('insurance_plan')
        insurance_tier = request.form.get('insurance_tier') if insurance_plan != "Waive" else None

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (first_name, last_name, date_of_birth, insurance_plan, insurance_tier)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, date_of_birth, insurance_plan, insurance_tier))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)