import pickle
import pandas as pd
import xgboost as xgb
from flask import Flask, request, render_template
import plotly.graph_objects as go
import math
from math import radians
from math import sin
from math import cos
from math import asin
from math import asin
from math import sqrt
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


with open('xgbmodel.pkl', 'rb') as f:
    xgbmodel = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        input_data = request.form.to_dict()


        matchdf = pd.read_csv('tofitdata.csv')
        OE = pd.read_csv('../oe.csv')

        user_input_df=pd.DataFrame()
        user_input_df['Origin']=input_data['Origin']
        user_input_df['Dest']=input_data['Dest']

        def haversine(lon1, lat1, lon2, lat2):
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))

            km = 6371 * c
            return km


        airport_coords = {'ATL': (-84.4281, 33.6367),
                        'CLT': (-80.9431, 35.2140),
                        'DEN': (-104.6737, 39.8561),
                        'DFW': (-97.0403, 32.8998),
                        'EWR': (-74.1687, 40.6925),
                        'IAH': (-95.3414, 29.9844),
                        'JFK': (-73.7789, 40.6398),
                        'LAS': (-115.1523, 36.0804),
                        'LAX': (-118.4085, 33.9416),
                        'MCO': (-81.3089, 28.4294),
                        'MIA': (-80.2906, 25.7933),
                        'ORD': (-87.9073, 41.9742),
                        'PHX': (-112.0116, 33.4342),
                        'SEA': (-122.3088, 47.4502),
                        'SFO': (-122.3748, 37.6189)}

        fig = go.Figure()

        origin=input_data['Origin']
        destination=input_data['Dest']
        #dist bt origin and destination
        dist_km = haversine(airport_coords[origin][0], airport_coords[origin][1],
                            airport_coords[destination][0], airport_coords[destination][1])
        dist_mi = dist_km * 0.621371

        time_hrs = (dist_mi / 560.0)+1
        time_mins = int(time_hrs * 60)

        for airport, coord in airport_coords.items():
            fig.add_trace(
                go.Scattergeo(
                    locationmode='USA-states',
                    lon=[coord[0]],
                    lat=[coord[1]],
                    mode='markers',
                    marker=dict(size=5, color='red'),
                    name=airport,
                )
            )
        fig.add_trace(
            go.Scattergeo(
                locationmode='USA-states',
                lon=[airport_coords[origin][0], airport_coords[destination][0]],
                lat=[airport_coords[origin][1], airport_coords[destination][1]],
                mode='lines',
                line=dict(width=1, color='blue'),
                name=str(origin+" to "+destination),

                opacity=0.7,
            )
        )
        fig.update_layout(
            title_text='Flight path between {} and {}<br>(Hover for airport names)'.format(origin, destination),
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)',
                subunitcolor='rgb(217, 217, 217)',
                subunitwidth=0.5,
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
                showsubunits=True,
                showcountries=True,
                resolution=50,
            ),

        annotations=[
                dict(
                    x=0,
                    y=0.95,
                    xref='paper',
                    yref='paper',
                    showarrow=False,
                    align='left',
                    bgcolor='rgba(255, 255, 255, 0.5)',
                    text='Distance: {} miles<br>Standard Flight time : {} hours'.format(round(dist_mi), round(time_hrs)),
                    font=dict(size=12),
                )
            ]
        )
        #fig.show()
        ORGF = OE.loc[OE['Origin'] == input_data['Origin']]
        ORGF=ORGF['Origin_encoded'].iloc[0]
        ORGF=int(ORGF)

        DESTF = OE.loc[OE['Origin'] == input_data['Dest']]
        DESTF=DESTF['Origin_encoded'].iloc[0]
        DESTF=int(DESTF)

        input_date = datetime.strptime(str(input_data['month']) + '-' + str(input_data['dayOfMonth']) + '-' + str(input_data['year']), '%m-%d-%Y')

        if input_data['year'][0]==2016 or input_data['year'][0]==2017:
            start_date = input_date - timedelta(days=5)
            end_date = input_date + timedelta(days=5)
            date_range = pd.date_range(start=start_date, end=end_date)
        else:
            yrand= random.randint(2016,2017)
            input_date = datetime.strptime(str(input_data['month']) + '-' + str(input_data['dayOfMonth']) + '-' + str(yrand), '%m-%d-%Y')

        start_date = input_date - timedelta(days=5)
        end_date = input_date + timedelta(days=5)
        date_range = pd.date_range(start=start_date, end=end_date)

        df_filtered = matchdf.loc[
                     (matchdf['Month'] == int(input_data['month'])) & 
                     (matchdf['DayofMonth'] == int(input_data['dayOfMonth'])) & 
                     (matchdf['OriginE'] == ORGF) & 
                     (matchdf['DestE'] == DESTF)
                     ]

        df_ranges = matchdf.loc[
                            (matchdf['Month'] .isin(date_range.month)) & 
                            (matchdf['DayofMonth'] .isin(date_range.day)) &
                            (matchdf['Year'] .isin(date_range.year)) &
                            (matchdf['OriginE'] == ORGF) & 
                            (matchdf['DestE'] == DESTF)
                            ]

        df_ranges = df_ranges.drop_duplicates(subset='DayofMonth', keep='first')
        topassDFranges = df_ranges[['Quarter', 'Year', 'Month', 'DayofMonth', 'DepTime', 'CRSDepTime', 'CRSAbstime', 'windspeedKmph_y', 'winddirDegree_y', 'weatherCode_y', 'precipMM_y', 'visibility_y', 'pressure_y', 'cloudcover_y', 'DewPointF_y', 'WindGustKmph_y', 'tempF_y', 'WindChillF_y', 'humidity_y', 'time_y', 'OriginE', 'DestE']]
        predictionranges = xgbmodel.predict(topassDFranges)
        result = predictionranges.tolist()

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=date_range, y=result, name='Delay', marker_color=['red' if r > 45 else 'blue' for r in result]))

        fig1.update_layout(title='Delays during the week',
        xaxis_title='Day',
        yaxis_title='Delay (minutes)',
        xaxis=dict(
        tickmode='array',
        tickvals=date_range,
        ticktext=date_range.strftime('%a %d-%m'),
        range=[date_range.min() - pd.Timedelta(days=0.5), date_range.max() + pd.Timedelta(days=0.5)]
        ))

        finaldatapre=df_filtered.head(1)
        topassDF = finaldatapre[['Quarter', 'Year', 'Month', 'DayofMonth', 'DepTime', 'CRSDepTime', 'CRSAbstime', 'windspeedKmph_y', 'winddirDegree_y', 'weatherCode_y', 'precipMM_y', 'visibility_y', 'pressure_y', 'cloudcover_y', 'DewPointF_y', 'WindGustKmph_y', 'tempF_y', 'WindChillF_y', 'humidity_y', 'time_y', 'OriginE', 'DestE']]
        prediction = xgbmodel.predict(topassDF)

        plot_html = fig.to_html(full_html=False)
        rangeplot_html = fig1.to_html(full_html=False)
        

        prediction_str = 'The predicted flight delay is {:.2f} minutes.'.format(prediction[0])
        return render_template('index.html', prediction=prediction_str,plt1=plot_html,ranges=rangeplot_html)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
