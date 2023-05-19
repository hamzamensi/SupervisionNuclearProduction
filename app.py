from datetime import datetime, timedelta, timezone

from flask import Flask, render_template, request
import json
import plotly
import plotly.express as px
from core.utils import get_data
from flask_socketio import SocketIO
from threading import Lock

thread = None
thread_lock = Lock()
# Create Home Page Route
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

def background_thread():
    print("Generating random sensor values")
    # Students data available in a list of list
    while True:
        start_date = (datetime.now(timezone.utc).astimezone() + timedelta(days=-7)).isoformat(sep="T", timespec="seconds")
        end_date = (datetime.now(timezone.utc).astimezone() + timedelta(days=1)).isoformat(sep="T", timespec="seconds")
        df = get_data(start_date, end_date)
        print(len(df))
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
        print(graphJSON)
        socketio.emit('data', graphJSON)
        socketio.sleep(180)



@app.route('/')
def bar_with_plotly():
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
def realtime_show():
    start_date = (datetime.now(timezone.utc).astimezone() + timedelta(days=-7)).isoformat(sep="T", timespec="seconds")
    end_date = datetime.now(timezone.utc).astimezone().isoformat(sep="T", timespec="seconds")
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
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)