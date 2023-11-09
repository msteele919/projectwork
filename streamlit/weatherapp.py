import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

nav = st.sidebar.radio('Huvudmeny', ['Bakgrund', 'Frågeställning', 'Platsinformation', 'Vind', 'Snödjup', 'Nederbörd', 
                                     'Temperatur', 'Relationen mellan nederbörd & temperatur', 'Slutsatser'])

if nav == 'Bakgrund':

    st.text('''1. Kan man med hjälp av historisk väderdata se trender kring förändringar i vädret?
            
            \nHur har temperaturen ändrats sedan första datan?
            \nHar regn blivit mer intensivt under de senaste 50 åren? (Definiera intensivt)
	        \nFlera dagar med regn? Har totala nederbörden ökat/minskat mellan åren?
            \nHar åskoväder och stormar blivit mer intensiva under de senaste 50 åren? - sekundär
            \nHur har snödjupet ändrats över tid? 
            \nKan vi förutspå hur vädret ser ut i till exempel juli 2028?''')


# if nav == 'EDA':
    # st.session_state




if nav == 'Platsinformation':
    st.title('Stationernas platser Göteborg')
    st.write("Under åren har mätstationen i Göteborg stått på olika ställen. \nSedan 1998 är den belägen vid Gullbergsvass")

    st.write('Säve ligger på Hisingen, ungefär 10km fågelvägen från centrala Göteborg. Stationen har inte flyttats. Vinga ligger ute i skärgården.')
    current_station_gbg_lat_long = [57.7156, 11.9924]
    stations = pd.read_pickle('../Dataframes/station_info.pkl')
    green_hex = '#06a94d'
    red_hex = '#EE0000'
    # current = df['Tidsperiod (t.o.m)'].max()
    for ind, row in stations.iterrows():
        if row['LON'] == current_station_gbg_lat_long[1]:
            stations.at[ind, 'Colour'] = green_hex
        else:
            stations.at[ind, 'Colour'] = red_hex
    st.map(stations, latitude='LAT', longitude='LON', zoom=9.5, size=500, color='Colour')



if nav == 'Nederbörd':
    st.write('Nä')

