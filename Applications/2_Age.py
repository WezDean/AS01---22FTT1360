import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_csv('guns_cleaned.csv')

# Sidebar filters
st.sidebar.header('Filters')
year_filter = st.sidebar.slider('Select Year:', min_value=df['year'].min(), max_value=df['year'].max())
intent_filter = st.sidebar.selectbox('Select Intent:', df['intent'].unique())
race_filter = st.sidebar.selectbox('Select Race:', df['race'].unique())

# Apply filters to the dataset
filtered_df = df[(df['year'] == year_filter) & (df['intent'] == intent_filter) & (df['race'] == race_filter)]

# Title
st.title('Gun Violence Insights')

# Insights and visualizations
st.subheader('Insights and Visualizations')

# Distribution of victim ages
st.subheader('Distribution of Victim Ages')
plt.figure(figsize=(10, 6))
sns.histplot(filtered_df['age'], bins=20, kde=True, color='skyblue', edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Distribution of Victim Ages')
st.pyplot()

# Additional insights and visualizations can be added here

# Footer
st.sidebar.markdown('Created with ❤️ by Your Name')
