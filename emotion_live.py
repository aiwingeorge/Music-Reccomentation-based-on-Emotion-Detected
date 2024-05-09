import cv2
import numpy as np
from keras.models import model_from_json
import tensorflow as tf

emotion_dict = {0: "Angry", 1: "Fearful", 2: "Happy", 3: "Neutral", 4: "Sad", 5: "Surprised"}


emotion_model = tf.keras.models.load_model('C:/Users/aiwin/OneDrive/Desktop/Hub/P6_emotion_Detection/modelv1.h5')

cap = cv2.VideoCapture(0)

while True:
  
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1080, 720))
    if not ret:
        break
    face_detector = cv2.CascadeClassifier('C:/Users/aiwin/OneDrive/Desktop/Hub/P6_emotion_Detection/haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

  
  
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

    
    
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Emotion Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()