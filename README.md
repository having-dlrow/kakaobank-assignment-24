# Env기술 백엔드 공고

## 📖 [사용자 가이드 및 개발 산출물](https://docs.google.com/document/d/11kZqcgO5hj7WdrPIEkNJb-CIvaZipfpZZrm1cA8tIBg/edit?usp=sharing)


### APP 실행 명령어
```
$ cd /{project-root}
$ docker-compose up app --build
```

### 테스트 실행 명령어
```
$ cd /{project-root}
$ docker-compose up tests --build
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
🌎 [code_sandbox로 프로젝트 확인하기](https://codesandbox.io/p/github/having-dlrow/project-kiwipiepy/master?import=true&embed=1&file=%2F.gitignore&layout=%257B%2522sidebarPanel%2522%253A%2522GIT%2522%252C%2522rootPanelGroup%2522%253A%257B%2522direction%2522%253A%2522horizontal%2522%252C%2522contentType%2522%253A%2522UNKNOWN%2522%252C%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522id%2522%253A%2522ROOT_LAYOUT%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522UNKNOWN%2522%252C%2522direction%2522%253A%2522vertical%2522%252C%2522id%2522%253A%2522clupakak80006356jyxlkivnw%2522%252C%2522sizes%2522%253A%255B100%252C0%255D%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522EDITOR%2522%252C%2522direction%2522%253A%2522horizontal%2522%252C%2522id%2522%253A%2522EDITOR%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL%2522%252C%2522contentType%2522%253A%2522EDITOR%2522%252C%2522id%2522%253A%2522clupakak70002356je12pbo2o%2522%257D%255D%257D%252C%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522SHELLS%2522%252C%2522direction%2522%253A%2522horizontal%2522%252C%2522id%2522%253A%2522SHELLS%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL%2522%252C%2522contentType%2522%253A%2522SHELLS%2522%252C%2522id%2522%253A%2522clupakak70004356jqfeduwhm%2522%257D%255D%252C%2522sizes%2522%253A%255B100%255D%257D%255D%257D%252C%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522DEVTOOLS%2522%252C%2522direction%2522%253A%2522vertical%2522%252C%2522id%2522%253A%2522DEVTOOLS%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL%2522%252C%2522contentType%2522%253A%2522DEVTOOLS%2522%252C%2522id%2522%253A%2522clupakak70005356jkn4jedak%2522%257D%255D%252C%2522sizes%2522%253A%255B100%255D%257D%255D%252C%2522sizes%2522%253A%255B40%252C60%255D%257D%252C%2522tabbedPanels%2522%253A%257B%2522clupakak70002356je12pbo2o%2522%253A%257B%2522tabs%2522%253A%255B%257B%2522id%2522%253A%2522clupakak70001356j5etl5y0w%2522%252C%2522mode%2522%253A%2522permanent%2522%252C%2522type%2522%253A%2522FILE%2522%252C%2522filepath%2522%253A%2522%252F.gitignore%2522%257D%255D%252C%2522id%2522%253A%2522clupakak70002356je12pbo2o%2522%252C%2522activeTabId%2522%253A%2522clupakak70001356j5etl5y0w%2522%257D%252C%2522clupakak70005356jkn4jedak%2522%253A%257B%2522id%2522%253A%2522clupakak70005356jkn4jedak%2522%252C%2522activeTabId%2522%253A%2522clupapyt400co356jwkj8uvn8%2522%252C%2522tabs%2522%253A%255B%257B%2522type%2522%253A%2522SETUP_TASKS%2522%252C%2522id%2522%253A%2522clupapyt400co356jwkj8uvn8%2522%252C%2522mode%2522%253A%2522permanent%2522%257D%255D%257D%252C%2522clupakak70004356jqfeduwhm%2522%253A%257B%2522id%2522%253A%2522clupakak70004356jqfeduwhm%2522%252C%2522activeTabId%2522%253A%2522clupakak70003356jn9lbmhfq%2522%252C%2522tabs%2522%253A%255B%257B%2522id%2522%253A%2522clupakak70003356jn9lbmhfq%2522%252C%2522mode%2522%253A%2522permanent%2522%252C%2522type%2522%253A%2522TERMINAL%2522%252C%2522shellId%2522%253A%2522clupak9cx000oddjfhxzg5ji2%2522%257D%252C%257B%2522type%2522%253A%2522TASK_LOG%2522%252C%2522taskId%2522%253A%2522CSB_RUN_OUTSIDE_CONTAINER%253D1%2520devcontainer%2520templates%2520apply%2520--template-id%2520%255C%2522ghcr.io%252Fdevcontainers%252Ftemplates%252Fpython%255C%2522%2520--template-args%2520%27%257B%257D%27%2520--features%2520%27%255B%255D%27%2522%252C%2522id%2522%253A%2522clupapnxg006j356jem1w3iep%2522%252C%2522mode%2522%253A%2522permanent%2522%257D%255D%257D%257D%252C%2522showDevtools%2522%253Atrue%252C%2522showShells%2522%253Afalse%252C%2522showSidebar%2522%253Atrue%252C%2522sidebarPanelSize%2522%253A15%257D)

