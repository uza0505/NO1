# 무료 AI 챗봇 (Gradio + Groq)

Groq API를 사용한 무료 AI 챗봇입니다. Llama 3.3, Mixtral 등 고성능 모델을 무료로 사용할 수 있습니다.

## 특징

- **무료**: Groq API 무료 티어 사용 (30 요청/분, 14,400 요청/일)
- **고성능 모델**: Llama 3.3 70B, Mixtral 8x7B 등 지원
- **스트리밍**: 실시간 응답 스트리밍
- **커스터마이징**: 시스템 프롬프트로 AI 성격 설정 가능

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. API 키 설정

[Groq Console](https://console.groq.com/)에서 무료 API 키를 발급받으세요.

**방법 1: 환경변수 설정**
```bash
export GROQ_API_KEY="your-api-key"
```

**방법 2: .env 파일 생성**
```bash
cp .env.example .env
# .env 파일을 열어 API 키 입력
```

### 3. 실행

```bash
python app.py
```

브라우저에서 http://localhost:7860 으로 접속하세요.

## 사용 가능한 모델

| 모델 | 설명 |
|------|------|
| Llama 3.3 70B | 가장 강력한 모델, 복잡한 작업에 적합 |
| Llama 3.1 8B | 빠른 응답 속도, 간단한 대화에 적합 |
| Mixtral 8x7B | 균형 잡힌 성능 |
| Gemma 2 9B | Google의 경량 모델 |

## 스크린샷

실행 후 다음과 같은 웹 인터페이스가 표시됩니다:
- 왼쪽: 대화 영역
- 오른쪽: 모델 선택 및 시스템 프롬프트 설정

## 라이선스

MIT License
