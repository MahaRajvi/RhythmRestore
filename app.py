from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pandas as pd
from src.recommender import get_recommendations

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for session management

# Connect to DB
def get_db_connection():
    conn = sqlite3.connect('data/rhythm_restore.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Register Page
from src.send_sms import send_sms  # import this at top if not already

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        welcome_message = "Welcome to Rhythm Restore!"

        # Comment out SMS sending for now
        send_sms(phone, welcome_message)

        # Continue normal flow
        return redirect(url_for('input_page'))
    return render_template('register.html')



# Input Daily Data Page
@app.route('/input')
def input_page():
    return render_template('input.html')

# After Form Submit - Recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = {
        "sleep_time": request.form.get("sleep_time"),
        "wake_time": request.form.get("wake_time"),
        "meals_skipped": request.form.get("meals_skipped"),
        "stress": int(request.form.get("stress")),
        "mood": request.form.get("mood"),
        "traffic": request.form.get("traffic"),
        "screen_time": request.form.get("screen_time")  # Don't cast to int here
    }
    results = get_recommendations(user_input)

    # Save today's input
    session['today_input'] = user_input
    session['today_recommendations'] = results

    # Calculate sleep duration
    try:
        sleep = pd.to_datetime(user_input['sleep_time'])
        wake = pd.to_datetime(user_input['wake_time'])
        sleep_hours = (wake - sleep).seconds / 3600
        if sleep_hours < 0:
            sleep_hours += 24
    except:
        sleep_hours = 7.0  # default

    # Insert today's initial progress (stars will be updated after feedback)
    conn = get_db_connection()
    conn.execute('INSERT INTO progress (sleep, stress, stars) VALUES (?, ?, ?)', 
                 (sleep_hours, user_input['stress'], 0))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'today_recommendations' not in session:
        return redirect('/input')
    today = session['today_recommendations']
    return render_template('dashboard.html', today=today)

# Feedback Page
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Submit Feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    sleep_improved = request.form.get('sleep_improved')
    followed_diet = request.form.get('followed_diet')

    stars = 0
    if sleep_improved == 'yes':
        stars += 1
    if followed_diet == 'yes':
        stars += 1

    conn = get_db_connection()
    conn.execute('UPDATE progress SET stars = ? WHERE id = (SELECT MAX(id) FROM progress)', (stars,))
    
    # Insert into feedbacks table
    conn.execute('INSERT INTO feedbacks (sleep_improved, followed_diet, stars_earned) VALUES (?, ?, ?)',
                 (sleep_improved, followed_diet, stars))
    conn.commit()
    conn.close()

    session['stars_earned'] = stars
    return redirect('/starjar')


# Star Jar Page
@app.route('/starjar')
def starjar():
    stars = session.get('stars_earned', 0)
    return render_template('starjar.html', total_stars=stars)

# Weekly Progress Page
@app.route('/progress')
def progress():
    conn = get_db_connection()
    rows = conn.execute('SELECT sleep, stress, stars FROM progress ORDER BY id DESC LIMIT 7').fetchall()
    conn.close()

    progress = []
    total_stars = 0
    day = len(rows)

    for row in reversed(rows):  # show from Day 1 to Day 7
        sleep = float(row['sleep'])
        stress = int(row['stress'])
        stars = int(row['stars'])
        progress.append((day, sleep, stress, stars))
        total_stars += stars
        day -= 1

    return render_template('progress.html', progress=progress, total_stars=total_stars)
@app.route('/progress_graph')
def progress_graph():
    import matplotlib
    matplotlib.use('Agg')  # ✅ Force non-GUI backend

    import matplotlib.pyplot as plt
    import io
    import base64
    from flask import Response
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect('data/rhythm_restore.db')
    query = "SELECT sleep, stress FROM progress ORDER BY id DESC LIMIT 7"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = df[::-1].reset_index(drop=True)
    df.index = [f"Day {i+1}" for i in range(len(df))]

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(df.index, df['sleep'], marker='o', color='blue', label='Sleep')
    ax1.set_ylabel('Sleep Hours', color='blue')
    ax1.set_ylim(0, 10)
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(df.index, df['stress'], marker='s', color='red', label='Stress')
    ax2.set_ylabel('Stress Level (1–5)', color='red')
    ax2.set_ylim(0, 6)
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('📊 Sleep & Stress Trend (Past 7 Days)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')  # ✅ Save to buffer
    buf.seek(0)

    return Response(buf.getvalue(), mimetype='image/png')

# Admin Login Page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect('/admin_dashboard')
        else:
            return "Invalid credentials. Try again."
    return render_template('admin_login.html')

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    conn = get_db_connection()
    feedbacks = conn.execute('SELECT * FROM feedbacks').fetchall()

    # Count sleep improvements
    sleep_yes = conn.execute('SELECT COUNT(*) FROM feedbacks WHERE sleep_improved = "yes"').fetchone()[0]
    sleep_no = conn.execute('SELECT COUNT(*) FROM feedbacks WHERE sleep_improved = "no"').fetchone()[0]
    conn.close()

    return render_template('admin_dashboard.html', feedbacks=feedbacks, sleep_yes=sleep_yes, sleep_no=sleep_no)


# Admin Logout
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
