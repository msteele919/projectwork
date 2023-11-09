import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

precip = pd.read_pickle("../Dataframes/df_compiled_daily_precipitation_gbg_save.pkl")
snodjup = pd.read_pickle("../Dataframes/df_snow_save.pkl")
aprilregn = ("../plottar/aprilregn.png")
oktoberregn = ("../plottar/oktoberregn.png")
sno10 = snodjup.query("Snödjup >= .1")
sno20 = snodjup.query("Snödjup >= .2")
sno30 = snodjup.query("Snödjup >= .3")
sno40 = snodjup.query("Snödjup >= .4")
sno50 = snodjup.query("Snödjup >= .5")

intervaller = { '10 cm' : sno10, '20 cm' : sno20, '30 cm' : sno30, '40 cm' : sno40, '50 cm' : sno50} 
snointervaller = [sno10, sno20, sno30, sno40, sno50]

# def snodjupfunk(djup):
#     sns.scatterplot(data=djup, x='Datum', y='Snödjup')
#     plt.title(f'Antal observerade dagar per år med mer än {djup}cm snö.')
#     plt.xlabel('År')
#     plt.ylabel('Snödjup i meter')
#     plt.show()

def count_10_year_intervals(data):
    data = data.drop_duplicates(subset='Datum')
    bins = list(range(1944, 2005, 10))
    interval_counts = data.groupby(pd.cut(data['Year'], bins=bins), observed=True).size()
    return interval_counts

nav = st.sidebar.radio('Huvudmeny', ['Bakgrund', 'Frågeställning', 'EDA', 'Platsinformation',  'Vind', 'Snödjup', 'Nederbörd', 'Temperatur', 'Relationen mellan nederbörd & temperatur','Sommarens och vinterns ankomst' ])

