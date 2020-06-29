from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  #create instance of Flask class, provide name of module
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # three slashes is a relative path
db = SQLAlchemy(app)

class Todo(db.Model):   #Klasse die einen Eintrag darstellt?
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return'<Task %r>' % self.id #Keine Ahnung was hier passiert, repr ist offizieller Name


@app.route('/', methods=['POST','GET']) # tells which URL triggers the function
def index():
    if request.method == 'POST':  #Wenn Button gedrüct wird der POST methode verwendet
        task_content = request.form['content'] #ordnet Variable Wert der Eingabe zu
        new_task = Todo(content=task_content) #Erschafft neuen Eintrag über Klasse

        try:
            db.session.add(new_task)  #fügt Eintrag zur aktiven Datenbank hinzu
            db.session.commit()  #Bestätigt Eintrag
            return redirect('/')  #Zurück zum Index
        except:  #nimmt jede Art von Ausnahme
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  #gibt alle Einträge in Datenbank aus
        return render_template('index.html', tasks=tasks) #ruft Seite auf, gibt Variable weiter
@app.route('/delete/<int:id>')  #Unterseite delete mit integer als id, Variable in <...>
def delete(id):  #wird durch Aufrufen des Links oben ausgelöst
    task_to_delete = Todo.query.get_or_404(id)  #holt Task mit vorgegebener id oder zeigt 404
    try:
        db.session.delete(task_to_delete)
        db.session.commit()  #bestätigt Eingabe
        return redirect('/')  #Zurück zur HP
    except:
        return 'There was an error deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']  #get data from input form
        try:
            db.session.commit()  #commit changes
            return redirect('/')
        except:
            return 'There was an issue updating the task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)