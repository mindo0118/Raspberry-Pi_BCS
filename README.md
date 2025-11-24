# 📸 MQTT 기반 공유 스마트 사진부스  
Raspberry Pi 3대를 활용한 분산 스마트 포토부스 시스템 — 촬영 · 웹서버 · 통계 분리 구조

---

## 🌟 프로젝트 개요

사용자에게 더 다양한 기능과 편의를 제공하기 위해 개발된 **차세대 스마트 사진 부스 시스템**입니다.  
3대의 라즈베리파이를 기반으로 **촬영 · 웹 표시 · 통계 처리**를 분산하여 안정성과 확장성을 높인 것이 특징입니다.


| https://github.com/user-attachments/assets/245de9b0-3def-4ded-bd83-9f99c2d21b21 | 

https://github.com/user-attachments/assets/1ecc0e89-dcc7-4c47-adfe-5c4ee20880c8

 |


---

## 📦 프로젝트 구조 예시
```
/project
├── pi1_camera_sender/
├── pi2_receiver_web/
├── pi3_controller_stats/
└── README.md
```
---
## ✨ 주요 기능

### 📷 사용자 친화적 촬영 환경
- 버튼·리모컨·조이스틱 기반 간편 촬영  
- OLED 디스플레이 2개로 **실시간 포즈·표정 추천**

### ⚙️ 하드웨어 기능
- 서보모터로 카메라 **상하좌우 각도 조절**  
- LED, 버튼, 카메라 모듈 기반 인터랙션 제공

### 📡 MQTT 이미지 전송
- 촬영 이미지를 base64로 인코딩하여 MQTT로 전송  
- JSON 기반 메타데이터 포함 (topic, timestamp 등)

### 🔗 QR 코드 즉시 공유
- 촬영 직후 QR 코드 생성 → 웹 페이지에서 바로 확인·다운로드 가능

### 🗂 토픽 기반 사진 분류
- me / family / couple / friend 등 **토픽별 폴더 자동 분류**  
- 웹 갤러리 UI로 사진 조회

---

## 💻 개발 환경 및 사용 기술

| 구분 | 내용 |
|---|---|
| **하드웨어** | Raspberry Pi 3대, 서보모터, OLED(2개), LED, 버튼, 카메라 모듈 |
| **통신** | MQTT (Mosquitto 기반) |
| **데이터 처리** | base64 이미지 인코딩/디코딩, JSON 파싱 |
| **소프트웨어** | Flask 웹 서버, QR 코드 생성, OpenCV 카메라 촬영 |

---

## 🏗 시스템 아키텍처 (3-Tier 분산 구조)

<img width="1271" height="640" alt="image" src="https://github.com/user-attachments/assets/57b9fd91-579a-4e15-88bc-8d17a1dd0725" />

---

## 👥 팀 구성 및 역할

| **민도현** | **김다연**  |   **김민정**  |  
| :------------: | :------------: | :------------: | 
| <img src="https://github.com/user-attachments/assets/7d5b65b3-3751-4c6a-b4bc-69b742cc3053" width=180> |  <img src="https://github.com/user-attachments/assets/47ec901d-ee5e-4259-8d4b-064f10562f17" width=170> | <img src="https://github.com/user-attachments/assets/a2effb4f-3521-48f4-8d66-512d270aeead" width=160> |  
| **github**: [mindo0118](https://github.com/mindo0118)|**github**: [double2-22](https://github.com/double2-22) | **github**: [gnujnim475](https://github.com/gnujnim475) |  
| ![Team%20Leader](https://img.shields.io/badge/-Team%20leader-yellow) </br>  MQTT 통신, 디코딩·폴더 저장, LED/서보/OLED 제어 | 외형 제작, OLED 연결, base64/JSON 처리, QR 생성, 폴더 선택 UI | 외형 제작, 버튼/카메라 연결, base64/JSON 처리, 촬영·QR UI | 
---

## 🔧 향후 개선 사항

1. **원거리 조작 강화** — 리모컨·조이스틱 기능 보완  
2. **비밀번호 기반 접근 제한** — 특정 사진 잠금 기능  
3. **개인 저장 옵션 추가** — 공유/개인 저장 선택 버튼 제공  
4. **통계 페이지 완성** — QR 접속 수·촬영 수 시각화  
5. **하드웨어 개선** — LED 밝기, 스위치 내구성 개선

---

