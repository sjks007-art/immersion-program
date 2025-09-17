# app.py - 직장인 몰입 체험 프로그램 v4.0 (최종 완성판)
# 황농문 교수님 몰입 이론 기반
# 개발자: 갯버들 (구 한승희)
# GitHub: sjks007-art/immersion-program

import streamlit as st
import time
from datetime import datetime, timedelta
import json
from pathlib import Path
import random

# 페이지 설정
st.set_page_config(
    page_title="직장인 몰입 체험 프로그램",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 자동 새로고침 비활성화
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# 데이터 저장 경로
DATA_DIR = Path("immersion_data")
DATA_DIR.mkdir(exist_ok=True)
USER_DATA_FILE = DATA_DIR / "user_data.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"

# 데이터 관리 함수
def load_user_data():
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_sessions():
    if SESSIONS_FILE.exists():
        with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_session(session_data):
    sessions = load_sessions()
    sessions.append(session_data)
    with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)
    return sessions

# CSS 스타일 (깜빡임 제거, 안정적 UI)
st.markdown("""
<style>
    /* 기본 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    
    /* 의식의 무대 스타일 */
    .stage-container {
        background: linear-gradient(180deg, #1a1a2e, #0f0f1e);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .spotlight {
        background: radial-gradient(circle, rgba(255,255,255,0.8), transparent);
        width: 200px;
        height: 200px;
        margin: 0 auto;
        border-radius: 50%;
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* 호흡 가이드 */
    .breathing-circle {
        width: 150px;
        height: 150px;
        border: 3px solid #4CAF50;
        border-radius: 50%;
        margin: 20px auto;
        animation: breathe 12s ease-in-out infinite;
    }
    
    @keyframes breathe {
        0%, 100% { transform: scale(1); }
        33% { transform: scale(1.3); }
        66% { transform: scale(1); }
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* 레벨 배지 */
    .level-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem;
        font-size: 1.1rem;
    }
    .level-beginner { background: linear-gradient(135deg, #4CAF50, #8BC34A); color: white; }
    .level-intermediate { background: linear-gradient(135deg, #FF9800, #FFB74D); color: white; }
    .level-advanced { background: linear-gradient(135deg, #9C27B0, #BA68C8); color: white; }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'immersion_step' not in st.session_state:
    st.session_state.immersion_step = 0
if 'immersion_active' not in st.session_state:
    st.session_state.immersion_active = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'thoughts' not in st.session_state:
    st.session_state.thoughts = []
if 'insights' not in st.session_state:
    st.session_state.insights = []
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ''
if 'breathing_done' not in st.session_state:
    st.session_state.breathing_done = False
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = 10

# 황농문 교수님 인용구
QUOTES = [
    "몰입은 긴장이 아니라 이완입니다.",
    "1초 원칙: 의식의 조명을 단 1초도 다른 곳에 비추지 마세요.",
    "천천히 오래 생각하는 것이 빨리 생각하는 것보다 중요합니다.",
    "뇌의 안전한 놀이터를 만드세요.",
    "슬로싱킹은 느리게 생각하는 것이 아니라, 오래 생각하는 것입니다.",
    "문제를 해결하려 하지 말고, 문제와 함께 머물러보세요.",
    "의식적 이완이 진정한 몰입의 시작입니다.",
    "포기하지 않고 계속 생각하면 반드시 답이 나옵니다.",
    "몰입의 즐거움을 아는 사람은 인생이 행복합니다."
]

# 레벨별 주제 (슬로싱킹 중심)
TOPICS = {
    "초급": [
        "오늘 하루 감사한 것 3가지는 무엇인가요?",
        "나의 가장 큰 장점은 무엇일까요?",
        "오늘 가장 행복했던 순간은 언제였나요?",
        "내가 정말 좋아하는 일은 무엇인가요?"
    ],
    "중급": [
        "지난 1년간 나를 가장 성장시킨 경험은?",
        "나에게 성공이란 무엇을 의미하는가?",
        "실패에서 배운 가장 중요한 교훈은?",
        "내 일이 세상에 주는 가치는 무엇인가?"
    ],
    "고급": [
        "5년 후 내가 되고 싶은 모습과 그를 위한 현재의 노력은?",
        "인생에서 가장 중요한 결정을 내리는 나만의 기준은?",
        "내가 세상에 남기고 싶은 유산은 무엇인가?",
        "진정한 행복의 조건은 무엇이라고 생각하는가?"
    ]
}

def get_user_level(session_count):
    if session_count < 5:
        return "초급", "🌱", 1
    elif session_count < 20:
        return "중급", "🌿", 2
    else:
        return "고급", "🌳", 3

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# 데이터 로드
user_data = load_user_data()
sessions = load_sessions()

# 헤더
st.markdown("<h1 style='text-align: center;'>🎯 직장인 몰입 체험 프로그램</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>황농문 교수님의 몰입 철학 기반</p>", unsafe_allow_html=True)
st.markdown("---")

# 사이드바
with st.sidebar:
    st.markdown("### 📌 메뉴")
    
    if st.button("🏠 홈", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
    
    if st.button("🎯 몰입 시작", use_container_width=True):
        st.session_state.page = 'immersion'
        st.session_state.immersion_step = 1
        st.rerun()
    
    if st.button("📊 나의 통계", use_container_width=True):
        st.session_state.page = 'stats'
        st.rerun()
    
    if st.button("📝 보고서", use_container_width=True):
        st.session_state.page = 'report'
        st.rerun()
    
    st.markdown("---")
    
    # 사용자 정보
    if st.session_state.user_name:
        user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
        level, emoji, _ = get_user_level(len(user_sessions))
        
        st.markdown(f"### {emoji} {st.session_state.user_name}")
        st.markdown(f"**레벨:** {level}")
        st.markdown(f"**총 몰입:** {len(user_sessions)}회")
        
        total_time = sum(s.get('duration', 0) for s in user_sessions)
        st.markdown(f"**누적 시간:** {format_time(total_time)}")
    
    st.markdown("---")
    
    # 오늘의 지혜
    st.info(f"💡 **오늘의 지혜**\n\n_{random.choice(QUOTES)}_\n\n- 황농문")

# 메인 콘텐츠
if st.session_state.page == "home":
    st.markdown("## 🏠 환영합니다!")
    
    st.markdown("""
    ### 📖 프로그램 소개
    이 프로그램은 황농문 교수님의 **'슬로싱킹'** 철학을 바탕으로 
    직장인들이 일상에서 몰입을 실천할 수 있도록 돕습니다.
    
    #### 핵심 기능:
    1. **🎭 의식의 무대** - 주제에 조명을 비추어 몰입
    2. **🧘 4-8 호흡법** - 이완된 집중 상태 유도
    3. **📝 잡념/통찰 분리** - 생각 정리와 아이디어 기록
    4. **⏰ 다양한 시간 설정** - 5분부터 60분까지
    5. **📊 자동 보고서** - 몰입 세션 자동 기록
    
    #### 몰입의 3단계:
    1. **준비** - 몸과 마음의 준비
    2. **이완** - 의식적 이완을 통한 최적화
    3. **슬로싱킹** - 천천히 오래 생각하기
    
    > **"몰입은 긴장이 아니라 이완입니다"** - 황농문
    """)
    
    # 시작하기
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("🏷️ 이름을 입력하세요", placeholder="예: 갯버들")
        if st.button("🚀 프로그램 시작", type="primary", use_container_width=True):
            if name:
                st.session_state.user_name = name
                st.session_state.page = "immersion"
                st.session_state.immersion_step = 1
                st.rerun()
            else:
                st.error("이름을 입력해주세요!")

elif st.session_state.page == "immersion":
    if not st.session_state.user_name:
        st.warning("먼저 홈에서 이름을 입력해주세요!")
        if st.button("홈으로 가기"):
            st.session_state.page = "home"
            st.rerun()
    else:
        user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
        level, emoji, level_num = get_user_level(len(user_sessions))
        
        st.markdown(f"### {st.session_state.user_name}님, {level} 레벨")
        
        # Step 1: 준비 단계
        if st.session_state.immersion_step == 1:
            st.markdown("## 🎯 1단계: 준비")
            st.info("몸과 마음을 준비합니다. 모든 항목은 선택사항입니다.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("🏃 30분 이상 운동 완료")
                st.checkbox("💧 충분한 수분 섭취")
                st.checkbox("🔇 핸드폰 무음 설정")
            with col2:
                st.checkbox("🪑 편안한 자세")
                st.checkbox("🚫 방해요소 제거")
                st.checkbox("🧘 마음 비우기")
            
            if st.button("다음 단계로 →", type="primary"):
                st.session_state.immersion_step = 2
                st.rerun()
        
        # Step 2: 이완 단계 (4-8 호흡)
        elif st.session_state.immersion_step == 2:
            st.markdown("## 🧘 2단계: 의식적 이완")
            st.info("이완된 집중이 진정한 몰입입니다")
            
            st.markdown("""
            ### 4-8 호흡법
            1. 4초간 천천히 숨을 들이마십니다
            2. 8초간 천천히 숨을 내쉽니다
            3. 3-5회 반복합니다
            """)
            
            # 호흡 가이드 애니메이션
            st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🧘 호흡 시작", type="primary"):
                    with st.spinner("4초 들숨... 8초 날숨..."):
                        time.sleep(12)  # 1회 호흡
                    st.success("호흡 완료!")
                    st.session_state.breathing_done = True
            
            with col2:
                if st.button("건너뛰기 →"):
                    st.session_state.immersion_step = 3
                    st.rerun()
            
            if st.session_state.breathing_done:
                if st.button("몰입 시작 →", type="primary"):
                    st.session_state.immersion_step = 3
                    st.rerun()
        
        # Step 3: 몰입 단계
        elif st.session_state.immersion_step == 3:
            st.markdown("## 🎭 3단계: 의식의 무대")
            
            # 주제 선택
            col1, col2 = st.columns([3, 1])
            with col1:
                topic_type = st.radio(
                    "주제 선택",
                    ["직접 입력", f"{level} 추천 주제"],
                    horizontal=True
                )
            
            if topic_type == "직접 입력":
                st.session_state.current_topic = st.text_input(
                    "오늘 몰입할 주제를 입력하세요:",
                    placeholder="예: 나에게 가장 중요한 가치는 무엇인가?"
                )
            else:
                topics = TOPICS[level][:3]
                st.session_state.current_topic = st.selectbox(
                    "추천 주제를 선택하세요:",
                    topics
                )
            
            # 시간 선택
            time_options = {
                "5분 (시작하기)": 5,
                "10분 (기본)": 10,
                "15분 (집중)": 15,
                "25분 (뽀모도로)": 25,
                "45분 (심화)": 45,
                "60분 (마스터)": 60
            }
            
            selected = st.selectbox("몰입 시간을 선택하세요:", list(time_options.keys()), index=1)
            st.session_state.selected_time = time_options[selected]
            
            # 몰입 시작
            if st.button("🎯 몰입 시작", type="primary", use_container_width=True):
                if st.session_state.current_topic:
                    st.session_state.immersion_active = True
                    st.session_state.start_time = time.time()
                    st.session_state.immersion_step = 4
                    st.rerun()
                else:
                    st.error("주제를 입력해주세요!")
        
        # Step 4: 몰입 진행
        elif st.session_state.immersion_step == 4:
            st.markdown('<div class="stage-container">', unsafe_allow_html=True)
            st.markdown("## 🎭 의식의 무대")
            
            # 스포트라이트 효과
            st.markdown('<div class="spotlight"></div>', unsafe_allow_html=True)
            
            # 주제 표시
            st.markdown(f"### 📍 주제: {st.session_state.current_topic}")
            
            # 타이머
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                elapsed = time.time() - st.session_state.start_time if st.session_state.start_time else 0
                remaining = max(0, st.session_state.selected_time * 60 - elapsed)
                
                st.markdown(f"### ⏰ 남은 시간: {format_time(remaining)}")
                
                # 수동 업데이트 버튼
                if st.button("⏱️ 타이머 업데이트"):
                    st.rerun()
                
                progress = min(1.0, elapsed / (st.session_state.selected_time * 60))
                st.progress(progress)
            
            st.markdown("---")
            
            # 메모 영역
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🌊 잡념 (관객석으로)")
                thought = st.text_area(
                    "떠오르는 잡념을 적고 놓아주세요",
                    height=150,
                    key="thought_input"
                )
                if st.button("💭 잡념 보내기"):
                    if thought and thought not in st.session_state.thoughts:
                        st.session_state.thoughts.append(thought)
                        st.success("잡념을 관객석으로 보냈습니다")
                        st.rerun()
            
            with col2:
                st.markdown("### 💡 통찰 (무대 위로)")
                insight = st.text_area(
                    "떠오른 통찰을 기록하세요",
                    height=150,
                    key="insight_input"
                )
                if st.button("✨ 통찰 기록"):
                    if insight and insight not in st.session_state.insights:
                        st.session_state.insights.append(insight)
                        st.success("통찰을 무대에 올렸습니다")
                        st.rerun()
            
            # 몰입 종료
            if st.button("🏁 몰입 종료", type="secondary", use_container_width=True):
                st.session_state.immersion_step = 5
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 5: 완료 및 보고서
        elif st.session_state.immersion_step == 5:
            duration = time.time() - st.session_state.start_time if st.session_state.start_time else 0
            
            # 세션 저장
            session_data = {
                "user": st.session_state.user_name,
                "date": datetime.now().isoformat(),
                "topic": st.session_state.current_topic,
                "duration": duration,
                "thoughts": st.session_state.thoughts,
                "insights": st.session_state.insights,
                "level": level
            }
            save_session(session_data)
            
            st.balloons()
            st.success("🎉 몰입 완료!")
            
            # 보고서
            st.markdown("## 📊 몰입 보고서")
            st.markdown(f"**날짜:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            st.markdown(f"**주제:** {st.session_state.current_topic}")
            st.markdown(f"**몰입 시간:** {format_time(duration)}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**잡념 개수:** {len(st.session_state.thoughts)}개")
                if st.session_state.thoughts:
                    for i, t in enumerate(st.session_state.thoughts, 1):
                        st.write(f"{i}. {t}")
            
            with col2:
                st.markdown(f"**통찰 개수:** {len(st.session_state.insights)}개")
                if st.session_state.insights:
                    for i, insight in enumerate(st.session_state.insights, 1):
                        st.write(f"{i}. {insight}")
            
            # 16시간 법칙 알림
            if duration >= 60:
                st.info("💫 16시간 법칙: 오늘 몰입한 내용이 잠재의식에서 계속 처리됩니다!")
            
            # 초기화
            if st.button("🔄 새로운 몰입 시작", type="primary"):
                st.session_state.immersion_step = 1
                st.session_state.thoughts = []
                st.session_state.insights = []
                st.session_state.current_topic = ''
                st.session_state.breathing_done = False
                st.session_state.start_time = None
                st.rerun()

elif st.session_state.page == "stats":
    st.markdown("## 📊 나의 몰입 통계")
    
    if st.session_state.user_name:
        user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
        
        if user_sessions:
            total_sessions = len(user_sessions)
            total_time = sum(s.get('duration', 0) for s in user_sessions)
            avg_time = total_time / total_sessions if total_sessions > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 몰입 횟수", f"{total_sessions}회")
            with col2:
                st.metric("총 몰입 시간", format_time(total_time))
            with col3:
                st.metric("평균 몰입 시간", format_time(avg_time))
            
            # 최근 세션
            st.markdown("### 📝 최근 몰입 기록")
            for session in user_sessions[-5:]:
                with st.expander(f"{session['date'][:10]} - {session.get('topic', '제목 없음')}"):
                    st.write(f"몰입 시간: {format_time(session.get('duration', 0))}")
                    st.write(f"잡념: {len(session.get('thoughts', []))}개")
                    st.write(f"통찰: {len(session.get('insights', []))}개")
        else:
            st.info("아직 몰입 기록이 없습니다. 첫 몰입을 시작해보세요!")
    else:
        st.warning("먼저 로그인해주세요!")

elif st.session_state.page == "report":
    st.markdown("## 📝 종합 보고서")
    
    if st.session_state.user_name:
        user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
        
        if user_sessions:
            st.markdown(f"### {st.session_state.user_name}님의 몰입 여정")
            
            # 주요 통찰 모음
            all_insights = []
            for session in user_sessions:
                all_insights.extend(session.get('insights', []))
            
            if all_insights:
                st.markdown("#### 💎 주요 통찰 모음")
                for i, insight in enumerate(all_insights[-10:], 1):
                    st.write(f"{i}. {insight}")
            
            # 성장 그래프 (간단한 텍스트 버전)
            st.markdown("#### 📈 성장 추이")
            st.info(f"첫 몰입: {user_sessions[0]['date'][:10]}")
            st.info(f"최근 몰입: {user_sessions[-1]['date'][:10]}")
            st.success(f"총 {len(user_sessions)}회의 몰입으로 성장 중!")
        else:
            st.info("몰입 기록이 없습니다.")
    else:
        st.warning("먼저 로그인해주세요!")

# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 직장인 몰입 체험 프로그램 | "
    "황농문 교수님의 몰입 철학 기반 | "
    "Made with ❤️ by 갯버들"
    "</div>", 
    unsafe_allow_html=True
)
