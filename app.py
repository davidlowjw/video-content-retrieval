import streamlit as st

# Custom imports 
from multipage import MultiPage
import pg_example, pg_search

st.set_page_config(layout="wide")

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Video Content Search")

# Add all your applications (pages) here
app.add_page("Keyword Search", pg_search.app)
app.add_page("Video Segmentation", pg_example.app)

# The main app
app.run()