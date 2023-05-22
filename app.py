import json
import time
import schedule

from datetime import datetime, timedelta, timezone
from threading import Lock

import plotly
import plotly.express as px
from flask import Flask, render_template, request
from flask_socketio import SocketIO

from core.utils import get_data

thread = None
thread_lock = Lock()
# Create Home Page Route
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


def background_thread():
    today = datetime.now(timezone.utc).astimezone()
    start_date = (datetime(today.year, today.month, today.day).astimezone() + timedelta(days=-7)).isoformat(sep="T", timespec="seconds")
    end_date = (datetime(today.year, today.month, today.day).astimezone() + timedelta(days=1)).isoformat(sep="T", timespec="seconds")
    print(f"take data from {start_date} to {end_date}")
    df = get_data(start_date, end_date)
    result = {
        'x': df['start_date'].to_list(),
        'y': df['Sum_per_hour'].to_list()
    }
    socketio.emit('data', result)


def launch_background_task():
    schedule.every().hour.at(":01").do(background_thread)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/mean')
def view_mean_by_hour():
    # route pour afficher les données de 01 Décembre jusqu'à 10 décembre
    start_date = '2022-12-01T00:00:00+01:00'
    end_date = '2022-12-11T00:00:00+01:00'
    # Students data available in a list of list
    df = get_data(start_date, end_date)

    # Create Bar chart
    fig = px.bar(
        df,
        x='start_date',
        y='mean_by_hour',
        barmode='group',
        labels={
            'start_date': 'Date/Heure de producution',
            'mean_by_hour': 'La moyenne de production nucléaire par heure par unité'
        })

    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # Use render_template to pass graphJSON to html
    return render_template('index.html', graphJSON=graphJSON)


@app.route('/')
def view_sum_by_hour():
    # route pour afficher les données de 01 Décembre jusqu'à 10 décembre
    start_date = '2022-12-01T00:00:00+01:00'
    end_date = '2022-12-11T00:00:00+01:00'
    # Students data available in a list of list
    df = get_data(start_date, end_date)

    # Create Bar chart
    fig = px.bar(
        df,
        x='start_date',
        y='Sum_per_hour',
        barmode='group',
        labels={
            'start_date': 'Date/Heure de producution',
            'Sum_per_hour': 'La somme de production nucléaire par heure'
        })

    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # Use render_template to pass graphJSON to html
    return render_template('index.html', graphJSON=graphJSON)


@app.route('/realtime')
def view_realtime_show():
    # Route pour Récuperer les données d'une période hebdomaidaire glissante et les afficher.
    today = datetime.now(timezone.utc).astimezone()
    start_date = (datetime(today.year, today.month, today.day).astimezone() + timedelta(days=-7)).isoformat(sep="T",
                                                                                                            timespec="seconds")
    end_date = (datetime(today.year, today.month, today.day).astimezone() + timedelta(days=1)).isoformat(sep="T",
                                                                                                         timespec="seconds")
    # Students data available in a list of list
    df = get_data(start_date, end_date)
    # Create Bar chart
    fig = px.bar(
        df,
        x='start_date',
        y='Sum_per_hour',
        barmode='group',
        labels={
            'start_date': 'Date/Heure de producution',
            'Sum_per_hour': 'La somme de production nucléaire par heure'
        })
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # Use render_template to pass graphJSON to html
    return render_template('realtime.html', graphJSON=graphJSON)

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(launch_background_task)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
