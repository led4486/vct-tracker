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
st.caption("Upper Semi GE 승리 고정 | 플레이오프 단계별 순위(S2_Rank) 자동 변동 및 실시간 포인트 반영 시스템")

# ------------------------------------------
# 🔐 관리자 사이드바
# ------------------------------------------
st.sidebar.title("🔐 관리자 설정")
admin_password = st.sidebar.text_input("데이터 편집 비밀번호", type="password")

# ==========================================
# 2. 기본 포인트 및 팀 데이터
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
# 3. UI 및 동적 대진표 생성기
# ==========================================
tab1, tab2 = st.tabs(["📊 1. 전체 브라켓 동적 시뮬레이터", "🏆 2. 데이터 편집"])

with tab2:
    st.subheader("🏆 대회별 포인트 데이터 수정")
    if admin_password == "1234":
        st.session_state.points_table = st.data_editor(st.session_state.points_table, num_rows="dynamic", use_container_width=True)
    else:
        st.warning("데이터를 수정하려면 좌측 사이드바에 관리자 비밀번호를 입력해주세요.")
        st.dataframe(st.session_state.points_table, use_container_width=True)

with tab1:
    st.subheader("🎯 잔여 플레이오프 전체 매치 진행상황 입력")
    st.markdown("Upper Semi는 **GE 승리**로 고정되었습니다. 남은 경기의 승자를 선택하면 **패배한 팀의 순위(S2_Rank)와 포인트가 공식 룰에 맞게 실시간 갱신**됩니다.")

    match_labels = {}
    fixed_outcomes = {0: 1} # 0번 매치(Upper Semi) GE 승리(1)로 강제 고정

    def match_ui(idx, col, title, t1, t2, w_place, l_place=None, default_idx=0):
        if idx == 0:
            col.markdown(f"**{title}**")
            col.info("🔥 Global Esports 승리 (확정)")
            match_labels[idx] = (t1, t2)
            return t2, t1 # 승자 GE, 패자 VARREL
            
        opts = ["미정", f"{t1} 승", f"{t2} 승"]
        res = col.radio(title, opts, key=f"m_{idx}", index=default_idx)
        match_labels[idx] = (t1, t2)
        if res == opts[1]:
            fixed_outcomes[idx] = 0
            return t1, t2
        elif res == opts[2]:
            fixed_outcomes[idx] = 1
            return t2, t1
        return w_place, (l_place if l_place else f"{w_place}패자")

    # [1라운드] 
    st.markdown("#### 🔹 Round 1 (상위/하위)")
    c1, c2, c3 = st.columns(3)
    w_m0, l_m0 = match_ui(0, c1, "⚔️ Upper Semi", "VARREL", "Global Esports", "[US 승자]", "[US 패자]")
    w_m1, l_m1 = match_ui(1, c2, "🛡️ Lower R1 (1)", "Paper Rex", "ONSIDE GAMING (ONG)", "[LR1(1) 승자]", "[LR1(1) 패자]")
    w_m2, l_m2 = match_ui(2, c3, "🛡️ Lower R1 (2)", "KRX", "T1", "[LR1(2) 승자]", "[LR1(2) 패자]")

    # [2라운드]
    st.markdown("#### 🔹 Round 2 (어퍼 결승 / 하위 R2)")
    c4, c5, c6 = st.columns(3)
    w_m3, l_m3 = match_ui(3, c4, "🔥 Upper Final", "Nongshim RedForce", w_m0, "[UF 승자]", "[UF 패자]")
    w_m4, l_m4 = match_ui(4, c5, "🛡️ Lower R2 (1)", l_m0, w_m1, "[LR2(1) 승자]", "[LR2(1) 패자]")
    w_m5, l_m5 = match_ui(5, c6, "🛡️ Lower R2 (2)", "Gen.G Esports", w_m2, "[LR2(2) 승자]", "[LR2(2) 패자]")

    # [3라운드 & 파이널]
    st.markdown("#### 🔹 Finals & Lower R3")
    c7, c8, c9 = st.columns(3)
    w_m6, l_m6 = match_ui(6, c7, "🛡️ Lower R3", w_m4, w_m5, "[LR3 승자]", "[LR3 패자]")
    w_m7, l_m7 = match_ui(7, c8, "🔥 Lower Final", l_m3, w_m6, "[LF 승자]", "[LF 패자]")
    w_m8, l_m8 = match_ui(8, c9, "🏆 Grand Final", w_m3, w_m7, "[우승]", "[준우승]")

    # ----------------------------------------------------
    # 🎲 9경기 512개 시나리오 전수조사 및 순위(S2_Rank) 부여
    # ----------------------------------------------------
    raw_df = st.session_state.points_table.copy()
    score_cols = ["Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]
    for col in score_cols: raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce").fillna(0)
    raw_df["Total Points"] = raw_df[score_cols].sum(axis=1)
    
    base_stats_dict = {row["팀명"]: row["Total Points"] for _, row in raw_df.iterrows()}

    valid_universes = []
    qual_counts = {t: 0 for t in all_teams}
    team_success_ranks = {t: set() for t in all_teams}

    for combo in itertools.product([0, 1], repeat=9):
        skip = False
        for k, v in fixed_outcomes.items():
            if combo[k] != v: skip = True; break
        if skip: continue

        c_w0 = "VARREL" if combo[0] == 0 else "Global Esports"
        c_l0 = "Global Esports" if combo[0] == 0 else "VARREL"
        c_w1 = "Paper Rex" if combo[1] == 0 else "ONSIDE GAMING (ONG)"
        c_l1 = "ONSIDE GAMING (ONG)" if combo[1] == 0 else "Paper Rex"
        c_w2 = "KRX" if combo[2] == 0 else "T1"
        c_l2 = "T1" if combo[2] == 0 else "KRX"
        
        c_w3 = "Nongshim RedForce" if combo[3] == 0 else c_w0
        c_l3 = c_w0 if combo[3] == 0 else "Nongshim RedForce"
        
        c_w4 = c_l0 if combo[4] == 0 else c_w1
        c_l4 = c_w1 if combo[4] == 0 else c_l0
        
        c_w5 = "Gen.G Esports" if combo[5] == 0 else c_w2
        c_l5 = c_w2 if combo[5] == 0 else "Gen.G Esports"
        
        c_w6 = c_w4 if combo[6] == 0 else c_w5
        c_l6 = c_w5 if combo[6] == 0 else c_w4  # 4위 (Lower R3 패자)
        
        c_w7 = c_l3 if combo[7] == 0 else c_w6
        c_l7 = c_w6 if combo[7] == 0 else c_l3  # 3위 (Lower Final 패자)
        
        c_w8 = c_w3 if combo[8] == 0 else c_w7  # 1위
        c_l8 = c_w7 if combo[8] == 0 else c_w3  # 2위

        placements = {1: c_w8, 2: c_l8, 3: c_l7, 4: c_l6}

        # ----------------------------------------------------
        # 📌 단계별 탈락 팀 Stage 2 순위 매핑 (S2_Rank)
        # Lower R1 패자(2팀) > 8위
        # Lower R2 패자(2팀) > 6위
        # Lower R3 패자(1팀) > 4위
        # Lower Final 패자(1팀) > 3위
        # Grand Final 패자(1팀) > 2위
        # Grand Final 승자(1팀) > 1위
        # ----------------------------------------------------
        sim_ranks = {t: 99 for t in all_teams}
        sim_ranks[c_w8] = 1
        sim_ranks[c_l8] = 2
        sim_ranks[c_l7] = 3
        sim_ranks[c_l6] = 4
        sim_ranks[c_l4] = 6 # Lower R2 패자
        sim_ranks[c_l5] = 6 # Lower R2 패자
        sim_ranks[c_l1] = 8 # Lower R1 패자
        sim_ranks[c_l2] = 8 # Lower R1 패자
        sim_ranks[c_l0] = 5 # Upper Semi 패자는 Upper Final 패자와 동급이거나 하위 R2 진출하므로 유동적 (기본유지)

        sim_pts = base_stats_dict.copy()
        sim_pts[c_l7] += 5
        sim_pts[c_l6] += 4

        # 동률 순위 산정용 타이브레이커 튜플 구성
        tiebreaker_stats = {}
        for tname in all_teams:
            s2_val = sim_ranks[tname]
            tiebreaker_stats[tname] = (
                s2_val,
                pd.to_numeric(raw_df.loc[raw_df["팀명"]==tname, "M2_Rank"], errors="coerce").values[0],
                pd.to_numeric(raw_df.loc[raw_df["팀명"]==tname, "S1_Rank"], errors="coerce").values[0],
                pd.to_numeric(raw_df.loc[raw_df["팀명"]==tname, "M1_Rank"], errors="coerce").values[0],
                pd.to_numeric(raw_df.loc[raw_df["팀명"]==tname, "KO_Rank"], errors="coerce").values[0],
                -pd.to_numeric(raw_df.loc[raw_df["팀명"]==tname, "Reg_Wins"], errors="coerce").values[0],
                -pd.to_numeric(raw_df.loc[raw_df["팀명"]==tname, "Reg_Map_Diff"], errors="coerce").values[0],
                -pd.to_numeric(raw_df.loc[raw_df["팀명"]==tname, "Reg_Round_Diff"], errors="coerce").values[0]
            )

        sortable = []
        for tname in all_teams:
            sortable.append((-sim_pts[tname],) + tiebreaker_stats[tname] + (tname,))
        sortable.sort()

        qualified = set([c_w8, c_l8])
        for item in sortable:
            if len(qualified) >= 4: break
            tname = item[-1]
            if tname in playin_challenger_teams:
                if tname in placements.values(): qualified.add(tname)
            else:
                qualified.add(tname)

        valid_universes.append((combo, qualified, placements))
        for t in qualified: qual_counts[t] += 1

    total_valid = len(valid_universes)

    # ----------------------------------------------------
    # 🎯 UI 표출용 실시간 점수 및 순위 반영
    # ----------------------------------------------------
    l1_losers = {l_m1} if l_m1 else set()
    l2_losers = {l_m2} if l_m2 else set()
    l6_set = set(u[2][4] for u in valid_universes)
    l7_set = set(u[2][3] for u in valid_universes)
    
    fixed_4th = l6_set.pop() if len(l6_set) == 1 else None
    fixed_3rd = l7_set.pop() if len(l7_set) == 1 else None

    # 실시간 포인트 및 순위(S2_Rank) 덮어쓰기
    if l_m1 in all_teams: raw_df.loc[raw_df["팀명"] == l_m1, "S2_Rank"] = 8
    if l_m2 in all_teams: raw_df.loc[raw_df["팀명"] == l_m2, "S2_Rank"] = 8
    if fixed_4th:
        raw_df.loc[raw_df["팀명"] == fixed_4th, "Stage 2"] += 4
        raw_df.loc[raw_df["팀명"] == fixed_4th, "Total Points"] += 4
        raw_df.loc[raw_df["팀명"] == fixed_4th, "S2_Rank"] = 4
    if fixed_3rd:
        raw_df.loc[raw_df["팀명"] == fixed_3rd, "Stage 2"] += 5
        raw_df.loc[raw_df["팀명"] == fixed_3rd, "Total Points"] += 5
        raw_df.loc[raw_df["팀명"] == fixed_3rd, "S2_Rank"] = 3

    # ----------------------------------------------------
    # 🧠 AI 힌트 및 표출 로직
    # ----------------------------------------------------
    status_list, prob_list = [], []
    for _, row in raw_df.iterrows():
        tname = row["팀명"]
        if tname not in alive_teams:
            if row["Total Points"] >= 25:
                status_list.append("🏆 100% 진출 확정 (누적 포인트로 확정)")
                prob_list.append("100.0%")
            else:
                status_list.append("❌ 탈락 확정")
                prob_list.append("0.0%")
            continue
        
        prob = (qual_counts[tname] / total_valid) * 100 if total_valid > 0 else 0
        
        if prob == 100.0:
            cond_text = "🏆 100% 진출 확정"
        elif prob == 0.0:
            cond_text = "❌ 탈락 확정"
        else:
            hint = ""
            for m_idx in range(9):
                if m_idx not in fixed_outcomes:
                    t1, t2 = match_labels[m_idx]
                    if t1.startswith("[") or t2.startswith("["): continue
                    sub0 = [u for u in valid_universes if u[0][m_idx] == 0]
                    if sub0 and all(tname in u[1] for u in sub0):
                        hint = f" 👉 [💡AI: '{t1}' 승리 시 100% 확정]"
                        break
                    sub1 = [u for u in valid_universes if u[0][m_idx] == 1]
                    if sub1 and all(tname in u[1] for u in sub1):
                        hint = f" 👉 [💡AI: '{t2}' 승리 시 100% 확정]"
                        break
                if hint: break
            cond_text = f"🔥 진출 경쟁 중 ({prob:.1f}%)" + hint

        status_list.append(cond_text)
        prob_list.append(f"{prob:.1f}%")

    raw_df["경우의 수 및 진출 상태"] = status_list
    raw_df["진출 확률 (%)"] = prob_list

    display_cols = ["팀명", "Total Points", "진출 확률 (%)", "경우의 수 및 진출 상태", "S2_Rank", "Stage 2"]

    def highlight_rows(row):
        status = str(row["경우의 수 및 진출 상태"])
        if "100% 진출 확정" in status:
            return ["background-color: #fff3cc; color: #000000; font-weight: bold;"] * len(row)
        elif "탈락 확정" in status:
            return ["background-color: #f0f0f0; color: #888888;"] * len(row)
        elif "💡AI" in status:
            return ["background-color: #e6f7ff; color: #000000;"] * len(row)
        return [""] * len(row)

    final_df = raw_df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)
    final_df.index = final_df.index + 1
    final_df.index.name = "현재 순위"

    st.dataframe(final_df[display_cols].style.apply(highlight_rows, axis=1), use_container_width=True)
    st.markdown("---")
