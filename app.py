# -*- coding: utf-8 -*-
# app.py - 통합 몰입 체험 프로그램 v6.0 (완전 재작성)
# Created by 갯버들
# Version: 6.0 - 모든 기능 정상 작동 보장

import streamlit as st
import time
from datetime import datetime, timedelta
import json
import pytz

# 한국 시간대 설정
KST = pytz.timezone('Asia/Seoul')

# 페이지 설정
st.set_page_config(
    page_title="통합 몰입 프로그램",
    page_icon="🎯",
    layout="wide"
)

# CSS 스타일 - 의식의 극장 효과 포함
st.markdown("""
<style>
    /* 메인 헤더 */
    .main-header {
        text-align: center;
        color: #1e3d59;
        padding: 2rem;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* 서브 헤더 */
    .sub-header {
        text-align: center;
        color: #5d6d7e;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* 의식의 극장 효과 - 색상 개선 버전 */
    .theater-stage {
        background: linear-gradient(180deg, #2a2a3e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 60px 20px;
        margin: 30px auto;
        position: relative;
        overflow: hidden;
        box-shadow: 
            inset 0 0 100px rgba(0,0,0,0.5),
            0 0 50px rgba(255,215,0,0.2);
    }
    
    .theater-stage::before {
        content: '';
        position: absolute;
        top: -50%;
        left: 50%;
        transform: translateX(-50%);
        width: 300px;
        height: 300px;
        background: radial-gradient(
            ellipse at center,
            rgba(255,255,200,0.6) 0%,
            rgba(255,215,0,0.3) 30%,
            transparent 70%
        );
        animation: spotlight 3s ease-in-out infinite;
    }
    
    @keyframes spotlight {
        0%, 100% { opacity: 0.8; transform: translateX(-50%) scale(1); }
        50% { opacity: 1; transform: translateX(-50%) scale(1.1); }
    }
    
    .stage-title {
        color: #ffffff;
        text-align: center;
        font-size: 2rem;
        margin-bottom: 20px;
        text-shadow: 0 0 30px rgba(255,255,255,0.8);
        position: relative;
        z-index: 1;
    }
    
    .stage-topic {
        color: #ffd700;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        text-shadow: 
            0 0 30px rgba(255,215,0,1),
            0 0 60px rgba(255,215,0,0.5);
        position: relative;
        z-index: 1;
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { opacity: 0.9; }
        50% { opacity: 1; }
    }
    
    /* 타이머 스타일 */
    .timer-display {
        font-size: 3.5rem;
        color: #ff6b6b;
        text-align: center;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        margin: 20px 0;
        text-shadow: 0 0 10px rgba(255,107,107,0.5);
    }
    
    /* 질문 박스 */
    .question-box {
        background: linear-gradient(135deg, #fffef0 0%, #fff9e6 100%);
        border-left: 5px solid #ffd700;
        padding: 20px;
        margin: 20px 0;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255,215,0,0.2);
    }
    
    /* 노트 영역 강조 */
    .note-section {
        background: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
def init_session_state():
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = ""
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'selected_duration' not in st.session_state:
        st.session_state.selected_duration = 5
    if 'today_sessions' not in st.session_state:
        st.session_state.today_sessions = []
    if 'total_minutes' not in st.session_state:
        st.session_state.total_minutes = 0
    if 'daily_question' not in st.session_state:
        st.session_state.daily_question = ""
    if 'gratitude_entries' not in st.session_state:
        st.session_state.gratitude_entries = []
    if 'today_insights' not in st.session_state:
        st.session_state.today_insights = []
    if 'last_question_date' not in st.session_state:
        st.session_state.last_question_date = None
    if 'is_premium' not in st.session_state:
        st.session_state.is_premium = False
    if 'transcriptions' not in st.session_state:
        st.session_state.transcriptions = []

init_session_state()

# 오늘의 질문 생성 함수
def get_today_question():
    questions = [
        "오늘 나는 무엇을 위해 시간을 쓸 것인가?",
        "지금 이 순간, 나에게 가장 중요한 것은 무엇인가?",
        "오늘 내가 감사해야 할 세 가지는 무엇인가?",
        "어제보다 나은 오늘을 만들기 위해 무엇을 할 것인가?",
        "내가 진정으로 원하는 삶의 모습은 무엇인가?",
        "오늘 누군가에게 줄 수 있는 가치는 무엇인가?",
        "지금 이 일이 10년 후에도 중요할까?",
        "오늘 내가 피하고 있는 것은 무엇인가?",
        "지금 이 순간 집중해야 할 한 가지는?",
        "오늘 마주한 도전을 어떻게 기회로 만들까?",
        "내가 가진 것들에 얼마나 감사하고 있는가?",
        "오늘 누군가를 미소짓게 할 수 있는 일은?",
        "지금 내 마음을 무겁게 하는 것은 무엇인가?",
        "오늘 배운 가장 중요한 교훈은 무엇인가?",
        "내일의 나에게 전하고 싶은 메시지는?"
    ]
    today = datetime.now(KST).date()
    index = today.toordinal() % len(questions)
    return questions[index]

# 필사 문구 생성 함수
def get_daily_quote():
    quotes = [
        "사랑한다는 것은 상대방이 나와 다른 존재임을 인정하는 일이다.",
        "진정한 성장은 불편함을 견디는 데서 시작된다.",
        "매일 조금씩 나아지는 것이 큰 변화보다 중요하다.",
        "고독은 자신과 대화할 수 있는 소중한 시간이다.",
        "질문하는 능력이 답을 찾는 능력보다 중요하다.",
        "오늘의 작은 실천이 미래의 큰 변화를 만든다.",
        "실패는 성공으로 가는 필수 과정이다.",
        "타인과의 비교는 성장의 적이다.",
        "감사는 행복으로 가는 가장 빠른 길이다.",
        "침묵 속에서 진정한 지혜가 태어난다."
    ]
    today = datetime.now(KST).date()
    index = today.toordinal() % len(quotes)
    return quotes[index]

# 사이드바 - 후원 시스템
with st.sidebar:
    st.markdown("### 💝 프로그램 후원")
    st.markdown("""
    **토스아이디로 간편 후원**
    `gaetbeodeul`
    
    **후원 금액**
    - ☕ 커피: 3,000원
    - 🍔 식사: 8,000원
    - 💎 프리미엄: 9,900원/월
    
    **프리미엄 혜택**
    ✅ 무제한 몰입 세션
    ✅ 데이터 클라우드 저장
    ✅ 고급 통계 분석
    ✅ 광고 없음
    
    후원 후: immersion@gmail.com
    """)
    
    st.markdown("---")
    
    # 프리미엄 인증
    with st.expander("🔐 프리미엄 인증"):
        email = st.text_input("이메일", key="premium_email")
        if st.button("인증하기", key="auth_btn"):
            # 실제로는 DB 확인 필요
            if email == "premium@test.com":
                st.session_state.is_premium = True
                st.success("✨ 프리미엄 활성화!")
            else:
                st.error("인증 실패. 후원 후 이메일을 보내주세요.")
    
    if st.session_state.is_premium:
        st.success("🌟 프리미엄 사용자")
    else:
        sessions_left = 3 - len(st.session_state.today_sessions)
        st.info(f"무료: 오늘 {sessions_left}회 남음")

# 메인 헤더
st.markdown('<h1 class="main-header">🎯 통합 몰입 프로그램</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">이완된 집중 · 깊은 사고 · 내면 소통</p>', unsafe_allow_html=True)

# 사용자 이름 입력
if not st.session_state.user_name:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 👋 환영합니다!")
        name = st.text_input("닉네임을 입력하세요", placeholder="예: 갯버들")
        if st.button("🚀 시작하기", type="primary", use_container_width=True):
            if name:
                st.session_state.user_name = name
                st.session_state.daily_question = get_today_question()
                st.session_state.last_question_date = datetime.now(KST).date()
                st.rerun()
            else:
                st.error("닉네임을 입력해주세요!")
else:
    # 날짜 변경 체크
    current_date = datetime.now(KST).date()
    if st.session_state.last_question_date != current_date:
        st.session_state.daily_question = get_today_question()
        st.session_state.last_question_date = current_date
        st.session_state.today_sessions = []  # 새로운 날 세션 초기화
        st.session_state.total_minutes = 0
    
    # 환영 메시지 & 통계
    st.success(f"안녕하세요, {st.session_state.user_name}님! 오늘도 몰입을 실천해보세요.")
    
    # 통계 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("오늘 몰입", f"{st.session_state.total_minutes}분")
    with col2:
        st.metric("완료 세션", f"{len(st.session_state.today_sessions)}회")
    with col3:
        level = "초급" if st.session_state.total_minutes < 30 else "중급" if st.session_state.total_minutes < 60 else "고급"
        st.metric("레벨", level)
    with col4:
        st.metric("감사 기록", f"{len(st.session_state.gratitude_entries)}개")
    
    # 오늘의 질문
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown(f"### 📌 오늘의 질문: {st.session_state.daily_question}")
    st.markdown("*이 질문을 하루 3번 이상 떠올려보세요*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭 메뉴
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📖 사용법", 
        "🫁 호흡명상", 
        "🎭 몰입실천", 
        "📝 감사일기", 
        "✍️ 필사하기", 
        "🏃 움직임", 
        "📊 오늘기록", 
        "🔗 추천영상"
    ])
    
    # 탭1: 사용법
    with tab1:
        st.markdown("""
        ### 프로그램 사용법
        
        #### 일일 루틴
        1. **아침**: 호흡명상 → 오늘의 질문 확인 → 필사
        2. **낮**: 몰입 세션 (25분) → 노트 작성
        3. **저녁**: Zone 2 운동 → 감사일기 → 기록 확인
        
        #### 핵심 원칙
        - 이완된 집중 (황농문)
        - 3번 생각하기 (김종원)
        - 감사 습관 (김주환)
        """)
    
    # 탭2: 호흡명상
    with tab2:
        st.markdown("### 🫁 4-8 호흡명상")
        st.info("이완된 상태로 천천히 집중하기")
        
        col1, col2 = st.columns(2)
        with col1:
            rounds = st.slider("호흡 횟수", 3, 10, 3)
        with col2:
            if st.button("🎯 호흡 시작", type="primary", use_container_width=True):
                progress = st.progress(0)
                status = st.empty()
                
                for r in range(rounds):
                    # 들숨 4초
                    for i in range(40):
                        progress.progress((r * 120 + i) / (rounds * 120))
                        status.text(f"🌬️ {r+1}회: 들이쉬기... {i/10:.1f}초")
                        time.sleep(0.1)
                    # 날숨 8초
                    for i in range(80):
                        progress.progress((r * 120 + 40 + i) / (rounds * 120))
                        status.text(f"💨 {r+1}회: 내쉬기... {i/10:.1f}초")
                        time.sleep(0.1)
                
                st.success("✨ 호흡명상 완료! 몰입할 준비가 되었습니다.")
                st.balloons()
    
    # 탭3: 몰입실천 (핵심 기능)
    with tab3:
        st.markdown("### 🎭 의식의 극장 - 몰입 실천")
        
        # 주제 입력
        topic = st.text_input(
            "집중할 주제를 입력하세요",
            value=st.session_state.current_topic,
            placeholder="예: 프로젝트 기획서 작성"
        )
        
        # 시간 선택
        duration = st.select_slider(
            "몰입 시간 (분)",
            options=[5, 10, 15, 25, 45, 60],
            value=st.session_state.selected_duration
        )
        
        # 시작/종료 버튼
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎬 몰입 시작", type="primary", use_container_width=True):
                if not topic:
                    st.error("주제를 입력해주세요!")
                elif not st.session_state.is_premium and len(st.session_state.today_sessions) >= 3:
                    st.warning("🔒 무료 버전은 하루 3회까지입니다.")
                    st.info("사이드바에서 프리미엄 업그레이드하세요!")
                else:
                    st.session_state.current_topic = topic
                    st.session_state.selected_duration = duration
                    st.session_state.is_running = True
                    st.session_state.start_time = datetime.now()
                    st.rerun()
        
        with col2:
            if st.button("⏹️ 몰입 종료", use_container_width=True, disabled=not st.session_state.is_running):
                if st.session_state.is_running:
                    elapsed = int((datetime.now() - st.session_state.start_time).total_seconds() / 60)
                    st.session_state.today_sessions.append({
                        'topic': st.session_state.current_topic,
                        'duration': elapsed,
                        'time': datetime.now(KST).strftime("%H:%M")
                    })
                    st.session_state.total_minutes += elapsed
                    st.session_state.is_running = False
                    st.rerun()
        
        # 몰입 진행 중 표시 (의식의 극장 효과)
        if st.session_state.is_running:
            # 극장 무대 효과
            st.markdown("""
            <div class="theater-stage">
                <h2 class="stage-title">🎭 의식의 극장</h2>
                <h3 class="stage-topic">💡 {}</h3>
            </div>
            """.format(st.session_state.current_topic), unsafe_allow_html=True)
            
            # 타이머 표시
            if st.session_state.start_time:
                elapsed_seconds = (datetime.now() - st.session_state.start_time).total_seconds()
                remaining_seconds = max(0, st.session_state.selected_duration * 60 - elapsed_seconds)
                
                if remaining_seconds > 0:
                    mins, secs = divmod(int(remaining_seconds), 60)
                    st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                    
                    # 진행률
                    progress = min(elapsed_seconds / (st.session_state.selected_duration * 60), 1.0)
                    st.progress(progress)
                    
                    # 자동 새로고침 (3초마다)
                    time.sleep(3)
                    st.rerun()
                else:
                    # 완료
                    st.balloons()
                    st.success("🎉 몰입 완료!")
                    
                    # 세션 저장
                    st.session_state.today_sessions.append({
                        'topic': st.session_state.current_topic,
                        'duration': st.session_state.selected_duration,
                        'time': datetime.now(KST).strftime("%H:%M")
                    })
                    st.session_state.total_minutes += st.session_state.selected_duration
                    st.session_state.is_running = False
                    time.sleep(2)
                    st.rerun()
        
        # 몰입 노트 (항상 표시)
        st.markdown("---")
        st.markdown('<div class="note-section">', unsafe_allow_html=True)
        st.markdown("### 💡 몰입 노트")
        st.info("몰입 중이든 아니든 언제나 메모할 수 있습니다")
        
        note_text = st.text_area(
            "떠오른 생각을 기록하세요",
            height=200,
            placeholder="• 아이디어\n• 해결 방법\n• 통찰\n• 기타 메모",
            key="note_area"
        )
        
        if st.button("💾 노트 저장", use_container_width=True):
            if note_text and note_text.strip():
                st.session_state.today_insights.append({
                    'time': datetime.now(KST).strftime("%H:%M"),
                    'content': note_text
                })
                st.success("✅ 노트가 저장되었습니다!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭4: 감사일기
    with tab4:
        st.markdown("### 📝 감사일기")
        
        category = st.selectbox(
            "카테고리",
            ["일상", "사람", "자신", "자연", "기타"]
        )
        
        gratitude = st.text_area(
            "감사한 일을 적어주세요",
            height=150,
            placeholder="오늘 감사한 일들..."
        )
        
        if st.button("🙏 감사 기록", type="primary"):
            if gratitude:
                st.session_state.gratitude_entries.append({
                    'category': category,
                    'content': gratitude,
                    'time': datetime.now(KST).strftime("%Y-%m-%d %H:%M")
                })
                st.success("감사가 기록되었습니다!")
                st.balloons()
        
        # 최근 감사 목록
        if st.session_state.gratitude_entries:
            st.markdown("#### 최근 감사")
            for entry in st.session_state.gratitude_entries[-3:]:
                st.write(f"• [{entry['category']}] {entry['content'][:50]}...")
    
    # 탭5: 필사하기
    with tab5:
        st.markdown("### ✍️ 오늘의 필사")
        
        today_quote = get_daily_quote()
        st.markdown(f"> **{today_quote}**")
        st.caption("- 김종원 작가")
        
        transcription = st.text_area(
            "위 문구를 천천히 따라 써보세요",
            height=150,
            placeholder="필사하기..."
        )
        
        if st.button("✍️ 필사 완료"):
            if transcription:
                st.session_state.transcriptions.append({
                    'quote': today_quote,
                    'text': transcription,
                    'time': datetime.now(KST).strftime("%Y-%m-%d %H:%M")
                })
                st.success("필사를 완료했습니다!")
    
    # 탭6: 움직임
    with tab6:
        st.markdown("### 🏃 Zone 2 운동")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Zone 2란?**
            - 대화 가능한 강도
            - 심박수 60-70%
            - 30-60분 권장
            """)
        
        with col2:
            if st.checkbox("오늘 운동했나요?"):
                duration = st.slider("운동 시간(분)", 10, 120, 30)
                if st.button("기록"):
                    st.success(f"{duration}분 운동 완료!")
    
    # 탭7: 오늘의 기록
    with tab7:
        st.markdown("### 📊 오늘의 기록")
        
        if st.session_state.today_sessions:
            # 요약
            st.markdown(f"#### {datetime.now(KST).strftime('%Y년 %m월 %d일')} 보고서")
            
            # 세션 목록
            st.markdown("**몰입 세션:**")
            for s in st.session_state.today_sessions:
                st.write(f"• {s['time']} - {s['topic']} ({s['duration']}분)")
            
            # 통찰
            if st.session_state.today_insights:
                st.markdown("**통찰:**")
                for i in st.session_state.today_insights:
                    st.write(f"• {i['time']} - {i['content'][:50]}...")
            
            # 감사
            if st.session_state.gratitude_entries:
                st.markdown("**감사:**")
                for g in st.session_state.gratitude_entries[-3:]:
                    st.write(f"• {g['content'][:50]}...")
            
            # 보고서 다운로드
            report = f"""
=== {datetime.now(KST).strftime('%Y년 %m월 %d일 %H시%M분%S초')} 몰입 보고서 ===

[오늘의 질문]
{st.session_state.daily_question}

[몰입 통계]
총 {st.session_state.total_minutes}분 | {len(st.session_state.today_sessions)}회

[세부 기록]
{chr(10).join([f"• {s['time']} - {s['topic']} ({s['duration']}분)" for s in st.session_state.today_sessions])}

[통찰]
{chr(10).join([f"• {i['content']}" for i in st.session_state.today_insights]) if st.session_state.today_insights else "없음"}

[감사]
{chr(10).join([f"• {g['content']}" for g in st.session_state.gratitude_entries]) if st.session_state.gratitude_entries else "없음"}
"""
            
            st.download_button(
                "📥 보고서 다운로드",
                data=report,
                file_name=f"몰입보고서_{datetime.now(KST).strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.info("아직 기록이 없습니다")
    
    # 탭8: 추천 영상
    with tab8:
        st.markdown("### 🔗 추천 YouTube 채널")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **황농문 교수님**
            
            [몰입아카데미](https://youtube.com/@molipacademy)
            
            몰입의 즐거움을 체험하고
            의식의 무대를 활용하는
            이완된 집중의 방법론
            """)
        
        with col2:
            st.markdown("""
            **김종원 작가님**
            
            [채널 바로가기](https://youtube.com/channel/UCR8ixAPYVq4uzN_w_gtGxOw)
            
            하루 한 질문으로
            깊이 생각하는 힘을 기르고
            필사로 마음을 다스리기
            """)
        
        with col3:
            st.markdown("""
            **김주환 교수님**
            
            [채널 바로가기](https://youtube.com/@joohankim)
            
            내면소통과 회복탄력성으로
            감사의 과학을 실천하고
            그릿을 기르는 방법
            """)

# 푸터
st.markdown("---")
st.markdown("*🌿 Created by 갯버들 | 황농문·김종원·김주환 님의 지혜를 존중하며*")
