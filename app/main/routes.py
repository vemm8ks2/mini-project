import pandas as pd
import plotly.graph_objects as go
from flask import Blueprint, render_template, request, current_app

from app.data_process.재무제표_제어 import 재무제표_가져오기

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
    app = current_app  # 현재 활성화된 앱에 접근

    #통합본_생성("별도")
    #통합본_생성("연결")
    #통합본_생성("별도-연결")

    #전체_통합본_생성('별도')
    #전체_통합본_생성('연결')
    #전체_통합본_생성('별도-연결')

    #완전_통합본_생성('전체_별도_')
    #완전_통합본_생성('전체_연결_')
    #완전_통합본_생성('전체_별도-연결_')

    완전_통합본 = 재무제표_가져오기(f"{app.config["루트_경로"]}/전체_별도-연결_완전_통합본.csv")

    if "완전_통합본" not in app.config:
        app.config["완전_통합본"] = 완전_통합본

    return render_template('index.html', 업종_및_업종명=pd.DataFrame())


@main.route('/tmp1', methods=["GET"])
def tmp1_method():
    app = current_app  # 현재 활성화된 앱에 접근

    완전_통합본 = app.config["완전_통합본"]

    회사명 = request.args.get('company-name')
    종목코드 = request.args.get('stock-number')

    종목 = 완전_통합본[(완전_통합본["종목코드"] == 종목코드) | (완전_통합본["회사명"] == 회사명)]

    if 종목코드:
        app.config["종목코드"][f"[{종목코드}]"] = 종목["회사명"]

    if 회사명:
        app.config["종목코드"][종목["종목코드"].iloc[-1]] = 종목["회사명"].iloc[-1]

    종목.loc[:, "재무제표종류"] = 종목["재무제표종류"].str.strip()
    종목.loc[:, '항목코드'] = 종목['항목코드'].str.strip()

    app.config["종목"][회사명] = 종목 # 캐싱

    return render_template(
        "step1.html",
        회사명=회사명,
        종목코드=종목코드,
        재무제표종류=종목["재무제표종류"].drop_duplicates().tolist(),
    )


@main.route('/tmp2', methods=["GET"])
def tmp2_method():
    app = current_app  # 현재 활성화된 앱에 접근

    회사명 = request.args.get('company-name')
    종목코드 = request.args.get('stock-number')
    재무제표종류 = request.args.getlist('financial-statement-type')

    if 종목코드:
        회사명 = app.config["종목코드"][종목코드]

    종목 = app.config["종목"][회사명]
    종목 = 종목[종목['재무제표종류'].isin(재무제표종류)]

    return render_template(
        'step2.html',
        회사명=회사명,
        종목코드=종목코드,
        재무제표종류=재무제표종류,
        항목코드=종목["항목코드"].drop_duplicates().tolist(),
    )


@main.route('/tmp3', methods=["GET"])
def tmp3_method():
    app = current_app  # 현재 활성화된 앱에 접근

    회사명 = request.args.get('company-name')
    종목코드 = request.args.get('stock-number')
    재무제표종류 = request.args.getlist('financial-statement-type')
    항목코드 = request.args.getlist('code')

    if 종목코드:
        회사명 = app.config["종목코드"][종목코드]

    종목 = app.config["종목"][회사명]
    종목 = 종목[종목['항목코드'].isin(항목코드)]

    return render_template(
        'step3.html',
        회사명=회사명,
        종목코드=종목코드,
        재무제표종류=재무제표종류,
        항목코드 = 항목코드,
        결산기준일=종목["결산기준일"].drop_duplicates().tolist(),
    )


@main.route('/tmp4', methods=["GET"])
def tmp4_method():
    app = current_app  # 현재 활성화된 앱에 접근

    회사명 = request.args.get('company-name')
    종목코드 = request.args.get('stock-number')
    재무제표종류 = request.args.getlist('financial-statement-type')
    항목코드 = request.args.getlist('code')
    결산기준일 = request.args.getlist('settlement-date')

    if 종목코드:
        회사명 = app.config["종목코드"][종목코드]

    종목 = app.config["종목"][회사명]
    종목 = 종목[종목['재무제표종류'].isin(재무제표종류)]
    종목 = 종목[종목['항목코드'].isin(항목코드)]
    종목 = 종목[종목['결산기준일'].isin(결산기준일)]

    종목.loc[:, '당기'] = 종목['당기'].str.replace(',', '').astype('int64')


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=종목['결산기준일'],
        y=종목['당기'],
        mode='lines+markers',
        name='당기순이익'
    ))

    # 레이아웃 설정
    fig.update_layout(
        title=f"{회사명} 연도별 당기순이익",
        xaxis_title="연도",
        xaxis=dict(
            tickvals=종목['결산기준일'],
            ticktext=종목['결산기준일'],
        ),
        yaxis_title="당기순이익",
        yaxis=dict(
            tickformat=',.0f',
        ),
        template="simple_white"
    )

    graph_html = fig.to_html(full_html=False)

    return render_template(
        "step4.html",
        결과=종목.to_dict(orient="records"),
        그래프=graph_html
    )
