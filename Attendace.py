import maskpass  
from pymongo import MongoClient #pip install pymongo, pip install pymongo[srv]
import cv2 
import face_recognition #pip3 install face_recognition AFTER 
import numpy as np 
import os 
import cmake 

class Attendance():
    def __init__(self , mongo , d , s):
        #self.db = MongoClient(mongo) ; 
        self.day = d
        self.session = s 
        self.path = 'StudentImages'
        self.session_student , self.student_names = self.getKnownStudents();
        self.present = [] 

    '''
    Method uploads session doc to the mongodb session doc comprises of a list of all student nums scanned and verified. And terminates program for the day. 
    doc = { day: , sesh: , users: []}  
    '''
    def sessionEnd():
        print("I DON'T WORK YET")
        pass
    

    '''
    Method to register student's iamge and their student number. 
    Images stored locally on machine where this script is running, but a solution using S3 to store the pictures and downloading them per sesh can be easily done 
    '''
    def addStudent():
        print("I DON'T WORK YET , ADD pics manually for now")
        pass
    
    '''
    Method to mark attendance of students using open cv library 
    '''
    def mark(self): 
        cam = cv2.VideoCapture(0) #initialize camera 
        while(True):
            success , image = cam.read()
            compressed_img = cv2.resize(image,(0,0),None,0.25,0.25 )#   Scalling image down to 1/4 size to make processing faster
            compressed_img = cv2.cvtColor(compressed_img , cv2.COLOR_BGR2RGB)
            frame = face_recognition.face_locations(compressed_img)
            encodedframe= face_recognition.face_encodings(compressed_img,frame)

            for encodface,faceloc in zip(encodedframe,frame): #Iterate through  faces and encoded faces in the 2 lists
                matches = face_recognition.compare_faces(self.session_student ,encodface)
                face_distance = face_recognition.face_distance(self.session_student,encodface) #Face distances to data , where smaller the distance the higher chance of a match
                matchIndex = np.argmin(face_distance) #Get match from face distance list
                 
                if matches[matchIndex]:
                     student_num = self.student_names[matchIndex].upper() #E.G NYSTAD002
                     print('GET OFF MY SCREENNNN')
                     #Student found , show that on camera and add them to present list.
                     y1,x2,y2,x1 =  faceloc #Bounds for person's face
                     y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 #Scalling frame bound up as they were generated using a scaled down
                     cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                    # cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)
                     cv2.putText(image,student_num,(x1+6 , y2-6) , cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255) ,2)
            cv2.imshow("joe" , image)
            cv2.waitKey(1)
        
    def encode(self , image):
         image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
         encode  = face_recognition.face_encodings(image)[0]
         return encode

    def getKnownStudents(self):
        students = os.listdir(self.path) ; 
        student_names = [] 
        student_encodings = [] 
        for file in students:
            currentImg = cv2.imread(f'{self.path}/{file}')
            student_encodings.append(self.encode(currentImg))
            student_names.append(os.path.splitext(file)[0])
            print(file)

        return student_encodings ,student_names
    

'''

    Main method for attendace script , tutor enters session details for the day , and makes connection to db using private password reserved for them.
    Launces instance of Attendance object which then runs for the marking 
'''
def main():
     
  day_of_week = "Tuesday"#input('Enter the day of your session\n')
  start_time = 1400#int(input('Enter start time of session,  Format:HHMM\n')) #All sessions are assumed to be 2 hrs , so if start is 1400 hrs this is the 1400 to 1600 session
  username ='dsdfds' #input('Enter username for database\n')
  password = 'dsed'#maskpass.askpass(mask="*")
  user_and_pass = username + ':'+ password 
  mongo = 'mongodb+srv://'+user_and_pass+'INSERT YOUR DATABASE CONNECTION HERE '

  tut = Attendance(mongo, day_of_week , start_time) 
  tut.mark()
#   INSERT MENU HERE 
#   while(True):
#       print('*****_____Attendance System_____*****')


if __name__ == '__main__':
     main();