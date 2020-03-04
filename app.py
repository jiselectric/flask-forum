from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pickle as pk

app = Flask(__name__)
app.secret_key = "jiselectric"

RESPONSE_SUCCES = "success"
RESPONSE_FAIL = "fail"

try:
    f = open("user.db", "rb")
    users = pk.load(f)
    f.close()
except:
    users = {}

# Articles
myArticles = [{"article_id": 1,
               "title": "Come Together.",
               "content": "I buried Paul.",
               "author": "beatles"},
              {"article_id": 2,
               "title": "I Can't Get No (Satisfaction).",
               "content": "She's like a rainbow",
               "author": "rollingstones"},
              {"article_id": 3,
               "title": "There Is A Light That Never Goes Out.",
               "content": "500 Days of Summer.",
               "author": "jikim"}
              ]


# Main Page - Log In & Articles Page
@app.route('/session_check')
def session_check():
    if "username" in session:
        return RESPONSE_SUCCES
    else:
        return RESPONSE_FAIL


@app.route('/test')
def testest():
    return render_template('test.html', testString='hi')


@app.route('/articles')
def login():
    return render_template('articles.html')


@app.route('/getArticleTitles')
def getArticleTitles():
    return jsonify(myArticles)


# Verify Log In Data
@app.route('/login_check', methods=['GET', 'POST'])
def login_check():
    id = request.form.get("id")
    pw = request.form.get("pw")

    if request.method == 'POST':
        if id not in users:
            return render_template('alert.html', message="No Matching Account.", back=True)
        elif users[id] != pw:
            return render_template('alert.html', message="Wrong Password.", back=True)
        else:
            session["username"] = id
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


# After Log In
@app.route('/content')
def content():
    articleID = request.args.get('article_id')
    if 'username' not in session:
        return "<script>alert('Login Needed.');location.href='/articles';</script>"
    else:

        # session 은 발급되어있음
        # TODO : 내가 선택한 게시글의 author가 session['username']과 일치하는지 확인
        for article in myArticles:
            if article['article_id'] == int(articleID):
                if article['author'] == session['username']:
                    return render_template('content.html', aid=articleID)
                else:
                    return render_template('alert.html', message="No Access to Content", back=True)
        return render_template('alert.html', message="No Available Content", back=False)


@app.route('/getContent')
def getContent():
    aid = request.args.get('article_id')

    for article in myArticles:
        if article['article_id'] == int(aid):
            return jsonify(article)

    return jsonify([])


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/regist', methods=["POST"])
def regist():
    id = request.form.get("id")
    pw = request.form.get("pw")

    if id not in users:
        users[id] = pw
        f = open("user.db", "wb")
        pk.dump(users, f)
        f.close()
        return "Account Created"
    else:
        return "Cannot Create"


# ID Check
@app.route('/id_check', methods=["POST"])
def id_check():
    id = request.form.get("id")
    if id in users:
        return "already"
    else:
        return "available"


# Check Users
@app.route('/users')
def getUsers():
    return str(users)


# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)

    return 'success'


app.run()