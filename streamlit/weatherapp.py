import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


nav = st.sidebar.radio('Huvudmeny', ['Bakgrund & frågeställning', 'Platsinformation', 'Vind',
                                      'Nederbörd', 'Temperatur', 'Relationen mellan nederbörd & temperatur', 'Temperatur prediktion', 'Slutsatser'])


if nav == 'Bakgrund & frågeställning':
    st.header("Introduktion")
    st.write("""Det här projektet undersöker väderdata i Göteborgsområdet med hjälp av SMHI-data.


\nData mängder som användes var:
\n    - Temperaturdata från Göteborg & Säve
    - Nederbörddata från Göteborg & Säve
    - Vinddata från Göteborg, Säve och Vinga


Målet med projektet var att analysera väderdata och se hur det har förändrats över
tid.""")
    st.header("Frågeställning")
    st.write('''1. Hur har temperaturen ändrats över tid? Vilken variation finns mellan
olika månader?
            \n2. Hur har vindriktning och vindhastighet ändrats över tid? Vilka skillander
kan vi se mellan skärgården och fastlandet?
            \n3. Regnar det mer eller mindre nu än förr?
            \n4. Finns det en korrelation mellan temperatur och nederbörd över tid?
            \n5.  Hur skulle framtida temperaturer vara i Göteborg baserat på
historiska temperaturtrender?''')


if nav == 'Platsinformation':
    st.title('Stationernas platser Göteborg')
    st.write("Under åren har mätstationen i Göteborg stått på olika ställen. \nSedan 1998 är den belägen vid Gullbergsvass")


    st.write('Säve ligger på Hisingen, ungefär 10km fågelvägen från centrala Göteborg. Stationen har inte flyttats. Vinga ligger ute i skärgården.')
    current_station_gbg_lat_long = [57.7156, 11.9924]
    stations = pd.read_pickle('../Dataframes/station_info.pkl')
    green_hex = '#06a94d'
    red_hex = '#EE0000'
    for ind, row in stations.iterrows():
        if row['LON'] == current_station_gbg_lat_long[1]:
            stations.at[ind, 'Colour'] = green_hex
        else:
            stations.at[ind, 'Colour'] = red_hex
    st.map(stations, latitude='LAT', longitude='LON', zoom=9.5, size=500, color='Colour')


if nav == 'Nederbörd':
    precip = pd.read_pickle("../Dataframes/df_compiled_daily_precipitation_gbg_save.pkl")
    st.title('Nederbörd')
    st.subheader('Beskrivning av dataset')
    st.write("""Regndatan är insamlad från mätstationerna i Säve och i Göteborg. Datan från Säve är insamlad från första januari 1944 och sträcker sig till 30e november 2002.
             Göteborgsdatan var inkomplett, så vi har valt att ta vid Göteborgsdatan där Sävedatan slutar, så hela datasettet sträcker sig till sista juni i år.
             \nMängden nederbörd mäts i millimeter, vilket är ett mått på hur högt vattnet skulle nå ovan marken om det inte sjönk undan.""")
    st.subheader('Hur ser det ut med nederbörden?')
    st.image("../plottar/snittnederbördövertid.png")
    st.write("""Enligt grafen så verkar det pendla en del mellan åren, men det verkar ju som att det snittnederbörden ökar över tid.
             Vi kan dubbelkolla detta genom att göra en plot med en trendlinje som med enkel linjär regression räknar ut ett samband mellan genomsnitssregnfall och datum.""")
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
    st.title('Överblick över vind-data ')
    st.write('"Den vindhastighet som meteorologen anger i prognoser och flertalet av våra mätningar avser ett medelvärde under 10 minuter av vindhastigheten på 10 meters höjd ovan markytan." /SMHI')
    vind_1 = "../plottar/mean_wind_daily_sv.png"
    vind_2 = "../plottar/mean_wind_daily_gbg.png"
    vind_3 = "../plottar/mean_wind_daily_vinga.png"
   
    compare_visuals = [ vind_1, vind_2, vind_3]

    visual_names = ["Säve Snittvindhastighet p/dag", "GBG Snittvindhastighet p/dag", "Vinga Snittvindhastighet p/dag"]
    # Display the current visual based on a user-selected name
    current_index = st.selectbox("Välj Dataset", visual_names, index=0)
    visual_index = visual_names.index(current_index)  # Get the index of the selected name
    st.image(compare_visuals[visual_index], caption=current_index)

    st.write("""När vi tittar på vinddata över tid märker vi en minskning av den genomsnittliga vindhastigheten per dag.
            Skulle vindminskningen i Säve vara en effekt av ökad byggnation i Göteborg?
            """)
    st.header('Är vind minskning i Säve relaterad med byggnation i Göteborg?')
    st.write("""Bygnationsdata""")
    st.write("""Vi beräknade den kummulativa nybyggdlägenhetsmängd i Göteborg från 1975 - 2006, när Säve datamängden slutades.  """)
    st.write("""Källa: SCBs datamängden:  "Färdigställda lägenheter och rumsenheter i nybyggda hus i Göteborg från 1975-2022""")
    st.image('../plottar/kumulativ_lägenheter_gbg.png', width=700)
    st.write("""När kumulativt antal lägenheter plottas mot årlig vindhastighet i Säve verkar det som det finns en moderat till svag negativ relation.""")

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
 




    selected_location = st.selectbox("Select Location", ["Säve", "Vinga"]) # Removed GBG
    vinddir_gbg_1 = "../plottar/windrose_all_winds_pre_1992_gbg.png"
    vinddir_gbg_2 = "../plottar/windrose_all_winds_post_1992_gbg.png"
    vinddir_sav_1 = "../plottar/windrose_all_winds_pre_1990_save.png"
    vinddir_sav_2 = "../plottar/windrose_all_winds_post_1990_save.png"
    vinddir_vinga_1 = "../plottar/windrose_all_winds_pre_1990_vinga.png"
    vinddir_vinga_2 = "../plottar/windrose_all_winds_post_1990_vinga.png"




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
    st.write('- Cirklarna visar andelen av observationerna i procent.')
    st.write('- Färgerna visar vindhastigheten')
    st.write('- Automatiska proportioner')
    st.write('Har de kraftigare vindarna ändrat riktning?')
    hard_winds_save_pre_1978 = ('../plottar/windrose_hard_winds_pre_1990_save.png')
    hard_winds_save_post_1978 = ('../plottar/windrose_hard_winds_post_1990_save.png')
    col1, col2, = st.columns(2)
    with col1:
        st.image(hard_winds_save_pre_1978)
    with col2:
        st.image(hard_winds_save_post_1978)

    #### Harder winds

    hard_winds_over_time = ('../Olof_viz/hard_winds_over_time_comparison.png')
    hard_winds_over_time_save = "../plottar/hard_winds_save_barplot.png"
    hard_winds_over_time_vinga = "../plottar/hard_winds_vinga_barplot.png"
    # '\n'
    st.write('1978 är halvvägs mellan början på tillförlitlig data (1950) och sista mätningen i Säve (2006)')
    st.image(hard_winds_over_time_save, caption='Drastisk minskning i andra halvan av datasetet.')
    st.image(hard_winds_over_time_vinga, 'Ganska stor ökning, förmodligen relaterat till det högre antalet mätningar per år.')
    st.write('Slutsats: Större andel kraftiga vindar från söder, men överlag lägre hastigheter.')
    st.write('Ingen större skilnad i vindar från Göteborgs-hållet.')


