
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from math import ceil
from datetime import date
from streamlit_dynamic_filters import DynamicFilters
import urllib.request
from PIL import Image
import time





def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

download_image('https://belyse.gr/image/cache/catalog/assets/logos/logo-708x278.png','belyse.png')
lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
def metrics_customize(red,green,blue,iconname,sline,i):
    htmlstr = f"""<p style='background-color: rgb({red},{green},{blue}, 0.75); 
                        color: rgb(0,0,0, 0.75); 
                        font-size: 25px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 22px; 
                        margin-top: 0;'>{sline}</style></span></p>"""
    return htmlstr

st.set_page_config(layout='wide',page_title="Belyse Lights")
belysefo= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Belyse/main/Belysefo.csv")

belysefo['Acceptance_Date'] = pd.to_datetime(belysefo['Acceptance_Date'])

belysefo['Month']=belysefo['Acceptance_Date'].dt.month_name()
belysefo['Year']=belysefo['Acceptance_Date'].dt.year

belysefo['Month_Year']=belysefo['Acceptance_Date'].dt.strftime('%m-%Y')
belysefo['Month_Year']=pd.to_datetime(belysefo['Month_Year'],format='mixed')
month_levels = pd.Series([
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
])
belysefo['Month']=pd.Categorical(belysefo['Month'],categories=month_levels)
belysefo['Profit']=belysefo['Total Price']-belysefo['Supplier buy']
belysefo['Date_order']=belysefo['Acceptance_Date'].dt.date
dynamic_filters = DynamicFilters(belysefo, filters=['Month','Year'])
belysefo_filter = dynamic_filters.filter_df()

image,filters=st.columns(2)
with image:
    st.image(Image.open("belyse.png"), width=400)
with filters:
    dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')


kpi1,kpi2,kpi3,kpi4= st.columns(4)
with kpi1:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-shopping-cart","Ολοκληρωμένες Παραγγελίες",belysefo_filter['id_order'].nunique()), unsafe_allow_html=True)
with kpi2:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-euro-sign","Έσοδα πωλήσεων",belysefo_filter['Total Price'].sum().round(2)), unsafe_allow_html=True)
with kpi3:
    st.markdown(lnk + metrics_customize(0,204,102, "fas fa-euro-sign", "Κέρδη πωλήσεων",
                                        (belysefo_filter['Total Price'].sum() - belysefo_filter['Supplier buy'].sum()).round(2)),
                unsafe_allow_html=True)
with kpi4:
    st.markdown(lnk + metrics_customize(0,204,102, "fas fa-percent", "Ποσοστό προμήθειας αγορών",
                                        (100*(1 - (belysefo_filter['Supplier buy'].sum()/belysefo_filter['Total Price'].sum()).round(3))).round(4)),
                unsafe_allow_html=True)



st.write('##### Εξέλιξη παραγωγής')
tab1,tab2,tab3=st.tabs(['Συνολικές παραγγελίες','Έσοδα πωλήσεων','Κέρδη πωλήσεων'])

with tab1:
    fig_line_comp_orders_mbm = px.line(
        belysefo_filter['Date_order'].value_counts().reset_index(),
        x="Date_order", y="count",
        title='',
        labels={'Date_order': 'Ημ. παραγγελίας', "count": 'Ολοκληρωμένες παραγγελίες'},
        width=300,markers=True)
    fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
    st.write(fig_line_comp_orders_mbm)

with tab2:
    fig_line_comp_orders_mbm = px.line(
        belysefo_filter.groupby(['Date_order'])['Total Price'].sum().reset_index(),
        x="Date_order", y="Total Price",
        title='',
        labels={'Date_order': 'Ημ. παραγγελίας', "Total Price": 'Έσοδα πωλήσεων'},
        width=400,markers=True)
    fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
    st.write(fig_line_comp_orders_mbm)


with tab3:
    fig_line_comp_orders_mbm = px.line(
        belysefo_filter.groupby(['Date_order'])['Profit'].sum().reset_index(),
        x="Date_order", y="Profit",
        title='',
        labels={'Date_order': 'Ημ. παραγγελίας', "Profit": 'Κέρδη πωλήσεων'},
        width=1000,markers=True)
    fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
    st.write(fig_line_comp_orders_mbm)

    st.write('##### Πωλήσεις ανά μήνα')

month, year = st.columns(2)
with month:
    tab4,tab5,tab6=st.tabs(['Συνολικές παραγγελίες','Έσοδα πωλήσεων','Κέρδη πωλήσεων'])
    with tab4:
        fig_line_comp_orders_mbm = px.bar(
            belysefo_filter['Month_Year'].value_counts().reset_index(),
            x="Month_Year", y="count",
            title='',
            labels={'Month_Year': 'Μήνας-Έτος', "count": 'Ολοκληρωμένες παραγγελίες'},
            width=300,text_auto=True)
        fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
        fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
        st.write(fig_line_comp_orders_mbm)

    with tab5:
        fig_line_comp_orders_mbm = px.bar(
            belysefo_filter.groupby(['Month_Year'])['Total Price'].sum().reset_index(),
            x="Month_Year", y="Total Price",
            title='',
            labels={'Month_Year': 'Μήνας-Έτος', "Total Price": 'Έσοδα πωλήσεων'},
            width=300,text_auto=True)
        fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
        fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
        st.write(fig_line_comp_orders_mbm)


    with tab6:
        fig_line_comp_orders_mbm = px.bar(belysefo_filter.groupby(['Month_Year'])['Profit'].sum().reset_index(),
            x="Month_Year", y="Profit",
            title='',
            labels={'Month_Year': 'Μήνας-Έτος', "Profit": 'Κέρδη πωλήσεων'},
            width=300,text_auto=True)
        fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
        fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
        st.write(fig_line_comp_orders_mbm)

with year:
    st.write("##### Πωλήσεις ανά ετός")
    tab7, tab8, tab9 = st.tabs(['Συνολικές παραγγελίες', 'Έσοδα πωλήσεων', 'Κέρδη πωλήσεων'])
    with tab7:
        fig_line_comp_orders_mbm = px.bar(
            belysefo_filter['Year'].value_counts().reset_index(),
            x="Year", y="count",
            title='',
            labels={'Year': 'Έτος', "count": 'Ολοκληρωμένες παραγγελίες'},
            width=400, text_auto=True)
        fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
        fig_line_comp_orders_mbm.update_xaxes(type='category')
        fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13,bargap=0.5,bargroupgap=0.01)
        st.write(fig_line_comp_orders_mbm)

    with tab8:
        fig_line_comp_orders_mbm = px.bar(
            belysefo_filter.groupby(['Year'])['Total Price'].sum().reset_index(),
            x="Year", y="Total Price",
            title='',
            labels={'Year': 'Έτος', "Total Price": 'Έσοδα πωλήσεων'},
            width=400, text_auto=True)
        fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
        fig_line_comp_orders_mbm.update_xaxes(type='category')
        fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
        st.write(fig_line_comp_orders_mbm)

    with tab9:
        fig_line_comp_orders_mbm = px.bar(
            belysefo_filter.groupby(['Year'])['Profit'].sum().reset_index().sor,
            x="Year", y="Profit",
            title='',
            labels={'Year': 'Έτος', "Profit": 'Κέρδη πωλήσεων'},
            width=400, text_auto=True)
        fig_line_comp_orders_mbm.update_xaxes(type='category')
        fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
        fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=13)
        st.write(fig_line_comp_orders_mbm)
