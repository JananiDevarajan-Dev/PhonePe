import streamlit as st
import pandas as pd
from sqlalchemy import create_engine,text
import urllib.parse
import plotly.express as px


# Database connection details
username = "root"          # your MySQL username
password = urllib.parse.quote_plus("Password@0274")  # encode special characters  # your MySQL password
host = "localhost"         # local system
port = 3306                # default MySQL port
database = "Phonepe"        # your database name

# Create connection engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

def format_state_name(db_value):
    name = db_value.replace("-", " ")   # hyphens to spaces
    
    # Normalize spacing around "&"
    name = name.replace(" & ", " & ")
    name = name.replace("&", "&")  # just in case
    
    # Special cases
    exceptions = {
        "dadra & nagar haveli & daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
        "jammu & kashmir": "Jammu & Kashmir",
        "andaman & nicobar islands": "Andaman & Nicobar",
        "uttar pradesh": "Uttar Pradesh",
    }
    
    lower_name = name.lower().strip()
    if lower_name in exceptions:
        return exceptions[lower_name]
    
    return name.title()


# Queries

transaction_q = """ select distinct quater from agg_transaction ;"""
transaction_quarter = pd.read_sql(transaction_q, engine)

transaction_y = """select distinct year from agg_transaction;"""
transaction_year = pd.read_sql(transaction_y, engine)

transaction_s="""select distinct state from agg_transaction;"""
transaction_state = pd.read_sql(transaction_s, engine)

insurance_y = """select distinct year from top_insurance where year between 2020 and 2024;"""
insurance_year = pd.read_sql(insurance_y, engine)

# Queries End

# Streamlit Code


r=st.sidebar.radio("Navigation",["Home","Business Case Study"])
st.title("Phonepay Data Analysis")


