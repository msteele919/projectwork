import pandas as pd
import sqlite3


class WeatherDatabase:
    url: str

    def __init__(self, url: str, *args):
        self.url = url
        con = sqlite3.connect(url)
        cur = con.cursor()
        for table in args:
            con.execute(
                f"""
                CREATE DATABASE IF NOT EXISTS Expences
                """)
        cur.close()
        con.commit()
        con.close()

    def call_db(self, query, *args):
        con = sqlite3.connect(self.url)
        cur = con.cursor()
        res = cur.execute(query, args)
        data = res.fetchall()
        cur.close()
        con.commit()
        con.close()
        return data
    
db = WeatherDatabase('../Database/WeatherGBG.db')
    
conn = sqlite3.connect('../Database/WeatherGBG.db')

# Queery

df_warmer_union = pd.read_sql("""WITH Temp_comp AS (
                        SELECT *, LAG(Avg_daily_temp) OVER (ORDER BY Datum_date) AS Prev_temp
                        FROM 
                            (SELECT *, ROUND(AVG(Lufttemperatur), 2) AS Avg_daily_temp 
                            FROM Temp_save_raw 
                            GROUP BY Datum_date
                                UNION ALL
                            SELECT *, ROUND(AVG(Lufttemperatur), 2) AS Avg_daily_temp 
                            FROM Temp_GBG_raw 
                            WHERE Datum_date > '2006-12-05'
                            GROUP BY Datum_date))
                        SELECT *,
                        CASE WHEN Avg_daily_temp > Prev_temp THEN 1
                        ELSE 0
                        END AS Warmer
                        FROM Temp_comp;
                        """, conn, parse_dates=['Datum_date']).drop(columns=['Tid_UTC', 'id']).drop(columns=['Prev_temp'])

# Create column to see when summer has arrived

df_warmer_union['Över_10_grader_i_5_dagar'] = 0
counter = 0
for ind, val in df_warmer_union[1:].iterrows():
    temp_prev = df_warmer_union[ind-1:ind]['Avg_daily_temp'][ind-1]
    if val['Avg_daily_temp'] > 10:
        counter += 1
    else:
        counter = 0
    if counter >= 5:
        df_warmer_union.loc[ind, 'Över_10_grader_i_5_dagar'] = 1
    else:
        pass


df_warmer_union = df_warmer_union.drop(columns=['Warmer'])

def get_first_summer_day_per_year(year):
    for ind, val in df_warmer_union[df_warmer_union['Datum_date'].dt.year == year].iterrows():
        if df_warmer_union['Över_10_grader_i_5_dagar'][ind] == 1:
            first_summer_day = df_warmer_union['Datum_date'][ind-4].strftime('%Y-%m-%d')
            return first_summer_day
            break
        else:
            pass
    return None


# Create column to see when winter has arrived

df_warmer_union['Under_0_grader_i_5_dagar'] = 0
counter = 0
for ind, val in df_warmer_union[1:].iterrows():
    temp_prev = df_warmer_union[ind-1:ind]['Avg_daily_temp'][ind-1]
    if val['Avg_daily_temp'] <= 0:
        counter += 1
    else:
        counter = 0
    if counter >= 5:
        df_warmer_union.loc[ind, 'Under_0_grader_i_5_dagar'] = 1
    else:
        pass

def get_first_winter_day_per_year(year):
    for ind, val in df_warmer_union[(df_warmer_union['Datum_date'].dt.year == year) & (df_warmer_union['Datum_date'].dt.month > 6)].iterrows():
        if df_warmer_union['Under_0_grader_i_5_dagar'][ind] == 1:
            first_winter_day = df_warmer_union['Datum_date'][ind-4].strftime('%Y-%m-%d')
            return first_winter_day
            break
        else:
            pass

    return None