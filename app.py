import sqlite3
import json
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from mhz14a import MHZ14A


app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')


db_name = "record.db"
connect = sqlite3.connect(db_name)
cursor = connect.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS co2
(
    created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    ppm INTEGER
)
''')
connect.commit()
connect.close()


scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@scheduler.task('interval', id='get_ppm', minutes=5, misfire_grace_time=30)
def get_ppm():
    co2 = MHZ14A("/dev/ttyS1")
    ppm = co2.get()
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO co2 (ppm) VALUES (?)
    ''', (ppm, ))
    conn.commit()
    conn.close()

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response


@app.route('/api/now')
def get_now():
    co2 = MHZ14A("/dev/ttyS1")
    ppm = co2.get()
    res = {"ppm": ppm}
    return res


@app.route('/api/all')
def get_all():
    db_name = "record.db"
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('''
            SELECT * FROM co2 
        ''')
    res = cur.fetchall()
    res = json.dumps(res)
    print(res)
    conn.commit()
    conn.close()
    return res


@app.route('/api/day')
def get_day():
    db_name = "record.db"
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM co2 WHERE created_at > DATETIME('now', '-1 days', 'localtime');
            ''')
    res = cur.fetchall()
    res = json.dumps(res)
    conn.commit()
    conn.close()
    return res


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
