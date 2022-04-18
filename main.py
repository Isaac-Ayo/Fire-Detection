import cv2
import streamlit as st
from playsound import playsound
import threading
import smtplib

Email_Status = False

st.title("Webcam Application")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])

def send_mail_function():

    recipientEmail = "recipient's email"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.ehlo()
        server.starttls()
        server.login("sender email", 'sender password')
        server.sendmail('sender email', recipientEmail, 'Subject: FIRE\n\nWarning! Fire has been detected in your control area!')
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
        print(e)


fire_cascade = cv2.CascadeClassifier(r"C:\Users\isaac\Desktop\Fire_Detection\fire_detection.xml")

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    FRAME_WINDOW.image(gray)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        print("fire is detected")
        st.write('Warning! Fire has been detected in your control area!')
        playsound(r"C:\Users\isaac\Desktop\Fire_Detection\audio.mp3")
        if Email_Status == False:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True
        st.write('email is sent to isaacayob@gmail.com')
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
else:
    st.write('Stopped')

cv2.destroyAllWindows()
cap.release()