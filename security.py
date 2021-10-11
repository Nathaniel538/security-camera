import cv2#import statements
import time
import datetime

cap=cv2.VideoCapture(0)#accessing webcam with index 0

face_cascade=cv2.CascadeClassifier(
    cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
body_cascade=cv2.CascadeClassifier(
    cv2.data.haarcascades+"haarcascade_fullbody_default.xml")

detection=False
detection_stopped_time=None
timer_started=False
strad=5

frame_size=(int(cap.get(3)),int(cap.get(4))) #frame size
fourcc=cv2.VideoWriter_fourcc(*"mp4v") #fromat

while True:#dipalying the video as frames
    _,frame=cap.read() #returns 2 values,_is a placeholder

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #grayscaling the image
    faces=face_cascade.detectMultiScale(gray,1.1,5) #using the classifier to detect faces
    bodies=face_cascade.detectMultiScale(gray,1.1,5) #using the classifier to detect bodies

    if len(faces)+len(bodies)>0:
        if detection:
            timer_started=False
        else:
            detection=True
            current_time=datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out=cv2.VideoWriter(f"{current_time}.mp4",fourcc,20,frame_size) #output stream
            print("Started recording!")
    elif detection:
        if timer_started:
            if time.time()-detection_stopped_time>=strad:
                detection=False
                timer_started=False
                out.release()
                print("Stop Recording!")
            else:
                timer_started=True
                detection_stopped_time=time.time()
    
    if detection:
        out.write(frame)

    #for(x,y,width,height) in faces:
        #cv2.rectangle(frame,(x,y),(x + width,y + height),(255,0,0),3) #drawing a rectangle over the face

    cv2.imshow("Camera",frame)

    if cv2.waitKey(1)==ord('q'): #quitting the display
        break

out.release()
cap.release() #releasing the resources
cv2.destroyAllWindows()