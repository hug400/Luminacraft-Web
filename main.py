from flask import Flask, render_template, request, session, url_for, redirect
import pymongo
import os
import bcrypt

# Création de l'appli
app = Flask(__name__)
mongo = pymongo.MongoClient("mongodb+srv://Hug400:<axel2012>@cluster0.cimtd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

#cookie de connexion
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    Luminacraft_annoncewiki = mongo.Luminacraft.Annonce
    annonce = Luminacraft_annoncewiki.find({})
    if 'util' in session :
        return render_template('index.html', annonce=annonce, nom=session['util'])
    else:
        return render_template('index.html', annonce=annonce)

@app.route('/wiki')
def wiki():

    return render_template('wiki.html')

@app.route('/bddtest')
def test():
    Luminacraft_test = mongo.Luminacraft.test
    test = Luminacraft_test.find({})
    return render_template('test.html' , test=test)

#############
#Utilisateur#
#############

@app.route('/register', methods={'POST', 'GET'})
def register():
    if request.method == 'POST':
        Luminacraft_utils = mongo.Luminacraft.Utilisateur
        if (Luminacraft_utils.find_one({'nom' : request.form['pseudo']})):
            return render_template('register.html', erreur="Ce pseudo existe déja")
        else:
            if (request.form['mot_de_passe'] == request.form['verif_mot_de_passe']):
                #Cryptage
                mdp_encrypte = bcrypt.hashpw(request.form['mot_de_passe'].encode('utf-8'), bcrypt.gensalt())
                Luminacraft_utils.insert_one({
                    'nom': request.form['pseudo'],
                    'mdp': mdp_encrypte
                })
                session['util'] = request.form['pseudo']
                return redirect(url_for('index'))
            else:
                return render_template('register.html', erreur="Les mots de passe doivent être identiques")
    else:
        return render_template('register.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        Luminacraft_utils = mongo.Luminacraft.Utilisateur
        util = Luminacraft_utils.find_one({'nom' : request.form['pseudo']})
        if util : 
            if bcrypt.checkpw(request.form['mot_de_passe'].encode('utf-8'), util['mdp']):
                session['util'] = request.form['pseudo']
                return redirect(url_for("index"))
            else : 
                return render_template('login.html', erreur = "Le mot de passe est incorect 🤖 ")
        else : 
            return render_template('login.html', erreur = "Le nom d'utilisateur est incorect ou n'existe pas 🤖 ")
    else : 
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


#Fin d'Utilisateur



# Toujour en bas du fichier main.py
# Palette de couleur : 
# https://coolors.co/palette/90f1ef-ffd6e0-ffef9f-c1fba4-7bf1a8
# https://coolors.co/palette/bcf4f5-b4ebca-d9f2b4-d3fac7-ffb7c3
# https://coolors.co/palette/d7fff1-aafcb8-8cd790-77af9c-285943

app.run(host='0.0.0.0', port=81)