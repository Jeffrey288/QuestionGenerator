# we'll be using flask
# set FLASK_APP=main
# set FLASK_ENV=development
# flask run

from flask import Flask, render_template, request, abort
from modules.vector_proj import vector_proj
from modules.system_of_eq import system_of_eq
from markdown import markdown
import regex as re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

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