import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

nav = st.sidebar.radio('Huvudmeny', ['Bakgrund', 'Frågeställning', 'EDA', 'Platsinformation', 'Nederbörd', 'Vind', 'Temperatur', 'Sommarens och vinterns ankomst'])

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
    df = pd.read_pickle('../dataframes/df_compiled_adjusted_monthly_temp_gbg_save.pkl')
    first_year = df['Year'].min()
    last_year = df['Year'].max()
    
    col1, col2, col3 = st.columns(3)

    res_January = col1.button('Januari')
    res_February = col1.button('Febuari')
    res_March = col1.button('Mars')
    res_April = col1.button('April')
    res_May = col2.button('Maj')
    res_June = col2.button('Juni')
    res_July = col2.button('Juli')
    res_August = col2.button('Augusti')
    res_September = col3.button('September')
    res_October = col3.button('Oktober')
    res_November = col3.button('November')
    res_December = col3.button('December')    

    month_list = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']
    res_list = [res_January, res_February, res_March, res_April, res_May, res_June, res_July, res_August, res_September, res_October, res_November, res_December]
    res_list_str = ['res_Januari', 'res_Februari', 'res_Mars', 'res_April', 'res_Maj', 'res_Juni', 'res_Juli', 'res_Augusti', 'res_September', 'res_Oktober', 'res_November', 'res_December']

    

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
        ax.set_title(f'Temperaturer i {month_list[month]}')
        ax.set_xlabel('År')
        ax.set_ylabel('Snittemperatur per dag, Celcius')
        st.pyplot(fig)


if nav == 'Platsinformation':
    st.title('Stationernas platser Göteborg')
    st.text("Under åren har mätstationen i Göteborg stått på olika ställen. \nSedan 1998 är den belägen vid Gullbergsvass")
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

    st.title('Säve och Vinga')
    st.write('Säve ligger på Hisingen, ungefär 10km fågelvägen från centrala Göteborg. Stationen har inte flyttats. Vinga ligger ute i skärgården.')
    save_long = '11.8824'
    save_lat = '57.7786'
    vinga_long = '11.6061'
    vinga_lat = '57.6322'
    df_save = pd.DataFrame({'LON': [float(save_long), float(vinga_long)], 'LAT': [float(save_lat), float(vinga_lat)]})
    st.map(df_save, latitude='LAT', longitude='LON', zoom=9, size=1000)


if nav == 'Nederbörd':
    st.write('Nä')

if nav == 'Vind':
    st.title('Överblick över wind data ')

    st.write('"Den vindhastighet som meteorologen anger i prognoser och flertalet av våra mätningar avser ett medelvärde under 10 minuter av vindhastigheten på 10 meters höjd ovan markytan." /SMHI')
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
    
    st.write("""När vi tittar på vinddata över tid märker vi en minskning av den genomsnittliga vindhastigheten per dag.
                Låt oss börja med att undersöka hur vindhastigheten har förändrats beroende på vindriktningen.
             """)
    # wind direction Rose plots 
    vinddir_gbg_1 = "../plottar/wind_dir_gbg_pre1980.png"
    vinddir_gbg_2 = "../plottar/wind_dir_gbg_post1980.png"
    vinddir_sav_1 = "../plottar/wind_dir_sav_pre1980.png"
    vinddir_sav_2 = "../plottar/wind_dir_sav_post1980.png"
    '\n'
    '\n'
    st.write('Lägg till för Vinga, se till att plottarna visar rätt saker')
    st.write('Förklaring av vindrosor:  \n0 grader: Norr  \n90 grader: Öst  \n180 grader: Syd  \n270 grader: Väst')
    st.write('Cirklarna visar andelen av observationerna i procent.')
    st.write('Färgerna visar vindhastigheten')
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
    hard_winds_over_time = ('../Olof_viz/hard_winds_over_time_comparison.png')
    st.image(hard_winds_over_time)

    st.write('Trots att antalet mätningar per år ökat rejält på 2000-talet, så har andelen dagar med vindar från riktningarna 0-90 grader (Norr till Öster) minskat i Säve.')
    winds_from_NE_save = ('../Olof_viz/change_of_wind_0_90_save.png')
    winds_from_NE_vinga = ('../Olof_viz/change_of_wind_0_90_vinga.png')
    st.image(winds_from_NE_save, caption='Andelen dagar med uppmätta vindar från 0-90, Säve')
    st.image(winds_from_NE_vinga, caption='Andelen dagar med uppmätta vindar från 0-90, Vinga')

    st.write('Hur pålitlig är då denna nedgång i vindar från 0-90?')
    no_meassurements_save = ('../Olof_viz/wind_meassurements_per_year_save.png')
    st.image(no_meassurements_save, caption='Antalet mätningar per år är ungefär samma sedan 1960')


if nav == 'Temperatur':
    total_temps_plus_adjusted = ('../Olof_viz/medeltemperaturer.png')
    temp_diff = ('../Olof_viz/temp_diff_gbg_save.png')
    unadjusted = ('../Olof_viz/medeltemp_ojusterad.png')
    adjusted = ('../Olof_viz/medeltemp_justerad.png')
    both_datasets_compared = ('../Olof_viz/temp_skilnad_snitt_gbg_save_resp_dataset.png')
    st.title('EDA')
    st.text('Data för Säve: 1944-2006 \nData för Göteborg: 1961 ->')
    st.image(both_datasets_compared, caption='Snabb jämförelse mellan snittemperaturer för båda dataseten')
    st.write('''Det är i snitt lite varmare i städer. Om vi vill komplettera Säve-datan med data från Göteborg borde vi därför justera något av dataseten så att det blir lite mer
             rättvisande. Annars kan snittemperaturen stiga drastisk när vi tar data från Göteborg, 
             utan att det nödvändigtvis var varmare.''')
    
    st.image(temp_diff, caption='''Skillnader i månadstemperatur mellan Görborg och Säve under den överlappande perioden 1961 till 2006. 
             Visar hur mycket varmare/kallare Göteborg var än Säve. Vid positivt tal var Göteborg varmare''')
    

    col1, col2 = st.columns(2)
    with col1:
        st.image(unadjusted, caption='Sammansatt dataset av data från Säve fram till 2006.')
    with col2:
        st.image(adjusted, caption='Justerat dataset, där temperaturerna från 2006 och framåt justerats enlit resultaten ovan')


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
