from flask import Flask,render_template,request, redirect, session
from jinja2 import Template
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"


@app.route('/home')
def render_home():
    
    ssn = session.get('ssn')
    if ssn:
        with sqlite3.connect('place.db') as conn:
            c = conn.cursor()
            name = c.execute("SELECT name FROM student WHERE ssn=?", (ssn,)).fetchone()[0]
    else:
        name = None
        
        

    return render_template('homepage.html', name=name)

@app.route('/infosys')
def render_infosys():
    return render_template('infosys.html')


@app.route('/microsoft')
def microsoft():
    return render_template('microsoft.html')

@app.route('/ibm')
def ibm():
    return render_template('ibm.html')


@app.route('/add_infosys')
def render_add_infosys():
    return render_template("infosys.html")


@app.route('/add_question_button', methods=['POST'])
def add_question_button():
    with sqlite3.connect("place.db") as conn:
        c = conn.cursor()

        qid = request.form.get("id")
        quest = request.form.get("questions")
        diff = request.form.get("difficultylevel")
        number = request.form.get("nooftimesasked")
        year = request.form.get("year")
        company = request.form.get("company_id")

        c.execute("""
                    INSERT INTO questions(q_id, question, dif_level,year,no_of_times,company_id) VALUES(?,?,?,?,?,?)
                    """, (qid,quest,diff,year,number,company))
        ques = c.execute("""SELECT * FROM QUESTIONS  """).fetchall()

        return render_template('viewquestion.html', questions=ques)
        
@app.route('/view_question', methods=['POST'])
def view_question():
    with sqlite3.connect("place.db") as conn:
        c = conn.cursor()
        questions=c.execute("""SELECT * FROM questions """).fetchall()
        return render_template("viewquestion.html", questions=questions)

@app.route('/add_answers')
def render_ans():
    return render_template("answers.html")

@app.route('/add_answers_button', methods=['POST'])
def add_answers_button():
    with sqlite3.connect("place.db") as conn:
        c = conn.cursor()

        answerid = request.form.get("ansid")
        answr = request.form.get("answer")
        qid = request.form.get("id")
        # ssn = request.form.get("ssn")
        print(qid)
        c.execute("""
                    INSERT INTO answers(ans_id,solution,q_id) VALUES(?,?,?)
                    """, (answerid,answr,qid))
        ans=c.execute("""SELECT * FROM ANSWERS """).fetchall()
        return render_template('viewanswer.html',answers=ans)

@app.route('/questionanswers', methods=['GET'])
def view_questions_button():
    with sqlite3.connect("place.db") as conn:
        c = conn.cursor()
        qa = c.execute("""SELECT Q.*,A.* FROM QUESTIONS Q,ANSWERS A 
            WHERE Q.q_id=A.q_id""").fetchall()

        return render_template('questionanswers.html', questions=qa)

@app.route('/companies', methods=['GET'])
def companies():
    with sqlite3.connect("place.db") as conn:
        c= conn.cursor()
        comp=c.execute("""SELECT * FROM company""").fetchall()
        print(comp)

        return render_template('companies.html',companies=comp)
        

@app.route('/add_feedback_button')
def render_feedback():
    return render_template('feedback.html')

@app.route('/add_feedback', methods=['POST'])
def add_feedback_button():
    with sqlite3.connect("place.db") as conn:
        c = conn.cursor()

        fid = request.form.get("f_id")
        feed = request.form.get("feedback")
        ssn = request.form.get("ssn")
        c.execute("""
                    INSERT INTO feedback(f_id,feedback,ssn) VALUES(?,?,?)
                    """, (fid,feed,ssn))
        # feedbck = c.execute("""SELECT * FROM FEEDBACK  """).fetchall()

        return redirect('/')

@app.route('/')
@app.route('/login')
def render_login():
    return render_template('loginform.html')


@app.route('/login_button', methods=['POST'])
def check_login():
    ssn = request.form.get("ssn")
    password = request.form.get("password")
    with sqlite3.connect('place.db') as conn:
        c = conn.cursor()

        k = c.execute("""SELECT * FROM student
            WHERE ssn=? AND password=?
            """, (ssn, password)).fetchone()

        if k is not None:
            session['ssn'] = ssn
            print("sign in  success")
            return redirect('/home')
        else:
            return redirect('/login')


@app.route('/signout')
def signout():
    if "ssn" in session:
        session.pop("ssn", None)
        print("signed out success")

        return redirect('/home')
    else:
        return redirect('/home')


if __name__ == "__main__":
    app.run(debug=True) 

