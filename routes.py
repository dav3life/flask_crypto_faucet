from flask_wtf import FlaskForm, RecaptchaField
from flask import render_template, g, request, flash, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from wtforms import StringField
from wtforms.validators import length #, validators
from block_io import BlockIo

from __init__ import app, db, login_manager
from models import User

login_manager.login_view = 'login'

import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)

from decimal import Decimal, getcontext
getcontext().prec = 8

app.logger.info("faucet is restarting")


## register on block io and add the crypto currency you would like this faucet to dispense 
## this app was made primarily for doge coin but bitcoin and litecoin can also be used 

apikey = "your blockio api key "

secretpin = "your blockio secret pin"




version = 2
b = BlockIo(apikey,secretpin,version)

addresses = b.get_my_addresses()
donation_address = addresses['data']['addresses'][0]['address']
network = addresses['data']['network']

# TODO: get this from env or make random?
drip_amount = '10'

import requests

import time
limited = {}
hours_to_wait = 0.5
seconds_to_wait = 60 * 60 * hours_to_wait


class CLaimForm(FlaskForm):
    user = StringField('username', validators=[length(min=0,max=10,message="hello world")])
    recaptcha = RecaptchaField(label='recap', validators=None)


def wow():
    balance = b.get_balance()['data']['available_balance']
    return Decimal(balance)

def very(address):
    response = requests.get('https://chain.so/api/v2/is_address_valid/'+network+'/'+address)
    if response.status_code == 200:
        content = response.json()
        return content['data']['is_valid']
    else:
        return False

def excite(address):
    if address in limited:
        if limited[address] + seconds_to_wait < time.time():
            del limited[address]
            return True
        else:
            return False
    else:
        limited[address] = time.time()
        return True


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/home')
def home():
    user = g.user
    if user.is_active == False:
        return render_template('index.html',
            title = 'Home Page',
            user = '')
    return render_template(
        'index.html',
        title = 'Home Page',
        user = user.get_string()
    )


@app.route('/faq')
@login_required
def faq():
    return render_template(
        'faq.html',
        title = 'faq',
        message = 'Your faq page.'
    )

@app.route('/test')
@login_required
def test():
    return render_template(
        'test.html',
        title = 'test',
        message = 'Your test page.'
    )




@app.route("/faucet", methods=['GET','POST'])
@login_required
def faucet():
    user = g.user
    if user.is_anonymous(): return redirect(url_for('login'))

    counter = user.counter

    balance = wow()
    
    seconds_left = 0

    form = CLaimForm()
    #form.username = user.getstring()
    if form.validate_on_submit():
        tokens = request.form.get('token')
        test_data=tokens
        requested_address = user.get_string()
        if balance > 0 and balance > Decimal(drip_amount):
            if very(requested_address):
                if excite(requested_address):
                    is_request_good = True
                    if user.counter%10.0 == 0 and user.counter != 0: 
                        message = 'A pay out of '+drip_amount+' coins has been sent to your Dogecoin Address'
                        r = b.withdraw(amounts=drip_amount,to_addresses=requested_address)
                    else: 
                        message = 'you have been rewarded 1 more doge coin' 
                    user.counter +=1 
                    db.session.commit()                  
                else:
                    is_request_good = False
                    seconds_left = str( int( ( limited[requested_address] + seconds_to_wait) - time.time() ) )
                    message = ''
            else:
                is_request_good = False
                message = 'The address is not good.'
        else:
            is_request_good = False
            message = 'We are out of coins right now.'
    else:
        is_request_good = False
        requested_address = user.get_string()
        message = ''
    return render_template('faucet.html', 
        is_request_good=is_request_good,
        requested_address=requested_address,
        message=message,
        balance=balance,
        form=form , seconds_left=seconds_left, counter=user.get_counter(), payouts=user.get_counter()/10)





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    blanace = wow()
    if request.method == 'GET':
        return render_template('signup.html')
    username = request.form.get('username')

    if very(username) == False:
        flash('enter a valid doge coin address ')
        return redirect(url_for('signup'))

    filter_user = User.query.filter_by(username=username).first()
    user = User(username=username)
    if filter_user is None:
        user = User(username=username)
        if user is not None:
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(request.args.get('next') or url_for('home'))
        #return redirect(url_for('login'), code=302)
    elif str(filter_user.get_string()) == str(username) :
        login_user(filter_user)

        return redirect(request.args.get('next') or url_for('faucet'))
    return redirect(url_for('home'), code=302)



    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid username or password')
        return render_template('login.html')
    flash('Login successful')
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('faucet'))
 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



#