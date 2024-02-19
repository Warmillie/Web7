from sqlalchemy import func
from main import Student, Group, Teacher, Subject, Grade
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    top_students = (
        session.query(Student, func.avg(Grade.grade).label('average_grade'))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return top_students

def select_2(subject_id):
    #Знайти студента із найвищим середнім балом з певного предмета
    top_student = (
        session.query(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    return top_student

def select_3(subject_id):
    #Знайти середній бал у групах з певного предмета.
    avg_grades_by_group = (
        session.query(Group.name, func.avg(Grade.grade).label('average_grade'))
        .select_from(Group) 
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    return avg_grades_by_group


def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок)
    avg_grade_all = (
        session.query(func.avg(Grade.grade).label('average_grade'))
        .scalar()
    )
    return avg_grade_all

def select_5(teacher_id):
    # Знайти які курси читає певний викладач
    courses_taught_by_teacher = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .all()
    )
    return courses_taught_by_teacher

def select_6(group_id):
    # Знайти список студентів у певній групі
    students_in_group = (
        session.query(Student)
        .filter(Student.group_id == group_id)
        .all()
    )
    return students_in_group

def select_7(group_id, subject_id):
    # Знайти оцінки студентів у окремій групі з певного предмета
    grades_in_group_for_subject = (
        session.query(Grade)
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    return grades_in_group_for_subject

def select_8(teacher_id):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів
    avg_grade_by_teacher = (
        session.query(func.avg(Grade.grade).label('average_grade'))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return avg_grade_by_teacher

def select_9(student_id):
    # Знайти список курсів, які відвідує певний студент
    courses_attended_by_student = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    return courses_attended_by_student

def select_10(student_id, teacher_id):
    # Список курсів, які певному студенту читає певний викладач
    courses_taught_to_student_by_teacher = (
        session.query(Subject.name)
        .join(Grade)
        .join(Teacher)
        .filter(Grade.student_id == student_id, Teacher.id == teacher_id)
        .distinct()
        .all()
    )
    return courses_taught_to_student_by_teacher

if __name__ == "__main__":
    engine = create_engine('postgresql://postgres:11111@localhost/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()


    result_1 = select_1()
    print("Top 5 students with highest average grades:")
    for student, average_grade in result_1:
        print(f"Student: {student.name}, Average Grade: {average_grade}")

    result_2 = select_2(subject_id=1)  
    print("Top student with highest average grade for a specific subject:")
    print(f"Student: {result_2.name}")

    result_3 = select_3(subject_id=1)  
    print("Average grades in groups for a specific subject:")
    for group_name, average_grade in result_3:
        print(f"Group: {group_name}, Average Grade: {average_grade}")

    result_4 = select_4()
    print("Average grade across all grades:")
    print(f"Average Grade: {result_4}")

    result_5 = select_5(teacher_id=1)  
    print("Courses taught by a specific teacher:")
    for course in result_5:
        print(course)

    result_6 = select_6(group_id=1)  
    print("Students in a specific group:")
    for student in result_6:
        print(student.name)

    result_7 = select_7(group_id=1, subject_id=1)  
    print("Grades of students in a specific group for a specific subject:")
    for grade in result_7:
        print(f"Student ID: {grade.student_id}, Grade: {grade.grade}")

    result_8 = select_8(teacher_id=1) 
    print("Average grade given by a specific teacher for their subjects:")
    print(f"Average Grade: {result_8}")

    result_9 = select_9(student_id=1)  
    print("Courses attended by a specific student:")
    for course in result_9:
        print(course)

    result_10 = select_10(student_id=1, teacher_id=1) 
    print("Courses taught to a specific student by a specific teacher:")
    for course in result_10:
        print(course)