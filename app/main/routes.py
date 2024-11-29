import os
from flask import Blueprint, render_template, request, current_app, redirect, session

from app.data_process.완전_통합본_생성 import 완전_통합본_생성
from app.data_process.재무제표_제어 import 재무제표_가져오기
from app.data_process.전체_통합본_생성 import 전체_통합본_생성
from app.data_process.차트_생성 import 차트_생성
from app.data_process.통합본_생성 import 통합본_생성
from app.util.종목_가져오기 import 종목_가져오기

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    app = current_app  # 현재 활성화된 앱에 접근

    완전_통합본 = app.config["완전_통합본"]
    회사_목록 = 완전_통합본.loc[:, ['종목코드', '회사명']]
    회사_목록 = 회사_목록.groupby("종목코드").last().reset_index()

    return render_template('index.html', 회사_목록=회사_목록.to_dict("records"))


@main.route('/loading', methods=['GET'])
def loading_method():
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

    분류 = "별도-연결"
    완전_통합본_경로 = f"{app.config["루트_경로"]}/전체_별도-연결_완전_통합본.csv"

    if os.path.isfile(완전_통합본_경로):
        완전_통합본 = 재무제표_가져오기(완전_통합본_경로)
    else:
        전체_통합본_경로 = f"{app.config["루트_경로"]}/전체_{분류}_통합본.csv"

        if not os.path.isfile(전체_통합본_경로):
            통합본_생성(분류)
            전체_통합본_생성(분류)

        완전_통합본 = 완전_통합본_생성(f"전체_{분류}_")

    if "완전_통합본" not in app.config:
        app.config["완전_통합본"] = 완전_통합본

    origin_path = session.get('origin_path', '/')

    return redirect(origin_path)


@main.route('/process', methods=["GET"])
def process_method():
    회사명 = request.args.get('company-name')
    종목코드 = request.args.get('stock-number')
    재무제표종류 = request.args.getlist('financial-statement-type') or None
    항목코드 = request.args.getlist('code') or None
    결산기준일 = request.args.getlist('settlement-date') or None

    종목 = 종목_가져오기(회사명, 종목코드)
    데이터테이블_항목 = ("재무제표종류", "financial-statement-type", [])

    if 재무제표종류:
        종목 = 종목[종목['재무제표종류'].isin(재무제표종류)]
        데이터테이블_항목 = ("항목코드", "code", ["항목명"])

    if 항목코드:
        종목 = 종목[종목['항목코드'].isin(항목코드)]
        데이터테이블_항목 = ("결산기준일", "settlement-date", [])

    if 결산기준일:
        종목 = 종목[종목['결산기준일'].isin(결산기준일)]

    데이터테이블 = 종목.groupby(데이터테이블_항목[0], as_index=False).last()
    데이터테이블 = [(인덱스, 행.to_dict()) for 인덱스, 행 in 데이터테이블.iterrows()]

    if 재무제표종류 and 항목코드 and 결산기준일:
        선_차트_HTML = 차트_생성(종목, "선")
        막대_차트_HTML = 차트_생성(종목, "막대")

        return render_template(
            "result.html",
            결과=종목.to_dict(orient="records"),
            선_그래프=선_차트_HTML,
            막대_그래프=막대_차트_HTML
        )

    return render_template(
        "process.html",
        회사명=회사명,
        종목코드=종목코드,
        재무제표종류=재무제표종류,
        항목코드=항목코드,
        결산기준일=결산기준일,
        데이터테이블_항목=데이터테이블_항목,
        데이터테이블=데이터테이블
    )
