from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class CountDown:
    def __init__(self, curr_time):
        self.curr_time = curr_time

    def decrement(self):
        if self.curr_time > 0:
            self.curr_time -= 1
        return self.curr_time

@app.route("/")
def index():
    return render_template('index.html')

teacherName = ''
studentName = ''
adminName = ''
studentAnswer = ''
teacherQuestion = ''
questionTime = CountDown(0)
teacherMarks = 0
totalMarks = 0
totalQuestion = 0
avgMarks = 0
hint = ''

@app.route('/home', methods = ['POST', 'GET'])
def home():
    global teacherName
    global studentName
    global adminName

    if request.method == 'POST':
        name = str(request.form['name'])
        select = request.form['select']

        if select == 'Teacher':
            teacherName = name
            return render_template('teacher.html')

        if select == 'Student':
            studentName = name
            return render_template('student.html')

        if select == 'Admin':
            adminName = name
            return render_template('admin.html')

    else:
        return render_template('index.html')

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    global hint

    if request.method == 'POST':
        hint = request.form['hint']

    return render_template('admin.html')

@app.route('/student', methods=['POST', 'GET'])
def student():

    global studentAnswer

    if request.method == 'POST':
        studentAnswer = request.form['answer']
        
        
    return render_template('/student.html')

@app.route('/teacher', methods=['POST','GET'])
def teacher():
    global teacherQuestion
    global questionTime
    global teacherMarks
    global totalMarks
    global totalQuestion
    global avgMarks
    global studentAnswer

    if request.method == 'POST':
        if request.form['question'] != '':
            teacherQuestion = request.form['question']
            # questionTime = int(request.form['time'])
            # questionTime = CountDown(questionTime)
            questionTime = CountDown(int(request.form['time']))
            totalQuestion += 1
            teacherMarks = 0

        
        if request.form['grade'] != '':
            teacherMarks = int(request.form['grade'])
            totalMarks += teacherMarks
            avgMarks = totalMarks / totalQuestion
            teacherQuestion = ''
            studentAnswer = ''
            questionTime.curr_time = 0



    return render_template('teacher.html')



@app.route('/find', methods = ['POST', 'GET'])
def find():
    global teacherName
    global studentName
    global adminName
    global studentAnswer
    global teacherQuestion
    global questionTime
    global teacherMarks
    global totalMarks
    global totalQuestion
    global avgMarks
    global hint

    questionTime.decrement()

    if questionTime.curr_time == 0:
        teacherQuestion = ''
        studentAnswer = ''

    return jsonify(tName = teacherName, sName = studentName, aName = adminName, sAnswer = studentAnswer, tQuestion = teacherQuestion, qTime = questionTime.curr_time, tMarks = teacherMarks, totMarks = totalMarks, totQues = totalQuestion, avgMarks = avgMarks, hint = hint)

    





if __name__ == "__main__":
    app.run(debug=True)