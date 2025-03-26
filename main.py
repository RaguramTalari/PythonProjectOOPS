from db_connector import get_db_connection as gt
from Class_2 import Student,Teacher,Counsellor,Courses,CareerPath,Session,User,create_user,list_teachers,list_counsellors,update_user_details
if __name__ == "__main__":
    print("_________________WELCOME TO JEET CAREER GUIDANCE PROGRAM__________________")
    while(1):
       print("1.ADD USER \n ")
       print("2.UPDATE USER \n")
       print("3.QUIT\n")
       a=int(input("Enter the number"))
       if(a==1):
           create_user()
           conn=gt()
           cursor = conn.cursor()
           cursor.close()
           conn.close()
       elif(a==2):
           conn= gt()
           cursor = conn.cursor()
           update_user_details()
           cursor.close()
           conn.close()
       elif(a==3):
           conn = gt()
           cursor = conn.cursor()
           c=User.fetch_all_users()
           for i in c:
               print(i)
           cursor.close()
           conn.close()
           print("THANKYOU")
           break
       else:
           print("invalid number try again")
