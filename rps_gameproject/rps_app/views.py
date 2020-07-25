from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Score
from cryptography.fernet import Fernet
import bcrypt
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)
def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

def register(request):
    return render(request, 'register.html')


def check(request):
    name = request.GET.get("Name")
    mail = request.GET.get("MailID")
    passw = request.GET.get("password")
    conn = sqlite3.connect('db.sqlite3')
    cc = conn.cursor()
    cc.execute("SELECT * from rps_app_user where User_Name=? and Mail_id=?", (name, mail))
    records = cc.fetchall()
    #hashable_pw = bytes(passw, encoding='utf-8')
    #hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())
    #print("Total rows are:  ", len(records))
    encrypted = encrypt_password(passw)
    print("encrypted:", encrypted)
    #encrypted=encrypt(passw)
    if len(records) > 0:
        msg = 0
    else:
        cc.execute("INSERT INTO rps_app_user (User_Name, Mail_id,password) VALUES(?, ?,?)",
                   (name, mail, encrypted))
        conn.commit()
        msg = 1
        cc.close()
        conn.close()
    return render(request, 'register.html', {'data': msg})


def login(request):
    return render(request, 'login.html')


def checklogin(request):
    name = request.GET.get("Name")

    passw = request.GET.get("password")
    #hashable_pw = bytes(passw, encoding='utf-8')
    #print(hashable_pw)
    #hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())
    #print(hashed_pw)
    # print(hashed_pw)

    conn = sqlite3.connect('db.sqlite3')
    cc = conn.cursor()
    query_str = "SELECT password from rps_app_user where User_Name='"+name+"'"
    print(query_str)
    #cc.execute("SELECT password from rps_app_user where User_Name=?", (name))
    cc.execute(query_str)
    passwd_from_db = cc.fetchall()
    #if bcrypt.checkpw(passw,hashed_pw):
    print("db---:", type(passwd_from_db))
    print("db---1:", type(passwd_from_db[0]))
    decrypted = check_encrypted_password(passw, passwd_from_db[0][0])
    print(decrypted)
    if decrypted:
        msg = 0
    else:
        msg = 1
    # hashable_pw = bytes(passw, encoding='utf-8')
    # hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())
    cc.close()
    conn.close()
    return render(request, 'login.html', {'data': msg})


def home(request):
    # request.session['c_count'] = 1
    print("session-keys:", request.session.keys())
    request.session['c_count'] = 0
    request.session['user_score'] = 0
    request.session['sys_score'] = 0
    print("session-keys-after:", request.session.keys())
    return render(request, 'home.html')


def newpage(request):
    data_a = request.GET["With"]
    request.session['With'] = data_a
    print("session-keys1:", request.session.keys())

    return render(request, 'newpage.html', {'data': data_a})


def includes(request):
    x = request.session['c_count'] + 1
    request.session['c_count'] = x
    print("session-keys2:", request.session.keys())
    msg = ''
    # request.session['c_count'] =
    b = request.GET["user_input"]
    data_c = 'Your choice:' + b
    print(data_c)
    import random

    ran = ['Rock', 'Paper', 'Scissor']
    system = []
    user = []
    user_sys = {'Rock-Paper': [0, 1], 'Paper-Scissor': [0, 1], 'Rock-Scissor': [1, 0], 'Paper-Rock': [1, 0],
                'Scissor-Paper': [1, 0], 'Scissor-Rock': [0, 1], 'Rock-Rock': [0, 0], 'Paper-Paper': [0, 0],
                'Scissor-Scissor': [0, 0]}
    sys_points = []
    score = []
    user_points = []
    sys_points = []
    user.append(b);
    c = random.choice(ran);
    # print(c)
    # print("computer choice:", c)
    d = 'System choice :' + c
    val = (b + '-' + c)
    print(val)
    system.append(c);
    for key, value in user_sys.items():
        if val == key:
            print(value)
            user_points.append(user_sys[val][0])
            sys_points.append(user_sys[val][1])
            print('You scored %d' % (user_sys[val][0]))
            val1 = "You scored:" + str(user_sys[val][0])
            dd = user_sys[val][0]
            request.session['user_score'] = request.session['user_score'] + user_sys[val][0]
            print('Computer has scored %d' % (user_sys[val][1]))
            dd1 = user_sys[val][1]
            request.session['sys_score'] = request.session['sys_score'] + user_sys[val][1]
            val2 = "Computer scored:" + str(user_sys[val][1])
    u = sum(user_points)
    s = sum(sys_points)
    print("Total points of Yours is %d" % (request.session['user_score']))
    print("Total points of computer is %d" % (request.session['sys_score']))
    if (u > s):
        win = "You are the winner"
    elif (u < s):
        win = "Computer is winner"
    else:
        win = "Draw match"

    if request.session['c_count'] == 5:
        conn = sqlite3.connect('db.sqlite3')
        cc = conn.cursor()
        cc.execute("INSERT INTO rps_app_score (Player_score, System_score) VALUES(?, ?)",
                   (request.session['user_score'], request.session['sys_score']))
        conn.commit()
        print("Data added to database successfully")
        cc.close()
        conn.close()
        if request.session['user_score'] > request.session['sys_score']:
            msg = "You Won the Game"
        else:
            msg = "System Won the Game"
    return render(request, 'includes.html',
                  {'data': data_c, 'c': d, 'v': val1, 'v1': val2, 'ww': win, 'user': request.session['user_score'],
                   'system': request.session['sys_score'], 'mm': msg})


#
#
from django.shortcuts import render
