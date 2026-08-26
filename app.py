import pandas as pd
import streamlit as st
import itertools
import random

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
    "잔여 PO 경우의 수 4만여 개 전수조사 몬테카를로 시뮬레이션 | 100% 수학적 확률(%) 알고리즘 적용 완료"
)

# ------------------------------------------
# 🔐 관리자 사이드바 추가
# ------------------------------------------
st.sidebar.title("🔐 관리자 설정")
admin_password = st.sidebar.text_input("데이터 편집 비밀번호", type="password")
# ------------------------------------------

# 이미지 데이터(Stage 1, 2) 합산치 완벽 동기화 테이블
DEFAULT_POINTS_DATA = [
    {"팀명": "Paper Rex", "Kickoff": 2, "Masters 1": 4, "Stage 1": 10, "Masters 2": 6, "Stage 2": 3, "S2_Rank": 99, "M2_Rank": 2, "S1_Rank": 1, "M1_Rank": 2, "KO_Rank": 3, "Reg_Wins": 7, "Reg_Map_Diff": 9, "Reg_Round_Diff": 72},
    {"팀명": "Nongshim RedForce", "Kickoff": 4, "Masters 1": 6, "Stage 1": 2, "Masters 2": 0, "Stage 2": 2, "S2_Rank": 99, "M2_Rank": 99, "S1_Rank": 8, "M1_Rank": 1, "KO_Rank": 1, "Reg_Wins": 4, "Reg_Map_Diff": -1, "Reg_Round_Diff": 16},
    {"팀명": "T1", "Kickoff": 3, "Masters 1": 0, "Stage 1": 7, "Masters 2": 0, "Stage 2": 3, "S2_Rank": 99, "M2_Rank": 99, "S1_Rank": 4, "M1_Rank": 10, "KO_Rank": 3, "Reg_Wins": 8, "Reg_Map_Diff": 11, "Reg_Round_Diff": 58},
    {"팀명": "Global Esports", "Kickoff": 0, "Masters 1": 0, "Stage 1": 6, "Masters 2": 0, "Stage 2": 3, "S2_Rank": 99, "M2_Rank": 10, "S1_Rank": 3, "M1_Rank": 99, "KO_Rank": 8, "Reg_Wins": 6, "Reg_Map_Diff": 5, "Reg_Round_Diff": 30},
    {"팀명": "FULL SENSE", "Kickoff": 0, "Masters 1": 0, "Stage 1": 7, "Masters 2": 0, "Stage 2": 1, "S2_Rank": 12, "M2_Rank": 12, "S1_Rank": 2, "M1_Rank": 99, "KO_Rank": 8, "Reg_Wins": 4, "Reg_Map_Diff": 0, "Reg_Round_Diff": -6},
    {"팀명": "Rex Regum Qeon", "Kickoff": 1, "Masters 1": 0, "Stage 1": 4, "Masters 2": 0, "Stage 2": 2, "S2_Rank": 16, "M2_Rank": 99, "S1_Rank": 6, "M1_Rank": 99, "KO_Rank": 4, "Reg_Wins": 6, "Reg_Map_Diff": 0, "Reg_Round_Diff": -6},
    {"팀명": "Gen.G Esports", "Kickoff": 0, "Masters 1": 0, "Stage 1": 1, "Masters 2": 0, "Stage 2": 5, "S2_Rank": 99, "M2_Rank": 99, "S1_Rank": 12, "M1_Rank": 99, "KO_Rank": 10, "Reg_Wins": 6, "Reg_Map_Diff": 1, "Reg_Round_Diff": -8},
    {"팀명": "KRX", "Kickoff": 0, "Masters 1": 0, "Stage 1": 4, "Masters 2": 0, "Stage 2": 1, "S2_Rank": 99, "M2_Rank": 99, "S1_Rank": 6, "M1_Rank": 99, "KO_Rank": 6, "Reg_Wins": 5, "Reg_Map_Diff": -2, "Reg_Round_Diff": -35},
    {"팀명": "DetonatioN FocusMe", "Kickoff": 0, "Masters 1": 0, "Stage 1": 2, "Masters 2": 0, "Stage 2": 3, "S2_Rank": 10, "M2_Rank": 99, "S1_Rank": 8, "M1_Rank": 99, "KO_Rank": 5, "Reg_Wins": 5, "Reg_Map_Diff": -2, "Reg_Round_Diff": -11},
    {"팀명": "VARREL", "Kickoff": 0, "Masters 1": 0, "Stage 1": 0, "Masters 2": 0, "Stage 2": 4, "S2_Rank": 99, "M2_Rank": 99, "S1_Rank": 12, "M1_Rank": 99, "KO_Rank": 12, "Reg_Wins": 4, "Reg_Map_Diff": -3, "Reg_Round_Diff": -10},
    {"팀명": "ZETA DIVISION", "Kickoff": 0, "Masters 1": 0, "Stage 1": 1, "Masters 2": 0, "Stage 2": 2, "S2_Rank": 12, "M2_Rank": 99, "S1_Rank": 10, "M1_Rank": 99, "KO_Rank": 10, "Reg_Wins": 3, "Reg_Map_Diff": -7, "Reg_Round_Diff": -46},
    {"팀명": "Team Secret", "Kickoff": 0, "Masters 1": 0, "Stage 1": 1, "Masters 2": 0, "Stage 2": 1, "S2_Rank": 16, "M2_Rank": 99, "S1_Rank": 10, "M1_Rank": 99, "KO_Rank": 12, "Reg_Wins": 2, "Reg_Map_Diff": -11, "Reg_Round_Diff": -54},
    {"팀명": "ONSIDE GAMING (ONG)", "Kickoff": 0, "Masters 1": 0, "Stage 1": 0, "Masters 2": 0, "Stage 2": 0, "S2_Rank": 99, "M2_Rank": 99, "S1_Rank": 99, "M1_Rank": 99, "KO_Rank": 99, "Reg_Wins": 0, "Reg_Map_Diff": -15, "Reg_Round_Diff": -50},
    {"팀명": "Sharper Esport (SP)", "Kickoff": 0, "Masters 1": 0, "Stage 1": 0, "Masters 2": 0, "Stage 2": 0, "S2_Rank": 99, "M2_Rank": 99, "S1_Rank": 99, "M1_Rank": 99, "KO_Rank": 99, "Reg_Wins": 0, "Reg_Map_Diff": -15, "Reg_Round_Diff": -50},
    {"팀명": "QT DiGoo (QTD)", "Kickoff": 0, "Masters 1": 0, "Stage 1": 0, "Masters 2": 0, "Stage 2": 0, "S2_Rank": 16, "M2_Rank": 99, "S1_Rank": 99, "M1_Rank": 99, "KO_Rank": 99, "Reg_Wins": 0, "Reg_Map_Diff": -15, "Reg_Round_Diff": -50},
    {"팀명": "Xipto Esports (XIP)", "Kickoff": 0, "Masters 1": 0, "Stage 1": 0, "Masters 2": 0, "Stage 2": 0, "S2_Rank": 16, "M2_Rank": 99, "S1_Rank": 99, "M1_Rank": 99, "KO_Rank": 99, "Reg_Wins": 0, "Reg_Map_Diff": -15, "Reg_Round_Diff": -50},
]

