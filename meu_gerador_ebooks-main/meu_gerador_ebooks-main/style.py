import streamlit as st

def set_theme(mode="light"):
    if mode == "dark":
        st.markdown(
            '''
            <style>
            body {
                background-color: #0e1117;
                color: #c7d5e0;
            }
            </style>
            ''', unsafe_allow_html=True
        )
    else:
        st.markdown(
            '''
            <style>
            body {
                background-color: #ffffff;
                color: #000000;
            }
            </style>
            ''', unsafe_allow_html=True
        )