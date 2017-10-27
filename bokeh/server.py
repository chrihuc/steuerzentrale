# -*- coding: utf-8 -*-
"""
Created on Mon May 29 16:55:21 2017

@author: christoph
"""

from os.path import join, dirname
import datetime

import mysql.connector as sql
import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.palettes import Blues4
from bokeh.plotting import figure

STATISTICS = ['record_min_temp', 'actual_min_temp', 'average_min_temp', 'average_max_temp', 'actual_max_temp', 'record_max_temp']

def get_dataset(src, name):
    df = src[src.Name == name].copy()
    del df['Name']
    df['Date'] = pd.to_datetime(df.Date)
    # timedelta here instead of pd.DateOffset to avoid pandas bug < 0.18 (Pandas issue #11925)
    df['left'] = df.Date - datetime.timedelta(days=0.5)
    df['right'] = df.Date + datetime.timedelta(days=0.5)
    df = df.set_index(['Date'])
    df.sort_index(inplace=True)
    if distribution == 'Smoothed':
        window, order = 51, 3
        for key in STATISTICS:
            df[key] = savgol_filter(df[key], window, order)

    return ColumnDataSource(data=df)

def make_plot(source, title):
    plot = figure(x_axis_type="datetime", plot_width=800, tools="", toolbar_location=None)
    plot.title.text = title
#
#    plot.quad(top='record_max_temp', bottom='record_min_temp', left='left', right='right',
#              color=Blues4[2], source=source, legend="Record")
#    plot.quad(top='average_max_temp', bottom='average_min_temp', left='left', right='right',
#              color=Blues4[1], source=source, legend="Average")
#    plot.quad(top='actual_max_temp', bottom='actual_min_temp', left='left', right='right',
#              color=Blues4[0], alpha=0.5, line_color="black", source=source, legend="Actual")

    plot.line('Date', 'Value', source=source, line_width=3, line_alpha=0.6)
    # fixed attributes
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Temperature (degC)"
    plot.axis.axis_label_text_font_style = "bold"
    plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.3

    return plot

def update_plot(attrname, old, new):
    sensor = sensor_select.value
#    plot.title.text = "Weather data for " + cities[city]['title']
    df = pd.read_sql('SELECT * FROM Steuerzentrale.HIS_inputs order by id desc LIMIT 50000;', con=db_connection)
    src = get_dataset(df, sensors[sensor])
    source.data.update(src.data)

#city = 'Austin'
distribution = 'Discrete'

sensors = {'Wohnzimmer': 'V00WOH1RUM1TE01',
           'Aussentemperatur': 'A00TER1GEN1TE01',
           'Bad': 'V01BAD1RUM1TE01'}


sensor_select = Select(value='Wohnzimmer', title='Sensor', options=sorted(sensors.keys()))
#distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])

#df = pd.read_csv(join(dirname(__file__), 'data/Book1.csv'))
db_connection = sql.connect(host='192.168.192.10', database='Steuerzentrale', user='customer', password='user')
df = pd.read_sql('SELECT * FROM Steuerzentrale.HIS_inputs order by id desc LIMIT 50000;', con=db_connection)
source = get_dataset(df, 'V00WOH1RUM1TE01')
plot = make_plot(source, "Daten von")

sensor_select.on_change('value', update_plot)
#distribution_select.on_change('value', update_plot)

#controls = column(city_select, distribution_select)
controls = column(sensor_select)

curdoc().add_root(row(plot, controls))
#curdoc().add_root(row(plot))
curdoc().title = "Unterm Aspalter 22"# -*- coding: utf-8 -*-

