
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
belyse= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Belyse/main/Belyse.csv")
belyse['entry_date'] = pd.to_datetime(belyse['entry_date'],dayfirst=True)
belyse['Date_order']=belyse["entry_date"].dt.date
belyse['Month_order']=belyse["entry_date"].dt.month_name()
belyse['Year_order']=belyse["entry_date"].dt.year
belyse['Month_Year']=belyse["entry_date"].dt.strftime('%m-%Y')
month_levels = pd.Series([
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
])


belyse['Availability']=belyse['Availability'].replace("’μεσα διαθέσιμο","Άμεσα διαθέσιμο")
belyse['acceptance_date']=belyse['acceptance_date'].replace("0","01/01/1900 00:00")
belyse['Availability']=pd.Categorical(belyse['Availability'],categories=pd.Series(['Άμεσα διαθέσιμο','Διαθέσιμο από 1 έως 3 ημέρες','Διαθέσιμο από 4 έως 10 ημέρες','Διαθέσιμο από 10 έως 30 ημέρες']))
belyse['Month_Year']=pd.to_datetime(belyse['Month_Year'],format='mixed')
belyse['Month_order']=pd.Categorical(belyse['Month_order'],categories=month_levels)
belyse['Product']=belyse['Product'].replace('� ','')
belyse['MPN']="C-"+ belyse['MPN']
belyse['Total_Price']=belyse['Price']*belyse['Quantity']
belyse['Supplier']=pd.Categorical(belyse['Supplier'],categories=pd.Series(['ARKOLIGHT', 'GLOBOSTAR', 'HERONIA LIGHTING', 'SOLOMON GROUP']))
belyse['acceptance_date'] = pd.to_datetime(belyse['acceptance_date'],dayfirst=True)
belyse['acceptance_days']=((belyse['acceptance_date'].dt.year-belyse['entry_date'].dt.year)*365 +(belyse['acceptance_date'].dt.month-belyse['entry_date'].dt.month)*30+belyse['acceptance_date'].dt.day-belyse['entry_date'].dt.day).round(0)
belyse['delivery_date'] = pd.to_datetime(belyse['delivery_date'],dayfirst=True)
belyse['delivery_days']=((belyse['delivery_date'].dt.year-belyse['entry_date'].dt.year)*365 +(belyse['delivery_date'].dt.month-belyse['entry_date'].dt.month)*30+belyse['delivery_date'].dt.day-belyse['entry_date'].dt.day).round(0)
belyse_complete_orders=belyse.loc[(belyse['order_situation']=="Ολοκληρώθηκε")|((belyse['order_situation']=="Μέρος της έχει επιστραφεί")& (belyse['Return']==0))]
Quantity_products=pd.merge(belyse_complete_orders[['MPN','Product']].value_counts().reset_index(),belyse_complete_orders.groupby(['MPN','Product'])['Quantity'].sum().reset_index())
Quantity_products['Total_quantity']=Quantity_products['Quantity']*Quantity_products['count']


st.image(Image.open("belyse.png"),width=400)


kpi1,kpi2,kpi3,kpi4= st.columns(4)
with kpi1:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-shopping-cart","Ολοκληρωμένες Παραγγελίες",belyse_complete_orders['id_order'].nunique()), unsafe_allow_html=True)
with kpi1:
    st.markdown(lnk + metrics_customize(0,204,102,"far fa-lightbulb","Συνολικά προϊόντα που πουλήθηκαν",belyse_complete_orders['id'].nunique()), unsafe_allow_html=True)
with kpi1:
    st.markdown(lnk + metrics_customize(0,204,102, "far fa-lightbulb", "Κωδικοί προϊόντων που πουλήθηκαν",
                                        belyse_complete_orders['MPN'].nunique()),
                unsafe_allow_html=True)
with kpi2:
    st.markdown(lnk + metrics_customize(233,58,28,"fas fa-ban","Aκυρωμένες Παραγγελίες",belyse[belyse['order_situation']=="Ακυρωμένη"]['id_order'].nunique()), unsafe_allow_html=True)
with kpi2:
    st.markdown(lnk + metrics_customize(255,192,0,"fas fa-times","Παραγγελίες που απορρίφθηκαν",belyse[belyse['order_situation']=="Απορρίφθηκε"]['id_order'].nunique()), unsafe_allow_html=True)
