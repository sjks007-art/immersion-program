# app.py - 직장인 몰입 체험 프로그램 v5.0 (최종 완성판)
# 황농문 교수님 몰입 이론 기반 - 1초 원칙 중심
# 개발자: 갯버들 (한승희)
# GitHub: sjks007-art/immersion-program
# 최종 완성: 2025년 9월 17일

import streamlit as st
import time
from datetime import datetime, timedelta
import json
from pathlib import Path
import random
import base64

try:
    import pytz
    KST = pytz.timezone('Asia/Seoul')
except ImportError:
    KST = None
    st.warning("pytz 라이브러리가 없습니다. UTC 시간을 사용합니다.")

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

def create_download_link(text, filename):
    """텍스트를 다운로드 가능한 링크로 변환"""
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">📥 보고서 다운로드</a>'

def get_korean_time():
    """한국 시간 반환"""
    if KST:
        return datetime.now(KST)
    else:
        return datetime.now() + timedelta(hours=9)  # UTC+9

def format_time(seconds):
    """시간을 MM:SS 형식으로 변환"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def get_user_level(session_count):
    """사용자 레벨 결정"""
    if session_count < 5:
        return "초급", "🌱", 1
    elif session_count < 20:
        return "중급", "🌿", 2
    else:
        return "고급", "🌳", 3

def get_personalized_feedback(duration, thoughts_count, insights_count):
    """개인화된 피드백 생성"""
    feedback = []
    
    # 1초 원칙 평가 - 개인화
    if duration < 300:  # 5분 미만
        feedback.append(f"[짧은 몰입도 의미있습니다]\n"
                       f"{format_time(duration)} 동안 주제에 집중하셨네요. "
                       f"처음 시작하기 좋은 시간입니다.")
    elif duration < 900:  # 15분 미만
        feedback.append(f"[집중력이 늘고 있습니다]\n"
                       f"{format_time(duration)} 동안 1초 원칙을 실천했습니다. "
                       f"일상에서 활용하기 좋은 몰입 시간입니다.")
    elif duration < 1800:  # 30분 미만
        feedback.append(f"[깊은 몰입 단계]\n"
                       f"{format_time(duration)} 동안 의식의 조명을 유지했습니다. "
                       f"프로 수준의 집중력입니다.")
    else:  # 30분 이상
        feedback.append(f"[몰입 마스터]\n"
                       f"{format_time(duration)} 동안 완전한 몰입을 경험했습니다. "
                       f"황농문 교수님의 '강한 몰입' 단계입니다.")
    
    # 잡념 처리 평가
    if thoughts_count == 0:
        feedback.append("[맑은 의식]\n잡념 없이 순수하게 집중했습니다.")
    elif thoughts_count <= 3:
        feedback.append(f"[잡념 관리 우수]\n{thoughts_count}개의 잡념을 잘 놓아주었습니다.")
    else:
        feedback.append(f"[적극적 정리]\n{thoughts_count}개의 잡념을 기록하고 놓아주었습니다. "
                       f"의식을 비우는 좋은 연습입니다.")
    
    # 통찰 평가
    if insights_count == 0:
        feedback.append("[고요한 관찰]\n조용히 주제를 품고 있었습니다.")
    elif insights_count <= 2:
        feedback.append(f"[통찰 발견]\n{insights_count}개의 귀한 깨달음을 얻었습니다.")
    else:
        feedback.append(f"[풍부한 통찰]\n{insights_count}개의 통찰이 떠올랐습니다. "
                       f"활발한 사고가 일어났네요.")
    
    # 16시간 법칙 - 시간대별 메시지
    current_hour = get_korean_time().hour
    if current_hour < 12:
        feedback.append("[16시간 법칙 - 오전]\n"
                       "오늘 저녁까지 잠재의식이 계속 처리합니다. "
                       "갑자기 답이 떠오를 수 있습니다.")
    elif current_hour < 18:
        feedback.append("[16시간 법칙 - 오후]\n"
                       "내일 아침 새로운 관점이 생길 수 있습니다. "
                       "잠들기 전 다시 한번 떠올려보세요.")
    else:
        feedback.append("[16시간 법칙 - 저녁]\n"
                       "오늘 밤 꿈에서, 내일 아침 샤워 중에 "
                       "갑자기 해답이 떠오를 수 있습니다.")
    
    return "\n\n".join(feedback)

# CSS 스타일
st.markdown("""
<style>
    /* 기본 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    
    /* 1초 원칙 의식의 무대 */
    .focus-stage {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        text-align: center;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .focus-topic {
        font-size: 32px;
        font-weight: bold;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        line-height: 1.5;
        padding: 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        max-width: 800px;
    }
    
    .one-second-rule {
        color: #FFD700;
        font-size: 18px;
        margin-top: 20px;
        padding: 15px;
        background: rgba(0,0,0,0.2);
        border-radius: 10px;
        animation: gentle-pulse 3s ease-in-out infinite;
    }
    
    @keyframes gentle-pulse {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    
    .timer-display {
        font-size: 64px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        font-family: 'Courier New', monospace;
        margin: 20px 0;
    }
    
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
    
    .memo-card {
        background: rgba(255, 255, 255, 0.9);
        border-left: 4px solid #667eea;
        padding: 10px 15px;
        margin: 10px 0;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
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
if 'breathing_count' not in st.session_state:
    st.session_state.breathing_count = 0

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
    이 프로그램은 황농문 교수님의 **'1초 원칙'**과 **'슬로싱킹'** 철학을 바탕으로 
    직장인들이 일상에서 몰입을 실천할 수 있도록 돕습니다.
    
    #### 핵심 원칙:
    
    ### 🎯 1초 원칙
    > "의식의 조명을 단 1초도 다른 곳에 비추지 마세요"
    
    선택한 주제에 온전히 집중하여, 의식이 흐트러질 때마다
    다시 주제로 돌아오는 연습을 합니다.
    
    #### 프로그램 특징:
    1. **🧘 4-8 호흡법** - 이완된 집중 상태 유도
    2. **💡 집중 주제 제시** - 레벨별 맞춤 주제
    3. **📝 잡념/통찰 분리** - 생각 정리 시스템
    4. **⏰ 다양한 시간 설정** - 5분부터 60분까지
    5. **📊 개인화된 피드백** - 몰입 패턴 분석
    
    > **"몰입은 긴장이 아니라 이완입니다"** - 황농문
    """)
    
    # 시작하기
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("🏷️ 닉네임을 입력하세요", placeholder="예: 갯버들")
        if st.button("🚀 프로그램 시작", type="primary", use_container_width=True):
            if name:
                st.session_state.user_name = name
                st.session_state.page = "immersion"
                st.session_state.immersion_step = 1
                st.rerun()
            else:
                st.error("닉네임을 입력해주세요!")

elif st.session_state.page == "immersion":
    if not st.session_state.user_name:
        st.warning("먼저 홈에서 닉네임을 입력해주세요!")
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
                st.session_state.breathing_done = False
                st.session_state.breathing_count = 0
                st.rerun()
        
        # Step 2: 이완 단계 - 점진적 호흡 애니메이션
        elif st.session_state.immersion_step == 2:
            st.markdown("## 🧘 2단계: 의식적 이완")
            st.info("이완된 집중이 진정한 몰입입니다")
            
            st.markdown("""
            ### 4-8 호흡법
            1. 4초간 천천히 숨을 들이마십니다
            2. 8초간 천천히 숨을 내쉽니다
            3. 3회 반복합니다
            """)
            
            # 호흡 가이드 플레이스홀더
            breathing_placeholder = st.empty()
            breathing_placeholder.markdown(
                '<div style="'
                'width: 150px; height: 150px; '
                'border: 4px solid #4CAF50; border-radius: 50%; '
                'margin: 20px auto; display: flex; '
                'align-items: center; justify-content: center; '
                'font-size: 20px; color: #4CAF50;">준비</div>', 
                unsafe_allow_html=True
            )
            
            # 버튼 배치
            button_col1, button_col2, button_col3 = st.columns(3)
            
            with button_col1:
                if st.button("🧘 호흡 시작", type="primary"):
                    progress_bar = st.progress(0)
                    
                    for cycle in range(3):
                        # 들숨 (4초) - 원이 점진적으로 커짐
                        for i in range(40):
                            scale = 1 + (0.3 * (i / 40))  # 1.0 → 1.3
                            opacity = 0.7 + (0.3 * (i / 40))  # 0.7 → 1.0
                            
                            breathing_placeholder.markdown(
                                f'''<div style="
                                    width: {150 * scale}px;
                                    height: {150 * scale}px;
                                    border: 4px solid rgba(76, 175, 80, {opacity});
                                    border-radius: 50%;
                                    margin: 20px auto;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-size: {20 + i/4}px;
                                    color: rgba(76, 175, 80, {opacity});
                                    background: rgba(76, 175, 80, {opacity * 0.1});
                                    transition: all 0.1s ease;
                                    font-weight: bold;
                                ">
                                들숨 {cycle+1}/3<br>{i//10 + 1}초
                                </div>''', 
                                unsafe_allow_html=True
                            )
                            progress_bar.progress((cycle * 120 + i) / 360)
                            time.sleep(0.1)
                        
                        # 날숨 (8초) - 원이 점진적으로 작아짐
                        for i in range(80):
                            scale = 1.3 - (0.4 * (i / 80))  # 1.3 → 0.9
                            opacity = 1 - (0.3 * (i / 80))  # 1.0 → 0.7
                            
                            breathing_placeholder.markdown(
                                f'''<div style="
                                    width: {150 * scale}px;
                                    height: {150 * scale}px;
                                    border: 4px solid rgba(76, 175, 80, {opacity});
                                    border-radius: 50%;
                                    margin: 20px auto;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-size: {24 - i/5}px;
                                    color: rgba(76, 175, 80, {opacity});
                                    background: rgba(76, 175, 80, {opacity * 0.05});
                                    transition: all 0.1s ease;
                                    font-weight: bold;
                                ">
                                날숨 {cycle+1}/3<br>{i//10 + 1}초
                                </div>''', 
                                unsafe_allow_html=True
                            )
                            progress_bar.progress((cycle * 120 + 40 + i) / 360)
                            time.sleep(0.1)
                    
                    st.session_state.breathing_done = True
                    st.session_state.breathing_count += 1
                    breathing_placeholder.markdown(
                        '<div style="'
                        'width: 200px; height: 200px; '
                        'border: 4px solid #4CAF50; border-radius: 50%; '
                        'margin: 20px auto; display: flex; '
                        'align-items: center; justify-content: center; '
                        'font-size: 24px; color: #4CAF50; '
                        'background: rgba(76, 175, 80, 0.1);">✅ 호흡 완료!</div>', 
                        unsafe_allow_html=True
                    )
                    st.success("호흡이 완료되었습니다! 이제 몰입을 시작할 수 있습니다.")
            
            with button_col2:
                st.info(f"호흡 횟수: {st.session_state.breathing_count}회")
            
            with button_col3:
                if st.button("건너뛰기 →"):
                    st.session_state.immersion_step = 3
                    st.rerun()
            
            # 호흡 완료 후 다음 단계
            if st.session_state.breathing_done:
                st.markdown("---")
                if st.button("🎯 몰입 시작하기 →", type="primary", use_container_width=True):
                    st.session_state.immersion_step = 3
                    st.rerun()
        
        # Step 3: 몰입 준비
        elif st.session_state.immersion_step == 3:
            st.markdown("## 🎯 3단계: 몰입 준비")
            
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
                topics = TOPICS[level]
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
            if st.button("🎯 몰입 시작 (1초 원칙)", type="primary", use_container_width=True):
                if st.session_state.current_topic:
                    st.session_state.immersion_active = True
                    st.session_state.start_time = time.time()
                    st.session_state.immersion_step = 4
                    st.rerun()
                else:
                    st.error("주제를 입력해주세요!")
        
        # Step 4: 1초 원칙 몰입
        elif st.session_state.immersion_step == 4:
            # 1초 원칙 의식의 무대
            st.markdown(
                '<div class="focus-stage">'
                f'<div class="focus-topic">{st.session_state.current_topic}</div>'
                '<div class="one-second-rule">💡 1초 원칙: 이 질문에만 의식의 조명을 비추세요</div>'
                '</div>',
                unsafe_allow_html=True
            )
            
            # 타이머
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                elapsed = time.time() - st.session_state.start_time if st.session_state.start_time else 0
                remaining = max(0, st.session_state.selected_time * 60 - elapsed)
                
                # 큰 타이머 표시
                st.markdown(f'<div class="timer-display">{format_time(remaining)}</div>', unsafe_allow_html=True)
                
                # 진행률
                progress = min(1.0, elapsed / (st.session_state.selected_time * 60))
                st.progress(progress, text=f"진행률: {int(progress * 100)}%")
                
                # 타이머 업데이트
                if st.button("⏱️ 타이머 업데이트", use_container_width=True):
                    st.rerun()
            
            st.markdown("---")
            
            # 메모 영역
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🌊 잡념 (놓아주기)")
                thought = st.text_area(
                    "떠오르는 잡념을 적고 놓아주세요",
                    height=150,
                    placeholder="예: 오늘 회의 준비, 저녁 약속...",
                    key="thought_input"
                )
                if st.button("💭 잡념 기록", use_container_width=True):
                    if thought and thought not in st.session_state.thoughts:
                        st.session_state.thoughts.append(thought)
                        st.success("잡념을 기록했습니다. 다시 주제로!")
                        st.rerun()
                
                # 잡념 목록
                if st.session_state.thoughts:
                    for i, t in enumerate(st.session_state.thoughts, 1):
                        st.markdown(f'<div class="memo-card">💭 {t}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 💡 통찰 (떠오른 생각)")
                insight = st.text_area(
                    "떠오른 통찰을 기록하세요",
                    height=150,
                    placeholder="예: 이 문제의 핵심은...",
                    key="insight_input"
                )
                if st.button("✨ 통찰 기록", use_container_width=True):
                    if insight and insight not in st.session_state.insights:
                        st.session_state.insights.append(insight)
                        st.success("통찰을 기록했습니다!")
                        st.rerun()
                
                # 통찰 목록
                if st.session_state.insights:
                    for i, ins in enumerate(st.session_state.insights, 1):
                        st.markdown(f'<div class="memo-card">💡 {ins}</div>', unsafe_allow_html=True)
            
            # 몰입 종료
            st.markdown("---")
            if st.button("🏁 몰입 종료", type="secondary", use_container_width=True):
                st.session_state.immersion_step = 5
                st.rerun()
        
        # Step 5: 완료 및 개인화된 보고서
        elif st.session_state.immersion_step == 5:
            duration = time.time() - st.session_state.start_time if st.session_state.start_time else 0
            korean_time = get_korean_time()
            
            # 세션 저장
            session_data = {
                "user": st.session_state.user_name,
                "date": korean_time.isoformat(),
                "topic": st.session_state.current_topic,
                "duration": duration,
                "thoughts": st.session_state.thoughts,
                "insights": st.session_state.insights,
                "level": level
            }
            save_session(session_data)
            
            st.balloons()
            st.success("🎉 몰입 완료! 수고하셨습니다!")
            
            # 개인화된 피드백 생성
            personalized_feedback = get_personalized_feedback(
                duration,
                len(st.session_state.thoughts),
                len(st.session_state.insights)
            )
            
            # 보고서
            st.markdown("## 📊 몰입 보고서")
            
            report_text = f"""
몰입 보고서
==========
날짜: {korean_time.strftime('%Y-%m-%d %H:%M')} (한국시간)
사용자: {st.session_state.user_name}
레벨: {level}
주제: {st.session_state.current_topic}
몰입 시간: {format_time(duration)}

잡념 기록 ({len(st.session_state.thoughts)}개):
{chr(10).join([f'- {t}' for t in st.session_state.thoughts]) if st.session_state.thoughts else '- 없음'}

통찰 기록 ({len(st.session_state.insights)}개):
{chr(10).join([f'- {i}' for i in st.session_state.insights]) if st.session_state.insights else '- 없음'}

--- 개인 맞춤 피드백 ---
{personalized_feedback}
"""
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📅 날짜:** {korean_time.strftime('%Y-%m-%d %H:%M')} KST")
                st.markdown(f"**💭 주제:** {st.session_state.current_topic}")
                st.markdown(f"**⏱️ 몰입 시간:** {format_time(duration)}")
                st.markdown(f"**🌊 잡념:** {len(st.session_state.thoughts)}개")
                st.markdown(f"**💡 통찰:** {len(st.session_state.insights)}개")
            
            with col2:
                # 다운로드 버튼
                st.markdown("### 📥 보고서 저장")
                filename = f"몰입보고서_{korean_time.strftime('%Y%m%d_%H%M')}.txt"
                st.markdown(create_download_link(report_text, filename), unsafe_allow_html=True)
                
                # 복사용 텍스트
                st.text_area("📋 보고서 내용 (전체 선택 후 Ctrl+C로 복사)", report_text, height=200)
            
            # 개인화된 피드백 표시
            st.markdown("### 🎯 개인 맞춤 피드백")
            feedback_parts = personalized_feedback.split("\n\n")
            for part in feedback_parts:
                st.info(part)
            
            # 통찰 요약
            if st.session_state.insights:
                st.markdown("### 💡 오늘의 주요 통찰")
                for i, insight in enumerate(st.session_state.insights, 1):
                    st.markdown(f"**{i}.** {insight}")
            
            # 초기화
            st.markdown("---")
            if st.button("🔄 새로운 몰입 시작", type="primary", use_container_width=True):
                st.session_state.immersion_step = 1
                st.session_state.thoughts = []
                st.session_state.insights = []
                st.session_state.current_topic = ''
                st.session_state.breathing_done = False
                st.session_state.breathing_count = 0
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
            total_thoughts = sum(len(s.get('thoughts', [])) for s in user_sessions)
            total_insights = sum(len(s.get('insights', [])) for s in user_sessions)
            
            # 통계 카드
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("총 몰입 횟수", f"{total_sessions}회")
            with col2:
                st.metric("총 몰입 시간", format_time(total_time))
            with col3:
                st.metric("평균 몰입 시간", format_time(avg_time))
            with col4:
                st.metric("통찰/잡념 비율", f"{total_insights}/{total_thoughts}")
            
            # 최근 세션
            st.markdown("### 📝 최근 몰입 기록")
            for session in user_sessions[-5:]:
                session_date = session['date'][:16]
                with st.expander(f"{session_date} - {session.get('topic', '제목 없음')[:30]}..."):
                    st.write(f"몰입 시간: {format_time(session.get('duration', 0))}")
                    st.write(f"잡념: {len(session.get('thoughts', []))}개")
                    st.write(f"통찰: {len(session.get('insights', []))}개")
                    
                    if session.get('insights'):
                        st.markdown("**통찰:**")
                        for ins in session['insights']:
                            st.write(f"- {ins}")
        else:
            st.info("아직 몰입 기록이 없습니다. 첫 몰입을 시작해보세요!")
    else:
        st.warning("먼저 로그인해주세요!")

elif st.session_state.page == "report":
    st.markdown("## 📝 종합 보고서")
    
    if st.session_state.user_name:
        user_sessions = [s for s in sessions if s.get('user') == st.session_state.user_name]
        
        if user_sessions:
            korean_time = get_korean_time()
            st.markdown(f"### {st.session_state.user_name}님의 몰입 여정")
            
            # 전체 통계
            total_sessions = len(user_sessions)
            total_time = sum(s.get('duration', 0) for s in user_sessions)
            avg_time = total_time / total_sessions if total_sessions > 0 else 0
            
            # 모든 통찰 수집
            all_insights = []
            for session in user_sessions:
                all_insights.extend(session.get('insights', []))
            
            # 전체 보고서 생성
            full_report = f"""
{st.session_state.user_name}님의 몰입 종합 보고서
{'='*50}
생성 시간: {korean_time.strftime('%Y-%m-%d %H:%M')} (한국시간)

[몰입 통계]
총 몰입 횟수: {total_sessions}회
총 몰입 시간: {format_time(total_time)}
평균 몰입 시간: {format_time(avg_time)}
첫 몰입: {user_sessions[0]['date'][:10]}
최근 몰입: {user_sessions[-1]['date'][:10]}

[주요 통찰 모음] - 총 {len(all_insights)}개
{'-'*30}
"""
            for i, insight in enumerate(all_insights, 1):
                full_report += f"{i}. {insight}\n"
            
            full_report += f"""
{'-'*30}

[성장 기록]
- 초급 단계: {min(5, total_sessions)}회 완료
- 중급 단계: {max(0, min(15, total_sessions - 5))}회 완료
- 고급 단계: {max(0, total_sessions - 20)}회 완료

[1초 원칙 실천]
총 {total_sessions}회의 몰입을 통해
의식의 조명을 주제에 집중하는 훈련을 지속했습니다.

황농문 교수님의 가르침을 따라
"몰입은 긴장이 아니라 이완"임을 체험했습니다.
"""
            
            # 다운로드 버튼과 통계
            col1, col2 = st.columns(2)
            with col1:
                filename = f"종합보고서_{st.session_state.user_name}_{korean_time.strftime('%Y%m%d_%H%M')}.txt"
                st.markdown(create_download_link(full_report, filename), unsafe_allow_html=True)
            
            with col2:
                level, emoji, _ = get_user_level(total_sessions)
                st.metric("현재 레벨", f"{emoji} {level}")
                st.metric("총 통찰 개수", f"{len(all_insights)}개")
            
            # 주요 통찰 표시
            if all_insights:
                st.markdown("#### 💎 최근 통찰 TOP 10")
                for i, insight in enumerate(all_insights[-10:], 1):
                    st.info(f"{i}. {insight}")
            
            # 성장 그래프
            st.markdown("#### 📈 성장 추이")
            growth_data = []
            for i, session in enumerate(user_sessions):
                level_at_time, _, _ = get_user_level(i + 1)
                growth_data.append(f"세션 {i+1}: {level_at_time}")
            
            with st.expander("세션별 레벨 변화 보기"):
                for data in growth_data[-10:]:
                    st.write(data)
            
            st.success(f"총 {total_sessions}회의 몰입으로 꾸준히 성장 중입니다!")
            
            # 전체 보고서 텍스트 영역
            st.text_area("📋 전체 보고서 (Ctrl+C로 복사)", full_report, height=400)
        else:
            st.info("몰입 기록이 없습니다.")
    else:
        st.warning("먼저 로그인해주세요!")

# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 직장인 몰입 체험 프로그램 | "
    "황농문 교수님의 1초 원칙 기반 | "
    "개발: 갯버들(한승희) | "
    "문의: sjks007@gmail.com | "
    "바이브 코딩으로 완성"
    "</div>", 
    unsafe_allow_html=True
)