if nav == 'Bakgrund':

    st.text('''1. Kan man med hjälp av historisk väderdata se trender kring förändringar i vädret?
            
            \nHur har temperaturen ändrats sedan första datan?
            \nRegnar det mer eller mindre nu än förr?
            \nHar det blivit någon förändring med snödjup?
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

if nav == 'Snödjup':
    st.title('Snödjup')
    st.subheader('Information om datan')
    st.write(f"""Snödjupet är mätt på Säve mätstation som ligger vid Säve flygplats. Datan är insamlad mellan januari 1944 och december 2003 och mäts i meter.
             \nDet är lite glapp i informationen.""")
    if st.checkbox('Visa antal mätningar per år.'):
        st.write(snodjup.Year.value_counts())
    st.subheader("""Hur ser det ut egentligen med snö över tid?""")
    # st.write(f"Minsta snödjup: {snodjup['Snödjup'].min()}m")
    # st.write(f"Medelsnödjup över alla år: {round(snodjup['Snödjup'].mean(),3)}m")
    # st.write(f"Max uppmätta snödjupet: {snodjup['Snödjup'].max()}m")
    # st.subheader('Vi tittar på perioden då det snöar.')
    # st.image("../plottar/snodjuppermånad.png")
    # st.write("""Det är ju rimligt att snö-observationerna är mellan januari och maj och oktober och december då det inte snöar under sommaren.""")
    # st.write("Hur ligger det då till med snödjupet när det väl snöar en period?")
    # st.image("../plottar/snöperperiod.png")
    # st.write('Som vi ser här är det inte så konstigt att det ligger mer snö på marken i slutet av perioden egentligen.')
    # st.write("Hur har det sett ut genom åren?")
    st.image("../plottar/totalsnödjup.png")
    st.write("Det verkar ju onekligen som att det är mindre snö på marken efter 90-talet jämfört med exempelvis 80-talet.")

    # selected_dataframe = st.selectbox("Visa antal dagar med snödjup över: ", list(intervaller.keys()))
    # if selected_dataframe in intervaller:
    #     selected_label = intervaller[selected_dataframe]
    #     interval_counts = count_10_year_intervals(selected_label)
    #     st.write("Antal dagar per årtionde:")
    #     st.write(interval_counts)
    # else:
    #     st.write("Ogiltigt val")


if nav == 'Nederbörd':
    st.title('Nederbörd')
    st.subheader('Beskrivning av dataset')
    st.write("""Regndatan är insamlad från mätstationerna i Säve och i Göteborg. Datan från Säve är insamlad från första januari 1944 och sträcker sig till 30e november 2002.
             Göteborgsdatan var inkomplett, så vi har valt att ta vid Göteborgsdatan där Sävedatan slutar, så hela datasettet sträcker sig till sista juni i år.
             \nMängden nederbörd mäts i millimeter, vilket är ett mått på hur högt vattnet skulle nå ovan marken om det inte sjönk undan.""")
    st.subheader('Hur ser det ut med nederbörden?')
    st.image("../plottar/snittnederbördövertid.png")
    st.write("""Enligt grafen så verkar det pendla en del mellan åren, men det verkar ju som att det snittnederbörden ökar över tid.
             Vi kan dubbelkolla detta genom att göra en plot med en trendlinje som med enkel linjär regression räknar ut ett samband mellan genomsnitssregnfall och datum.""")
    # st.image("../plottar/regn200808.png")
    # st.write('Där ser vi att det regnade som fasen den 27e augusti.')
    st.image("../plottar/regnperår.png")
    st.write("""Vi ser ju klart och tydligt att det trendar till att det regnar mer i dagsläget än på 50-talet. 
             Visserligen är det inte mycket, men tillräckligt mycket för att visas på en graf.
             Är det någon skillnad mellan nederbörd och månader?
             \nNär regnar det mest respektive minst, i snitt?""")
    st.image("../plottar/regnpermanad.png")
    st.write("""Denna grafen bekräftar att våren i snitt är en torrare period än hösten.
             \nÄr det så att dessa perioder blir blötare över tid med, som den tidigare trenden visar?""")
    st.image("../plottar/oktoberregn.png")
    st.write("""Som vi ser så regnar det i snitt 1mm mer i oktober på senare år än i början av mätningen.
             \nHur ser det ut för april månad?""")
    st.image("../plottar/aprilregn.png")
    st.write("""Även april visar en ökning av snittnederbörd över tid.
             \nHur är det med övriga månader? Hur har regnet förändrats?""")
    st.image("../plottar/genomsnittsändringregn.png", caption='Genomsnittsförändring per månad av regnfall i mm över hela perioden')
    st.write("""Intressant nog så är september minst påverkad av alla månader, 
             trots att det är i regel en väldigt regning månad medan oktober månad visar störst genomsnitssförändring, trots att det också i regel är en väldigt regnig månad.
              """)

if nav == 'Vind':
    #### Overview

    st.title('Överblick över vind-data ')

    st.write('"Den vindhastighet som meteorologen anger i prognoser och flertalet av våra mätningar avser ett medelvärde under 10 minuter av vindhastigheten på 10 meters höjd ovan markytan." /SMHI')
    st.write("""Som i de andra exempel har vi konkatenerat Säve och Göteborgs data för att kunna ha data från 1944 till 2023. Med knapparna nedan kan man skrolla igenom 
             """)
    # knappar där man kan kolla på till exempel Säve data, Göteborgs data 
        # Meta knappar: välj mellan säve, Göteborg, Säve & Göteborg
    vind_1 = "../plottar/mean_wind_daily_gbg.png"
    vind_2 = "../plottar/mean_wind_daily_sv.png"
    vind_3 = "../plottar/mean_wind_daily_vinga.png"
    
    compare_visuals = [ vind_1, vind_2, vind_3]

    visual_names = ["GBG Snittvindhastighet p/dag", "Säve Snittvindhastighet p/dag", "Vinga Snittvindhastighet p/dag"]
    # Display the current visual based on a user-selected name
    current_index = st.selectbox("Select Visual", visual_names, index=0)
    visual_index = visual_names.index(current_index)  # Get the index of the selected name
    st.image(compare_visuals[visual_index], caption=current_index)

    ## Olof version
    # st.write("""När vi tittar på vinddata över tid märker vi en minskning av den genomsnittliga vindhastigheten per dag.
    #             Låt oss börja med att undersöka hur vindhastigheten har förändrats beroende på vindriktningen.
            #  """)
    st.write("""När vi tittar på vinddata över tid märker vi en minskning av den genomsnittliga vindhastigheten per dag.
                Skulle vindminskningen i Säve vara en effekt av ökad byggnation i Göteborg? 
             """)
       #### Correlation with buildings

    st.header('Är vind minskning i Säve relaterad med byggnation i Göteborg?')
    
    # st.write("""Efter att vi hade kollat på vinddata i Göteborg och Säve märktes det att vindblås har sjunkit i sin krafighet över tiden. Vi har funderat på olika möjliga källor till denna försjunkning, som till exempel, klimatförändring. 
    #            En annan hypotes som uppstod under vår analysprocess var att vindhastighetsminskningen kan bero på ökad byggnation i Göteborg. För att undersöka detta jämförde vi vinddata från Säve med SCBs "Färdigställda lägenheter och rumsenheter i nybyggda hus i Göteborg från 1975-2022" """)
    
    st.write("""Bygnationsdata
        """)
    st.write(""" 
    Vi beräknade den kummulativa nybyggdlägenhetsmängd i Göteborg från 1975 - 2006, när Säve datamängden slutades.  """)
    st.write("""Källa: SCBs datamängden:  "Färdigställda lägenheter och rumsenheter i nybyggda hus i Göteborg från 1975-2022""")
    st.image('../plottar/kumulativ_lägenheter_gbg.png', width=700)
    st.write("""När kumulativt antal lägenheter plottas mot årlig vindhastighet i Säve verkar det som det finns en moderat till svag negativ relation.  
        """)

    st.write("""För att undersöka relationen använde vi en lineär OLS regression ekvation användes:""")
    st.write("""y = a * X + c """)
    
    st.image('../plottar/reg_results_sav_bygg_linear.png', width = 700)
    st.image('../plottar/bygg_wind_sav_linear.png', width = 700)
    st.write("""Resultatet visar att en lineärregression model är signifikant (p = 0,0248) med en R-squared värde av 16,7%. Kumulativt antal lägenheter koefficienten var signifikant (p = 0,025) och är relaterad till en 0,00000377 °C årlig minskning i snitttemperatur i genomsnitt. 
              
    """)
    st.write("""Det verkar som relationen är dock heteroskedastic, eller att vindhastighets variation minskas när byggnation ökas. Detta står i konflikt med OLS-antagandet om homoskedasticitet. 
    """)
    st.write(""" Skulle det vara så att relationen mellan byggnation och vindhastigheten starkas medan mer lägenheter byggs?""")

    st.header("""Har vinden blivit svagare i Säve från riktningen av Göteborg?""")
 

    # wind direction Rose plots 
    vinddir_gbg_1 = "../plottar/windrose_all_winds_pre_1992_gbg.png"
    vinddir_gbg_2 = "../plottar/windrose_all_winds_post_1992_gbg.png"
    vinddir_sav_1 = "../plottar/windrose_all_winds_pre_1978_save.png"
    vinddir_sav_2 = "../plottar/windrose_all_winds_post_1978_save.png"
    vinddir_vinga_1 = "../plottar/windrose_all_winds_pre_1978_vinga.png"
    vinddir_vinga_2 = "../plottar/windrose_all_winds_post_1978_vinga.png"
    '\n'
    '\n'

    st.write('Förklaring av vindrosor:  \n0 grader: Norr  \n90 grader: Öst  \n180 grader: Syd  \n270 grader: Väst')
    st.write('Varje arm täcker 22.5 grader. Så armern rakt norrut täcker vindar från 348.75 grader till 11.25 grader')
    st.write('Cirklarna visar andelen av observationerna i procent.')
    st.write('Färgerna visar vindhastigheten')
    selected_location = st.selectbox("Select Location", ["GBG", "Säve", "Vinga"])

        # Use if-else conditions to display the appropriate visuals
    if selected_location == "GBG":
        col1, col2 = st.columns(2)
        with col1:
            st.image(vinddir_gbg_1, caption="GBG Snittvindhastighet p/dag")
        with col2:
            st.image(vinddir_gbg_2, caption="GBG Snittvindhastighet p/dag")
    elif selected_location == "Säve":
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

    #### Look at reliability
    '\n'
    st.write('I Göteborgs-datan så mättes färre vindriktningar tidigare, men så är inte fallet med Säve och Vinga')
    st.write('I vindrosorna ovan är det stora skillnader i Göteborg och även Vinga, men inte i Säve.  \nVi kan titta på antalet observationer över tid för att se om detta påverkar.')

    no_meassurements_save = ('../Olof_viz/wind_meassurements_per_year_save.png')
    no_meassurements_gbg = ('../Olof_viz/wind_meassurements_per_year_gbg.png')
    no_meassurements_vinga = "../plottar/wind_meassurements_per_year_vinga.png"
    st.image(no_meassurements_save, caption='Antalet mätningar per år är ungefär samma sedan 1960')
    st.image(no_meassurements_gbg, caption='Drastisk skillnad i Göteborg')
    st.image(no_meassurements_vinga, caption='Stor skilnad även på Vinga')
    '\n'
    
    #### Change of directions, all winds
    st.write('Den enda riktningen där andelen vinddagar minskar är från 0 grader till 90 grader')
    winds_from_NE_save = ('../Olof_viz/change_of_wind_0_90_save.png')
    winds_from_NE_vinga = ('../Olof_viz/change_of_wind_0_90_vinga.png')
    st.image(winds_from_NE_save, caption='Andelen dagar med uppmätta vindar från 0-90, Säve')
    st.write('Detta gäller dock inte Vinga')
    st.image(winds_from_NE_vinga, caption='Andelen dagar med uppmätta vindar från 0-90, Vinga')

    #### Harder winds
    st.title('Hårdare vindar')
    hard_winds_over_time = ('../Olof_viz/hard_winds_over_time_comparison.png')
    st.image(hard_winds_over_time)



    hard_winds_over_time_save = "../plottar/hard_winds_save_barplot.png"
    hard_winds_over_time_vinga = "../plottar/hard_winds_vinga_barplot.png"
    st.image(hard_winds_over_time_save)
    st.image(hard_winds_over_time_vinga)
   

if nav == 'Temperatur':
    total_temps_plus_adjusted = ('../Olof_viz/medeltemperaturer.png')
    temp_diff = ('../Olof_viz/temp_diff_gbg_save.png')
    unadjusted = ('../Olof_viz/medeltemp_ojusterad.png')
    adjusted = ('../Olof_viz/medeltemp_justerad.png')
    both_datasets_compared = ('../plottar/temp_skilnad_snitt_gbg_save_resp_dataset.png')
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
        st.image(adjusted, caption='Justerat dataset, där temperaturerna från 2006 och framåt justerats enligt resultaten ovan')

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


if nav == 'Relationen mellan nederbörd & temperatur':
    st.title("Relationen mellan nederbörd & temperatur")
    st.write("På tidigare sidor har vi utforskat både temperatur och nederbörd i detalj. Syftet med denna sida är att upptäcka hur de två samverkar över tiden")
    st.header("Summary Statistics:")
    st.image("../plottar/sum_stat_temp_nederbörd.png", width=400)
    st.write("Histogram för både genomsnittlig månadstemperatur och total månatlig nederbörd:")
    st.image("../plottar/histogram_temp_nederbörd.png", width=700)
    st.write("Månatlig genomsnittstemperatur versus total månatlig nederbörd:")
    st.image("../plottar/scatter_temp_nederbörd.png", width = 700)
    st.write("Scatterplottan för månatlig genomsnittstemperatur gentemot total månatlig nederbörd visar ett möjligt heteroskedastiskt förhållande.  När den genomsnittliga temperaturen stiger, ökar omfånget av total månatlig nederbörd. ")
    st.header("Regression")
    st.write("En OLS-linjär regression används för att uttrycka förhållandet mellan genomsnittlig månadstemperatur och månatlig total nederbörd.")
    st.write("Ekvationen är: Y = a * X + b")
    st.image("../plottar/reg_results_ned_temp.png", width = 700)
    st.image("../plottar/scatter_trendline_temp_ned.png", width=700)
    st.write("""
    Snitt månadstemperatur är signifikant relaterad till 2,5% av förändringen i total månatlig nederbörd. Det föreslår att en ökning med en grad är relaterad till en ökning av 0,8956 mm i nederbörd.
    """)
    st.write("""
    Kan det vara så att det lilla sambandet beror på det måttliga förhållandet mellan temperatur och nederbörd vid temperaturer under noll?
    """)
    st.image("../plottar/reg_results_ned_temp_overzero.png", width = 700)
    st.image("../plottar/scatter_temp-ned_over_freezing_trend.png", width=700)
    st.write("""Det verkar så. När man tar bort temperaturer under 0°C blir modellen och koefficienterna insignifikanta.
    """)
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