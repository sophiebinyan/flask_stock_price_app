from flask import Flask, Blueprint, g, flash, redirect, render_template, request, url_for
app = Flask(__name__, instance_relative_config=True)

import os
import quandl
import pandas as pd

quandl.ApiConfig.api_key=os.environ.get('QUANDL_KEY')

from bokeh.embed import components
from bokeh.plotting import figure,show
from bokeh.resources import CDN
from bokeh.models import Legend
from math import pi
bokeh_css = CDN.render_css()
bokeh_js = CDN.render_js()

#===========================================
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        return redirect(url_for('graph', tickerSymbol=request.form['tickerSymbol']))
    """Show homepage."""
    return render_template('index.html')

#==========================================
@app.route('/<tickerSymbol>/', methods=('GET', 'POST'))
def graph(tickerSymbol):
    if request.method == 'POST':
        return redirect(url_for('graph', tickerSymbol=request.form['tickerSymbol']))
        
    df = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', 'close','open','adj_close','adj_open'] },date = { 'gte': '2018-01-01', 'lte': '2018-01-31' })
    p = figure(width=500, height=500,x_axis_type='datetime', tools='xpan,xwheel_zoom,box_zoom,reset,save', title='Quandl WIKI EOD Stock Prices: Jaunary, 2018')
    p.xaxis.major_label_orientation = pi/6
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    a=df[df['ticker']==tickerSymbol].copy()
    r1=p.line(a['date'],a['close'],color='blue',line_dash='solid')
    r2=p.line(a['date'],a['adj_close'],color='blue',line_dash='dashed')
    r3=p.line(a['date'],a['open'],color='red',line_dash='solid')
    r4=p.line(a['date'],a['adj_open'],color='red',line_dash='dashed')

    legend = Legend(items=[("close price",   [r1]),("adjusted close price", [r2]), \
                           ("open price", [r3]),("adjusted open price",   [r4])], location=(0, 0))
    p.add_layout(legend, 'right')
    plot_script, plot_div = components(p)
    return render_template('graph.html', tickerSymbol=tickerSymbol, bokeh_css=bokeh_css, bokeh_js=bokeh_js, plot_div=plot_div, plot_script=plot_script)
            
#==================================
if __name__ == '__main__':
    app.run()
