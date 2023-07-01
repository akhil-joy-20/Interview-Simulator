from imports import st,option_menu,dbconn,subprocess

st.set_page_config(
   page_title="Login"
)

conn = dbconn()

def authenticate(username, password):
    with conn.cursor() as cursor:
        # Check if the user exists
        cursor.execute('SELECT COUNT(*) FROM f_user_data WHERE username = %s', username)
        result = cursor.fetchone()
        if result[0] == 0:
            return False
        
        # Get the user's password
        cursor.execute('SELECT password FROM f_user_data WHERE username = %s', username)
        result = cursor.fetchone()
        db_password = result[0]
        
        # Compare the passwords
        if db_password == password:
            return True
        else:
            return False

st.markdown("<h1 style='font-size: 5rem; text-align: center; color: #fff;'>Login</h1><br><br>", unsafe_allow_html=True)
selected = option_menu(
            menu_title=None,  # required
            options=["User","Admin"],  # required
            icons=["person-fill","person-check-fill"],  
            menu_icon="cast", 
            default_index=0,  
            orientation="horizontal",
            styles={
                "container": {"padding": "5!important", "background-color": "#fff",},
                "icon": {"color": "black", "font-size": "25px"},
                "nav-link": {
                    "color": "#000",
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#c3bac9",
                },
                "nav-link-selected": {"background-color": "#00ff00",},
            },
        )
    
# Get the username and password from the user
username = st.text_input("Username")
password = st.text_input("Password", type="password")
    
# Authenticate the user when they click the button
if st.button("Login"):

    if selected == 'User':
        if authenticate(username, password):
            subprocess.Popen(["streamlit", "run", "home.py","--", username]) #link to admin page
        else:
            st.error("Incorrect username or password")
    else:
        if username == 'admin' and password == '1234':
            subprocess.Popen(["streamlit", "run", "admin.py"]) #link to admin page
        else:
            st.error("Incorrect username or password")