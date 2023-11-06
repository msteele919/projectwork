import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

monthly = pd.read_pickle("/Users/mstee/Documents/School/projectwork/Dataframes/df_monthly_temp.pkl")

# sns.scatterplot(x=monthly['Month'], y=monthly['Monthly avg'], data=monthly)
# sns.lineplot(x='Month', y= 'Monthly avg', data=monthly, errorbar=('ci', 0))
# plt.xlabel('Månad')
# plt.ylabel('Temperatur i °C')
# plt.xticks(ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
#            labels=['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']

manadtempovertid = ('../plottar/manadtempovertid.png')
julitempovertid = ('../plottar/julitempovertid.png')
decembertempovertid = ('../plottar/decembertempovertid.png')
regnpermanad = ('../plottar/regnpermanad.png')
oktoberregn = ('../plottar/oktoberregn.png')
aprilregn = ('../plottar/aprilregn.png')
regnperar = ('../plottar/regnperår.png')

## Förutsägelser om framtiden slides plottar 

# train_test split 
train_test_path = os.path.join("../plottar/train_test.png")
image = plt.imread(train_test_path)
# prediktion bad 
prediktion = os.path.join("../plottar/prediktion_bad.png")
pred_bad = plt.imread(prediktion)
#grid_search
grid = os.path.join("../plottar/grid_search.png")
grid_s = plt.imread(grid)

juli = monthly.query("Month == 7")
december = monthly.query("Month == 12")




# Creating the menu
nav = st.sidebar.radio('Meny',['Bakgrund', 'Data','Data & Modellering', 'EDA', 'Platser', 'Nederbörd', 'Vind', 'Temperatur', 'Sommarens och vinterns ankomst'])
if nav == 'Bakgrund':
    st.title('Undersökning av väderdata kring Göteborgsområdet från 1944 till 2023')
    st.header('Syftet med valt projekt:')
    st.write("""1. Kan man med hjälp av historisk väderdata se trender kring förändringar i vädret?
             \n2. Har regn blivit mer intensivt under de senaste 50 åren?
             \n3. Har åskoväder och stormar blivit mer intensiva under de senaste 50 åren?
             \n4. Har snödjupet ändrats? 
             \n5. Kan vi förutspå hur vädret ser ut i till exempel Juli 2028? 
             """)
    
if nav == 'Data':

    st.title('Behind the different data')
    st.header('Which data sets ')
    st.write("""We have used data from a few different stations locations....
             """)
    
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
    
    st.title('Vinga')
    st.write("""At some points in our analysis data was taken from Vinga's weather station. This data was used often as a control dataset. To see how different weather patterns 
             acted in a place close to Gothenburg and Säve, but without any building development .""")
    save_long = '11.6048'
    save_lat = '57.6322'
    df_save = pd.DataFrame({'LON': [float(save_long)], 'LAT': [float(save_lat)]})
    st.map(df_save, latitude='LAT', longitude='LON', zoom=9, size=1000)
    

if nav == 'Data & Modellering':
    
    st.title('Data & Modellering')
    st.write('I denna sektionen kommer vi att presentera data tillsammans med våra slutsatser och observationer.')

    st.header('Grafisk presentation av insamlad data')
    st.subheader('Månatlig snittemperatur mellan perioden Januari 1944 till Oktober 2023.')
    st.set_option('deprecation.showPyplotGlobalUse', False) # Döljer felmeddelandet från st.pyplot
    st.image(manadtempovertid)
    st.write("""Vi ser här medelvärdet av temperaturen per månad. Hur ser exempelvis Juli ut? """)
    st.write(f"Minsta uppmätta värde: {juli['Monthly avg'].min()} °C")
    st.write(f"Högsta uppmätta värde: {juli['Monthly avg'].max()} °C")
    st.write(f"Snittemperatur för juli sedan 1944: {round(juli['Monthly avg'].mean(),2)} °C")
    st.image(julitempovertid)
    st.write('Vi kan se på trendlinjen här att medeltemperaturen för Juli månad blir varmare med tiden. Är det detsamma för exempelvis December?')
    st.image(decembertempovertid)
    st.write(f"Minsta uppmätta värde: {december['Monthly avg'].min()} °C")
    st.write(f"Högsta uppmätta värde: {december['Monthly avg'].max()} °C")
    st.write(f"Snittemperatur för juli sedan 1944: {round(december['Monthly avg'].mean(),2)} °C")
    st.subheader('Hur ser det ut med nederbörd?')
    st.write('Så här ser fördelningen av nederbörd ut per år')
    st.image(regnpermanad)
    st.write('Vi ser här att den regnigaste perioden är Oktober månad och den minst regniga perioden är April')
    st.write('Har oktober månad blivit blötare över tid?')
    st.image(oktoberregn)
    st.write('Det ser ut som att den blöta perioden Oktober blir blötare med tiden. Är det likadant med den minst regniga månaden?')
    st.image(aprilregn)
    st.write('Ja, det ser onekligen ut så baserat på denna datan med. Inte i samma takt men ändå blötare med tiden.')
    st.write('Om vi ställer hela året över tid, hur ser det ut då?')
    st.image(regnperar)
    st.write('')

    st.write(' ')

    st.subheader('Rådata')
    st.write('För att ta del av rådatan till snittemperaturen per månad klicka i boxen')
    if st.checkbox('Visa rådata'):
        st.write(monthly)

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



