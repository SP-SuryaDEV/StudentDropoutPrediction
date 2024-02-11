import streamlit as st
import pandas as pd
from admin import Uploader_UI
from advisor import StudentReportMaker
from student import StudentInformationViewer
from Styles import Style
import base64

st.set_page_config(
    page_title="Student Success Network",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


adding_gif_background = Style(f"""
<style>
.stApp {{
  background-image: url("https://i.gifer.com/2iiB.gif");
  background-size: cover;
  background-position: center;
}}

@keyframes glow {{
    0% {{
        text-shadow: 0 0 10px rgba(0,0,0,0.3);
    }}
    50% {{
        text-shadow: 0 0 20px rgba(0,0,0,0.6), 0 0 30px rgba(0,0,0,0.6);
    }}
    100% {{
        text-shadow: 0 0 10px rgba(0,0,0,0.3);
    }}
}}
</style>
""")

#https://i.gifer.com/J4o.gif

adding_gif_background.run()

st.sidebar.markdown(
    """
    
    <h2 style='font-weight: bold; color: white; font-size: 24px; text-shadow: 0 0 10px rgba(255,255,255,0.6), 
    0 0 20px rgba(255,255,255,0.6), 0 0 30px rgba(255,255,255,0.6);'>Instructions:</h2>
    <hr style='border: 2px solid White;'>

    **For Admins:**
    
    - Your Job is to Upload and process general students Data Using the Portal and provide a General Report and Special Report to the Respective Advisors
    <hr style='border: 1px solid White;'>
    
    **For Advisors:**
    
    - Your Job is to Provide Students With their Own personalized learning tracks and such
    - Further Details are mentioned in your Portal
    <hr style='border: 1px solid White;'>
    
    **For Students:**
    
    - Your Job is to check the portal every day Using the login Credentials
    - There is no need to create accounts as it has been already created for you
    - Please Check Your Mail for your login credentials
    - After entering the portal follow the protocols mentioned over there to access your profile

    <hr style='border: 2px solid White;'>

    **NOTE:**

      Please Note that this website is under extensive development and many contain bugs and sloppy interface at certain junctures if you encounter such bugs contact us through the mail enlisted below

      Support : abc@gmail.com
    """, 
    unsafe_allow_html=True
)


def show_login_page():
    # Add code for your login page UI here
    st.markdown("<h1 style='text-align: center; color: white; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; font-family: Arial, sans-serif; animation: glow 1.5s ease-in-out infinite;'>Student Success Network</h1>", unsafe_allow_html=True)
    roles = ["Student", "Advisor", "Admin"]
    role = st.selectbox("Select Role", roles)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    st.warning("Check The instructions from the side bar at top left corner")
    st.warning("Please Select Your Designated Role and Enter Your Credentials Properly")

    if login_button:
        # Perform login validation based on the selected role
        if role == "Student":
            # Perform student login validation
            if username == "Test" and password == "pass23":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role  # Set the role attribute
                st.experimental_rerun()  # Rerun the script to switch to the next page
        elif role == "Advisor":
            # Perform admin login validation
            if username == "Teach" and password == "pass":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role  # Set the role attribute
                st.experimental_rerun()  # Rerun the script to switch to the next page
        elif role == "Admin":
            # Perform data uploader login validation
            if username == "Admin" and password == "222":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role  # Set the role attribute
                st.experimental_rerun()  # Rerun the script to switch to the next page

# Check if the user is already logged in
if st.session_state.get("logged_in"):
    if st.session_state.username == "Admin":
        st.markdown("<h1 style='text-align: center; color: white; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; font-family: Arial, sans-serif; animation: glow 1.5s ease-in-out infinite;'>Drop the Student's Details Below:</h1>", unsafe_allow_html=True)
        st.warning("Note: The Files Generated in this process need to be sent to the respective advisors")
        data_Updater= Uploader_UI()
        data_Updater.run()   
    
    # Add functionality to upload a CSV file for admins
    if st.session_state.username == "Teach":
        st.success("As an advisor, you can provide personalized recommendations to students based on their needs and provide them with custom learning plans and Learning Materials ")
        review_system = StudentReportMaker()
        review_system.run()
  # Display the contents of the uploaded CSV file

    if st.session_state.username == "Test":  # Fix typo here
        #st.write('<h1 style="font-size: larger; color: #ffffff; text-shadow: 0 0 5px #ffffff, 0 0 10px #ffffff, 0 0 15px #ffffff, 0 0 20px #ffffff, 0 0 25px #ffffff; -webkit-text-stroke: 0.8px black; animation: blink 1s linear infinite;"><span style="color: White;">🔥🔥📚📚<strong>Welcome Champ</strong>📚📚🔥🔥</span></h1>', unsafe_allow_html=True)
        st.write("<h4 style='text-align: left; color: white; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; font-family: Arial, sans-serif; animation: glow 1.5s ease-in-out infinite;'>📚📚Welcome Champ!!📚📚</h4>", unsafe_allow_html=True)
        information = StudentInformationViewer()
        information.run()
    
    if st.button("Log out"):
        st.session_state.logged_in = False
else:
    show_login_page()
