import cv2
from deepface import DeepFace
import threading
from numpy import dot
from numpy.linalg import norm
import os
import subprocess

count = 0
match = False
store = []

def capture():
    global store
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        try:
            faces = DeepFace.extract_faces(frame, enforce_detection=False)
            if len(faces) > 0:
                face = faces[0]['face']
                embedd = DeepFace.represent(face, model_name='VGG-Face', enforce_detection=False)[0]["embedding"]
                store.append(embedd)
                print("Face captured and embedding stored.")
                
                cv2.imshow("Captured Face", face)
                cv2.waitKey(3000) 
            else:
                print("No face detected.")
        except Exception as e:
            print(f"Error: {e}")
    cap.release()
    cv2.destroyAllWindows()

def cosine_similarity(embedding1, embedding2):
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))

def checking(frame):
    global match
    try:
        faces = DeepFace.extract_faces(frame, enforce_detection=False)
        if len(faces) > 0:
            face = faces[0]['face']
            current_embedding = DeepFace.represent(face, model_name='VGG-Face', enforce_detection=False)[0]["embedding"]
            
            match = False
            for stored_embedding in store:
                similarity = cosine_similarity(current_embedding, stored_embedding)
                if similarity > 0.7:  
                    match = True
                    print("Face match found. Launching Bank Management System.")
                    break
        else:
            print("No face detected in current frame.")
            match = False
    except Exception as e:
        print(f"Error in face verification: {e}")
        match = False

def open_bank():
    try:
        script = os.path.abspath('bank.py')
        subprocess.run(['python', script], check=True)
    except Exception as e:
        print(f"Error opening Bank Management System: {e}")

print("Please look at the camera to capture your reference image.")
input("Press Enter to continue...")
capture()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if ret:
        if count % 60 == 0:
            try:
                threading.Thread(target=checking, args=(frame.copy(),)).start()
            except Exception as e:
                print(f"Threading error: {e}")
        count += 1

        if match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.imshow("VIDEO", frame)
            cv2.waitKey(3000)  
            break  
        else:
            cv2.putText(frame, "NO MATCH", (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("VIDEO", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if match:
    open_bank()
