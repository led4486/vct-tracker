import pandas as pd
import streamlit as st
import itertools

# ==========================================
# 1. 페이지 설정 및 초기화
# ==========================================
st.set_page_config(
    page_title="VCT 2026 Champions 진출 트래커",
    layout="wide",
    page_icon="🎮",
)

st.title("🎮 VCT 2026 Champions 실시간 브라켓 시뮬레이터")
st.caption("플레이오프 512개 대진 시나리오 몬테카를로 전수조사 | 'GE 승리 & T1 패배 시 진출' 등 맞춤형 조건 자동 산출 엔진 탑재")

# ------------------------------------------
# 🔐 관리자 사이드바
# ------------------------------------------
st.sidebar.title("🔐 관리자 설정")
admin_password = st.sidebar.text_input("데이터 편집 비밀번호", type="password")

# ==========================================
# 2. 데이터 셋업 (점수 완벽 동기화)
# ==========================================
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
alive_teams = ["Nongshim RedForce", "VARREL", "Global Esports", "Gen.G Esports", "Paper Rex", "ONSIDE GAMING (ONG)", "KRX", "T1"]

# ==========================================
# 3. 탭 구성 및 메인 로직
# ==========================================
tab1, tab2 = st.tabs(["📊 1. 현재 브라켓 시뮬레이터", "🏆 2. 데이터 편집"])

with tab2:
    st.subheader("🏆 대회별 포인트 데이터 수정")
    if admin_password == "1234":
        st.session_state.points_table = st.data_editor(st.session_state.points_table, num_rows="dynamic", use_container_width=True)
    else:
        st.warning("데이터를 수정하려면 좌측 사이드바에 관리자 비밀번호를 입력해주세요.")
        st.dataframe(st.session_state.points_table, use_container_width=True)

