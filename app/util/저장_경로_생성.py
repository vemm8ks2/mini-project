import os
from flask import current_app


def 저장_경로_생성(회사명):
    app = current_app  # 현재 활성화된 앱에 접근

    저장_루트_경로 = "C:/saved_result"

    if not os.path.isdir(저장_루트_경로):
        os.makedirs(저장_루트_경로)

    저장_경로_당해 = f"{저장_루트_경로}/{app.config['년']}"

    if not os.path.isdir(저장_경로_당해):
        os.makedirs(저장_경로_당해)

    저장_경로_당월 = f"{저장_루트_경로}/{app.config['년']}/{app.config["월"]}"

    if not os.path.isdir(저장_경로_당월):
        os.makedirs(저장_경로_당월)

    저장_경로_당일 = f"{저장_루트_경로}/{app.config['년']}/{app.config["월"]}/{app.config["일"]}"

    if not os.path.isdir(저장_경로_당일):
        os.makedirs(저장_경로_당일)

    저장_경로 = f"{저장_경로_당일}/{회사명}"

    if not os.path.isdir(저장_경로):
        os.makedirs(저장_경로)

    return 저장_경로