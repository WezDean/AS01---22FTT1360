import streamlit as st 
import pandas as pd 

st.title('Gun Violence in America')
st.markdown('Did you know? Each day 12 children die from gun violence in America. Another 32 are shot and injured.')
st.image("M14.gif", width=500)

st.subheader('Context')
st.markdown('This Application aims to show In-depth Analysis of Gun Violence across America, navigate the sidebar on the left to display visualizations.')
st.write('This application makes use of a dataset which keeps records of gun related deaths in America from the year 2012-2014. The dataset mentioned contained many valuable information to discover insights and patterns to help further understand the topic ')
st.subheader('Acknowledgements')
st.write("This application would not be possible without the help of FiveThirtyEight's Gun Deaths in America project. The data originated from the CDC, and can be found [here.](https://github.com/fivethirtyeight/guns-data)")