from flask import Flask, render_template
import json
import plotly
import plotly.express as px
from core.utils import get_data
# Create Home Page Route
app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)