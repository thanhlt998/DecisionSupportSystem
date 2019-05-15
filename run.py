from flask import Flask, render_template, redirect, url_for, request
import model
from settings import *
from NLP import NLP
from queue import Queue
from multiprocessing import Process
from werkzeug.serving import run_simple
import sys, subprocess, time
import importlib, os
import threading

# app = Flask(__name__, static_folder='templates/static')

 
# @app.route('/')
# def welcome():
#     return redirect('/login')
 
to_reload = True
def get_app(): 
    app = Flask(__name__, static_folder='templates/static')
    print("newApp")
    @app.route('/result', methods=['GET', 'POST'])
    def resultGUI():
        error = None
        if request.method == 'GET':
            return redirect('/')
        else:
            price = int(request.form['price'])
            platforms = request.form.getlist('plat')
            types = request.form.getlist('typ')
            listGame = model.process(search_url=model.get_search_link(types), price=price, platform_list=platforms)
            
            return render_template('result.html', error=error, result_list=listGame)

 
# Route for handling the login page logic
    @app.route('/', methods=['GET', 'POST'])
    def findGUI():
        error = None
        if request.method == 'POST':
            if int(request.form['price']) < 500:
                error = 'Invalid Credentials. Please try again.'
            else:
                return redirect(url_for('home'))

        return render_template('index.html', error=error, typeList = GAME_TAGS.keys(), platformList=PLATFORMS)

    def reset():
        time.sleep(0.02)
        os.execl(sys.executable, sys.executable, *sys.argv)
        
    @app.route('/reload', methods=['GET','POST'])
    def reload():        
        if request.method == 'POST':
            # print("jumping to index")
            x = threading.Thread(target=reset)
            x.start()
            
        return redirect('/')

    return app

 
class AppReloader(object):
    def __init__(self, create_app):
        self.create_app = create_app
        self.app = create_app()

    def get_application(self):
        global to_reload
        if to_reload:
            self.app = self.create_app()
            to_reload = False

        return self.app

    def __call__(self, environ, start_response):
        app = self.get_application()
        return app(environ, start_response)
 
if __name__ == '__main__':
    application = AppReloader(get_app)

    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)
