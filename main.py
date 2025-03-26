from Class_2 import Student,Teacher,Counsellor,Courses,CareerPath,Session,User,create_user,list_teachers,list_counsellors
if __name__ == "__main__":
    print("_________________WELCOME TO JEET CAREER GUIDANCE PROGRAM__________________")
    while(1):
        a=int(input("1.Add a User -------- 2.Quit ::"))
        if(a==1):
            create_user()
            conn=gt()
            cursor = conn.cursor()
            cursor.close()
            conn.close()
        if(a==2):
            print("THANKYOU")
            break
        else:
            print("invalid number try again")
