# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, redirect, render_template, session, make_response
from flask_session import Session
from operator import itemgetter

import random
import json
import boto3
import uuid
from PIL import Image
from datetime import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

AWSKEY = 'AKIAVRUVVOGIQRYMIFGG'
AWSSECRET = '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'
PUBLIC_BUCKET = 'ai55853n-web-public'
STORAGE_URL = 'http://ai55853n-web-public.s3-website.us-east-2.amazonaws.com'


def get_table(name):
    client = boto3.resource(service_name='dynamodb',
                        region_name='us-east-2',
                        aws_access_key_id=AWSKEY,
                        aws_secret_access_key=AWSSECRET)
    table = client.Table(name)
    return table

def add_remember_key(email):
    table = get_table("remember")
    key = str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4())
    item = {"key":key, "email":email}
    table.put_item(Item=item)
    return key

# @app.route('/entry')
# def add_entries_key():
#     table = get_table("entries")
#     uniqueid = request.args.get("uniqueid")
#     title = request.args.get("title")
#     text = request.args.get("text")
#     date = request.args.get("date")

#     item = {"uniqueID":uniqueid, "title": title, "text": text, "date": date}
#     table.put_item(Item=item)


@app.route('/add_blog')
def add_blog():
    title = request.args.get("title")
    text = request.args.get("text")
    uniqueID = str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4())

    table = get_table("entries")


    current_datetime = datetime.now()
    current_date_time = current_datetime.strftime("%Y/%m/%d %H:%M:%S")

    item = {"uniqueID":uniqueID, "title": title, "text": text, "date":current_date_time}
    table.put_item(Item=item)
    result = {'result':'OK'}

    response = make_response(result)
    return response

@app.route('/list_blog')
def list_blog():
    table = get_table('entries')
    results = []
    for item in table.scan()['Items']:
        uniqueID = item['uniqueID']
        title = item['title']
        text = item['text']
        date = item['date']
        stud = {'uniqueID': uniqueID,'title':title, 'text':text, 'date':date}
        results.append(stud)
    # Sort
    results = sorted( results, key=itemgetter('date'), reverse=True)
    return {'results':results}

@app.route('/delete')
def delete_item():
    table = get_table('entries')
    uniqueID = request.args.get("id")
    table.delete_item(Key={"uniqueID":uniqueID})

    return redirect("editor.html")



@app.route('/')
def home():
    return render_template("blog.html")

@app.route('/thing')
def thing():
    return session["thing"]


@app.route('/login')
def login():
    email = request.args.get("email")
    password = request.args.get("password")

    table = get_table("users")
    item = table.get_item(Key={"email":email})

    if 'Item' not in item:
        return {'result':'Email not found.'}

    user = item['Item']

    if password != user['password']:
        return {'result':'Password does not match.'}

    session["email"] = user["email"]
    session["username"] = user["username"]

    result = {'result':'OK'}

    response = make_response(result)

    remember = request.args.get("remember")
    if(remember == "no"):
        response.delete_cookie("remember")
    else:
        key = add_remember_key(user["email"])
        response.set_cookie("remember", key, max_age=60*60*24*14) # Remember for 14 days

    return response


def auto_login():
    cookie = request.cookies.get("remember")
    if cookie is None:
        return False

    table = get_table("remember")
    result = table.get_item(Key={"key":cookie})
    if 'Item' not in result:
        return False


    remember = result['Item'] # row in the remember me table

    table = get_table("users")
    result = table.get_item(Key={"email":remember["email"]})

    user = result[ 'Item'] # row from users table

    session["email"] = user["email"]
    session["username"] = user["username"]

    return True


def is_logged_in():
    if not session.get("email"):
        return auto_login()
    return True


# @app.route('/account.html')
# def account():
#     if not is_logged_in():
#         return redirect("/")

#     return render_template("account.html", username=session["username"])


@app.route('/editor.html')
def editor():
    if not is_logged_in():
        return render_template("login.html")
    return render_template("editor.html", username=session["username"])

@app.route('/logout.html')
def logout():
    session.pop("email", None)
    session.pop("username", None)

    response = make_response(redirect("/"))
    response.delete_cookie("remember")
    return response

