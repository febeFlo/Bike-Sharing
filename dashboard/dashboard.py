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

def get_total_casual_per_month(day_df):
    casual_df = day_df.groupby('mnth')['casual'].count()
    return casual_df

def get_total_registered_per_month(day_df):
    registered_df = day_df.groupby('mnth')['registered'].count()
    return registered_df

day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

datetime_columns = ['dteday']
day_df.sort_values(by='dteday', inplace=True)
day_df.reset_index(inplace=True)
# hour_df.sort_values(by='dteday', inplace=True)
# hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    # hour_df[column] = pd.to_datetime(hour_df[column])

min_date_day = day_df['dteday'].min()
max_date_day = day_df['dteday'].max()

# min_date_hour = day_df['dteday'].min()
# max_date_hour = day_df['dteday'].max()
 
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
casual_df = get_total_casual_per_month(main_df_day)
registered_df = get_total_registered_per_month(main_df_day)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Monthly Sharing Hours')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_rent = hour_per_month.hr.sum()
    st.metric("Total Hours", value=total_rent)
 
with col2:
    total_reg = registered_df.registered.sum()
    st.metric("Total Registered", value=total_reg)

with col3:
    total_cas = casual_df.casual.sum() 
    st.metric("Total Casual", value=total_cas)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["dteday"],
    day_df["hr"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Best & Worst Performing Rent Base on Season")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="hr", y="season", data=rent_per_season.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Rent", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="hr", y="season", data=rent_per_season.sort_values(by="hr", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Rent", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

