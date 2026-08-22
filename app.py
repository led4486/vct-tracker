import pandas as pd
import streamlit as st

# ==========================================
# 1. 페이지 설정 및 초기화
# ==========================================
st.set_page_config(
    page_title="VCT 2026 Champions 진출 트래커",
    layout="wide",
    page_icon="🎮",
)

st.title("🎮 VCT 2026 Champions 진출 트래커 & 순위 시뮬레이터")
st.caption(
    "공식 챔스 포인트 및 Stage 1+2 정규시즌 누적 데이터 완벽 일치 버전 | PO 1·2위 우선 정렬 및 동률 규정 시스템"
)

# ------------------------------------------
# 🔐 관리자 사이드바 추가
# ------------------------------------------
st.sidebar.title("🔐 관리자 설정")
admin_password = st.sidebar.text_input("데이터 편집 비밀번호", type="password")
# ------------------------------------------

# 이미지 데이터(Stage 1, 2) 합산치 완벽 동기화 테이블
DEFAULT_POINTS_DATA = [
    {
        "팀명": "Paper Rex",
        "Kickoff": 2,
        "Masters 1": 4,
        "Stage 1": 10,
        "Masters 2": 6,
        "Stage 2": 3,
        "S2_Rank": 99,
        "M2_Rank": 2,
        "S1_Rank": 1,
        "M1_Rank": 2,
        "KO_Rank": 3,
        "Reg_Wins": 7,
        "Reg_Map_Diff": 9,
        "Reg_Round_Diff": 72,
    },
    {
        "팀명": "Nongshim RedForce",
        "Kickoff": 4,
        "Masters 1": 6,
        "Stage 1": 2,
        "Masters 2": 0,
        "Stage 2": 2,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 8,
        "M1_Rank": 1,
        "KO_Rank": 1,
        "Reg_Wins": 4,
        "Reg_Map_Diff": -1,
        "Reg_Round_Diff": 16,
    },
    {
        "팀명": "T1",
        "Kickoff": 3,
        "Masters 1": 0,
        "Stage 1": 7,
        "Masters 2": 0,
        "Stage 2": 3,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 4,
        "M1_Rank": 10,
        "KO_Rank": 3,
        "Reg_Wins": 8,
        "Reg_Map_Diff": 11,
        "Reg_Round_Diff": 58,
    },
    {
        "팀명": "Global Esports",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 6,
        "Masters 2": 0,
        "Stage 2": 3,
        "S2_Rank": 99,
        "M2_Rank": 10,
        "S1_Rank": 3,
        "M1_Rank": 99,
        "KO_Rank": 8,
        "Reg_Wins": 6,
        "Reg_Map_Diff": 5,
        "Reg_Round_Diff": 30,
    },
    {
        "팀명": "FULL SENSE",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 7,
        "Masters 2": 0,
        "Stage 2": 1,
        "S2_Rank": 99,
        "M2_Rank": 12,
        "S1_Rank": 2,
        "M1_Rank": 99,
        "KO_Rank": 8,
        "Reg_Wins": 4,
        "Reg_Map_Diff": 0,
        "Reg_Round_Diff": -6,
    },
    {
        "팀명": "Rex Regum Qeon",
        "Kickoff": 1,
        "Masters 1": 0,
        "Stage 1": 4,
        "Masters 2": 0,
        "Stage 2": 2,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 6,
        "M1_Rank": 99,
        "KO_Rank": 4,
        "Reg_Wins": 6,
        "Reg_Map_Diff": 0,
        "Reg_Round_Diff": -6,
    },
    {
        "팀명": "Gen.G Esports",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 1,
        "Masters 2": 0,
        "Stage 2": 5,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 12,
        "M1_Rank": 99,
        "KO_Rank": 10,
        "Reg_Wins": 6,
        "Reg_Map_Diff": 1,
        "Reg_Round_Diff": -8,
    },
    {
        "팀명": "KRX",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 4,
        "Masters 2": 0,
        "Stage 2": 1,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 6,
        "M1_Rank": 99,
        "KO_Rank": 6,
        "Reg_Wins": 5,
        "Reg_Map_Diff": -2,
        "Reg_Round_Diff": -35,
    },
    {
        "팀명": "DetonatioN FocusMe",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 2,
        "Masters 2": 0,
        "Stage 2": 3,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 8,
        "M1_Rank": 99,
        "KO_Rank": 5,
        "Reg_Wins": 5,
        "Reg_Map_Diff": -2,
        "Reg_Round_Diff": -11,
    },
    {
        "팀명": "VARREL",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 0,
        "Masters 2": 0,
        "Stage 2": 4,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 12,
        "M1_Rank": 99,
        "KO_Rank": 12,
        "Reg_Wins": 4,
        "Reg_Map_Diff": -3,
        "Reg_Round_Diff": -10,
    },
    {
        "팀명": "ZETA DIVISION",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 1,
        "Masters 2": 0,
        "Stage 2": 2,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 10,
        "M1_Rank": 99,
        "KO_Rank": 10,
        "Reg_Wins": 3,
        "Reg_Map_Diff": -7,
        "Reg_Round_Diff": -46,
    },
    {
        "팀명": "Team Secret",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 1,
        "Masters 2": 0,
        "Stage 2": 1,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 10,
        "M1_Rank": 99,
        "KO_Rank": 12,
        "Reg_Wins": 2,
        "Reg_Map_Diff": -11,
        "Reg_Round_Diff": -54,
    },
    {
        "팀명": "ONSIDE GAMING (ONG)",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 0,
        "Masters 2": 0,
        "Stage 2": 0,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 99,
        "M1_Rank": 99,
        "KO_Rank": 99,
        "Reg_Wins": 0,
        "Reg_Map_Diff": -15,
        "Reg_Round_Diff": -50,
    },
    {
        "팀명": "Sharper Esport (SP)",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 0,
        "Masters 2": 0,
        "Stage 2": 0,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 99,
        "M1_Rank": 99,
        "KO_Rank": 99,
        "Reg_Wins": 0,
        "Reg_Map_Diff": -15,
        "Reg_Round_Diff": -50,
    },
    {
        "팀명": "QT DiGoo (QTD)",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 0,
        "Masters 2": 0,
        "Stage 2": 0,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 99,
        "M1_Rank": 99,
        "KO_Rank": 99,
        "Reg_Wins": 0,
        "Reg_Map_Diff": -15,
        "Reg_Round_Diff": -50,
    },
    {
        "팀명": "Xipto Esports (XIP)",
        "Kickoff": 0,
        "Masters 1": 0,
        "Stage 1": 0,
        "Masters 2": 0,
        "Stage 2": 0,
        "S2_Rank": 99,
        "M2_Rank": 99,
        "S1_Rank": 99,
        "M1_Rank": 99,
        "KO_Rank": 99,
        "Reg_Wins": 0,
        "Reg_Map_Diff": -15,
        "Reg_Round_Diff": -50,
    },
]

