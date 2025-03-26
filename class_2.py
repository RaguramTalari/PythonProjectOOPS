
from db_connector import get_db_connection as gt
import datetime
class User:
    def __init__(self,uname,age,email,urole):
        self.uname=uname
        self.age=age
        self.email=email
        self.urole=urole
    def savetodb(self):
        conn = gt()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO USERS(uname, age, email,urole) VALUES (%s, %s, %s,%s)",
            (self.uname, self.age, self.email,self.urole)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"User {self.uname} added to the database.")
        return user_id
    @staticmethod
    def fetch_all_users():
        conn = gt()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
class Student(User):
    def __init__(self, uname, age, email,urole,college_id,college,careerpath=None,courses=None):
        super().__init__(uname, age, email,'student')
        self.college_id=college_id
        self.college=college
        self.careerpath=careerpath
        self.courses=courses

    def savetodb(self):
        user_id = super().savetodb()  # Save to USERS table and get user_id
        conn=gt()
        cursor =conn.cursor()
        cursor.execute("INSERT INTO students ( uname, age, email, career_path, courses, college_id, college) VALUES ( %s, %s, %s, %s, %s, %s, %s)",
                       ( self.uname, self.age, self.email, self.careerpath, self.courses, self.college_id, self.college))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Student '{self.uname}' details added to students table!")
class Teacher(User):
    def __init__(self, uname, age,email, courses, available=True, rating=0.0):
        super().__init__(uname,age,email,'teacher')
        self.courses = courses
        self.available = available
        self.rating = rating
    def savetodb(self):
        user_id = super().savetodb()
        conn = gt()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO teacher (uname, age, email,courses, available, rating) VALUES ( %s, %s, %s, %s, %s, %s)",
                       ( self.uname, self.age, self.email, self.courses, self.available, self.rating))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Teacher '{self.uname}' details added to teacher table!")
class Counsellor(User):
    def __init__(self, uname, age,email, career_path, available=True, rating=0.0):
        super().__init__(uname, age,email, "counsellor")
        self.career_path = career_path
        self.available = available
        self.rating = rating
    def savetodb(self):
        user_id = super().savetodb()
        conn = gt()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO counsellor ( uname, age, email,career_path, available, rating) VALUES ( %s, %s, %s, %s, %s, %s)",
            ( self.uname, self.age, self.email, self.career_path, self.available, self.rating))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Counsellor '{self.uname}' details added to counsellor table!")
class CareerPath:
    def __init__(self,careerpath=None):
        self.careerpath=careerpath
    def savetodbcp(self):
        conn = gt()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Career_path(career_path) VALUES (%s)",
            (self.careerpath,)
        )
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def chooseCareerpath():
        conn = gt()
        cursor = conn.cursor()
        cursor.execute("SELECT career_path FROM Career_path")
        career_paths = cursor.fetchall()
        if career_paths:
            print("\nCareer Paths")
            for i, (career,) in enumerate(career_paths, start=1):
                print(f"{i}. {career}")
            try:
                choice = int(input("Choose a career path (Enter number): ")) - 1
                if 0 <= choice < len(career_paths):
                    return career_paths[choice][0]
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
        else:
            print('No careerPaths at the moment')
class Courses(CareerPath):
    def __init__(self,careerpath,course_name,duration):
        super().__init__(careerpath)
        self.course_name=course_name
        self.duration=duration
    def savetodbcourse(self):
        conn = gt()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Courses (course_name, duration, career_path) VALUES (%s, %s, %s)",(self.course_name, self.duration, self.careerpath))
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def chooseCourse(career_path):
        conn = gt()
        cursor = conn.cursor()
        cursor.execute("SELECT course_name,duration FROM Courses where career_path=%s ",(career_path,))
        courses= cursor.fetchall()
        if courses:
            print("\ncourses")
            for i, (c,duration) in enumerate(courses, start=1):
                print(f"{i}. {c}|{duration}")
            try:
                choice = int(input("Choose a course (Enter number): ")) - 1
                if 0 <= choice < len(courses):
                    f=list(courses)
                    return courses[choice][0]


                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
        else:
            print('No Courses at the moment')

class Session:
    def __init__(self,student,mentor,role):
        self.student=student
        self.mentor=mentor
        self.role=role

    def book_session(self):
        conn = gt()
        cursor = conn.cursor()
        if self.role=="counsellor":
            cursor.execute("UPDATE counsellor set available = false where uname =%s",(self.mentor,))
        elif self.role=="teacher":
            cursor.execute("UPDATE teacher set available = false where uname =%s", (self.mentor,))

        date_of_booking = datetime.date.today().strftime("%Y-%m-%d")

        cursor.execute("INSERT INTO sessions (student_name, mentor_name, date_of_booking) VALUES (%s, %s, %s)",
                       (self.student, self.mentor, date_of_booking))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Session booked with {self.mentor} for {self.student} on {date_of_booking}.")










