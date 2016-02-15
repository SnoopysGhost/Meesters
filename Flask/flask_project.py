from flask import Flask
import jinja2
from bokeh.embed import components
from bokeh.plotting import figure, show, gridplot
from bokeh.models import ColumnDataSource
import sympy as sp
import numpy as np


# Defining default amplitude
default_a = 5


# Defining numpy function
def func(x, a=default_a):
    return x + a * np.sin(x)

# Defining sympy function for differentiation
x, a = sp.symbols('x a')
f_x = x**2 + a*sp.sin(x)
f_x_prime = sp.diff(f_x, x)
f_prime = sp.lambdify((x, a), f_x_prime, modules='numpy')

# Function range
x = np.linspace(1, 10, 100)

# Function values
y1 = func(x)
y2 = f_prime(x, default_a)

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


# Creating Jinja2 HTML template
template = jinja2.Template("""
<!DOCTYPE html>
<html lang="en-US">

<link
    href="http://cdn.pydata.org/bokeh/release/bokeh-0.11.1.min.css"
    rel="stylesheet" type="text/css">

<script
    src="http://cdn.pydata.org/bokeh/release/bokeh-0.11.1.min.js"
></script>

<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

<body>

    <h1>Function plot</h1>

    <p> Below is plotted a function with its derivative </p>
    <p> Data points can be selected by choosing the box select option in the toolbar </p>
    <p> The Function is:\n
        $$f(x) = x + 5sin(x)$$

    {{ script|safe }}

    {{ div|safe }}

</body>

</html>
""")

# Calling plotting Function
p = make_figure()

# Extracting HTML elements
script, div = components(p)

# Creating Flask app
app = Flask(__name__)


@app.route('/')
def function_plot():
    return template.render(script=script, div=div)

if __name__ == '__main__':
    app.run(debug=True)
