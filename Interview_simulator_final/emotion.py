from imports import st,sys,cv2,np,load_model,time,subprocess,dbconn

st.set_page_config(
   page_title="Emotion"
)

username = sys.argv[1] #reading username from previous page
st.write("Userid: "+username)

conn= dbconn()
cur = conn.cursor()

# Create the grneral table
cur.execute("""
CREATE TABLE IF NOT EXISTS f_emotion (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    emotion_score VARCHAR(8) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY username (username)
)
""")


def emotion():
    # Load the face cascade classifier and emotion detection model
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    emotion_detection_model = load_model('emotion_detection_model.h5')

    # Define the emotions
    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    # Define a function to detect the dominant emotion in a face
    def detect_emotion(face_img):
        # Resize the image to 64x64
        resized_img = cv2.resize(face_img, (64, 64))
        # Convert the image to grayscale
        grayscale_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        # Reshape the image to have a single channel
        reshaped_img = grayscale_img.reshape((64, 64, 1))
        # Normalize the image
        normalized_img = reshaped_img / 255.0
        # Make a prediction on the image
        prediction = emotion_detection_model.predict(np.array([normalized_img]))
        # Get the index of the dominant emotion
        emotion_index = np.argmax(prediction)
        # Get the name of the dominant emotion
        emotion_name = emotions[emotion_index]
        return emotion_name

    # Start the video stream
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    score = 0

    # Process each frame of the video stream
    while True:
        # Check if 15 seconds have elapsed
        if time.time() - start_time > 15:
            print("Final Score:", score)
            break
        
        # Capture a frame from the video stream
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to grayscale
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(grayscale_frame, scaleFactor=1.3, minNeighbors=5)
        
        # Process each face in the frame
        for (x, y, w, h) in faces:
            # Extract the face from the frame
            face_img = frame[y:y+h, x:x+w]
            
            # Detect the dominant emotion in the face
            emotion = detect_emotion(face_img)
            
            # Draw a rectangle around the face and label the dominant emotion
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            
            # Update the score if the dominant emotion is happy or surprise
            if emotion == 'Happy' or emotion == 'Surprise':
                score = min(score + 1, 10)
                print("Score:", score)
        
        # Display the processed frame
        cv2.imshow('Facial Emotion Detection', frame)
        
        # Check for a key press to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

    return score

subprocess.Popen(["streamlit", "run", "general_ques.py","--",username])

emotion_score = emotion()

query = f"INSERT INTO f_emotion (username,emotion_score) VALUES ('{username}', '{emotion_score}') ON DUPLICATE KEY UPDATE emotion_score='{emotion_score}'"
cur.execute(query)
conn.commit()
conn.close()
