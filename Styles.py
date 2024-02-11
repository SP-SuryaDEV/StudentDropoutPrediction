import streamlit as st 

class Style:
    """
    Class for passing CSS styles to streamlit
    """
    def __init__(self, styles_string):
        """
        Constructor function that accepts a css style string/file and stores it
        """
        self.styles_string = styles_string

    def run(self):
        """
        Runs the style 
        """
        st.markdown(self.styles_string, unsafe_allow_html=True)