with kpi2:
    st.markdown(lnk + metrics_customize(21,179,235,"fas fa-backward","Επιστροφές Προϊόντών",belyse['Return'].sum()), unsafe_allow_html=True)

with kpi3:
    st.markdown(lnk + metrics_customize(20, 102, 120, "fas fa-user", "Προμηθευτές",
                                        belyse_complete_orders['Supplier'].nunique()),
                unsafe_allow_html=True)
with kpi3:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-euro-sign","Έσοδα απο πωλήσεις",belyse_complete_orders['Total_Price'].sum().round(2)), unsafe_allow_html=True)
with kpi3:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-euro-sign","Προμήθεια Skroutz",belyse_complete_orders.groupby('id_order')['Skroutz_Commission'].mean().reset_index()['Skroutz_Commission'].sum().round(2)), unsafe_allow_html=True)
with kpi4:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-shopping-bag","Αρ. προϊόντων ανά παραγγελία",belyse_complete_orders['id_order'].value_counts().reset_index()['count'].mean().round(1)), unsafe_allow_html=True)
with kpi4:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-hourglass","Μέσο διάστημα αποδοχής παραγγελίας",belyse_complete_orders.loc[belyse['acceptance_date']!="1900-01-01 00:00:00"]['acceptance_days'].mean().round(1).astype('str')+" ημέρες"), unsafe_allow_html=True)
with kpi4:
    st.markdown(lnk + metrics_customize(0,204,102,"fas fa-truck","Μέσο διάστημα αποστολή παραγγελίας",belyse_complete_orders['delivery_days'].mean().round(1).astype('str')+" ημέρες"), unsafe_allow_html=True)


st.write('#### Top5 προϊόντα')
top41, top42,top43 = st.tabs(["Σε πωλήσεις","Σε ζήτηση ποσότητας","Σε έσοδα απο τις πωλησεις"])
with top41:
    fig_line_comp_orders_mbm = px.bar(
        belyse_complete_orders[['Product','MPN']].value_counts().head(5).reset_index().sort_values('count'),
        x="count", y="MPN",
        title='Top 5 προϊόντα σε πωλήσεις',hover_data=['Product','MPN'],
        labels={'MPN': 'Κωδ. Προϊόντος', "count": 'Συνολικές πωλήσεις'},
        text='count', width=1200, height=400)
    fig_line_comp_orders_mbm.update_traces(textfont_size=16, textangle=0, marker_color='#146678', cliponaxis=False,
                                           textposition='outside')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=8)
    st.write(fig_line_comp_orders_mbm)
with top42:
    fig_line_comp_orders_mbm = px.bar(
        Quantity_products.sort_values('Quantity', ascending=False).head(5).sort_values('Quantity'),
        x="Quantity", y="MPN",
        title='Top 5 προϊόντα σε ποσότητες προϊόντων',hover_data=['Product','MPN'],
        labels={'MPN': 'Κωδ. Προϊόντος', "Quantity": 'Ποσότητα'},
        text='Quantity', width=1200, height=400)
    fig_line_comp_orders_mbm.update_traces(textfont_size=16, textangle=0, marker_color='#146678', cliponaxis=False,
                                           textposition='outside')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=8)
    st.write(fig_line_comp_orders_mbm)
with top43:
    fig_line_comp_orders_mbm = px.bar(
        belyse_complete_orders.groupby(['Product','MPN'])['Total_Price'].sum().reset_index().sort_values('Total_Price',ascending=False).head(5).sort_values('Total_Price').round(2),
        x="Total_Price", y="MPN",
        title='',hover_data=['Product','MPN'],
        labels={'MPN': 'Κωδ. Προϊόντος', "Total_Price": 'Έσοδα'},
        text='Total_Price', width=1200, height=400)
    fig_line_comp_orders_mbm.update_traces(textfont_size=16, textangle=0, marker_color='#146678', cliponaxis=False,
                                           textposition='outside')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=8)
    st.write(fig_line_comp_orders_mbm)



st.write("#### Ολοκληρωμένες παραγγελίες")

