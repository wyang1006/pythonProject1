import streamlit as st
import openai

st.title("This is a test")

embed_url="https://app.powerbi.com/view?r=eyJrIjoiZTA2YzkyNTItMWFjMS00OTM1LTlmZGQtODdjMmEyMWZjMTc0IiwidCI6ImYyODEwNzRiLTc1MGQtNGM1Zi1iZDQ0LWYzYjg0OTk5NDk3NiIsImMiOjJ9"
st.markdown(
    f"""
    <iframe width="600" height="373.5" src="{embed_url}" frameborder="0" allowFullScreen="true"></iframe>
    """,
    unsafe_allow_html=True
)
# Set your API key
api_key="sk-iAym-FFx6dyhI2TBUnhlki4vecSbxKLsxdzrMAnxWzT3BlbkFJH2-hop5WVvs3-X-szYFJLP1JQYdcJbSC2IJXisnLcA"  # Replace with your API key
openai.api_key=api_key



# Streamlit app title
st.title("ChatGPT Assistant in Streamlit")

# Initial message
st.markdown("Welcome to the ChatGPT Assistant! Ask me anything.")

# Store chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []


# Function to call OpenAI's API with assistant ID
def get_chatgpt_response_with_assistant_id(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the correct model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        # Ensure the response contains the expected keys
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            return "Unexpected API response format."

    except Exception as e:
        # Log the error and return a friendly message
        st.error(f"An error occurred: {e}")
        return "Sorry, I couldn't process your request."

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text input for user query
if prompt := st.chat_input("Ask a question"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from ChatGPT with assistant ID
    response = get_chatgpt_response_with_assistant_id(prompt)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)