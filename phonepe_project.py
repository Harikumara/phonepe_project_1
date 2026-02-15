import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import psycopg2
import pandas as pd
import json
import requests

# Dataframe creation

#sql connection

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "phone_db",
                        password = "Swag5566!")

cursor= mydb.cursor()

#aggregated_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1, columns=("states","years","quater","Transaction_type","Transaction_count","Transaction_amount"))


#aggregated_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

agg_transaction  = pd.DataFrame(table2, columns=("states","years","quater","Transaction_type","Transaction_count","Transaction_amount"))


#aggregated_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

aggre_user  = pd.DataFrame(table3, columns=("states","years","quater","Brands","Transaction_count","Percentage"))


#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall()

map_insurance   = pd.DataFrame(table4, columns=("states","years","quater","Districts","Transaction_count","Transaction_amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cursor.fetchall()

map_transaction   = pd.DataFrame(table5, columns=("states","years","quater","Districts","Transaction_count","Transaction_amount"))

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall()

map_user  = pd.DataFrame(table6, columns=("states","years","quater","Districts","RegisteredUsers","AppOpens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cursor.fetchall()

top_insurance  = pd.DataFrame(table7, columns=("states","years","quater","Pincodes","Transaction_count","Transaction_amount"))


#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cursor.fetchall()

top_transaction  = pd.DataFrame(table8, columns=("states","years","quater","Pincodes","Transaction_count","Transaction_amount"))


#top_users_df
cursor.execute("SELECT * FROM top_users")
mydb.commit()
table9 = cursor.fetchall()

top_users  = pd.DataFrame(table9, columns=("states","years","quater","Pincodes","RegisteredUsers"))

def Transaction_amount_count_Y(df,year):

    tacy = df[df["years"] == year]
    tacy.reset_index(drop = True, inplace = True)


    tacyg= tacy.groupby("states")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="states", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with(col2):   

        fig_count= px.bar(tacyg, x="states", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
        
        st.plotly_chart(fig_count)



    col1,col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1 = json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "states", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)



    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "states", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy  


def Transaction_amount_count_Y_Q(df,quater):
    tacy = df[df["quater"] == quater]
    tacy.reset_index(drop = True, inplace = True)


    tacyg= tacy.groupby("states")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="states", y="Transaction_amount", title=f"{tacy['years'].min()} year {quater}  quater TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="states", y="Transaction_count", title=f"{tacy['years'].min()} year {quater}  quater TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width= 600)
        
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1 = json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "states", title= f"{tacy['years'].min()} year {quater}  quater TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "states", title= f"{tacy['years'].min()} year {quater}  quater TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy
     

def Aggre_Tran_Transaction_type(df, state):
    
    tacy= df[df["states"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        
        st.plotly_chart(fig_pie_1)

    with col2:    
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        
        st.plotly_chart(fig_pie_2)

def Aggre_user_plot_1(df, year):
    aguy= df[df['years']== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy


def Aggre_user_plot_2(df, quater):
    aguyq= df[df["quater"]== quater]
    aguyq.reset_index(drop= True,inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quater} QUATER, BRANDS AND TRANSACTION COUNT",
                        width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")

    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggree_user_analysis_3:
def Aggre_user_plot_3(df,state):
   auyqs= df[df["states"] == state]
   auyqs.reset_index(drop= True, inplace= True)

   fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                       title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
   
   st.plotly_chart(fig_line_1)



#map_isnurance_district
def map_insur_district(df, state):
    
    tacy= df[df["states"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        
        st.plotly_chart(fig_count)


#map_user_plot1
def map_user_plot_1(df,year):
    muy= df[df["years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("states")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x="states", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{year} REGISTEREDUSER APPOPENS", width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

#map_user_plot2
def map_user_plot_2(df,quater):
    muyq= df[df["quater"]== quater]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("states")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x="states", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{df['years'].min()} YEAR {quater} QUATER REGISTEREDUSER USER, APPOPENS", width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["states"]== states]
    muyqs.reset_index(drop= True, inplace= True)


    col1,col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUsers", y= "Districts", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)
    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts", orientation= "h",
                                title= f"{states.upper()} APPOPENS USER", height= 800, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

#top_insurance_plot_1
def top_insurance_plot_1(df, state):
    tiy= df[df["states"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "quater", y= "Transaction_amount", hover_data= "Pincodes",
                                    title= "TRANSACTION AMOUNT", height= 650, width= 600, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "quater", y= "Transaction_count", hover_data= "Pincodes",
                                    title= "TRANSACTION COUNT", height= 650, width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

#top_user_analysis
def top_user_plot_1(df, year):
    tuy= df[df['years']== year]
    tuy.reset_index(drop= True, inplace= True)


    tuyg= pd.DataFrame(tuy.groupby(["states", "quater"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)
    

    fig_top_plot_1= px.bar(tuyg, x="states", y= "RegisteredUsers", color= "quater", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burg_r, hover_name= "states",
                        title= f"{year} REGISTERED USERS")

    st.plotly_chart(fig_top_plot_1)

    return tuy

#top_user_plot_2
def top_user_plot_2(df, states):
    tuys= df[df["states"]== states]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2= px.bar(tuys, x="quater", y= "RegisteredUsers", title= "REGISTEREDUSERS,PINCODES,QUATER",
                           width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                           color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)
    
#sql connection

def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phone_db",
                            password = "Swag5566!")

    cursor= mydb.cursor()

    #plot_1
    query1= f'''select states, sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount",))
    
    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title= "TOP 10 OF TRANSACTION AMOUNT",hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig_amount)




    #plot_2

    query2= f'''select states, sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount 
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount",))
    
    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title= "LAST 10 OF TRANSACTION AMOUNT",hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height= 650,width= 600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query3= f'''select states, avg(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount",))
    

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title= "AVERAGE OF TRANSACTION AMOUNT",hover_name= 'states', orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection

def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phone_db",
                            password = "Swag5566!")

    cursor= mydb.cursor()

    #plot_1
    query1= f'''select states, sum(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count",))
   

    col1,col2= st.columns(2)
    with col1:

        fig_amount_4= px.bar(df_1, x="states", y="transaction_count", title= "TOP 10 OF TRANSACTION COUNT",hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig_amount_4)




    #plot_2

    query2= f'''select states, sum(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count 
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count",))
    
    with col2:
        fig_amount_5= px.bar(df_2, x="states", y="transaction_count", title= "LAST 10 OF TRANSACTION COUNT",hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height= 650,width= 600)
        st.plotly_chart(fig_amount_5)



    #plot_3
    query3= f'''select states, avg(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count",))
    

    fig_amount_6= px.bar(df_3, y="states", x="transaction_count", title= "AVERAGE OF TRANSACTION COUNT",hover_name= 'states', orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height= 800,width= 1000)
    st.plotly_chart(fig_amount_6)


#sql connection

def top_chart_registered_user(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phone_db",
                            password = "Swag5566!")

    cursor= mydb.cursor()

    #plot_1
    query1= f'''select districts, sum(registeredusers) as registereduser
                from {table_name}
                where states= '{state}'
                group by districts
                order by registereduser desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "registeredusers",))
    
    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registeredusers", title= "TOP 10 OF REGISTERED USERS",hover_name= 'districts',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig_amount)




    #plot_2

    query2= f'''select districts, sum(registeredusers) as registereduser
                from {table_name}
                where states= '{state}'
                group by districts
                order by registereduser 
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "registeredusers",))

   
    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registeredusers", title= "LAST 10 OF REGISTERED USERS",hover_name= 'districts',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height= 650,width= 600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query3= f'''select districts, avg(registeredusers) as registereduser
                from {table_name}
                where states= '{state}'
                group by districts
                order by registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "registeredusers",))
    df_3

    fig_amount_3= px.bar(df_3, y="districts", x="registeredusers", title= "AVERAGE OF REGISTERED USERS",hover_name= 'districts', orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

def top_chart_appopens(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phone_db",
                            password = "Swag5566!")

    cursor= mydb.cursor()

    #plot_1
    query1= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states= '{state}'
                group by districts
                order by appopens desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens",))
    
    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="appopens", title= "TOP 10 OF APPOPENS",hover_name= 'districts',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig_amount)




    #plot_2

    query2= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states= '{state}'
                group by districts
                order by appopens 
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens",))
   
    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title= "LAST 10 OF APPOPENS",hover_name= 'districts',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height= 650,width= 600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query3= f'''select districts, avg(appopens) as appopens
                from {table_name}
                where states= '{state}'
                group by districts
                order by appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens",))
    

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title= "AVERAGE OF APPOPENS",hover_name= 'districts', orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


#sql connection

def top_chart_registered_users(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phone_db",
                            password = "Swag5566!")

    cursor= mydb.cursor()

    #plot_1
    query1= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                 group by states
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registeredusers",))
    col1,col2= st.columns(2)
    with col1:
    

        fig_amount= px.bar(df_1, x="states", y="registeredusers", title= "TOP 10 OF REGISTERED USERS",hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig_amount)




    #plot_2

    query2= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                 group by states
                order by registeredusers 
                limit 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registeredusers",))

    with col2:

        fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title= "LAST 10 OF REGISTERED USERS",hover_name= 'states',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height= 650,width= 600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query3= f'''select states, avg(registeredusers) as registeredusers
                from {table_name}
                 group by states
                order by registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registeredusers",))
    

    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title= "AVERAGE OF REGISTERED USERS",hover_name= 'states', orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

# Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    

    select= option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])


if select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("Phonepe is an Indian digital payments and financial technology comapany")
        st.write("*****FEAUTURES******")
        st.write("*****Credit & Debit card linking*****")
        st.write("*****Bank Balance check******")
        st.write("*****Money Storage******")
        st.write("*****PIN Authorization******")
        st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")

    with col2:
        st.image(r"C:\Users\Dell\Pictures\download.png", width= 600)

    col3,col4= st.columns(2)

    with col3:
        st.image(r"C:\Users\Dell\Pictures\spain-11th-aug-2021-in-this-photo-illustration-a-phonepe-logo-seen-displayed-on-a-smartphone-credit-image-thiago-prudenciosopa-images-via-zuma-press-wire-2GF3E40.jpg",width= 600)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payements****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transafer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown("  ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(r"C:\Users\Dell\Pictures\download.jpg",width= 600)

elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:


              years= st.slider("Select The Year",Aggre_insurance["years"].min(), Aggre_insurance["years"].max(), Aggre_insurance["years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)

            col1,col2= st.columns(2)
            with col1:

                quater= st.slider("Select The Quater",tac_Y["quater"].min(), tac_Y["quater"].max(), tac_Y["quater"].min())
            Transaction_amount_count_Y_Q(tac_Y,quater)

        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:


              years= st.slider("Select The Year_ta",agg_transaction["years"].min(), agg_transaction["years"].max(), agg_transaction["years"].min())
            aggre_tran_tac_Y= Transaction_amount_count_Y(agg_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_sta", aggre_tran_tac_Y["states"].unique())

            Aggre_Tran_Transaction_type(aggre_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quater= st.slider("Select The Quater_Atq",aggre_tran_tac_Y["quater"].min(), aggre_tran_tac_Y["quater"].max(), aggre_tran_tac_Y["quater"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(aggre_tran_tac_Y,quater)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["states"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)
            

        elif method == "User Analysis":

            col1,col2= st.columns(2)
            with col1:


              years= st.slider("Select The Year_ua",aggre_user["years"].min(), aggre_user["years"].max(), aggre_user["years"].min())
            Aggre_user_Y= Aggre_user_plot_1(aggre_user, years)

            col1,col2= st.columns(2)
            with col1:
                quater= st.slider("Select The quater_uq",Aggre_user_Y["quater"].min(), Aggre_user_Y["quater"].max(), Aggre_user_Y["quater"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quater)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_us", Aggre_user_Y_Q["states"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

          

    with tab2:

        method_2 = st.radio("Select The Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
            col1,col2= st.columns(2)
            with col1:


              years= st.slider("Select The Year_my",map_insurance["years"].min(), map_insurance["years"].max(), map_insurance["years"].min())
            map_insur_tac_Y= Transaction_amount_count_Y(map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_ms", map_insur_tac_Y["states"].unique())

            map_insur_district(map_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quater= st.slider("Select The Quater_mq",map_insur_tac_Y["quater"].min(), map_insur_tac_Y["quater"].max(), map_insur_tac_Y["quater"].min())
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y,quater)

            col1, col2 = st.columns(2)

            with col1:
                states = st.selectbox(
                    "Select The State_my",
                    map_insur_tac_Y_Q["states"].unique(),
                    key="insurance_state_select"
                )

            map_insur_district(map_insur_tac_Y_Q, states)


        elif method_2 == "Map Transaction":
            col1,col2= st.columns(2)
            with col1:


              years= st.slider("Select The Year_mt",map_transaction["years"].min(), map_transaction["years"].max(), map_transaction["years"].min())
            map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mts", map_tran_tac_Y["states"].unique())

            map_insur_district(map_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quater= st.slider("Select The Quater_mqs",map_tran_tac_Y["quater"].min(), map_tran_tac_Y["quater"].max(), map_tran_tac_Y["quater"].min())
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y,quater)

            col1, col2 = st.columns(2)

            with col1:
                states = st.selectbox("Select The State_mss",map_tran_tac_Y_Q["states"].unique())

            map_insur_district(map_tran_tac_Y_Q, states)

        elif method_2 == "Map User":
            col1,col2= st.columns(2)
            with col1:


              years= st.slider("Select The Year_muy",map_user["years"].min(), map_user["years"].max(), map_user["years"].min())
            map_user_Y= map_user_plot_1(map_user, years)

            col1,col2= st.columns(2)
            with col1:

                quater= st.slider("Select The Quater_muq",map_user_Y["quater"].min(), map_user_Y["quater"].max(), map_user_Y["quater"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quater)

            col1, col2 = st.columns(2)

            with col1:
                states = st.selectbox("Select The State_mus",map_user_Y_Q["states"].unique())

            map_user_plot_3(map_user_Y_Q, states)


    with tab3:
        method_top = st.radio("Select The Method",["Top Insurance", "Top Transaction", "Top User"])

        if method_top == "Top Insurance":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_tit",top_insurance["years"].min(), top_insurance["years"].max(), top_insurance["years"].min())
            top_insur_tac_Y= Transaction_amount_count_Y(top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tst", top_insur_tac_Y["states"].unique())
            top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quater= st.slider("Select The Quater_tqr",top_insur_tac_Y["quater"].min(), top_insur_tac_Y["quater"].max(), top_insur_tac_Y["quater"].min())
            Transaction_amount_count_Y_Q(top_insur_tac_Y, quater)

        elif method_top == "Top Transaction":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_tt",top_transaction["years"].min(), top_transaction["years"].max(), top_transaction["years"].min())
            top_tran_tac_Y= Transaction_amount_count_Y(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tts", top_tran_tac_Y["states"].unique())
            top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quater= st.slider("Select The Quater_ttq",top_tran_tac_Y["quater"].min(), top_tran_tac_Y["quater"].max(), top_tran_tac_Y["quater"].min())
            Transaction_amount_count_Y_Q(top_tran_tac_Y, quater)

        elif method_top == "Top User":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_tuy",top_users["years"].min(), top_users["years"].max(), top_users["years"].min())
            top_user_Y= top_user_plot_1(top_users, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tus", top_user_Y["states"].unique())
            top_user_plot_2(top_user_Y, states)


elif select == "TOP CHARTS":
    questions= st.selectbox("Select the question", ["1.transaction Amount and Count of Aggregated insurance",
                                                    "2.Transaction Amount and Count of Map insurance",
                                                    "3.Transation Amount and Count of Top insurance",
                                                    "4.Transaction Amount and Count of Aggregated Transaction",
                                                    "5.Transaction Amount and Count of Map Transaction",
                                                    "6.Transaction Amount and Count of Top Transaction", 
                                                    "7.Transaction Count of Aggregated User",
                                                    "8.Registered Count of Aggregated User",
                                                    "9.App opens of Map User",
                                                    "10.Registered Users of Top User"])
    if questions == "1.transaction Amount and Count of Aggregated insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")


    elif questions == "2.Transaction Amount and Count of Map insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif questions == "3.Transation Amount and Count of Top insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif questions == "4.Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif questions == "5.Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif questions == "6.Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif questions == "7.Transaction Count of Aggregated User":


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif questions == "8.Registered Count of Aggregated User":

        states= st.selectbox("select the State", map_user["states"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif questions == "9.App opens of Map User":

        states= st.selectbox("select the State", map_user["states"].unique())
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif questions == "10.Registered Users of Top User":

        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_users")



    

