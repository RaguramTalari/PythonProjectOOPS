import datetime

# Base Class
class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Email: {self.email}")

# Student Class inheriting from User
class Student(User):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.career_path = None
        self.course = None

    def choose_career_path(self, career_paths):
        print("\nAvailable Career Paths:")
        for i, path in enumerate(career_paths):
            print(f"{i+1}. {path.name}")

        try:
            choice = int(input("Choose a career path (Enter number): ")) - 1
            if 0 <= choice < len(career_paths):
                self.career_path = career_paths[choice]
                print(f"{self.name} has chosen the career path: {self.career_path.name}")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input! Please enter a number.")

    def choose_course(self):
        if not self.career_path:
            print("You must choose a career path first!")
            return

        print("\nAvailable Courses:")
        self.career_path.list_courses()

        course_choice = input("Enter the course name: ").strip()
        selected_course = None
        for course in self.career_path.available_courses:
            if course.course_name.lower() == course_choice.lower():
                selected_course = course
                break

        if selected_course:
            self.course = selected_course
            print(f"{self.name} has chosen the course: {self.course.course_name}")
        else:
            print("Invalid course selection!")

    def book_session(self, mentor):
        if mentor.is_available():
            session = SessionBooking(self, mentor)
            session.schedule_session()
        else:
            print(f"{mentor.name} is not available for a session.")

    def book_counselor_session(self, counselors):
        available_counselors = [c for c in counselors if c.is_available()]

        if not available_counselors:
            print("No counselors are available at the moment.")
            return

        print("\nAvailable Counselors:")
        for i, counselor in enumerate(available_counselors):
            print(f"{i+1}. {counselor.name} - Rating: {counselor.rating}/5")

        choice = input("Would you like to book a session with a counselor? (yes/no): ").strip().lower()
        if choice == "yes":
            try:
                counselor_choice = int(input("Choose a counselor (Enter number): ")) - 1
                if 0 <= counselor_choice < len(available_counselors):
                    self.book_session(available_counselors[counselor_choice])
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def book_course_session(self, teachers):
        if not self.course:
            print("You must choose a course first!")
            return

        relevant_teachers = [t for t in teachers if t.specialization == self.course.course_name and t.is_available()]

        if not relevant_teachers:
            print(f"Currently, no available teachers for {self.course.course_name}.")
            return

        choice = input(f"Would you like to book a session for {self.course.course_name}? (yes/no): ").strip().lower()
        if choice == "yes":
            print("\nAvailable Teachers:")
            for i, teacher in enumerate(relevant_teachers):
                print(f"{i+1}. {teacher.name} - Rating: {teacher.rating}/5 - Duration: {self.course.duration} months")

            try:
                teacher_choice = int(input("Choose a teacher (Enter number): ")) - 1
                if 0 <= teacher_choice < len(relevant_teachers):
                    self.book_session(relevant_teachers[teacher_choice])
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")

# Mentor Class
class Mentor(User):
    def __init__(self, name, age, email, specialization, available=True, rating=5):
        super().__init__(name, age, email)
        self.specialization = specialization
        self.__available = available  # Private attribute
        self.rating = rating

    def is_available(self):
        return self.__available

    def set_availability(self, status):
        if isinstance(status, bool):
            self.__available = status
        else:
            print("Invalid input! Availability must be True or False.")

    def conduct_session(self):
        print(f"{self.name} is conducting a session on {self.specialization}.")

# Counselor Class inheriting from Mentor
class Counselor(Mentor):
    def guide_student(self):
        print(f"Counselor {self.name} is guiding a student on career choices.")

# Teacher Class inheriting from Mentor
class Teacher(Mentor):
    def teach_course(self):
        print(f"Teacher {self.name} is teaching {self.specialization}.")

# CareerPath Class
class CareerPath:
    def __init__(self, name, available_courses):
        self.name = name
        self.available_courses = available_courses

    def list_courses(self):
        for course in self.available_courses:
            print(f"- {course.course_name}")

# Course Class
class Course:
    def __init__(self, course_name, duration):
        self.course_name = course_name
        self.duration = duration

    def course_details(self):
        print(f"Course: {self.course_name}, Duration: {self.duration} months")

# SessionBooking Class
class SessionBooking:
    def __init__(self, student, mentor):
        self.student = student
        self.mentor = mentor
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def schedule_session(self):
        print(f"\nSession booked! {self.student.name} will meet {self.mentor.name} on {self.date}.")
        self.mentor.set_availability(False)  # Set mentor as unavailable after booking

# Main Execution
if __name__ == "__main__":
    # Getting student input
    student_name = input("Enter student name: ")
    student_age = int(input("Enter student age: "))
    student_email = input("Enter student email: ")
    student_id = input("Enter student ID: ")
    student1 = Student(student_name, student_age, student_email, student_id)

    # Creating Courses
    python_course = Course("Python Programming", 3)
    ai_course = Course("Artificial Intelligence", 6)
    data_science = Course("Data Science", 5)
    analog_electronics = Course("Analog Electronics", 12)

    # Creating Career Paths
    software_engineering = CareerPath("Software Engineering", [python_course, ai_course])
    data_analysis = CareerPath("Data Analysis", [data_science])
    electronics = CareerPath("Electronics", [analog_electronics])

    career_paths = [software_engineering, data_analysis, electronics]

    # Creating Counselors
    counselor1 = Counselor("Dr. Smith", 45, "smith@example.com", "Career Guidance", available=True, rating=4.5)
    counselor2 = Counselor("Dr. Jane", 50, "jane@example.com", "Career Development", available=True, rating=4.8)
    counselors = [counselor1, counselor2]

    # Creating Teachers
    teacher1 = Teacher("Prof. John", 40, "john@example.com", "Python Programming", available=True, rating=4.7)
    teacher2 = Teacher("Dr. Sarah", 38, "sarah@example.com", "Artificial Intelligence", available=True, rating=4.9)
    teacher3 = Teacher("Dr. Alan", 50, "alan@example.com", "Analog Electronics", available=True, rating=4.5)
    teachers = [teacher1, teacher2, teacher3]

    student1.choose_career_path(career_paths)
    student1.book_counselor_session(counselors)
    student1.choose_course()
    student1.book_course_session(teachers)
