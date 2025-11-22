# app.py - FINAL & ERROR-PROOF
from flask import Flask, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Default values in case DB is empty
    stats = {
        'entries': 0, 'exits': 0, 'peak': 0,
        'total_people': 0, 'avg_dwell': '0s', 'max_dwell': '0s',
        'session_time': 'No session yet', 'recent_sessions': []
    }

    if not os.path.exists('analytics.db'):
        return render_template('index.html', **stats)

    conn = sqlite3.connect('analytics.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get latest session
    c.execute("SELECT * FROM sessions ORDER BY id DESC LIMIT 1")
    session = c.fetchone()

    if session:
        stats['entries'] = session['total_entries'] or 0
        stats['exits'] = session['total_exits'] or 0
        stats['peak'] = session['peak_people'] or 0
        stats['session_time'] = session['start_time']

        # Dwell stats
        c.execute("""
            SELECT COUNT(*) as count, 
                   AVG(dwell_time_seconds) as avg_dwell,
                   MAX(dwell_time_seconds) as max_dwell
            FROM tracks WHERE session_id = ?
        """, (session['id'],))
        dwell = c.fetchone()
        stats['total_people'] = dwell['count'] or 0
        stats['avg_dwell'] = f"{dwell['avg_dwell'] or 0:.1f}s"
        stats['max_dwell'] = f"{dwell['max_dwell'] or 0:.1f}s"

    # Recent sessions
    c.execute("SELECT start_time FROM sessions ORDER BY id DESC LIMIT 5")
    stats['recent_sessions'] = [row[0] for row in c.fetchall()]

    conn.close()
    return render_template('index.html', **stats)

# Serve static files properly
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)