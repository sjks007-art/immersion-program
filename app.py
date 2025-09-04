# app.py - 직장인 몰입 체험 프로그램 (완전 수정판)
import streamlit as st
import time
from datetime import datetime
import json
from pathlib import Path
import random

# 페이지 설정
st.set_page_config(
    page_title="몰입 체험 프로그램",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# CSS 스타일
st.markdown("""
<style>
    /* Streamlit 기본 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    
    /* 페이지 높이 고정 */
    .main > div {
        max-height: 100vh;
        overflow-y: auto;
    }
    
    /* 진행 단계 표시 */
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    .step-item {
        flex: 1;
        text-align: center;
        padding: 1rem;
        margin: 0 0.5rem;
        border-radius: 10px;
    }
    .step-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .step-completed {
        background: #4CAF50;
        color: white;
    }
    .step-pending {
        background: #e0e0e0;
        color: #999;
    }
    
    /* 타이머 */
    .timer-display {
        font-size: 5rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin: 2rem 0;
        font-family: 'Courier New', monospace;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
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
    .level-beginner { 
        background: linear-gradient(135deg, #4CAF50, #8BC34A); 
        color: white; 
    }
    .level-intermediate { 
        background: linear-gradient(135deg, #FF9800, #FFB74D); 
        color: white; 
    }
    .level-advanced { 
        background: linear-gradient(135deg, #9C27B0, #BA68C8); 
        color: white; 
    }
    
    /* 라디오 버튼 스타일 개선 */
    .stRadio > div {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    /* Spinner 숨기기 */
    .stSpinner > div {
        display: none !important;
    }
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
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ''
if 'breathing_done' not in st.session_state:
    st.session_state.breathing_done = False
if 'selected_quote' not in st.session_state:
    st.session_state.selected_quote = None

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

# 레벨별 주제
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
    
    # 라디오 버튼으로 변경 (더 안정적)
    menu_options = ["🏠 홈", "🎯 몰입 시작", "📊 나의 통계", "📝 보고서", "ℹ️ 도움말"]
    selected_menu = st.radio(
        "페이지 선택",
        menu_options,
        key="menu_radio",
        label_visibility="collapsed"
    )
    
    # 선택된 메뉴에 따라 페이지 설정
    if "홈" in selected_menu:
        st.session_state.page = "home"
    elif "몰입 시작" in selected_menu:
        st.session_state.page = "immersion"
        if st.session_state.user_name and st.session_state.immersion_step == 0:
            st.session_state.immersion_step = 1
    elif "통계" in selected_menu:
        st.session_state.page = "stats"
    elif "보고서" in selected_menu:
        st.session_state.page = "report"
    elif "도움말" in selected_menu:
        st.session_state.page = "help"
    
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
    
    # 오늘의 지혜 - 고정된 명언 표시
    if not st.session_state.selected_quote:
        st.session_state.selected_quote = random.choice(QUOTES)
    
    st.info(f"💡 **오늘의 지혜**\n\n_{st.session_state.selected_quote}_\n\n- 황농문")

# 메인 콘텐츠
if st.session_state.page == "home":
    st.markdown("## 🏠 환영합니다!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📖 프로그램 소개
        
        이 프로그램은 **황농문 교수님의 몰입 이론**을 바탕으로
        직장인들이 일상에서 쉽게 몰입을 체험할 수 있도록 설계되었습니다.
        
        #### ✨ 핵심 기능
        - 🧘 **의식적 이완** - 4-8 호흡법
        - 💭 **슬로싱킹 훈련** - 천천히 오래 생각하기
        - ⏱️ **실시간 타이머** - 자동 측정
        - 📈 **레벨 시스템** - 성장 가시화
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 몰입의 3단계
        
        **1️⃣ 준비 단계** (선택)
        - 가벼운 스트레칭
        - 물 한 모금
        
        **2️⃣ 이완 단계** 
        - 호흡 명상으로 마음 안정
        
        **3️⃣ 몰입 단계**
        - 주제에 깊이 집중
        
        > **"몰입은 긴장이 아니라 이완입니다"**
        """)
    
    if not st.session_state.user_name:
        st.markdown("---")
        st.markdown("### 🚀 시작하기")
        name = st.text_input("이름을 입력하세요", placeholder="예: 홍길동")
        if st.button("프로그램 시작", type="primary", use_container_width=True):
            if name:
                st.session_state.user_name = name
                user_data[name] = {"created_at": datetime.now().isoformat()}
                save_user_data(user_data)
                st.session_state.page = "immersion"
                st.session_state.immersion_step = 1

elif st.session_state.page == "immersion":
    if not st.session_state.user_name:
        st.warning("먼저 홈에서 이름을 입력해주세요.")
        if st.button("홈으로 가기"):
            st.session_state.page = "home"
    else:
        st.markdown("## 🎯 몰입 훈련")
        
        user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
        level, emoji, level_num = get_user_level(len(user_sessions))
        
        st.markdown(f"<div class='level-badge level-{'beginner' if level_num==1 else 'intermediate' if level_num==2 else 'advanced'}'>{emoji} {st.session_state.user_name}님 - {level} 레벨</div>", unsafe_allow_html=True)
        
        # 진행 단계 표시
        st.markdown("""
        <div class='step-container'>
            <div class='step-item {}'>1️⃣ 준비</div>
            <div class='step-item {}'>2️⃣ 이완</div>
            <div class='step-item {}'>3️⃣ 몰입</div>
        </div>
        """.format(
            'step-completed' if st.session_state.immersion_step > 1 else 'step-active' if st.session_state.immersion_step == 1 else 'step-pending',
            'step-completed' if st.session_state.immersion_step > 2 else 'step-active' if st.session_state.immersion_step == 2 else 'step-pending',
            'step-active' if st.session_state.immersion_step == 3 else 'step-pending'
        ), unsafe_allow_html=True)
        
        # 단계별 내용
        if st.session_state.immersion_step == 1:
            st.markdown("### 1️⃣ 몰입 준비")
            st.success("💡 준비 항목은 모두 선택사항입니다. 체크 없이도 다음 단계로 진행 가능합니다!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**가벼운 준비** (권장)")
                exercise = st.checkbox("🤸 움직임 (스트레칭, 목 돌리기 등)", key="check_exercise")
                water = st.checkbox("💧 수분 (물 한 모금)", key="check_water")
            
            with col2:
                st.markdown("**환경** (선택)")
                phone = st.checkbox("📱 방해 금지 모드", key="check_phone")
                comfort = st.checkbox("🪑 편안한 자세", key="check_comfort")
            
            checked_count = sum([exercise, water, phone, comfort])
            
            st.markdown("---")
            
            if checked_count == 0:
                st.info("바로 시작하셔도 좋습니다! 준비는 선택입니다.")
            elif checked_count <= 2:
                st.info(f"가벼운 준비 완료! ({checked_count}개 선택)")
            else:
                st.success(f"철저한 준비! ({checked_count}개 선택)")
            
            if st.button("다음 단계로 →", type="primary", use_container_width=True):
                st.session_state.immersion_step = 2
        
        elif st.session_state.immersion_step == 2:
            st.markdown("### 2️⃣ 의식적 이완")
            st.info("황농문 교수님: '이완된 집중'이 진정한 몰입의 시작입니다")
            
            if level_num == 1:
                inhale, exhale, rounds = 3, 6, 2
                st.markdown("🌱 **초급 설정**: 3-6 호흡, 2회 반복")
            elif level_num == 2:
                inhale, exhale, rounds = 4, 8, 3
                st.markdown("🌿 **중급 설정**: 4-8 호흡, 3회 반복")
            else:
                inhale, exhale, rounds = 5, 10, 3
                st.markdown("🌳 **고급 설정**: 5-10 호흡, 3회 반복")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🧘 호흡 명상 시작", type="primary", use_container_width=True):
                    # 컨테이너 생성으로 레이아웃 고정
                    breath_container = st.container()
                    with breath_container:
                        placeholder = st.empty()
                        progress_bar = st.progress(0)
                        
                        total_steps = rounds * (inhale + exhale)
                        current_step = 0
                        
                        for round in range(rounds):
                            for i in range(inhale):
                                current_step += 1
                                progress_bar.progress(current_step / total_steps)
                                
                                placeholder.markdown(f"""
                                <div style='text-align: center; height: 300px; padding: 2rem; background: #f0f8ff; border-radius: 20px; margin: 1rem 0;'>
                                    <div style='font-size: 6rem; margin: 2rem 0;'>🫁</div>
                                    <h2 style='color: #1976D2;'>숨을 들이마시세요</h2>
                                    <h3 style='color: #666;'>라운드 {round+1}/{rounds} | {i+1}/{inhale}초</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                time.sleep(1)
                            
                            for i in range(exhale):
                                current_step += 1
                                progress_bar.progress(current_step / total_steps)
                                
                                placeholder.markdown(f"""
                                <div style='text-align: center; height: 300px; padding: 2rem; background: #fff0f5; border-radius: 20px; margin: 1rem 0;'>
                                    <div style='font-size: 6rem; margin: 2rem 0;'>😮‍💨</div>
                                    <h2 style='color: #FF69B4;'>천천히 내쉬세요</h2>
                                    <h3 style='color: #666;'>라운드 {round+1}/{rounds} | {i+1}/{exhale}초</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                time.sleep(1)
                        
                        placeholder.empty()
                        progress_bar.empty()
                        st.success("✅ 의식적 이완 완료!")
                        time.sleep(1)
                        st.session_state.immersion_step = 3
            
            with col2:
                if st.button("건너뛰기 →", type="secondary", use_container_width=True):
                    st.session_state.immersion_step = 3
        
        elif st.session_state.immersion_step == 3:
            st.markdown("### 3️⃣ 슬로싱킹 - 천천히 오래 생각하기")
            
            if not st.session_state.immersion_active:
                st.info("이제 본격적인 몰입을 시작합니다")
                
                topics = TOPICS[level]
                selected_topic = st.selectbox(
                    "오늘의 몰입 주제",
                    topics + ["직접 입력"],
                    help="레벨에 맞는 주제가 자동으로 제공됩니다"
                )
                
                if selected_topic == "직접 입력":
                    selected_topic = st.text_input("주제를 입력하세요")
                
                if st.button("🚀 몰입 시작", type="primary", use_container_width=True):
                    if selected_topic and selected_topic != "직접 입력":
                        st.session_state.immersion_active = True
                        st.session_state.start_time = time.time()
                        st.session_state.current_topic = selected_topic
                        st.session_state.thoughts = []
            
            else:
                elapsed = time.time() - st.session_state.start_time
                
                # 타이머 표시
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"<div class='timer-display'>{format_time(elapsed)}</div>", unsafe_allow_html=True)
                
                st.markdown(f"#### 📝 주제: {st.session_state.current_topic}")
                
                thought = st.text_area(
                    "💭 떠오르는 생각을 자유롭게 기록하세요",
                    height=150,
                    placeholder="생각을 입력하고 '기록' 버튼을 누르세요...",
                    key="thought_input"
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💾 생각 기록", use_container_width=True, key=f"save_{len(st.session_state.thoughts)}"):
                        if thought:
                            st.session_state.thoughts.append({
                                "time": format_time(time.time() - st.session_state.start_time),
                                "content": thought
                            })
                            st.success("✅ 기록 완료!", icon="✅")
                
                with col2:
                    if st.button("⏱️ 타이머 새로고침", use_container_width=True, key="refresh"):
                        st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
                
                with col3:
                    if st.button("🏁 몰입 종료", type="secondary", use_container_width=True, key="end"):
                        final_duration = time.time() - st.session_state.start_time
                        session_data = {
                            "user": st.session_state.user_name,
                            "date": datetime.now().isoformat(),
                            "topic": st.session_state.current_topic,
                            "duration": final_duration,
                            "thoughts": st.session_state.thoughts
                        }
                        save_session(session_data)
                        
                        st.session_state.immersion_active = False
                        st.session_state.immersion_step = 0
                        
                        st.success(f"🎉 몰입 완료! {format_time(final_duration)}")
                        st.balloons()
                        
                        # 보고서 페이지로 이동 버튼 표시
                        if st.button("📝 보고서 보기", type="primary", use_container_width=True):
                            st.session_state.page = "report"
                            st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
                
                if st.session_state.thoughts:
                    st.markdown("---")
                    st.markdown("#### 💭 기록된 생각들")
                    for i, t in enumerate(st.session_state.thoughts, 1):
                        st.markdown(f"**{i}.** [{t['time']}] {t['content']}")
                
                with st.expander("💡 몰입 도움말"):
                    st.markdown("""
                    - **타이머 업데이트**: 버튼을 눌러 시간을 확인하세요
                    - **생각 기록**: 떠오르는 생각을 자유롭게 적어주세요
                    - **몰입 종료**: 언제든 종료할 수 있으며, 자동으로 보고서가 생성됩니다
                    """)

elif st.session_state.page == "stats":
    st.markdown("## 📊 나의 몰입 통계")
    
    user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
    
    if not user_sessions:
        st.info("아직 몰입 기록이 없습니다. 첫 몰입을 시작해보세요!")
    else:
        total_sessions = len(user_sessions)
        total_time = sum(s.get('duration', 0) for s in user_sessions)
        avg_time = total_time / total_sessions if total_sessions > 0 else 0
        
        level, emoji, level_num = get_user_level(total_sessions)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("레벨", f"{emoji} {level}")
        with col2:
            st.metric("총 몰입", f"{total_sessions}회")
        with col3:
            st.metric("총 시간", format_time(total_time))
        with col4:
            st.metric("평균 시간", format_time(avg_time))
        
        st.markdown("### 📈 레벨 진행률")
        if level_num == 1:
            progress = (total_sessions / 5) * 100
            st.progress(min(progress / 100, 1.0))
            st.info(f"🌱 중급까지 {max(0, 5 - total_sessions)}회 남았습니다!")
        elif level_num == 2:
            progress = ((total_sessions - 5) / 15) * 100
            st.progress(min(progress / 100, 1.0))
            st.info(f"🌿 고급까지 {max(0, 20 - total_sessions)}회 남았습니다!")
        else:
            st.success("🌳 최고 레벨 달성! 몰입 마스터입니다!")
        
        st.markdown("### 📝 최근 몰입 기록")
        recent_sessions = sorted(user_sessions, key=lambda x: x['date'], reverse=True)[:5]
        
        for session in recent_sessions:
            date = datetime.fromisoformat(session['date']).strftime('%Y-%m-%d %H:%M')
            duration = format_time(session.get('duration', 0))
            topic = session.get('topic', '주제 없음')
            
            with st.expander(f"📅 {date} | ⏱️ {duration}"):
                st.markdown(f"**주제:** {topic}")
                thoughts = session.get('thoughts', [])
                if thoughts:
                    st.markdown("**기록된 생각들:**")
                    for t in thoughts:
                        st.markdown(f"- [{t['time']}] {t['content']}")

elif st.session_state.page == "report":
    st.markdown("## 📝 몰입 실천 보고서")
    
    user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
    
    if not user_sessions:
        st.warning("아직 몰입 기록이 없습니다.")
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        today_sessions = [s for s in user_sessions if s.get('date', '').startswith(today)]
        
        if today_sessions:
            level, emoji, _ = get_user_level(len(user_sessions))
            total_time_today = sum(s.get('duration', 0) for s in today_sessions)
            
            report = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 몰입 실천 보고서

📅 작성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}
👤 작성자: {st.session_state.user_name}
{emoji} 레벨: {level}

【오늘의 몰입】
• 몰입 횟수: {len(today_sessions)}회
• 총 몰입 시간: {format_time(total_time_today)}
• 누적 몰입: {len(user_sessions)}회

【세부 내용】"""
            
            for i, session in enumerate(today_sessions, 1):
                topic = session.get('topic', '')
                duration = format_time(session.get('duration', 0))
                thoughts = session.get('thoughts', [])
                
                report += f"\n\n{i}. 주제: {topic}\n   시간: {duration}"
                
                if thoughts:
                    report += "\n   기록:"
                    for t in thoughts:
                        report += f"\n   - [{t['time']}] {t['content']}"
            
            report += f"""

【오늘의 성장】
황농문 교수님의 '1초 원칙'을 실천하며
의식의 조명을 한 곳에 집중하는 훈련을 계속했습니다.

{st.session_state.user_name} 올림
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
            
            st.text_area("보고서 내용", report, height=400, key="report_text")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    "📥 보고서 다운로드",
                    report,
                    file_name=f"몰입보고서_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🎯 새 몰입 시작", type="primary", use_container_width=True):
                    st.session_state.page = "immersion"
                    st.session_state.immersion_step = 1
        else:
            st.info("오늘의 몰입 기록이 없습니다.")
            if st.button("🎯 몰입 시작하기", type="primary", use_container_width=True):
                st.session_state.page = "immersion"
                st.session_state.immersion_step = 1
                st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()

