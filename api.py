import streamlit as st
from openai import OpenAI





# Set your API key
api_key="sk-iAym-FFx6dyhI2TBUnhlki4vecSbxKLsxdzrMAnxWzT3BlbkFJH2-hop5WVvs3-X-szYFJLP1JQYdcJbSC2IJXisnLcA"  # Replace with your API key
client=OpenAI(api_key=api_key)
assistant_id="asst_2CNArz6z3k7YC6Y8x3QYrewi"
st.set_page_config(
    page_title="FAF Disaggregated Freight Flow APP",  # Title of the tab in the browser
    page_icon="🚚",  # Emoji or path to an image file to use as the favicon
    layout="wide",  # Can be "centered" or "wide"
)

# Custom CSS to adjust the layout
# st.markdown(
#     """
#     <style>
#     /* Adjust the width of the sidebar */
#     .css-1d391kg {  /* This class targets the sidebar */
#         width: 10% !important;  /* Adjust the width percentage as needed */
#     }
#
#     /* Adjust the width of the main content */
#     .css-1gkypgm {  /* This class targets the main content area */
#         max-width: 85% !important;  /* Adjust the width percentage as needed */
#         margin-left: 10%;  /* This shifts the content to fill the gap */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
st.markdown(
    """
    <h1 style="text-align: center;">FAF Interactive Tool</h1>
    """,
    unsafe_allow_html=True
)
sb=st.sidebar.title('Navigation')
page=st.sidebar.selectbox("Choose A Section",["Freight Flow Dashboard","AI-Assisted Chat"])
if page == "Freight Flow Dashboard":
    st.header("Disaggregated Freight Flow Dashboard")
    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiZTQ4MWEyMzQtZmY2ZC00ZWUzLThmNzItN2JjMmUzNTU4YzAyIiwidCI6ImYyODEwNzRiLTc1MGQtNGM1Zi1iZDQ0LWYzYjg0OTk5NDk3NiIsImMiOjJ9"
    # fit_to_page_url = f"{embed_url}&rs:embed=true&$filter=fitToWidth"

    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <iframe src="{embed_url}" width="1100" height="720" style="border:none;"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.header("FAF Freight Flow AI-Assisted Chat")

    # Initial message
    st.markdown("Welcome to the FAF Freight Flow AI Assistant!")
    st.markdown("The dataset contains the following columns:")
    st.markdown("""
    - 'Origin': all Florida counties
    - 'Destination': all Florida counties
    - 'Year': 2020 and 2050
    - 'Commodity': 12 commodity types
    - 'Tonnage': numerical tons""")


    # function to call assistant API

    def chat_manager(conversation_history):
        # only refer to the last 3 messages
        recent_history = conversation_history[-4:]
        # Create a new thread for each conversation
        thread = client.beta.threads.create()

        # Add all the messages in the conversation history to the thread
        for message in recent_history:
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role=message["role"],
                content=message["content"]
            )

        # Generate a response from the assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions="Please address the users as 'Dear User'."
        )

        # Retrieve the last message from the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0]  # Get the last message from the list

        response_text = ""
        response_image = None
        response_file = None

        # return text or chart
        for m in last_message.content:
            if m.type == "image_file":
                image_file_id = m.image_file.file_id
                image_data = client.files.content(image_file_id)
                image_bytes = image_data.read()
                response_image = image_bytes

            elif m.text.annotations:
                file_path = m.text.annotations[0].text
                file_name = file_path.split("/")[-1]
                file_id = m.text.annotations[0].file_path.file_id

                file_data = client.files.content(file_id)
                file_content = file_data.read()
                response_file={"name":file_name,"content":file_content}
                response_text = m.text.value.split(":")[0]





            else:
                response_text = m.text.value

        return response_image, response_text, response_file
        



    # Initialize the chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("image"):
                st.image(message["image"])
            if message.get("file"):
                st.download_button(label = f"Download {message['file']['name']}",
                                   data = message['file']['content'],
                                   file_name= message['file']['name'])


    # Text input for user query
    if prompt := st.chat_input("Start here! Ask a question about the data"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user's input
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare the full conversation history for the API request
        conversation_history = st.session_state.messages

        response_image, response_text,response_file = chat_manager(conversation_history)

        response_content = {"role": "assistant", "content": response_text}
        if response_image:
            response_content["image"] = response_image
        if response_file:
            response_content["file"] = response_file

        # Add combined assistant response to history
        st.session_state.messages.append(response_content)

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response_text)
            if response_image:
                st.image(response_image)
            if response_file:
                st.download_button(label= f"Download {response_file['name']}",
                                   data = response_file['content'],
                                   file_name = response_file['name'])
                

# 