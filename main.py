import  streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_csv("26_social_media_screentime_mental_health.csv")
#Step 1: Page configuration
st.set_page_config(
    page_title="Digipulse: Digital Well-being Dashboard",
    page_icon="📱",
    layout="wide"
)
st.title("📱 Digipulse: Social Media & Mental Well-being Analytics")
st.write("Explore how screen time,platform habits, and digital behaviours correlate with mental health metrices.")
# Step 2: Sidebar Filters
st.sidebar.header("Filter Options")
#Filter 1: Gender(dropdown)
gender_options=["All"]+list(df["gender"].unique())
selected_gender=st.sidebar.selectbox("Select Gender",gender_options)
#Filter 2: Age Range(slider)
min_age=int(df["age"].min())
max_age=int(df["age"].max())
selected_age_range=st.sidebar.slider("Select Age Range",min_age,max_age,(min_age,max_age))
#Filter 3: Primary Platform(multiselect)
platform_options=list(df["most_used_platform"].unique())
selected_platforms=st.sidebar.multiselect("Select Platforms",platform_options,default=platform_options)
#--- Apply Filters to the Dataframe---
filtered_df=df[
    (df["age"] >= selected_age_range[0]) &
    (df["age"] <= selected_age_range[1]) &
    (df["most_used_platform"].isin(selected_platforms))
]
if selected_gender !="All":
    filtered_df=filtered_df[filtered_df["gender"]==selected_gender]

# print(filtered_df.shape)
# Step 3: Key Metrices
st.subheader("📊 Key Performance Indicators(KPIs)")
# Create 4 columns for layout
col1,col2,col3=st.columns(3)
with col1:
    avg_screen_time=round(filtered_df["daily_screen_hours"].mean(),1)
    st.metric(label="Avg Screen Time",value=f"{avg_screen_time} hrs")
with col2:
    avg_sleep=round(filtered_df["avg_sleep_hours"].mean(),1)
    st.metric(label="Avg Sleep Duration",value=f"{avg_sleep} hrs")
with col3:
    avg_anxiety=round(filtered_df["anxiety_score_0to27"].mean(),1)
    st.metric(label="Avg Anxiety Score",value=f"{avg_anxiety} / 27")

# Step 4: Charts & Visualizations
st.write("---")#Visual Separation line
st.subheader("📈 Insights & Visualizations")
#Create two columns for side-by-side charts
chart_col1,chart_col2=st.columns([2,3])
with chart_col1:
    st.write("### Primary Purpose of Use")
    purpose_counts=filtered_df["primary_purpose"].value_counts()
    if not purpose_counts.empty:
        fig,ax=plt.subplots(figsize=(7,7.5))
        ax.pie(purpose_counts,labels=purpose_counts.index,autopct="%1.1f%%",startangle=90,colors=["#ff9999","#6bbffa","#6b5f8b","#20c43b"])
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")
# CHART 2    
with chart_col2:
    st.write("### Top Most Used Platforms")
    platform_counts=filtered_df["most_used_platform"].value_counts()
    if not purpose_counts.empty:
        fig,ax=plt.subplots(figsize=(7,3.4))
        ax.bar(platform_counts.index,platform_counts.values,color="skyblue",edgecolor="black")
        ax.set_xlabel("Platform")
        ax.set_ylabel("Count") 
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")
st.write("---")

# Chart 3 : Line/Trend plo
st.write("### Daily Screen Hours vs. Life Satisfaction ")
# Sorting data by screen hours to see if a trend exists
trend_df=filtered_df.groupby("daily_screen_hours")["life_satisfaction_1to10"].mean().reset_index()
if not trend_df.empty:
    fig,ax=plt.subplots(figsize=(10,4))
    ax.plot(trend_df["daily_screen_hours"],trend_df["life_satisfaction_1to10"],marker="o",color="purple",linestyle="-")
    ax.set_xlabel("Daily Screen Hours")
    ax.set_ylabel("Avg Life Satisfaction (1-10)")
    ax.grid("True",linestyle="--",alpha=0.6)
    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")

st.write("---")
st.subheader("🌍 Regional Screen Time Analysis")
#1.Calculate the avg daily screen hours for each region
region_screen_time=(filtered_df.groupby("region")["daily_screen_hours"].mean().sort_values(ascending=True))
if not region_screen_time.empty:
# Set up a layout with text on left and chart on the right
    text_col,chart_col=st.columns([1,2])
    with text_col:
        st.write("### ⌚ Usage at a Glance")
        st.markdown("This breakdown reveals regional gaps in daily device engagement.")
        highest_region=region_screen_time.index[-1]
        highest_value=round(region_screen_time.values[-1],1)
        lowest_region=region_screen_time.index[0]
        lowest_value=round(region_screen_time.values[0],1)
        st.warning(f"**Highest Usage :** {highest_region}({highest_value} hrs/day)")
        st.success(f"**Lowest Usage :** {lowest_region}({lowest_value} hrs/day)")
    with chart_col:
        #2. Build the Matplotlib horizontal bar chart 
        fig,ax=plt.subplots(figsize=(7,3))
        bars=ax.barh(
            region_screen_time.index,region_screen_time.values,color="#9bc4e5",edgecolor="#1c7ed6",height=0.6
        )
        ax.set_xlabel("Average Daily Screen Hours",fontsize=11)
        ax.set_title("Average Screen Time per Day by Region",fontsize=13,pad=15)
        # ax.spines["top"].set_visible(False)
        # ax.spines["right"].set_visible(False)
        st.pyplot(fig)
else:
    st.warning("No regional data available for the current selected filters.")
st.write("---")
st.subheader("🛡 Proactive Coping vs. Professional Support")
col_detox,col_support=st.columns(2)
#---- Column 1
with col_detox:
    st.write("### Attempted a Digital Detox?")
    detox_counts=filtered_df["attempted_digital_detox"].value_counts()
    #print(detox_counts)
    if not detox_counts.empty:
        fig,ax=plt.subplots(figsize=(5,3.5))
        bars=ax.bar(detox_counts.index,detox_counts.values,color="#a3ce93",edgecolor="#27523d",width=0.4)
        ax.set_ylabel("Count")
        # ax.spines["top"].set_visible(False)
        # ax.spines["right"].set_visible(False)
        st.pyplot(fig)
    else:
        st.warning("No detox data available.")
# Column 2
with col_support:
    st.write("### 🩺 Seeks Mental Health Suppport?")
    support_counts=filtered_df["seeks_mental_health_support"].value_counts()
    #print(support_counts)
    if not support_counts.empty:
        fig,ax=plt.subplots(figsize=(5,3.5))
        bars=ax.bar(support_counts.index,support_counts.values,color="#e6bcdb",edgecolor="#91176c",width=0.4)
        ax.set_ylabel("Count")
        # ax.spines["top"].set_visible(False)
        # ax.spines["right"].set_visible(False)
        st.pyplot(fig)
    else:
        st.warning("No support data available.")

