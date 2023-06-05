import streamlit as st
from tensorflow import keras
from keras.models import load_model
import joblib
import numpy as np
import pandas as pd
import csv
from PIL import Image
import altair as alt

st.set_page_config(page_title='Well Test ML Model', layout='wide')

tabs_font_css = """
<style type="text/css">
h2 {text-align: center;
font-weight:700;
color:#162D32}

h3 {text-align: center;
font-weight:700;
font-size: calc(0.5rem + .6vw);
color:#162D32}

p {color:#3B7C89;
font-weight:700;}

.css-184tjsw p {
font-size:16px;
}

div[class*="stButton"] p {
  color: black;
}

div[class*="stAlert"] p {
  color: #414141;
  font-weight:500;
}
<style>
"""
st.write(tabs_font_css, unsafe_allow_html=True)

col1,col2,col3 = st.columns([1.3,0.3,2],gap='small')
with col1:
  image = Image.open('ML.jpg')
  st.subheader("“If you invent a breakthrough in artificial intelligence, so machines can learn, that is worth 10 Microsofts.” -Bill Gates")
  st.image(image)
  st.write('####')
  prediction_method = st.selectbox('Prediction Machine Learning Method', ['Neural Network', 'Extra Trees'])
  actual_fluid_rate = st.number_input('Actual Fluid Rate (if available)')
  test_method = st.selectbox('Testing Method', ['Separator', 'PTS', 'MPFM', 'Clamp on meter', 'Other'])
  remarks = st.text_area("Remarks")

with col3:
  st.header('Well Test Machine Learning Model')
  date = st.date_input('Date')
  field = st.text_input('Field')
  well = st.text_input('Well')
  WHP = st.number_input('Wellhead Pressure, psi')
  WHT= st.number_input('Wellhead Temperature, °F')
  Pr = st.number_input('Reservoir Pressure, psi')
  Tr = st.number_input('Reservoir Temperature, °F')
  Wg = st.number_input('Water Gravity')
  WC = st.number_input('Watercut %')
  IG = st.number_input('Injection Gas, MMSCFD')
  DS = st.number_input('Downstream Pressure, psi')
  Tubing_type = st.selectbox('Tubing Type', ['Normal 4.5 short*3.5', 'Normal 4.5 long*3.5', 'Big bore 5.5 short*(4.5*3.5 joints)',
                                        'Big bore 5.5 long*4.5*3.5', 'Big bore 5.5 long*4.5', 'Big bore (5.5*4.5 joints)*(4.5*3.5 joints)',
                                        'Slim 4.5 long*3.5*2.875', 'Slim (4.5*3.5 joints)*2.875'])
  Well_type = st.selectbox('Well Type', ['GL', 'NF'])
  actual_oil_rate = actual_fluid_rate * (1-(WC/100))

  df = pd.DataFrame(np.array([[WHP, WHT, Tr, Wg, Pr, Tubing_type, WC, IG, DS, Well_type]]), 
                    columns=['WHP', 'WHT', 'Tr', 'Ɣw', 'Pr', 'Tubing_type', 'WC', 'I.GAS', 'D/S', 'Well_type'])

  ct_st = joblib.load('column_transformer_st.joblib')
  pipe = joblib.load('pipeline_ex.joblib')
  model = load_model('ANN_model.h5')
      
  numerical = [WHP, WHT, Tr, Wg, Pr]
  if st.button('Predict'):
      if not(all(numerical)):
          st.error('Missing data')
      elif Tr < WHT or Pr < WHP or (Well_type == 'NF' and IG != 0) or (Well_type == 'NF' and DS != 1):
          st.error('Check the data again')
      else:
          if prediction_method == 'Neural Network':
              predcited_fluid_rate = int(model.predict(ct_st.transform(df)))

          elif prediction_method == 'Extra Trees':
              predcited_fluid_rate = int(pipe.predict(df))
          predcited_oil_rate = int(predcited_fluid_rate * (1-(WC/100)))
          
          st.success('Model run successfully')
          st.subheader('Fluid Rate = ' + str(predcited_fluid_rate)+' BFPD')
          st.subheader(':green[Oil Rate = ' + str(predcited_oil_rate)+' BOPD]')

          df_chart1 = pd.DataFrame({'Predicted Rate':['Fluid Rate', 'Oil Rate'], 'BPD':[predcited_fluid_rate, predcited_oil_rate]})
          c1 = alt.Chart(df_chart1).mark_bar().encode(x='Predicted Rate', y=alt.Y('BPD', scale=alt.Scale(domain=[0, round(max(predcited_fluid_rate, actual_fluid_rate)+500,-3)])),
              color=alt.Color('Predicted Rate', scale=alt.Scale(domain=['Fluid Rate', 'Oil Rate'], range=['black', 'green']))).properties(width=alt.Step(70))

          df_chart2 = pd.DataFrame({'Actual Rate':['Fluid Rate', 'Oil Rate'], 'BPD':[actual_fluid_rate, actual_oil_rate]})
          c2 = alt.Chart(df_chart2).mark_bar().encode(x='Actual Rate', y=alt.Y('BPD', scale=alt.Scale(domain=[0, round(max(predcited_fluid_rate, actual_fluid_rate)+500,-3)])),
              color=alt.Color('Actual Rate', scale=alt.Scale(domain=['Fluid Rate', 'Oil Rate'], range=['black', 'green']))).properties(width=alt.Step(70))

          col4, col5 = st.columns(2)
          col4.altair_chart(c1)
          if actual_fluid_rate > 0:
              col5.altair_chart(c2)

          fields = [date, field, well, WHP, WHT, Pr, Tr, WC, IG, DS, Wg, Tubing_type, 
              Well_type, actual_fluid_rate, test_method, predcited_fluid_rate, prediction_method, remarks]
          with open('Well Tests Database.csv','a', newline='', encoding='utf8', errors = 'ignore') as f:
              writer = csv.writer(f)
              writer.writerow(fields) 