if nav == 'Vind':
    st.title('Överblick över wind data ')
    st.write("""Som i de andra exempel har vi konkatenerat Säve och Göteborgs data för att kunna ha data från 1944 till 2023. Med knapparna nedan kan man skrolla igenom 
             """)
    # knappar där man kan kolla på till exempel Säve data, Göteborgs data 
        # Meta knappar: välj mellan säve, Göteborg, Säve & Göteborg
    vind_1 = "../plottar/mean_wind_daily_gbg.png"
    vind_2 = "../plottar/mean_wind_daily_sv.png"
    vind_3 = "../plottar/mean_wind_daily_sv_gt.png"
    compare_visuals = [ vind_1, vind_2, vind_3]

    visual_names = ["GBG Snittvindhastighet p/dag", "Säve Snittvindhastighet p/dag", "GBG, Säve sammanlagt, Snittvindhastighet p/dag"]
    # Display the current visual based on a user-selected name
    current_index = st.selectbox("Select Visual", visual_names, index=0)
    visual_index = visual_names.index(current_index)  # Get the index of the selected name
    st.image(compare_visuals[visual_index], caption=current_index)
    
    st.write("""När vi tittar på vinddata över tid märker vi en minskning av den högsta vindhastigheten per dag.
                Låt oss börja med att undersöka hur vindhastigheten har förändrats beroende på vindriktningen.
             """)
    # wind direction Rose plots 
    vinddir_gbg_1 = "../plottar/wind_dir_gbg_pre1980.png"
    vinddir_gbg_2 = "../plottar/wind_dir_gbg_post1980.png"
    vinddir_sav_1 = "../plottar/wind_dir_sav_pre1980.png"
    vinddir_sav_2 = "../plottar/wind_dir_sav_post1980.png"
    
    selected_location = st.selectbox("Select Location", ["GBG", "Säve"])

        # Use if-else conditions to display the appropriate visuals
    if selected_location == "GBG":
        col1, col2 = st.columns(2)
        with col1:
            st.image(vinddir_gbg_1, caption="GBG Snittvindhastighet p/dag")
        with col2:
            st.image(vinddir_gbg_2, caption="Säve Snittvindhastighet p/dag")
    elif selected_location == "Säve":
        col1, col2 = st.columns(2)
        with col1:
            st.image(vinddir_sav_1, caption="GBG Snittvindhastighet p/dag")
        with col2:
            st.image(vinddir_sav_2, caption="Säve Snittvindhastighet p/dag")
    
    # compare_dir = [ vinddir_gbg_1, vinddir_gbg_2]
    # visual_names_dir = ["GBG Snittvindhastighet p/dag", "Säve Snittvindhastighet p/dag", "GBG, Säve sammanlagt, Snittvindhastighet p/dag"]
    # # Display the current visual based on a user-selected name
    # current_index_dir = st.selectbox("Select Visual", visual_names_dir, index=0)
    # visual_index_dir = visual_names_dir.index(current_index_dir)  # Get the index of the selected name
    # st.image(compare_dir[visual_index_dir], caption=current_index_dir)
    


   
    

    # Display the visuals
    # st.image(vind_1, caption='Visual 1')
    # st.image(vind_2, caption='Visual 2')
    # st.image(vind_3, caption='Visual 3')

   
        # snitt vindblås per dag, max vindblås per dag, snitt vindblås per månad
    st.header('Har vinden minskat i Göteborg?')
    
    st.write("""Efter vi hade kollat på vinddata i Göteborg och Säve märkets det att Vindblås har sjunkit i sin krafighet över tiden. Vi har funderat på olika möjliga källor till denna försjunkning, som klimatförändring,
               men har en hypotes att det kan bero på ökad byggnation i Göteborg och Säve under det
            n senaste århundraden.""")
    
    
if nav == 'Temperatur':
    temp_comp = ('temp_adjusted_comparison.png')
    st.image(temp_comp, width=1000)

    st.title('Förutsägelser om framtids snitt temperatur')
    st.write('Med temperaturdata från Save väder station har en recursive multisteg autoregressiv modell använts inom sciket learn.')
    st.header('Metodik:')
    st.write('En recursive multi-step autoregressiv modell är ett sätt att kunna använda time series data och förutsäga framtida värde. I en recursiv autoregression modell så används ett antal steg som kallas lags som modellen skall basera sina prediktioner på. Denna siffra bestämdes efter en grid search. Lag som fick lägst root mean square error var 30 dagar. Detta skulle då representera månadsvis trender. ')
    st.header('Placeholder för algoritmen. Nedan visas grafer:')
    st.subheader('Data Split med Säve data. Training data innan 2010-01-01')
    st.image(image)
    st.subheader('Resultat från gridsearch.')
    st.write('Lag med 30 dagar visade sig ha bäst root mean square error')
    st.image(grid_s)
    st.subheader('Resultat från prediktion')
    st.image(pred_bad)
    st.write('Root Mean square error var faktiskt hög för denna modell. 13,59°C root mean square visar att modellen ännu inte har en bra prediktionsförmåga. Nästa steg skulle vara att använd en seasonal ARIMA modell. Då denna modell tog hansyn till månadsvis skillnader säsong förändringar måste tänkas över.')

if nav == 'Slutsats och reflektioner':
    st.title('Slutsats')
    st.write("""Här är en placeholder för vår slutsats.\n""")
    st.subheader('Reflektioner')
    st.write("""Här är en placeholder för våra reflektioner som vi skall skriva. Kommer vi att vilja ha 3st subheaders för oss var?""")