if nav == 'Temperatur':
    total_temps_plus_adjusted = ('../Olof_viz/medeltemperaturer.png')
    temp_diff = ('../Olof_viz/temp_diff_gbg_save.png')
    medeltemp = ('../plottar/medeltemp_sammanslaget.png')
    both_datasets_compared = ('../plottar/temp_skilnad_snitt_gbg_save_resp_dataset.png')
    st.title('Temperaturdata')
    st.text('Data för Säve: 1944-2006 \nData för Göteborg: 1961-2023')
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


    st.write('Modellen fångar en svag ökning i snitt temperatur över tiden. Den prediktera att snitt temperaturen i Juli 2042 blir 18,68°C, uppe från 18,43°C i Juli 2022')
if nav == 'Relationen mellan nederbörd & temperatur':
    st.title("Relationen mellan nederbörd & temperatur")
    st.write("På tidigare sidor har vi utforskat både temperatur och nederbörd i detalj. Syftet med denna sida är att upptäcka hur de två samverkar över tiden")
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




if nav == 'Temperatur prediktion':
    st.title('Vad skulle framtida temperaturer i Göteborg vara baserade på historiska temperaturtrender?')
    st.write('När man ser på temperaturen över tid verkar det finnas en positiv trend.')
    st.image('../plottar/pred_temp_snitt_overtid.png', width=700)
    st.header('Metod')
    st.write('En SARIMA-modell används med tidsseriedata när det finns säsongsbetonade trender i datan som måste beaktas.')
    st.write("""Data split
    Vi tittade på månatlig genomsnittstemperatur och bröt upp datan i
    tränings- 1944 - 2017
    validerings-  2017 - 2022
    testdata- 2022 - 2023""")
    st.image('../plottar/pred_test_train_val_split.png', width=700)
    st.write('Modellens prestanda')
    st.image('../plottar/pred_temp_performance graphs.png', width= 700)
    st.write('Prestandan för modellen mättes med ett RMSE på 1.9768 °C.')
    st.write('Modelens predikterad värden vs test data')
    st.image('../plottar/pred_temp_2023_perforamance.png', width = 700)    
    st.write('Att extrapolera modellen över tid. Vad blir temperaturen om 20 år?')
    st.image('../plottar/pred_temperature_till_2042.png', width=700)
if nav == 'Slutsatser':
    st.title("Slutsatser")
    st.write("""- Temperaturfäändringen stämmer bra med vad man har hört om global uppvärming; varmare vintrar, svalare somrar.  
             \n- Ingen påvisbar effekt av byggnation i Göteborg på vindriktingingar i Säve.
             \n- Alla månader blir blötare, men det är lite mindre ökning på sommaren.
             \n- Temperaturer över 0 grader verkar vara orelaterat till total nederbördsmängd.""")
    st.subheader('Potentiell vidareutveckling')
    st.write("""- Hur kan man förklara minskningen av vind i Säve?
             \n - Korrelation mellan vind och nederbörd?
             \n - Korrelation mellan vind och temperatur?
             \n - Mer specifika frågor över bredare områden.""")

