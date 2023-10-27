import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

juli_temp = ('../plottar/julitempovertid.png')

nav = st.sidebar.radio('Huvudmeny', ['Syfte', 'EDA', 'Locations', 'Nederbörd', 'Vind', 'Temperatur'])

if nav == 'Syfte':

    st.title('Jasså, det vill du allt bra veta va?')
    st.text('Vi vill klara skolan och få jobb och tjäna fett med casshhhhh!!!!')

if nav == 'EDA':

    st.title('Lol, fat chance')
    st.text('Choose plot to see:')
    df = pd.read_pickle('../dataframes/df_compiled_monthly_temp_gbg_save.pkl')
    first_year = df['Year'].min()
    last_year = df['Year'].max()
    
    col1, col2, col3 = st.columns(3)

    res_january = col1.button('January temp')
    res_february = col1.button('Febuary temp')
    res_march = col1.button('March temp')
    res_april = col1.button('April temp')
    res_may = col2.button('May temp')
    res_june = col2.button('June temp')
    res_july = col2.button('Junly temp')
    res_august = col2.button('August temp')
    res_september = col3.button('September temp')
    res_october = col3.button('October temp')
    res_november = col3.button('November temp')
    res_december = col3.button('December temp')    

    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    res_list = [res_january, res_february, res_march, res_april, res_may, res_june, res_july, res_august, res_september, res_october, res_november, res_december]
    res_list_str = ['res_january', 'res_february', 'res_march', 'res_april', 'res_may', 'res_june', 'res_july', 'res_august', 'res_september', 'res_october', 'res_november', 'res_december']

    for ind, val in enumerate(res_list):
        if val == True:
            button = (f'res_{month_list[ind]}')
            st.session_state.last_button = button
        elif 'last_button' not in st.session_state:
            st.session_state.last_button = None

    desired_start, desired_end = st.slider('Select timeframe (optional):', min_value=first_year, max_value=last_year, value=[first_year, last_year])
    desired_start = int(desired_start)
    desired_end = int(desired_end)
    
    st.session_state.desired_start = desired_start
    st.session_state.desired_end = desired_end

    button = st.session_state.last_button
    start = st.session_state.desired_start
    end = st.session_state.desired_end

    df = df[(df['Year'] >= start) & (df['Year'] <= end)]
    for ind, val in enumerate(res_list_str):
        if val == button:
            month = ind

    df = df[df['Month'] == month+1]
    fig, ax = plt.subplots()
    ax.scatter(x=df['Year'], y=df['Snittemperatur'])
    ax.set_title(f'Temperatures in {month_list[month]}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average daily temperature, Celcius')
    st.pyplot(fig)


if nav == 'Locations':
    st.title('Locations')
    st.text("The station in Gothenburg has changed locations throught the years. \nSince 1998 it's located by Gullbergsvass")
    df = pd.DataFrame(pd.read_csv('../data/station_info.csv'))
    df = df.rename(columns={'Latitud (decimalgrader)': 'LAT', 'Longitud (decimalgrader)': 'LON'})
    green_hex = '#06a94d'
    red_hex = '#EE0000'
    current = df['Tidsperiod (t.o.m)'].max()
    for ind, row in df.iterrows():
        if row['Tidsperiod (t.o.m)'] == current:
            df.at[ind, 'Colour'] = green_hex
        else:
            df.at[ind, 'Colour'] = red_hex

    st.map(df, color='Colour')
