from imports import st,dbconn,PDFResourceManager,PDFPageInterpreter,PDFPage,ResumeParser,LAParams,LTTextBox,TextConverter,st_tags,base64,io,sys,subprocess

st.set_page_config(
   page_title="Round 1"
)

conn = dbconn()
cur = conn.cursor()

DB_table_name = 'f_resume_data'
table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                   (ID INT NOT NULL AUTO_INCREMENT,
                    username varchar(100) NOT NULL,
                    Email_ID VARCHAR(50) ,
                    phone VARCHAR(15),
                    resume_score VARCHAR(8) NOT NULL,
                    Page_no VARCHAR(5) NOT NULL,
                    skill1 VARCHAR(30),
                    skill2 VARCHAR(30),
                    skill3 VARCHAR(30),
                    PRIMARY KEY (ID));
                """
cur.execute(table_sql)

#functions start
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def insert_data(username, email, phone, res_score, no_of_pages, skill1, skill2, skill3):
    DB_table_name = 'f_resume_data'

    # Check if the record already exists in the database
    cur.execute(f"SELECT * FROM {DB_table_name} WHERE username=%s", (username))
    existing_record = cur.fetchone()
    
    if existing_record:
        # Record already exists, update it instead of inserting a new one
        update_sql = f"UPDATE {DB_table_name} SET phone=%s, resume_score=%s, page_no=%s, skill1=%s, skill2=%s, skill3=%s WHERE id=%s"
        rec_values = (str(phone), str(res_score), str(no_of_pages), skill1, skill2, skill3, existing_record[0])
        cur.execute(update_sql, rec_values)
        conn.commit()
    else:
        # Record doesn't exist, insert it into the database
        insert_sql = f"INSERT INTO {DB_table_name} VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s)"
        rec_values = (username, email, str(phone), str(res_score), str(no_of_pages), skill1, skill2, skill3)
        cur.execute(insert_sql, rec_values)
        conn.commit()

def skills_new_fn(keywords):
    # Define the priority dictionary higher number higher priority small case
    priority_dict = {
        'python': 10,
        'java': 9,
        'c': 18,
        'mi': 5,
        'cloud': 7
    }

    # Use a list comprehension to make all elements lower case
    keywords = [word.lower() for word in keywords]

    # Sort the keywords by priority, in descending order
    sorted_keywords = sorted(keywords, key=lambda x: priority_dict.get(x, 0), reverse=True)

    # Select the top 5 keywords
    return sorted_keywords[:3]

#functions end

username = sys.argv[1] #getting username from previous page

st.write("Userid: "+username)
st.markdown("<h1 style='font-size: 4rem; text-align: center; color: #fff;'>Round 1<br> Resume Analyzer</h1><br><br>", unsafe_allow_html=True)

#fetching name from db using username
cur.execute('SELECT name FROM f_user_data WHERE username = %s', username)
result = cur.fetchone()
name = result[0]

cgpa=' '
cgpa = st.number_input("Enter cgpa:",min_value=0, max_value=10)

if(cgpa>6):
    res_pdf = st.file_uploader("Upload Resume", type=["pdf"])

    if res_pdf is not None:
        #to store analysed resumes in local folder
        save_resume_loc = 'C:\\Users\\Admin\Desktop\\Interview_simulator_final\\resumes/'+res_pdf.name
        with open(save_resume_loc, "wb") as f:
            f.write(res_pdf.getbuffer())
                
        #display pdf
        st.markdown("<hr>", unsafe_allow_html=True)
        show_pdf(save_resume_loc)
        st.markdown("<hr>", unsafe_allow_html=True)

        #to extract resume key details
        resume_data = ResumeParser(save_resume_loc).get_extracted_data()

        if resume_data:
            #to extract whole resume text
            resume_text=[]
            resume_text = pdf_reader(save_resume_loc)
                
            st.markdown( '''<br><h2 style='text-align: left; color: #FF00FF;'>Personal Information</h2>''',unsafe_allow_html=True)

            try:
                if name == resume_data['name']:
                    st.text('Name : '+resume_data['name'])
                else:
                    st.text('Name : '+name)
                st.text('Email: ' + resume_data['email'])
                st.text('Phone: ' + resume_data['mobile_number'])
            except:
                pass

            #skills
            st.markdown( '''<br><h2 style='text-align: left; color: #FF00FF;'>Skills</h2>''',unsafe_allow_html=True)
            keywords = st_tags(label='',
            text='Add ->',value=resume_data['skills'],key = '1')

            #score calculating-------------------------------------------------------------------------------------------------------------
            st.markdown( '''<br><h2 style='text-align: left; color: #FF00FF;'>Resume Analysis</h2>''',unsafe_allow_html=True)
            score=0
            t=0

            rec_skills = ['html','tensorflow','keras','pytorch','machine learning','deep Learning','flask',
                            'react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                            'javascript', 'angular js', 'c#','android','android development','flutter','kotlin','xml','kivy',
                            'ios','ios development','swift','ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping',
                            'wireframes','storyframes','adobe photoshop','photoshop','editing','c','python','mysql','java']
            for i in resume_data["skills"]:
                if i.lower() in rec_skills:
                    if score<30:        #max score for skills is 30
                        score+=1
            if(score>=10):
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>✔️ Relevant Skills 👍 </h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h4 style='text-align: left; color: #fabc10;'>❌ Relevant Skills </h4>''',unsafe_allow_html=True)
                
            proj=['project','projects','Projects','Project','PROJECTS','PROJECT']
            for i in proj:
                if i in resume_text:
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>✔️ Projects 👨‍💻 </h4>''',unsafe_allow_html=True)
                    score+=20
                    t=1
                    break
            if t==0:
                st.markdown('''<h4 style='text-align: left; color: #fabc10;'>❌ Projects </h4>''',unsafe_allow_html=True)
                
            if 'Objective' or 'OBJECTIVE' or 'objective' in resume_text:
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>✔️ Objective 🔲 </h4>''',unsafe_allow_html=True)
                score+=20
            else:
                st.markdown('''<h4 style='text-align: left; color: #fabc10;'>❌ Objective </h4>''',unsafe_allow_html=True)
                
            if 'Hobbies' or 'Interests' in resume_text:
                score+=10
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>✔️ Hobbies 🔸 </h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h4 style='text-align: left; color: #fabc10;'>❌ Hobbies </h4>''',unsafe_allow_html=True)

            if 'Achievements' or 'Certificates' or 'certificates' in resume_text:
                score+=20
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>✔️ Acheivements 👏 </h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h4 style='text-align: left; color: #fabc10;'>❌ Acheivements </h4>''',unsafe_allow_html=True)
            #-------------------------------------------------------------------------------------------------------------------------
            st.markdown("<br>",unsafe_allow_html=True)
            st.subheader("**Resume Score**")
            st.markdown(
                """
                <style>
                    .stProgress > div > div > div > div {
                        background-color: #1E90FF;
                    }
                </style>""",
                unsafe_allow_html=True,
            )
            my_bar = st.progress(0)
            my_bar.progress(score)
            if score>50:
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Resume Score : &nbsp;&nbsp;'''+str(score)+''' </h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h4 style='text-align: left; color: #fabc10;'>Resume Score : &nbsp;&nbsp;'''+str(score)+''' </h4>''',unsafe_allow_html=True)

            #PRIORITIZE AND SHORTLIST SKILLS
            skills_new = skills_new_fn(resume_data['skills'])
            print(skills_new)
            skill1 = skills_new[0]
            skill2 = skills_new[1]
            skill3 = skills_new[2]
            

            # database entry
            insert_data(username, resume_data['email'], str(resume_data['mobile_number']),str(score),
                            str(resume_data['no_of_pages']), skill1, skill2, skill3
                        )

            conn.commit()
            if score>=60:
                if st.button("proceed"):  
                    subprocess.Popen(["streamlit", "run", "emotion.py","--", username])
            else:
                st.error("Cannot proceed")
        else:
            st.error('No data found')

else:
    if(cgpa!=0.00):
        st.error("Requirement doesn't match")


