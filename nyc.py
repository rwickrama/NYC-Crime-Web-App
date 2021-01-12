import streamlit as st 
import pandas as pd
import pydeck as pdk
import numpy as np
import plotly.express as px


st.title("Crime Statistics in New York City")

@st.cache(persist=True)
def load_data(nrows):
    data=pd.read_excel('NYPD_Complaint_Data_Historic.xls',nrows=nrows,parse_dates=[['CMPLNT_FR_DT','CMPLNT_FR_TM']],encoding="ISO-8859-1")
    data.dropna(subset=['Latitude','Longitude'],inplace=True)
    lowercase=lambda x: str(x).lower()
    data.rename(lowercase,axis="columns",inplace=True)
    data.rename(columns={"cmplnt_fr_dt_cmplnt_fr_tm":"date/time"},inplace=True)
    return data
    
data=load_data(27100)



st.header("How many crimes occur during a given time of day?")
hour=st.slider("Hour to look at",0,23)
original_data=data
data=data[data["date/time"].dt.hour==hour]
data_in=data[data['loc_of_occur_desc']=='INSIDE']
data_out=data[data['loc_of_occur_desc']!='INSIDE']
data_street=data[data['prem_typ_desc']=='STREET']
data_house=data[data['prem_typ_desc']=='RESIDENCE-HOUSE']

midpoint=(np.average(data['latitude']),np.average(data['longitude']))
st.markdown("All Crimes")
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['date/time','latitude','longitude']],
        get_position=["longitude","latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))

st.markdown("Crimes that occur indoors")
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data_in[['date/time','latitude','longitude']],
        get_position=["longitude","latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))

st.markdown("Crimes that occur outdoors")
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data_out[['date/time','latitude','longitude']],
        get_position=["longitude","latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))

st.markdown("Crimes that occur on streets")
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data_street[['date/time','latitude','longitude']],
        get_position=["longitude","latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))


st.markdown("Crimes that occur in resident houses")
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data_house[['date/time','latitude','longitude']],
        get_position=["longitude","latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))      

st.header("Breakdown of crimes by minute during a specific hour")
hour1=st.slider("Pick a time:",0,23)

filtered=original_data[(original_data['date/time'].dt.hour>=hour1)&(original_data['date/time'].dt.hour<(hour1+1))]
hist=np.histogram(filtered['date/time'].dt.minute,bins=60,range=(0,60))[0]
chart_data=pd.DataFrame({"minutes":range(60),"crimes":hist})

filtered

fig=px.bar(chart_data,x='minutes',y='crimes',height=400)
st.write(fig)