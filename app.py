# -*- coding: utf-8 -*-
# app.py - 5분 몰입 프로그램 (황농문 교수 이론 기반)
# Version: 2.0 - 타이머 자동업데이트 + 몰입아카데미 홍보
# Date: 2025.09.16

import streamlit as st
from datetime import datetime, timedelta
import json
import random
import time

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
    }
    
    .stat-number {
        font-size: 36px;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 14px;
        margin-top: 5px;
    }
    
    .link-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        text-decoration: none;
        display: inline-block;
        margin: 10px;
        font-weight: bold;
    }
    
    .report-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
def init_session_state():
    defaults = {
        'user_name': '',
        'timer_active': False,
        'start_time': None,
        'end_time': None,
        'current_topic': '',
        'current_category': '',
        'total_sessions': 0,
        'total_minutes': 0,
        'streak_days': 0,
        'last_session_date': None,
        'today_sessions': 0,
        'checklist_done': [],
        'selected_tab': '⚡ 시작하기',
        'session_history': [],
        'timer_completed': False,
        'daily_report': []  # 일일 몰입 보고서용
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# 초기화 실행
init_session_state()

# 시간대별 인사말
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return "🌅 상쾌한 아침, 몰입으로 하루를 시작하세요"
    elif 9 <= hour < 12:
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

# 몰입 보고서 생성 함수
def generate_immersion_report():
    if not st.session_state.session_history:
        return None
    
    today = datetime.now()
    today_sessions = [s for s in st.session_state.session_history 
                     if datetime.fromisoformat(s['date']).date() == today.date()]
    
    if not today_sessions:
        return None
    
    report = f"""
    📋 **{st.session_state.user_name}님의 일일 몰입 보고서**
    
    📅 날짜: {today.strftime('%Y년 %m월 %d일')}
    
    ✅ **오늘의 성과**
    - 총 몰입 횟수: {len(today_sessions)}회
    - 총 몰입 시간: {len(today_sessions) * 5}분
    - 주요 활동: {', '.join(set([s['topic'] for s in today_sessions]))}
    
    💡 **몰입 인사이트**
    - 가장 집중이 잘 된 시간: {datetime.fromisoformat(today_sessions[0]['date']).strftime('%H시')}
    - 연속 몰입 일수: {st.session_state.streak_days}일
    
    🎯 **내일의 목표**
    - 목표 몰입 횟수: {len(today_sessions) + 1}회
    - 추천 몰입 시간: 오전 중 2회, 오후 중 3회
    
    💪 **황농문 교수님의 한마디**
    "오늘도 Think Hard를 실천하셨군요! 
    매일 조금씩 몰입하다 보면 큰 변화가 일어납니다."
    
    ---
    🔗 몰입아카데미에서 더 깊은 몰입을 경험하세요
    """
    
    return report

# 헤더
st.markdown('<h1 class="main-header">⚡ 5분 몰입의 기적</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{get_greeting()}</div>', unsafe_allow_html=True)

# 몰입아카데미 링크 (상단)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <a href='https://www.youtube.com/@molipacademy' target='_blank' style='margin:0 10px;'>
            📺 황농문 교수 유튜브
        </a>
        <a href='https://molip.co.kr/' target='_blank' style='margin:0 10px;'>
            🎓 몰입아카데미
        </a>
    </div>
    """, unsafe_allow_html=True)

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
            <div class="stat-label">전체 세션</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_minutes}</div>
            <div class="stat-label">총 몰입(분)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.streak_days}</div>
            <div class="stat-label">연속 일수</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 탭 메뉴
    tab_names = ["⚡ 시작하기", "📊 기록", "🎯 습관", "💡 인사이트", "📋 보고서"]
    selected_tab = st.radio("", tab_names, 
                           index=tab_names.index(st.session_state.selected_tab) if st.session_state.selected_tab in tab_names else 0,
                           horizontal=True, key="tab_selector")
    
    if selected_tab != st.session_state.selected_tab:
        st.session_state.selected_tab = selected_tab
        st.rerun()
    
    st.markdown("---")
    
    # 탭 내용
    if st.session_state.selected_tab == "⚡ 시작하기":
        # 타이머 활성화 상태
        if st.session_state.timer_active:
            # 타이머 표시 (자동 업데이트)
            timer_placeholder = st.empty()
            
            if st.session_state.end_time:
                while True:
                    now = datetime.now()
                    if now < st.session_state.end_time:
                        remaining = (st.session_state.end_time - now).total_seconds()
                        mins = int(remaining // 60)
                        secs = int(remaining % 60)
                        
                        timer_placeholder.markdown(f"""
                        <div class="immersion-card">
                            <h2 style="color:white;">🎯 {st.session_state.current_topic}</h2>
                            <div class="timer-display">{mins:02d}:{secs:02d}</div>
                            <p style="color:white; opacity:0.9;">집중하세요! 5분은 금방입니다</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 중단 버튼
                        col1, col2, col3 = st.columns([1,2,1])
                        with col2:
                            if st.button("⏹️ 중단하기", use_container_width=True, type="secondary", key="stop_timer"):
                                st.session_state.timer_active = False
                                st.rerun()
                        
                        # 1초 대기
                        time.sleep(1)
                    else:
                        # 타이머 완료
                        timer_placeholder.empty()
                        st.balloons()
                        st.success("🎉 5분 몰입 완료! 훌륭합니다!")
                        
                        # 세션 기록 추가
                        st.session_state.session_history.append({
                            'date': datetime.now().isoformat(),
                            'topic': st.session_state.current_topic,
                            'category': st.session_state.current_category
                        })
                        
                        st.session_state.total_sessions += 1
                        st.session_state.today_sessions += 1
                        st.session_state.total_minutes += 5
                        st.session_state.timer_active = False
                        
                        # 연속일수 업데이트
                        today = datetime.now().date()
                        if st.session_state.last_session_date:
                            last_date = datetime.fromisoformat(st.session_state.last_session_date).date()
                            if (today - last_date).days == 1:
                                st.session_state.streak_days += 1
                            elif today != last_date:
                                st.session_state.streak_days = 1
                        else:
                            st.session_state.streak_days = 1
                        
                        st.session_state.last_session_date = datetime.now().isoformat()
                        
                        # 몰입 후 피드백
                        st.info("💡 몰입 후 1분간 휴식하고 느낀점을 기록해보세요")
                        
                        # 느낀점 기록
                        feedback = st.text_area("오늘의 몰입은 어떠셨나요?", key="feedback_input")
                        
                        if st.button("다시 시작", use_container_width=True, type="primary", key="restart"):
                            st.rerun()
                        
                        break
        
        else:
            # 빠른 시작
            st.markdown("### 🚀 빠른 시작")
            col1, col2 = st.columns([2,1])
            with col1:
                quick_topic = st.text_input("무엇에 집중하시겠습니까?", 
                                           placeholder="예: 이메일 정리, 보고서 작성...")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("⚡ 바로 시작", use_container_width=True, type="primary"):
                    if quick_topic:
                        st.session_state.current_topic = quick_topic
                        st.session_state.timer_active = True
                        st.session_state.start_time = datetime.now()
                        st.session_state.end_time = datetime.now() + timedelta(minutes=5)
                        st.rerun()
            
            # 카테고리 선택
            st.markdown("### 📂 카테고리별 몰입")
            cols = st.columns(2)
            for idx, (category, topics) in enumerate(IMMERSION_CATEGORIES.items()):
                with cols[idx % 2]:
                    if st.button(category, use_container_width=True, key=f"cat_{idx}"):
                        st.session_state.current_category = category
                        st.session_state.current_topic = random.choice(topics)
                        st.session_state.timer_active = True
                        st.session_state.start_time = datetime.now()
                        st.session_state.end_time = datetime.now() + timedelta(minutes=5)
                        st.rerun()
            
            # 준비 체크리스트
            st.markdown("### ✅ 몰입 준비 체크리스트")
            for item in PREPARATION_CHECKLIST:
                checked = st.checkbox(item, key=f"check_{item}")
                if checked and item not in st.session_state.checklist_done:
                    st.session_state.checklist_done.append(item)
            
            if len(st.session_state.checklist_done) == len(PREPARATION_CHECKLIST):
                st.success("완벽한 준비! 이제 몰입을 시작하세요 🚀")
    
    elif st.session_state.selected_tab == "📊 기록":
        st.markdown("### 📊 나의 몰입 기록")
        
        # 오늘의 진행률
        daily_goal = 6
        progress = min(1.0, st.session_state.today_sessions / daily_goal)
        st.progress(progress)
        st.caption(f"오늘 목표: {st.session_state.today_sessions}/{daily_goal}회")
        
        # 최근 세션
        st.markdown("#### 📅 최근 몰입 기록")
        if st.session_state.session_history:
            recent = st.session_state.session_history[-10:][::-1]
            for session in recent:
                date = datetime.fromisoformat(session['date'])
                st.write(f"• {date.strftime('%m/%d %H:%M')} - {session['topic']}")
        else:
            st.info("몰입을 시작하면 기록이 표시됩니다")
    
    elif st.session_state.selected_tab == "🎯 습관":
        st.markdown("### 🎯 21일 몰입 습관 만들기")
        
        # 습관 트래커
        st.markdown("#### 📅 습관 트래커")
        cols = st.columns(7)
        for i in range(7):
            with cols[i]:
                if i < st.session_state.streak_days:
                    st.success("✅")
                else:
                    st.info("⭕")
        
        st.markdown("#### 🏆 목표 설정")
        daily_target = st.slider("하루 목표 세션 수", 1, 10, 5)
        st.write(f"하루 {daily_target}회 × 5분 = {daily_target * 5}분 몰입")
        
        # 몰입 팁
        st.markdown("#### 💡 오늘의 몰입 팁")
        tips = [
            "짧은 시간이라도 완전히 집중하면 놀라운 성과를 얻을 수 있습니다",
            "몰입 전 심호흡 3번으로 마음을 정리하세요",
            "한 가지 일에만 집중하세요. 멀티태스킹은 몰입의 적입니다",
            "타이머가 울릴 때까지 절대 다른 일을 하지 마세요",
            "몰입 후 1분간 휴식으로 다음 몰입을 준비하세요"
        ]
        st.info(random.choice(tips))
    
    elif st.session_state.selected_tab == "💡 인사이트":
        st.markdown("### 💡 몰입 인사이트")
        
        # 황농문 교수 명언
        quotes = [
            "5분의 완벽한 몰입이 하루를 바꾸고, 하루가 인생을 바꿉니다",
            "Work Hard에서 Think Hard로, 그리고 Work Smart로",
            "짧은 몰입의 반복이 깊은 몰입으로 이어집니다",
            "몰입은 강요가 아닌 즐거움에서 시작됩니다",
            "작은 성공이 큰 성공의 씨앗입니다"
        ]
        
        st.markdown(f"""
        <div class="immersion-card">
            <h3 style="color:white;">황농문 교수의 가르침</h3>
            <p style="color:white; font-size:18px; margin:20px 0;">
            "{random.choice(quotes)}"
            </p>
            <p style="color:#ffd700;">- Think Hard의 시작 -</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 황농문 교수 유튜브 영상 추천
        st.markdown("#### 📺 추천 영상")
        st.markdown("""
        <div style='background:#f0f2f6; padding:20px; border-radius:10px;'>
            <h4>황농문 교수의 몰입 강의</h4>
            <p>더 깊은 몰입을 원하신다면 황농문 교수님의 강의를 들어보세요!</p>
            <a href='https://www.youtube.com/@molipacademy' target='_blank' 
               style='background:#ff0000; color:white; padding:10px 20px; 
                      border-radius:5px; text-decoration:none; display:inline-block;'>
                유튜브에서 보기
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # 통계
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 몰입 통계")
            if st.session_state.total_sessions > 0:
                avg_daily = st.session_state.total_sessions / max(1, st.session_state.streak_days or 1)
                st.metric("일평균 몰입", f"{avg_daily:.1f}회")
                st.metric("총 몰입 시간", f"{st.session_state.total_minutes}분")
                st.metric("시간 환산", f"{st.session_state.total_minutes/60:.1f}시간")
        
        with col2:
            st.markdown("#### 🎯 몰입 레벨")
            level_thresholds = [
                (0, "🌱 몰입 씨앗"),
                (10, "🌿 몰입 새싹"),
                (50, "🌳 몰입 나무"),
                (100, "🏔️ 몰입 산"),
                (200, "🌟 몰입 마스터")
            ]
            
            current_level = "🌱 몰입 씨앗"
            for threshold, level in level_thresholds:
                if st.session_state.total_sessions >= threshold:
                    current_level = level
            
            st.info(f"현재: {current_level}")
    
    elif st.session_state.selected_tab == "📋 보고서":
        st.markdown("### 📋 몰입 보고서")
        
        # 일일 보고서 생성
        report = generate_immersion_report()
        
        if report:
            st.markdown(report)
            
            # 보고서 다운로드 버튼
            st.download_button(
                label="📥 보고서 다운로드",
                data=report,
                file_name=f"몰입보고서_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.info("오늘의 몰입을 시작하면 보고서가 자동으로 생성됩니다!")
        
        # 몰입아카데미 안내
        st.markdown("""
        <div style='background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color:white; padding:30px; border-radius:15px; margin-top:30px;'>
            <h3 style='color:white;'>🎓 몰입아카데미에서 만나요!</h3>
            <p style='color:white;'>
            황농문 교수님의 직접 지도로 더 깊은 몰입을 경험하세요.
            16시간 몰입 이론의 모든 것을 배울 수 있습니다.
            </p>
            <div style='margin-top:20px;'>
                <a href='https://molip.co.kr/' target='_blank' 
                   style='background:white; color:#667eea; padding:10px 30px; 
                          border-radius:25px; text-decoration:none; font-weight:bold;
                          display:inline-block; margin-right:10px;'>
                    몰입아카데미 방문
                </a>
                <a href='https://www.youtube.com/@molipacademy' target='_blank' 
                   style='background:white; color:#667eea; padding:10px 30px; 
                          border-radius:25px; text-decoration:none; font-weight:bold;
                          display:inline-block;'>
                    유튜브 구독
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:20px;'>
<b>5분 몰입의 기적</b><br>
황농문 교수 몰입 이론 기반 | 직장인 특화 프로그램<br>
개발: 갯버들 | 2025.09.16<br>
<a href='https://molip.co.kr/' target='_blank'>몰입아카데미</a> | 
<a href='https://www.youtube.com/@molipacademy' target='_blank'>유튜브</a>
</div>
""", unsafe_allow_html=True)
