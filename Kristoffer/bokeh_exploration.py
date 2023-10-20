from bokeh.plotting import figure, show
import numpy as np
import pandas as pd
import seaborn as sns

monthly = pd.read_pickle("../Dataframes/df_monthly_temp.pkl")
juli = monthly.query("Month == 7")
december = monthly.query("Month == 12")

x = juli['Year']
y1 = juli['Monthly avg']
y2 = december['Monthly avg']

p = figure(title = 'Snittemperatur Juli och December', 
       x_axis_label = 'År', 
       y_axis_label = 'Temperatur i °C')

p.line(x, y1, legend_label= 'Juli', line_width=2, color = 'red')
p.line(x, y2, legend_label='December', line_width=2, color='blue')
show(p)