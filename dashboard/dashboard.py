import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_hour_per_month(hour_df):
    hour_per_month = hour_df.groupby('mnth')['hr'].sum()
    return hour_per_month

def get_total_rent_per_season(day_df):
    rent_per_season = day_df.groupby('season')['instant'].count()
    return rent_per_season

def get_total_renter(day_df):
    registered_df = day_df['registered'].count()
    return registered_df

day_df = pd.read_csv('./dashboard/day.csv')
hour_df = pd.read_csv('./dashboard/hour.csv')

datetime_columns = ['dteday']
day_df.sort_values(by='dteday', inplace=True)
day_df.reset_index(inplace=True)
hour_df.sort_values(by='dteday', inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date_day = day_df['dteday'].min()
max_date_day = day_df['dteday'].max()

min_date_hour = day_df['dteday'].min()
max_date_hour = day_df['dteday'].max()
 
with st.sidebar:
    st.image('https://i.pinimg.com/550x/31/7e/e1/317ee1c243497fb0d51cf40842e2ecfa.jpg')
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )

main_df_day = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

hour_per_month =  get_total_hour_per_month(main_df_hour)
rent_per_season = get_total_rent_per_season(main_df_day)
registered_df = get_total_renter(main_df_day)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Monthly Sharing Hours')
 
col1, col2 = st.columns(2)
 
with col1:
    total_rent = hour_per_month.sum()
    st.metric("Total Hours", value=total_rent)
 
with col2:
    total_renter = registered_df.sum()
    st.metric("Total Renter", value=total_renter)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    ['January', 'February', 'March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    hour_per_month,
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Best Performing Rent Base on Season")
fig, ax = plt.subplots(nrows=1, figsize=(35, 15))
colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"]
rent_per_season_df = pd.DataFrame({'season': rent_per_season.index, 'hr': rent_per_season.values})
rent_per_season_df.season.replace((1,2,3,4), ('Semi', 'Panas', 'Gugur', 'Salju'), inplace=True)

sns.barplot(x="hr", y="season", data=rent_per_season_df, palette=colors)
ax.set_ylabel(None)
ax.set_xlabel("Number of Rent", fontsize=30)
ax.set_title("Best Performing Months", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="hr", y="season", data=rent_per_season_df, palette=colors)
ax.set_ylabel(None)
ax.set_xlabel("Number of Rent", fontsize=30)
ax.set_title("Worst Performing Months", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

