import os
import streamlit as st
from openai import OpenAI
from utils import create_thread, upload_image, add_image_message, run_assistant
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# Streamlit 앱 레이아웃
st.title("지쿠 주차 사진 AI 평가")
st.write("주차 사진을 업로드하고 AI 평가를 받으세요.")

# API 키를 환경 변수에서 가져오기
api_key = os.getenv("OPENAI_API_KEY")

# 기존 Assistant ID
assistant_id = "asst_gXioDoR3TTu7JMpd2rcGnlvO"

if api_key:
    client = OpenAI(api_key=api_key)

    # 이미지 업로드 버튼
    uploaded_file = st.file_uploader("주차 사진을 선택하세요...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # 업로드된 이미지 표시
            st.image(uploaded_file, caption='업로드된 주차 사진.', use_column_width=True)
            st.write("")
            st.write("AI 평가 중...")

            # 임시 디렉토리 생성
            if not os.path.exists("temp"):
                os.makedirs("temp")

            # 업로드된 이미지를 로컬 파일로 저장
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Thread 생성
            thread = create_thread(client)

            # 이미지 업로드 및 파일 ID 획득
            file_id = upload_image(client, file_path)

            # 메시지 추가
            add_image_message(client, thread.id, file_id)

            # 평가 실행
            run_assistant(client, thread.id, assistant_id)
        except Exception as e:
            st.error(f"오류 발생: {e}")
else:
    st.error("유효한 OpenAI API 키를 제공하세요.")