if nav == 'Vind':
    #### Overview

    st.title('Överblick över vind-data')

    st.write('"Den vindhastighet som meteorologen anger i prognoser och flertalet av våra mätningar avser ett medelvärde under 10 minuter av vindhastigheten på 10 meters höjd ovan markytan." /SMHI')
    # st.write("""Som i de andra exempel har vi konkatenerat Säve och Göteborgs data för att kunna ha data från 1944 till 2023. Med knapparna nedan kan man skrolla igenom 
    #          """)
    st.write('Göteborg har luckor i sin data, så vi jämför bara Säve med Vinga. ')
    #### Below is the section for seeing the wind data decrease

    # knappar där man kan kolla på till exempel Säve data, Göteborgs data 
        # Meta knappar: välj mellan säve, Göteborg, Säve & Göteborg
    # vind_1 = "../plottar/mean_wind_daily_gbg.png"
    vind_2 = "../plottar/mean_wind_daily_sv.png"
    # vind_3 = "../plottar/mean_wind_daily_sv_gt.png"
    st.image(vind_2, caption='Vindarna blir svagare över tid')

    # compare_visuals = [ vind_1, vind_2, vind_3]

    # visual_names = ["GBG Snittvindhastighet p/dag", "Säve Snittvindhastighet p/dag", "GBG, Säve sammanlagt, Snittvindhastighet p/dag"]
    # # Display the current visual based on a user-selected name
    # current_index = st.selectbox("Select Visual", visual_names, index=0)
    # visual_index = visual_names.index(current_index)  # Get the index of the selected name
    # st.image(compare_visuals[visual_index], caption=current_index)

    ## Michael verison
    st.title('En läringsprocess: Finns det en trend i vind hastighet över tid och går det att jämföra Göteborg och Säve?')

    st.write("""När vi tittade på den sammanställda snittvindhästighets datamängden från Säve/Göteborg trodde vi först att det visades en negativ trend i Göteborg/Säves vindhastighet övertid.
            """)
    st.write("""Var detta en välgrundad slutsats? Följ med på vår journey och ta reda på det""")

    st.write("""När vi försökte ta reda på varför vindhastigheten hade minskat i Göteborg/Säve data mängden påstådde vi att byggnation i Göteborg över tid skulle kunna stå för den minskning. 
                """)

    ## Olof version
    st.write("""När vi tittar på vinddata över tid märker vi en minskning av den genomsnittliga vindhastigheten per dag.
                Låt oss börja med att undersöka hur vindhastigheten har förändrats beroende på vindriktningen.
             """)
    
    # wind direction Rose plots 
    vinddir_gbg_1 = "../plottar/windrose_all_winds_pre_1992_gbg.png"
    vinddir_gbg_2 = "../plottar/windrose_all_winds_post_1992_gbg.png"
    vinddir_sav_1 = "../plottar/windrose_all_winds_pre_1990_save.png"
    vinddir_sav_2 = "../plottar/windrose_all_winds_post_1990_save.png"
    vinddir_vinga_1 = "../plottar/windrose_all_winds_pre_1978_vinga.png"
    vinddir_vinga_2 = "../plottar/windrose_all_winds_post_1978_vinga.png"
    '\n'
    '\n'



    #### Look at reliability
    '\n'

    

    
    #### Change of directions, all winds
    # st.write('Den enda riktningen där andelen vinddagar minskar är från 0 grader till 90 grader')
    # winds_from_NE_save = ('../Olof_viz/change_of_wind_0_90_save.png')
    # winds_from_NE_vinga = ('../Olof_viz/change_of_wind_0_90_vinga.png')
    # other_winds_save = '../plottar/wind_direction_changes_save_increases_collection.png'
    # st.image(winds_from_NE_save, caption='Andelen dagar med uppmätta vindar från 0-90, Säve')
    # st.image(other_winds_save, caption='Andra vindrisktningar ökar under perioden.')
    # st.write('Detta gäller dock inte Vinga')
    # st.image(winds_from_NE_vinga, caption='Andelen dagar med uppmätta vindar från 0-90, Vinga')



    #### Correlation with buildings

    st.header('Är vind minskning i Säve relaterad med byggnation i Göteborg?')
    
    st.write("""Efter att vi hade kollat på vinddata i Göteborg och Säve märktes det att vindblås har sjunkit i sin krafighet över tiden. Vi har funderat på olika möjliga källor till denna försjunkning, som till exempel, klimatförändring. 
               En annan hypotes som uppstod under vår analysprocess var att vindhastighetsminskningen kan bero på ökad byggnation i Göteborg. För att undersöka detta jämförde vi vinddata från Säve med SCBs "Färdigställda lägenheter och rumsenheter i nybyggda hus i Göteborg från 1975-2022" """)
    
    st.header("""Bygnationsdata
        """)
    st.write("""Med byggnationsdata beräknade vi den kummulativa nybyggdlägenhetsmängd i Göteborg från 1975 - 2006, när Säve datamängden slutades.  
        """)
    st.image('../plottar/kumulativ_lägenheter_gbg.png', width=700)
    st.write("""När kumulativt antal lägenheter plottas mot årlig vindhastighet i Säve verkar det som det finns en moderat till svag negativ relation.  
        """)

    st.write("""För att undersöka relationen använde vi en lineär OLS regression ekvation användes:""")
    st.write("""y = a * X + c """)
    
    st.image('../plottar/reg_results_sav_bygg_linear.png', width = 700)

    st.write("""Resultatet visar att en lineärregression model är signifikant (p = 0,0248) med en R-squared värde av 16,7%. Kumulativt antal lägenheter koefficienten var signifikant (p = 0,025) och är relaterad till en 0,00000377 °C årlig minskning i snitttemperatur i genomsnitt. 
             Det verkar som relationen är dock heteroskedastic. Detta står i konflikt med OLS-antagandet om homoskedasticitet. 
    """)
    st.write("""Det kan emellertid finnas utrymme för tolkning som skulle förklara detta heteroskedastiska beteende. Eftersom en lägre mängd bostäder skulle påverka vinden mindre, kan variationsnivån därför variera kraftigt. 
             Verkligen kan vinden vissa år vara lägre eller högre baserat på många andra faktorer. Dock, när byggnadsnivåerna ökar, ökar även mängden vindhinder, vilket gör att högre vindhastigheter är mindre troliga att registreras, vilket förklarar det tydligare sambandet mellan byggnadsnivåer och vindhastigheter när byggnadsnivåerna ökar.
    """)
    

    st.image('../plottar/bygg_wind_sav_linear.png', width = 700)


    
    selected_location = st.selectbox("Select Location", ["Säve", "Vinga"]) # Removed GBG

        # Use if-else conditions to display the appropriate visuals
    # if selected_location == "GBG":
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.image(vinddir_gbg_1, caption="GBG Snittvindhastighet p/dag")
    #     with col2:
    #         st.image(vinddir_gbg_2, caption="GBG Snittvindhastighet p/dag")
    if selected_location == "Säve":
        col1, col2 = st.columns(2)
        with col1:
            st.image(vinddir_sav_1, caption="Säve Snittvindhastighet p/dag")
        with col2:
            st.image(vinddir_sav_2, caption="Säve Snittvindhastighet p/dag")
    elif selected_location == "Vinga":
        col1, col2 = st.columns(2)
        with col1:
            st.image(vinddir_vinga_1, caption="Vinga Snittvindhastighet p/dag")
        with col2:
            st.image(vinddir_vinga_2, caption="Vinga Snittvindhastighet p/dag")

    st.write('Förklaring av vindrosor:  \n0 grader: Norr  \n90 grader: Öst  \n180 grader: Syd  \n270 grader: Väst')
    # st.write('- Varje arm täcker 22.5 grader. Så armern rakt norrut täcker vindar från 348.75 grader till 11.25 grader')
    st.write('- Cirklarna visar andelen av observationerna i procent.')
    st.write('- Färgerna visar vindhastigheten')
    st.write('- Automatiska proportioner')
    #### Harder winds
    st.title('Hårdare vindar')
    hard_winds_over_time = ('../Olof_viz/hard_winds_over_time_comparison.png')
    st.image(hard_winds_over_time)



    hard_winds_over_time_save = "../plottar/hard_winds_save_barplot.png"
    hard_winds_over_time_vinga = "../plottar/hard_winds_vinga_barplot.png"
    st.image(hard_winds_over_time_save)
    st.image(hard_winds_over_time_vinga)
    st.write('Har de kraftigare vindarna ändrat riktning?')
    hard_winds_save_pre_1978 = ('../plottar/windrose_hard_winds_pre_1990_save.png')
    hard_winds_save_post_1978 = ('../plottar/windrose_hard_winds_post_1990_save.png')
    col1, col2, = st.columns(2)
    with col1: 
        st.image(hard_winds_save_pre_1978)
    with col2:
        st.image(hard_winds_save_post_1978)
    st.write('Slutsats: Större andel kraftiga vindar från söder, men överlag lägre hastigheter.')
    st.write('Ingen större skilnad i vindar från Göteborgs-hållet.')

