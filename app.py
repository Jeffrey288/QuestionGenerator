# we'll be using flask
# set FLASK_APP=main
# set FLASK_ENV=development
# flask run

from flask import Flask, render_template, request, abort
from modules.vector_proj import vector_proj
from markdown import markdown
import regex as re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-question', methods=['GET'])
def generate_question():
    # print(request.args)
    # q_type = request.args.get('q_type')
    # if (q_type == 'vector_proj'):
    # else:
    #     abort(400)
    md = vector_proj()

    for k in md.keys():
        if (k != "num_questions"):
            md[k] = markdown(md[k].strip('\n ')) # accidentally removes a slash from a double slash
            md[k] = re.sub(r"(\$\$)([^\$]+)(\$\$)", lambda x: re.sub(r'(\\)[^a-zA-Z0-9]', r'\\\\', x.group(2)), md[k]) # double \\ only in $$
            if (k[0] == 'q'):
                md[k] = re.sub(r"(^<p>)(.*)(</p>$)", lambda x: x.group(2), md[k])
            md[k] = md[k].replace("$", "\\$")
    return md

if __name__ == '__main__':
    app.run(port=5000, debug=True)