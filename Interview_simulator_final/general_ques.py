from imports import st,sys,cv2,np,load_model,time,pm,dbconn,json,subprocess

st.set_page_config(
   page_title="Round 2"
)

#general ques
username = sys.argv[1] #getting username from previous page

st.write("Userid: "+username)
st.markdown("<h1 style='font-size: 4rem; text-align: center; color: #fff;'>Round 2<br> General Interview</h1><br><br>", unsafe_allow_html=True)

conn= dbconn()
cur = conn.cursor()

# Create the grneral table
cur.execute("""
CREATE TABLE IF NOT EXISTS f_hr (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    degree VARCHAR(255) NOT NULL,
    internship ENUM('Yes', 'No') NOT NULL,
    internship_desc TEXT,
    project ENUM('Yes', 'No') NOT NULL,
    project_relevance ENUM('Not relevant', 'Somewhat relevant', 'Very relevant'),
    project_desc TEXT,
    strengths TEXT,
    weaknesses TEXT,
    PRIMARY KEY (id),
    UNIQUE KEY username (username)
)
""")

degree = st.selectbox("What is your highest education level?", ["High School", "Bachelors Degree", "Masters Degree", "PhD"])
strengths = st.multiselect("What are your strengths?", ["Teamwork", "Leadership", "Problem Solving", "Communication", "Technical Skills"])
weaknesses = st.multiselect("What are your weaknesses?", ["Perfectionism", "Procrastination", "Public Speaking", "Attention to Detail"])
internship = st.radio("Have you done any internships before?", ["No", "Yes"])
if internship == "Yes":
    internship_desc = st.text_input("Please describe your internship experience.")
else:
    internship_desc = ""
project = st.radio("Have you completed any projects?", ["No", "Yes"])
if project == "Yes":
    project_relevance = st.selectbox("How relevant is your project to the job you are applying for?", ["Not relevant", "Somewhat relevant", "Very relevant"])
    project_desc = st.text_input("Please describe your project.")
else:
    project_relevance = ""
    project_desc = ""

#general ques end

#************************************************************************************************************

#db insertion
if st.button("Submit"):
    strengths_str = ', '.join(strengths)
    weaknesses_str = ', '.join(weaknesses)
    query = f"INSERT INTO f_hr (username, degree, internship, internship_desc, project, project_relevance, project_desc, strengths, weaknesses) VALUES ('{username}', '{degree}', '{internship}', '{internship_desc}', '{project}', '{project_relevance}', '{project_desc}', '{strengths_str}', '{weaknesses_str}') ON DUPLICATE KEY UPDATE degree='{degree}', internship='{internship}', internship_desc='{internship_desc}', project='{project}', project_relevance='{project_relevance}', project_desc='{project_desc}', strengths='{strengths_str}', weaknesses='{weaknesses_str}'"
    cur.execute(query)
    conn.commit()
    st.success("Your responses have been saved.")

    subprocess.Popen(["streamlit", "run", "tech_int.py","--",username])

# Close the connection to the database
conn.close()