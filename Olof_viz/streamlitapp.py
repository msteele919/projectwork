import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# juli_temp = ('../plottar/julitempovertid.png')

nav = st.sidebar.radio('Huvudmeny', ['Bakgrund', 'Frågeställning' 'EDA', 'Platser', 'Nederbörd', 'Vind', 'Temperatur', 'Sommarens och vinterns ankomst'])

if nav == 'Bakgrund':

    st.title('Jasså, det vill du allt bra veta va?')
    st.text('''1. Kan man med hjälp av historisk väderdata se trender kring förändringar i vädret?
            
            \nHur har temperaturen ändrats sedan första datan?
            \nHar regn blivit mer intensivt under de senaste 50 åren? (Definiera intensivt)
	        \nFlera dagar med regn? Har totala nederbörden ökat/minskat mellan åren?
            \nHar åskoväder och stormar blivit mer intensiva under de senaste 50 åren? - sekundär
            \nHur har snödjupet ändrats över tid? 
            \nKan vi förutspå hur vädret ser ut i till exempel juli 2028?''')


if nav == 'EDA':
    # st.session_state
    st.title('Lol, fat chance')
    st.text('Välj månad att se:')
    df = pd.read_pickle('../dataframes/df_compiled_monthly_temp_gbg_save.pkl')
    first_year = df['Year'].min()
    last_year = df['Year'].max()
    
    col1, col2, col3 = st.columns(3)

    res_January = col1.button('January temp')
    res_February = col1.button('Febuary temp')
    res_March = col1.button('March temp')
    res_April = col1.button('April temp')
    res_May = col2.button('May temp')
    res_June = col2.button('June temp')
    res_July = col2.button('July temp')
    res_August = col2.button('August temp')
    res_September = col3.button('September temp')
    res_October = col3.button('October temp')
    res_November = col3.button('November temp')
    res_December = col3.button('December temp')    

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    res_list = [res_January, res_February, res_March, res_April, res_May, res_June, res_July, res_August, res_September, res_October, res_November, res_December]
    res_list_str = ['res_January', 'res_February', 'res_March', 'res_April', 'res_May', 'res_June', 'res_July', 'res_August', 'res_September', 'res_October', 'res_November', 'res_December']

    

    for ind, val in enumerate(res_list):
        if val == True:
            button = (f'res_{month_list[ind]}')
            st.session_state.last_button = button
        elif 'last_button' not in st.session_state:
            st.session_state.last_button = None

    desired_start, desired_end = st.slider('Välj tisdsperiod (om du känner för det):', min_value=first_year, max_value=last_year, value=[first_year, last_year])
    desired_start = int(desired_start)
    desired_end = int(desired_end)
    
    st.session_state.desired_start = desired_start
    st.session_state.desired_end = desired_end

    button = st.session_state.last_button
    start = st.session_state.desired_start
    end = st.session_state.desired_end

    if st.session_state.last_button == None:
        pass
    else:
        df = df[(df['Year'] >= start) & (df['Year'] <= end)]
        for ind, val in enumerate(res_list_str):
            if val == button:
                month = ind

        df = df[df['Month'] == month+1]
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='Year', y='Snittemperatur')
        sns.regplot(x=df['Year'], y=df['Snittemperatur'], ci=False)
        # ax.scatter(x=df['Year'], y=df['Snittemperatur'])
        ax.set_title(f'Temperatures in {month_list[month]}')
        ax.set_xlabel('Year')
        ax.set_ylabel('Average daily temperature, Celcius')
        st.pyplot(fig)


if nav == 'Locations':
    st.title('Locations in Göteborg')
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

    st.title('Säve')
    st.write('Säve is located on Hisingen, about 10km from Göteborg. This station has not changed place.')
    save_long = '11.8824'
    save_lat = '57.7786'
    df_save = pd.DataFrame({'LON': [float(save_long)], 'LAT': [float(save_lat)]})
    st.map(df_save, latitude='LAT', longitude='LON', zoom=9, size=1000)

if nav == 'Nederbörd':
    st.write('Nä')

if nav == 'Vind':
     st.write('Nä')

if nav == 'Temperatur':
    temp_comp = ('temp_adjusted_comparison.png')
    st.image(temp_comp, width=1000)

if nav == 'Sommarens och vinterns ankomst':
    st.title('Sommarens och vinterns ankomst')
    st.write('"Den meteorologiska definitionen av sommar är att dygnsmedeltemperaturen varaktigt ska vara minst 10,0°C." /SMHI')
    st.write('"Meteorologer definierar vinter som den period då dygnets medeltemperatur varaktigt är 0,0 grader eller lägre." /SMHI')
    '\n'
    '\n'
    '\n'
    '\n'
    st.title('Sommarens anskomst')
    summer_arrival = ('summer_arrival_adjusted_comp.png')
    st.image(summer_arrival, width=1000)
