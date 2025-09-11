# -*- coding: utf-8 -*-
# app.py - 직장인 몰입 체험 프로그램 (최종 수정판)
# Created by 갯버들
# Based on 황농문 교수님's 몰입 이론
# GitHub: https://github.com/sjks007-art/immersion-program
# Version: 3.0 - 모든 버그 수정 및 UI 개선

import streamlit as st
import time
from datetime import datetime, timedelta
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="몰입 체험 프로그램 - 의식의 무대",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일
st.markdown("""
<style>
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
    
    .stage-container {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        min-height: 400px;
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
    }
    
    .focus-topic {
        color: #333;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255,255,200,0.8);
    }
    
    .timer-display {
        font-size: 48px;
        color: #ffd700;
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255,215,0,0.5);
    }
    
    .postit {
        background: #fffacd;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        display: inline-block;
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

# 헤더
st.markdown('<h1 class="main-header">🎯 몰입 체험 프로그램</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">황농문 교수님의 몰입 이론을 실천하는 의식의 무대</div>', unsafe_allow_html=True)

# 사용자 이름 입력
if not st.session_state.user_name:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        name = st.text_input("🙋 이름을 입력해주세요", placeholder="예: 갯버들")
        if st.button("시작하기", use_container_width=True, type="primary"):
            if name:
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("이름을 입력해주세요!")
else:
    # 환영 메시지
    st.success(f"👋 안녕하세요, {st.session_state.user_name}님! 오늘도 16시간 몰입에 도전하세요!")
    
    # Think Hard 명언
    st.markdown("""
    <div style='text-align:center; padding:10px; background:#f0f2f6; border-radius:10px; margin-bottom:20px;'>
    <i>"Work Hard가 아닌 Think Hard가 성공의 열쇠입니다"</i><br>
    - 황농문 서울대 명예교수 -
    </div>
    """, unsafe_allow_html=True)
    
    # 탭 생성 (사용법을 첫 번째로)
    tab1, tab2, tab3, tab4 = st.tabs(["📖 사용법", "🧘 호흡 명상", "🎭 의식의 무대", "📊 나의 기록"])
    
    # 탭1: 사용법
    with tab1:
        st.markdown("### 🎯 프로그램 사용 가이드")
        
        st.markdown("""
        <div class="info-box">
        <h4>👉 추천 사용 순서</h4>
        <ol>
        <li><b>호흡 명상</b>으로 마음을 준비합니다 (3분)</li>
        <li><b>의식의 무대</b>에서 주제에 몰입합니다 (5-30분)</li>
        <li><b>나의 기록</b>에서 진행 상황을 확인합니다</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        #### 🧘 호흡 명상 (4-8 호흡법)
        - 4초 동안 숨을 들이쉬고, 8초 동안 내쉽니다
        - 3회 반복하여 마음을 안정시킵니다
        - 몰입 전 준비 단계로 추천됩니다
        
        #### 🎭 의식의 무대
        1. **주제 설정**: 오늘 집중할 한 가지 주제를 정합니다
        2. **무대 조명**: 타이머를 설정하고 시작합니다
        3. **잡념 처리**: 떠오르는 잡념은 '잡념 보관함'에 기록합니다
        4. **몰입 노트**: 주제에 대한 생각을 자유롭게 적습니다
        
        #### 💡 황농문 교수님의 몰입 원칙
        - **16시간 법칙**: 문제를 풀고 16시간 후 다시 생각해보세요
        - **1초 원칙**: 잡념이 떠오르면 1초 안에 처리하세요
        - **Think Hard**: 열심히 일하지 말고, 깊이 생각하세요
        """)
        
        st.info("🌟 매일 같은 시간에 5분이라도 꾸준히 실천하는 것이 중요합니다!")
    
    # 탭2: 호흡 명상
    with tab2:
        st.markdown("### 🧘 호흡 명상 - 몰입을 위한 준비")
        
        st.markdown("""
        <div class="info-box">
        <b>4-8 호흡법</b>: 4초 들이쉬고, 8초 내쉬기를 3회 반복합니다.
        편안한 자세로 앉아 시작 버튼을 누르세요.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 호흡 명상 시작", use_container_width=True, type="primary", key="breath_start"):
                st.session_state.breathing_active = True
        
        if st.session_state.breathing_active:
            breathing_container = st.empty()
            
            for round in range(1, 4):
                # 들이쉬기
                for i in range(4, 0, -1):
                    breathing_container.markdown(f"""
                    <div style='text-align:center; padding:50px;'>
                        <h1 style='color:#4a90e2;'>🫁 들이쉬기</h1>
                        <h2>{i}</h2>
                        <p>라운드 {round}/3</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                
                # 내쉬기
                for i in range(8, 0, -1):
                    breathing_container.markdown(f"""
                    <div style='text-align:center; padding:50px;'>
                        <h1 style='color:#28a745;'>💨 내쉬기</h1>
                        <h2>{i}</h2>
                        <p>라운드 {round}/3</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
            
            breathing_container.markdown("""
            <div class="success-box">
            <h3 style='text-align:center;'>✅ 호흡 명상 완료!</h3>
            <p style='text-align:center;'>이제 의식의 무대로 이동하여 몰입을 시작하세요.</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.breathing_active = False
            time.sleep(3)
            st.rerun()
    
    # 탭3: 의식의 무대
    with tab3:
        st.markdown("### 🎭 의식의 무대 - 깊은 몰입 경험")
        
        # 주제 입력
        topic = st.text_input("🎯 오늘 몰입할 주제를 입력하세요", 
                             placeholder="예: 프로젝트 기획, 문제 해결, 창의적 아이디어...")
        
        # 시간 설정
        col1, col2 = st.columns(2)
        with col1:
            minutes = st.selectbox("⏰ 몰입 시간 (분)", [5, 10, 15, 20, 25, 30], index=1)
        
        with col2:
            if st.button("🔦 무대 조명 켜기", use_container_width=True, type="primary", key="stage_start"):
                if topic:
                    st.session_state.stage_active = True
                    st.session_state.focus_topic = topic
                    st.session_state.immersion_time = minutes
                    st.session_state.timer_running = True
                else:
                    st.error("먼저 몰입할 주제를 입력해주세요!")
        
        # 무대 표시
        if st.session_state.stage_active:
            st.markdown('<div class="stage-container">', unsafe_allow_html=True)
            
            # 스포트라이트 효과
            st.markdown(f"""
            <div class="spotlight">
                <div class="focus-topic">🎯 {st.session_state.focus_topic}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 타이머
            if st.session_state.timer_running:
                timer_placeholder = st.empty()
                end_time = time.time() + (st.session_state.immersion_time * 60)
                
                while time.time() < end_time and st.session_state.timer_running:
                    remaining = int(end_time - time.time())
                    mins, secs = divmod(remaining, 60)
                    timer_placeholder.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', 
                                              unsafe_allow_html=True)
                    time.sleep(1)
                
                if st.session_state.timer_running:
                    st.balloons()
                    st.success("🎉 몰입 세션 완료! 16시간 후 다시 생각해보세요.")
                    st.session_state.total_sessions += 1
                    st.session_state.total_time += st.session_state.immersion_time
                    st.session_state.timer_running = False
                    st.session_state.stage_active = False
            
            # 잡념 보관함
            st.markdown("#### 💭 잡념 보관함")
            distraction = st.text_input("떠오르는 잡념을 여기에 기록하세요", key="distraction_input")
            if st.button("📌 보관", key="save_distraction"):
                if distraction:
                    st.session_state.distractions.append(distraction)
                    st.success("잡념을 보관했습니다!")
            
            # 보관된 잡념 표시
            if st.session_state.distractions:
                for d in st.session_state.distractions:
                    st.markdown(f'<div class="postit">💭 {d}</div>', unsafe_allow_html=True)
            
            # 몰입 노트
            st.markdown("#### 📝 몰입 노트")
            notes = st.text_area("주제에 대한 생각을 자유롭게 기록하세요", height=200)
            
            # 종료 버튼
            if st.button("🛑 몰입 종료", type="secondary"):
                st.session_state.stage_active = False
                st.session_state.timer_running = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 탭4: 나의 기록
    with tab4:
        st.markdown("### 📊 나의 몰입 기록")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("총 세션 수", f"{st.session_state.total_sessions}회")
        
        with col2:
            st.metric("총 몰입 시간", f"{st.session_state.total_time}분")
        
        with col3:
            if st.session_state.total_sessions > 0:
                avg_time = st.session_state.total_time / st.session_state.total_sessions
                st.metric("평균 몰입 시간", f"{avg_time:.1f}분")
            else:
                st.metric("평균 몰입 시간", "0분")
        
        # 레벨 시스템
        st.markdown("#### 🏆 나의 몰입 레벨")
        
        total_hours = st.session_state.total_time / 60
        if total_hours < 1:
            level = "🌱 초급 몰입가"
            next_level = "중급까지 " + str(1 - total_hours) + "시간"
        elif total_hours < 10:
            level = "🌿 중급 몰입가"
            next_level = "고급까지 " + str(10 - total_hours) + "시간"
        else:
            level = "🌳 고급 몰입가"
            next_level = "몰입 마스터의 길을 걷고 있습니다!"
        
        st.info(f"현재 레벨: **{level}**\n\n다음 레벨: {next_level}")
        
        # 16시간 알림
        if st.session_state.total_sessions > 0:
            last_session_time = datetime.now()
            next_review_time = last_session_time + timedelta(hours=16)
            st.markdown(f"""
            <div class="info-box">
            <b>💡 16시간 법칙</b><br>
            다음 복습 시간: {next_review_time.strftime('%m월 %d일 %H시 %M분')}<br>
            황농문 교수님: "16시간 후 다시 생각하면 새로운 아이디어가 떠오릅니다"
            </div>
            """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888;'>
🌿 Created by 갯버들 | Based on 황농문 교수님's 몰입 이론<br>
문의: immersion.program@gmail.com
</div>
""", unsafe_allow_html=True)