tab1, tab2 = st.tabs(['Συνολικές παραγγελίες', "Έσοδα"])
with tab1:
        tab11,tab12,tab13=st.tabs(['Ανά ημέρα',"Ανά μήνα",'Σύγκριση ανά έτος'])
        with tab11:
                fig_line_comp_orders_dbd = px.line(belyse[belyse['order_situation']=="Ολοκληρώθηκε"][['Date_order','id_order']].value_counts().reset_index().groupby('Date_order')['count'].count().reset_index().sort_values('Date_order'),
                                        x="Date_order", y="count",
                                        title='',
                                labels={'Date_order':'Ημερομηνία',"count":'Ολοκληρωμένες παραγγελίες'},
                                markers=True,width=1800)
                fig_line_comp_orders_dbd.update_traces(marker_color='#146678',line_color="#F0BF4C")
                fig_line_comp_orders_dbd.update_layout(plot_bgcolor='white',font_size=13)
                st.write(fig_line_comp_orders_dbd)
        with tab12:
                fig_line_comp_orders_mbm = px.bar(belyse[belyse['order_situation']=="Ολοκληρώθηκε"][['Month_Year','id_order']].value_counts().reset_index().groupby('Month_Year')['count'].count().reset_index().sort_values('Month_Year'),
                                        x="Month_Year", y="count",
                                        title='',
                                labels={'Month_Year':'Μήνας-Έτος',"count":'Ολοκληρωμένες παραγγελίες'},
                                text_auto=True,width=1000)
                fig_line_comp_orders_mbm.update_traces(marker_color='#146678')
                fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white',font_size=13)
                st.write(fig_line_comp_orders_mbm)
        with tab13:
            fig_line_comp_orders_yby = px.line(
                belyse_complete_orders[['Month_order', 'Year_order']].value_counts().reset_index().sort_values('Month_order'),
                x="Month_order", y="count",
                title='', color='Year_order',
                labels={'Month_order': 'Ημερομηνία', "count": 'Ολοκληρωμένες παραγγελίες','Year_order':'Έτος'},
                markers=True, width=1800)
            fig_line_comp_orders_yby.update_layout(plot_bgcolor='white', font_size=13)
            st.write(fig_line_comp_orders_yby)

with tab2:
    tab21, tab22, tab23 = st.tabs(['Ανά ημέρα', "Ανά μήνα", 'Σύγκριση ανά έτος'])
    with tab21:
        fig_line_comp_orders_dbd = px.line(
            belyse_complete_orders.groupby(['Date_order', 'id_order'])['Total_Price'].mean().reset_index().groupby(
                'Date_order')['Total_Price'].sum().reset_index().sort_values('Date_order'),
            x="Date_order", y="Total_Price",
            title='',
            labels={'Date_order': 'Ημερομηνία', "Price": 'Έσοδα από πωλήσεις'},
            markers=True, width=1800)
        fig_line_comp_orders_dbd.update_traces(marker_color='#146678', line_color="#F0BF4C")
        fig_line_comp_orders_dbd.update_layout(plot_bgcolor='white', font_size=13)
        st.write(fig_line_comp_orders_dbd)
    with tab22:
        fig_line_comp_orders_mbm = px.bar(
            belyse_complete_orders.groupby(['Month_Year', 'id_order'])['Total_Price'].mean().reset_index().groupby(
                'Month_Year')['Total_Price'].sum().reset_index().sort_values('Month_Year'),
            x="Month_Year", y="Total_Price",
            title='',
            labels={'Month_Year': 'Μήνας-Έτος', "Total_Price": 'Έσοδα από πωλήσεις'},
            text='Total_Price', width=1000)
        fig_line_comp_orders_mbm.update_traces(textfont_size=13, texttemplate='%{text:.3s} €', textangle=0,
                                               cliponaxis=False,marker_color='#146678')
        fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=12)
        st.write(fig_line_comp_orders_mbm)
    with tab23:
        fig_line_comp_orders_yby = px.line(belyse_complete_orders.groupby(['Month_order', 'Year_order'])['Total_Price'].sum().reset_index().sort_values(
                'Month_order'),
            x="Month_order", y="Total_Price",
            title='', color='Year_order',
            labels={'Month_order': 'Ημερομηνία', "Price": 'Έσοδα από πωλήσεις','Year_order':'Έτος'},
            markers=True, width=1800)
        fig_line_comp_orders_yby.update_layout(plot_bgcolor='white', font_size=13)
        st.write(fig_line_comp_orders_yby)

pie1,pie2,pie3= st.columns(3)

