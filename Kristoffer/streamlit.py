
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

## avg monthly temp plot 
avgmonthlytemp = pd.read_csv("../projectwork/data/avg_monthly_temp_curated.csv")

testplot = plt.plot(avgmonthlytemp['Month'], avgmonthlytemp['Snittemperatur'])
plt.xlabel('År')
plt.ylabel('Temperatur i °C')
plt.xlim(left=0, right=84)
plt.xticks(ticks=[0, 12, 24, 36, 48, 60, 72, 84], labels=["'61", "'62", "'63","'64","'65","'66","'67", "'68"])
testplot = plt.savefig('testplot')

## Förutsägelser om framtiden slides plottar 

# train_test split 
train_test_path = os.path.join("brainstorming/temp_prediktion", "train_test.png")
image = plt.imread(train_test_path)
# prediktion bad 
prediktion = os.path.join("brainstorming/temp_prediktion", "prediktion_bad.png")
pred_bad = plt.imread(prediktion)
#grid_search
grid = os.path.join("brainstorming/temp_prediktion", "grid_search.png")
grid_s = plt.imread(grid)


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
    st.title('Förutsägelser om framtids snitt temperatur')
    st.write('Med temperaturdata från Save väder station har en recursive multisteg autoregressiv modell använts inom sciket learn.')
    st.header('Metodik:')
    st.write('En recursive multi-step autoregressiv modell är ett sätt att kunna använda time series data och förutsäga framtida värde. I en recursiv autoregression modell, ett antal steg (lags) används som modellen ska basera sina predikteringar på. Denna siffra bestämdes efter en grid search. Lag som fick lägste root mean square error var 30 dagar. Detta skulle då representera månadsvis trender. ')
    st.header('Placeholder för algoritmen. Nedan visas grafer:')
    st.subheader('Data Split med Save data. Training data innan 2010-01-01')
    st.image(image)
    st.subheader('Resultat från gridsearch.')
    st.write('Lag med 30 dagar visade sig ha bäst root mean square error')
    st.image(grid_s)
    st.subheader('Resultat från prediktion')
    st.image(pred_bad)
    st.write('Root Mean square error var faktiskt hög för denna modell. 13,59°C root mean square visar att så länge modellen har ingen bra förmågan att prediktera temperatur. Nästa steget skulle vara att använder en seasonal ARIMA modell. Då denna modell tog hansyn till månadsvis skillnader säsong förändringar måste tänkas över.')

if nav == 'Slutsats och reflektioner':
    st.title('Slutsats')
    st.write("""Här är en placeholder för vår slutsats.\n""")
    st.subheader('Reflektioner')
    st.write("""Här är en placeholder för våra reflektioner som vi skall skriva. Kommer vi att vilja ha 3st subheaders för oss var?""")