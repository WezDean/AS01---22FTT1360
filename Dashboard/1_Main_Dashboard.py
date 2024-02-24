import streamlit as st
import pandas as pd
import altair as alt
st.set_page_config(page_title="Gun Violence in America" ,layout="wide")

st.title("Gun Violence in America Analysis")
st.caption('Did you know? Each day 12 children die from gun violence in America. Another 32 are shot and injured.')

col1, col2 = st.columns(2)

with col1:
    st.caption(' ')
    st.image('gunfiring.gif')

with col2:
    st.subheader('Context')
    st.caption('This dataset includes information about gun-death in the US in the years 2012-2014.')
    st.subheader('Content')
    st.caption("The data includes data regarding the victim's age, sex, race, education, intent, time (month and year) and place of death, and whether or not police was at the place of death.")
    st.subheader('Acknowledgments')
    st.caption("This Web Application was made possible by [FiveThirtyEight's Gun Deaths in America project](https://fivethirtyeight.com/features/gun-deaths/).")

class AgeDistributionByRaceChart:
    def __init__(self, data):
        self.data = data
        self.race_options = None
        self.age_range = None
        self.bin_size = 30
        
    def apply_filters(self):
        filtered_data = self.data.copy()
        if self.race_options:
            filtered_data = filtered_data[filtered_data['race'].isin(self.race_options)]
        if self.age_range:
            filtered_data = filtered_data[(filtered_data['age'] >= self.age_range[0]) & (filtered_data['age'] <= self.age_range[1])]
        return filtered_data
        
    def generate_chart(self):
        filtered_data = self.apply_filters()

        chart = alt.Chart(filtered_data).mark_bar(opacity=0.7).encode(
            x=alt.X('age:Q', bin=alt.Bin(maxbins=self.bin_size), title='Age'),
            y=alt.Y('count():Q', stack=None, title='Number of Victims'),
            color='race:N',
            tooltip=['race:N', 'age:Q']
        ).properties(
            width=600,
            height=400,
            title='Age Distribution of Victims by Race'
        ).interactive()

        return chart

class DonutPieChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Filtered dataset based on location and time
        place_filter = st.selectbox('Select Place:', ['All'] + list(self.data['place'].unique()), key='place_filter')
        year_filter = st.selectbox('Select Year:', ['All'] + sorted(self.data['year'].unique()), key='year_filter')
        
        filtered_df = self.data
        if place_filter != 'All':
            filtered_df = filtered_df[filtered_df['place'] == place_filter]
        if year_filter != 'All':
            filtered_df = filtered_df[filtered_df['year'] == year_filter]

        # Aggregate data by intent
        intent_counts = filtered_df['intent'].value_counts().reset_index()
        intent_counts.columns = ['intent', 'count']

        # Donut pie chart for intents with a different color scheme
        donut_chart = alt.Chart(intent_counts).mark_arc(innerRadius=50).encode(
            theta='count',
            color=alt.Color('intent:N', scale=alt.Scale(scheme='Tableau10')),  # Change the color scheme here
            tooltip=['intent', 'count']
        ).properties(
            width=400,
            height=400
        )
        
        return donut_chart

class AgeHistogram:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Age filter using a slider
        min_age = int(self.data['age'].min())
        max_age = int(self.data['age'].max())
        age_range = st.slider('Select Age Range:', min_value=min_age, max_value=max_age, value=(min_age, max_age))

        # Intent filter
        intent_options = ['All'] + list(self.data['intent'].unique())
        intent_filter = st.selectbox('Select Intent:', intent_options)

        # Race filter
        race_options = ['All'] + list(self.data['race'].unique())
        race_filter = st.selectbox('Select Race:', race_options)

        # Apply filters to the dataset
        filtered_df = self.data[(self.data['age'] >= age_range[0]) & (self.data['age'] <= age_range[1])]

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

class TimeSeriesLinePlot:
    def __init__(self, data):
        self.data = data
        self.location_filter = None
        self.intent_filter = None
        
    def apply_filters(self):
        filtered_data = self.data.copy()
        if self.location_filter and self.location_filter != 'All':
            filtered_data = filtered_data[filtered_data['place'] == self.location_filter]
        if self.intent_filter and self.intent_filter != 'All':
            filtered_data = filtered_data[filtered_data['intent'] == self.intent_filter]
        return filtered_data
        
    def generate_chart(self):
        filtered_data = self.apply_filters()

        # Combine 'year' and 'month' columns into a single datetime column
        filtered_data['Date'] = pd.to_datetime(filtered_data['year'].astype(str) + '-' + filtered_data['month'].astype(str), format='%Y-%m')

        # Calculate the count of gun deaths over time
        gun_deaths_over_time = filtered_data.groupby('Date').size().reset_index(name='count')

        # Create a time series line plot using Altair
        line_plot = alt.Chart(gun_deaths_over_time).mark_line(color='darkorange', point=True).encode(
            x='Date:T',
            y=alt.Y('count:Q', scale=alt.Scale(domain=('0', '3200'))),
        ).properties(
            width=800,
            height=400,
            title='Trend in Gun Deaths Over Months'
        )

        return line_plot

