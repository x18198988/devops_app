from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from weasyprint import HTML

app = Flask(__name__)
app.secret_key = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Model
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    summary = db.Column(db.Text)
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)

with app.app_context():
    db.create_all()

# Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/resumes')
def index():
    resumes = Resume.query.all()
    return render_template('index.html', resumes=resumes)

@app.route('/add', methods=['GET', 'POST'])
def add_resume():
    if request.method == 'POST':
        resume = Resume(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            linkedin=request.form['linkedin'],
            github=request.form['github'],
            summary=request.form['summary'],
            skills=request.form['skills'],
            experience=request.form['experience'],
            education=request.form['education']
        )
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
        resume.phone = request.form['phone']
        resume.linkedin = request.form['linkedin']
        resume.github = request.form['github']
        resume.summary = request.form['summary']
        resume.skills = request.form['skills']
        resume.experience = request.form['experience']
        resume.education = request.form['education']
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

@app.route('/view/<int:id>')
def view_resume(id):
    resume = Resume.query.get_or_404(id)
    return render_template('view_resume.html', resume=resume)

@app.route('/download/<int:id>')
def download_pdf(id):
    resume = Resume.query.get_or_404(id)
    rendered = render_template('view_resume.html', resume=resume)
    pdf = HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={resume.name}_resume.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