with tab1:
    st.subheader("🎯 오늘의 매치업 결과 반영 (시뮬레이터)")
    st.markdown("오늘 진행되는 플레이오프 경기의 결과를 선택해보세요. AI 알고리즘이 남은 브라켓의 모든 경우의 수를 분석하여 실시간 진출 확률과 100% 확정 조건을 산출합니다.")

    # UI 라디오 버튼 배치
    c1, c2, c3 = st.columns(3)
    with c1: m0_res = st.radio("⚔️ Upper Semi", ["미정 (시뮬레이션)", "VARREL 승", "GE 승"])
    with c2: m1_res = st.radio("🛡️ Lower R1 (1경기)", ["미정 (시뮬레이션)", "PRX 승", "ONG 승"])
    with c3: m2_res = st.radio("🛡️ Lower R1 (2경기)", ["미정 (시뮬레이션)", "KRX 승", "T1 승"])

    # 선택 결과 데이터화
    fixed_outcomes = {}
    if "VARREL" in m0_res: fixed_outcomes[0] = 0
    elif "GE" in m0_res: fixed_outcomes[0] = 1
    
    if "PRX" in m1_res: fixed_outcomes[1] = 0
    elif "ONG" in m1_res: fixed_outcomes[1] = 1
    
    if "KRX" in m2_res: fixed_outcomes[2] = 0
    elif "T1" in m2_res: fixed_outcomes[2] = 1

    st.markdown("---")
    st.subheader("📊 VCT Pacific 공식 챔피언스 진출 확률 및 맞춤형 경우의 수")

    # 기본 데이터 전처리
    raw_df = st.session_state.points_table.copy()
    score_cols = ["Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]
    for col in score_cols: raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce").fillna(0)
    raw_df["Base Points"] = raw_df[score_cols].sum(axis=1)
    
    base_stats_dict = {}
    tiebreaker_stats = {}
    for _, row in raw_df.iterrows():
        tname = row["팀명"]
        base_stats_dict[tname] = row["Base Points"]
        tiebreaker_stats[tname] = (
            pd.to_numeric(row.get("S2_Rank", 99), errors="coerce"),
            pd.to_numeric(row.get("M2_Rank", 99), errors="coerce"),
            pd.to_numeric(row.get("S1_Rank", 99), errors="coerce"),
            pd.to_numeric(row.get("M1_Rank", 99), errors="coerce"),
            pd.to_numeric(row.get("KO_Rank", 99), errors="coerce"),
            -pd.to_numeric(row.get("Reg_Wins", 0), errors="coerce"),
            -pd.to_numeric(row.get("Reg_Map_Diff", 0), errors="coerce"),
            -pd.to_numeric(row.get("Reg_Round_Diff", 0), errors="coerce")
        )

    # ----------------------------------------------------
    # 🎲 남은 브라켓 경우의 수 512개 몬테카를로 전수조사
    # ----------------------------------------------------
    valid_universes = []
    qual_counts = {t: 0 for t in all_teams}

    for combo in itertools.product([0, 1], repeat=9):
        # 사용자가 고정한 결과 필터링
        skip = False
        for k, v in fixed_outcomes.items():
            if combo[k] != v: skip = True; break
        if skip: continue

        # 1. 브라켓 진행 로직 (회원님 제공 기준)
        w_m0 = "VARREL" if combo[0] == 0 else "Global Esports"
        l_m0 = "Global Esports" if combo[0] == 0 else "VARREL"
        
        w_m1 = "Paper Rex" if combo[1] == 0 else "ONSIDE GAMING (ONG)"
        w_m2 = "KRX" if combo[2] == 0 else "T1"

        w_m3 = "Nongshim RedForce" if combo[3] == 0 else w_m0  # UF
        l_m3 = w_m0 if combo[3] == 0 else "Nongshim RedForce"
        
        w_m4 = l_m0 if combo[4] == 0 else w_m1  # LR2 (1)
        w_m5 = "Gen.G Esports" if combo[5] == 0 else w_m2  # LR2 (2)

        w_m6 = w_m4 if combo[6] == 0 else w_m5  # LR3 (승자 LF진출, 패자 4위)
        l_m6 = w_m5 if combo[6] == 0 else w_m4  # 4위
        
        w_m7 = l_m3 if combo[7] == 0 else w_m6  # LF (승자 GF진출, 패자 3위)
        l_m7 = w_m6 if combo[7] == 0 else l_m3  # 3위
        
        w_m8 = w_m3 if combo[8] == 0 else w_m7  # 1위
        l_m8 = w_m7 if combo[8] == 0 else w_m3  # 2위

        placements = {"1st": w_m8, "2nd": l_m8, "3rd": l_m7, "4th": l_m6}

        # 2. 포인트 적용 및 순위 정렬
        sim_pts = base_stats_dict.copy()
        sim_pts[l_m7] += 5
        sim_pts[l_m6] += 4

        sortable = []
        for tname in all_teams:
            sortable.append((-sim_pts[tname],) + tiebreaker_stats[tname] + (tname,))
        sortable.sort()

        # 3. 챔피언스 진출권(4장) 부여
        qualified = set([w_m8, l_m8])
        for item in sortable:
            if len(qualified) >= 4: break
            tname = item[-1]
            # 플레이인 팀 조건 필터 (Top 4 안에 들어야만 가능)
            if tname in playin_challenger_teams:
                if tname in placements.values(): qualified.add(tname)
            else:
                qualified.add(tname)

        valid_universes.append((combo, qualified))
        for t in qualified: qual_counts[t] += 1

    total_valid = len(valid_universes)

    # ----------------------------------------------------
    # 🧠 경우의 수 분석 조건 도출 함수
    # ----------------------------------------------------
    m_cond_text = [
        ("VARREL 승리", "GE 승리"),
        ("PRX 승리", "ONG 승리"),
        ("KRX 승리(T1 패배)", "T1 승리")
    ]

    def get_dynamic_condition(tname, prob, universes):
        if prob == 100.0:
            if tname == "Nongshim RedForce": return "🏆 100% 진출 확정 (최소 3위 확보로 타팀 역전 수학적 불가)"
            if tname == "Paper Rex": return "🏆 100% 진출 확정 (이미 확보한 압도적 누적 점수로 확정)"
            return "🏆 100% 진출 확정 (경우의 수 무관 확정)"
        if prob == 0.0:
            return "❌ 탈락 확정 (수학적 진출 경우의 수 소멸)"

        # 1경기 조건 분석
        for m_idx in range(3):
            if m_idx in fixed_outcomes: continue
            for out in [0, 1]:
                sub = [u for u in universes if u[0][m_idx] == out]
                if sub and all(tname in u[1] for u in sub):
                    return f"🔥 {m_cond_text[m_idx][out]} 시 100% 진출 확정!"
        
        # 2경기 조건 분석 (예: GE승 & T1패)
        active_m = [i for i in range(3) if i not in fixed_outcomes]
        for m1, m2 in itertools.combinations(active_m, 2):
            for o1, o2 in itertools.product([0,1], [0,1]):
                sub = [u for u in universes if u[0][m1] == o1 and u[0][m2] == o2]
                if sub and all(tname in u[1] for u in sub):
                    return f"🔥 {m_cond_text[m1][o1]} 및 {m_cond_text[m2][o2]} 시 100% 확정!"

        # 3경기 모두 맞물려야 하는 경우
        if len(active_m) == 3:
            for o0, o1, o2 in itertools.product([0,1], [0,1], [0,1]):
                sub = [u for u in universes if u[0][0] == o0 and u[0][1] == o1 and u[0][2] == o2]
                if sub and all(tname in u[1] for u in sub):
                    return f"🔥 {m_cond_text[0][o0]}, {m_cond_text[1][o1]}, {m_cond_text[2][o2]} 충족 시 확정!"

        if tname == "Gen.G Esports":
            return "⚡ 벼랑 끝 경쟁 중 (로어 브라켓 연승 필수 및 상위팀 대이변 필요)"
        return "⚡ 진출 경쟁 중 (타팀 결과 의존 및 후속 라운드 연승 등 복합적 작용 필요)"

    # ----------------------------------------------------
    # 🎯 데이터 매핑 및 최종 표출
    # ----------------------------------------------------
    status_list, prob_list = [], []
    for _, row in raw_df.iterrows():
        tname = row["팀명"]
        if tname not in alive_teams:
            if base_stats_dict[tname] >= 25:
                status_list.append("🏆 100% 진출 확정 (시즌 아웃에도 확보 포인트로 진출)")
                prob_list.append("100.0%")
            else:
                status_list.append("❌ 탈락 확정 (시즌 아웃 및 포인트 미달)")
                prob_list.append("0.0%")
            continue
        
        prob = (qual_counts[tname] / total_valid) * 100 if total_valid > 0 else 0
        cond_text = get_dynamic_condition(tname, prob, valid_universes)
        
        if prob == 100.0 and "진출 확정" not in cond_text:
            cond_text = "🏆 100% 진출 확정 (모든 경우의 수 통과)"

        status_list.append(cond_text)
        prob_list.append(f"{prob:.1f}%")

    raw_df["경우의 수 및 진출 상태"] = status_list
    raw_df["진출 확률 (%)"] = prob_list

    display_cols = ["팀명", "Base Points", "진출 확률 (%)", "경우의 수 및 진출 상태", "Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]

    def highlight_rows(row):
        status = str(row["경우의 수 및 진출 상태"])
        if "100% 진출 확정" in status:
            return ["background-color: #fff3cc; color: #000000; font-weight: bold;"] * len(row)
        elif "탈락 확정" in status:
            return ["background-color: #f0f0f0; color: #999999;"] * len(row)
        elif "🔥" in status:
            return ["background-color: #ffe5d0; color: #000000;"] * len(row)
        elif "⚡" in status:
            return ["background-color: #ffcccc; color: #000000;"] * len(row)
        return [""] * len(row)

    final_df = raw_df.sort_values(by="Base Points", ascending=False).reset_index(drop=True)
    final_df.index = final_df.index + 1
    final_df.index.name = "현재 순위"

    st.dataframe(final_df[display_cols].style.apply(highlight_rows, axis=1), use_container_width=True)

    st.markdown("---")
    st.info("💡 **AI 정밀 분석 코멘트:** 상단 UI에서 **'GE 승'**과 **'KRX 승(T1 패)'**를 선택해 보세요! GE의 확률이 100%로 솟구치며 자력 진출이 확정되는 짜릿한 수학적 알고리즘을 실시간으로 확인하실 수 있습니다.")
