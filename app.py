from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import json
from datetime import date



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@127.0.0.1/omnivox'
app.config['SECRET_KEY'] = 'votre_secret_key_ici'
db = SQLAlchemy(app)


class CoursGestion(db.Model):
    __tablename__ = 'cours_gestion'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    programme = db.Column(db.String(100))
    description = db.Column(db.String(500))
    nombre_heures = db.Column(db.Integer)
    prof = db.Column(db.String(100))
    salle = db.Column(db.String(100))
    heure = db.Column(db.Time)
    date_limite = db.Column(db.Date,nullable=True)


class Etudiant(db.Model):
    __tablename__ = 'etudiant'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    code_permanent = db.Column(db.String(20), unique=True)
    mot_de_passe = db.Column(db.String(80))
    cours = db.relationship('CoursGestion', secondary='association', backref='etudiants')

class Cours(db.Model):
    __tablename__ = 'cours'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    raison = db.Column(db.String(200))


association = db.Table('association',
    db.Column('etudiant_id', db.Integer, db.ForeignKey('etudiant.id')),
    db.Column('cours_id', db.Integer, db.ForeignKey('cours_gestion.id'))
)



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        code_permanent = request.form.get('code_permanent')
        mot_de_passe = generate_password_hash(request.form.get('mot_de_passe'))
        nouvel_etudiant = Etudiant(nom=nom, prenom=prenom, code_permanent=code_permanent, mot_de_passe=mot_de_passe)
        db.session.add(nouvel_etudiant)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('inscription.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code_permanent = request.form.get('code_permanent')
        mot_de_passe = request.form.get('mot_de_passe')
        etudiant = Etudiant.query.filter_by(code_permanent=code_permanent).first()
        if etudiant and check_password_hash(etudiant.mot_de_passe, mot_de_passe):
            session['etudiant_id'] = etudiant.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'etudiant_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/choisir_cours')
def choisir_cours():
    if 'etudiant_id' not in session:
        return redirect(url_for('login'))
    cours_disponibles = CoursGestion.query.all()
    return render_template('ajout_cours.html', cours_disponibles=cours_disponibles)

@app.route('/ajout_cours', methods=['POST'])
def ajouter_cours_etudiant():
    if 'etudiant_id' not in session:
        return redirect(url_for('login'))

    titre_cours = request.form.get('titre')
    etudiant = Etudiant.query.get(session['etudiant_id'])

    cours_existant = CoursGestion.query.filter_by(titre=titre_cours).first()
    if cours_existant:
        etudiant.cours.append(cours_existant)
        db.session.commit()
        flash('Le cours a été ajouté avec succès.')
    else:
        flash('Le cours demandé n\'existe pas.')

    return redirect(url_for('mes_cours'))



@app.route('/ajouter_cours', methods=['GET'])
def afficher_formulaire_ajout_cours():
    
    return render_template('ajout_cours.html')



@app.route('/mes_cours')
def mes_cours():
    if 'etudiant_id' not in session:
        return redirect(url_for('login'))
    etudiant = db.session.get(Etudiant, session['etudiant_id'])

    return render_template('mes_cours.html', cours=etudiant.cours)


@app.route('/abandonner_cours/<int:cours_id>')
def abandonner_cours(cours_id):
    if 'etudiant_id' not in session:
        return redirect(url_for('login'))

    etudiant = Etudiant.query.get(session['etudiant_id'])
    db.session.refresh(etudiant) 
    cours = CoursGestion.query.get(cours_id)

    
    if cours.date_limite and cours.date_limite < date.today():
        flash("Attention, vous aurez une mention d'échec si vous abandonnez ce cours après la date limite!", "warning")
        return redirect(url_for('mes_cours')) 
    cours = CoursGestion.query.get(cours_id)
    etudiant.cours.remove(cours)
    db.session.commit()
    flash("Cours abandonné avec succès.", "success")
    return redirect(url_for('mes_cours'))


@app.route('/mon_emploi')
def mon_emploi():
    if 'etudiant_id' not in session:
        return redirect(url_for('login'))

    etudiant = Etudiant.query.get(session['etudiant_id'])
    cours_inscrits = etudiant.cours

    cours_data = []
    for cours in cours_inscrits:
        cours_data.append({
            'title': cours.titre,
            'start': cours.heure.isoformat()
        })

    cours_data_js = jsonify(cours_data).data.decode("utf-8")
    return render_template('emploi.html', cours_data_js=cours_data_js)



@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        code_admin = request.form.get('code_admin')
        mot_de_passe = request.form.get('mot_de_passe')
        if code_admin == "admin" and mot_de_passe == "1111":
            session['admin_id'] = code_admin
            return redirect(url_for('admin'))
    return render_template('login_admin.html')

@app.route('/ajouter_cours_admin', methods=['GET', 'POST'])
def ajouter_cours_admin():
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))
    if request.method == 'POST':
        titre = request.form.get('titre')
        programme = request.form.get('programme')
        description = request.form.get('description')
        nombre_heures = request.form.get('nombre_heures')
        prof = request.form.get('prof')
        salle = request.form.get('salle')
        heure = request.form.get('heure')
        date_limite = request.form.get('date_limite')  
        
        if not date_limite:
            date_limite = None

        nouveau_cours = CoursGestion(
            titre=titre, 
            programme=programme, 
            description=description, 
            nombre_heures=nombre_heures, 
            prof=prof, 
            salle=salle, 
            heure=heure,
            date_limite=date_limite
        )
        db.session.add(nouveau_cours)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('ajouter_cours_admin.html')


@app.route('/admin')
def admin():
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))
    return render_template('ajouter_cours_admin.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
