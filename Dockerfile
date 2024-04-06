# Python 이미지를 기반으로 시작
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 현재 디렉토리의 파일들을 컨테이너의 작업 디렉토리로 복사
COPY . /app

MOUNT . /app/result
# requirements.txt에 명시된 패키지들 설치
RUN pip install --no-cache-dir -r requirements.txt

# 컨테이너 실행 시 기본 명령어 설정
CMD ["python", "app.py"]