# -*- coding: utf-8 -*-
# app.py - 5분 몰입 프로그램 (황농문 교수 이론 기반)
# Created by 갯버들 (한승희)
# Based on Prof. Hwang Nong-Moon's Immersion Theory
# 
# GitHub: https://github.com/sjks007-art/immersion-program
# Version: 4.0 - plotly 제거 버전
# Date: 2025.09.15

import streamlit as st
from datetime import datetime, timedelta
import json
import random
import time
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="5분 몰입의 기적 | 황농문 교수 이론",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .immersion-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
        text-align: center;
    }
    
    .timer-display {
        font-size: 72px;
        color: #ffd700;
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255,215,0,0.5);
        font-family: 'Courier New', monospace;
        margin: 20px 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
        border: 2px solid #f0f0f0;
    }
    
    .stat-number {
        font-size: 28px;
        font-weight: bold;
        color: #667eea;
        margin: 5px 0;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 14px;
    }
    
    .level-badge {
        display: inline-block;
        padding: 5px 15px;
        background: #ffd700;
        color: #333;
        border-radius: 20px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .hwang-quote {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-left: 4px solid #667eea;
        padding: 20px;
        margin: 20px 0;
        border-radius: 10px;
        font-style: italic;
    }
    
    .molip-academy-box {
        background: #f8f9fa;
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    
    .link-button {
        display: inline-block;
        padding: 10px 20px;
        margin: 5px;
        background: #667eea;
        color: white;
        text-decoration: none;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .link-button:hover {
        background: #764ba2;
        transform: translateY(-2px);
    }
    
    .report-section {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .tab-button {
        padding: 10px 20px;
        margin: 0 5px;
        border-radius: 20px 20px 0 0;
        background: #f0f0f0;
        border: none;
        cursor: pointer;
        font-weight: bold;
    }
    
    .tab-button.active {
        background: #667eea;
        color: white;
    }
    
    .challenge-day {
        display: inline-block;
        width: 40px;
        height: 40px;
        line-height: 40px;
        text-align: center;
        margin: 2px;
        border-radius: 50%;
        font-weight: bold;
    }
    
    .challenge-day.completed {
        background: #28a745;
        color: white;
    }
    
    .challenge-day.today {
        background: #ffd700;
        color: #333;
        animation: pulse 2s infinite;
    }
    
    .challenge-day.future {
        background: #e9ecef;
        color: #6c757d;
    }
    
    .challenge-day.missed {
        background: #f8f9fa;
        color: #dee2e6;
        opacity: 0.5;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "시작"
if 'session_history' not in st.session_state:
    st.session_state.session_history = []
if 'total_sessions' not in st.session_state:
    st.session_state.total_sessions = 0
if 'today_sessions' not in st.session_state:
    st.session_state.today_sessions = 0
if 'streak_days' not in st.session_state:
    st.session_state.streak_days = 0
if 'total_minutes' not in st.session_state:
    st.session_state.total_minutes = 0
if 'last_session_date' not in st.session_state:
    st.session_state.last_session_date = None
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'current_category' not in st.session_state:
    st.session_state.current_category = ""
if 'level' not in st.session_state:
    st.session_state.level = "초급"
if 'challenge_start_date' not in st.session_state:
    st.session_state.challenge_start_date = None
if 'completed_days' not in st.session_state:
    st.session_state.completed_days = set()

# 시간대별 인사말
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "☀️ 오전의 집중력이 최고인 시간입니다"
    elif 12 <= hour < 14:
        return "🍽️ 점심 후 5분 몰입으로 오후를 준비하세요"
    elif 14 <= hour < 18:
        return "🚀 오후의 생산성을 높일 시간입니다"
    elif 18 <= hour < 22:
        return "🌙 하루를 마무리하는 몰입의 시간"
    else:
        return "✨ 고요한 시간, 깊은 몰입이 가능합니다"

# 몰입 카테고리
IMMERSION_CATEGORIES = {
    "📧 이메일 정리": [
        "받은편지함 비우기",
        "중요 메일 답장하기",
        "스팸 정리하기"
    ],
    "📝 문서 작업": [
        "보고서 한 섹션 작성",
        "회의록 정리",
        "제안서 아이디어 정리"
    ],
    "💡 아이디어": [
        "브레인스토밍",
        "문제 해결 방안 찾기",
        "개선점 도출"
    ],
    "📚 학습": [
        "자료 읽기",
        "영상 하나 시청",
        "핵심 내용 정리"
    ],
    "🎯 계획": [
        "오늘의 우선순위 정하기",
        "주간 목표 점검",
        "일정 정리"
    ],
    "🧘 마음정리": [
        "호흡 명상",
        "감사 일기",
        "하루 돌아보기"
    ]
}

# 체크리스트
PREPARATION_CHECKLIST = [
    "📱 스마트폰 무음 설정",
    "💬 메신저 알림 끄기",
    "🎧 집중 환경 준비",
    "📝 목표 명확히 하기",
    "💧 물 한잔 준비"
]

# 몰입 명언
IMMERSION_QUOTES = [
    "5분의 완벽한 몰입이 하루를 바꾸고, 하루가 인생을 바꿉니다. - 황농문",
    "Think Hard가 Work Hard보다 중요한 시대입니다. - 황농문",
    "16시간 이미지 트레이닝으로 잠재의식을 깨우세요. - 황농문",
    "몰입은 긴장이 아니라 이완입니다. - 황농문",
    "슬로싱킹으로 천천히 오래 생각하세요. - 황농문"
]

# 레벨 계산 (도파민 보상 시스템 강화)
def calculate_level():
    sessions = st.session_state.total_sessions
    
    # 레벨 임계값과 뱃지
    levels = [
        (100, "🏆 마스터", "#ffd700", "몰입의 경지에 도달하셨습니다!"),
        (50, "⭐ 전문가", "#ffc107", "당신은 진정한 몰입 전문가입니다!"),
        (20, "🌳 고급", "#764ba2", "깊은 몰입을 경험하고 계십니다!"),
        (5, "🌿 중급", "#17a2b8", "몰입이 습관이 되어가고 있어요!"),
        (0, "🌱 초급", "#28a745", "몰입의 여정을 시작하셨군요!")
    ]
    
    for threshold, badge, color, message in levels:
        if sessions >= threshold:
            # 레벨업 직전에 특별 메시지 (다음 레벨까지 2세션 이하)
            next_threshold = next((l[0] for l in levels if l[0] > sessions), None)
            if next_threshold and next_threshold - sessions <= 2:
                message += f" (곧 레벨업! {next_threshold - sessions}세션 남음)"
            
            return badge, color
    
    return "🌱 초급", "#28a745"

# 보고서 생성
def generate_report():
    report = f"""
    # 📊 몰입 실천 보고서
    
    **작성일시**: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}
    **실천자**: {st.session_state.user_name}
    
    ## 📈 통계
    - **총 몰입 세션**: {st.session_state.total_sessions}회
    - **총 몰입 시간**: {st.session_state.total_minutes}분
    - **연속 실천일**: {st.session_state.streak_days}일
    - **오늘 세션**: {st.session_state.today_sessions}회
    - **현재 레벨**: {calculate_level()[0]}
    
    ## 💡 황농문 교수님의 가르침
    "{random.choice(IMMERSION_QUOTES)}"
    
    ## 🎯 최근 몰입 주제
    """
    
    if st.session_state.session_history:
        recent_sessions = st.session_state.session_history[-5:]
        for session in reversed(recent_sessions):
            date = datetime.fromisoformat(session['date']).strftime('%m/%d %H:%M')
            report += f"- [{date}] {session['category']}: {session['topic']}\n"
    
    report += """
    
    ## 🚀 다음 목표
    - 21일 연속 몰입 도전
    - 일일 3회 이상 실천
    - 팀원과 함께 몰입 문화 만들기
    
    ---
    *이 보고서는 황농문 교수님의 몰입 이론을 기반으로 자동 생성되었습니다.*
    *몰입아카데미: https://molip.co.kr*
    """
    
    return report

# 21일 챌린지 표시 (도파민 최적화 버전)
def display_21_day_challenge():
    st.markdown("### 🎯 21일 몰입 습관 만들기")
    
    if not st.session_state.challenge_start_date:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 10px; text-align: center;'>
            <h4>21일이면 습관이 됩니다!</h4>
            <p>매일 5분, 작은 몰입이 큰 변화를 만듭니다</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 챌린지 시작하기", type="primary", use_container_width=True):
            st.session_state.challenge_start_date = datetime.now().date()
            st.rerun()
    else:
        start_date = st.session_state.challenge_start_date
        today = datetime.now().date()
        days_passed = (today - start_date).days
        
        # 현재 연속 기록 강조
        completed_count = len([d for d in st.session_state.completed_days if d <= today.isoformat()])
        
        if st.session_state.streak_days > 0:
            st.success(f"🔥 {st.session_state.streak_days}일 연속 몰입 중! 대단해요!")
        
        # 주간 뷰 (7일씩만 표시)
        st.markdown("#### 📅 이번 주 몰입 기록")
        
        # 이번 주의 시작일과 끝일 계산
        week_start = today - timedelta(days=today.weekday())
        
        cols = st.columns(7)
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            day_label = weekdays[i]
            
            with cols[i]:
                if current_date < start_date:
                    # 챌린지 시작 전
                    st.markdown(f"""
                    <div style='text-align:center; color:#dee2e6;'>
                        <div style='font-size:10px;'>{day_label}</div>
                        <div style='font-size:20px;'>-</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif current_date < today:
                    # 과거
                    if current_date.isoformat() in st.session_state.completed_days:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:10px;'>{day_label}</div>
                            <div style='font-size:24px;'>✅</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # 놓친 날은 희미하게 표시 (실패 강조 X)
                        st.markdown(f"""
                        <div style='text-align:center; opacity:0.3;'>
                            <div style='font-size:10px;'>{day_label}</div>
                            <div style='font-size:20px;'>💤</div>
                        </div>
                        """, unsafe_allow_html=True)
                elif current_date == today:
                    # 오늘
                    if today.isoformat() in st.session_state.completed_days:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:10px; color:#667eea; font-weight:bold;'>{day_label}</div>
                            <div style='font-size:24px;'>✅</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:10px; color:#667eea; font-weight:bold;'>{day_label}</div>
                            <div class='challenge-day today' style='margin:auto;'>🎯</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # 미래 (물음표로 미스터리 유지)
                    st.markdown(f"""
                    <div style='text-align:center;'>
                        <div style='font-size:10px;'>{day_label}</div>
                        <div style='font-size:20px; color:#dee2e6;'>❓</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 전체 진행 상황 (긍정적 표현)
        st.markdown("---")
        if completed_count > 0:
            progress = min(completed_count / 21, 1.0)
            st.progress(progress)
            
            # 단계별 격려 메시지
            if completed_count < 7:
                stage_msg = f"🌱 시작이 반입니다! ({completed_count}/21일)"
            elif completed_count < 14:
                stage_msg = f"🌿 습관이 형성되고 있어요! ({completed_count}/21일)"
            elif completed_count < 21:
                stage_msg = f"🌳 거의 다 왔어요! ({completed_count}/21일)"
            else:
                stage_msg = f"🏆 21일 달성! 축하합니다! 🎉"
                st.balloons()
            
            st.info(stage_msg)
            
            # 다음 마일스톤까지 남은 일수 (긍정적 목표 제시)
            milestones = [7, 14, 21]
            next_milestone = next((m for m in milestones if m > completed_count), None)
            if next_milestone:
                remaining = next_milestone - completed_count
                st.caption(f"💫 다음 목표까지 {remaining}일 더 도전하면 됩니다!")
        else:
            st.info("🚀 오늘 첫 몰입을 시작해보세요! 작은 시작이 큰 변화를 만듭니다.")

# 헤더
st.markdown('<h1 class="main-header">⚡ 5분 몰입의 기적</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{get_greeting()}</div>', unsafe_allow_html=True)

# 사용자 이름 입력
if not st.session_state.user_name:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="immersion-card">
            <h3>황농문 교수의 몰입 이론을</h3>
            <h2>5분으로 시작하세요</h2>
            <p>Think Hard의 첫걸음</p>
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("이름을 입력하세요", placeholder="홍길동")
        if st.button("시작하기", use_container_width=True, type="primary"):
            if name:
                st.session_state.user_name = name
                st.rerun()
else:
    # 상단 통계
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.today_sessions}</div>
            <div class="stat-label">오늘 세션</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_sessions}</div>
            <div class="stat-label">총 세션</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.streak_days}</div>
            <div class="stat-label">연속일수</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        level, color = calculate_level()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: {color};">{level}</div>
            <div class="stat-label">레벨</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 몰입아카데미 홍보
    st.markdown("""
    <div class="molip-academy-box">
        <h4>🎓 황농문 교수님의 몰입아카데미</h4>
        <p>더 깊은 몰입을 원하신다면?</p>
        <a href="https://molip.co.kr" target="_blank" class="link-button">몰입아카데미 방문</a>
        <a href="https://www.youtube.com/@molipacademy" target="_blank" class="link-button">유튜브 채널</a>
    </div>
    """, unsafe_allow_html=True)
    
    # 탭 메뉴
    tabs = st.tabs(["⚡ 시작", "📊 기록", "🎯 습관", "💡 인사이트", "📄 보고서"])
    
    with tabs[0]:  # 시작 탭
        st.markdown("### ⚡ 5분 몰입 시작")
        
        # 빠른 시작
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 빠른 시작 (주제 자동)", use_container_width=True, type="primary", disabled=st.session_state.timer_active):
                topics = ["오늘의 핵심 과제", "해결해야 할 문제", "새로운 아이디어", "개선점 찾기"]
                st.session_state.current_topic = random.choice(topics)
                st.session_state.current_category = "자동 선택"
                st.session_state.timer_active = True
                st.session_state.timer_start = datetime.now()
                st.rerun()
        
        with col2:
            if st.button("🎯 주제 선택하기", use_container_width=True, disabled=st.session_state.timer_active):
                st.session_state.show_categories = True
        
        # 카테고리 선택
        if hasattr(st.session_state, 'show_categories') and st.session_state.show_categories:
            st.markdown("### 📂 카테고리 선택")
            
            cols = st.columns(3)
            for idx, (category, topics) in enumerate(IMMERSION_CATEGORIES.items()):
                col = cols[idx % 3]
                with col:
                    if st.button(category, use_container_width=True):
                        st.session_state.current_category = category
                        st.session_state.current_topic = random.choice(topics)
                        st.session_state.timer_active = True
                        st.session_state.timer_start = datetime.now()
                        st.session_state.show_categories = False
                        st.rerun()
        
        # 타이머 표시
        if st.session_state.timer_active:
            st.markdown(f"### 🎯 현재 몰입 주제: {st.session_state.current_topic}")
            
            # 타이머 계산
            elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
            remaining = max(0, 300 - elapsed)  # 5분 = 300초
            
            if remaining > 0:
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                
                # 타이머 표시
                st.markdown(f'<div class="timer-display">{minutes:02d}:{seconds:02d}</div>', unsafe_allow_html=True)
                
                # 진행 바
                progress = (300 - remaining) / 300
                st.progress(progress)
                
                # 응원 메시지 (도파민 변화를 위한 다양화)
                encouragement_pool = {
                    240: [  # 4분 이상
                        "🚀 시작! 깊게 집중하세요",
                        "🌊 몰입의 파도가 시작됩니다",
                        "💫 당신의 뇌가 깨어나고 있어요"
                    ],
                    180: [  # 3분 이상
                        "💪 잘하고 있어요! 계속 집중!",
                        "🔥 몰입의 불꽃이 타오르고 있어요",
                        "⚡ 뇌의 시냅스가 활발해지고 있습니다"
                    ],
                    120: [  # 2분 이상
                        "🌟 절반 지났습니다! 조금만 더!",
                        "💎 당신의 집중력이 빛나고 있어요",
                        "🎯 목표에 가까워지고 있습니다"
                    ],
                    60: [  # 1분 이상
                        "⭐ 거의 다 왔어요! 마지막 스퍼트!",
                        "🏃 마지막 직선 구간입니다",
                        "🌈 곧 무지개가 나타날 거예요"
                    ],
                    0: [  # 1분 미만
                        "🏆 1분 남았습니다! 마무리 집중!",
                        "🎊 곧 축하할 시간입니다",
                        "✨ 마지막 순간까지 최선을!"
                    ]
                }
                
                # 시간대별 메시지 선택
                for threshold, messages in encouragement_pool.items():
                    if remaining > threshold:
                        message = random.choice(messages)
                        
                        # 가끔 특별 메시지 추가 (5% 확률)
                        if random.random() < 0.05:
                            bonus_messages = [
                                " 💝 (오늘따라 특별히 잘하시네요!)",
                                " 🎁 (숨겨진 재능이 보입니다!)",
                                " 🌠 (황농문 교수님이 지켜보고 계십니다)"
                            ]
                            message += random.choice(bonus_messages)
                        
                        st.info(message)
                        break
                
                # 중단 버튼
                if st.button("⏹️ 중단하기", use_container_width=True):
                    st.session_state.timer_active = False
                    st.rerun()
                
                # 자동 새로고침
                time.sleep(1)
                st.rerun()
            else:
                # 완료
                st.balloons()
                st.success("🎉 5분 몰입 완료! 훌륭합니다!")
                
                # 도파민 서프라이즈 이벤트 (10% 확률)
                if random.random() < 0.1:
                    surprise_events = [
                        ("🎁 서프라이즈! 오늘은 더블 포인트!", 2),
                        ("🌟 대단해요! 숨겨진 업적 '몰입 마스터' 달성!", 1),
                        ("💎 레어 이벤트! 황농문 교수님의 특별 격려!", 1),
                        ("🏆 퍼펙트 타이밍! 보너스 연속일수 +1!", 1)
                    ]
                    event_msg, bonus = random.choice(surprise_events)
                    st.balloons()
                    st.success(event_msg)
                    
                    # 보너스 적용
                    if "더블 포인트" in event_msg:
                        st.session_state.total_sessions += 1  # 추가 세션
                    elif "연속일수" in event_msg:
                        st.session_state.streak_days += 1  # 추가 연속일
                    
                    # 황농문 교수님 특별 메시지
                    if "황농문" in event_msg:
                        special_quotes = [
                            "당신의 몰입이 16시간으로 이어질 것입니다.",
                            "이완된 집중의 완벽한 예시입니다!",
                            "Think Hard의 진정한 의미를 깨달으셨군요."
                        ]
                        st.info(f"💬 \"{random.choice(special_quotes)}\" - 황농문")
                
                # 일반 완료 메시지 다양화 (예측 불가능성)
                completion_messages = [
                    "훌륭합니다! 오늘의 몰입이 내일의 통찰로 이어집니다.",
                    "멋져요! 당신의 뇌가 최적화되고 있습니다.",
                    "완벽해요! 이완된 집중 상태를 경험하셨군요.",
                    "대단해요! 몰입의 깊이가 점점 더해지고 있습니다."
                ]
                st.info(random.choice(completion_messages))
                
                # 기록 저장
                st.session_state.session_history.append({
                    'date': datetime.now().isoformat(),
                    'topic': st.session_state.current_topic,
                    'category': st.session_state.current_category
                })
                
                # 통계 업데이트
                st.session_state.total_sessions += 1
                st.session_state.today_sessions += 1
                st.session_state.total_minutes += 5
                
                # 오늘 날짜를 완료 목록에 추가
                today = datetime.now().date().isoformat()
                st.session_state.completed_days.add(today)
                
                # 연속일수 업데이트
                if st.session_state.last_session_date:
                    last_date = datetime.fromisoformat(st.session_state.last_session_date).date()
                    if (datetime.now().date() - last_date).days == 1:
                        st.session_state.streak_days += 1
                    elif datetime.now().date() != last_date:
                        st.session_state.streak_days = 1
                else:
                    st.session_state.streak_days = 1
                
                st.session_state.last_session_date = datetime.now().isoformat()
                st.session_state.timer_active = False
                
                # 피드백
                feedback = st.text_area("💭 몰입 후기를 남겨주세요", placeholder="어떤 생각이 들었나요?")
                if st.button("저장하고 계속", type="primary"):
                    st.rerun()
        
        # 준비 체크리스트
        st.markdown("### ✅ 몰입 준비 체크리스트")
        for item in PREPARATION_CHECKLIST:
            st.checkbox(item)
    
    with tabs[1]:  # 기록 탭
        st.markdown("### 📊 몰입 기록")
        
        if st.session_state.session_history:
            # 최근 세션
            st.markdown("#### 최근 몰입 세션")
            for session in reversed(st.session_state.session_history[-10:]):
                date = datetime.fromisoformat(session['date'])
                st.write(f"• {date.strftime('%m/%d %H:%M')} - {session['category']}: {session['topic']}")
            
            # 주간 차트
            st.markdown("#### 주간 몰입 통계")
            
            # 데이터 준비
            week_data = []
            for i in range(7):
                date = (datetime.now() - timedelta(days=6-i)).date()
                count = sum(1 for s in st.session_state.session_history 
                          if datetime.fromisoformat(s['date']).date() == date)
                week_data.append({
                    '날짜': date.strftime('%m/%d'),
                    '세션': count
                })
            
            df = pd.DataFrame(week_data)
            
            # Streamlit 기본 막대 차트 사용
            st.bar_chart(df.set_index('날짜')['세션'], color='#667eea')
        else:
            st.info("아직 기록이 없습니다. 첫 몰입을 시작해보세요!")
    
    with tabs[2]:  # 습관 탭
        st.markdown("### 🎯 몰입 습관 만들기")
        
        # 21일 챌린지
        display_21_day_challenge()
        
        # 몰입 팁 (도파민 예측 불가능성을 위한 확장)
        st.markdown("### 💡 오늘의 몰입 팁")
        
        # 황농문 교수님 이론 기반 팁
        tips_categories = {
            "슬로싱킹": [
                "천천히 오래 생각하세요. 서두르지 마세요.",
                "이완된 집중이 진정한 몰입입니다.",
                "의자에 편안히 기대고 생각의 흐름을 따라가세요."
            ],
            "실천법": [
                "타이머가 시작되면 절대 다른 일을 하지 마세요",
                "스마트폰은 시야에서 완전히 치워두세요",
                "한 가지 주제에만 집중하세요"
            ],
            "마인드셋": [
                "완벽하지 않아도 괜찮습니다. 시작이 중요해요",
                "몰입 후 1분간 휴식으로 다음 몰입을 준비하세요",
                "실패는 성장의 기회입니다. 내일 다시 도전하세요"
            ],
            "16시간 이론": [
                "5분 몰입이 16시간 이미지 트레이닝으로 이어집니다",
                "잠재의식이 당신을 위해 계속 일하고 있습니다",
                "Think Hard가 Work Hard보다 중요합니다"
            ]
        }
        
        # 랜덤 카테고리와 팁 선택
        category = random.choice(list(tips_categories.keys()))
        tip = random.choice(tips_categories[category])
        
        # 특별 이벤트 (3% 확률로 황농문 교수님 직접 인용)
        if random.random() < 0.03:
            st.success(f"🎓 [황농문 교수님 특별 메시지]\n\"{tip}\"")
        else:
            st.info(f"💡 [{category}] {tip}")
        
        # 황농문 교수 명언
        st.markdown("### 📖 황농문 교수님의 가르침")
        st.markdown(f"""
        <div class="hwang-quote">
            "{random.choice(IMMERSION_QUOTES)}"
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[3]:  # 인사이트 탭
        st.markdown("### 💡 몰입 인사이트")
        
        if st.session_state.total_sessions > 0:
            # 통계 분석
            col1, col2 = st.columns(2)
            
            with col1:
                avg_daily = st.session_state.total_sessions / max(1, st.session_state.streak_days)
                st.metric("일평균 몰입 횟수", f"{avg_daily:.1f}회")
                st.metric("총 몰입 시간", f"{st.session_state.total_minutes}분")
            
            with col2:
                productivity = st.session_state.total_minutes * 12  # 5분 몰입이 1시간 효과
                st.metric("예상 생산성 향상", f"{productivity}분")
                st.metric("목표 달성률", f"{min(100, st.session_state.total_sessions*2)}%")
            
            # 성장 곡선
            if len(st.session_state.session_history) > 1:
                st.markdown("#### 📈 성장 곡선")
                
                # 누적 세션 데이터
                growth_data = []
                for i, session in enumerate(st.session_state.session_history):
                    date = datetime.fromisoformat(session['date'])
                    growth_data.append({
                        '날짜': date.strftime('%m/%d %H:%M'),
                        '누적 세션': i + 1
                    })
                
                df_growth = pd.DataFrame(growth_data)
                
                # Streamlit 기본 라인 차트 사용
                st.line_chart(df_growth.set_index('날짜')['누적 세션'], color='#667eea')
        
        # 다음 목표
        st.markdown("### 🎯 다음 목표")
        next_goals = [
            "오늘 3회 몰입 도전",
            "내일도 같은 시간에 몰입",
            "동료와 함께 몰입 챌린지",
            "더 어려운 문제에 도전",
            "몰입 시간을 10분으로 늘리기"
        ]
        for goal in next_goals[:3]:
            st.checkbox(goal)
    
    with tabs[4]:  # 보고서 탭
        st.markdown("### 📄 몰입 실천 보고서")
        
        # 보고서 생성
        report = generate_report()
        
        # 보고서 표시
        st.markdown("""
        <div class="report-section">
        """, unsafe_allow_html=True)
        st.markdown(report)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 다운로드 버튼
        st.download_button(
            label="📥 보고서 다운로드",
            data=report,
            file_name=f"몰입보고서_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
        
        # 공유 버튼
        if st.button("📤 황농문 교수님께 보고", type="primary"):
            st.info("보고서가 준비되었습니다. 이메일이나 메신저로 공유해주세요.")
            st.code(report)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:20px;'>
<b>5분 몰입의 기적</b><br>
황농문 교수 몰입 이론 기반 | 직장인 특화 프로그램<br>
개발: 갯버들 (한승희) | 2025.09.15<br>
<a href="https://molip.co.kr" target="_blank">몰입아카데미</a> | 
<a href="https://www.youtube.com/@molipacademy" target="_blank">유튜브</a>
</div>
""", unsafe_allow_html=True)
