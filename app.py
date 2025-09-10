# -*- coding: utf-8 -*-
# app.py - 통합 몰입 체험 프로그램 (최종 수정판)
# Created by 갯버들
# Version: 5.0 - 완전 수정 버전

import streamlit as st
import time
from datetime import datetime, timedelta
import random
import json

# 페이지 설정
st.set_page_config(
    page_title="통합 몰입 프로그램",
    page_icon="🎯",
    layout="wide"
)

# 스타일 정의
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1e3d59;
        padding: 1rem;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        text-align: center;
        color: #5d6d7e;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stage-box {
        background: linear-gradient(180deg, #f0f4f8 0%, #d9e2ec 100%);
        border: 2px solid #ddd;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .timer-text {
        font-size: 3rem;
        color: #ff6b6b;
        text-align: center;
        font-weight: bold;
    }
    .question-box {
        background: #fffef0;
        border-left: 4px solid #ffd700;
        padding: 15px;
        margin: 15px 0;
        font-style: italic;
    }
    .gratitude-box {
        background: #f0fff4;
        border-left: 4px solid #48bb78;
        padding: 15px;
        margin: 15px 0;
    }
    .spotlight {
        background: radial-gradient(circle at center, rgba(255,255,255,0.9) 0%, rgba(255,255,200,0.3) 50%, rgba(0,0,0,0.1) 100%);
        border-radius: 50%;
        padding: 30px;
        margin: 20px auto;
        max-width: 400px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
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
if 'breathing_complete' not in st.session_state:
    st.session_state.breathing_complete = False
if 'today_insights' not in st.session_state:
    st.session_state.today_insights = []
if 'last_question_date' not in st.session_state:
    st.session_state.last_question_date = None

# 오늘의 질문 생성 (날짜 기반으로 매일 변경)
def get_today_question():
    daily_questions = [
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
    # 날짜를 기반으로 매일 다른 질문 선택
    today_index = datetime.now().timetuple().tm_yday % len(daily_questions)
    return daily_questions[today_index]

# 필사할 문구들 (김종원 작가님)
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
    today_index = datetime.now().timetuple().tm_yday % len(quotes)
    return quotes[today_index]

# 헤더
st.markdown('<h1 class="main-header">🎯 통합 몰입 프로그램</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">이완된 집중 · 깊은 사고 · 내면 소통</p>', unsafe_allow_html=True)

# 이름 입력
if not st.session_state.user_name:
    with st.container():
        st.markdown("### 👋 환영합니다!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            name = st.text_input("닉네임을 입력하세요", placeholder="예: 갯버들")
            if st.button("시작하기", type="primary", use_container_width=True):
                if name:
                    st.session_state.user_name = name
                    st.session_state.daily_question = get_today_question()
                    st.session_state.last_question_date = datetime.now().date()
                    st.rerun()
                else:
                    st.warning("닉네임을 입력해주세요")
else:
    # 날짜가 바뀌었으면 새로운 질문 생성
    if st.session_state.last_question_date != datetime.now().date():
        st.session_state.daily_question = get_today_question()
        st.session_state.last_question_date = datetime.now().date()
    
    # 오늘의 통계 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("오늘의 몰입", f"{st.session_state.total_minutes}분")
    with col2:
        st.metric("완료 세션", f"{len(st.session_state.today_sessions)}회")
    with col3:
        level = "초급" if st.session_state.total_minutes < 30 else "중급" if st.session_state.total_minutes < 60 else "고급"
        st.metric("몰입 레벨", level)
    with col4:
        st.metric("감사 기록", f"{len(st.session_state.gratitude_entries)}개")
    
    # 오늘의 질문 표시
    st.markdown("---")
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown(f"### 📌 오늘의 질문")
    st.markdown(f"**{st.session_state.daily_question}**")
    st.markdown("*이 질문을 품고 하루를 보내세요. 3번 이상 떠올리며 깊이 생각해보세요.*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭 구성 (필사 메뉴 추가)
    tabs = st.tabs(["📖 사용법", "🫁 호흡명상", "🎭 몰입실천", "📝 감사일기", "✍️ 필사하기", "🏃 움직임", "📊 오늘의 기록", "🔗 추천 영상"])
    
    with tabs[0]:
        st.markdown("""
        ### 🌟 통합 몰입 프로그램 사용법
        
        이 프로그램은 세 분의 지혜를 통합했습니다:
        - **황농문 교수님**: 이완된 집중, 의식의 무대
        - **김종원 작가님**: 하루 한 질문, 3번 이상 생각하기, 필사
        - **김주환 교수님**: 내면소통, 감사일기, 존2 운동
        
        #### 📅 일일 루틴
        
        **아침 (기상 직후)**
        1. 오늘의 질문 확인
        2. 호흡명상 (4-8 호흡법)
        3. 오늘의 문구 필사
        4. 첫 몰입 세션 (5-10분)
        
        **낮 (업무 중)**
        - 오늘의 질문 떠올리기 (최소 3회)
        - 짧은 몰입 세션 (포모도로)
        - 떠오른 통찰 기록
        
        **저녁 (퇴근 후)**
        1. 존2 운동 (가벼운 걷기/조깅)
        2. 감사일기 작성 (3가지)
        3. 오늘의 기록 확인
        
        #### 💡 핵심 원칙
        - **이완된 집중**: 힘을 빼고 자연스럽게
        - **반복 사고**: 한 가지를 깊이, 여러 번
        - **감사 습관**: 작은 것에도 감사하기
        - **꾸준한 기록**: 성장의 흔적 남기기
        """)
    
    with tabs[1]:
        st.markdown("### 🫁 4-8 호흡명상")
        st.info("이완된 상태에서 천천히 생각하기")
        
        col1, col2 = st.columns(2)
        with col1:
            breathing_rounds = st.number_input("호흡 횟수", min_value=3, max_value=10, value=3)
        with col2:
            if st.button("호흡명상 시작", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for round in range(breathing_rounds):
                    # 들숨
                    for i in range(40):
                        progress = (round * 120 + i) / (breathing_rounds * 120)
                        progress_bar.progress(progress)
                        status_text.text(f"🌬️ {round+1}회차: 들이쉬기... {i/10:.1f}초")
                        time.sleep(0.1)
                    
                    # 날숨
                    for i in range(80):
                        progress = (round * 120 + 40 + i) / (breathing_rounds * 120)
                        progress_bar.progress(progress)
                        status_text.text(f"💨 {round+1}회차: 내쉬기... {i/10:.1f}초")
                        time.sleep(0.1)
                
                st.success("✨ 호흡명상 완료! 이제 몰입할 준비가 되었습니다.")
                st.balloons()
    
    with tabs[2]:
        st.markdown("### 🎭 의식의 무대 - 몰입 실천")
        
        # 주제 입력
        topic = st.text_input(
            "오늘 집중할 주제", 
            value=st.session_state.current_topic,
            placeholder="예: 프로젝트 기획서 작성"
        )
        
        # 시간 선택
        duration = st.select_slider(
            "몰입 시간",
            options=[5, 10, 15, 25, 45, 60],
            value=st.session_state.selected_duration
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎬 몰입 시작", type="primary", use_container_width=True):
                if topic:
                    # 무료 사용자 제한 확인
                    if not st.session_state.get('is_premium', False):
                        if len(st.session_state.today_sessions) >= 3:
                            st.warning("🔒 무료 버전은 하루 3회까지 사용 가능합니다.")
                            st.info("프리미엄으로 업그레이드하여 무제한 몰입하세요!")
                            st.stop()
                    
                    st.session_state.current_topic = topic
                    st.session_state.selected_duration = duration
                    st.session_state.is_running = True
                    st.session_state.start_time = datetime.now()
                    st.rerun()
                else:
                    st.warning("주제를 입력해주세요")
        
        with col2:
            if st.button("⏹️ 몰입 종료", use_container_width=True):
                if st.session_state.is_running:
                    elapsed = (datetime.now() - st.session_state.start_time).total_seconds() // 60
                    st.session_state.today_sessions.append({
                        'topic': st.session_state.current_topic,
                        'duration': int(elapsed),
                        'time': datetime.now().strftime("%H:%M")
                    })
                    st.session_state.total_minutes += int(elapsed)
                    st.session_state.is_running = False
                    st.rerun()
        
        # 몰입 진행 중 표시
        if st.session_state.is_running:
            # 무대 효과 추가 (스포트라이트)
            st.markdown('<div class="spotlight">', unsafe_allow_html=True)
            st.markdown("## 🎭 의식의 무대")
            st.markdown(f"### 💡 {st.session_state.current_topic}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 타이머
            if st.session_state.start_time:
                elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
                remaining = max(0, st.session_state.selected_duration * 60 - elapsed)
                
                if remaining > 0:
                    mins, secs = divmod(int(remaining), 60)
                    st.markdown(f'<div class="timer-text">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                    
                    # 진행률 표시
                    progress = min(elapsed / (st.session_state.selected_duration * 60), 1.0)
                    st.progress(progress)
                    
                    # 3초마다 자동 새로고침
                    time.sleep(3)
                    st.rerun()
                else:
                    # 몰입 완료
                    st.balloons()
                    st.success("🎉 몰입 완료!")
                    
                    # 세션 기록
                    st.session_state.today_sessions.append({
                        'topic': st.session_state.current_topic,
                        'duration': st.session_state.selected_duration,
                        'time': datetime.now().strftime("%H:%M")
                    })
                    st.session_state.total_minutes += st.session_state.selected_duration
                    st.session_state.is_running = False
                    time.sleep(2)
                    st.rerun()
        
        # 몰입 노트 (통합 버전)
        st.markdown("---")
        st.markdown("#### 💡 몰입 노트")
        note = st.text_area(
            "떠오른 생각을 자유롭게 기록하세요",
            height=200,
            placeholder="• 주제 관련 아이디어\n• 해결해야 할 문제\n• 떠오른 통찰\n• 기타 메모",
            key="immersion_note"
        )
        
        if st.button("💾 노트 저장", use_container_width=True):
            if note and note.strip():
                st.session_state.today_insights.append({
                    'time': datetime.now().strftime("%H:%M"),
                    'content': note
                })
                st.success("노트가 저장되었습니다!")
    
    with tabs[3]:
        st.markdown("### 📝 감사일기")
        st.info("감사는 내면소통의 시작입니다")
        
        # 감사 카테고리
        category = st.selectbox(
            "감사 카테고리",
            ["일상의 감사", "사람에 대한 감사", "나 자신에 대한 감사", "자연에 대한 감사", "기타"]
        )
        
        # 감사 내용 입력
        gratitude_text = st.text_area(
            "오늘 감사한 일을 적어주세요",
            placeholder="예: 아침을 차려준 아내에게 감사합니다\n동료가 커피를 사주어 감사합니다\n건강하게 일어난 것에 감사합니다",
            height=150
        )
        
        if st.button("감사 기록하기", type="primary"):
            if gratitude_text:
                st.session_state.gratitude_entries.append({
                    'category': category,
                    'content': gratitude_text,
                    'time': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("✨ 감사가 기록되었습니다!")
                st.balloons()
        
        # 오늘의 감사 목록
        if st.session_state.gratitude_entries:
            st.markdown("---")
            st.markdown("### 오늘의 감사 목록")
            for i, entry in enumerate(st.session_state.gratitude_entries[-5:], 1):
                st.markdown(f"**{i}. [{entry['category']}]** {entry['content'][:50]}...")
    
    with tabs[4]:
        st.markdown("### ✍️ 오늘의 필사")
        st.info("손으로 쓰며 마음에 새기기")
        
        # 오늘의 필사 문구
        today_quote = get_daily_quote()
        
        st.markdown("#### 📜 오늘의 문구")
        st.markdown(f"> **{today_quote}**")
        st.caption("- 김종원 작가님의 말씀 중에서")
        
        st.markdown("---")
        
        # 필사 공간
        st.markdown("#### ✏️ 필사하기")
        st.info("아래 공간에 위 문구를 천천히 따라 써보세요. 손으로 쓰면 더 좋습니다.")
        
        written_text = st.text_area(
            "필사 공간",
            height=150,
            placeholder="위 문구를 이곳에 천천히 따라 써보세요...",
            key="transcription"
        )
        
        if st.button("필사 완료", use_container_width=True):
            if written_text:
                st.success("✅ 필사를 완료했습니다! 오늘의 문구가 마음에 새겨지길 바랍니다.")
                st.balloons()
        
        st.markdown("---")
        st.markdown("""
        #### 💭 필사의 의미
        - 천천히 쓰며 의미를 되새김
        - 손과 마음의 연결
        - 깊은 사고의 시작
        - 하루 한 문장의 지혜
        """)
    
    with tabs[5]:
        st.markdown("### 🏃 움직임과 사고 (Zone 2 운동)")
        st.info("움직이면서 생각하면 창의성이 2배 증가합니다")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🚶 Zone 2 운동이란?
            - 대화 가능한 강도의 유산소 운동
            - 심박수: 최대심박수의 60-70%
            - 권장시간: 30-60분
            
            #### 💡 운동 중 할 일
            1. 오늘의 질문 떠올리기
            2. 몰입 주제 재정리
            3. 감사할 일 찾기
            """)
        
        with col2:
            st.markdown("""
            #### 📱 실천 방법
            1. 가벼운 산책 시작
            2. 오늘의 질문 3번 반복
            3. 떠오른 생각 음성 메모
            4. 돌아와서 기록 정리
            
            #### 🎯 목표
            - 주 3회 이상
            - 회당 30분 이상
            - 꾸준함이 핵심
            """)
        
        # 운동 기록
        st.markdown("---")
        exercise_done = st.checkbox("오늘 Zone 2 운동을 했나요?")
        if exercise_done:
            exercise_duration = st.slider("운동 시간 (분)", 10, 120, 30)
            exercise_insight = st.text_area("운동 중 떠오른 생각", placeholder="걸으면서 떠오른 아이디어나 통찰을 적어주세요")
            if st.button("운동 기록 저장"):
                st.success(f"✅ {exercise_duration}분 운동 완료!")
    
    with tabs[6]:
        st.markdown("### 📊 오늘의 기록 & 자동 보고서")
        
        # 자동 보고서 생성
        if st.session_state.today_sessions or st.session_state.gratitude_entries:
            st.markdown("---")
            st.markdown(f"### 📋 {datetime.now().strftime('%Y년 %m월 %d일')} 몰입 보고서")
            
            # 요약 통계
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 몰입 시간", f"{st.session_state.total_minutes}분")
            with col2:
                st.metric("완료 세션", f"{len(st.session_state.today_sessions)}개")
            with col3:
                avg_duration = st.session_state.total_minutes / len(st.session_state.today_sessions) if st.session_state.today_sessions else 0
                st.metric("평균 집중 시간", f"{avg_duration:.0f}분")
            
            # 세션 상세
            if st.session_state.today_sessions:
                st.markdown("#### 🎯 몰입 세션")
                for session in st.session_state.today_sessions:
                    st.markdown(f"- **{session['time']}** | {session['topic']} ({session['duration']}분)")
            
            # 통찰 기록
            if st.session_state.today_insights:
                st.markdown("#### 💡 오늘의 통찰")
                for insight in st.session_state.today_insights:
                    st.markdown(f"- **{insight['time']}** | {insight['content']}")
            
            # 감사 요약
            if st.session_state.gratitude_entries:
                st.markdown(f"#### 🙏 감사 기록 ({len(st.session_state.gratitude_entries)}개)")
                for entry in st.session_state.gratitude_entries[-3:]:
                    st.markdown(f"- {entry['content'][:50]}...")
            
            # 보고서 다운로드
            report_text = f"""
=== {datetime.now().strftime('%Y년 %m월 %d일')} 몰입 보고서 ===

[오늘의 질문]
{st.session_state.daily_question}

[몰입 통계]
- 총 몰입 시간: {st.session_state.total_minutes}분
- 완료 세션: {len(st.session_state.today_sessions)}개

[세부 기록]
{chr(10).join([f"- {s['time']} | {s['topic']} ({s['duration']}분)" for s in st.session_state.today_sessions]) if st.session_state.today_sessions else "- 기록 없음"}

[감사 일기]
{chr(10).join([f"- {e['content']}" for e in st.session_state.gratitude_entries]) if st.session_state.gratitude_entries else "- 기록 없음"}

[통찰과 아이디어]
{chr(10).join([f"- {i['content']}" for i in st.session_state.today_insights]) if st.session_state.today_insights else "- 기록 없음"}

---
Created by 통합 몰입 프로그램
"""
            st.download_button(
                label="📥 보고서 다운로드",
                data=report_text,
                file_name=f"몰입보고서_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.info("아직 기록이 없습니다. 몰입을 시작해보세요!")
    
    with tabs[7]:
        st.markdown("### 🔗 추천 영상")
        st.info("더 깊은 이해를 위한 YouTube 영상들")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 황농문 교수님")
            st.markdown("""
            📺 **몰입 이론 강의**
            - [몰입아카데미 YouTube 채널](https://youtube.com/@molipacademy?si=8GZv6-99UVO2-yYG)
            - 몰입의 즐거움
            - 의식의 무대
            - 천천히 생각하기
            """)
        
        with col2:
            st.markdown("#### 김종원 작가님")
            st.markdown("""
            📺 **사고력 강의**
            - [김종원 YouTube 채널](https://youtube.com/channel/UCR8ixAPYVq4uzN_w_gtGxOw?si=EE17IdSNpg_czM5u)
            - 하루 한 질문
            - 필사의 힘
            - 깊이 생각하기
            """)
        
        with col3:
            st.markdown("#### 김주환 교수님")
            st.markdown("""
            📺 **내면소통 강의**
            - [김주환 YouTube 채널](https://youtube.com/@joohankim?si=PZxhHus79e2-IObP)
            - 감사의 과학
            - 회복탄력성
            - 그릿의 힘
            """)
        
        st.markdown("---")
        st.info("📚 위 링크를 통해 더 깊은 이론과 실천법을 배워보세요!")

# 푸터
st.markdown("---")
st.markdown("""
*🌿 Created by 갯버들 | 황농문·김종원·김주환 님의 지혜를 존중하며*

본 프로그램은 교육적 목적으로 제작되었으며, 각 이론의 핵심 가치를 
실천적으로 체험할 수 있도록 구성했습니다.
""")
