from flask import Flask, render_template
from flask.ext.wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required
from bokeh.embed import components
from bokeh.plotting import figure, show, gridplot, output_file
from bokeh.models import ColumnDataSource
import sympy as sp
import numpy as np


# Defining default amplitude
amp = 5


# Defining numpy function
def func(x, amp):
    return x + amp * np.sin(x)

# Defining sympy function for differentiation
x, a = sp.symbols('x a')
f_x = x**2 + a*sp.sin(x)
f_x_prime = sp.diff(f_x, x)
f_prime = sp.lambdify((x, a), f_x_prime, modules='numpy')

# Function range
x = np.linspace(1, 10, 100)

# Function values
y1 = func(x, amp)
y2 = f_prime(x, amp)

# Compiling data into dictionary for linked plotting
source = ColumnDataSource(data=dict(x=x, y1=y1, y2=y2))

# Interaction tools
TOOLS = 'box_select, help, reset, resize'


# Figure plotting function
def make_figure():
    top = figure(tools=TOOLS, width=600, height=400,
                 x_axis_label='x',
                 y_axis_label='f(x)')

    top.line('x', 'y1', source=source, line_width=2)
    top.scatter('x', 'y1', source=source, size=0)

    bottom = figure(tools=TOOLS, width=600, height=400,
                    x_axis_label='x',
                    y_axis_label="f(x)'")
    bottom.line('x', 'y2', source=source, alpha=1, line_width=2)
    bottom.scatter('x', 'y2', source=source, size=0)

    plot = gridplot([[top], [bottom]])

    show(plot)
    return plot



# Calling plotting Function
p = make_figure()


# Extracting HTML elements
script, div = components(p)

# Creating Flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/templates/plot.html')
def function_plot():
    return render_template('plot.html', script=script, div=div)


if __name__ == '__main__':
    app.run(debug=True)
