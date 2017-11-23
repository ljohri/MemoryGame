'''# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)'''


from timeit import default_timer as timer

import logging
import sqlite3
import signal
import sys
import time
import random

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request, context, version


################################################################################
#db functions

def insert(device_id, name, session, type,duration,score,timeofday) :
    val = (device_id,name,session,type,duration,score,timeofday)    
    print(val)
    c.execute('INSERT INTO ' + table_name + ' VALUES (?,?,?,?,?,?,?)',val)    

def num_rows():
    c.execute("SELECT * FROM " + table_name)
    rows = c.fetchall()
    return len(rows)

def print_game():
    c.execute("SELECT * FROM " + table_name)
    rows = c.fetchall()
    for row in rows:
        print(row)

def get_last_user():
    #SELECT user,timeofday FROM dbtable ORDER BY timeofday LIMIT 1
    t = ('GAME',)
    c.execute('SELECT name,type, timeofday from ' + table_name + ' WHERE type = ? ORDER BY timeofday DESC LIMIT 1 ',t)   
    row = c.fetchall()
    print(row) 
    if len(row) :
        return row[0][0]
    else :
        return 'ChotaKutta'    
 

def insert_test() :
    device_id = random.randint(0,100)
    name = 'Bunty' + str(device_id)
    session = 'Test'    
    type = 'NO_GAME'
    duration = random.randint(9,20)
    score = random.randint(1000,2000)
    epochtime = time.time()

    initial_rows = num_rows()
    insert(device_id=device_id,name=name,type=type,session=session,\
        duration=duration, score=score ,timeofday = epochtime)
    if num_rows()-initial_rows == 1 :
        print('row insertion test passed. Rows: ',initial_rows+1)
        get_last_user()

def signal_handler(signal, frame):
        print('exception detected')
        if conn:
            #print_game() 
            commit()   
            dbclose()
        sys.exit(0)

def dbopen():
    myconn = sqlite3.connect(db_filename)
    return (myconn,myconn.cursor())

def commit():
    conn.commit()

def dbclose():
    conn.close()

################close db functions###########################


#start
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

#########Game Constants
level=5

#open db
signal.signal(signal.SIGINT, signal_handler)
db_filename = 'memorygame.sq3db'
table_name = 'game3'
(conn,c) = dbopen()
insert_test()
 


@ask.launch
def new_game():
    print('Entering new game')
    last_user = get_last_user();
    print(last_user)

    session.attributes['state'] = 'launch'
    session.attributes['user'] = last_user
    session.attributes['start_time'] = timer()
    welcome_msg = render_template('welcome',user=last_user)
    return  question(welcome_msg)

@ask.intent("start")

@ask.intent("UserIntent")
def set_user(user):
    session.attributes['user'] = user
    mysession = 'FIRST'    
    type = 'GAME'
    duration = 0
    score = 0
    epochtime = time.time()
    insert(device_id=context.System.device.deviceId,name=user,type=type,session=mysession,\
        duration=duration, score=score ,timeofday = epochtime)
    return question('user set to ' + user + '  Start Now?')


@ask.session_ended
def ask_session_ended():
    return '{}',200

@ask.intent("NoIntent")
def endit():
    return statement(render_template('bye'))

@ask.intent("YesIntent")
def next_round():
    numbers = [randint(0, 9) for _ in range(level)]
    round_msg = render_template('round', numbers=numbers)
    session.attributes['numbers'] = numbers[::-1]  # reverse
    session.attributes['start_time'] = timer()
    return question(round_msg)



@ask.intent("LevelIntent", convert={'level':int})
def level_fix(level):
    print('Entering level intent')
    print('your level is {{level}}')

    numbers = [randint(0, 9) for _ in range(level)]
    session.attributes['numbers'] = numbers[::-1]  # reverse

    level_msg = render_template('level_round',level=level, numbers=numbers)
    
    session.attributes['start_time'] = timer()
    return question(level_msg) 



@ask.intent("AnswerIntentE", convert={'first': int, 'second': int, 'third': int,'fourth':int,'fifth':int})
def answer(first, second, third,fourth,fifth):
    score = int(((timer() - session.attributes['start_time'])-9.0)*1000)
    winning_numbers = session.attributes['numbers']

    if [first, second, third,fourth,fifth] == winning_numbers:
        msg = render_template('win',delta=score)
        user=session.attributes['user'] 
        mysession = 'FIRST'    
        type = 'GAME'
        duration = 0
        score = score
        epochtime = time.time()
        insert(device_id=context.System.device.deviceId,name=user,type=type,session=mysession,\
        duration=duration, score=score ,timeofday = epochtime)
    else:
        msg = render_template('lose')   
    return question(msg+' Repeat?')


if __name__ == '__main__':
    app.run(debug=False)
        