"""
@app.route('/listfiles')
def api_listfiles():
    bucket = get_public_bucket()
    items = []
    for item in bucket.objects.all():
        items.append(item.key)
    return {'url':STORAGE_URL, 'items':items }


@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    bucket = get_public_bucket()
    file = request.files["file"]
    filename = file.filename
    caption = request.form.get('caption')

    # DB stuff
    table = get_table('images')
    id = str(uuid.uuid4())
    user = {'id':id, 'caption':caption, 'filename':filename}
    table.put_item(Item=user)

    ct = 'image/jpeg'
    if filename.endswith('.png'):
        ct = "image/png"
    bucket.upload_fileobj(file, filename, ExtraArgs={'ContentType': ct})
    return {'results':'OK'}


@app.route('/listimages')
def listimages():
    table = get_table('images')
    results = []
    for item in table.scan()['Items']:
        id = item['id']
        caption = item['caption']
        filename = item['filename']
        stud = {'id':id, 'caption':caption, 'filename':filename}
        results.append(stud)

    return {'results':results}

# @app.route('/liststudents')
# def liststudents():
#     table = get_table('students')
#     results = []
#     for item in table.scan()['Items']:
#         firstname = item['firstname']
#         lastname = item['lastname']
#         email = item['email']
#         stud = {'firstname':firstname, 'lastname':lastname, 'email':email}
#         results.append(stud)

#     return {'results':results}




@app.route('/liststudents')
def liststudents():
    table = get_table('students')
    results = []
    for item in table.scan()['Items']:
        firstname = item['firstname']
        lastname = item['lastname']
        email = item['email']
        stud = {'firstname':firstname, 'lastname':lastname, 'email':email}
        results.append(stud)

    return {'results':results}


@app.route('/hello')
def hello():
    return '<h1><b>Carmine</b> says Hello!</h1>'

@app.route('/dice')
def dice():
    x = random.randint(1, 6)
    result = 'Your roll was <b>' + str(x) + '</b>'
    return result

@app.route('/pizza')
def pizza():
    pizzas = [
        {'name':'Plain', 'price':10.50},
        {'name':'Pepperoni', 'price':12.75},
        {'name':'Grandmas', 'price':14.00},
        {'name':'Meat Lovers', 'price':18.75}
        ]
    p = random.choice(pizzas)
    return p

@app.route('/add')
def add():
    a = request.args.get('a')
    b = request.args.get('b')
    total = int(a) + int(b)
    return 'I added those for you: ' + str(total)


@app.route('/catalog/<search>')
def catalog(search):
    f = open('/home/thunderlegend/mysite/data/courses.json')
    courses = json.load(f)
    f.close()

    result_list = []
    for c in courses:
        if c['number'].lower().startswith(search.lower()) or search.lower() in c['name'].lower():
            result_list.append(c)

    return { 'result':result_list }

@app.route('/apt/<search>/<beds>/<sort>')
def apt(search, beds, sort):
    f = open('/home/thunderlegend/mysite/data/apartments.json')
    apartments = json.load(f)
    f.close()

    result_list = []

    # filter
    for a in apartments:
        if search.lower() in a['title'].lower() or search.lower() in a['description'].lower():
            if a['beds'] >= int(beds):
                result_list.append(a)

    # Sort
    if sort == "1":
        result_list = sorted( result_list, key=lambda d: d['monthly rent'])

    elif sort == "2":
        result_list = sorted( result_list, key=itemgetter('monthly rent'), reverse=True)



    return { 'result':result_list }


@app.route('/date/<search>/<beds>/<sort>')
def date(search, beds, sort):
    f = open('/home/thunderlegend/mysite/data/apartments.json')
    apartments = json.load(f)
    f.close()

    result_list = []

    # filter
    for a in apartments:
        if search.lower() in a['title'].lower() or search.lower() in a['description'].lower():
            if a['beds'] >= int(beds):
                result_list.append(a)

    # Sort
    if sort == "1":
        result_list = sorted( result_list, key=lambda d: d['monthly rent'])

    elif sort == "2":
        result_list = sorted( result_list, key=itemgetter('monthly rent'), reverse=True)



    return { 'result':result_list }




@app.route('/seidenberg')
def seidenberg():
    return redirect('https://www.pace.edu/seidenberg')

"""