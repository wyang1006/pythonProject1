import streamlit as st

st.title("This is a test")
button=st.button

if button('CLICK'):
    st.write('Welcome')

embed_url="https://app.powerbi.com/view?r=eyJrIjoiZTA2YzkyNTItMWFjMS00OTM1LTlmZGQtODdjMmEyMWZjMTc0IiwidCI6ImYyODEwNzRiLTc1MGQtNGM1Zi1iZDQ0LWYzYjg0OTk5NDk3NiIsImMiOjJ9"
st.markdown(
    f"""
    <iframe width="600" height="373.5" src="{embed_url}" frameborder="0" allowFullScreen="true"></iframe>
    """,
    unsafe_allow_html=True
)