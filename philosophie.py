#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

#  globale cache
cache = {}

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"


@app.route('/', methods=['GET'])
def index():
    # initialisation
    session['score'] = 0
    session['title'] = ''
    session['content'] = []
    return render_template('index.html', message="Ready for a new game ?")


@app.route('/new-game', methods=['POST'])
def new_game():
    if request.method == 'POST':
        # vérification de la première selection
        if request.form['query'].lower() == 'philosophie':
            flash('Cheater !', 'lose')
            return redirect('/')
        else:
            # sauvegarde du choix du joueur
            session['article'] = request.form['query']
            return redirect('/game')


@app.route('/game', methods=['GET'])
def game():
    # recherche dans le cache
    if session['article'] in cache.keys():
        session['title'], session['content'] = cache[session['article']]
        return render_template('game.html', message="Game Started !")
    else:
        # appel à l'API
        session['title'], session['content'] = getPage(session['article'])
        # verification du retour de l'API
        if session['content'] == []:
            if session['score'] > 0:
                flash('You Lose !', 'lose')
                flash('Final Score : ' + str(session['score']), 'lose')
            else:
                flash('Try another research !', 'other')
            return redirect('/')
        elif session['title'] is None:
            flash('Page inexistante !', 'lose')
        else:
            cache[session['article']] = [session['title'], session['content']]
            return render_template('game.html', message="Enjoy !")


@app.route('/move', methods=['POST'])
def move():
    if session['content'][int(request.form['selected']) - 1].lower() == 'philosophie' or session['title'].lower() == 'philosophie':
        if session['score'] > 0:
            flash('You WIN !!!!', 'win')
            flash('Final Score : ' + str(session['score']), 'win')
        else:
            flash('Cheater never win !', 'lose')
        return redirect('/')
    else:
        if session['score'] == int(request.form['current_score']):
            session['score'] += 1
            session['article'] = session['content'][int(request.form['selected']) - 1]
            return redirect('/game')
        else:
            flash('Tentative de fraude détecté !', 'lose')
            return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
