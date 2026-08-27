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
st.caption("플레이오프 9경기 전수조사 | 3위(+5점), 4위(+4점) 실시간 점수 반영 및 진출 힌트 AI 탑재")

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

# ----------------------------------------------------
# ⚡ 연산 속도 향상을 위한 시뮬레이션 캐싱 함수 추가
# ----------------------------------------------------
@st.cache_data
def run_simulation(fixed_outcomes_tuple, base_stats_dict, extra_stats_dict):
    fixed_outcomes = dict(fixed_outcomes_tuple)
    valid_universes = []
    qual_counts = {t: 0 for t in all_teams}
    team_success_ranks = {t: set() for t in all_teams}

    for combo in itertools.product([0, 1], repeat=9):
        skip = False
        for k, v in fixed_outcomes.items():
            if combo[k] != v:
                skip = True
                break
        if skip:
            continue

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

        sim_ranks = {t: 99 for t in all_teams}
        sim_ranks[c_w8], sim_ranks[c_l8], sim_ranks[c_l7], sim_ranks[c_l6] = 1, 2, 3, 4
        sim_ranks[c_l4], sim_ranks[c_l5] = 6, 6
        sim_ranks[c_l1], sim_ranks[c_l2] = 8, 8

        sim_pts = base_stats_dict.copy()
        sim_pts[c_l7] += 5
        sim_pts[c_l6] += 4

        sortable = []
        for tname in all_teams:
            s2_val = sim_ranks[tname]
            ext = extra_stats_dict[tname]
            tb_tuple = (s2_val, ext["M2"], ext["S1"], ext["M1"], ext["KO"], -ext["Reg_Wins"], -ext["Reg_Map"], -ext["Reg_Round"])
            sortable.append((-sim_pts[tname],) + tb_tuple + (tname,))
        sortable.sort()

        qualified = set([c_w8, c_l8])
        for item in sortable:
            if len(qualified) >= 4:
                break
            tname = item[-1]
            if tname in playin_challenger_teams:
                if tname in placements.values():
                    qualified.add(tname)
            else:
                qualified.add(tname)

        valid_universes.append((combo, qualified, placements))
        for t in qualified:
            qual_counts[t] += 1
            rank = 5
            for r, team in placements.items():
                if team == t:
                    rank = r
            team_success_ranks[t].add(rank)

    return valid_universes, qual_counts, team_success_ranks


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
    st.markdown("Upper Semi는 **GE 승리**로 고정되었습니다. 남은 경기의 승자를 선택하면 **3위(+5점), 4위(+4점)** 및 단계별 탈락 순위가 실시간 반영됩니다.")

    match_labels = {}
    fixed_outcomes = {0: 1} # Upper Semi GE 승리(1) 고정

    def match_ui(idx, col, title, t1, t2, w_place, l_place=None):
        if idx == 0:
            col.markdown(f"**{title}**")
            col.info("🔥 Global Esports 승리 (확정)")
            match_labels[idx] = (t1, t2)
            return t2, t1
            
        opts = ["미정", f"{t1} 승", f"{t2} 승"]
        res = col.radio(title, opts, key=f"m_{idx}")
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

    st.markdown("---")
    st.subheader("📊 VCT Pacific 실시간 챔피언스 진출 확률 및 누적 포인트 현황")

    # 기본 데이터 전처리 및 사전 딕셔너리 생성
    raw_df = st.session_state.points_table.copy()
    score_cols = ["Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]
    for col in score_cols: raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce").fillna(0)
    raw_df["Total Points"] = raw_df[score_cols].sum(axis=1)
    
    base_stats_dict = {row["팀명"]: row["Total Points"] for _, row in raw_df.iterrows()}
    extra_stats_dict = {}
    for _, row in raw_df.iterrows():
        extra_stats_dict[row["팀명"]] = {
            "M2": pd.to_numeric(row.get("M2_Rank", 99), errors="coerce"),
            "S1": pd.to_numeric(row.get("S1_Rank", 99), errors="coerce"),
            "M1": pd.to_numeric(row.get("M1_Rank", 99), errors="coerce"),
            "KO": pd.to_numeric(row.get("KO_Rank", 99), errors="coerce"),
            "Reg_Wins": pd.to_numeric(row.get("Reg_Wins", 0), errors="coerce"),
            "Reg_Map": pd.to_numeric(row.get("Reg_Map_Diff", 0), errors="coerce"),
            "Reg_Round": pd.to_numeric(row.get("Reg_Round_Diff", 0), errors="coerce"),
        }

    # ----------------------------------------------------
    # 🎲 캐싱된 시뮬레이션 전수조사 호출 (속도 최적화 핵심)
    # ----------------------------------------------------
    fixed_outcomes_tuple = tuple(sorted(fixed_outcomes.items()))
    valid_universes, qual_counts, team_success_ranks = run_simulation(fixed_outcomes_tuple, base_stats_dict, extra_stats_dict)

    total_valid = len(valid_universes)

    # ----------------------------------------------------
    # 🎯 UI 표출용 실시간 점수 및 S2_Rank 반영
    # ----------------------------------------------------
    l6_set = set(u[2][4] for u in valid_universes)
    l7_set = set(u[2][3] for u in valid_universes)
    
    fixed_4th = l6_set.pop() if len(l6_set) == 1 else None
    fixed_3rd = l7_set.pop() if len(l7_set) == 1 else None

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
    # 🧠 AI 분석: 남은 매치 결과 기반 100% 힌트 도출
    # ----------------------------------------------------
    def get_dynamic_condition(tname, prob, universes):
        if prob == 100.0:
            if tname == "Nongshim RedForce": return "🏆 100% 진출 확정 (어퍼 파이널 진출로 자력 확정)"
            if tname == "Paper Rex" and len(fixed_outcomes) == 0: return "🏆 100% 진출 확정 (누적 포인트 압도적 1위)"
            return "🏆 100% 진출 확정 (현재 선택된 매치 결과로 확정)"
        if prob == 0.0:
            return "❌ 탈락 확정 (수학적 진출 경우의 수 소멸)"

        ranks = team_success_ranks[tname]
        easiest_rank = max(ranks) if ranks else 5
        if easiest_rank == 5: base_text = f"🔥 경쟁 중 ({prob:.1f}% / PO 하위권 탈락 시에도 타팀 부진 시 진출)"
        elif easiest_rank == 4: base_text = f"🔥 경쟁 중 ({prob:.1f}% / 4위(+4점) 이상 진입 시 확률 상승)"
        elif easiest_rank == 3: base_text = f"⚡ 경쟁 중 ({prob:.1f}% / 최소 3위(+5점) 확보 필수)"
        else: base_text = f"⚡ 벼랑 끝 ({prob:.1f}% / 결승 직행 필수)"

        hint = ""
        for m_idx in range(9):
            if m_idx not in fixed_outcomes:
                t1, t2 = match_labels[m_idx]
                if t1.startswith("[") or t2.startswith("["): continue
                
                sub0 = [u for u in universes if u[0][m_idx] == 0]
                if sub0 and all(tname in u[1] for u in sub0):
                    hint = f" 👉 [💡AI: '{t1}' 승리 시 진출 확정]"
                    break
                sub1 = [u for u in universes if u[0][m_idx] == 1]
                if sub1 and all(tname in u[1] for u in sub1):
                    hint = f" 👉 [💡AI: '{t2}' 승리 시 진출 확정]"
                    break
            if hint: break

        return base_text + hint

    # ----------------------------------------------------
    # 🎯 데이터 매핑 및 최종 표출
    # ----------------------------------------------------
    status_list, prob_list = [], []
    for _, row in raw_df.iterrows():
        tname = row["팀명"]
        if tname not in alive_teams:
            if base_stats_dict[tname] >= 25:
                status_list.append("🏆 100% 진출 확정 (시즌 아웃에도 누적 포인트로 진출)")
                prob_list.append("100.0%")
            else:
                status_list.append("❌ 탈락 확정 (시즌 아웃 및 포인트 미달)")
                prob_list.append("0.0%")
            continue
        
        prob = (qual_counts[tname] / total_valid) * 100 if total_valid > 0 else 0
        cond_text = get_dynamic_condition(tname, prob, valid_universes)
        
        status_list.append(cond_text)
        prob_list.append(f"{prob:.1f}%")

    raw_df["경우의 수 및 진출 상태"] = status_list
    raw_df["진출 확률 (%)"] = prob_list

    display_cols = ["팀명", "Total Points", "진출 확률 (%)", "경우의 수 및 진출 상태", "Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]

    def highlight_rows(row):
        status = str(row["경우의 수 및 진출 상태"])
        if "100% 진출 확정" in status:
            return ["background-color: #fff3cc; color: #000000; font-weight: bold;"] * len(row)
        elif "탈락 확정" in status:
            return ["background-color: #f0f0f0; color: #888888;"] * len(row)
        elif "💡AI" in status:
            return ["background-color: #e6f7ff; color: #000000;"] * len(row)
        elif "🔥" in status:
            return ["background-color: #ffe5d0; color: #000000;"] * len(row)
        elif "⚡" in status:
            return ["background-color: #ffcccc; color: #000000;"] * len(row)
        return [""] * len(row)

    final_df = raw_df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)
    final_df.index = final_df.index + 1
    final_df.index.name = "현재 순위"

    st.dataframe(final_df[display_cols].style.apply(highlight_rows, axis=1), use_container_width=True)

    st.markdown("---")

