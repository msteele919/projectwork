import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

nav = st.sidebar.radio('Huvudmeny', ['Bakgrund', 'Frågeställning', 'EDA', 'Platsinformation',  'Vind', 'Snödjup', 'Nederbörd', 'Temperatur', 'Relationen mellan nederbörd & temperatur','Sommarens och vinterns ankomst' ])

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
    st.title('Överblick över wind data')
    st.write("""Som i de andra exempel tänkte vi konkatenera Säve och Göteborgs data för att kunna få en datamängd som sträckte sig över en längre period, från 1944 till 2023. Med knapparna nedan kan man se varenda plotta och sedan Göteborg och Säve data sammanställt. 
            """)
    
    # Meta knappar: välj mellan säve, Göteborg, Säve & Göteborg
    vind_1 = "../plottar/mean_wind_daily_gbg.png"
    vind_2 = "../plottar/mean_wind_daily_sv.png"
    vind_3 = "../plottar/mean_wind_daily_sv_gt.png"
    compare_visuals = [ vind_1, vind_2, vind_3]

    visual_names = ["GBG Snittvindhastighet p/dag", "Säve Snittvindhastighet p/dag", "GBG, Säve sammanlagt, Snittvindhastighet p/dag"]
    # Display the current visual based on a user-selected name
    current_index = st.selectbox("Välj stationen", visual_names, index=0)
    visual_index = visual_names.index(current_index)  # Get the index of the selected name
    st.image(compare_visuals[visual_index], caption=current_index)
    
    st.title('En läringsprocess: Finns det en trend i vind hastighet över tid och går det att jämföra Göteborg och Säve?')

    st.write("""När vi tittade på den sammanställda snittvindhästighets datamängden från Säve/Göteborg trodde vi först att det visades en negativ trend i Göteborg/Säves vindhastighet övertid.
            """)
    st.write("""Var detta en välgrundad slutsats? Följ med på vår journey och ta reda på det""")

    st.write("""När vi försökte ta reda på varför vindhastigheten hade minskat i Göteborg/Säve data mängden påstådde vi att byggnation i Göteborg över tid skulle kunna stå för den minskning. 
                """)

    


    # intensitivitet över tiden 


    # wind direction Rose plots 
    vinddir_gbg_1 = "../plottar/wind_dir_gbg_pre1980.png"
    vinddir_gbg_2 = "../plottar/wind_dir_gbg_post1980.png"
    vinddir_sav_1 = "../plottar/wind_dir_sav_pre1980.png"
    vinddir_sav_2 = "../plottar/wind_dir_sav_post1980.png"
    
    selected_location = st.selectbox("Välj stationen", ["GBG", "Säve"])

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
             rättvisande. Annars kan snittemperaturen stiga drastisk när vi tar data från Göteborg, Annars kan snittemperaturen stiga drastisk när vi tar data från Göteborg, 
             utan att det nödvändigtvis var varmare.''')
    
    st.image(temp_diff, caption='''Skillnader i månadstemperatur mellan Görborg och Säve under den överlappande perioden 1961 till 2006. 
             Visar hur mycket varmare/kallare Göteborg var än Säve. Vid positivt tal var Göteborg varmare''')
    

    col1, col2 = st.columns(2)
    with col1:
        st.image(unadjusted, caption='Sammansatt dataset av data från Säve fram till 2006.')
    with col2:
        st.image(adjusted, caption='Justerat dataset, där temperaturerna från 2006 och framåt justerats enlit resultaten ovan')

if nav == 'Relationen mellan nederbörd & temperatur':
    st.title("Relationen mellan nederbörd & temperatur")
    st.write("På tidigare sidor har vi utforskat både temperatur och nederbörd i detalj. Syftet med denna sida är att upptäcka hur de två samverkar över tiden")
    st.header("Summary Statistics:")
    st.image("../plottar/sum_stat_temp_nederbörd.png", width=400)
    st.write("Histogram för både genomsnittlig månadstemperatur och total månatlig nederbörd:")
    st.image("../plottar/histogram_temp_nederbörd.png", width=700)
    st.write("Månatlig genomsnittstemperatur versus total månatlig nederbörd:")
    st.image("../plottar/scatter_temp_nederbörd.png", width = 700)
    st.write("Scatterplottan för månatlig genomsnittstemperatur gentemot total månatlig nederbörd visar ett möjligt heteroskedastiskt förhållande. Det verkar som att när snittemperatur är låg, är även total nederbörd låg. När den genomsnittliga temperaturen stiger, ökar omfånget av total månatlig nederbörd. När den genomsnittliga månadstemperaturen når cirka 0 till 2 °C, verkar förhållandet mellan de två variablerna helt okorrelerat, om inte visar en svagt positiv korrelation.")
    st.header("Regression")
    st.write("En OLS-linjär regression används för att uttrycka förhållandet mellan genomsnittlig månadstemperatur och månatlig total nederbörd.")
    st.write("Den enkla ekvationen är: y = a + b * x + C")
    st.write(" Vid första anblicken verkar variablerna kunna ha potentiellt oroväckande egenskaper för att köra en OLS. Som tidigare nämnts förefaller det finnas heteroskedasticitet. Därför används robust kovarians för att hjälpa till att rätta till koefficienterna för heteroskedasticitet.")
    st.image("../plottar/reg_results_ned_temp.png", width = 700)
    st.image("../plottar/scatter_trendline_temp_ned.png", width=700)
    st.write("""
    Den linjära OLS-modellen är statistiskt signifikant med en F-poäng på 26,04 (p = 4,04e-07). R-torget är 2,25%. Koefficienterna är en intercep för 60,955 (p = 0,000) och koefficienten för månatlig genomsnittstemperatur är 0,89 (p = 0,000).
    Detta resultat tyder på att genomsnittlig månadstemperaturdata är signifikant relaterad till 2,5% av förändringen i total månatlig nederbörd i datasetet. Det är inte mycket, men det kan ha konsekvenser att säga att temperaturen har en viss liten prediktiv korrelation med nederbördsvolymerna. Det föreslår att i denna dataset är en ökning med en enhet i temperaturen relaterad till en ökning av 0,8956 mm i nederbörd.
    Som syns i spridningsdiagrammet är trendlinjen inte brant. Det är möjligt att överväga att den positiva lutningen kan relatera till den initiala positiva förändringen vid lägre temperaturer och även det möjligtvis heteroskedastiska förhållandet som verkar finnas i hela datasetet.""")
   

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
