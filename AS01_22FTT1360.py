import streamlit as st
import pandas as pd

# Load your dataset
# Assuming your dataset is in a CSV file named 'gun_violence_data.csv'
df = pd.read_csv('gun_violence_data.csv')

# Sidebar filters
st.sidebar.header('Filters')
year_filter = st.sidebar.slider('Select Year:', min_value=df['year'].min(), max_value=df['year'].max())
intent_filter = st.sidebar.selectbox('Select Intent:', df['intent'].unique())
race_filter = st.sidebar.selectbox('Select Race:', df['race'].unique())

# Apply filters to the dataset
filtered_df = df[(df['year'] == year_filter) & (df['intent'] == intent_filter) & (df['race'] == race_filter)]

# Main content
st.title('Gun Violence Insights')

# Display filtered data
st.subheader('Filtered Data:')
st.dataframe(filtered_df)

# Insights and visualizations
st.subheader('Insights and Visualizations')

# Example visualization: Bar chart of incidents by month
monthly_incidents = filtered_df.groupby('month')['Unnamed: 0'].count()
st.bar_chart(monthly_incidents)

# Additional components and insights can be added based on your requirements

# Footer
st.sidebar.markdown('Created with ❤️ by Waiz')

# Run the app with streamlit run gun_violence_app.py in your terminal
