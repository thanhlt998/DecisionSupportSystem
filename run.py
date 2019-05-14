from flask import Flask, render_template, redirect, url_for, request
from model import *

app = Flask(__name__, static_folder='templates/static')
 
 
# @app.route('/')
# def welcome():
#     return redirect('/login')
 
 
@app.route('/result', methods=['GET', 'POST'])
def resultGUI():
    error = None
    if request.method == 'GET':
        return redirect('/')
    else:
        price = int(request.form['price'])
        platforms = request.form.getlist('plat')
        types = request.form.getlist('typ')
        listGame = process(search_url=get_search_link(types), price=price, platform_list=platforms)
       
        res = [(444, 'https://store.steampowered.com/app/49520/Borderlands_2/?snr=1_7_7_230_150_2', 'Borderlands 2', 19.99, 'PC', 89.0, 8.2, 555, 373),(571, 'https://store.steampowered.com/app/306130/The_Elder_Scrolls_Online/?snr=1_7_7_230_150_1', 'The Elder Scrolls® Online', 19.99, 'PC', 71.0, 5.8, 855, 457), (692, 'https://store.steampowered.com/app/22380/Fallout_New_Vegas/?snr=1_7_7_230_150_7', 'Fallout: New Vegas', 9.99, 'PC', 84.0, 8.7, 636, 467), (1598, 'https://store.steampowered.com/app/620/Portal_2/?snr=1_7_7_230_150_8', 'Portal 2', 9.99, 'PC', 95.0, 9.0, 1827, 1418)]
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
 
 
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)