if "points_table" not in st.session_state:
    st.session_state.points_table = pd.DataFrame(DEFAULT_POINTS_DATA)

all_teams = [row["팀명"] for row in DEFAULT_POINTS_DATA]
team_options = ["[미정]"] + all_teams

playin_challenger_teams = [
    "ONSIDE GAMING (ONG)",
    "Sharper Esport (SP)",
    "QT DiGoo (QTD)",
    "Xipto Esports (XIP)",
]

# ==========================================
# 2. 탭 구성
# ==========================================
tab1, tab2 = st.tabs(
    [
        "📊 1. 순위 지정 & 진출 확정 (통합 페이지)",
        "🏆 2. 포인트 및 동률 규정 데이터 편집",
    ]
)

# ------------------------------------------
# TAB 2: 데이터 편집 (권한 확인 로직 적용)
# ------------------------------------------
with tab2:
    st.subheader("🏆 대회별 포인트 및 공식 동률 결정 규정 데이터 수정")
    
    # 설정한 비밀번호 "1234"가 맞아야만 편집기(data_editor)가 열림
    if admin_password == "1234":
        st.session_state.points_table = st.data_editor(
            st.session_state.points_table,
            num_rows="dynamic",
            use_container_width=True,
        )
    else:
        # 비밀번호가 틀리거나 없으면 조회용 표(dataframe)만 보여줌
        st.warning("데이터를 수정하려면 좌측 사이드바에 관리자 비밀번호를 입력해주세요.")
        st.dataframe(st.session_state.points_table, use_container_width=True)

