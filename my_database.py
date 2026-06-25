from sqlalchemy import Table, Column ,create_engine , String, Boolean, ForeignKey
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///my_database.db", echo=True )

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    university: Mapped[str] = mapped_column(String(100))
    specialty: Mapped[str] = mapped_column(String(100))
    group: Mapped[str] = mapped_column(String(100))
    exams: Mapped[list["ExamResult"]] = relationship("ExamResult", back_populates="student")

class ExamResult(Base):
    __tablename__ = "exam_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject: Mapped[str] = mapped_column(String(100))
    grade: Mapped[int] = mapped_column()
    passing_grade: Mapped[int] = mapped_column()
    passed: Mapped[bool] = mapped_column(Boolean)
    student: Mapped["Student"] = relationship("Student", back_populates="exams")


class Guests(Base):
    __tablename__ = "guests"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(15))

   
def add_Guests():
    with Session() as session:
        new_guest = Guests(
            name = "Іван Петренко",
            phone = "+0987654321"
        )
        session.add(new_guest)
        session.commit()


def add_exam_result():
    with Session() as session:
            new_result = ExamResult(
                student_id=1,
                subject="Вища математика",
                grade=85,
                passing_grade=60,
                passed=True
            )
            session.add(new_result)
            session.commit()

        


def get_all_students():
    with Session() as session:
        students = session.query(Student).all() 
        for student in students:
            print(f"ID: {student.id}, Ім'я: {student.name}, Університет: {student.university}, Спеціальність: {student.specialty}, Група: {student.group}")
            print("Результати екзаменів:")
            if student.exams:
                for exam in student.exams:
                    print(f"Предмет: {exam.subject}, Оцінка: {exam.grade}, Пройшов: {exam.passed}")
            else:
                print("  Немає оцінок")

def update_exam_grade():
    with Session() as session:
        exam = session.query(ExamResult).filter_by(id = 3).first()

        exam.grade = 100
        session.commit()
    


def delete_grades():
    with Session() as session:
        student = session.query(ExamResult).filter_by(id = 1).first()

        session.delete(student)
        session.commit()

base = Base()
base.create_db()