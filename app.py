from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pickle as pk
app = Flask(__name__)
app.secret_key = "jiselectric"

try:
    f = open("user.db", "rb")
    users = pk.load(f)
    f.close()
except:
    users = {}

# Articles
myArticles = [{"article_id" : 1,
            "title" : "Come Together.",
            "content" : "I buried Paul.",
            "author" : "beatles"},
            {"article_id" : 2,
            "title" : "I Can't Get No (Satisfaction).",
            "content" : "She's like a rainbow",
            "author" : "rollingstones"},
            {"article_id" : 3,
            "title" : "There Is A Light That Never Goes Out.",
            "content" : "500 Days of Summer.",
            "author" : "jikim"}
            ]

# Main Page - Log In & Articles Page
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
            return "No Matching Account."
        elif users[id] != pw:
            return "Wrong Password."
        else:
            session["username"] = id
            return "success"

# After Log In
@app.route('/content')
def content():
    articleAuthor = request.args.get('author')

    if 'username' not in session:
        return "<script>alert('Login Needed.');location.href='/articles';</script>"
    elif 'username' in session:
        for article in myArticles:
            if article['author'] == id:
                return render_template('content.html', articleAuthor)
            else:
                return "<script>alert('No Access to Content');</script>"

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
    session.pop('login_id', None)
    return 'success'


app.run()