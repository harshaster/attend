from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,Text,Column,Boolean
import datetime

app= Flask(__name__)

app.app_context().push()
app.config["DEBUG"]=True
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///./db.sqlite3"



db=SQLAlchemy(app)

class reg(db.Model):
    roll=Column(Integer, primary_key=True)
    timestamp=Column(Text)
    name=Column(Text)
    course=Column(Text)
    year=Column(Text)
    phone=Column(Text)
    email=Column(Text)
    seminar_051122=Column(Boolean)    #change this when seminar changes

db.create_all()

acc=open("access.txt",'a')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method=="GET":
        return render_template('index.html',step=1)
    elif request.method=="POST":
        data=request.form
        s=reg.query.get(data["roll"])
        if s:
            if s.seminar_051122:
                msg=f"{s.roll} , {s.name}, {datetime.datetime.now()} , already\n"
                acc.write(msg)
                acc.flush()
                return render_template('done.html',already=True)
            return(render_template('index.html',step=2,name=s.name,roll=s.roll,course=s.course,year=s.year))
        else:
            return render_template('new.html',roll=data["roll"])
@app.route("/done", methods=["POST"])
def record():
    data=request.form
    s=reg.query.get(data["roll"])
    s.seminar_051122=True
    db.session.commit()
    msg=f"{s.roll} , {s.name}, {datetime.datetime.now()} , marked\n"
    acc.write(msg)
    acc.flush()
    return render_template('done.html',already=False)


@app.route("/new", methods=["POST"])
def new():
    data = request.form
    nn=reg(
        timestamp=str(datetime.datetime.now()),
        name=data["name"],
        roll=data["roll"],
        course=data["course"],
        year=data["year"],
        phone=data["phone"],
        email=data["email"],
        seminar_051122=True
    )
    db.session.add(nn)
    db.session.commit()
    msg=f"{nn.roll} , {nn.name}, {datetime.datetime.now()} , registered\n"
    acc.write(msg)
    acc.flush()
    return render_template('done.html')
    


if __name__=="__main__":
    app.run(debug=True)