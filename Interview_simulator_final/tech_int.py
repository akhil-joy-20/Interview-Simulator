from imports import st,pd,spacy,random,json,subprocess,pm,dbconn,sys

st.set_page_config(
   page_title="Round 3"
)


username = sys.argv[1] #getting username from previous page
# username ="@khil"
nlp = spacy.load('en_core_web_sm') #English language model,GENERATE QUESTION FN AND EXTRACTING KEYWORDS FROM USERS ANSWER

conn = dbconn()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS f_tech (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    tech_score VARCHAR(8) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY username (username)
)
""")

#extracting selected skills from f_resume_data
cur.execute('SELECT skill1 FROM f_resume_data WHERE username = %s', username)
result = cur.fetchone()
skill1 = result[0]

cur.execute('SELECT skill2 FROM f_resume_data WHERE username = %s', username)
result = cur.fetchone()
skill2 = result[0]

cur.execute('SELECT skill3 FROM f_resume_data WHERE username = %s', username)
result = cur.fetchone()
skill3 = result[0]

keywords = [skill1,skill2,skill3]
print(keywords)
# answer begin
def calculate_accuracy(answer, expected_answer):
    score=0

    _expected_answer_list = expected_answer.split() #convert string to list
    _answer_list = answer.split()
    
    expected_answer_list = [elem.lower() for elem in _expected_answer_list] #convert to lowercase
    answer_list = [elem.lower() for elem in _answer_list]

    print("E",expected_answer_list)
    print("U",answer_list)

    for i in expected_answer_list:  #updating score if keywords in expected ans found in users ans
        if i in answer_list:
            score+=1
    
    return round((score/len(expected_answer_list))*100,2)
    # return round(SequenceMatcher(None, answer, expected_answer).ratio() * 100, 2) #sequence matcher
#answer end

@st.cache
def load_dataset(filename):
    # Replace this with your own dataset loading code
    df = pd.read_csv(filename)
    return df

# @st.cache
def generate_questions(df, keywords):
    questions = []
    for i, row in df.iterrows():
        doc = nlp(row['key'])
        if all(keyword in doc.text for keyword in keywords):
            questions.append(row['question'])
    return questions

#savestate begin
def get_state():
    # Try to get the state from local storage
    query_params = st.experimental_get_query_params()
    if 'state' in query_params:
        # If the state exists, parse it from JSON and return it
        return json.loads(query_params['state'][0])
    else:
        # Otherwise, return a default state
        return {'state_ques': [], 'state_exp_ans' : []}
    
def set_state(state):
    # Convert the state to JSON and set it in local storage
    st.experimental_set_query_params(state=json.dumps(state))
#savestate end


def run_file2(username):    #link
    subprocess.Popen(["streamlit", "run", "res.py","--",str(username)])


def main():
    keywords = [skill1,skill2,skill3]
    state = get_state() #savestate

    st.write("Userid: "+username)
    st.markdown("<h1 style='font-size: 4rem; text-align: center; color: #fff;'>Round 3<br> Technical Interview</h1><br><br>", unsafe_allow_html=True)
    df = load_dataset('ques1.csv')

    accuracy_list = [] #to store all accuracy values

    sl=0
    key_ans_inpt=2

    state_var=0          #save state (index variables)
    state_var_ans=0      #save state
    state_var_ans_two=0  #save state
 
    first_ques=0        #first ques repeating

    with st.form(key='my_form'):
        for keyword in  keywords:

            questions = []
            questions = generate_questions(df, keyword)
            p=random.sample(questions,2)
        
            for k in p:

                digits=""       #to extract digits from question in dataset 
                for char in k:
                    if char.isdigit():
                        digits += char
                    else:
                        break

                row = digits  #row = k[0]
                row = int(row) - 1

                while len(k)>0 and not k[0].isalpha(): #removing question number
                    k = k[1:]

                state['state_ques'].append(k) #appending generated question to state variable

                if state['state_ques']: #load prev ques if exists else prints new question
                    st.write(f"{sl+1}.{state['state_ques'][state_var]}")
                    state_var+=1
                    sl+=1
                else:
                    st.write(f"{sl+1}.{k}")
                    sl+=1
                    first_ques=1  #to avoid first question repeating twice

                
            
                if first_ques==1:   #to avoid first question repeating twice
                    del state['state_ques'][0]
                    first_ques=0

                keywords = df.loc[row, "key"]
                expected_answer = df.loc[row, "answer"]
                state['state_exp_ans'].append(expected_answer) #appending expec ans to state variable
                # st.write("Keywords:", keywords)

                if state['state_exp_ans']: #load prev exp_ans if exists else prints question mapped exp_ans
                    # st.write(state['state_exp_ans'][state_var_ans])
                    state_var_ans+=1
                # else:
                #     st.write("Expected Answer:", expected_answer)

                answer = st.text_area("Answer",key=key_ans_inpt)
                key_ans_inpt+=2
                
                if answer:
                    doc = nlp(answer) # Process the paragraph with spaCy - EXTRACT KEYWORDS FROM USERS ANSWER
                    user_ans_keywords = set(token.text for token in doc if token.pos_ in ["NOUN", "PROPN"])
                    user_ans_keywords_string = ' '.join(user_ans_keywords) #convert set to string
                    print(user_ans_keywords_string)

                    accuracy = calculate_accuracy(user_ans_keywords_string, state['state_exp_ans'][state_var_ans_two])
                    state_var_ans_two+=1
                    st.write("Accuracy:", accuracy, "%")
                    accuracy_list.append(accuracy)

        submitted = st.form_submit_button(label='Submit')

    set_state(state) #save state

    if submitted:
        
        # st.balloons()

        css = """          
        <style>
        textarea {
        pointer-events: none;
        }
        </style>
        """
        st.write(css, unsafe_allow_html=True) #to make answer input non editable after submitting

        tech_score = (sum(accuracy_list)/600)*100
        tech_score = round(tech_score,2)

        query = f"INSERT INTO f_tech (username,tech_score) VALUES ('{username}', '{tech_score}') ON DUPLICATE KEY UPDATE tech_score='{tech_score}'"
        cur.execute(query)
        conn.commit()
        conn.close()

        run_file2(username) #link
        #st.experimental_rerun() #to rerun when submit btn is pressed and not reload when enter is pressed in text input


if __name__ == "__main__":
    main()
  
