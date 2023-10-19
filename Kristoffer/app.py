import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

monthly = pd.read_pickle("../Dataframes/df_monthly_temp.pkl")

sns.scatterplot(x=monthly['Month'], y=monthly['Monthly avg'], data=monthly)
sns.lineplot(x='Month', y= 'Monthly avg', data=monthly, errorbar=('ci', 0))
plt.xlabel('Månad')
plt.ylabel('Temperatur i °C')
plt.xticks(ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
           labels=['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'])
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
    st.subheader('Månatlig snittemperatur')
    st.set_option('deprecation.showPyplotGlobalUse', False) # Döljer felmeddelandet från st.pyplot
    st.pyplot(testplot)
    st.write("""Vi ser här medelvärdet av temperaturen per månad.
            \nKommer mer data att visa någonting annat?""")
    st.write(' ')


    st.subheader('Rådata')
    st.write('För att ta del av rådatan till snittemperaturen per månad klicka i boxen')
    if st.checkbox('Visa rådata'):
        st.write(monthly)

if nav == 'Förutsägelser om framtiden':
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