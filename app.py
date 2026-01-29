"""
Gradio Chatbot using Groq API (Free Tier)

Groq provides free access to high-performance LLM models like Llama 3, Mixtral, etc.
Free tier includes: 30 requests/minute, 14,400 requests/day

To get your free API key:
1. Visit https://console.groq.com/
2. Sign up for a free account
3. Create an API key
4. Set it as environment variable: export GROQ_API_KEY="your-key"
   Or create a .env file with: GROQ_API_KEY=your-key
"""

import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Available free models on Groq
AVAILABLE_MODELS = {
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it",
}

# Default model
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def create_client():
    """Create Groq client with API key."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def chat(message: str, history: list, model_name: str, system_prompt: str):
    """
    Chat function that processes user messages and returns AI responses.

    Args:
        message: Current user message
        history: List of previous message pairs [[user, assistant], ...]
        model_name: Selected model display name
        system_prompt: System prompt for the AI

    Yields:
        Streaming response text
    """
    client = create_client()

    if client is None:
        yield "⚠️ GROQ_API_KEY가 설정되지 않았습니다.\n\n" \
              "무료 API 키를 받으려면:\n" \
              "1. https://console.groq.com/ 에 접속\n" \
              "2. 무료 계정 생성\n" \
              "3. API 키 생성\n" \
              "4. 환경변수 설정: export GROQ_API_KEY='your-key'\n" \
              "   또는 .env 파일에 GROQ_API_KEY=your-key 추가"
        return

    # Get the model ID from display name
    model_id = AVAILABLE_MODELS.get(model_name, DEFAULT_MODEL)

    # Build messages list
    messages = []

    # Add system prompt if provided
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})

    # Add conversation history
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

    # Add current message
    messages.append({"role": "user", "content": message})

    try:
        # Create streaming completion
        stream = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
            stream=True,
        )

        # Stream the response
        response_text = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
                yield response_text

    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower():
            yield f"⚠️ API 호출 제한에 도달했습니다. 잠시 후 다시 시도해주세요.\n\n오류: {error_msg}"
        elif "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
            yield f"⚠️ API 키가 유효하지 않습니다. 키를 확인해주세요.\n\n오류: {error_msg}"
        else:
            yield f"⚠️ 오류가 발생했습니다: {error_msg}"


def clear_history():
    """Clear the chat history."""
    return [], ""


# Custom CSS
CUSTOM_CSS = """
.chatbot-container { height: 500px !important; }
footer { display: none !important; }
"""

# Create Gradio interface
with gr.Blocks(title="무료 AI 챗봇") as demo:
    gr.Markdown(
        """
        # 🤖 무료 AI 챗봇

        **Groq API**를 사용한 무료 AI 챗봇입니다.
        Llama 3.3, Mixtral 등 고성능 모델을 무료로 사용할 수 있습니다.

        > 💡 API 키가 필요합니다. [Groq Console](https://console.groq.com/)에서 무료로 발급받으세요.
        """
    )

    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                label="대화",
                height=500,
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="메시지",
                    placeholder="여기에 메시지를 입력하세요...",
                    scale=8,
                    show_label=False,
                )
                submit_btn = gr.Button("전송", variant="primary", scale=1)

            with gr.Row():
                clear_btn = gr.Button("🗑️ 대화 초기화", variant="secondary")

        with gr.Column(scale=1):
            model_dropdown = gr.Dropdown(
                choices=list(AVAILABLE_MODELS.keys()),
                value="Llama 3.3 70B",
                label="모델 선택",
                info="사용할 AI 모델을 선택하세요",
            )

            system_prompt = gr.Textbox(
                label="시스템 프롬프트",
                placeholder="AI의 역할이나 성격을 정의하세요...",
                lines=5,
                value="당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 대화합니다.",
            )

            gr.Markdown(
                """
                ### 📋 사용 가능한 모델
                - **Llama 3.3 70B**: 가장 강력한 모델
                - **Llama 3.1 8B**: 빠른 응답
                - **Mixtral 8x7B**: 균형잡힌 성능
                - **Gemma 2 9B**: Google의 경량 모델

                ### 🔑 API 키 설정
                ```bash
                export GROQ_API_KEY="your-key"
                ```
                또는 `.env` 파일 생성:
                ```
                GROQ_API_KEY=your-key
                ```
                """
            )

    # Event handlers
    def respond(message, chat_history, model, system):
        if not message.strip():
            return "", chat_history

        chat_history = chat_history + [[message, ""]]
        return "", chat_history

    def bot_response(chat_history, model, system):
        if not chat_history:
            return chat_history

        message = chat_history[-1][0]
        history = chat_history[:-1]

        for response in chat(message, history, model, system):
            chat_history[-1][1] = response
            yield chat_history

    # Submit message on Enter or button click
    msg.submit(
        respond,
        [msg, chatbot, model_dropdown, system_prompt],
        [msg, chatbot],
    ).then(
        bot_response,
        [chatbot, model_dropdown, system_prompt],
        chatbot,
    )

    submit_btn.click(
        respond,
        [msg, chatbot, model_dropdown, system_prompt],
        [msg, chatbot],
    ).then(
        bot_response,
        [chatbot, model_dropdown, system_prompt],
        chatbot,
    )

    # Clear button
    clear_btn.click(
        lambda: ([], ""),
        outputs=[chatbot, msg],
    )


if __name__ == "__main__":
    print("🚀 챗봇 서버를 시작합니다...")
    print("💡 GROQ_API_KEY 환경변수가 설정되어 있는지 확인하세요.")
    print("🔗 https://console.groq.com/ 에서 무료 API 키를 발급받을 수 있습니다.\n")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        theme=gr.themes.Soft(),
        css=CUSTOM_CSS,
    )
