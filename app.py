# -*- coding: utf-8 -*-
# app.py - 직장인 몰입 체험 프로그램 (안정화 버전)
# Created by 갯버들
# Based on 황농문 교수님's 몰입 이론
# Version: 3.1 - 탭 순서 최적화

import streamlit as st
import time
from datetime import datetime, timedelta
import random

# 페이지 설정
st.set_page_config(
    page_title="몰입 체험 프로그램",
    page_icon="🎯",
    layout="centered"
)

# 간단한 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1e3d59;
        padding: 1rem;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .sub-header {
        text-align: center;
        color: #5d6d7e;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stage-box {
        background: #f0f0f0;
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    .timer-text {
        font-size: 3rem;
        color: #ff6b6b;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화 (심플하게)
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

# 헤더
st.markdown('<h1 class="main-header">🎯 몰입 체험 프로그램</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">황농문 교수님의 몰입 이론 실천하기</p>', unsafe_allow_html=True)

# 이름 입력
if not st.session_state.user_name:
    with st.container():
        st.markdown("### 👋 환영합니다!")
        name = st.text_input("닉네임을 입력하세요", placeholder="예: 갯버들")
        if st.button("시작하기", type="primary"):
            if name:
                st.session_state.user_name = name
                st.rerun()
            else:
                st.warning("닉네임을 입력해주세요")
else:
    # 환영 메시지
    st.success(f"안녕하세요, {st.session_state.user_name}님! 오늘도 몰입을 실천해보세요.")
    
    # 탭 - 논리적 순서로 재배치
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 사용법",
        "🧘 호흡 명상",
        "🎭 몰입 실천",
        "📊 오늘의 기록"
    ])
    
    # 탭1: 사용법
    with tab1:
        st.markdown("""
        ### 📖 프로그램 사용법
        
        #### 1️⃣ 호흡 명상으로 시작
        - **호흡 명상** 탭에서 4-8 호흡법 실천
        - 4초 들이쉬고, 8초 내쉬기를 3번 반복
        - 몸과 마음을 이완시켜 몰입 준비
        
        #### 2️⃣ 몰입 실천
        - **몰입 실천** 탭에서 주제 입력
        - 5분부터 시작해서 점차 늘려가기
        - 타이머가 끝날 때까지 주제에만 집중
        
        #### 3️⃣ 핵심 원칙
        **🎭 의식의 무대**
        - 주제 = 무대 위의 주인공
        - 잡념 = 관객석으로 보내기
        
        **⏱️ 1초 원칙**
        - 잡념이 떠오르면 메모하고
        - 1초 안에 다시 주제로 돌아오기
        
        **💡 16시간 법칙**
        - 오늘 몰입한 내용은 잠재의식이 계속 처리
        - 내일 아침 다시 생각하면 새로운 아이디어 발견
        
        #### 4️⃣ 레벨 시스템
        - 초급 (0-100분): 기초 훈련
        - 중급 (100-300분): 심화 훈련
        - 고급 (300분+): 마스터 레벨
        """)
    
    # 탭2: 호흡 명상
    with tab2:
        st.markdown("### 🧘 4-8 호흡 명상")
        st.markdown("몰입 전, 마음을 준비하는 시간")
        
        st.info("""
        **이완된 집중을 위한 호흡법**
        1. 편안한 자세로 앉기
        2. 4초간 숨 들이쉬기
        3. 8초간 천천히 내쉬기
        4. 3회 반복
        """)
        
        if st.button("🧘 호흡 명상 시작", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 3회 반복
            for cycle in range(1, 4):
                # 들이쉬기
                for i in range(4):
                    status_text.text(f"🫁 {cycle}회차: 들이쉬기... {4-i}초")
                    progress_bar.progress((i+1)/12)
                    time.sleep(1)
                
                # 내쉬기
                for i in range(8):
                    status_text.text(f"😮‍💨 {cycle}회차: 내쉬기... {8-i}초")
                    progress_bar.progress((4+i+1)/12)
                    time.sleep(1)
                
                progress_bar.progress(0)
            
            status_text.text("✨ 호흡 명상 완료! 이제 몰입을 시작하세요.")
            st.success("몸과 마음이 이완되었습니다")
    
    # 탭3: 몰입 실천
    with tab3:
        st.markdown("### 🎭 의식의 무대")
        
        if not st.session_state.is_running:
            # 몰입 시작 전
            st.info("💡 먼저 호흡 명상으로 마음을 준비하면 더 깊은 몰입이 가능합니다")
            
            # 주제 입력
            topic = st.text_input(
                "오늘 집중할 주제를 입력하세요",
                placeholder="예: 프로젝트 기획, 문제 해결, 감사한 일 3가지"
            )
            
            # 시간 선택
            duration = st.select_slider(
                "몰입 시간 (분)",
                options=[5, 10, 15, 20, 25, 30],
                value=5
            )
            
            # 시작 버튼
            if st.button("🎬 몰입 시작", type="primary", use_container_width=True):
                if topic:
                    st.session_state.current_topic = topic
                    st.session_state.selected_duration = duration
                    st.session_state.is_running = True
                    st.session_state.start_time = time.time()
                    st.rerun()
                else:
                    st.error("주제를 입력해주세요")
            
            # 추천 주제
            with st.expander("💡 오늘의 추천 주제"):
                st.markdown("""
                **초급**
                - 오늘 감사한 일 3가지
                - 나의 장점 찾기
                - 이번 주 가장 중요한 일
                
                **중급**
                - 업무 개선 아이디어
                - 문제 해결 방안
                - 창의적 기획
                
                **고급**
                - 복잡한 프로젝트 설계
                - 전략적 의사결정
                - 혁신적 솔루션
                """)
        
        else:
            # 몰입 진행 중
            elapsed = time.time() - st.session_state.start_time
            remaining = (st.session_state.selected_duration * 60) - elapsed
            
            if remaining > 0:
                # 타이머 표시
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                
                st.markdown(f'<div class="timer-text">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                
                # 주제 표시
                st.markdown(f"""
                <div class="stage-box">
                    <h2>💡 {st.session_state.current_topic}</h2>
                    <p>이 주제에만 집중하세요</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 두 개의 메모장
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📝 잡념 메모장")
                    st.text_area(
                        "떠오르는 잡념",
                        height=100,
                        placeholder="관객석으로 보낼 잡념",
                        key="distraction_memo"
                    )
                
                with col2:
                    st.markdown("#### 💡 아이디어 메모장")
                    st.text_area(
                        "떠오르는 통찰",
                        height=100,
                        placeholder="주제 관련 아이디어",
                        key="idea_memo"
                    )
                
                # 종료 버튼
                if st.button("⏹️ 몰입 종료", type="secondary"):
                    # 세션 저장
                    actual_duration = int(elapsed / 60)
                    st.session_state.today_sessions.append({
                        "time": datetime.now().strftime("%H:%M"),
                        "topic": st.session_state.current_topic,
                        "duration": actual_duration
                    })
                    st.session_state.total_minutes += actual_duration
                    
                    # 상태 초기화
                    st.session_state.is_running = False
                    st.session_state.current_topic = ""
                    st.rerun()
                
                # 자동 새로고침
                time.sleep(1)
                st.rerun()
            
            else:
                # 시간 완료
                st.balloons()
                st.success("🎉 몰입 완료!")
                
                # 세션 저장
                st.session_state.today_sessions.append({
                    "time": datetime.now().strftime("%H:%M"),
                    "topic": st.session_state.current_topic,
                    "duration": st.session_state.selected_duration
                })
                st.session_state.total_minutes += st.session_state.selected_duration
                
                st.info(f"""
                💡 16시간 법칙
                
                '{st.session_state.current_topic}'에 대한 몰입이 완료되었습니다.
                잠재의식이 계속 처리할 것입니다.
                내일 아침 다시 생각해보세요!
                """)
                
                # 다시 시작 버튼
                if st.button("🔄 새로운 몰입", type="primary"):
                    st.session_state.is_running = False
                    st.session_state.current_topic = ""
                    st.rerun()
    
    # 탭4: 오늘의 기록
    with tab4:
        st.markdown("### 📊 오늘의 몰입 기록")
        
        if st.session_state.today_sessions:
            # 오늘 통계
            total_sessions = len(st.session_state.today_sessions)
            total_time = sum(s['duration'] for s in st.session_state.today_sessions)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("세션 수", f"{total_sessions}회")
            with col2:
                st.metric("총 시간", f"{total_time}분")
            with col3:
                level = "초급"
                if st.session_state.total_minutes >= 300:
                    level = "고급"
                elif st.session_state.total_minutes >= 100:
                    level = "중급"
                st.metric("레벨", level)
            
            # 세션 목록
            st.markdown("#### 오늘의 세션")
            for i, session in enumerate(st.session_state.today_sessions, 1):
                st.write(f"{i}. [{session['time']}] {session['topic']} - {session['duration']}분")
        else:
            st.info("아직 오늘의 몰입 기록이 없습니다. 첫 몰입을 시작해보세요!")
        
        # 진행도
        st.markdown("#### 레벨 진행도")
        progress = min(st.session_state.total_minutes / 100, 1.0)
        st.progress(progress)
        
        if st.session_state.total_minutes < 100:
            st.caption(f"중급까지 {100 - st.session_state.total_minutes}분 남았습니다")
        elif st.session_state.total_minutes < 300:
            st.caption(f"고급까지 {300 - st.session_state.total_minutes}분 남았습니다")
        else:
            st.caption("🏆 최고 레벨 달성!")

# 푸터
st.markdown("---")
st.markdown("*🌿 갯버들과 함께하는 몰입 여정*")
st.markdown("*Based on 황농문 교수님's 몰입 이론*")
