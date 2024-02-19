from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from main import Student, Group, Teacher, Subject, Grade
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


fake = Faker()


def create_students(num_students):
    for _ in range(num_students):
        student = Student(name=fake.name())
        session.add(student)


def create_groups(num_groups):
    for i in range(1, num_groups + 1):
        group = Group(name=f'Group {i}')
        session.add(group)


def create_teachers(num_teachers):
    for _ in range(num_teachers):
        teacher = Teacher(name=fake.name())
        session.add(teacher)


def create_subjects(num_subjects):
    for _ in range(num_subjects):
        teacher_id = random.randint(1, session.query(Teacher).count())
        subject = Subject(name=fake.word(), teacher_id=teacher_id)
        session.add(subject)


def create_grades_for_students():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        for subject in subjects:
            num_grades = random.randint(1, 20)
            for _ in range(num_grades):
                date_received = fake.date_time_between(start_date='-30d', end_date='now')
                grade = Grade(student_id=student.id, subject_id=subject.id, grade=random.uniform(1, 10), date_received=date_received)
                session.add(grade)

if __name__ == "__main__":
    
    
    engine = create_engine('postgresql://postgres:11111@localhost/postgres')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


    create_students(50)
    create_groups(3)
    create_teachers(5)
    create_subjects(8)
    create_grades_for_students()
    
    
    session.commit()