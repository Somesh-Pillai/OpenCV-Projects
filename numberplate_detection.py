import cv2


nPlateCascade= cv2.CascadeClassifier("Resources/haarcascade_russian_plate_number.xml")
maxArea=500


video = cv2.VideoCapture(0)
video.set(3,640)
video.set(4,480)
video.set(10,100)
while True:
    success, img = video.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberpltes = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in numberpltes:
        area=w*h
        if area>maxArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,'Number Plate',(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,255),2)
        numberplateRegion =img[y:y+h,x:x+w]
        cv2.imshow("Number Plate", numberplateRegion)
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
