from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# --- Model integrated here ---
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    summary = db.Column(db.Text)

# --- Create DB and tables ---
with app.app_context():
    db.create_all()

# --- Routes and Views ---
@app.route('/')
def index():
    resumes = Resume.query.all()
    return render_template('index.html', resumes=resumes)

@app.route('/add', methods=['GET', 'POST'])
def add_resume():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        summary = request.form['summary']
        resume = Resume(name=name, email=email, summary=summary)
        db.session.add(resume)
        db.session.commit()
        flash('Resume added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('resume_form.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_resume(id):
    resume = Resume.query.get_or_404(id)
    if request.method == 'POST':
        resume.name = request.form['name']
        resume.email = request.form['email']
        resume.summary = request.form['summary']
        db.session.commit()
        flash('Resume updated!', 'info')
        return redirect(url_for('index'))
    return render_template('resume_form.html', resume=resume)

@app.route('/delete/<int:id>')
def delete_resume(id):
    resume = Resume.query.get_or_404(id)
    db.session.delete(resume)
    db.session.commit()
    flash('Resume deleted!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)