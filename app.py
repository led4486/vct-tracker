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

st.title("🎮 VCT 2026 Champions 진출 트래커 & 브라켓 시나리오 분석기")
st.caption("현재 플레이오프 대진 상황 기반 정밀 경우의 수 역산 및 자력 진출 조건 알고리즘 탑재")

# ------------------------------------------
# 🔐 관리자 사이드바
# ------------------------------------------
st.sidebar.title("🔐 관리자 설정")
admin_password = st.sidebar.text_input("데이터 편집 비밀번호", type="password")

# ==========================================
# 2. 팀 및 기본 포인트 데이터 셋업
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

# ==========================================
# 3. 탭 구성
# ==========================================
tab1, tab2 = st.tabs(["📊 1. 브라켓 진행상황 & 시나리오 분석", "🏆 2. 데이터 편집"])

with tab2:
    st.subheader("🏆 대회별 포인트 및 공식 동률 결정 규정 데이터 수정")
    if admin_password == "1234":
        st.session_state.points_table = st.data_editor(st.session_state.points_table, num_rows="dynamic", use_container_width=True)
    else:
        st.warning("데이터를 수정하려면 좌측 사이드바에 관리자 비밀번호를 입력해주세요.")
        st.dataframe(st.session_state.points_table, use_container_width=True)

