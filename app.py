from datetime import datetime
from functools import wraps, update_wrapper
import json
import os.path as osp

from flask import Flask, request, render_template, send_from_directory, make_response
import plotly
from werkzeug.http import http_date
from werkzeug.utils import secure_filename

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
@nocache
def index():
    data = load('data.json')

    if request.method == 'POST':
        xkey = request.form.get('x')
        ykeys = request.form.getlist('y')
        xlog = request.form.get('xlog') is not None
        ylog = request.form.get('ylog') is not None

        plot(data, xkey, ykeys, xlog, ylog)

        return render_template('index.html', data=data, plot=True, xkey=xkey, ykeys=ykeys, xlog=xlog, ylog=ylog)

    return render_template('index.html', data=data, plot=False, xkey=None, ykeys=[])

@app.route('/plots/<filename>')
@nocache
def send_plot(filename):
    return send_from_directory('plots', filename)

def plot(data, xkey, ykeys, xlog, ylog):
    fig = plotly.graph_objects.Figure()
    for key in ykeys:
        fig.add_trace(plotly.graph_objects.Scatter(x=data[xkey], y=data[key], name=key))

    if xlog:
        fig.update_xaxes(type='log')
    if ylog:
        fig.update_yaxes(type='log')

    ytitle = ykeys[0] if len(ykeys) == 1 else 'value'
    fig.update_layout(xaxis_title=xkey, yaxis_title=ytitle)

    plotly.io.write_html(fig, './plots/plot.html')

# loads a json or dir of jsons
def load(path):
    if osp.isdir(path):
        data = {}
        files = glob.glob(osp.join(path, '*.json'))
        for f in files:
            key = osp.basename(f).rstrip('.json')
            data[key] = json.load(f)

    elif osp.isfile(path):
        with open(path, 'r') as f: 
            data = json.load(f)
    return data

if __name__=='__main__':
    main()
