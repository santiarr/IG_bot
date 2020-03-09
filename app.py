from flask import render_template, request, Flask, redirect
from IGbot import Bot

app = Flask(__name__)
app.static_folder = 'static'
app.tags = ''
app.username = ''
app.password = ''
app.hashtags = []
app.added = []
app.numcomments = 1
app.numlikes =1
@app.route('/')
def index():
    app.hashtags = []
    app.added = []
    return render_template('index.html')

@app.route('/', methods=['POST'])
def getValue():
    app.username = request.form["username"]
    app.password = request.form["password"]
    app.numlikes = request.form['num-likes']
    app.numcomments = request.form['num-comments']
    return redirect('/next')

@app.route('/next')
def next():
    return render_template('addtags.html')

@app.route('/next', methods=['POST'])
def getValue2():
    t = request.form['hashtags']
    if t not in app.hashtags:
        app.hashtags.append(t)
    for tag in app.hashtags:
        if tag not in app.added:
            if not tag =='':
                app.tags += '#{tag}, '.format(tag=tag)
                app.added.append(tag)

    return render_template('tagAdded.html', tags=app.tags)


@app.route('/startbot', methods=['POST'])
def startBot():
    tags = app.hashtags
    return render_template('success.html'), Bot(app.username, app.password, tags, numcomment=app.numcomments, numlike=app.numlikes, topPosts=False)

