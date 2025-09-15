# app.py - 직장인 몰입 프로그램 v5.0 (모든 문제 해결)
import streamlit as st
import time
from datetime import datetime, timedelta
import json
from pathlib import Path
import random
import base64

# 페이지 설정
st.set_page_config(
    page_title="직장인 몰입 프로그램",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 데이터 저장 경로
DATA_DIR = Path("immersion_data")
DATA_DIR.mkdir(exist_ok=True)
USER_DATA_FILE = DATA_DIR / "user_data.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
HABIT_FILE = DATA_DIR / "habit_tracking.json"

# 데이터 관리 함수
def load_user_data():
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_habit_data():
    if HABIT_FILE.exists():
        with open(HABIT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"start_date": str(datetime.now().date()), "total_days": 0, "streak": 0}

def save_habit_data(data):
    with open(HABIT_FILE, 'w', encoding='utf-8') as f:
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

# CSS - 깜빡거림 완전 제거, 안정적인 UI
st.markdown("""
<style>
    /* 애니메이션 비활성화 */
    * {
        animation: none !important;
        transition: none !important;
    }
    
    /* Streamlit 기본 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 타이머 스타일 - 고정된 크기 */
    .timer-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin: 2rem 0;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 도파민 보상 시스템 */
    .reward-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        padding: 1rem 2rem;
        border-radius: 30px;
        text-align: center;
        font-weight: bold;
        color: #333;
        margin: 1rem 0;
    }
    
    /* 습관 추적 */
    .habit-tracker {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .habit-day {
        display: inline-block;
        width: 30px;
        height: 30px;
        margin: 2px;
        border-radius: 5px;
        text-align: center;
        line-height: 30px;
        font-size: 12px;
    }
    
    .day-completed {
        background: #4CAF50;
        color: white;
    }
    
    .day-pending {
        background: #e0e0e0;
        color: #666;
    }
    
    /* 레벨 시스템 */
    .level-display {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    
    /* Stop 버튼 숨기기 */
    button[kind="stop"] {
        display: none !important;
    }
    
    /* Running 아이콘 숨기기 */
    .stSpinner {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript 타이머 (깜빡거림 없음)
def inject_timer_script():
    timer_script = """
    <script>
    var startTime = Date.now();
    var timerInterval;
    
    function updateTimer() {
        var elapsed = Math.floor((Date.now() - startTime) / 1000);
        var minutes = Math.floor(elapsed / 60);
        var seconds = elapsed % 60;
        var display = minutes + "분 " + seconds + "초";
        
        var timerElement = document.getElementById('timer-display');
        if (timerElement) {
            timerElement.innerHTML = display;
        }
    }
    
    function startTimer() {
        startTime = Date.now();
        timerInterval = setInterval(updateTimer, 1000);
    }
    
    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
        }
    }
    
    // 자동 시작
    startTimer();
    </script>
    """
    st.markdown(timer_script, unsafe_allow_html=True)

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'immersion_step' not in st.session_state:
    st.session_state.immersion_step = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'thoughts' not in st.session_state:
    st.session_state.thoughts = []
if 'distractions' not in st.session_state:
    st.session_state.distractions = []
if 'daily_quote' not in st.session_state:
    # 하루에 한 번만 선택되도록
    st.session_state.daily_quote = None
    st.session_state.quote_date = None
if 'preparation_checks' not in st.session_state:
    st.session_state.preparation_checks = {}
if 'session_report' not in st.session_state:
    st.session_state.session_report = None

# 황농문 교수님 명언 (매일 하나씩)
QUOTES = [
    "몰입은 긴장이 아니라 이완입니다.",
    "1초 원칙: 의식의 조명을 단 1초도 다른 곳에 비추지 마세요.",
    "천천히 오래 생각하는 것이 빨리 생각하는 것보다 중요합니다.",
    "뇌의 안전한 놀이터를 만드세요.",
    "슬로싱킹은 느리게 생각하는 것이 아니라, 오래 생각하는 것입니다.",
    "문제를 해결하려 하지 말고, 문제와 함께 머물러보세요.",
    "의식적 이완이 진정한 몰입의 시작입니다.",
    "포기하지 않고 계속 생각하면 반드시 답이 나옵니다."
]

# 김주환 교수 도파민 이론 기반 보상 메시지
DOPAMINE_REWARDS = {
    "unexpected": [
        "🎉 와! 오늘 특별 보너스 포인트 획득!",
        "💎 숨겨진 보상 발견! 몰입 마스터의 길이 열렸습니다!",
        "🌟 예상치 못한 선물! 당신의 노력이 빛나고 있어요!"
    ],
    "milestone": [
        "🏆 10일 연속 몰입 달성! 습관이 형성되고 있어요!",
        "🎯 30일 챌린지 완료! 진정한 몰입러가 되셨네요!",
        "👑 66일 달성! 완벽한 습관 형성 완료!"
    ]
}

def get_daily_quote():
    """매일 다른 명언 선택 (날짜 기반)"""
    today = datetime.now().date()
    if st.session_state.quote_date != today:
        st.session_state.daily_quote = QUOTES[today.toordinal() % len(QUOTES)]
        st.session_state.quote_date = today
    return st.session_state.daily_quote

def calculate_habit_progress():
    """66일 습관 형성 진행률 계산"""
    habit_data = load_habit_data()
    start_date = datetime.strptime(habit_data["start_date"], "%Y-%m-%d").date()
    today = datetime.now().date()
    days_passed = (today - start_date).days + 1
    
    progress = min(days_passed / 66 * 100, 100)
    return days_passed, progress, habit_data

def generate_txt_report(session_data):
    """TXT 형식 보고서 생성"""
    report = []
    report.append("=" * 50)
    report.append(f"직장인 몰입 실천 보고서")
    report.append(f"제목: {session_data['topic']}")
    report.append(f"일시: {session_data['date']}")
    report.append(f"이름: {session_data['user_name']}")
    report.append("=" * 50)
    report.append("")
    
    report.append(f"⏱️ 몰입 시간: {session_data['duration_min']}분 {session_data['duration_sec']}초")
    report.append(f"📍 몰입 주제: {session_data['topic']}")
    report.append("")
    
    report.append("💭 떠오른 생각들:")
    for i, thought in enumerate(session_data['thoughts'], 1):
        report.append(f"  {i}. {thought}")
    report.append("")
    
    if session_data['distractions']:
        report.append("🔄 알아차린 잡념들:")
        for i, distraction in enumerate(session_data['distractions'], 1):
            report.append(f"  {i}. {distraction}")
        report.append("")
    
    report.append(f"📊 몰입 품질 점수: {session_data['quality_score']}/5")
    report.append(f"💬 소감: {session_data['reflection']}")
    report.append("")
    
    report.append(f"🎯 66일 습관 형성 진행: Day {session_data['habit_day']}/66 ({session_data['habit_progress']:.1f}%)")
    report.append("")
    
    report.append("=" * 50)
    report.append("황농문 교수님의 몰입 이론 기반")
    report.append("김주환 교수님의 도파민 이론 적용")
    report.append("Made with ❤️ by 갯버들")
    
    return "\n".join(report)

# 메인 페이지
if st.session_state.page == 'home':
    st.title("🎯 직장인 몰입 프로그램")
    
    # 매일 바뀌는 명언 (안정적으로 표시)
    daily_quote = get_daily_quote()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; padding: 2rem; border-radius: 15px; 
                text-align: center; margin-bottom: 2rem;'>
        <h3>오늘의 지혜</h3>
        <p style='font-size: 1.2rem; margin-top: 1rem;'>"{daily_quote}"</p>
        <p style='margin-top: 1rem; opacity: 0.9;'>- 황농문 교수 -</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 👋 환영합니다!
        
        이 프로그램은 **황농문 교수님의 몰입 이론**과 **김주환 교수님의 도파민 연구**를 기반으로
        직장인들이 일상에서 몰입을 실천할 수 있도록 돕습니다.
        
        #### 🧪 과학적 기반
        - **슬로싱킹**: 천천히 오래 생각하기
        - **도파민 보상**: 예측 오차를 통한 동기부여
        - **66일 법칙**: 진짜 습관 형성 기간
        
        #### 📊 현재 진행 상황
        """)
        
        # 습관 추적 표시
        days_passed, progress, habit_data = calculate_habit_progress()
        
        st.markdown(f"""
        <div class='habit-tracker'>
            <h4>🗓️ 66일 습관 형성 챌린지</h4>
            <div style='margin: 1rem 0;'>
                <strong>Day {days_passed}/66</strong> ({progress:.1f}% 완료)
            </div>
            <div style='background: #ddd; height: 30px; border-radius: 15px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #4CAF50, #8BC34A); 
                           width: {progress}%; height: 100%; 
                           display: flex; align-items: center; justify-content: center;'>
                    {f'{progress:.0f}%' if progress > 10 else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 예상치 못한 보상 (도파민 이론)
        if random.random() < 0.2:  # 20% 확률로 보상
            reward = random.choice(DOPAMINE_REWARDS["unexpected"])
            st.markdown(f"""
            <div class='reward-badge'>
                {reward}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        user_data = load_user_data()
        
        if user_data:
            sessions = load_sessions()
            total_sessions = len(sessions)
            
            # 레벨 계산
            if total_sessions < 5:
                level = "🌱 초급"
                level_color = "#4CAF50"
            elif total_sessions < 20:
                level = "🌿 중급"
                level_color = "#FF9800"
            else:
                level = "🌳 고급"
                level_color = "#9C27B0"
            
            st.markdown(f"""
            <div class='level-display'>
                <h3>{level}</h3>
                <p>총 {total_sessions}회 몰입</p>
            </div>
            """, unsafe_allow_html=True)
        
        name = st.text_input("닉네임을 입력하세요", 
                            value=st.session_state.user_name,
                            placeholder="예: 갯버들")
        
        if name:
            st.session_state.user_name = name
            if st.button("🎯 몰입 시작하기", type="primary", use_container_width=True):
                st.session_state.page = "immersion"
                st.session_state.immersion_step = 1
                st.rerun()

elif st.session_state.page == "immersion":
    st.title("🎯 몰입 체험")
    
    # 단계별 진행
    if st.session_state.immersion_step == 1:
        st.markdown("### 1️⃣ 몰입 전 준비 체크")
        
        st.info("최적의 몰입을 위한 준비 상태를 확인합니다. 필수가 아닙니다!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            exercise = st.checkbox("💪 30분 이상 운동 완료", 
                                  value=st.session_state.preparation_checks.get('exercise', False))
            water = st.checkbox("💧 충분한 수분 섭취", 
                               value=st.session_state.preparation_checks.get('water', False))
        
        with col2:
            phone = st.checkbox("📱 핸드폰 무음 설정", 
                              value=st.session_state.preparation_checks.get('phone', False))
            distraction = st.checkbox("🚫 방해 요소 제거", 
                                    value=st.session_state.preparation_checks.get('distraction', False))
        
        st.session_state.preparation_checks = {
            'exercise': exercise,
            'water': water,
            'phone': phone,
            'distraction': distraction
        }
        
        # 체크 개수에 따른 피드백
        checked_count = sum([exercise, water, phone, distraction])
        
        if checked_count == 4:
            st.success("완벽한 준비 상태입니다! 🎉")
        elif checked_count >= 2:
            st.warning("준비가 잘 되어있네요! 몰입을 시작해도 좋습니다.")
        else:
            st.info("준비가 부족해도 괜찮습니다. 몰입은 언제든 가능합니다!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("다음 단계로 →", type="primary", use_container_width=True):
                st.session_state.immersion_step = 2
                st.rerun()
    
    elif st.session_state.immersion_step == 2:
        st.markdown("### 2️⃣ 의식적 이완 (4-8 호흡)")
        
        st.info("몰입을 위한 최적의 뇌 상태를 만듭니다")
        
        breathing_done = st.checkbox("호흡 명상 완료", 
                                    value=st.session_state.get('breathing_done', False))
        
        if breathing_done:
            st.success("✅ 의식적 이완 완료! 이제 몰입할 준비가 되었습니다.")
            st.session_state.breathing_done = True
        else:
            st.markdown("""
            **4-8 호흡법 안내:**
            1. 코로 4초간 들이마시기
            2. 입으로 8초간 내쉬기
            3. 3회 반복
            
            천천히 따라해보세요. 서두르지 마세요.
            """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("몰입 시작 →", type="primary", use_container_width=True):
                st.session_state.immersion_step = 3
                st.session_state.start_time = datetime.now()
                st.rerun()
    
    elif st.session_state.immersion_step == 3:
        st.markdown("### 3️⃣ 슬로싱킹 - 천천히 오래 생각하기")
        
        # 주제 선택
        topics = [
            "오늘 나에게 가장 중요한 일은?",
            "최근 나를 성장시킨 경험은?",
            "내가 정말 원하는 것은 무엇인가?",
            "오늘 감사한 것 3가지는?",
            "나의 강점을 어떻게 활용할까?"
        ]
        
        topic = st.selectbox("오늘의 몰입 주제", topics + ["직접 입력"])
        
        if topic == "직접 입력":
            topic = st.text_input("주제를 입력하세요")
        
        st.session_state.current_topic = topic
        
        # 타이머 표시 (JavaScript 기반 - 깜빡거림 없음)
        st.markdown("""
        <div class='timer-display' id='timer-display'>
            타이머 시작 중...
        </div>
        """, unsafe_allow_html=True)
        
        inject_timer_script()
        
        # 생각 기록
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💡 떠오른 생각")
            thought = st.text_area("통찰이나 아이디어를 기록하세요", key="thought_input")
            if st.button("생각 저장", type="secondary"):
                if thought and thought not in st.session_state.thoughts:
                    st.session_state.thoughts.append(thought)
                    st.success("저장되었습니다!")
            
            if st.session_state.thoughts:
                st.markdown("**저장된 생각들:**")
                for i, t in enumerate(st.session_state.thoughts, 1):
                    st.write(f"{i}. {t}")
        
        with col2:
            st.markdown("#### 🔄 잡념 포착")
            distraction = st.text_area("잡념을 알아차렸다면 기록하세요", key="distraction_input")
            if st.button("잡념 기록", type="secondary"):
                if distraction and distraction not in st.session_state.distractions:
                    st.session_state.distractions.append(distraction)
                    st.info("잡념을 알아차렸네요! 다시 주제로 돌아오세요.")
            
            if st.session_state.distractions:
                st.markdown("**포착한 잡념들:**")
                for i, d in enumerate(st.session_state.distractions, 1):
                    st.write(f"{i}. {d}")
        
        st.markdown("---")
        
        if st.button("🏁 몰입 종료 & 보고서 생성", type="primary", use_container_width=True):
            end_time = datetime.now()
            duration = end_time - st.session_state.start_time
            
            # 세션 데이터 생성
            session_data = {
                "date": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "user_name": st.session_state.user_name,
                "topic": topic,
                "duration_min": int(duration.total_seconds() // 60),
                "duration_sec": int(duration.total_seconds() % 60),
                "thoughts": st.session_state.thoughts,
                "distractions": st.session_state.distractions,
                "quality_score": 0,
                "reflection": "",
                "habit_day": 0,
                "habit_progress": 0
            }
            
            st.session_state.session_report = session_data
            st.session_state.immersion_step = 4
            st.rerun()
    
    elif st.session_state.immersion_step == 4:
        st.markdown("### 📊 몰입 보고서")
        
        # 성취감 피드백 (도파민 보상)
        st.balloons()
        
        session_data = st.session_state.session_report
        
        # 몰입 품질 평가
        st.markdown("#### 자기 평가")
        quality_score = st.slider("오늘 몰입의 품질은?", 1, 5, 3)
        reflection = st.text_area("몰입 소감을 남겨주세요")
        
        session_data["quality_score"] = quality_score
        session_data["reflection"] = reflection
        
        # 습관 진행 상황 업데이트
        days_passed, progress, habit_data = calculate_habit_progress()
        session_data["habit_day"] = days_passed
        session_data["habit_progress"] = progress
        
        # 보고서 미리보기
        st.markdown("#### 📄 보고서 미리보기")
        report_text = generate_txt_report(session_data)
        st.text_area("", report_text, height=400)
        
        # TXT 다운로드 버튼
        col1, col2 = st.columns(2)
        
        with col1:
            # 파일명에 날짜와 시간 포함
            filename = f"몰입보고서_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            b64 = base64.b64encode(report_text.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">📥 보고서 다운로드 (TXT)</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            if st.button("💾 세션 저장 & 홈으로", type="primary"):
                # 세션 저장
                save_session(session_data)
                
                # 습관 데이터 업데이트
                habit_data["total_days"] = days_passed
                save_habit_data(habit_data)
                
                # 상태 초기화
                st.session_state.thoughts = []
                st.session_state.distractions = []
                st.session_state.immersion_step = 0
                st.session_state.page = 'home'
                st.session_state.session_report = None
                st.rerun()

# 사이드바
with st.sidebar:
    st.markdown("### 📚 몰입 가이드")
    
    st.markdown("""
    **황농문 교수님의 몰입 원칙:**
    1. 의식적 이완
    2. 1초 원칙
    3. 슬로싱킹
    
    **김주환 교수님의 도파민 이론:**
    - 예측 오차가 동기부여의 핵심
    - MCII: 목표와 현실의 격차 인식
    
    **66일 습관 형성:**
    - UCL 연구 기반
    - 평균 66일이 진짜 습관
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ by 갯버들")
    st.markdown("황농문 교수님께 드리는 프로그램")
