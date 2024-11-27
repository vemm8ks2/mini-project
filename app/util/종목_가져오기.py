from flask import current_app


def 종목_초기화(종목):
    종목.loc[:, "재무제표종류"] = 종목["재무제표종류"].str.strip()
    종목.loc[:, "항목코드"] = 종목["항목코드"].str.strip()
    종목.loc[:, "항목명"] = 종목["항목명"].str.strip()

    종목.loc[종목["항목코드"] == "ifrs_ProfitLoss", "항목코드"] = "ifrs-full_ProfitLoss"
    종목.loc[종목["항목코드"] == "ifrs_Revenue", "항목코드"] = "ifrs-full_Revenue"
    종목.loc[종목["재무제표종류"] == "손익계산서, 기능별 분류 - 별도재무제표", "재무제표종류"] = "손익계산서, 기능별 분류 - 별도"
    종목.loc[종목["재무제표종류"] == "손익계산서, 기능별 분류 - 연결재무제표", "재무제표종류"] = "손익계산서, 기능별 분류 - 연결"


def 종목_할당(회사명, 종목코드):
    app = current_app  # 현재 활성화된 앱에 접근

    완전_통합본 = app.config["완전_통합본"]
    종목 = 완전_통합본[(완전_통합본["종목코드"] == 종목코드) | (완전_통합본["회사명"] == 회사명)]

    if 종목코드:
        app.config["종목코드"][f"[{종목코드}]"] = 종목["회사명"]

    if 회사명:
        app.config["종목코드"][종목["종목코드"].iloc[-1]] = 종목["회사명"].iloc[-1]

    종목_초기화(종목)

    return 종목

def 종목_가져오기(회사명, 종목코드):
    app = current_app  # 현재 활성화된 앱에 접근

    회사명_할당여부 = lambda 이름: 이름 in app.config["종목"]
    종목코드_할당여부 = lambda 코드: f"[{코드}]" in app.config["종목코드"]

    if 회사명 and 회사명_할당여부(회사명):
        return app.config["종목"][회사명]

    if 종목코드 and 종목코드_할당여부(종목코드):
        사명 = app.config["종목코드"][f"[{종목코드}]"]

        if 회사명_할당여부(사명):
            return app.config["종목"][사명]

    return 종목_할당(회사명, 종목코드)