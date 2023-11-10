import streamlit as st
from io import StringIO
from vectors import *
import response
from streamlit_chat import message
from utils2 import get_initial_message, get_chatgpt_response, update_chat
import response
from utils import *

# Initialize session state
if 'corpusData' not in st.session_state:
    st.session_state['corpusData'] = None

if 'index' not in st.session_state:
    st.session_state['index'] = None

if 'store_context' not in st.session_state:
    st.session_state['store_context'] = None

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

st.header("Web scraping & Semantic search - Ver2")

url = False
query = False

options = st.radio(
    'Select below options', ('Update the Database', 'Ask me'))

if 'Update the Database' in options:
    url = st.text_input("Enter the url of the document")
    button = st.button("Submit")

if 'Ask me' in options:
    query = st.text_input("Type your query here")

if 'Update the Database' in options and button and url:
    with st.spinner("In progress..."):
        website_scraping(url)
        dir = "C:/Users/vamsh/Desktop/NLP/chatBot-AI-Final/Data"
        print('Scan the directory')
        ind = create_index_llama(dir)
        query_engine(ind)
        st.session_state['store_context'] = save_index1(ind)
        st.success("Database updated")

if 'Ask me' in options and query:
    with st.spinner("Searching for Answer..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        sto_con = st.session_state['store_context']
        answer = load_reply_index1(sto_con,query)
        #print('Final answer -',answer)
        messages = update_chat(messages, "assistant", answer)
        st.session_state.past.append(query)
        st.session_state.generated.append(answer)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