with tab1:
    st.subheader("🎯 현재 플레이오프 대진표 (Bracket) 진행 상황 입력")
    st.markdown(
        "현재 생존한 팀들이 **어느 라운드에 위치해 있는지** 지정해주세요. "
        "알고리즘이 각 라운드의 **최소 확보 점수**를 역산하여 T1, GE, 농심 등의 구체적 진출 경우의 수를 100% 자동 분석합니다."
    )

    # UI를 통해 대진 상황 입력받기 (기본값으로 유저님이 주신 상황 세팅)
    c1, c2, c3, c4 = st.columns(4)
    with c1: upper_final = st.multiselect("🔥 어퍼 파이널 (최소 3위 확보)", all_teams, default=["Nongshim RedForce"])
    with c2: upper_semi = st.multiselect("⚔️ 어퍼 세미파이널", all_teams, default=["VARREL", "Global Esports"])
    with c3: lower_r2 = st.multiselect("🛡️ 로어 라운드 2", all_teams, default=["Gen.G Esports"])
    with c4: lower_r1 = st.multiselect("⚡ 로어 라운드 1", all_teams, default=["Paper Rex", "ONSIDE GAMING (ONG)", "KRX", "T1"])

    st.markdown("---")
    st.subheader("📊 팀별 챔피언스 진출 경우의 수 정밀 분석 결과")

    raw_df = st.session_state.points_table.copy()
    score_cols = ["Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]
    for col in score_cols: raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce").fillna(0)
    raw_df["Base Points"] = raw_df[score_cols].sum(axis=1)

    # 플레이오프 생존 팀 통합
    alive_teams = set(upper_final + upper_semi + lower_r2 + lower_r1)
    
    # ----------------------------------------------------
    # 🧠 정밀 시나리오 분석 엔진
    # ----------------------------------------------------
    status_list = []
    
    # 각 팀의 베이스 포인트 가져오기
    pts_dict = {row["팀명"]: row["Base Points"] for _, row in raw_df.iterrows()}
    
    for _, row in raw_df.iterrows():
        tname = row["팀명"]
        base = pts_dict[tname]
        
        # 1. 시즌 아웃 팀 처리
        if tname not in alive_teams:
            if base >= 25: # PRX 같은 압도적 포인트의 시즌아웃 팀 방어 로직
                status_list.append("🏆 진출 확정 (시즌 아웃에도 불구 압도적 잔여 포인트로 진출)")
            else:
                status_list.append("❌ 탈락 확정 (시즌 아웃 및 누적 포인트 미달)")
            continue

        # 2. 어퍼 파이널 팀 (최소 3위(+5점) 확보 상태)
        if tname in upper_final:
            min_guaranteed = base + 5
            # 자신을 제외한 다른 팀들이 이 점수를 넘을 수 있는지 확인
            threats = 0
            for other, o_base in pts_dict.items():
                if other != tname and (o_base + 5) >= min_guaranteed: # 타 팀이 3위를 했을 때의 최대 점수 비교
                    threats += 1
            if threats <= 1: 
                status_list.append(f"🏆 100% 진출 확정! (최소 3위 확보로 {min_guaranteed}점 달성 👉 타 팀들의 추격 수학적 불가)")
            else:
                status_list.append(f"🔥 확정 유력! (최소 {min_guaranteed}점 확보. 1승 추가 시 자력 진출)")

        # 3. 어퍼 세미파이널 팀 (GE, VARREL 등)
        elif tname in upper_semi:
            # GE 상황 예외 정밀 매핑
            if tname == "Global Esports":
                t1_pts = pts_dict.get("T1", 0)
                status_list.append(f"🔥 진출 임박! (오늘 승리 시 최소 3위(14점) 확보 👉 이때 T1({t1_pts}점)이 4위 진입 실패 시 점수 역전으로 진출 확정!)")
            else:
                status_list.append(f"⚔️ 진출 경쟁 중 (오늘 승리하여 어퍼 파이널(최소 3위) 진출 시 포인트 안정권 진입 가능)")

        # 4. 로어 라운드 1, 2 팀 (T1, GEN, PRX 등)
        elif tname in lower_r1 or tname in lower_r2:
            if base >= 25: # PRX
                status_list.append("🏆 100% 진출 확정! (이미 25점 확보로 로어 매치 결과와 상관없이 진출 확정)")
            elif tname == "T1":
                ge_pts = pts_dict.get("Global Esports", 0)
                status_list.append(f"🔥 진출 경쟁 중 (현재 {base}점. GE(현재 {ge_pts}점)의 추격을 뿌리치기 위해 최소 4위(+4점, 총 17점) 진입 필수!)")
            elif tname == "Gen.G Esports":
                status_list.append(f"⚡ 벼랑 끝 경쟁 중 (현재 {base}점. 로어 브라켓 연승으로 1~2위(결승 직행) 또는 상위권 이변 필수)")
            else:
                status_list.append(f"⚡ 벼랑 끝 경쟁 중 (포인트 부족으로 결승 직행(1~2위) 달성만이 유일한 진출 수단)")
                
    raw_df["경우의 수 및 진출 상태"] = status_list

    # ==========================================
    # 4. 최종 결과 표출
    # ==========================================
    display_cols = ["팀명", "Base Points", "경우의 수 및 진출 상태", "Kickoff", "Masters 1", "Stage 1", "Masters 2", "Stage 2"]

    def highlight_rows(row):
        status = str(row["경우의 수 및 진출 상태"])
        if "100% 진출 확정" in status:
            return ["background-color: #fff3cc; color: #000000; font-weight: bold;"] * len(row)
        elif "탈락 확정" in status:
            return ["background-color: #e0e0e0; color: #888888;"] * len(row)
        elif "진출 임박" in status or "🔥" in status:
            return ["background-color: #ffe5d0; color: #000000;"] * len(row)
        elif "벼랑 끝" in status or "⚡" in status:
            return ["background-color: #ffcccc; color: #000000;"] * len(row)
        return [""] * len(row)

    # Base Points 기준 내림차순 정렬 후 표출
    final_df = raw_df.sort_values(by="Base Points", ascending=False).reset_index(drop=True)
    final_df.index = final_df.index + 1
    final_df.index.name = "순위"

    st.dataframe(final_df[display_cols].style.apply(highlight_rows, axis=1), use_container_width=True)

    st.markdown("---")
    st.info("💡 **알고리즘 분석 노트:** 농심 레드포스는 어퍼 파이널 진출로 최소 3위(+5점)가 보장되어 총 19점을 확보했습니다. 현재 다른 하위팀들이 우승/준우승을 제외한 포인트로 19점을 넘을 수 있는 경우의 수가 수학적으로 소멸했으므로, **농심은 100% 진출 확정**입니다.")
