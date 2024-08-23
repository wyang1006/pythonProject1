import streamlit as st
from openai import OpenAI


st.title("FAF Flow Dashboard")

embed_url="https://app.powerbi.com/view?r=eyJrIjoiZTA2YzkyNTItMWFjMS00OTM1LTlmZGQtODdjMmEyMWZjMTc0IiwidCI6ImYyODEwNzRiLTc1MGQtNGM1Zi1iZDQ0LWYzYjg0OTk5NDk3NiIsImMiOjJ9&rs:Fit=True"
st.markdown(
    f"""
    <iframe width="1000" height="600" src="{embed_url}" frameborder="0" allowFullScreen="true"></iframe>
    """,
    unsafe_allow_html=True
)
# Set your API key
api_key="sk-iAym-FFx6dyhI2TBUnhlki4vecSbxKLsxdzrMAnxWzT3BlbkFJH2-hop5WVvs3-X-szYFJLP1JQYdcJbSC2IJXisnLcA"  # Replace with your API key
client=OpenAI(api_key=api_key)
assistant_id="asst_2CNArz6z3k7YC6Y8x3QYrewi"


# Streamlit app title
st.title("FAF FLOW AI-Assisted Chat")

# Initial message
st.markdown("Welcome to the FAF Freight Flow AI Assistant! Ask me anything.")




# Function to call OpenAI's API with assistant ID
def  chat_manager(prompt):
    thread=client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id= thread.id,
        role= "user",
        content= prompt
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id= thread.id,
        assistant_id= assistant_id,
        instructions="Please address the users as 'Dear User'."
    )
    messages=client.beta.threads.messages.list(thread_id=thread.id)
    last_message=messages.data[0]
    response=last_message.content[0].text.value

    return response



# Store chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text input for user query
if prompt := st.chat_input("Ask a question about the data"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    #display user's input
    with st.chat_message("user"):
        st.markdown(prompt)
    # Get response from ChatGPT with assistant ID
    response = chat_manager(prompt)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)