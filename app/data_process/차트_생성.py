import plotly.graph_objects as go

def 차트_생성(종목, 유형):
    fig = go.Figure()

    재무제표종류_목록 = 종목["재무제표종류"].unique()
    항목코드_목록 = 종목["항목코드"].unique()

    for 종류 in 재무제표종류_목록:
        for 항목코드 in 항목코드_목록:
            차트화 = 종목[(종목["재무제표종류"] == 종류) & (종목["항목코드"] == 항목코드)]

            if 차트화.empty:
                continue

            차트화 = 차트화.sort_values(by="결산기준일")

            if 유형 == "선":
                fig.add_trace(go.Scatter(
                    x=차트화["결산기준일"],
                    y=차트화["당기"].str.replace(',', '').astype('int64'),
                    mode="lines+markers",
                    name=차트화["항목명"].iloc[-1]
                ))
            elif 유형 == "막대":
                fig.add_trace(go.Bar(
                    x=차트화["결산기준일"],
                    y=차트화["당기"].str.replace(',', '').astype('int64'),
                    name=차트화["항목명"].iloc[-1]
                ))

    # 레이아웃 설정
    fig.update_layout(
        title=f"{종목["회사명"].iloc[-1]} 연도별, 항목코드별 비교 차트",
        xaxis_title="연도",
        xaxis=dict(
            tickvals=종목['결산기준일'],
            ticktext=종목['결산기준일'],
        ),
        yaxis_title="당기",
        yaxis=dict(
           tickformat=',.0f',
        ),
        width=1280,
        height=600,
        template="simple_white"
    )

    return fig.to_html(full_html=False)