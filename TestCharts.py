import streamlit as st
import pandas as pd
import altair as alt

class DonutPieChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Aggregate data by intent
        intent_counts = self.data['intent'].value_counts().reset_index()
        intent_counts.columns = ['intent', 'count']

        # Donut pie chart for intents with a different color scheme
        donut_chart = alt.Chart(intent_counts).mark_arc(innerRadius=50).encode(
            theta='count',
            color=alt.Color('intent:N', scale=alt.Scale(scheme='viridis')),  # Change the color scheme here
            tooltip=['intent', 'count']
        ).properties(
            width=400,
            height=400
        )
        
        return donut_chart

class Histogram:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Year filter
        years = self.data['year'].unique()
        all_years = st.checkbox('All Years', value=True)
        if all_years:
            selected_years = years
        else:
            selected_years = st.multiselect('Select Years:', years, default=years)

        # Intent filter
        intent_options = ['All'] + list(self.data['intent'].unique())
        intent_filter = st.selectbox('Select Intent:', intent_options)

        # Race filter
        race_options = ['All'] + list(self.data['race'].unique())
        race_filter = st.selectbox('Select Race:', race_options)

        # Apply filters to the dataset
        filtered_df = self.data[self.data['year'].isin(selected_years)]

        if intent_filter != 'All':
            filtered_df = filtered_df[filtered_df['intent'] == intent_filter]

        if race_filter != 'All':
            filtered_df = filtered_df[filtered_df['race'] == race_filter]

        # Altair Histogram with rolling mean line overlay
        hist = alt.Chart(filtered_df).mark_bar(interpolate='step').encode(
            alt.X('age:Q', bin=alt.Bin(maxbins=20), title='Age'),
            alt.Y('count():Q', stack=None, title='No. of Victims'),
            color=alt.Color('education:N', scale=alt.Scale(scheme='set1'), legend=alt.Legend(orient='left')),  # Set legend orientation to left
            tooltip=['education:N']  # Add tooltip for education
        ).properties(
            width=500,  # Set width to 600 pixels
            height=400  # Set height to 400 pixels
        )

        return hist

class IntentRaceBarChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Aggregate data by intent and race
        intent_race_counts = self.data.groupby(['intent', 'race']).size().reset_index(name = 'count')

        bar_chart = alt.Chart(intent_race_counts).mark_bar().encode(
            x=alt.X('count:Q', title='Count'),
            y=alt.Y('race:N', sort='-x', title='Race'),
            color=alt.Color('intent:N', scale=alt.Scale(scheme='plasma')),  # Change the color scheme here
            tooltip=['intent', 'race', 'count']
        ).properties(
            width=700,  
            height=400 
        )

        return bar_chart

class GenderPieChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Calculate male and female counts
        gender_counts = self.data['sex'].value_counts()
        
        # Create a DataFrame from the counts
        gender_df = pd.DataFrame({
            'Gender': gender_counts.index,
            'Count': gender_counts.values
        })
        
        # Create a pie chart using Altair
        pie_chart = alt.Chart(gender_df).mark_arc().encode(
            color=alt.Color('Gender', scale=alt.Scale(scheme='category10')),
            tooltip=['Gender', 'Count'],
            theta='Count'
        ).properties(
            width=400,
            height=400
        )
        
        return pie_chart
    

# Load the cleaned dataset
df = pd.read_csv('guns_cleaned.csv')

# Instances of Visualizaitions
donut_chart = DonutPieChart(df)
histogram = Histogram(df)
barchart = IntentRaceBarChart(df)
gender_pie_chart = GenderPieChart(df)

# Display all visualizations side by side using Streamlit columns
col1, col2 = st.columns(2)

with col1:
    st.caption("Education Level Chart")
    hist_chart = histogram.generate_chart()
    st.altair_chart(hist_chart, use_container_width=True)

with col2:
    st.caption("Overall Races")
    donut_chart = donut_chart.generate_chart()
    st.altair_chart(donut_chart, use_container_width=True)

    st.caption("Male to Female Ratio")
    pie_chart = gender_pie_chart.generate_chart()
    st.altair_chart(pie_chart, use_container_width=True)

col3, _ = st.columns(2)
with col3:
    st.caption("Age & Intents Bar Chart")
    scatter_plot = barchart.generate_chart()
    st.altair_chart(scatter_plot, use_container_width=False)

histogram = Histogram(df)