# ------------------------------------------
# TAB 1: 순위 지정 및 진출 확정 (통합 페이지)
# ------------------------------------------
with tab1:
    st.subheader("🎯 Stage 2 PO 상위 4개 팀 순위 지정")
    st.markdown(
        "결승 직행(1·2위) 및 3·4위 팀을 지정하면, PO 1·2위 팀이 테이블 최상단에 우선 노출되며 3위(+5점)와 4위(+4점) 포인트가 **Stage 2 열에 자동으로 합산**됩니다."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        champ_1st = st.selectbox(
            "🥇 Stage 2 PO 1위 (결승 직행)", team_options, index=0, key="ch_1"
        )
    with c2:
        champ_2nd = st.selectbox(
            "🥈 Stage 2 PO 2위 (결승 직행)", team_options, index=0, key="po_2"
        )
    with c3:
        po_3rd = st.selectbox(
            "🥉 Stage 2 PO 3위 (+5점)", team_options, index=0, key="po_3"
        )
    with c4:
        po_4th = st.selectbox(
            "4️⃣ Stage 2 PO 4위 (+4점)", team_options, index=0, key="po_4"
        )

    st.markdown("---")
    st.subheader(
        "📊 VCT Pacific 공식 노출 우선순위 & 동률 프로세스 반영 순위표"
    )

    df = st.session_state.points_table.copy()
    score_cols = ["Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if po_3rd != "[미정]":
        df.loc[df["팀명"] == po_3rd, "Stage 2"] += 5
    if po_4th != "[미정]":
        df.loc[df["팀명"] == po_4th, "Stage 2"] += 4

    df["Total Points"] = df[score_cols].sum(axis=1)

    for rc in [
        "S2_Rank",
        "M2_Rank",
        "S1_Rank",
        "M1_Rank",
        "KO_Rank",
        "Reg_Wins",
        "Reg_Map_Diff",
        "Reg_Round_Diff",
    ]:
        if rc in df.columns:
            df[rc] = pd.to_numeric(df[rc], errors="coerce").fillna(99)

    # 1차 기본 정렬 (공식 동률 규정 적용)
    df = df.sort_values(
        by=[
            "Total Points",
            "S2_Rank",
            "M2_Rank",
            "S1_Rank",
            "M1_Rank",
            "KO_Rank",
            "Reg_Wins",
            "Reg_Map_Diff",
            "Reg_Round_Diff",
            "팀명",
        ],
        ascending=[
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            True,
        ],
    ).reset_index(drop=True)

    # ----------------------------------------------------
    # 🎯 노출 우선순위 정렬 적용 (PO 1위 -> PO 2위 -> 나머지 포인트 상위순)
    # ----------------------------------------------------
    priority_rows = []

    if champ_1st != "[미정]":
        match_1st = df[df["팀명"] == champ_1st]
        if not match_1st.empty:
            priority_rows.append(match_1st)

    if champ_2nd != "[미정]" and champ_2nd != champ_1st:
        match_2nd = df[df["팀명"] == champ_2nd]
        if not match_2nd.empty:
            priority_rows.append(match_2nd)

    exclude_teams = [
        t for t in [champ_1st, champ_2nd] if t != "[미정]"
    ]
    remaining_df = df[~df["팀명"].isin(exclude_teams)]

    if priority_rows:
        priority_df = pd.concat(priority_rows, ignore_index=True)
        df = pd.concat([priority_df, remaining_df], ignore_index=True)

    # 동률 판정 및 규정 명시 로직
    tie_descriptions = []
    points_counts = df["Total Points"].value_counts()

    for i, row in df.iterrows():
        pts = row["Total Points"]
        if points_counts[pts] == 1:
            tie_descriptions.append("단독 순위")
            continue

        if i == 0:
            tie_descriptions.append("동률 (기준 적용)")
            continue

        prev_row = df.iloc[i - 1]
        if prev_row["Total Points"] != pts:
            tie_descriptions.append("동률 (기준 적용)")
            continue

        reason = ""
        if row["S2_Rank"] != prev_row["S2_Rank"]:
            reason = (
                "스테이지 2 순위에 의해 "
                + (
                    "상위"
                    if row["S2_Rank"] < prev_row["S2_Rank"]
                    else "하위"
                )
            )
        elif row["M2_Rank"] != prev_row["M2_Rank"]:
            reason = (
                "마스터스 2 순위에 의해 "
                + (
                    "상위"
                    if row["M2_Rank"] < prev_row["M2_Rank"]
                    else "하위"
                )
            )
        elif row["S1_Rank"] != prev_row["S1_Rank"]:
            reason = (
                "스테이지 1 순위에 의해 "
                + (
                    "상위"
                    if row["S1_Rank"] < prev_row["S1_Rank"]
                    else "하위"
                )
            )
        elif row["M1_Rank"] != prev_row["M1_Rank"]:
            reason = (
                "마스터스 1 순위에 의해 "
                + (
                    "상위"
                    if row["M1_Rank"] < prev_row["M1_Rank"]
                    else "하위"
                )
            )
        elif row["KO_Rank"] != prev_row["KO_Rank"]:
            reason = (
                "킥오프 순위에 의해 "
                + (
                    "상위"
                    if row["KO_Rank"] < prev_row["KO_Rank"]
                    else "하위"
                )
            )
        elif row["Reg_Wins"] != prev_row["Reg_Wins"]:
            reason = (
                "시즌 총 승수에 의해 "
                + (
                    "상위"
                    if row["Reg_Wins"] > prev_row["Reg_Wins"]
                    else "하위"
                )
            )
        elif row["Reg_Map_Diff"] != prev_row["Reg_Map_Diff"]:
            reason = (
                "시즌 총 맵 득실에 의해 "
                + (
                    "상위"
                    if row["Reg_Map_Diff"] > prev_row["Reg_Map_Diff"]
                    else "하위"
                )
            )
        elif row["Reg_Round_Diff"] != prev_row["Reg_Round_Diff"]:
            reason = (
                "시즌 총 라운드 득실에 의해 "
                + (
                    "상위"
                    if row["Reg_Round_Diff"] > prev_row["Reg_Round_Diff"]
                    else "하위"
                )
            )
        else:
            reason = "보조 기준(팀명 순)에 의해 처리"

        tie_descriptions.append(reason)

    df["동률 규정 적용 결과"] = tie_descriptions

    df.index = df.index + 1
    df.index.name = "Ranking"

    finalists = [t for t in [champ_1st, champ_2nd] if t != "[미정]"]
    qualified_teams = set(finalists)

    for _, row in df.iterrows():
        if len(qualified_teams) >= 4:
            break
        tname = row["팀명"]
        if tname in playin_challenger_teams:
            if tname in finalists or tname in [po_3rd, po_4th]:
                qualified_teams.add(tname)
        else:
            qualified_teams.add(tname)

    status_list = []
    for idx, row in df.iterrows():
        tname = row["팀명"]
        is_finalist = tname in finalists
        is_challenger = tname in playin_challenger_teams

        if tname in qualified_teams:
            if is_finalist:
                status_list.append("🏆 Champions 진출 확정 (결승 직행)")
            else:
                status_list.append("🏆 Champions 진출 확정 (포인트 상위 승계)")
        elif is_challenger:
            status_list.append("❌ 탈락 (플레이인 조건 미달)")
        else:
            my_pts = row["Total Points"]
            if idx <= 4 and my_pts >= 25 and len(finalists) == 2:
                status_list.append("🏆 Champions 진출 확정 (포인트 상위 안전권)")
            else:
                status_list.append("🟡 진출 경쟁 중")

    df["Champions 진출 상태"] = status_list

    display_cols = [
        "팀명",
        "Total Points",
        "동률 규정 적용 결과",
        "Champions 진출 상태",
        "Kickoff",
        "Masters 1",
        "Stage 1",
        "Masters 2",
        "Stage 2",
    ]

    # ----------------------------------------------------
    # 🎨 진출팀 및 동률 그룹 하이라이트 로직
    # ----------------------------------------------------
    tie_colors = [
        "background-color: #ffe5d0;",  # 연한 주황
        "background-color: #ffcccc;",  # 연한 빨강
    ]

    point_to_color = {}
    color_idx = 0
    for pts in df["Total Points"]:
        if pts not in point_to_color:
            if points_counts[pts] > 1:
                point_to_color[pts] = tie_colors[
                    color_idx % len(tie_colors)
                ]
                color_idx += 1
            else:
                point_to_color[pts] = ""

    def highlight_rows(row):
        # 1. 최우선 순위: 진출이 확정된 팀 (연한 노란색)
        if "진출 확정" in str(row["Champions 진출 상태"]):
            return ["background-color: #fff3cc;"] * len(row)
        
        # 2. 다음 순위: 동률인 팀 (주황색, 빨간색 교차)
        pts = row["Total Points"]
        color_style = point_to_color.get(pts, "")
        return [color_style] * len(row)

    styled_df = df[display_cols].style.apply(highlight_rows, axis=1)

    st.dataframe(styled_df, use_container_width=True)

    # ==========================================
    # 📌 페이지 맨 아래: VCT 공식 동률 규정 안내 섹션
    # ==========================================
    st.markdown("---")
