from imports import st,pm,subprocess,dbconn

st.set_page_config(page_title="User Registration", page_icon=":guardsman:")

#mysql connection
conn = dbconn()
cur = conn.cursor()

# Create the DB
db_sql = """CREATE DATABASE IF NOT EXISTS final_vis;"""
cur.execute(db_sql)

# # Create table
table_sql = """
        CREATE TABLE IF NOT EXISTS f_user_data (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY (username)
        )
                """
cur.execute(table_sql)

def register():
    # Insert user data into the database
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO f_user_data (username, password, name)
            VALUES (%s, %s, %s)
        """, (username, password, name))
    conn.commit()

    # Display success message
    st.success("User registered successfully!")
    subprocess.Popen(["streamlit", "run", "login.py"]) #link to login page

st.markdown("<h1 style='font-size: 5rem; text-align: center; color: #fff;'>User Registration</h1><br><br>", unsafe_allow_html=True)

name = st.text_input("Name")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if not username:
        st.error("Please enter a username.")
    elif not password:
        st.error("Please enter a password.")
    elif not name:
        st.error("Please enter your name.")
    else:
        register()

