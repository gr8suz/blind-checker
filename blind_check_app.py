import streamlit as st
import re
import fitz  # PyMuPDF

# 블라인드 채용 기준 위반 항목 정의
VIOLATION_RULES = {
    "출신지역": [
        "고향", "출신지",
        "서울", "부산", "인천", "대구", "광주", "대전", "세종", "울산", "제주",
        "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", 
        "경상북도", "경상남도", "제주도", "서울특별시", "부산광역시", "대구광역시",
        "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",
        r"[가-힣]{2,10}(시|도|군|구|읍|면)"
    ],
    "가족관계": [
        "아버지", "어머니", "부모님", "형", "누나", "오빠", "언니", "동생", "가족"
    ],
    "종교": [
        "교회", "성당", "불교", "기독교", "천주교", "청년부", "기도회", "예배", "종교"
    ],
    "정치": [
        "더불어민주당", "국민의힘", "보좌관", "국회의원", "정당", "정치"
    ],
    "연령": [
        r"\d{2}세", r"\d{2}살", "20대", "30대", "40대", "한일 월드컵", "90년대생", "2000년생"
    ],
    "성별": [
    "남자", "여자", "아빠", "엄마", "임신", "육아", "현역", "복무", "군대",
    # 군 복무 관련 키워드 추가
    "행정병", "운전병", "통신병", "보병", "이병", "일병", "상병", "병장",
    "육군", "해군", "공군", "해병대", "전역", "군생활", "군번", "자대", "조교", "훈련소", "GOP", "ROTC"
    ],
    "출신학교": [
        r"(?![O○]+대)[가-힣]{2,10}대",
        r"[가-힣]{2,10}대학교",
        "고등학교", "중학교"
    ]
}

# 위반 항목 감지 함수
def detect_violations(text):
    results = []
    for category, patterns in VIOLATION_RULES.items():
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                results.append((category, match))
    return results

# Streamlit UI
st.title("🔍 NRC 자기소개서 블라인드 체크기")
st.write("경제인문사회연구회 자기소개서에서 블라인드 채용 기준 위반 항목이 포함되었는지 자동으로 점검합니다.")
with st.expander("📌 블라인드 채용 기준 보기 (클릭하여 펼치기/닫기)"):
    st.image("blind.jpg", caption="경제인문사회연구회 블라인드 채용 기준 요약", use_container_width=True)


tab1, tab2 = st.tabs(["📄 직접 입력", "📎 PDF 업로드"])

with tab1:
    user_input = st.text_area("자기소개서 내용을 입력하세요", height=300)

    if st.button("직접 입력 검사하기"):
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

with tab2:
    uploaded_file = st.file_uploader("자기소개서 PDF 파일 업로드", type="pdf")

    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        extracted_text = ""
        for page in doc:
            extracted_text += page.get_text()
        
        st.text_area("📄 추출된 자기소개서 내용", extracted_text, height=300)

        if st.button("PDF 내용 검사하기"):
            if not extracted_text.strip():
                st.warning("PDF에서 내용을 추출하지 못했습니다.")
            else:
                violations = detect_violations(extracted_text)
                if violations:
                    st.error("❗ 다음 항목들이 블라인드 채용 기준을 위반할 수 있습니다:")
                    for category, keyword in set(violations):
                        st.markdown(f"- **[{category}]** 키워드 발견: `{keyword}`")
                else:
                    st.success("✅ 위반 요소가 없습니다. 안전한 자기소개서입니다.")
