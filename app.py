import streamlit as st
import helpers
import json
import os


if 'first_run' not in st.session_state:
    st.session_state.first_run = True
if st.session_state.first_run:
    helpers.clear_history()
    st.session_state.first_run = False

st.title("Interview Chat")

st.session_state.messages = helpers.load_messages()
for message in st.session_state.messages:
    if message["role"]=="system":
        with st.chat_message("system", avatar="🔮"):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if user_message := st.chat_input("Say something to your interviewer"):
    with st.chat_message("user"):
        # user_message = helpers.get_user_input()
        st.markdown(user_message)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        chat_response = helpers.get_chat_response(user_message)
        st.markdown(chat_response)

