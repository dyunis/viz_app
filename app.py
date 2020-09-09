from datetime import datetime
from functools import wraps, update_wrapper
import json

from flask import Flask, request, render_template, redirect, send_from_directory, make_response
import plotly
import plotly.graph_objects as go
from werkzeug.http import http_date
from werkzeug.utils import secure_filename

app = Flask(__name__)

# stop caching plot.html
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def main():
    app.run(debug=True)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = http_date(datetime.now())
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

# no cacheing at all
# @app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/', methods=['GET', 'POST'])
@nocache
def index():
    with open('data.json', 'r') as f: 
        data = json.load(f)

    if request.method == 'POST':
        xkey = request.form.get('x')
        ykeys = request.form.getlist('y')

        # make fig with plotly
        fig = go.Figure()
        for key in ykeys:
            fig.add_trace(go.Scatter(x=data[xkey], y=data[key], name=key))

        plot_html = plotly.io.write_html(fig, './plots/plot.html')

        return render_template('index.html', data=data, plot=True, xkey=xkey, ykeys=ykeys)

    return render_template('index.html', data=data, plot=False, xkey=None, ykeys=[])

@app.route('/plots/<filename>')
@nocache
def send_plot(filename):
    return send_from_directory('plots', filename)

if __name__=='__main__':
    main()
