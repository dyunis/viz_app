from datetime import datetime
from functools import wraps, update_wrapper
import json
import os.path as osp
import re

from flask import Flask, request, render_template, send_from_directory, make_response, jsonify
import plotly
from werkzeug.http import http_date
from werkzeug.utils import secure_filename

app = Flask(__name__)

def main():
    if not osp.exists('plots'):
        os.makedirs('plots')

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

@app.route('/')
def index():
    global data
    data = load('data/data.json')
    return render_template('index.html', data=data, plot=True)

# post without a form
@app.route('/options', methods=['POST'])
def options():
    post_json = request.get_json()

    xkey = post_json['xkey']
    ykeys = post_json['ykeys']
    xlog = post_json['xlog']
    ylog = post_json['ylog']

    regex = re.compile("^r'.+'$")
    regexes = list(filter(lambda key: regex.match(key), ykeys))

    if len(regexes) > 0:
        ykeys = [key for key in ykeys if key not in regexes]

        regexes = list(map(lambda reg: reg.lstrip("r'").rstrip("'"), regexes))

        # should be a functional way to do this with reduce? turns out faster to set union all at once
        matches = list(map(lambda reg: set(filter(lambda key: bool(re.search(reg, key)), data.keys())), regexes))
        matches = set().union(*matches)

        for key in matches:
            if key not in ykeys:
                ykeys.append(key)

    plot(data, xkey, ykeys, xlog, ylog)
    
    return 'OK', 200


@app.route('/plots/<filename>')
@nocache
def send_plot(filename):
    return send_from_directory('plots', filename)

def plot(dset, xkey, ykeys, xlog=False, ylog=False):
    fig = plotly.graph_objects.Figure()
    for key in ykeys:
        fig.add_trace(plotly.graph_objects.Scatter(x=dset[xkey], y=dset[key], name=key))

    if xlog:
        fig.update_xaxes(type='log')
    if ylog:
        fig.update_yaxes(type='log')

    # general layout
    ytitle = ykeys[0] if len(ykeys) == 1 else 'value'
    legend = {'xanchor': 'left', 'x': 1.02, 'y': 1}
    fig.update_layout(xaxis_title=xkey, yaxis_title=ytitle, template='plotly_dark', legend=legend, font={'family': 'Arial'})

    # small color changes
    template = {'layout': {'paper_bgcolor': '#272727', 'plot_bgcolor': '#222', 'font': {'color': '#ccc'}}}
    fig.update_layout(template=template)

    # adding toggle to hide legend
    buttons = [{ 'visible': True, 
                 'label': 'legend',
                 'method': 'update',
                 'args': [{'showlegend': True}],
                 'args2':[{'showlegend': False}] }]
    fig.update_layout(updatemenus=[{'type': 'buttons', 'buttons': buttons, 'x': 1.02, 'xanchor': 'left', 'y': 1.02, 'yanchor': 'bottom'}])

    # editable would be nice but makes clicking on legend names impossible
    # maybe js button to toggle editable mode?
    config = {'responsive': True, 'scrollZoom': True, 'displayModeBar': True, 'editable': False}

    plotly.io.write_html(fig, './plots/plot.html', config=config)

# loads a json or dir of jsons
def load(path):
    if osp.isdir(path):
        dset = {}
        files = glob.glob(osp.join(path, '*.json'))
        for f in files:
            key = osp.basename(f).rstrip('.json')
            dset[key] = json.load(f)

    elif osp.isfile(path):
        with open(path, 'r') as f: 
            dset = json.load(f)

    return dset

if __name__=='__main__':
    main()
