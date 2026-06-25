from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import my_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_database import Student, ExamResult

engine = create_engine("sqlite:///my_database.db", echo=True)
Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-super-flexible-secret-key-12345'

csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def f_page_1():
    with Session() as session:
        students = session.query(Student).all()
    return render_template('first_page.html', data=students)

@app.route('/search_greades', methods=['GET', 'POST'])
def f_page_2():
    if request.method == 'GET':
        return render_template('search_greades.html')
    
    student_name = request.form.get('username')
    if not student_name:
        return render_template('search_greades.html', message="Вкажіть ім'я студента.", status="error")
        
    with Session() as session:
        student_info = session.query(Student).filter_by(name=student_name).first()
        if student_info:
            exams = [{
                'subject': exam.subject,
                'grade': exam.grade,
                'passing_grade': exam.passing_grade,
                'passed': exam.passed
            } for exam in student_info.exams]
            
            student_data = {
                'name': student_info.name,
                'university': student_info.university,
                'specialty': student_info.specialty,
                'group': student_info.group
            }
            return render_template('search_greades.html', data=student_data, data_grades=exams)
        else:
            return render_template('search_greades.html', message='Студента не знайдено.', status="error")

@app.route('/add_student', methods=['GET', 'POST'])
def add_student_route():
    if request.method == 'GET':
        return render_template('add_student.html')
    
    name = request.form.get('username')
    university = request.form.get('university')
    specialty = request.form.get('specialty')
    group = request.form.get('group')
    
    if not all([name, university, specialty, group]):
        return render_template('add_student.html', message='Усі поля обов\'язкові для заповнення!', status="error")
        
    with Session() as session:
        new_student = Student(
            name=name,
            university=university,
            specialty=specialty,
            group=group
        )
        session.add(new_student)
        session.commit()
        
    return render_template('add_student.html', message='Студента успішно додано!', status="success")

@app.route('/join', methods=['GET', 'POST'])
def join_route():
    if request.method == 'GET':
        return render_template('join.html')
    return render_template('join.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'GET':
        return render_template('register.html')
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)