import pandas as pd
from flask import Blueprint, render_template, request, current_app

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def get_method():
    return render_template('index.html', 업종_및_업종명=pd.DataFrame())

@main.route('/', methods=['POST'])
def post_method():
    업종 = request.form.get('업종')
    print(업종)

    return render_template('index.html', 업종_및_업종명=pd.DataFrame())

@main.route('/tmp', methods=['POST'])
def tmp_method():
    print('데이터를 불러옵니다.')

    return render_template('index.html', 업종_및_업종명=pd.DataFrame())