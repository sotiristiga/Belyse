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
st.set_page_config(layout='wide',page_title="Belyse")
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
belyse['Month_Year']=pd.to_datetime(belyse['Month_Year'],format='mixed')
belyse_complete_orders=belyse.loc[(belyse['order_situation']=="Ολοκληρώθηκε")|((belyse['order_situation']=="Μέρος της έχει επιστραφεί")& (belyse['Return']==0))]

kpi1,kpi2,kpi3,kpi4,kpi5 = st.columns(5)
kpi1.metric(label="Ολοκληρωμένες Παραγγελίες",
        value=belyse_complete_orders['id_order'].nunique())
kpi2.metric(label="Aκυρωμένες Παραγγελίες",
        value=belyse[belyse['order_situation']=="Ακυρωμένη"]['order_situation'].nunique())
kpi3.metric(label="Επιστροφή Προϊόντών",
        value=belyse['Return'].sum())
kpi4.metric(label="Έσοδα απο πωλήσεις",
        value=belyse_complete_orders['Total_payment'].sum().round(2))
kpi5.metric(label="Προμήθεια Skroutz",
        value=belyse_complete_orders.groupby('id_order')['Skroutz_Commission'].mean().reset_index()['Skroutz_Commission'].sum().round(2))


pie1, pie2,pie3= st.columns([3,3,9])
with pie1:
    pie1=px.pie(belyse_complete_orders[['id_order','Invoice']].value_counts().reset_index().groupby('Invoice').count().reset_index(),
        values='count',names='Invoice', color='Invoice',
        color_discrete_sequence= px.colors.sequential.Aggrnyl,labels={'count':'Σύνολο',
                                                            'Invoice':'Τύπος παραστατικού'}, 
        height=350,
        title='Τύπος παραστατικού',hole=0.5,width=800)
    pie1.update_traces(hoverinfo="value",textfont_size=17)
    pie1.update_layout(plot_bgcolor='white',font_size=20,
                       legend=dict(yanchor="bottom",y=0.05,xanchor="left",x=0.01),legend_title_text='',title_x=0.1,title_y=0.8)
    st.write(pie1)

with pie2:
    pie2=px.pie(belyse_complete_orders[['id_order','Courier']].value_counts().reset_index().groupby('Courier').count().reset_index(),
        values='count',names='Courier', color='Courier',
        color_discrete_sequence= px.colors.sequential.Aggrnyl,labels={'count':'Σύνολο'}, 
        height=350,
        title='Courier',hole=0.5,width=1000)
    pie2.update_traces(hoverinfo="value",textfont_size=17)
    pie2.update_layout(plot_bgcolor='white',font_size=20,legend=dict(yanchor="top",y=0.005,xanchor="left",x=0.001),title_y=0.8)
    st.write(pie2)

with pie3:
       fig_line_comp_orders_mbm = px.bar(belyse_complete_orders['Product'].value_counts().head(4).reset_index(), 
                                x="count", y="Product", 
                                title='Top 4 προϊόντα σε πωλήσεις',
                        labels={'Product':'Προϊόν',"count":'Συνολικές πωλήσεις'},
                        text='count',width=1200)
       fig_line_comp_orders_mbm.update_traces(textfont_size=14, textangle=0, cliponaxis=False)
       fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white',font_size=14)
       st.write(fig_line_comp_orders_mbm)


st.write("#### Ολοκληρωμένες παραγγελίες")

tab1,tab2=st.tabs(['Συνολικές παραγγελίες',"Έσοδα"])

with tab1:
        tab11,tab12=st.tabs(['Ανά ημέρα',"Ανά μήνα"])
        with tab11:
                fig_line_comp_orders_dbd = px.line(belyse[belyse['order_situation']=="Ολοκληρώθηκε"][['Date_order','id_order']].value_counts().reset_index().groupby('Date_order')['count'].count().reset_index().sort_values('Date_order'), 
                                        x="Date_order", y="count", 
                                        title='',
                                labels={'Date_order':'Ημερομηνία',"count":'Ολοκληρωμένες παραγγελίες'},
                                markers=True,width=1800)
                fig_line_comp_orders_dbd.update_layout(plot_bgcolor='white',font_size=13)
                st.write(fig_line_comp_orders_dbd)
        with tab12:
                fig_line_comp_orders_mbm = px.bar(belyse[belyse['order_situation']=="Ολοκληρώθηκε"][['Month_Year','id_order']].value_counts().reset_index().groupby('Month_Year')['count'].count().reset_index().sort_values('Month_Year'), 
                                        x="Month_Year", y="count", 
                                        title='',
                                labels={'Month_Year':'Μήνας-Έτος',"count":'Ολοκληρωμένες παραγγελίες'},
                                text_auto=True,width=1000)
                fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white',font_size=13)
                st.write(fig_line_comp_orders_mbm)

with tab2:
        tab21,tab22=st.tabs(['Ανά ημέρα',"Ανά μήνα"])
        with tab21:
                fig_line_comp_orders_dbd = px.line(belyse.loc[(belyse['order_situation']=="Ολοκληρώθηκε")|((belyse['order_situation']=="Μέρος της έχει επιστραφεί")& (belyse['Return']==0))].groupby(['Date_order','id_order'])['Total_payment'].mean().reset_index().groupby('Date_order')['Total_payment'].sum().reset_index().sort_values('Date_order'), 
                                        x="Date_order", y="Total_payment", 
                                        title='',
                                labels={'Date_order':'Ημερομηνία',"Total_payment":'Έσοδα από πωλήσεις'},
                                markers=True,width=1800)
                fig_line_comp_orders_dbd.update_layout(plot_bgcolor='white',font_size=13)
                st.write(fig_line_comp_orders_dbd)
        with tab22:
                fig_line_comp_orders_mbm = px.bar(belyse.loc[(belyse['order_situation']=="Ολοκληρώθηκε")|((belyse['order_situation']=="Μέρος της έχει επιστραφεί")& (belyse['Return']==0))].groupby(['Month_Year','id_order'])['Total_payment'].mean().reset_index().groupby('Month_Year')['Total_payment'].sum().reset_index().sort_values('Month_Year'), 
                                        x="Month_Year", y="Total_payment", 
                                        title='',
                                labels={'Month_Year':'Μήνας-Έτος',"Total_payment":'Έσοδα από πωλήσεις'},
                                text='Total_payment',width=1000)
                fig_line_comp_orders_mbm.update_traces(textfont_size=13, texttemplate = '%{text:.3s} €',textangle=0, cliponaxis=False)
                fig_line_comp_orders_mbm.update_layout(plot_bgcolor='white',font_size=12)
                st.write(fig_line_comp_orders_mbm)