if nav == 'Temperatur':
    total_temps_plus_adjusted = ('../Olof_viz/medeltemperaturer.png')
    temp_diff = ('../Olof_viz/temp_diff_gbg_save.png')
    medeltemp = ('../plottar/medeltemp_sammanslaget.png')
    both_datasets_compared = ('../plottar/temp_skilnad_snitt_gbg_save_resp_dataset.png')
    st.title('Temperaturdata')
    st.text('Data för Säve: 1944-2006 \nData för Göteborg: 1961 ->')
    st.write('Sätter vi samman dataseten får vi mycket längre spann att titta på.')
    temps_meassures_gbg = ('../plottar/temp_meassurements_gbg.png')
    temps_meassures_save = ('../plottar/temp_meassurements_save.png')

    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.image(temps_meassures_gbg)
    with col2:
        st.write('Saknas det dagar?')
        '\n'
        st.write('GÖTEBORG')
        df_gbg = pd.read_pickle('../Dataframes/df_daily_temp_gbg.pkl')
        def get_no_meassures_per_year_temp_gbg(year):
            if (len(df_gbg[df_gbg['Year'] == year]) < 365) and (len(df_gbg[df_gbg['Year'] == year]) > 0):
                days = len(df_gbg[df_gbg['Year'] == year])
                return f'{year} mättes {days} dagar'
            else:
                pass
        for i in range(1961, 2023):
            ret = get_no_meassures_per_year_temp_gbg(i)
            if ret == None:
                pass
            else:
                st.write(ret)


    '\n'
    with col1:
        st.image(temps_meassures_save)
    with col2:
        '\n'
        '\n'
        st.write('SÄVE')
        df_save = pd.read_pickle('../Dataframes/df_daily_temp_save.pkl')
        def get_no_meassures_per_year_temp_save(year):
            if len(df_save[df_save['Year'] == year]) < 365 and len(df_save[df_save['Year'] == year]) > 0:
                days = len(df_save[df_save['Year'] == year])
                return f'{year} mättes {days} dagar'
            else:
                pass
        for i in range(1961, 2007):
            ret = get_no_meassures_per_year_temp_save(i)
            if ret == None:
                pass
            else:
                st.write(ret)
    st.write('Med tanke på luckorna i datasetet för Göteborg bestämde vi oss för att lägga på Göteborgsdatan där Säve-mätningarna tog slut, 2006.')
    
    st.write('''Det är i snitt lite varmare i städer ([SMHI](https://www.smhi.se/forskning/forskningsenheter/meteorologi/varme-och-luftmiljo-i-stader/hogre-temperaturer-i-staden-1.160049)). 
             Om vi vill komplettera Säve-datan med data från Göteborg borde vi därför justera något av dataseten så att det blir lite mer
             rättvisande. Annars kan snittemperaturen stiga drastisk när vi tar data från Göteborg, 
             utan att det nödvändigtvis var varmare.''')
    st.image(both_datasets_compared, caption='Snabb jämförelse mellan snittemperaturer för båda dataseten')
    '\n'
    '\n'
    '\n'
    st.image(temp_diff, caption='''Skillnader i månadstemperatur mellan Görborg och Säve under den överlappande perioden 1961 till 2006. 
             Visar temperatur i Göteborg minus temperatur i Säve''')
    st.subheader('Temperaturer justerat efter månadssnitten ovan.')
    st.image(medeltemp)
    '\n'
    '\n'
    '\n'
    st.subheader('Det blir varmare på vintern')
    avg_temp_increase = ('../plottar/avg_temp_change_per_month.png')
    st.image(avg_temp_increase)
    '\n'
    '\n'
    '\n'
    st.write('"Den meteorologiska definitionen av sommar är att dygnsmedeltemperaturen varaktigt ska vara minst 10,0°C." /SMHI')
    st.write('"Meteorologer definierar vinter som den period då dygnets medeltemperatur varaktigt är 0,0 grader eller lägre." /SMHI')
    summer_arrival_trendline = ('../plottar/summer_arrivals_trendline.png')
    st.image(summer_arrival_trendline, caption='I snitt ankommer sommaren 5e Maj')
    '\n'
    '\n'
    '\n'
    #### Just for fun, see temps

    st.subheader('Se temperaturer för månad och tidspann.')
    '\n'
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
        sns.scatterplot(data=df, x='Year', y='Snittemperatur', c='b')
        sns.regplot(x=df['Year'], y=df['Snittemperatur'], ci=False, color='g', line_kws={'linestyle': '--'})
        ax.scatter(x=df['Year'], y=df['Snittemperatur'])
        ax.set_title(f'Temperaturer i {month_list[month]}')
        ax.set_xlabel('År')
        ax.set_ylabel('Snittemperatur per dag, Celcius')
        st.pyplot(fig)

# if nav == 'Sommarens och vinterns ankomst':
#     st.title('Sommarens och vinterns ankomst')
#     st.write('"Den meteorologiska definitionen av sommar är att dygnsmedeltemperaturen varaktigt ska vara minst 10,0°C." /SMHI')
#     st.write('"Meteorologer definierar vinter som den period då dygnets medeltemperatur varaktigt är 0,0 grader eller lägre." /SMHI')
#     '\n'
#     '\n'
#     '\n'
#     '\n'
#     st.title('Sommarens ankomst')
#     summer_arrival = ('../plottar/summer_arrivals.png')
#     st.image(summer_arrival)
#     df = pd.read_pickle('../Dataframes/summer_days_diff.pkl')
#     st.table(df)
#     st.write('I snitt skiljer det 4.8 dagar mellan justerad och ojusterad temperatur.')
#     summer_arrival_trendline = ('../plottar/summer_arrivals_trendline.png')
#     st.image(summer_arrival_trendline, caption='I snitt ankommer sommaren 5e Maj')