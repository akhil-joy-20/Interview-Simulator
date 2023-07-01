from imports import st,dbconn,pd,subprocess

st.markdown("<h1 style='font-size: 4rem; text-align: center; color: #fff;'>ADMIN</h1><br><br>", unsafe_allow_html=True)

conn = dbconn()
cur = conn.cursor()

cur.execute("""
SELECT f_user_data.*, 
       f_resume_data.resume_score AS resume_score,          #TO AVOID DUPLICATE COLOUMN NAMES
       f_hr.degree AS degree, 
       f_hr.internship AS internship, 
       f_hr.internship_desc AS internship_desc, 
       f_hr.project AS project, 
       f_hr.project_relevance AS project_relevance, 
       f_hr.project_desc AS project_desc, 
       f_hr.strengths AS strengths, 
       f_hr.weaknesses AS weaknesses, 
       f_emotion.emotion_score AS emotion_score, 
       f_tech.tech_score AS tech_score, 
       f_final.final_score AS final_score
FROM f_user_data
LEFT JOIN f_resume_data ON f_user_data.username = f_resume_data.username
LEFT JOIN f_emotion ON f_user_data.username = f_emotion.username
LEFT JOIN f_hr ON f_user_data.username = f_hr.username
LEFT JOIN f_tech ON f_user_data.username = f_tech.username
LEFT JOIN f_final ON f_user_data.username = f_final.username
ORDER BY f_final.final_score DESC
""")

# Fetch all the rows of the result set
results = cur.fetchall()

# Convert the results to a pandas DataFrame
df = pd.DataFrame(results, columns=[i[0] for i in cur.description])

# Display the results in a Streamlit app in a tabular form
st.write(df)

# Close the cursor and connection
cur.close()
conn.close()

if st.button("Log out"):
    subprocess.Popen(["streamlit", "run", "login.py",])