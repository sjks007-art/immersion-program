# -*- coding: utf-8 -*-
# app.py - K-몰입 프로그램 (황농문 교수 16시간 이론)
# Created by 갯버들 (한승희)
# Based on Prof. Hwang Nong-Moon's Immersion Theory
# Seoul National University Honorary Professor
# 
# 핵심 이론:
# - 16시간 이상 이미지 트레이닝
# - Work Hard → Think Hard 패러다임 전환
# - 릴렉싱 상태에서의 지속적 몰입
#
# GitHub: https://github.com/sjks007-art/immersion-program
# Version: 5.0 - 황농문 교수님 전용 최종판
# Date: 2025.09.11

import streamlit as st
import time
from datetime import datetime, timedelta
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="K-몰입 프로그램 | 황농문 교수 16시간 이론",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 (황농문 교수님 이론 특화)
st.markdown("""
<style>
    /* 메인 헤더 - 교수님 이론 강조 */
    .main-header {
        text-align: center;
        color: #1e3d59;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 2.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #5d6d7e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* 황농문 이론 특별 박스 */
    .hwang-theory-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .hwang-theory-box h3, .hwang-theory-box h4 {
        color: white !important;
    }
    
    /* 의식의 무대 스타일 */
    .stage-container {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        min-height: 400px;
        border: 2px solid #764ba2;
    }
    
    .spotlight {
        background: radial-gradient(circle at center, 
            rgba(255,255,200,0.9) 0%, 
            rgba(255,255,200,0.3) 30%, 
            transparent 70%);
        border-radius: 50%;
        padding: 60px;
        text-align: center;
        margin: 20px auto;
        animation: pulse 3s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .focus-topic {
        color: #333;
        font-size: 28px;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255,255,200,0.8);
    }
    
    .timer-display {
        font-size: 56px;
        color: #ffd700;
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255,215,0,0.7);
        font-family: 'Courier New', monospace;
    }
    
    .think-hard-badge {
        background: #ffd700;
        color: #1a1a2e;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: #f0f2f6;
        border-left: 4px solid #4a90e2;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .postit {
        background: #fffacd;
        padding: 12px;
        margin: 8px;
        border-radius: 5px;
        box-shadow: 3px 3px 7px rgba(0,0,0,0.2);
        display: inline-block;
        transform: rotate(-1deg);
        transition: transform 0.2s;
    }
    
    .postit:hover {
        transform: rotate(0deg) scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'stage_active' not in st.session_state:
    st.session_state.stage_active = False
if 'focus_topic' not in st.session_state:
    st.session_state.focus_topic = ""
if 'distractions' not in st.session_state:
    st.session_state.distractions = []
if 'immersion_time' not in st.session_state:
    st.session_state.immersion_time = 10
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'breathing_active' not in st.session_state:
    st.session_state.breathing_active = False
if 'total_sessions' not in st.session_state:
    st.session_state.total_sessions = 0
if 'total_time' not in st.session_state:
    st.session_state.total_time = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'think_hard_points' not in st.session_state:
    st.session_state.think_hard_points = 0

# 헤더
st.markdown('<h1 class="main-header">🎯 K-몰입 프로그램</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">황농문 서울대 명예교수의 16시간 몰입 이론 실천 플랫폼<br><b>"Work Hard에서 Think Hard로!"</b></div>', unsafe_allow_html=True)

# 사용자 이름 입력
if not st.session_state.user_name:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="hwang-theory-box">
        <h3 style='text-align:center;'>황농문 교수님의 몰입아카데미</h3>
        <p style='text-align:center;'>16시간 이미지 트레이닝으로<br>당신의 잠재력을 깨우세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("🙋 이름을 입력해주세요", placeholder="예: 갯버들")
        if st.button("Think Hard 시작하기", use_container_width=True, type="primary"):
            if name:
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("이름을 입력해주세요!")
else:
    # 환영 메시지와 Think Hard 점수
    col1, col2 = st.columns([3,1])
    with col1:
        st.success(f"👋 {st.session_state.user_name}님, 오늘도 16시간 몰입에 도전하세요!")
    with col2:
        st.markdown(f'<div class="think-hard-badge">Think Hard: {st.session_state.think_hard_points}점</div>', unsafe_allow_html=True)
    
    # 황농문 교수님 명언
    quotes = [
        "Work Hard가 아닌 Think Hard가 성공의 열쇠입니다",
        "16시간 동안 문제를 품고 있으면 반드시 해결됩니다",
        "몰입은 긴장이 아닌 릴렉싱 상태에서 시작됩니다",
        "1초 안에 잡념을 처리하고 다시 집중하세요",
        "실제 작업은 짧아도, 생각은 16시간 이상 지속되어야 합니다"
    ]
    import random
    selected_quote = random.choice(quotes)
    
    st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#f0f2f6; border-radius:10px; margin-bottom:20px;'>
    <i>"{selected_quote}"</i><br>
    <b>- 황농문 서울대 명예교수 -</b>
    </div>
    """, unsafe_allow_html=True)
    
    # 탭 생성 (황농문 이론 중심)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 황농문 이론", 
        "🧘 릴렉싱 준비", 
        "🎭 의식의 무대", 
        "📊 몰입 기록",
        "🎓 몰입아카데미"
    ])
    
    # 탭1: 황농문 이론
    with tab1:
        st.markdown("### 🎓 황농문 교수님의 16시간 몰입 이론")
        
        st.markdown("""
        <div class="hwang-theory-box">
        <h3>🔑 핵심 이론: Work Hard → Think Hard</h3>
        <p>성공의 비결은 '열심히 일하는 것'이 아니라 '깊이 생각하는 것'입니다.<br>
        16시간 이상 문제를 품고 있으면, 잠재의식이 해답을 찾아냅니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📌 16시간 이미지 트레이닝
            
            **골프 선수의 예:**
            - 실제 연습: 3-4시간
            - 이미지 트레이닝: 16시간+
            - 결과: 월등한 실력 향상
            
            **기업인의 적용:**
            - 회의 시간: 2-3시간
            - 문제 몰입: 16시간+
            - 결과: 창의적 해결책 발견
            """)
        
        with col2:
            st.markdown("""
            #### 📌 몰입의 3대 원칙
            
            **1. Think Hard 원칙**
            - 단순 노력 ❌
            - 깊은 사고 ⭕
            
            **2. 16시간 법칙**
            - 지속적 이미지 트레이닝
            - 잠재의식 활용
            
            **3. 1초 처리 원칙**
            - 잡념 즉시 처리
            - 의식의 무대 유지
            """)
        
        st.markdown("""
        <div class="info-box">
        <h4>💡 실천 방법</h4>
        <ol>
        <li><b>릴렉싱</b>: 긴장을 풀고 편안한 상태 만들기</li>
        <li><b>집중</b>: 의식의 무대에 한 가지만 올리기</li>
        <li><b>지속</b>: 16시간 동안 계속 생각하기</li>
        <li><b>기록</b>: 떠오르는 아이디어 즉시 메모</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # 탭2: 릴렉싱 준비
    with tab2:
        st.markdown("### 🧘 릴렉싱 - 몰입의 시작")
        
        st.markdown("""
        <div class="hwang-theory-box">
        <h4>황농문 교수님의 릴렉싱 이론</h4>
        <p>"진정한 몰입은 긴장이 아닌 이완에서 시작됩니다.<br>
        릴렉싱 상태에서 뇌는 최고의 성능을 발휘합니다."</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        #### 🌬️ 4-8 호흡법
        - **4초** 동안 천천히 들이쉬기
        - **8초** 동안 천천히 내쉬기
        - **3회** 반복으로 완벽한 릴렉싱
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 릴렉싱 시작", use_container_width=True, type="primary", key="breath_start"):
                st.session_state.breathing_active = True
        
        if st.session_state.breathing_active:
            breathing_container = st.empty()
            
            for round in range(1, 4):
                # 들이쉬기
                for i in range(4, 0, -1):
                    breathing_container.markdown(f"""
                    <div style='text-align:center; padding:50px; background:#e3f2fd; border-radius:10px;'>
                        <h1 style='color:#4a90e2; font-size:48px;'>🫁 들이쉬기</h1>
                        <h2 style='font-size:72px;'>{i}</h2>
                        <p style='font-size:20px;'>라운드 {round}/3</p>
                        <p>코로 천천히, 깊게...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                
                # 내쉬기
                for i in range(8, 0, -1):
                    breathing_container.markdown(f"""
                    <div style='text-align:center; padding:50px; background:#e8f5e9; border-radius:10px;'>
                        <h1 style='color:#28a745; font-size:48px;'>💨 내쉬기</h1>
                        <h2 style='font-size:72px;'>{i}</h2>
                        <p style='font-size:20px;'>라운드 {round}/3</p>
                        <p>입으로 천천히, 모두...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
            
            breathing_container.markdown("""
            <div class="success-box">
            <h3 style='text-align:center;'>✅ 완벽한 릴렉싱 상태!</h3>
            <p style='text-align:center;'>황농문 교수님: "이제 당신의 뇌는 최고의 몰입 준비가 되었습니다"<br>
            의식의 무대로 이동하여 Think Hard를 시작하세요!</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.breathing_active = False
            st.session_state.think_hard_points += 10
            time.sleep(3)
            st.rerun()
    
    # 탭3: 의식의 무대
    with tab3:
        st.markdown("### 🎭 의식의 무대 - Think Hard 실천")
        
        # 모드 선택 (황농문 교수님 타겟별)
        mode = st.radio("몰입 모드 선택", 
                       ["🏢 기업 임원 모드", "⛳ 프로 선수 모드", "📚 수험생 모드", "🎯 일반 몰입"],
                       horizontal=True)
        
        mode_tips = {
            "🏢 기업 임원 모드": "💡 회의 후에도 16시간 동안 문제를 계속 생각하세요",
            "⛳ 프로 선수 모드": "💡 실제 운동 외 16시간은 이미지 트레이닝하세요",
            "📚 수험생 모드": "💡 공부 후에도 16시간 동안 내용이 머릿속에서 정리됩니다",
            "🎯 일반 몰입": "💡 어떤 주제든 16시간 품고 있으면 답이 나옵니다"
        }
        
        st.info(mode_tips[mode])
        
        # 주제 입력
        topic = st.text_input("🎯 오늘의 Think Hard 주제", 
                             placeholder="한 가지 주제만 선택하세요. 예: 신제품 전략, 스윙 개선, 수학 문제...")
        
        # 시간 설정
        col1, col2 = st.columns(2)
        with col1:
            minutes = st.selectbox("⏰ 집중 몰입 시간 (분)", 
                                  [5, 10, 15, 20, 25, 30, 45, 60], 
                                  index=2)
        
        with col2:
            if st.button("🔦 의식의 무대 조명 ON", use_container_width=True, type="primary", key="stage_start"):
                if topic:
                    st.session_state.stage_active = True
                    st.session_state.focus_topic = topic
                    st.session_state.immersion_time = minutes
                    st.session_state.timer_running = True
                else:
                    st.error("Think Hard할 주제를 입력해주세요!")
        
        # 무대 활성화 시
        if st.session_state.stage_active:
            st.markdown('<div class="stage-container">', unsafe_allow_html=True)
            
            # 스포트라이트 효과
            st.markdown(f"""
            <div class="spotlight">
                <div class="focus-topic">🎯 {st.session_state.focus_topic}</div>
                <p style="color:#666; margin-top:10px;">의식의 무대에 오른 주제</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 타이머
            if st.session_state.timer_running:
                timer_placeholder = st.empty()
                progress_bar = st.progress(0)
                end_time = time.time() + (st.session_state.immersion_time * 60)
                total_seconds = st.session_state.immersion_time * 60
                
                while time.time() < end_time and st.session_state.timer_running:
                    remaining = int(end_time - time.time())
                    elapsed = total_seconds - remaining
                    progress = elapsed / total_seconds
                    
                    mins, secs = divmod(remaining, 60)
                    timer_placeholder.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', 
                                              unsafe_allow_html=True)
                    progress_bar.progress(progress)
                    time.sleep(1)
                
                if st.session_state.timer_running:
                    st.balloons()
                    st.markdown("""
                    <div class="hwang-theory-box">
                    <h3 style='text-align:center;'>🎉 집중 세션 완료!</h3>
                    <p style='text-align:center;'>황농문 교수님: "이제부터가 진짜입니다!<br>
                    16시간 동안 이 주제를 계속 생각하세요.<br>
                    걸을 때도, 밥 먹을 때도, 잠들기 전에도..."</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.total_sessions += 1
                    st.session_state.total_time += st.session_state.immersion_time
                    st.session_state.think_hard_points += minutes * 2
                    st.session_state.timer_running = False
                    st.session_state.stage_active = False
            
            # 잡념 보관함 (1초 원칙)
            st.markdown("#### 💭 잡념 보관함 (1초 처리)")
            col1, col2 = st.columns([3,1])
            with col1:
                distraction = st.text_input("떠오르는 잡념을 1초 안에 여기에!", key="distraction_input")
            with col2:
                if st.button("📌 보관", key="save_distraction"):
                    if distraction:
                        st.session_state.distractions.append(distraction)
                        st.success("1초 처리 완료!")
            
            # 보관된 잡념 표시
            if st.session_state.distractions:
                st.markdown("**관객석으로 보낸 잡념들:**")
                for d in st.session_state.distractions:
                    st.markdown(f'<div class="postit">💭 {d}</div>', unsafe_allow_html=True)
            
            # Think Hard 노트
            st.markdown("#### 📝 Think Hard 노트")
            notes = st.text_area("떠오르는 아이디어를 자유롭게 기록", height=150, 
                               placeholder="판단하지 말고, 떠오르는 대로 적으세요...")
            
            # 16시간 가이드
            st.markdown("""
            <div class="hwang-theory-box">
            <h4>🎯 16시간 이미지 트레이닝 가이드</h4>
            <p>지금부터 16시간 동안:</p>
            <ul style="color:white;">
            <li>🚶 걸으면서도 → 이 주제 생각</li>
            <li>🍽️ 식사하면서도 → 이 주제 상상</li>
            <li>🚿 샤워하면서도 → 이 주제 탐구</li>
            <li>🛏️ 잠들기 전 5분 → 이 주제 정리</li>
            <li>🌅 일어나자마자 → 새로운 아이디어 확인</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # 종료 버튼
            if st.button("🛑 세션 종료 (16시간 시작)", type="secondary", use_container_width=True):
                st.session_state.stage_active = False
                st.session_state.timer_running = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭4: 몰입 기록
    with tab4:
        st.markdown("### 📊 나의 Think Hard 기록")
        
        # 통계 카드
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 세션", f"{st.session_state.total_sessions}회")
        
        with col2:
            st.metric("총 몰입 시간", f"{st.session_state.total_time}분")
        
        with col3:
            st.metric("Think Hard 점수", f"{st.session_state.think_hard_points}점")
        
        with col4:
            if st.session_state.total_sessions > 0:
                avg_time = st.session_state.total_time / st.session_state.total_sessions
                st.metric("평균 몰입", f"{avg_time:.1f}분")
            else:
                st.metric("평균 몰입", "0분")
        
        # Think Hard 레벨
        st.markdown("#### 🏆 Think Hard 레벨")
        
        points = st.session_state.think_hard_points
        if points < 100:
            level = "🌱 Think Hard 입문"
            next_level = f"중급까지 {100-points}점"
            progress = points / 100
        elif points < 500:
            level = "🌿 Think Hard 중급"
            next_level = f"고급까지 {500-points}점"
            progress = (points - 100) / 400
        elif points < 1000:
            level = "🌳 Think Hard 고급"
            next_level = f"마스터까지 {1000-points}점"
            progress = (points - 500) / 500
        else:
            level = "👑 Think Hard 마스터"
            next_level = "황농문 교수님도 인정하는 수준!"
            progress = 1.0
        
        st.info(f"현재 레벨: **{level}**")
        st.progress(progress)
        st.caption(f"다음 레벨: {next_level}")
        
        # 16시간 추적
        if st.session_state.total_sessions > 0:
            last_session_time = datetime.now()
            next_review_time = last_session_time + timedelta(hours=16)
            
            st.markdown(f"""
            <div class="hwang-theory-box">
            <h4>💡 16시간 법칙 추적</h4>
            <p><b>다음 아이디어 확인 시간:</b><br>
            {next_review_time.strftime('%m월 %d일 %H시 %M분')}</p>
            <p>황농문 교수님: "16시간 후, 놀라운 아이디어가 떠오를 것입니다"</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 예상 성과
            st.markdown("""
            #### 📈 예상 몰입 성과
            """)
            
            total_immersion_hours = (st.session_state.total_time * 16) / 60
            st.markdown(f"""
            - **실제 집중 시간**: {st.session_state.total_time}분
            - **예상 이미지 트레이닝**: {total_immersion_hours:.1f}시간
            - **Think Hard 효율**: {min(100, points/10):.1f}%
            """)
    
    # 탭5: 몰입아카데미
    with tab5:
        st.markdown("### 🎓 황농문 교수님 몰입아카데미")
        
        st.markdown("""
        <div class="hwang-theory-box">
        <h3>몰입아카데미 1:1 코칭 프로그램</h3>
        <p>황농문 서울대 명예교수가 직접 지도하는<br>
        진정한 Think Hard 마스터 과정</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📚 주요 저서
            - 『몰입』
            - 『몰입, 두 번째 이야기』
            - 『공부하는 힘』
            
            #### 🏢 기업 강연
            - 삼성, LG, SK 등 대기업
            - 영림원 차세대리더포럼
            - CEO 혁신교육
            """)
        
        with col2:
            st.markdown("""
            #### 🎯 코칭 프로그램
            - 1:1 개인 몰입 코칭
            - 기업 임원 몰입 교육
            - 프로 선수 멘탈 트레이닝
            - 수험생 몰입 학습법
            
            #### 📺 YouTube
            "황농문의 몰입 이야기" 채널 운영
            """)
        
        st.markdown("""
        <div class="info-box">
        <h4>💬 교수님 말씀</h4>
        <p>"50년간 아무도 풀지 못한 난제들을 몰입으로 해결했습니다.<br>
        여러분도 Think Hard를 통해 불가능을 가능으로 만들 수 있습니다.<br>
        성공의 비결은 Work Hard가 아닌 Think Hard입니다."</p>
        <p style="text-align:right;"><b>- 황농문 서울대 명예교수 -</b></p>
        </div>
        """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:20px;'>
<b>🎓 Based on Prof. Hwang Nong-Moon's 16-Hour Immersion Theory</b><br>
Seoul National University Honorary Professor<br>
Author of "Immersion" Series | Founder of Immersion Academy<br><br>
<b>🌿 Developed by 갯버들 (한승희)</b><br>
K-Immersion Program | Global Launch 2025<br>
📧 Contact: immersion.program@gmail.com<br><br>
<i>"From Work Hard to Think Hard"</i>
</div>
""", unsafe_allow_html=True)