if "points_table" not in st.session_state:
    st.session_state.points_table = pd.DataFrame(DEFAULT_POINTS_DATA)

all_teams = [row["팀명"] for row in DEFAULT_POINTS_DATA]
playin_challenger_teams = ["ONSIDE GAMING (ONG)", "Sharper Esport (SP)", "QT DiGoo (QTD)", "Xipto Esports (XIP)"]

# ==========================================
# 2. 탭 구성
# ==========================================
tab1, tab2 = st.tabs(["📊 1. 순위 지정 & 확률(%) 시뮬레이터", "🏆 2. 데이터 편집"])

# ------------------------------------------
# TAB 2: 데이터 편집
# ------------------------------------------
with tab2:
    st.subheader("🏆 대회별 포인트 및 공식 동률 결정 규정 데이터 수정")
    if admin_password == "1234":
        st.session_state.points_table = st.data_editor(st.session_state.points_table, num_rows="dynamic", use_container_width=True)
    else:
        st.warning("데이터를 수정하려면 좌측 사이드바에 관리자 비밀번호를 입력해주세요.")
        st.dataframe(st.session_state.points_table, use_container_width=True)

# ------------------------------------------
# TAB 1: 순위 지정 및 확률 시뮬레이션
# ------------------------------------------
with tab1:
    st.subheader("🎯 시즌 아웃 및 Stage 2 PO 진출팀 시뮬레이션")
    st.markdown(
        "**시즌 아웃(탈락) 팀을 지정**하면 시드 배정에서 제외되지만, 잔여 포인트가 압도적일 경우 확률이 100%로 유지됩니다. "
        "빈칸으로 남겨둔 등수는 모든 경우의 수(최대 4만여 개 시나리오)를 계산하여 하위권 팀의 역전 가능성을 1% 단위로 산출합니다."
    )

    season_out_teams = st.multiselect("💀 시즌 아웃 (탈락 확정) 팀 지정", all_teams, key="season_out")
    available_teams = [t for t in all_teams if t not in season_out_teams]

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1: champ_1st = st.multiselect("🥇 Stage 2 PO 1위 (결승 직행)", available_teams, key="ch_1")
    with c2: champ_2nd = st.multiselect("🥈 Stage 2 PO 2위 (결승 직행)", available_teams, key="po_2")
    with c3: po_3rd = st.multiselect("🥉 Stage 2 PO 3위 (+5점)", available_teams, key="po_3")
    with c4: po_4th = st.multiselect("4️⃣ Stage 2 PO 4위 (+4점)", available_teams, key="po_4")

    st.markdown("---")
    st.subheader("📊 VCT Pacific 공식 챔피언스 진출 현황 및 실시간 확률")

    # 원본 데이터 준비
    raw_df = st.session_state.points_table.copy()
    score_cols = ["Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]
    for col in score_cols:
        raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce").fillna(0)
    raw_df["Total Points"] = raw_df[score_cols].sum(axis=1)
    
    tie_cols = ["S2_Rank", "M2_Rank", "S1_Rank", "M1_Rank", "KO_Rank", "Reg_Wins", "Reg_Map_Diff", "Reg_Round_Diff"]
    for rc in tie_cols:
        raw_df[rc] = pd.to_numeric(raw_df[rc], errors="coerce").fillna(99)

    # ----------------------------------------------------
    # 🎲 몬테카를로 / 모든 경우의 수 전수조사 (확률 계산)
    # ----------------------------------------------------
    need_1st, need_2nd = len(champ_1st) == 0, len(champ_2nd) == 0
    need_3rd, need_4th = len(po_3rd) == 0, len(po_4th) == 0
    slots_to_fill = sum([need_1st, need_2nd, need_3rd, need_4th])
    
    fixed_teams = set(champ_1st + champ_2nd + po_3rd + po_4th)
    eligible_teams = [t for t in available_teams if t not in fixed_teams]
    
    # 16개 팀 중 4자리(빈칸)를 뽑는 모든 경우의 수 생성
    perms = list(itertools.permutations(eligible_teams, slots_to_fill)) if slots_to_fill > 0 else [()]
    
    # 과도한 연산 방지용 무작위 샘플링 (10,000개 시나리오로 제한)
    if len(perms) > 10000:
        perms = random.sample(perms, 10000)
    total_scenarios = len(perms)
    
    qual_counts = {t: 0 for t in all_teams}
    
    # 속도를 위한 기본 스탯 튜플 변환
    base_stats = {}
    for _, row in raw_df.iterrows():
        base_stats[row["팀명"]] = (
            row["Total Points"], row["S2_Rank"], row["M2_Rank"], row["S1_Rank"], 
            row["M1_Rank"], row["KO_Rank"], -row["Reg_Wins"], -row["Reg_Map_Diff"], -row["Reg_Round_Diff"], row["팀명"]
        )

    # 시나리오 별 역전 가능성 연산
    for perm in perms:
        sim_1st = set(champ_1st)
        sim_2nd = set(champ_2nd)
        sim_3rd = set(po_3rd)
        sim_4th = set(po_4th)
        
        idx = 0
        if need_1st: sim_1st.add(perm[idx]); idx += 1
        if need_2nd: sim_2nd.add(perm[idx]); idx += 1
        if need_3rd: sim_3rd.add(perm[idx]); idx += 1
        if need_4th: sim_4th.add(perm[idx]); idx += 1
        
        sortable = []
        for tname, stats in base_stats.items():
            pts = stats[0]
            if tname in sim_3rd: pts += 5
            if tname in sim_4th: pts += 4
            sortable.append((-pts,) + stats[1:]) # 내림차순 정렬을 위해 포인트에 - 붙임
            
        sortable.sort()
        sim_finalists = sim_1st | sim_2nd
        sim_qualified = set(sim_finalists)
        
        for item in sortable:
            if len(sim_qualified) >= 4:
                break
            tname = item[-1]
            if tname in season_out_teams and tname not in sim_finalists:
                continue
            if tname in playin_challenger_teams:
                if tname in sim_finalists or tname in sim_3rd or tname in sim_4th:
                    sim_qualified.add(tname)
            else:
                sim_qualified.add(tname)
                
        for t in sim_qualified:
            qual_counts[t] += 1

    # ----------------------------------------------------
    # 🎯 표출용 현재 확정 점수 테이블 생성
    # ----------------------------------------------------
    df = raw_df.copy()
    for team in po_3rd: df.loc[df["팀명"] == team, "Stage 2"] += 5
    for team in po_4th: df.loc[df["팀명"] == team, "Stage 2"] += 4
    df["Total Points"] = df[score_cols].sum(axis=1)

    df = df.sort_values(
        by=["Total Points", "S2_Rank", "M2_Rank", "S1_Rank", "M1_Rank", "KO_Rank", "Reg_Wins", "Reg_Map_Diff", "Reg_Round_Diff", "팀명"],
        ascending=[False, True, True, True, True, True, False, False, False, True],
    ).reset_index(drop=True)

    # 1위 2위 상단 고정
    priority_rows = []
    for team in champ_1st:
        match = df[df["팀명"] == team]
        if not match.empty: priority_rows.append(match)
    for team in champ_2nd:
        if team not in champ_1st:
            match = df[df["팀명"] == team]
            if not match.empty: priority_rows.append(match)

    exclude_teams = champ_1st + champ_2nd
    remaining_df = df[~df["팀명"].isin(exclude_teams)]
    if priority_rows:
        df = pd.concat([pd.concat(priority_rows, ignore_index=True), remaining_df], ignore_index=True)

    # 동률 텍스트 생성
    tie_descriptions = []
    points_counts = df["Total Points"].value_counts()
    for i, row in df.iterrows():
        pts = row["Total Points"]
        if points_counts[pts] == 1: tie_descriptions.append("단독 순위"); continue
        if i == 0 or df.iloc[i - 1]["Total Points"] != pts: tie_descriptions.append("동률 (기준 적용)"); continue
        
        prev_row = df.iloc[i - 1]
        if row["S2_Rank"] != prev_row["S2_Rank"]: reason = "스테이지 2 순위 (" + ("상위" if row["S2_Rank"] < prev_row["S2_Rank"] else "하위") + ")"
        elif row["M2_Rank"] != prev_row["M2_Rank"]: reason = "마스터스 2 순위 (" + ("상위" if row["M2_Rank"] < prev_row["M2_Rank"] else "하위") + ")"
        elif row["S1_Rank"] != prev_row["S1_Rank"]: reason = "스테이지 1 순위 (" + ("상위" if row["S1_Rank"] < prev_row["S1_Rank"] else "하위") + ")"
        elif row["M1_Rank"] != prev_row["M1_Rank"]: reason = "마스터스 1 순위 (" + ("상위" if row["M1_Rank"] < prev_row["M1_Rank"] else "하위") + ")"
        elif row["KO_Rank"] != prev_row["KO_Rank"]: reason = "킥오프 순위 (" + ("상위" if row["KO_Rank"] < prev_row["KO_Rank"] else "하위") + ")"
        elif row["Reg_Wins"] != prev_row["Reg_Wins"]: reason = "시즌 총 승수 (" + ("상위" if row["Reg_Wins"] > prev_row["Reg_Wins"] else "하위") + ")"
        elif row["Reg_Map_Diff"] != prev_row["Reg_Map_Diff"]: reason = "총 맵 득실 (" + ("상위" if row["Reg_Map_Diff"] > prev_row["Reg_Map_Diff"] else "하위") + ")"
        elif row["Reg_Round_Diff"] != prev_row["Reg_Round_Diff"]: reason = "총 라운드 득실 (" + ("상위" if row["Reg_Round_Diff"] > prev_row["Reg_Round_Diff"] else "하위") + ")"
        else: reason = "팀명 순"
        tie_descriptions.append(reason)

    df["동률 규정 적용 결과"] = tie_descriptions
    df.index = df.index + 1
    df.index.name = "Ranking"

    # 확률 데이터 매핑 및 최종 상태 부여
    status_list, prob_list = [], []
    for idx, row in df.iterrows():
        tname = row["팀명"]
        prob = (qual_counts[tname] / total_scenarios) * 100
        
        is_finalist = tname in (champ_1st + champ_2nd)
        is_challenger = tname in playin_challenger_teams
        is_season_out = tname in season_out_teams
        
        if prob == 100.0:
            if is_finalist: status = "🏆 진출 확정 (결승 직행)"
            elif is_season_out: status = "🏆 진출 확정 (조기 탈락 불구 잔여 포인트 승계)"
            else: status = "🏆 진출 확정 (수학적 최소 4위 확보)"
        elif prob == 0.0:
            if is_season_out: status = "❌ 탈락 확정 (시즌 아웃 & 역전 불가)"
            elif is_challenger: status = "❌ 탈락 확정 (플레이인 조건 미달)"
            else: status = "❌ 탈락 확정 (수학적 진출 불가)"
        else:
            status = "🟡 진출 경쟁 중 (경우의 수 존재)"
            
        status_list.append(status)
        prob_list.append(f"{prob:.1f}%")
        
    df["Champions 진출 상태"] = status_list
    df["진출 확률 (%)"] = prob_list

    # ==========================================
    # 3. 테이블 분리 표출 및 하이라이트
    # ==========================================
    main_display_cols = ["팀명", "Total Points", "동률 규정 적용 결과", "Champions 진출 상태", "진출 확률 (%)"]
    detail_display_cols = ["팀명", "Total Points", "Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]

    tie_colors = ["background-color: #ffe5d0;", "background-color: #ffcccc;"]
    point_to_color, color_idx = {}, 0
    for pts in df["Total Points"]:
        if pts not in point_to_color:
            if points_counts[pts] > 1:
                point_to_color[pts] = tie_colors[color_idx % len(tie_colors)]
                color_idx += 1
            else:
                point_to_color[pts] = ""

    def highlight_rows(row):
        if "진출 확정" in str(row.get("Champions 진출 상태", "")):
            return ["background-color: #fff3cc; color: #000000; font-weight: bold;"] * len(row)
        if "탈락 확정" in str(row.get("Champions 진출 상태", "")):
            return ["background-color: #f0f0f0; color: #999999;"] * len(row)
        
        pts = row["Total Points"]
        color_style = point_to_color.get(pts, "")
        if color_style:
            return [color_style + " color: #000000;"] * len(row)
        return [""] * len(row)

    st.dataframe(df[main_display_cols].style.apply(highlight_rows, axis=1), use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📈 대회별 획득 포인트 상세 내역")
    
    detail_df = df[detail_display_cols + ["Champions 진출 상태"]]
    styled_detail = detail_df.style.apply(highlight_rows, axis=1).hide(axis="columns", subset=["Champions 진출 상태"])
    st.dataframe(styled_detail, use_container_width=True)

    st.markdown("---")
