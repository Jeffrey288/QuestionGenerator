from flask import Flask, render_template, request, abort, url_for, flash, redirect, make_response
from modules.vector_proj import vector_proj
from modules.system_of_eq import system_of_eq
from markdown import markdown
import regex as re
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import random, string
import os

import pymongo
import config
print(pymongo.version)

# https://www.mongodb.com/community/forums/t/secure-way-to-connect-to-mongodb-atlas-from-pythonanywhere/14323/3
# https://help.pythonanywhere.com/pages/MongoDB
client = pymongo.MongoClient(f"mongodb+srv://{config.db_username}:{config.db_password}@cluster0.a6atwar.mongodb.net/?retryWrites=true&w=majority", \
    connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db = client.website
projects_db = db.projects
# projects.create_index('post_id', unique=True)
# print(projects.index_information())

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hey'

UPLOAD_FOLDER = 'static/assets/projects'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           get_extension(filename) in ALLOWED_EXTENSIONS
def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()
           
@app.route('/upload', methods=("POST", ))
def project_upload_image():

    if 'file' not in request.files:
        return ('', 204)
    file = request.files['file']
    if file.filename == '':
        return ('', 204)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        extension = get_extension(filename)
        while True:
            new_filename = ''.join(random.choices(string.ascii_lowercase+string.digits, k=15)) + "." + extension
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + "/" + new_filename): break
        file.save(app.config['UPLOAD_FOLDER'] + "/" + new_filename) # app.config['UPLOAD_FOLDER'] + "/" +
        response = make_response(new_filename, 200)
        response.mimetype = "text/plain"
        return response
    return ('', 204)

@app.route('/project-template')
def projects_template():
    return render_template('project-template.html', get={})

@app.route('/projects')
def list_projects():
    posts = projects_db.find({}, {"content": 0})
    count = projects_db.count_documents({})
    return render_template('projects.html', posts=posts, count=count, enable_editing=config.enable_editing)

@app.route('/projects/<string:post_id>')
def display_project(post_id):
    # print(post_id)
    # print('heyyyy')
    pages = projects_db.find({'post_id': post_id})
    try:
        page = pages[0]
    except:
        abort(404)
    # print(pages[0])
    return render_template('project-template.html', get=page, enable_editing=config.enable_editing)

@app.route('/projects/<string:post_id>/edit', methods=('GET', 'POST'))
def edit_project(post_id):
    if config.enable_editing: 
        pages = projects_db.find({'post_id': post_id})
        try:
            page = pages[0]
        except:
            abort(404)
        if request.method == "POST":
            # print("THE FORM", request.form)
            if (not 'title' in request.form.keys()): return ('', 204)
            if (request.form.get('title', '') == ''):
                # flash('Title is required!')
                print("something", request.form.get('title', ''))
                return render_template('project-editor.html', get=page)
            projects_db.update_one({'post_id': post_id}, {
                "$set": {
                    'title': request.form.get('title', ''),
                    'desc': request.form.get('desc', ''),
                    'date': request.form.get('date', ''),
                    'tags': request.form.get('tags', ''),
                    'icon': request.form.get('icon', ''),
                    'content': request.form.get('content', '')
                }
            })
            # return redirect(url_for('display_project', post_id='f'))
            return redirect(url_for('display_project', post_id=post_id))
            # return redirect(url_for('index'))
        else:
            return render_template('project-editor.html', get=page)
    else:
        abort(403)

@app.route('/projects/<string:post_id>/delete', methods=('GET', 'POST'))
def delete_project(post_id):
    if config.enable_editing:
        projects_db.delete_one({'post_id': post_id})
        return redirect(url_for('list_projects'))
    else:
        abort(403)

@app.route('/projects/create', methods=('GET', 'POST'))
def create_project():
    if config.enable_editing:
        if request.method == "POST":
            print("THE FORM", request.form)
            if (not 'title' in request.form.keys()): return ('', 204)
            if (request.form.get('title', '') == ''):
                # flash('Title is required!')
                print("something", request.form.get('title', ''))
                return render_template('project-editor.html', get={})
            post_id = "-".join(request.form.get('title', '').strip().split(" ")).lower()
            suffix = ""
            while (projects_db.count_documents({'post_id': post_id + suffix}) != 0 and post_id+suffix != "create"):
                suffix = ''.join(random.choices(string.ascii_lowercase+string.digits, k=6))
            post_id = post_id + suffix
            projects_db.insert_one({
                'post_id': post_id,
                'title': request.form.get('title', ''),
                'desc': request.form.get('desc', ''),
                'date': request.form.get('date', ''),
                'tags': request.form.get('tags', ''),
                'icon': request.form.get('icon', ''),
                'content': request.form.get('content', '')
            })
            # return redirect(url_for('display_project', post_id='f'))
            return redirect(url_for('display_project', post_id=post_id))
            # return redirect(url_for('index'))
        else:
            return render_template('project-editor.html', get={})
    else:
        return abort(403)

@app.route('/question-generator')
def question_generator():
    return render_template('question-generator.html')

@app.route('/generate-question', methods=['GET'])
def generate_question():
    print(request.args)
    q_type = request.args.get('q_type')
    if (q_type == 'vector_proj'):
        md = vector_proj()
    elif (q_type == "system_of_eq"):
        md = system_of_eq()
    else:
        abort(400)

    for k in md.keys():
        if (k != "num_questions"):
            md[k] = md[k].rstrip('\n ')
            singleList = re.findall(r"[^\$]\$([^\$]+)\$(?!\$)", md[k])
            doubleList = re.findall(r"\${2}([^\$]+)\${2}", md[k])
            md[k] = re.sub(r"([^\$]\$)([^\$]+)(\$)(?!\$)", r"\1PLACEHOLDER\3", md[k])
            md[k] = re.sub(r"\${2}([^\$]+)\${2}", r"$$PLACEHOLDER2$$", md[k])
            md[k] = markdown(md[k])
            for item in singleList:
                md[k] = md[k].replace("$PLACEHOLDER$", "$"+item+"$", 1)
            for item in doubleList:
                md[k] = md[k].replace("$$PLACEHOLDER2$$", "$$"+item+"$$", 1)

            md[k] = md[k].strip('\n ')
            # md[k] = markdown(md[k].strip('\n ')) # accidentally removes a slash from a double slash
            # md[k] = re.sub(r"(\$\$)([^\$]+)(\$\$)", lambda x: re.sub(r'(\\)[^a-zA-Z0-9]', r'\\\\', x.group(2)), md[k]) # double \\ only in $$
            # if (k[0] == 'q'):
            md[k] = re.sub(r"(^<span>)(.*)(</span>$)", r"\2", md[k])
            md[k] = re.sub(r"(^<p>)(.*)(</p>$)", r"\2", md[k])
            md[k] = md[k].replace("$", "\\$")
    return md

if __name__ == '__main__':
    app.run(port=5000, debug=True)