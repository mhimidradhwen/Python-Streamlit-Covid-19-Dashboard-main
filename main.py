# -*- coding: utf-8 -*-

import os
from datetime import datetime
from matplotlib import pyplot as plt
from streamlit_globe import streamlit_globe

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from PIL import Image
from requests.exceptions import ConnectionError
import plotly.graph_objects as go
from datetime import date,datetime
from streamlit_echarts import st_echarts
def config():
    file_path = "./components/img/"
    img = Image.open(os.path.join(file_path, 'logo.ico'))
    st.set_page_config(page_title='COVID-DASHBOARD', page_icon=img, layout="wide", initial_sidebar_state="expanded")

    # code to check turn of setting and footer
    st.markdown(""" <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    # encoding format
    encoding = "utf-8"

    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #1c4b27;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    # I want it to show balloon when it finished loading all the configs


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def list_of_countries():
    df = pd.read_csv("./components/csv/countries.csv")
    return df["Name"].tolist()


def covid_data_menu():
    st.subheader('Covid Data Menu')
    col1, col2, col3 = st.columns([4, 4, 4])
    with col1:
        st.text_input(label="Last Updated", value=str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), disabled=True)
    with col2:
        pass
    with col3:
        try:
            url = "https://disease.sh/v3/covid-19/countries"
            response = requests.get(url)
            countries = [i.get("country") for i in response.json()]
            option = st.selectbox('please select country?', (countries), help="Please select country")


        except ConnectionError:
            st.error("There is a connection error we failed to fetch all the countries 😥")
    try:
        response = requests.get("https://disease.sh/v3/covid-19/countries/" + option)
        data = response.json()
        

        # st.write(all_countries_data)
        # df = pd.DataFrame.from_dict(data, orient="index", dtype=str, columns=['Value'])
        
        st.subheader("Country Info")
        country_data = data.pop("countryInfo")
        longitude, latitude = country_data["long"], country_data["lat"]
        country_data.update({"country": data["country"]})
        country_data.pop("lat")
        country_data.pop("long")
        # df = pd.DataFrame.from_dict(country_data, orient="index", dtype=str, columns=['Value'])
        # st.dataframe(df)
        remote_css("")
        st.markdown(f"""
           <table class="table table-borderless">
                <tr>
                  <td>country</td>
                  <td>{country_data["country"]}</td>
                </tr>
                 <tr>
                  <td>Continent</td>
                  <td>{data["continent"]}</td>
                </tr>
                <tr>
                  <td>Population</td>
                  <td>{data["population"]}</td>
                </tr>
                 <tr>
                  <td>flag</td>
                  <td><img src="{country_data["flag"]}" style="width:20%;height:40%"></td>
                </tr>
                
           </table></br>
        """, unsafe_allow_html=True)
        data.pop("country")
        data['updated'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        # st.write(data)
        # st.write(df)
        st.subheader("Covid Stats")
        cases_col, deaths_col, recovered_col,active_col = st.columns(4)
        with cases_col:
            st.metric("Total Cases",data["cases"])
            st.caption("Today Cases")
            st.caption(data["todayCases"])
        with deaths_col:
            st.metric("Total Deaths",data["deaths"])
            st.caption("Today Deaths")
            st.caption(data["todayDeaths"])
        with recovered_col:
                st.metric("Total Recovered",data["recovered"])
                st.caption("Today Recovered")
                st.caption(data["todayRecovered"])
        with active_col:
            st.metric("Total Active",data["active"])
        st.subheader("Map")
      
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=4.7,
                pitch=50,
            )

        )
)


        tests_col,stats_col=st.columns(2)
        with tests_col:
            st.subheader("Tests")
            tests_data = [{"population":data["population"],"tests":data["tests"]}]
            options = {
               "tooltip": {"trigger": "item"},
               "legend": {"top": "5%", "left": "center"},
               "series": [
                   {
                       "name": "Covid Stats",
                       "type": "pie",
                       "radius": ["40%", "70%"],
                       "avoidLabelOverlap": False,
                       "itemStyle": {
                           "borderRadius": 10,
                           "borderColor": "none",
                           "borderWidth": 2,
                       },
                       "label": {"show": False, "position": "center"},
                       "emphasis": {
                           "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                       },
                       "labelLine": {"show": False},
                       "data": [
                           {"value": tests_data[0]["population"], "name": "Population"},
                           {"value": tests_data[0]["tests"], "name": "Tests"},
                       ],
                   }
               ],
            }
            st_echarts(options=options, height="500px",)        
        with stats_col :
            st.subheader('Actives, Deaths,and Recoveries')
            options = {
               "tooltip": {"trigger": "item"},
               "legend": {"top": "5%", "left": "center"},
               "series": [
                   {
                       "name": "Covid Stats",
                       "type": "pie",
                       "radius": ["40%", "70%"],
                       "avoidLabelOverlap": False,
                       "itemStyle": {
                           "borderRadius": 10,
                           "borderColor": "none",
                           "borderWidth": 2,
                       },
                       "label": {"show": False, "position": "center"},
                       "emphasis": {
                           "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                       },
                       "labelLine": {"show": False},
                       "data": [
                           {"value": data["deaths"], "name": "Deaths"},
                           {"value": data["active"], "name": "Active"},
                           {"value": data["recovered"], "name": "Recovered"},
                       ],
                   }
               ],
            }
            st_echarts(options=options, height="500px",)
       
    except ConnectionError as e:
        st.error("There is a connection error please retry later 😥")


def other_tab():
    st.title("World-Wide Covid Stats")
    def normalize_number(number, min_val, max_val):
            return (number - min_val) / (max_val - min_val) * 0.9

    all_countries_response = requests.get("https://disease.sh/v3/covid-19/countries/")
    all_countries_data = all_countries_response.json()
    pointsData =[]
    labelsData =[]
    total_cases = 0
    total_deaths = 0
    total_active = 0
    total_recovered = 0

    country_no = 0
    max_deaths= 0
    min_deaths=100000
    tests_stats=[]
    per_one_million=[]
    testsPerOneMillion = 0 
    activePerOneMillion = 0
    recoveredPerOneMillion = 0
    deathsPerOneMillion = 0

    for elt in all_countries_data:
        total_cases = total_deaths + float(elt["cases"])
        total_deaths = total_deaths + float(elt["deaths"])
        total_active = total_deaths + float(elt["active"])
        total_recovered = total_deaths + float(elt["recovered"])
        testsPerOneMillion = testsPerOneMillion +float(elt["testsPerOneMillion"]) 
        activePerOneMillion = activePerOneMillion +float(elt["activePerOneMillion"])
        recoveredPerOneMillion = recoveredPerOneMillion+float(elt["recoveredPerOneMillion"])
        deathsPerOneMillion = deathsPerOneMillion+float(elt["deathsPerOneMillion"])

        country_no = country_no +1
        if float(elt["deaths"]) > max_deaths:
            max_deaths = float(elt["deaths"])
            max_deaths_country = elt["countryInfo"]
            max_deaths_country_name = elt["country"]
            element =elt
            
        if float(elt["deaths"]) < min_deaths:
            min_deaths = float(elt["deaths"])
            min_deaths_country = elt["countryInfo"]
            min_deaths_country_name = elt["country"]

    total_data = {"cases":total_cases,"active":total_active,"deaths":total_deaths,"recovered":total_recovered}
    per_one_million.append({"active":activePerOneMillion/country_no,"deaths":deathsPerOneMillion/country_no,"recovered":recoveredPerOneMillion/country_no,"test":testsPerOneMillion/country_no})
    for elt in all_countries_data:
        lat=elt["countryInfo"]["lat"]
        longi=elt["countryInfo"]["long"]
        deaths=elt["deaths"]
        color = "green"
        tests_stats.append({"country":elt["country"],"tests":elt["tests"]})
        if  normalize_number(deaths,min_deaths,max_deaths) > normalize_number((total_deaths/country_no),min_deaths,max_deaths):
            color = "red"
            
        pointsData.append({'lat': lat, 'lng': longi, 'size': normalize_number(deaths,min_deaths,max_deaths), 'color': color})
        labelsData.append({'lat': lat, 'lng': longi, 'size': normalize_number(deaths,min_deaths,max_deaths) , 'color': color, 'text': deaths})
    st.subheader("Tests Stats")
    cases_col, deaths_col, recovered_col,active_col = st.columns(4)
    with cases_col:
        st.metric("Total Cases",int(total_cases))
    with deaths_col:
        st.metric("Total Deaths",int(total_deaths))
    with recovered_col:
            st.metric("Total Recovered",int(total_recovered))
    with active_col:
        st.metric("Total Active",int(total_active))
    st.subheader("Map")
    streamlit_globe(pointsData=pointsData, labelsData=labelsData, daytime='day', width=800, height=600)
    
    col1,col2 =st.columns([6,6])
    with col1:
        st.subheader("Minumum Deaths")
        st.markdown(f"""
               <table class="table table-borderless">
                    <tr>
                      <td>country</td>
                      <td>{min_deaths_country_name}</td>
                    </tr>
                     <tr>
                      <td>flag</td>
                      <td><img src="{min_deaths_country["flag"]}" style="width:20%;height:40%"></td>
                    </tr>
<tr>
                      <td>Deaths</td>
                      <td>{min_deaths}</td>
                    </tr>
               </table></br>
            """, unsafe_allow_html=True)
    with col2:
        st.subheader("Maximum Deaths")
        st.markdown(f"""
               <table class="table table-borderless">
                    <tr>
                      <td>country</td>
                      <td>{max_deaths_country_name}</td>
                    </tr>
                     <tr>
                      <td>flag</td>
                      <td><img src="{max_deaths_country["flag"]}" style="width:20%;height:40%"></td>
                    </tr>
                    <tr>
                      <td>Deaths</td>
                      <td>{max_deaths}</td>
                    </tr>
               </table></br>
            """, unsafe_allow_html=True)
    # df = pd.DataFrame(total_data, index=['Total'])
    # fig1, ax1 = plt.subplots()
    # ax1.pie([df['active'][0], df['deaths'][0], df['recovered'][0]], labels=['Active', 'Deaths', 'Recovered'], autopct='%1.1f%%')
    # ax1.axis('equal')
    # st.pyplot(fig1)
    pie_col ,bar_col=st.columns(2)
    with pie_col :
        st.subheader('Actives, Deaths,and Recoveries')
        options = {
           "tooltip": {"trigger": "item"},
           "legend": {"top": "5%", "left": "center"},
           "series": [
               {
                   "name": "Covid Stats",
                   "type": "pie",
                   "radius": ["40%", "70%"],
                   "avoidLabelOverlap": False,
                   "itemStyle": {
                       "borderRadius": 10,
                       "borderColor": "none",
                       "borderWidth": 2,
                   },
                   "label": {"show": False, "position": "center"},
                   "emphasis": {
                       "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                   },
                   "labelLine": {"show": False},
                   "data": [
                       {"value": total_data["deaths"], "name": "Deaths"},
                       {"value": total_data["active"], "name": "Active"},
                       {"value": total_data["recovered"], "name": "Recovered"},
                   ],
               }
           ],
        }
        st_echarts(options=options, height="500px",)
    with bar_col :
        st.subheader('Per 1 Million')
        options = {
           "tooltip": {"trigger": "item"},
           "legend": {"top": "5%", "left": "center"},
           "series": [
               {
                   "name": "Covid Stats",
                   "type": "pie",
                   "radius": ["40%", "70%"],
                   "avoidLabelOverlap": False,
                   "itemStyle": {
                       "borderRadius": 10,
                       "borderColor": "none",
                       "borderWidth": 2,
                   },
                   "label": {"show": False, "position": "center"},
                   "emphasis": {
                       "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                   },
                   "labelLine": {"show": False},
                   "data": [
                       {"value": per_one_million[0]["deaths"], "name": "Deaths"},
                       {"value": per_one_million[0]["active"], "name": "Active"},
                       {"value": per_one_million[0]["recovered"], "name": "Recovered"},
                       {"value": per_one_million[0]["test"], "name": "Test"},
                   ],
               }
           ],
        }
        st_echarts(options=options, height="500px",)
        
    st.subheader("Tests")
    df = pd.DataFrame(tests_stats)
    st.bar_chart(df.set_index('country'))
        
def main():
    config()
    st.sidebar.subheader("COVID-19 DASHBOARD")
    menu = ["COVID-19 Country","World Stats"]
    choice = st.sidebar.selectbox("", menu)
    covid_data_menu() if (choice == "COVID-19 Country") else other_tab()


if __name__ == '__main__':
    main()