class GunDeathTrendByIntentOverTime:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        year_range = st.slider('Select Year Range:', min_value=2012, max_value=2014, value=(2012, 2014), key='year_range_slider')
        
        intent_options = ['All'] + list(self.data['intent'].unique())
        selected_intents = st.multiselect('Select Intents:', intent_options, default=['All'], key='intent_multiselect')

        # Filter data based on selected filters
        filtered_data = self.data.copy()
        filtered_data['Date'] = pd.to_datetime(filtered_data['year'].astype(str) + '-' + filtered_data['month'].astype(str), format='%Y-%m')
        filtered_data = filtered_data[(filtered_data['Date'].dt.year >= year_range[0]) & (filtered_data['Date'].dt.year <= year_range[1])]
        if 'All' not in selected_intents:
            filtered_data = filtered_data[filtered_data['intent'].isin(selected_intents)]

        # Calculate the count of gun deaths over time by intent
        gun_deaths_over_time = filtered_data.groupby(['Date', 'intent']).size().reset_index(name='count')

        # Create a stacked area chart using Altair
        stacked_area_chart = alt.Chart(gun_deaths_over_time).mark_area().encode(
            x='Date:T',
            y='count:Q',
            color='intent:N',
            tooltip=['Date:T', 'intent:N', 'count:Q']
        ).properties(
            width=800,
            height=400,
            title='Gun Death Trend by Intent Over Time'
        )

        return stacked_area_chart

class LocationIntentDistributionChart:
    def __init__(self, data):
        self.data = data
        
    def generate_chart(self):
        # Relevant filters
        location_options = ['All'] + list(self.data['place'].unique())
        selected_location = st.selectbox('Select Location:', location_options, index=0, key='location_filter')
        
        intent_options = ['All'] + list(self.data['intent'].unique())
        selected_intents = st.multiselect('Select Intents:', intent_options, default=['All'], key='intent_filter')
        
        # Apply filters to the dataset
        filtered_df = self.data.copy()
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['place'] == selected_location]
        if 'All' not in selected_intents:
            filtered_df = filtered_df[filtered_df['intent'].isin(selected_intents)]

        # Aggregate data by location and intent
        location_intent_counts = filtered_df.groupby(['place', 'intent']).size().reset_index(name='count')

        # Create stacked bar chart
        stacked_bar_chart = alt.Chart(location_intent_counts).mark_bar().encode(
            x=alt.X('place:N', title='Location'),
            y=alt.Y('count:Q', title='Count'),
            color=alt.Color('intent:N', scale=alt.Scale(scheme='category10'), title='Intent'),
            tooltip=['place', 'intent', 'count']
        ).properties(
            width=700,
            height=400,
            title='Gun Violence Incidents by Location and Intent'
        )

        return stacked_bar_chart

# Load the cleaned dataset
df = pd.read_csv('guns_cleaned.csv')

# Instances of each class
time_chart = TimeSeriesLinePlot(df)
donut_chart = DonutPieChart(df)
age_race_chart = AgeDistributionByRaceChart(df)
histogram = AgeHistogram(df)
location_intent_chart = LocationIntentDistributionChart(df)
trend_chart = GunDeathTrendByIntentOverTime(df)

# Displaying Each Visualization

# Filter Options for Age Distribution of Victims by Race
age_race_chart.race_options = st.multiselect('Select Race(s):', df['race'].unique(), key='race_options')
age_range_key = hash('age_range_slider')  # Generate a unique key for the age range slider
age_race_chart.age_range = st.slider('Select Age Range:', min_value=df['age'].min(), max_value=df['age'].max(), value=(df['age'].min(), df['age'].max()), key=age_range_key)
bin_size_key = hash('bin_size_slider')  # Generate a unique key for the bin size slider
age_race_chart.bin_size = st.slider('Select Bin Size:', min_value=5, max_value=50, value=30, key=bin_size_key)

st.caption("Age Distribution of Victims by Race")
age_race_chart = age_race_chart.generate_chart()
st.altair_chart(age_race_chart, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.caption("Location & Intent")
    donut_chart = donut_chart.generate_chart()
    st.altair_chart(donut_chart, use_container_width=True)

with col4:
    st.caption("Education Level Chart")
    hist_chart = histogram.generate_chart()
    st.altair_chart(hist_chart, use_container_width=True)

# Filter Options for Trend Over Months
location_key = 'Location Filter'  # Unique key for location filter
intent_key = 'Intent Filter'  # Unique key for intent filter
time_chart.location_filter = st.selectbox('Select Location:', ['All'] + list(df['place'].unique()), key=location_key)
time_chart.intent_filter = st.selectbox('Select Intent:', ['All'] + list(df['intent'].unique()), key=intent_key)

st.caption("Trend Over Months")
time_chart = time_chart.generate_chart()
st.altair_chart(time_chart, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    st.caption('Gun Violence Incidents by Location and Intent')
    bar_chart = location_intent_chart.generate_chart()
    st.altair_chart(bar_chart, use_container_width=True)

with col6:
    st.caption('Gun Death Trend by Intent Over Time')
    trend_chart = trend_chart.generate_chart()
    st.altair_chart(trend_chart, use_container_width=True)