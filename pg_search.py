import streamlit as st
from streamlit_player import st_player
from youtubesearchpython import VideosSearch

def app():
	user_input = st.text_input("Query", "singapore psle fraction")
	
	videosSearch = VideosSearch(user_input, limit = 5)

	results = videosSearch.result()
	if len(results['result']) > 0:
		for r in results['result']:
			st_player(r['link'])