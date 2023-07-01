from imports import st,sys,dbconn,subprocess



username = sys.argv[1] #getting data from previous page

st.write("userid:",username)
st.markdown("<h1 style='font-size: 4rem; text-align: center; color: #fff;'>Final Score</h1><br><br>", unsafe_allow_html=True)

conn= dbconn()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS f_final (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    final_score VARCHAR(8) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY username (username)
)
""")

cur.execute('SELECT resume_score FROM f_resume_data WHERE username = %s', username)
result = cur.fetchone()
resume_score = result[0]
st.write("Resume score: ",resume_score,"/100")
resume_score = float(resume_score)

cur.execute('SELECT emotion_score FROM f_emotion WHERE username = %s', username)
result = cur.fetchone()
emotion_score = result[0]
st.write("Facial actions: ",emotion_score,"/10")
emotion_score = float(emotion_score)

cur.execute('SELECT tech_score FROM f_tech WHERE username = %s', username)
result = cur.fetchone()
tech_score = result[0]
st.write("Technical interview score: ",tech_score,"/100")
tech_score = float(tech_score)

print(resume_score,emotion_score,tech_score)
final_score_ = round(((resume_score+emotion_score+tech_score)/210)*100,2)
print(final_score_)

st.markdown("<h1 style='font-size: 4rem; text-align: center; color: #0f0;'>SCORE: "+str(final_score_)+"</h1><br><br>", unsafe_allow_html=True)

query = f"INSERT INTO f_final (username,final_score) VALUES ('{username}', '{final_score_}') ON DUPLICATE KEY UPDATE final_score='{final_score_}'"
cur.execute(query)
conn.commit()
conn.close()

if st.button("Log out"):
    username = ""
    subprocess.Popen(["streamlit", "run", "login.py",])