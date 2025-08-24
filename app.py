from pickle import FALSE

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit import columns

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # Total invested Amount
    total = round(df['amount'].sum())


    # Max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    # Avg amount infused in a startup
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    # Total funded startup
    num_startups = df['startup'].nunique()


    col1,col2,col3,col4 = columns(4)

    with col1:
        st.metric('Total', str(total) + ' Cr')

    with col2:
        st.metric('Max Funding', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg Funding', str(avg_funding) + ' Cr')

    with col4:
        st.metric('Total StartUps', num_startups)

    # st.header('📈 Month-on-Month (MoM) Graph')
    #
    # selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    #
    # # Group data
    # if selected_option == 'Total':
    #     temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    # else:
    #     temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    #
    # # Create proper datetime column for sorting
    # temp_df['date'] = pd.to_datetime(temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str) + '-01')
    #
    # # Sort by date
    # temp_df = temp_df.sort_values('date')
    #
    # # Plot
    # fig3, ax3 = plt.subplots(figsize=(10, 5))
    # ax3.plot(temp_df['date'], temp_df['amount'], marker='o', linestyle='-', linewidth=2)
    #
    # # Labels & formatting
    # ax3.set_title(f"Month-on-Month {selected_option}", fontsize=14, weight='bold')
    # ax3.set_xlabel("Month", fontsize=12)
    # ax3.set_ylabel("Amount" if selected_option == 'Total' else 'Count', fontsize=12)
    # ax3.tick_params(axis='x', rotation=45)
    #
    # # Grid for readability
    # ax3.grid(True, linestyle='--', alpha=0.6)
    #
    # st.pyplot(fig3)

    st.header('📈 Month-on-Month (MoM) Graph')

    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['date'] = pd.to_datetime(temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str) + '-01')
    temp_df = temp_df.sort_values('date')

    st.line_chart(temp_df.set_index('date')['amount'])


def load_startup_details(startup):
    st.title(startup)
    st.subheader('Startup Analysis')
    investments = df[df['startup'] == startup].head(1)[['vertical','subvertical','city']]
    st.dataframe(investments,use_container_width=True, hide_index=True)

    st.subheader('All Investments')
    investments = df[df['startup']==startup].head()[['date','investors','round','amount']]
    st.dataframe(investments)



def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df  =df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)

    with col1:
        # biggest investment
        big_series = (
            df[df['investors'].str.contains(investor)]
            .groupby('startup')['amount']
            .sum()
            .sort_values(ascending=False)
            .head()
        )
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots(figsize=(6, 4))  # fixed size
        ax.bar(big_series.index, big_series.values)
        ax.tick_params(axis="x", rotation=30)
        st.pyplot(fig)

    with col2:
        vertical_series = (
            df[df['investors'].str.contains(investor)]
            .groupby('vertical')['amount']
            .sum()
            .sort_values(ascending=False)
            .head()
        )
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots(figsize=(6, 4))  # fixed size (same as bar)
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find StartUp Details')
    if btn2:
        load_investor_details(selected_investor)