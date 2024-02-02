from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dkss'
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
       return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])


def HelloW():
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')

        if not title or not desc:
            flash('Title and Description cannot be empty!', 'error')
        else:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            flash('Todo added successfully!', 'success')
    search_query = request.args.get('search')
    if search_query:
        # Perform a search based on the title
        alltodo = Todo.query.filter(or_(Todo.title.contains(search_query), Todo.desc.contains(search_query))).all()
    else:
        # Retrieve all todos if there is no search query
        alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method =='POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo =Todo.query.filter_by(sno=sno).first()
        todo.title= title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo =Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo =Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')
if __name__  == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
    

