# -*- coding: utf-8 -*-
# app.py - 통합 몰입 체험 프로그램 (완전판)
# Created by 갯버들
# 황농문, 김종원, 김주환 교수/작가님들의 지혜를 존중하며 통합
# Version: 4.0 - 모든 기능 통합

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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0
if 'today_insights' not in st.session_state:
    st.session_state.today_insights = []

# 오늘의 질문 생성 (김종원 방식)
daily_questions = [
    "오늘 나는 무엇을 위해 시간을 쓸 것인가?",
    "지금 이 순간, 나에게 가장 중요한 것은 무엇인가?",
    "오늘 내가 감사해야 할 세 가지는 무엇인가?",
    "어제보다 나은 오늘을 만들기 위해 무엇을 할 것인가?",
    "내가 진정으로 원하는 삶의 모습은 무엇인가?",
    "오늘 누군가에게 줄 수 있는 가치는 무엇인가?",
    "지금 이 일이 10년 후에도 중요할까?"
]

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
                    st.session_state.daily_question = random.choice(daily_questions)
                    st.rerun()
                else:
                    st.warning("닉네임을 입력해주세요")
else:
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
    
    # 오늘의 질문 표시 (김종원)
    st.markdown("---")
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown(f"### 📌 오늘의 질문")
    st.markdown(f"**{st.session_state.daily_question}**")
    st.markdown("*이 질문을 품고 하루를 보내세요. 3번 이상 떠올리며 깊이 생각해보세요.*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭 구성
    tabs = st.tabs(["📖 사용법", "🫁 호흡명상", "🎭 몰입실천", "📝 감사일기", "🏃 움직임", "📊 오늘의 기록"])
    
    # 호흡명상 완료 시 자동 탭 전환
    if st.session_state.breathing_complete and st.session_state.active_tab == 1:
        st.session_state.active_tab = 2
        st.session_state.breathing_complete = False
        st.rerun()
    
    with tabs[0]:
        st.markdown("""
        ### 🌟 통합 몰입 프로그램 사용법
        
        이 프로그램은 세 분의 지혜를 통합했습니다:
        - **황농문 교수님**: 이완된 집중, 의식의 무대
        - **김종원 작가님**: 하루 한 질문, 3번 이상 생각하기
        - **김주환 교수님**: 내면소통, 감사일기, 존2 운동
        
        #### 📅 일일 루틴
        
        **아침 (기상 직후)**
        1. 오늘의 질문 확인
        2. 호흡명상 (4-8 호흡법)
        3. 첫 몰입 세션 (5-10분)
        
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
        st.markdown("### 🫁 4-8 호흡명상 (황농문 교수님)")
        st.info("이완된 상태에서 천천히 생각하기의 시작")
        
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
                st.session_state.breathing_complete = True
                time.sleep(2)
                st.rerun()
    
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
            if st.button("🎬 무대 조명 켜기", type="primary", use_container_width=True):
                if topic:
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
                    elapsed = (datetime.now() - st.session_state.start_time).seconds // 60
                    st.session_state.today_sessions.append({
                        'topic': st.session_state.current_topic,
                        'duration': elapsed,
                        'time': datetime.now().strftime("%H:%M")
                    })
                    st.session_state.total_minutes += elapsed
                    st.session_state.is_running = False
                    st.rerun()
        
        # 몰입 진행 중 표시
        if st.session_state.is_running:
            st.markdown('<div class="stage-box">', unsafe_allow_html=True)
            st.markdown("## 🎭 의식의 무대")
            st.markdown(f"### 💡 {st.session_state.current_topic}")
            
            elapsed = (datetime.now() - st.session_state.start_time).seconds
            remaining = st.session_state.selected_duration * 60 - elapsed
            
            if remaining > 0:
                mins, secs = divmod(remaining, 60)
                st.markdown(f'<div class="timer-text">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                
                # 진행률 표시
                progress = elapsed / (st.session_state.selected_duration * 60)
                st.progress(progress)
                
                # 16시간 법칙 알림
                if elapsed == 60:
                    st.info("💡 기억하세요: 16시간 후 이 문제를 다시 생각해보세요!")
            else:
                st.balloons()
                st.success("🎉 몰입 완료! 자동 보고서를 생성합니다...")
                time.sleep(2)
                
                # 자동 보고서 생성
                elapsed_min = st.session_state.selected_duration
                st.session_state.today_sessions.append({
                    'topic': st.session_state.current_topic,
                    'duration': elapsed_min,
                    'time': datetime.now().strftime("%H:%M")
                })
                st.session_state.total_minutes += elapsed_min
                st.session_state.is_running = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 메모장
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 잡념 메모장")
            distraction = st.text_area(
                "떠오르는 잡념",
                height=150,
                placeholder="관객석으로 보낼 잡념을 적으세요",
                key="distraction_memo"
            )
        
        with col2:
            st.markdown("#### 💡 통찰 메모장")
            insight = st.text_area(
                "떠오른 아이디어",
                height=150,
                placeholder="3번 이상 생각한 내용을 적으세요",
                key="idea_memo"
            )
            if st.button("통찰 저장"):
                if insight:
                    st.session_state.today_insights.append({
                        'time': datetime.now().strftime("%H:%M"),
                        'content': insight
                    })
                    st.success("통찰이 저장되었습니다!")
    
    with tabs[3]:
        st.markdown("### 📝 감사일기 (김주환 교수님)")
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
    
    with tabs[5]:
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
            
            # 16시간 법칙 알림
            if st.session_state.today_sessions:
                first_session = st.session_state.today_sessions[0]
                reminder_time = datetime.now() + timedelta(hours=16)
                st.info(f"💡 16시간 법칙: 내일 {reminder_time.strftime('%H:%M')}에 '{first_session['topic']}'을 다시 생각해보세요!")
            
            # 보고서 다운로드
            report_text = f"""
=== {datetime.now().strftime('%Y년 %m월 %d일')} 몰입 보고서 ===

[오늘의 질문]
{st.session_state.daily_question}

[몰입 통계]
- 총 몰입 시간: {st.session_state.total_minutes}분
- 완료 세션: {len(st.session_state.today_sessions)}개

[세부 기록]
{chr(10).join([f"- {s['time']} | {s['topic']} ({s['duration']}분)" for s in st.session_state.today_sessions])}

[감사 일기]
{chr(10).join([f"- {e['content']}" for e in st.session_state.gratitude_entries])}

[통찰과 아이디어]
{chr(10).join([f"- {i['content']}" for i in st.session_state.today_insights])}

---
Created by 통합 몰입 프로그램
"""
            st.download_button(
                label="📥 보고서 다운로드",
                data=report_text,
                file_name=f"몰입보고서_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.info("아직 기록이 없습니다. 몰입을 시작해보세요!")

# 푸터
st.markdown("---")
st.markdown("""
*🌿 Created by 갯버들 | 황농문·김종원·김주환 님의 지혜를 존중하며*

본 프로그램은 교육적 목적으로 제작되었으며, 각 이론의 핵심 가치를 
실천적으로 체험할 수 있도록 구성했습니다.
""")