def list_counsellors(career_path):

    conn = gt()
    cursor = conn.cursor()
    cursor.execute("Select uname ,available,rating from Counsellor where career_path=(%s)",(career_path,))
    counsellors_list=cursor.fetchall()
    if counsellors_list:
        print("\nCounsellor List")
        for i, (uname, available, rating)in enumerate(counsellors_list, start=1):
            availability_status = "Available" if available else " Not Available"
            print(f"{i}. {uname} | {availability_status} |  Rating: {rating}")
        choice = input("Would you like to book a session with a counsellor? (yes/no): ").strip().lower()
        if choice == "yes":
            try:
                choice = int(input("Choose a Counsellor (Enter number): ")) - 1
                if 0 <= choice < len(counsellors_list):
                    return counsellors_list[choice][0]
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
def list_teachers(courses):
    conn = gt()
    cursor = conn.cursor()
    cursor.execute("SELECT uname, available, rating FROM teacher WHERE courses LIKE %s", ('%' + courses + '%',))

    teachers_list=cursor.fetchall()
    if teachers_list:
        print('\n Teachers List')
        for i ,(uname,available,rating) in enumerate(teachers_list,start=1):
            availability_status = "Available" if available else " Not Available"
            print(f"{i}. {uname} | {availability_status} |  Rating: {rating}")
        choice = input("Would you like to book a session with a Teacher? (yes/no): ").strip().lower()
        if choice == "yes":
            try:
                choice = int(input("Choose a Teacher (Enter number): ")) - 1
                if 0 <= choice < len(teachers_list):
                    return teachers_list[choice][0]


                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")








def create_user():

    uname = input("Enter Name: ")
    email = input("Enter Email: ")
    age = int(input("Enter Age: "))
    role = input("Enter Role (student/teacher/counsellor): ").lower()

    if role == "student":
        college_id = input("Enter College ID (or press Enter to skip): ") or None
        college = input("Enter College Name (or press Enter to skip): ") or None

        career_path = CareerPath.chooseCareerpath()
        a=list_counsellors(career_path)
        if a:
            s=Session(uname,a,'counsellor')
            s.book_session()

        if career_path:
            courses=Courses.chooseCourse(career_path)
            b=list_teachers(courses)
            if b:
                s1=Session(uname,b,"teacher")
                s1.book_session()
            else:
                courses=None
        else:
            career_path=None
            courses=None

        user = Student(uname, age,email,role, college_id, college,career_path, courses,)

    elif role == "teacher":

        courses = input("Enter Courses: ")
        user = Teacher(uname, age,email, courses)

    elif role == "counsellor":
        career_path = input("Enter Career Path: ")
        user = Counsellor(uname, age,email ,career_path)

    else:
        print("Invalid role! Please enter 'student', 'teacher', or 'counsellor'.")
        return
    user.savetodb()


def update_user_details():
    uname = input("Enter the username to update: ")
    conn = gt()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT urole FROM USERS WHERE uname = %s", (uname,))
    user = cursor.fetchone()

    if not user:
        print("User not found!")
        return

    role = user[0]
    new_email = input("Enter new Email (press Enter to skip): ") or None
    new_age = input("Enter new Age (press Enter to skip): ") or None

    if new_age:
        new_age = int(new_age)


    cursor.execute("UPDATE USERS SET email = COALESCE(%s, email), age = COALESCE(%s, age) WHERE uname = %s",
                   (new_email, new_age, uname))


    if role == "student":
        new_careerpath = input("Enter new Career Path (press Enter to skip): ") or None
        new_courses = input("Enter new Courses (press Enter to skip): ") or None
        cursor.execute(
            "UPDATE students SET career_path = COALESCE(%s, career_path), courses = COALESCE(%s, courses) WHERE uname = %s",
            (new_careerpath, new_courses, uname))

    elif role == "teacher":
        new_courses = input("Enter new Courses (press Enter to skip): ") or None
        new_availability = input("Update Availability? (yes/no, press Enter to skip): ").strip().lower()
        if new_availability == "yes":
            available = input("Enter Availability (true/false): ").strip().lower() == "true"
            cursor.execute("UPDATE teacher SET courses = COALESCE(%s, courses), available = %s WHERE uname = %s",
                           (new_courses, available, uname))

    elif role == "counsellor":
        new_careerpath = input("Enter new Career Path (press Enter to skip): ") or None
        new_availability = input("Update Availability? (yes/no, press Enter to skip): ").strip().lower()
        if new_availability == "yes":
            available = input("Enter Availability (true/false): ").strip().lower() == "true"
            cursor.execute(
                "UPDATE counsellor SET career_path = COALESCE(%s, career_path), available = %s WHERE uname = %s",
                (new_careerpath, available, uname))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"User '{uname}' details updated successfully!")






