# app.py - 직장인 몰입 체험 프로그램 (의식의 무대 통합 버전)
# Created by 갯버들
# Based on 황농문 교수님's 몰입 이론
# GitHub: https://github.com/sjks007-art/immersion-program
# Version: 2.2 - 호흡명상 우선 배치 및 버그 수정

import streamlit as st
import time
from datetime import datetime, timedelta
import json
import os
import random

# 페이지 설정
st.set_page_config(
    page_title="몰입 체험 프로그램 - 의식의 무대",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 통합 스타일 (기존 + 무대)
st.markdown("""
<style>
    /* 기존 프로그램 스타일 */
    .main-header {
        text-align: center;
        color: #1e3d59;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .sub-header {
        text-align: center;
        color: #5d6d7e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .level-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-weight: bold;
        margin: 0.25rem;
    }
    
    .beginner { background-color: #d4edda; color: #155724; }
    .intermediate { background-color: #fff3cd; color: #856404; }
    .advanced { background-color: #f8d7da; color: #721c24; }
    
    /* 의식의 무대 스타일 추가 */
    .stage-container {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        position: relative;
        min-height: 400px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .spotlight {
        background: radial-gradient(circle at center, 
            rgba(255,255,200,0.9) 0%, 
            rgba(255,255,200,0.3) 30%, 
            transparent 70%);
        border-radius: 50%;
        padding: 60px;
        text-align: center;
        animation: fadeIn 2s ease-in;
        margin: 20px auto;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .focus-topic {
        color: #333;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255,255,200,0.8);
        animation: pulse 3s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .postit {
        background: #fffacd;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transform: rotate(-2deg);
        display: inline-block;
        transition: transform 0.2s;
    }
    
    .postit:hover {
        transform: rotate(0deg) scale(1.1);
    }
    
    .timer-display {
        font-size: 48px;
        color: #ffd700;
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255,215,0,0.5);
    }
    
    .stage-ready {
        text-align: center;
        color: #888;
        font-style: italic;
        animation: breathe 3s infinite;
    }
    
    @keyframes breathe {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .breath-circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: radial-gradient(circle, #87CEEB 0%, #4682B4 100%);
        margin: 20px auto;
        animation: breathing 4s infinite;
    }
    
    @keyframes breathing {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    
    .report-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_level' not in st.session_state:
    st.session_state.user_level = "초급"
if 'total_sessions' not in st.session_state:
    st.session_state.total_sessions = 0
if 'total_time' not in st.session_state:
    st.session_state.total_time = 0
if 'daily_sessions' not in st.session_state:
    st.session_state.daily_sessions = []
if 'stage_active' not in st.session_state:
    st.session_state.stage_active = False
if 'focus_topic' not in st.session_state:
    st.session_state.focus_topic = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'distractions' not in st.session_state:
    st.session_state.distractions = []
if 'focus_notes' not in st.session_state:
    st.session_state.focus_notes = ""
if 'duration' not in st.session_state:
    st.session_state.duration = 300  # 기본 5분
if 'breathing_active' not in st.session_state:
    st.session_state.breathing_active = False
if 'breath_cycle' not in st.session_state:
    st.session_state.breath_cycle = 0

# 응원 메시지 풀
ENCOURAGEMENT_MESSAGES = [
    "당신의 의식이 무대 위의 주인공입니다! 🌟",
    "조명이 비추는 곳에만 집중하세요 💡",
    "잡념은 관객석으로, 주제는 무대 중앙으로 🎭",
    "오늘도 몰입의 즐거움을 경험하세요! ✨",
    "1초 원칙을 기억하세요 - 주제에서 눈을 떼지 마세요 👁️"
]

# 헤더
st.markdown('<h1 class="main-header">🎯 몰입 체험 프로그램</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">황농문 교수님의 몰입 이론을 실천하는 공간</p>', unsafe_allow_html=True)

# 사용자 정보 입력
if not st.session_state.user_name:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("닉네임을 입력하세요", placeholder="예: 갯버들")
        if st.button("시작하기", type="primary", use_container_width=True):
            if name:
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("닉네임을 입력해주세요!")
else:
    # 환영 메시지
    st.success(f"환영합니다, {st.session_state.user_name}님! " + random.choice(ENCOURAGEMENT_MESSAGES))
    
    # 탭 메뉴 - 호흡명상을 첫 번째로 이동
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧘 호흡 명상",
        "🎭 의식의 무대", 
        "📝 오늘의 기록", 
        "📊 누적 통계",
        "💡 사용법"
    ])
    
    with tab1:
        st.markdown("### 🧘 4-8 호흡 명상")
        st.markdown("*몰입 전 마음을 준비하는 시간*")
        
        st.info("""
        **황농문 교수님의 이완된 집중법**
        
        긴장된 집중이 아닌 이완된 집중을 위해
        먼저 호흡을 통해 몸과 마음을 이완시킵니다.
        
        **4-8 호흡법**
        1. 4초간 숨을 들이쉬고
        2. 8초간 천천히 내쉽니다
        3. 3회 반복하여 이완 상태를 만듭니다
        """)
        
        if not st.session_state.breathing_active:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🧘 호흡 명상 시작", type="primary", use_container_width=True):
                    st.session_state.breathing_active = True
                    st.session_state.breath_cycle = 0
                    st.rerun()
        else:
            # 호흡 명상 진행
            breath_container = st.container()
            
            with breath_container:
                # 호흡 애니메이션 표시
                st.markdown('<div class="breath-circle"></div>', unsafe_allow_html=True)
                
                if st.session_state.breath_cycle < 3:
                    # 현재 사이클 표시
                    st.markdown(f"### 🌬️ {st.session_state.breath_cycle + 1}/3 회차")
                    
                    # 프로그레스 바로 호흡 가이드
                    progress_text = st.empty()
                    progress_bar = st.progress(0)
                    
                    # 들이쉬기 (4초)
                    for i in range(40):
                        progress_bar.progress(i / 40)
                        if i < 40:
                            progress_text.markdown(f"**🫁 들이쉬기... {4 - i//10}초**")
                        time.sleep(0.1)
                    
                    # 내쉬기 (8초)
                    for i in range(80):
                        progress_bar.progress(i / 80)
                        progress_text.markdown(f"**😮‍💨 내쉬기... {8 - i//10}초**")
                        time.sleep(0.1)
                    
                    # 다음 사이클로
                    st.session_state.breath_cycle += 1
                    st.rerun()
                    
                else:
                    # 명상 완료
                    st.balloons()
                    st.success("✨ 호흡 명상이 완료되었습니다!")
                    st.info("이제 이완된 상태로 '의식의 무대'에서 몰입을 시작해보세요.")
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("✅ 완료", type="primary", use_container_width=True):
                            st.session_state.breathing_active = False
                            st.session_state.breath_cycle = 0
                            st.rerun()
    
    with tab2:
        st.markdown("### 🎭 의식의 무대")
        st.markdown("*주제에 조명을 비추고, 잡념은 관객석으로*")
        
        # 호흡 명상 유도
        if st.session_state.total_sessions == 0:
            st.warning("💡 Tip: 먼저 '호흡 명상'으로 마음을 준비하면 더 깊은 몰입이 가능합니다.")
        
        if not st.session_state.stage_active:
            # 몰입 시작 전
            st.markdown("#### 🎬 무대 준비")
            
            # 레벨별 주제 추천
            level_topics = {
                "초급": ["오늘 감사한 일 3가지", "나의 장점 찾기", "이번 주 목표"],
                "중급": ["업무 개선 아이디어", "문제 해결 방법", "창의적 기획"],
                "고급": ["복잡한 프로젝트 설계", "전략적 의사결정", "혁신적 솔루션"]
            }
            
            with st.expander("💡 오늘의 추천 주제"):
                topics = level_topics.get(st.session_state.user_level, level_topics["초급"])
                for topic in topics:
                    st.write(f"• {topic}")
            
            # 주제 입력
            topic_input = st.text_input(
                "집중할 주제를 입력하세요:",
                placeholder="예: 프로젝트 아이디어 구상",
                key="topic_input_field"
            )
            
            # 시간 선택
            col1, col2 = st.columns(2)
            with col1:
                duration_choice = st.selectbox(
                    "몰입 시간:",
                    options=[5, 10, 15, 20, 25, 30],
                    index=0,
                    format_func=lambda x: f"{x}분",
                    key="duration_select"
                )
            
            with col2:
                # 버튼 클릭 처리
                if st.button("🎭 무대 조명 켜기", type="primary", use_container_width=True):
                    if topic_input and topic_input.strip():
                        # 세션 상태 업데이트
                        st.session_state.focus_topic = topic_input
                        st.session_state.stage_active = True
                        st.session_state.start_time = time.time()
                        st.session_state.duration = duration_choice * 60
                        st.session_state.distractions = []
                        st.session_state.focus_notes = ""
                        st.rerun()
                    else:
                        st.error("⚠️ 집중할 주제를 입력해주세요!")
            
            # 무대 미리보기
            st.markdown("""
            <div class="stage-container">
                <div class="stage-ready">
                    <h3>🎭 무대가 준비되어 있습니다</h3>
                    <p>주제를 정하고 조명을 켜면<br>당신의 의식이 무대의 주인공이 됩니다</p>
                    <br>
                    <p style="font-size: 0.9em;">💡 Tip: 짧은 시간부터 시작하세요</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # 몰입 진행 중
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                remaining = st.session_state.duration - elapsed
                
                if remaining > 0:
                    # 타이머 표시
                    mins, secs = divmod(int(remaining), 60)
                    timer_display = f"{mins:02d}:{secs:02d}"
                    
                    # 무대 표시
                    st.markdown(f"""
                    <div class="stage-container">
                        <div class="timer-display">{timer_display}</div>
                        <div class="spotlight">
                            <div class="focus-topic">
                                💡 {st.session_state.focus_topic}
                            </div>
                        </div>
                        <p style="text-align: center; color: #666; margin-top: 20px;">
                            무대 위의 주제에만 집중하세요
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 잡념 처리 섹션
                    st.markdown("#### 🎫 잡념 보관함")
                    st.markdown("*무대에 올라온 관객(잡념)을 관객석으로 보내세요*")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        distraction = st.text_input(
                            "떠오른 잡념:",
                            key=f"distraction_input_{len(st.session_state.distractions)}",
                            placeholder="잡념을 적고 Enter 또는 보관 버튼"
                        )
                    with col2:
                        if st.button("📌 보관", key="save_distraction"):
                            if distraction and distraction.strip():
                                st.session_state.distractions.append(distraction)
                                st.rerun()
                    
                    # 보관된 잡념 표시
                    if st.session_state.distractions:
                        st.markdown("**관객석으로 보낸 잡념들:**")
                        cols = st.columns(3)
                        for i, d in enumerate(st.session_state.distractions):
                            with cols[i % 3]:
                                st.markdown(f'<div class="postit">📌 {d}</div>', 
                                          unsafe_allow_html=True)
                    
                    # 생각 기록
                    st.markdown("#### 📝 몰입 노트")
                    notes_input = st.text_area(
                        "주제에 대한 생각을 자유롭게 적으세요:",
                        value=st.session_state.focus_notes,
                        height=150,
                        placeholder="판단하지 말고 떠오르는 대로...",
                        key="notes_area_input"
                    )
                    st.session_state.focus_notes = notes_input
                    
                    # 종료 버튼
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("🏁 몰입 종료", type="secondary", use_container_width=True):
                            # 몰입 완료 처리
                            actual_duration = int((time.time() - st.session_state.start_time) / 60)
                            session_data = {
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "time": datetime.now().strftime("%H:%M"),
                                "topic": st.session_state.focus_topic,
                                "duration": actual_duration,
                                "distractions": len(st.session_state.distractions),
                                "distraction_list": st.session_state.distractions.copy(),
                                "notes": st.session_state.focus_notes,
                                "level": st.session_state.user_level
                            }
                            
                            st.session_state.daily_sessions.append(session_data)
                            st.session_state.total_sessions += 1
                            st.session_state.total_time += actual_duration
                            
                            # 레벨 업데이트
                            if st.session_state.total_time >= 300:
                                st.session_state.user_level = "고급"
                            elif st.session_state.total_time >= 100:
                                st.session_state.user_level = "중급"
                            
                            # 세션 종료
                            st.session_state.stage_active = False
                            st.session_state.start_time = None
                            st.rerun()
                    
                    # 자동 새로고침
                    time.sleep(1)
                    st.rerun()
                
                else:
                    # 시간 초과 - 몰입 완료
                    st.balloons()
                    
                    # 세션 저장
                    duration_mins = int(st.session_state.duration / 60)
                    session_data = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "time": datetime.now().strftime("%H:%M"),
                        "topic": st.session_state.focus_topic,
                        "duration": duration_mins,
                        "distractions": len(st.session_state.distractions),
                        "distraction_list": st.session_state.distractions.copy(),
                        "notes": st.session_state.focus_notes,
                        "level": st.session_state.user_level
                    }
                    
                    st.session_state.daily_sessions.append(session_data)
                    st.session_state.total_sessions += 1
                    st.session_state.total_time += duration_mins
                    
                    # 레벨 업데이트
                    if st.session_state.total_time >= 300:
                        st.session_state.user_level = "고급"
                    elif st.session_state.total_time >= 100:
                        st.session_state.user_level = "중급"
                    
                    # 완료 메시지
                    st.success("🎉 몰입 세션이 완료되었습니다!")
                    
                    # 결과 표시
                    st.markdown("### 🎭 무대를 내리며")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("몰입 시간", f"{duration_mins}분")
                    with col2:
                        st.metric("처리한 잡념", f"{len(st.session_state.distractions)}개")
                    with col3:
                        st.metric("현재 레벨", st.session_state.user_level)
                    
                    if st.session_state.focus_notes:
                        with st.expander("📝 오늘의 몰입 노트 보기"):
                            st.write(st.session_state.focus_notes)
                    
                    if st.session_state.distractions:
                        with st.expander("🎫 관객석으로 보낸 잡념들"):
                            for d in st.session_state.distractions:
                                st.write(f"• {d}")
                    
                    # 16시간 후 알림
                    st.info(f"""
                    💡 **황농문 교수님의 16시간 법칙**
                    
                    오늘 집중한 '{st.session_state.focus_topic[:30]}'은(는) 
                    잠재의식이 계속 처리합니다.
                    내일 아침에 다시 생각해보면 새로운 아이디어가 떠오를 거예요!
                    """)
                    
                    # 초기화 버튼
                    if st.button("🔄 새로운 몰입 시작", type="primary", use_container_width=True):
                        st.session_state.stage_active = False
                        st.session_state.focus_topic = ""
                        st.session_state.start_time = None
                        st.rerun()
    
    with tab3:
        st.markdown("### 📝 오늘의 몰입 기록")
        
        if st.session_state.daily_sessions:
            today = datetime.now().strftime("%Y-%m-%d")
            today_sessions = [s for s in st.session_state.daily_sessions if s['date'] == today]
            
            if today_sessions:
                st.success(f"오늘 {len(today_sessions)}번의 몰입을 완료했습니다!")
                
                for i, session in enumerate(today_sessions, 1):
                    with st.expander(f"세션 {i}: {session['time']} - {session['topic'][:30]}..."):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**몰입 시간:** {session['duration']}분")
                            st.write(f"**레벨:** {session['level']}")
                        with col2:
                            st.write(f"**처리한 잡념:** {session['distractions']}개")
                        
                        if session.get('notes'):
                            st.write("**노트:**")
                            st.write(session['notes'])
                        
                        if session.get('distraction_list'):
                            st.write("**잡념들:**")
                            for d in session['distraction_list']:
                                st.write(f"• {d}")
            else:
                st.info("오늘의 몰입 기록이 아직 없습니다.")
        else:
            st.info("첫 몰입을 시작해보세요!")
    
    with tab4:
        st.markdown("### 📊 누적 통계")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 몰입 시간", f"{st.session_state.total_time}분")
        with col2:
            st.metric("총 세션 수", f"{st.session_state.total_sessions}회")
        with col3:
            level_color = {"초급": "🟢", "중급": "🟡", "고급": "🔴"}
            st.metric("현재 레벨", f"{level_color.get(st.session_state.user_level, '🟢')} {st.session_state.user_level}")
        
        # 레벨 진행도
        st.markdown("#### 레벨 진행도")
        if st.session_state.user_level == "초급":
            progress = min(st.session_state.total_time / 100, 1.0)
            st.progress(progress)
            st.caption(f"중급까지 {max(0, 100 - st.session_state.total_time)}분 남았습니다")
        elif st.session_state.user_level == "중급":
            progress = min((st.session_state.total_time - 100) / 200, 1.0)
            st.progress(progress)
            st.caption(f"고급까지 {max(0, 300 - st.session_state.total_time)}분 남았습니다")
        else:
            st.progress(1.0)
            st.caption("🏆 최고 레벨 달성!")
        
        # 주간 목표
        st.markdown("#### 주간 목표")
        weekly_goal = 150  # 주 150분 목표
        this_week_time = sum(
            s['duration'] for s in st.session_state.daily_sessions 
            if datetime.strptime(s['date'], "%Y-%m-%d").isocalendar()[1] == datetime.now().isocalendar()[1]
        )
        
        st.progress(min(this_week_time / weekly_goal, 1.0))
        st.caption(f"이번 주 {this_week_time}분 / 목표 {weekly_goal}분")
        
        # 몰입 달력 (간단한 통계)
        if st.session_state.daily_sessions:
            st.markdown("#### 최근 7일 몰입 현황")
            last_7_days = {}
            today = datetime.now()
            
            for i in range(7):
                date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                day_sessions = [s for s in st.session_state.daily_sessions if s['date'] == date]
                if day_sessions:
                    total_mins = sum(s['duration'] for s in day_sessions)
                    last_7_days[date] = f"{len(day_sessions)}회, {total_mins}분"
                else:
                    last_7_days[date] = "휴식"
            
            for date, info in sorted(last_7_days.items(), reverse=True):
                st.write(f"• {date}: {info}")
    
    with tab5:
        st.markdown("""
        ### 💡 몰입 프로그램 사용법
        
        #### 🧘 호흡 명상 먼저!
        **이완된 집중**을 위해 호흡 명상으로 시작하세요.
        - 긴장을 풀고 이완된 상태 만들기
        - 4초 들이쉬고 8초 내쉬기 3회
        - 몰입의 질이 완전히 달라집니다
        
        #### 🎭 의식의 무대란?
        황농문 교수님의 '의식의 무대' 비유를 실제로 구현한 기능입니다.
        - **무대**: 현재 집중해야 할 주제
        - **조명**: 의식의 집중
        - **관객석**: 떠오르는 잡념들을 보관하는 곳
        
        #### 📌 1초 원칙
        잡념이 떠오르면 싸우지 말고:
        1. 빠르게 포스트잇(잡념 보관함)에 적기
        2. 다시 주제로 돌아오기
        3. 1초도 주제에서 떼지 않기
        
        #### ⏰ 왜 시간을 정하나요?
        1. **심리적 안정감**: 끝이 정해져 있으면 부담 없이 시작
        2. **점진적 성장**: 5분 → 10분 → 30분으로 늘려가기
        3. **일상 적용**: 직장에서 짬짬이 활용 가능
        
        #### 🎯 효과적인 사용법
        1. **호흡 명상으로 시작**: 이완 상태 만들기
        2. **짧게 시작**: 5분부터 천천히
        3. **구체적 주제**: 막연한 것보다 구체적인 주제
        4. **매일 실천**: 꾸준함이 가장 중요
        5. **16시간 법칙**: 다음날 아침 다시 생각하기
        
        #### 📊 레벨 시스템
        - **초급 (0-100분)**: 기초 몰입 훈련
        - **중급 (100-300분)**: 심화 몰입 훈련  
        - **고급 (300분+)**: 마스터 레벨
        
        ---
        *Created by 갯버들 | Based on 황농문 교수님's 몰입 이론*
        """)

# 푸터
st.markdown("---")
st.markdown("*🌿 갯버들과 함께하는 몰입 여정 | [GitHub](https://github.com/sjks007-art/immersion-program)*")