with pie1:
    pie1=px.pie(belyse_complete_orders[['id_order','Invoice']].value_counts().reset_index().groupby('Invoice').count().reset_index(),
        values='count',names='Invoice', color='Invoice',
        color_discrete_sequence= px.colors.sequential.Aggrnyl,labels={'count':'Σύνολο','Invoice':'Τύπος παραστατικού'},
        height=450,
        title='Τύπος παραστατικού',hole=0.5,width=2000)
    pie1.update_traces(hoverinfo="value",textfont_size=17)
    pie1.update_layout(plot_bgcolor='white',font_size=20,
                       legend=dict(yanchor="top",y=0.55,xanchor="right",x=0.1),legend_title_text='',title_x=0,title_y=0.55)
    st.write(pie1)

with pie2:
    pie2=px.pie(belyse_complete_orders[['id_order','Courier']].value_counts().reset_index().groupby('Courier').count().reset_index(),
        values='count',names='Courier', color='Courier',
        color_discrete_sequence= px.colors.sequential.Aggrnyl,labels={'count':'Σύνολο'},
        height=450,
        title='Courier',hole=0.5,width=2000)
    pie2.update_traces(hoverinfo="value",textfont_size=17)
    pie2.update_layout(plot_bgcolor='white',font_size=20,legend=dict(yanchor="top",y=0.65,xanchor="right",x=0.1),title_y=0.6,title_x=0)
    st.write(pie2)

with pie3:
    availability=belyse_complete_orders[['Availability',"id_order"]].value_counts().reset_index().groupby('Availability')['count'].sum().reset_index().sort_values('Availability')
    pie3=px.pie(availability,
        values='count',names=availability['Availability'],category_orders={'Availability':['Άμεσα διαθέσιμο','Διαθέσιμο από 1 έως 3 ημέρες','Διαθέσιμο από 4 έως 10 ημέρες','Διαθέσιμο από 10 έως 30 ημέρες']},
        color_discrete_sequence= px.colors.sequential.Aggrnyl,labels={'count':'Σύνολο','Availability':'Διαθεσιμότητα'},
        height=450,
        title='Διαθεσιμότητα',hole=0.5,width=2000)
    pie3.update_traces(hoverinfo="value",textfont_size=17)
    pie3.update_layout(plot_bgcolor='white',font_size=20,legend=dict(yanchor="top",y=0.65,xanchor="right",x=0.1),title_y=0.6,title_x=0.1)
    st.write(pie3)

st.write("#### Προμηθευτές")

col1,col2,col3=st.columns(3)
with col1:
    fig_line_comp_orders_mbm = px.bar(
        belyse_complete_orders[['Supplier']].value_counts().reset_index().groupby('Supplier')['count'].sum().reset_index().sort_values('count'),
        x="Supplier", y="count",
        title='Συνολικές παραγγελίες',
        labels={'Supplier': 'Προμηθευτής', "count": 'Αρ. παρραγγελίων'},
        text='count', width=1000)
    fig_line_comp_orders_mbm.update_traces(textfont_size=13,  textangle=0,
                                           cliponaxis=False,marker_color='#146678')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=12)
    st.write(fig_line_comp_orders_mbm)
with col2:
    fig_line_comp_orders_mbm = px.bar(
        belyse_complete_orders.groupby('Supplier')['Total_Price'].sum().reset_index().sort_values('Total_Price'),
        x="Supplier", y="Total_Price",
        title='Συνολική παραγωγή σε πωλήσεις',
        labels={'Supplier': 'Προμηθευτής', "Total_Price": 'Πωλήσεις €'},
        text='Total_Price', width=1000)
    fig_line_comp_orders_mbm.update_traces(textfont_size=13, texttemplate='%{text:.2s} €', textangle=0,
                                           cliponaxis=False,marker_color='#146678')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=12)
    st.write(fig_line_comp_orders_mbm)

with col3:
    fig_line_comp_orders_mbm = px.bar(
        belyse_complete_orders.groupby('Supplier')['Quantity'].sum().reset_index().sort_values('Quantity'),
        x="Supplier", y="Quantity",
        title='Συνολική παραγωγή σε ζήτηση ποσοτήτων',
        labels={'Supplier': 'Προμηθευτής', "Quantity": 'Ποσότητα'},
        text='Quantity', width=1000)
    fig_line_comp_orders_mbm.update_traces(textfont_size=13,  textangle=0,
                                           cliponaxis=False,marker_color='#146678')
    fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white', font_size=12)
    st.write(fig_line_comp_orders_mbm)





