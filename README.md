# Env기술 백엔드 공고

## 📖 [사용자 가이드 및 개발 산출물](https://docs.google.com/document/d/11kZqcgO5hj7WdrPIEkNJb-CIvaZipfpZZrm1cA8tIBg/edit?usp=sharing)


### APP 실행 명령어 (도커용)
```
$ cd /{project-root}
$ docker-compose up app --build
```
#### APP 실행
```
$ pip install -r requirements.txt
$ DEBUG=on python app.py
```


#### 테스트 실행 명령어 (도커용)
```
$ cd /{project-root}
$ docker-compose up tests --build
```
#### 테스트 실행
```
$ cd proejct-kiwipiepy
$ DEBUG=on python -m pytest
```


### 프로젝트 구조

```
project-root
├── src
│   ├── libs
│   │   ├── const.py
│   │   ├── debug.py
│   │   └── handler.py
│   └── resource
│       ├── comments.csv
│       └── userDict.txt
├── app.py             # 메인 파일
├── docker-compose.yml
└── requirements.txt
```

#### 만약, 실행이 안된다면 CodeSandBox을 확인해주십시오.
🌎 [Replit으로 프로젝트 확인하기](https://replit.com/join/kqzsxynego-havingdlrow)
