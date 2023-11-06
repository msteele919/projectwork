import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

precip = pd.read_pickle("../Dataframes/df_compiled_daily_precipitation_gbg_save.pkl")
snodjup = pd.read_pickle("../Dataframes/df_snow_save.pkl")
aprilregn = ("../plottar/aprilregn.png")
oktoberregn = ("../plottar/oktoberregn.png")


nav = st.sidebar.radio('Meny',['Syfte och frågeställning', 'Nederbörd', 'Snödjup'])
if nav == 'Syfte och frågeställning':
    st.title('Undersökning av väderdata kring Göteborgsområdet från 1944 till 2023')
    st.header('Syftet med valt projekt:')
    st.write("""1. Kan man med hjälp av historisk väderdata se trender kring förändringar i vädret kring göteborgsområdet?
             \n2. Har regn ändrats?
             \n3. Har snödjupet ändrats? 
             \n4. Kan vi förutspå hur vädret ser ut i till exempel Juli 2028? 
             """)

    st.write('')


if nav == 'Nederbörd':
    st.title('Nederbörd')
    st.subheader('Beskrivning av dataset')
    st.write("""Regndatan är insamlad från mätstationerna i Säve och i Göteborg. Datan från Säve är insamlad från första januari 1944 och sträcker sig till 30e november 2002.
             Göteborgsdatan var inkomplett, så vi har valt att ta vid Göteborgsdatan där Sävedatan slutar, så hela datasettet sträcker sig till sista juni i år.
             \nMängden nederbörd mäts i millimeter, vilket är ett mått på hur högt vattnet skulle nå ovan marken om det inte sjönk undan.""")
    st.subheader('Hur ser det ut med nederbörden?')
    st.image("../plottar/snittnederbördövertid.png")
    st.write("""Enligt grafen så verkar det pendla en del mellan åren, men det verkar ju som att det snittnederbörden ökar över tid.
             Vi kan dubbelkolla detta genom att göra en plot med en trendlinje som med enkel linjär regression räknar ut ett samband mellan genomsnitssregnfall och datum.
             \nNågonting hände där vid 2008, kan vi se när det blev av?""")
    st.image("../plottar/regn200808.png")
    st.write('Där ser vi att det regnade som fasen den 27e augusti.')
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


if nav == 'Snödjup':
    st.title('Snödjup')
    st.subheader('Information om datan')
    st.write(f"""Snödjupet är mätt på Säve mätstation som ligger vid Säve flygplats. Datan är insamlad mellan januari 1944 och december 2003 och mäts i meter.
             \nDet är lite glapp i informationen i form av bristande mätningar över åren.""")
    if st.checkbox('Visa antal observationer per år.'):
        st.write(snodjup.Year.value_counts())
    st.subheader("""Hur ser det ut egentligen med snö över tid?""")
    st.write("Snödjup i meter")
    st.write(f"Minsta snödjup: {snodjup['Snödjup'].min()}m")
    st.write(f"Medelsnödjup över alla år: {round(snodjup['Snödjup'].mean(),3)}m")
    st.write(f"Max uppmätta snödjupet: {snodjup['Snödjup'].max()}m")
    st.subheader('Vi tittar på perioden då det snöar.')
    st.image("../plottar/snodjuppermånad.png")
    st.write("""Det är ju rimligt att snö-observationerna är mellan januari och maj och oktober och december då det inte snöar under sommaren.""")
    
    