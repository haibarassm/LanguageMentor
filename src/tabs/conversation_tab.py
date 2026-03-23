# tabs/conversation_tab.py

import gradio as gr
from agents.conversation_agent import ConversationAgent
from utils.logger import LOG

# 初始化对话代理
conversation_agent = ConversationAgent()

# 处理用户对话的函数
def handle_conversation(user_input, chat_history):
    if chat_history is None:
        chat_history = []
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[ChatBot]: {bot_message}")
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": bot_message})
    return chat_history, ""

def create_conversation_tab():
    with gr.Tab("对话"):
        gr.Markdown("## 练习英语对话")

        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",
            height=800,
        )

        with gr.Row():
            conversation_input = gr.Textbox(
                placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",
                show_label=False,
                scale=9
            )
            conversation_submit = gr.Button("发送", scale=1)
            conversation_clear = gr.Button("清除历史记录", scale=1)

        # 处理对话练习提交
        conversation_submit.click(
            fn=handle_conversation,
            inputs=[conversation_input, conversation_chatbot],
            outputs=[conversation_chatbot, conversation_input]
        )

        # 支持回车键提交
        conversation_input.submit(
            fn=handle_conversation,
            inputs=[conversation_input, conversation_chatbot],
            outputs=[conversation_chatbot, conversation_input]
        )

        # 清除历史记录
        conversation_clear.click(
            fn=lambda: [],
            outputs=conversation_chatbot
        )