elif st.session_state.page == "help":
    st.markdown("""
    ## ℹ️ 사용 가이드
    
    ### 🎯 프로그램 특징
    
    **깜빡임 없는 안정적인 UI**
    - 자동 새로고침 완전 제거
    - 타이머는 수동 업데이트 버튼으로 확인
    - 모든 내용이 안정적으로 표시됨
    
    ### 📱 사용 방법
    
    **1. 몰입 시작**
    - 이름 입력 후 시작
    - 3단계 자동 진행
    - 준비 단계는 모두 선택사항
    
    **2. 타이머 사용**
    - "타이머 업데이트" 버튼으로 시간 확인
    - 생각 기록 후 자동 저장
    - 몰입 종료 시 보고서 자동 생성
    
    **3. 레벨 시스템**
    - 🌱 초급: 0-4회
    - 🌿 중급: 5-19회
    - 🌳 고급: 20회 이상
    
    ### 💾 데이터 저장
    
    - 모든 몰입 기록은 자동 저장됩니다
    - 브라우저를 닫아도 기록이 유지됩니다
    - 보고서 다운로드 기능 제공
    
    ### 🔧 문제 해결
    
    **메뉴가 작동하지 않을 때:**
    - 브라우저 새로고침 (F5 또는 Ctrl+R)
    - 다른 브라우저로 접속
    - 모바일에서도 사용 가능
    
    **타이머가 업데이트되지 않을 때:**
    - "타이머 업데이트" 버튼 클릭
    - 수동 업데이트 방식으로 안정성 확보
    
    ### 📧 황농문 교수님께 공유
    
    **URL 공유:**
    ```
    https://immersion-program.streamlit.app
    ```
    
    별도 설치 없이 위 링크로 바로 체험 가능합니다.
    
    ### 💡 몰입의 핵심
    
    > "몰입은 긴장이 아니라 이완입니다"
    > 
    > "천천히 오래 생각하는 슬로싱킹을 실천하세요"
    > 
    > - 황농문 교수님
    """)

# 푸터
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2025 직장인 몰입 체험 프로그램 | 황농문 교수님의 몰입 철학 기반 | Made with ❤️ by 한승희</div>", unsafe_allow_html=True)
