
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

avgmonthlytemp = pd.read_csv("../projectwork/data/avg_monthly_temp_curated.csv")

testplot = plt.plot(avgmonthlytemp['Month'], avgmonthlytemp['Snittemperatur'])
plt.xlabel('År')
plt.ylabel('Temperatur i °C')
plt.xlim(left=0, right=84)
plt.xticks(ticks=[0, 12, 24, 36, 48, 60, 72, 84], labels=["'61", "'62", "'63","'64","'65","'66","'67", "'68"])
testplot = plt.savefig('testplot')

# >>> fig, ax = plt.subplots()
# >>> ax.scatter([1, 2, 3], [1, 2, 3])
# >>>    ... other plotting actions ...
# >>> st.pyplot(fig)



# Creating the menu
nav = st.sidebar.radio('Meny',['Syfte', 'Data & Modellering', 'Förutsägelser om framtiden', 'Slutsats och reflektioner'])
if nav == 'Syfte':
    st.title('Undersökning av väderdata kring Göteborgsområdet från 1961 till 2023')
    st.header('Syftet med valt projekt:')
    st.write("""1. Kan man med hjälp av historisk väderdata se trender kring förändringar i vädret?
             \n2. Har regn blivit mer intensivt under de senaste 50 åren?
             \n3. Har åskoväder och stormar blivit mer intensiva under de senaste 50 åren?
             \n4. Har snödjupet ändrats? 
             \n5. Kan vi förutspå hur vädret ser ut i till exempel Juli 2028? 
             """)

    st.write('Funkar det?')

if nav == 'Data & Modellering':
    st.title('Data & Modellering')
    st.write('I denna sektionen kommer vi att presentera data tillsammans med våra slutsatser och observationer.')

    st.header('Grafisk presentation av insamlad data')
    st.subheader('Månatlig snittemperatur från 1961 till 1968')
    st.set_option('deprecation.showPyplotGlobalUse', False) # Döljer felmeddelandet från st.pyplot
    st.pyplot(testplot)
    st.write("""Vi ser klart och tydligt att snittemperaturen under 7 år är för lite information för att göra någonting med.
            \nKommer mer data att visa någonting annat?""")
    st.write(' ')


    st.subheader('Rådata')
    st.write('För att ta del av rådatan till snittemperaturen per månad klicka i boxen')
    if st.checkbox('Visa rådata'):
        st.write(avgmonthlytemp)

if nav == 'Förutsägelser om framtiden':
    st.header('Temperatur:')
    st.title('Placeholder för algoritmen. Nedan visas grafer')
    st.write('Här kommer slutsatsen för frågeställningarna att visas.')

if nav == 'Slutsats och reflektioner':
    st.title('Slutsats')
    st.write("""Här är en placeholder för vår slutsats.\n""")
    st.subheader('Reflektioner')
    st.write("""Här är en placeholder för våra reflektioner som vi skall skriva. Kommer vi att vilja ha 3st subheaders för oss var?""")