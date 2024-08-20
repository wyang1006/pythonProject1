import streamlit as st

st.title("This is a test")
button=st.button

if button('CLICK'):
    st.write('Welcome')

st.markdown("https://app.powerbi.com/view?r=eyJrIjoiZTA2YzkyNTItMWFjMS00OTM1LTlmZGQtODdjMmEyMWZjMTc0IiwidCI6ImYyODEwNzRiLTc1MGQtNGM1Zi1iZDQ0LWYzYjg0OTk5NDk3NiIsImMiOjJ9",unsafe_allow_html=Ture)