#Home Page Design
if r =="Home" :
    st.title("Home page")
    col1,col2,col3=st.columns(3)
    selected_value=col1.selectbox("",["Transactions","Users"])
    selected_quarter=col2.selectbox("Select Quarter",transaction_quarter)
    selected_year=col3.selectbox("Select Year",transaction_year)
    if selected_value == "Transactions" :
        #st.write(f"{selected_quarter},{selected_year}")
        query_quarter_year=""" select sum(transacion_amount)as Transacion_amount,state,year,quater from agg_transaction where year = :year and quater =:quater group by state order by Transacion_amount desc  ;"""
        query_quarter_map = pd.read_sql_query(sql=text(query_quarter_year),con=engine,params={"year": selected_year, "quater": selected_quarter})
        #print(query_quarter_map)

        # Apply formatting
        query_quarter_map["state"] = query_quarter_map["state"].apply(format_state_name)

        fig = px.choropleth(
        query_quarter_map,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='Transacion_amount',
        color_continuous_scale='Reds'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        st.table(query_quarter_map)
    if selected_value == "Users" :
        user_quarter_year=""" select sum(RegisteredUsers) as RegisteredUsers,state,year,quater from agg_user where year = :year and quater= :quater group by state order by RegisteredUsers desc;"""
        user_quarter_map = pd.read_sql_query(sql=text(user_quarter_year),con=engine,params={"year": selected_year, "quater": selected_quarter})
        #print(user_quarter_map)

        # Apply formatting
        user_quarter_map["state"] = user_quarter_map["state"].apply(format_state_name)

        fig = px.choropleth(
        user_quarter_map,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='RegisteredUsers',
        color_continuous_scale='Reds'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        st.table(user_quarter_map) 

#Business Case Study
if r =="Business Case Study" :
    st.title("Business Case Study")
    selected_business=st.selectbox("Select Any Questions:",["Transaction Analysis for Market Expansion","User Engagement and Growth Strategy","Transaction Analysis Across States and Districts","User Registration Analysis","Insurance Transactions Analysis"])
    if selected_business == "Transaction Analysis for Market Expansion" :
        st.header("Total Transaction Amount Analysis")
        col1,col2=st.columns(2)
        selected_quarter=col1.selectbox("Select quarter:",transaction_quarter)
        selected_year=col2.selectbox("Select Year",transaction_year)
        #st.write(f"{selected_quarter},{selected_year}")
        query_quarter_year=""" select sum(transacion_amount)as Transacion_amount,state,year,quater from agg_transaction where year = :year and quater =:quater group by state order by Transacion_amount desc  ;"""
        query_quarter_map = pd.read_sql_query(sql=text(query_quarter_year),con=engine,params={"year": selected_year, "quater": selected_quarter})
        #print(query_quarter_map)

        # Apply formatting
        query_quarter_map["state"] = query_quarter_map["state"].apply(format_state_name)

        fig = px.choropleth(
        query_quarter_map,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='Transacion_amount',
        color_continuous_scale='Reds'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

        #Payment Method popularity
        st.header("Payment Method Popularity")
        st.subheader("Distribution of Total Transaction Count")
        trans_query_count= """ select sum(transacion_count) as Transaction_Count,transacion_type as Transaction_Type from agg_transaction group by Transaction_Type order by Transaction_Count desc;"""
        trans_query_count_data = pd.read_sql_query(trans_query_count, engine)
        # Donut chart based on total transaction amount
        fig = px.pie(
        trans_query_count_data,
        names="Transaction_Type",              # column for labels
        values="Transaction_Count",      # column for values
        hole=0.4,                   # this makes it a donut (40% hole)
        title="Distribution of Total Count by Transaction Type"
        )
        st.plotly_chart(fig)

        st.subheader("Distribution of Total Transaction Amount")
        trans_query_payment = """select sum(Transacion_amount) as Transaction_Amount,transacion_type as Transaction_Type from agg_transaction group by Transacion_type order by Transaction_Amount desc; """
        trans_query_payement_df = pd.read_sql(trans_query_payment, engine)
        # Pie  chart based on total transaction amount
        fig = px.pie(
        trans_query_payement_df,
        names="Transaction_Type",              # column for labels
        values="Transaction_Amount",      # column for values
        title="Distribution of Total Amount by Transaction Type"
        )
        st.plotly_chart(fig)

        # Transactions by State and Payment Category
        st.header("Transactions by State and Payment Category")
        col1,col2=st.columns(2)
        selected_state=col1.selectbox("Select State",transaction_state)
        st.subheader("Transaction Distribution in " +selected_state)
        trans_query_state=""" select sum(Transacion_amount) as Transaction_Amount,transacion_type as Payment_Category,state from agg_transaction where state= :state group by Payment_Category order by Transaction_Amount desc;"""
        trans_query_state_values = pd.read_sql_query(sql=text(trans_query_state),con=engine,params={"state": selected_state})
        #print(query_quarter_map)
        fig = px.line(
        trans_query_state_values,
        x="Payment_Category",              # column for labels
        y="Transaction_Amount",      # column for values
        #title="Distribution of Total Count by Transaction Type"
        )
        st.plotly_chart(fig)

        # Trend Analysis
        st.header("Trend Analysis")
        col1,col2=st.columns(2)
        selected_year_trend=col1.selectbox("Select the Year",transaction_year)
        st.subheader("Transaction for Year  " +selected_year_trend)
        trans_query_year="""select sum(Transacion_amount) as Transaction_Amount,quater as Quarter,year from agg_transaction where year = :year group by year,quater order by Transaction_amount desc;"""
        trans_query_year_values = pd.read_sql_query(sql=text(trans_query_year),con=engine,params={"year": selected_year_trend})
        fig = px.bar(
        trans_query_year_values, 
        x='Quarter', 
        y='Transaction_Amount',
        title='Transaction Trend Analysis by  Year',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        st.plotly_chart(fig)

    if selected_business == "User Engagement and Growth Strategy" :
        st.header("Users State-Level Engagement")
        col1,col2=st.columns(2)
        user_quarter=col1.selectbox("Select the quarter:",transaction_quarter)
        user_year=col2.selectbox("Select the Year",transaction_year)
        user_quarter_year=""" select sum(RegisteredUsers) as RegisteredUsers,state,year,quater from agg_user where year = :year and quater= :quater group by state order by RegisteredUsers desc;"""
        user_quarter_map = pd.read_sql_query(sql=text(user_quarter_year),con=engine,params={"year": user_year, "quater": user_quarter})
        #print(user_quarter_map)

        # Apply formatting
        user_quarter_map["state"] = user_quarter_map["state"].apply(format_state_name)

        fig = px.choropleth(
        user_quarter_map,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='RegisteredUsers',
        color_continuous_scale='Reds'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

        #Payment Method popularity
        st.header("User Engagement Ratio Statewise")
        st.subheader("Distribution of Total Users Count")
        user_query_count= """ select sum(RegisteredUsers) as RegisteredUsers,quater from agg_user group by quater order by RegisteredUsers desc;"""
        user_query_count_data = pd.read_sql_query(user_query_count, engine)
        # Donut chart based on total transaction amount
        fig = px.pie(
            user_query_count_data,
            names="quater",              # column for labels
            values="RegisteredUsers",      # column for values
            title="Distribution of Total User Count Quarter Wise"
            )
        st.plotly_chart(fig)

         # Users Count by State
        st.header("Users Count in QuarterWise by State")
        col1,col2=st.columns(2)
        user_state=col1.selectbox("Select the State",transaction_state)
        st.subheader("Users Count in " +user_state)
        user_query_state=""" select sum(RegisteredUsers) as RegisteredUsers,state,quater as Quarter from agg_user where state= :state group by state,Quarter order by RegisteredUsers desc;"""
        user_query_state_values = pd.read_sql_query(sql=text(user_query_state),con=engine,params={"state": user_state})
        #print(query_quarter_map)
        fig = px.line(
        user_query_state_values,
        x="Quarter",              # column for labels
        y="RegisteredUsers",      # column for values
        title="Users Count in QuarterWise by State"
        )
        st.plotly_chart(fig)

        # User Trend Analysis
        st.header("User Trend Analysis")
        col1,col2=st.columns(2)
        user_year_trend=col1.selectbox("Select the Year for User Trend Analysis",transaction_year)
        st.subheader("RegisteredUser for the Year  " +user_year_trend)
        user_query_year="""select sum(RegisteredUsers) as RegisteredUsers,quater as Quarter,year from agg_user where year = :year group by year,quater order by RegisteredUsers desc;"""
        user_query_year_values = pd.read_sql_query(sql=text(user_query_year),con=engine,params={"year": user_year_trend})
        fig = px.bar(
        user_query_year_values, 
        x='Quarter', 
        y='RegisteredUsers',
        title='User Trend Analysis Through Year',
        text='RegisteredUsers',
        color='RegisteredUsers'  # Adds color differentiation
        )
        st.plotly_chart(fig)

        # User Trend Analysis for Top 20 States by Year
        st.header("User Trend Analysis for Top 20 States by Year")
        col1,col2=st.columns(2)
        user_year_trend1=col1.selectbox("Select Year:",transaction_year)
        st.subheader("RegisteredUser for the Year  " +user_year_trend1)
        user_query_year1="""select  sum(RegisteredUsers) as RegisteredUsers, state from agg_user where year = :year group by state order by RegisteredUsers desc limit 20"""
        user_query_year1_values = pd.read_sql_query(sql=text(user_query_year1),con=engine,params={"year": user_year_trend1})
        fig = px.bar(
        user_query_year1_values,
        x='RegisteredUsers',
        y='state',
        orientation='h',
        text='RegisteredUsers',
        color='RegisteredUsers',
        color_continuous_scale='Blues',
        title='Registered Users by State'
        )

        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(
            height=1000,  # Tall chart to fit all 36 states
            xaxis_title='Registered Users',
            yaxis_title='State',
            showlegend=False,
            plot_bgcolor='white'
        )
        st.plotly_chart(fig)
        
    if selected_business == "Transaction Analysis Across States and Districts" :
        st.header("Top 10 States based on Transaction Amount")
        top_states="""select state,sum(Transacion_amount) as Transaction_Amount FROM top_transaction group by state order by transaction_amount desc limit 10;"""
        top_states_query=pd.read_sql_query(top_states, engine)
        fig = px.bar(
        top_states_query, 
        x='state', 
        y='Transaction_Amount',
        title='Top 10 States by Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)
        
        st.header("Top 10 Districts based on Transaction Amount")
        top_district="""select District_Name , sum(Transacion_amount) as Transaction_Amount FROM top_transaction where District_Name is not null AND District_Name != 'none' group by District_Name order by transaction_amount desc limit 10;"""
        top_district_query=pd.read_sql_query(top_district, engine)
        fig = px.bar(
        top_district_query, 
        x='District_Name', 
        y='Transaction_Amount',
        title='Top 10 Districts by Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        st.header("Top 10 Pincodes based on Transaction Amount")
        top_pincodes="""select pincodes, sum(Transacion_amount) as Transaction_Amount FROM top_transaction where pincodes is not null AND pincodes != 'none' group by pincodes order by transaction_amount desc limit 10;"""
        top_pincodes_query=pd.read_sql_query(top_pincodes, engine)
        fig = px.pie(
            top_pincodes_query,
            names="pincodes",              # column for labels
            values="Transaction_Amount",      # column for values
            title="Top 10 Pincodes by Transaction_Amount"
            )
        st.plotly_chart(fig)

        st.header("Top Districts by Transaction Amount per State")
        col1,col2=st.columns(2)
        select_district_state=col1.selectbox("Select State for districts",transaction_state)
        st.subheader("Selected State: " +select_district_state)
        district_query_state=""" select district_name, sum(Transacion_amount) as Transaction_Amount,state FROM top_transaction where state = :state and district_name is not null AND district_name != 'none' group by district_name,state order by transaction_amount desc;"""
        district_query_state_values = pd.read_sql_query(sql=text(district_query_state),con=engine,params={"state": select_district_state})
        fig = px.bar(
        district_query_state_values,
        x="Transaction_Amount",
        y="district_name",
        color="state",
        orientation="h",
        title="Top Districts by Transaction Amount per State",
        text="Transaction_Amount",
        height=600
        )

        fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis_title="Transaction Amount",
        yaxis_title="District",
        legend_title="State"
        )
        st.plotly_chart(fig)

        st.header("Top 10 States by Transaction Count as per State")
        state_count_query=""" select state,sum(Transacion_count) as Transaction_Count FROM top_transaction group by state order by Transaction_Count desc limit 10 ;"""
        state_count_query_values = pd.read_sql_query(sql=text(state_count_query),con=engine)
        # --- Create horizontal bar chart ---
        fig = px.bar(
            state_count_query_values,
            x="Transaction_Count",
            y="state",
            orientation="h",
            title="Total 10 Transactions Count by State",
            text="Transaction_Count",
            color="Transaction_Count",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig)

        # --- Customize layout ---
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(
            xaxis_title="Total Transactions",
            yaxis_title="State",
            template="plotly_white",
            coloraxis_showscale=False,
            height=500
        )
        st.header("Top States by  Transaction Amount and  Transaction Count per Year")
        col1,col2=st.columns(2)
        select_year_transaction=col1.selectbox("Select Year for  Transaction Analysis : ",transaction_year)
        st.subheader("Selected  year is : " +select_year_transaction)
        select_year_transaction_query=""" select sum(Transacion_count) as Transaction_Count,sum(Transacion_amount) as Transaction_Amount ,state from top_transaction where year= :year group by state order by Transaction_Amount desc ,Transaction_Count desc;"""
        select_year_transaction_query_values = pd.read_sql_query(sql=text(select_year_transaction_query),con=engine,params={"year": select_year_transaction})
       # Melt the dataframe to long format for px.bar
        df_long = select_year_transaction_query_values.melt(
            id_vars='state',
            value_vars=['Transaction_Amount', 'Transaction_Count'],
            var_name='Metric',
            value_name='Value'
        )

        # Simple grouped bar chart
        fig = px.bar(
            df_long,
            x='state',
            y='Value',
            color='Metric',
            barmode='group',  # 'group' for side-by-side bars, 'stack' for stacked bars
            text='Value',
            title=f'Transaction Amount & Count by State for {select_year_transaction}',
            labels={'Value':'Values', 'state':'State'}
        )

        # Rotate x-axis labels for readability
        fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
        st.plotly_chart(fig)


        st.header("Bottom 10 States based on Transaction Amount")
        least_states="""select state,sum(Transacion_amount) as Transaction_Amount FROM top_transaction group by state order by transaction_amount asc limit 10;"""
        least_states_query=pd.read_sql_query(least_states, engine)
        fig = px.bar(
        least_states_query, 
        x='state', 
        y='Transaction_Amount',
        title='Bottom 10 States by Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)
        
        st.header("Bottom 10 Districts based on Transaction Amount")
        least_district="""select District_Name ,sum(Transacion_amount) as Transaction_Amount FROM top_transaction where District_Name is not null AND District_Name != 'none' group by District_Name order by transaction_amount asc limit 10;"""
        least_district_query=pd.read_sql_query(least_district, engine)
        fig = px.bar(
        least_district_query, 
        x='District_Name', 
        y='Transaction_Amount',
        title='Bottom 10 Districts by Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        

    if selected_business == "User Registration Analysis" :
        st.header("Top 10 States based on Registered Users")
        top_user_states="""select state,sum(RegisteredUsers) as RegisteredUsers FROM top_user group by state order by RegisteredUsers desc limit 10;"""
        top_states_query=pd.read_sql_query(top_user_states, engine)
        fig = px.bar(
        top_states_query, 
        x='state', 
        y='RegisteredUsers',
        title='Top 10 States by Registered Users',
        text='RegisteredUsers',
        color='RegisteredUsers'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        st.header("Top 10 Districts based on Registered Users")
        top_district_user="""select District_Name , sum(RegisteredUsers) as RegisteredUsers FROM top_user where District_Name is not null AND District_Name != 'none' group by District_Name order by RegisteredUsers desc limit 10;"""
        top_district_user_query=pd.read_sql_query(top_district_user, engine)
        fig = px.bar(
        top_district_user_query, 
        x='District_Name', 
        y='RegisteredUsers',
        title='Top 10 Districts by Registered Users',
        text='RegisteredUsers',
        color='RegisteredUsers'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        st.header("Top 10 Pincodes based on Registered Users")
        top_pincodes_user="""select pincodes,sum(RegisteredUsers) as RegisteredUsers FROM top_user where pincodes is not null AND pincodes != 'none' group by pincodes order by RegisteredUsers desc limit 10;"""
        top_pincodes_query_user=pd.read_sql_query(top_pincodes_user, engine)
        fig = px.pie(
            top_pincodes_query_user,
            names="pincodes",              # column for labels
            values="RegisteredUsers",      # column for values
            title="Top 10 Pincodes by Registered Users"
            )
        st.plotly_chart(fig)

        st.header("Registered Users based on Specific Year-Quarter Combination")
        col1,col2=st.columns(2)
        year_quarter_user=col1.selectbox("Select Year for Quarter User Analysis",transaction_year)
        st.subheader("Selected Year: " +year_quarter_user)
        year_quarter_user1="""select sum(RegisteredUsers) as RegisteredUsers ,quater as Quarter from top_user where year = :quarterYear group by quater order by RegisteredUsers desc;"""
        least_district_query_user=pd.read_sql_query(sql=text(year_quarter_user1),con=engine,params={"quarterYear": year_quarter_user})
        # Create interactive line chart
        fig = px.line(
            least_district_query_user,
            x="Quarter",
            y="RegisteredUsers",
            title="Total Registered Users per Quarter  "+year_quarter_user,
            markers=True,
            text="RegisteredUsers"
        )

        # Customize layout
        fig.update_traces(textposition="top center", line=dict(width=3))
        fig.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Registered Users",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig)

        st.header("Bottom 10 States based on Registered Users")
        least_states_user="""select state,sum(RegisteredUsers) as RegisteredUsers FROM top_user group by state order by RegisteredUsers asc limit 10;"""
        least_states_query_user=pd.read_sql_query(least_states_user, engine)
        fig = px.bar(
        least_states_query_user, 
        x='state', 
        y='RegisteredUsers',
        title='Bottom 10 States by RegisteredUsers',
        text='RegisteredUsers',
        color='RegisteredUsers'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        st.header("Bottom 10 Districts based on Registered Users")
        least_district_user="""select District_Name ,sum(RegisteredUsers) as RegisteredUsers FROM top_user where District_Name is not null AND District_Name != 'none' group by District_Name order by RegisteredUsers asc limit 10;"""
        least_district_query_user=pd.read_sql_query(least_district_user, engine)
        fig = px.bar(
        least_district_query_user, 
        x='District_Name', 
        y='RegisteredUsers',
        title='Bottom 10 Districts by Registered Users',
        text='RegisteredUsers',
        color='RegisteredUsers'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        
    if selected_business == "Insurance Transactions Analysis" :
        st.header("Top 10 States based on Insurance Transaction Amount")
        top_states_insurance="""select state,sum(Transacion_amount) as Transaction_Amount FROM top_Insurance group by state order by transaction_amount desc limit 10;"""
        top_states_query_insurance=pd.read_sql_query(top_states_insurance, engine)
        fig = px.bar(
        top_states_query_insurance, 
        x='state', 
        y='Transaction_Amount',
        title='Top 10 States by Insurance Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)
        
        st.header("Top 10 Districts based on Insurance Transaction Amount")
        top_district_insurance="""select District_Name , sum(Transacion_amount) as Transaction_Amount FROM Top_Insurance where District_Name is not null AND District_Name != 'none' group by District_Name order by transaction_amount desc limit 10;"""
        top_district_query_insurance=pd.read_sql_query(top_district_insurance, engine)
        fig = px.bar(
        top_district_query_insurance, 
        x='District_Name', 
        y='Transaction_Amount',
        title='Top 10 Districts by Insurance Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)
        
        st.header("Top 10 Pincodes based on Insurance Transaction Amount")
        top_pincodes_insurance="""select pincodes, sum(Transacion_amount) as Transaction_Amount FROM top_insurance where pincodes is not null AND pincodes != 'none' group by pincodes order by transaction_amount desc limit 10;"""
        top_pincodes_query_insurance=pd.read_sql_query(top_pincodes_insurance, engine)
        fig = px.pie(
            top_pincodes_query_insurance,
            names="pincodes",              # column for labels
            values="Transaction_Amount",      # column for values
            title="Top 10 Pincodes by Transaction_Amount"
            )
        st.plotly_chart(fig)

        st.header("Top Districts by Insurance Transaction Amount per State")
        col1,col2=st.columns(2)
        select_district_state_insurance=col1.selectbox("Select State for Insurance Transaction Analysis : ",transaction_state)
        st.subheader("Selected State: " +select_district_state_insurance)
        district_query_state_insurance=""" select district_name, sum(Transacion_amount) as Transaction_Amount,state FROM top_insurance where state = :state and district_name is not null AND district_name != 'none' group by district_name,state order by transaction_amount desc;"""
        district_query_state_values_insurance = pd.read_sql_query(sql=text(district_query_state_insurance),con=engine,params={"state": select_district_state_insurance})
        fig = px.bar(
        district_query_state_values_insurance,
        x="Transaction_Amount",
        y="district_name",
        color="state",
        orientation="h",
        title="Top Districts by Transaction Amount per State",
        text="Transaction_Amount",
        height=600
        )

        fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis_title="Transaction Amount",
        yaxis_title="District",
        legend_title="State"
        )
        st.plotly_chart(fig)

        st.header("Top States by Insurance Transaction Count as per State")
        state_count_query_insurance="""select state,sum(Transacion_count) as Transaction_Count FROM top_insurance group by state order by Transaction_Count desc limit 10 ;"""
        state_count_query_values_insurance = pd.read_sql_query(sql=text(state_count_query_insurance),con=engine)
        # --- Create horizontal bar chart ---
        fig = px.bar(
            state_count_query_values_insurance,
            x="Transaction_Count",
            y="state",
            orientation="h",
            title="Total Transactions Count by State",
            text="Transaction_Count",
            color="Transaction_Count",
            color_continuous_scale="Blues"
        )
        
        # --- Customize layout ---
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(
            xaxis_title="Total Transactions",
            yaxis_title="State",
            template="plotly_white",
            coloraxis_showscale=False,
            height=500
        )
        st.plotly_chart(fig)


        st.header("Top States by Insurance Transaction Amount and Insurance Transaction Count per Year")
        col1,col2=st.columns(2)
        select_year_insurance=col1.selectbox("Select Year for Insurance Transaction Analysis : ",insurance_year)
        st.subheader("Selected  year is : " +select_year_insurance)
        select_year_insurance_query="""select sum(Transacion_count) as Transaction_Count,sum(Transacion_amount) as Transaction_Amount ,state from top_insurance where year= :year group by state order by Transaction_Amount desc ,Transaction_Count desc;"""
        select_year_insurance_query_values = pd.read_sql_query(sql=text(select_year_insurance_query),con=engine,params={"year": select_year_insurance})
       # Melt the dataframe to long format for px.bar
        df_long = select_year_insurance_query_values.melt(
            id_vars='state',
            value_vars=['Transaction_Amount', 'Transaction_Count'],
            var_name='Metric',
            value_name='Value'
        )

        # Simple grouped bar chart
        fig = px.bar(
            df_long,
            x='state',
            y='Value',
            color='Metric',
            barmode='group',  # 'group' for side-by-side bars, 'stack' for stacked bars
            text='Value',
            title=f'Transaction Amount & Count by State for {select_year_insurance}',
            labels={'Value':'Values', 'state':'State'}
        )

        # Rotate x-axis labels for readability
        fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
        st.plotly_chart(fig)


        st.header("Bottom 10 States based on Insurance Transaction Amount")
        least_states_insurance="""select state,sum(Transacion_amount) as Transaction_Amount FROM top_insurance group by state order by transaction_amount asc limit 10;"""
        least_states_query_insurance=pd.read_sql_query(least_states_insurance, engine)
        fig = px.bar(
        least_states_query_insurance, 
        x='state', 
        y='Transaction_Amount',
        title='Bottom 10 States by Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

        st.header("Bottom 10 Districts based on Insurance Transaction Amount")
        least_district_insurance="""select District_Name ,sum(Transacion_amount) as Transaction_Amount FROM top_insurance where District_Name is not null AND District_Name != 'none' group by District_Name order by transaction_amount asc limit 10;"""
        least_district_query_insurance=pd.read_sql_query(least_district_insurance, engine)
        fig = px.bar(
        least_district_query_insurance, 
        x='District_Name', 
        y='Transaction_Amount',
        title='Bottom 10 Districts by Transaction_Amount',
        text='Transaction_Amount',
        color='Transaction_Amount'  # Adds color differentiation
        )
        # Rotate x labels for readability
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)






        





