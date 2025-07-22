import streamlit as st
import re

VIOLATION_RULES = {
    "출신지역": ["서울", "부산", "대전", "대구", "광주", "인천", "고향", "출신지"],
    "가족관계": ["아버지", "어머니", "부모님", "형", "누나", "오빠", "언니", "동생", "가족"],
    "종교": ["교회", "성당", "불교", "기독교", "천주교", "청년부", "기도회", "예배", "종교"],
    "정치": ["더불어민주당", "국민의힘", "보좌관", "국회의원", "정당", "정치"],
    "연령": ["\\d{2}세", "\\d{2}살", "20대", "30대", "40대", "한일 월드컵", "90년대생", "2000년생"],
    "성별": ["남자", "여자", "군대", "임신", "육아", "아빠", "엄마", "현역", "복무"],
    "출신학교": ["대학교", "고등학교", "중학교", "총장상", "학보사", "근로장학생", "OO대학교", "○○대학교"]
}

def detect_violations(text):
    results = []
    for category, patterns in VIOLATION_RULES.items():
        for keyword in patterns:
            if re.search(keyword, text):
                results.append((category, keyword))
    return results

st.title("🔍 NRC 자기소개서 블라인드 체크기")
st.write("경제인문사회연구회 자기소개서에서 블라인드 채용 기준 위반 항목이 포함되었는지 자동으로 점검합니다.")

user_input = st.text_area("자기소개서 내용을 입력하세요", height=300)

if st.button("점검하기"):
    if not user_input.strip():
        st.warning("자기소개서 내용을 입력해주세요.")
    else:
        violations = detect_violations(user_input)
        if violations:
            st.error("❗ 다음 항목들이 블라인드 채용 기준을 위반할 수 있습니다:")
            for category, keyword in set(violations):
                st.markdown(f"- **[{category}]** 키워드 발견: `{keyword}`")
        else:
            st.success("✅ 위반 요소가 없습니다. 안전한 자기소개서입니다.")
