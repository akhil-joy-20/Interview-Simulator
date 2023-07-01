import streamlit as st,subprocess,sys

# Set page title
st.set_page_config(page_title="Home")

username = sys.argv[1] #reading username from previous page
st.write("Userid: "+username)
st.markdown("<h1 style='font-size: 5rem; text-align: center; color: #fff;'>Virtual Interview System</h1><br><br>", unsafe_allow_html=True)

# Add section for instructions
st.header("Instructions")
st.write("Welcome to the virtual interview! Please make sure to follow these instructions:")
st.write("- Turn on your camera before starting the interview.")
st.write("- Sit in a well-lit, quiet room where you will not be interrupted.")
st.write("- Do not use any external devices or materials during the interview.")
st.write("- Be prepared to answer questions about your experience and qualifications.")
st.write("- Be honest and professional throughout the interview.")

st.write("---")

# Add section for resume analyzer
st.markdown("<h1 style='font-size: 2.5rem; text-align: center; color: #fff;'>Round 1: Resume Analyzer</h1><br><br>", unsafe_allow_html=True)
st.write("- Enter your CGPA.")
st.write("- Upload your resume.")
st.write("- We will analyze your resume and assess your qualifications for the position.")

st.markdown("<h1 style='font-size: 2.5rem; text-align: center; color: #fff;'>Round 2: General Interview</h1><br><br>", unsafe_allow_html=True)
st.write("- In this round, we will ask you general questions based on your resume.")

st.markdown("<h1 style='font-size: 2.5rem; text-align: center; color: #fff;'>Round 3: Technical Interview</h1><br><br>", unsafe_allow_html=True)

st.write("- In this round, we will test your technical knowledge and abilities.")
st.write("\n\n\n")
if st.button("START"):
   subprocess.Popen(["streamlit", "run", "resume_analyser.py", "--", username])