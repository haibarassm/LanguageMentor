# tabs/vocab_tab.py

import gradio as gr
from agents.vocab_agent import VocabAgent
from utils.logger import LOG

# 初始化词汇代理
vocab_agent = VocabAgent()

# 定义功能名称
feature = "vocab_study"

# 获取页面描述
def get_page_desc(feature):
    try:
        with open(f"content/page/{feature}.md", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        LOG.error(f"词汇学习介绍文件 content/page/{feature}.md 未找到！")
        return "词汇学习介绍文件未找到。"

# 重新启动词汇学习聊天机器人会话
def restart_vocab_study_chatbot():
    vocab_agent.restart_session()
    _next_round = "Let's do it"
    bot_message = vocab_agent.chat_with_history(_next_round)
    return [
        {"role": "user", "content": _next_round},
        {"role": "assistant", "content": bot_message}
    ]

# 处理用户输入的单词学习消息
def handle_vocab(user_input, chat_history):
    if chat_history is None:
        chat_history = []
    bot_message = vocab_agent.chat_with_history(user_input)
    LOG.info(f"[Vocab ChatBot]: {bot_message}")
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": bot_message})
    return chat_history, ""

# 创建词汇学习的 Tab 界面
def create_vocab_tab():
    with gr.Tab("单词"):
        gr.Markdown("## 闯关背单词")

        # 显示从文件中获取的页面描述
        gr.Markdown(get_page_desc(feature))

        # 初始化聊天机器人组件
        vocab_study_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>开始学习新单词吧！",
            height=800,
        )

        with gr.Row():
            vocab_input = gr.Textbox(
                placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>开始学习新单词吧！",
                show_label=False,
                scale=9
            )
            vocab_submit = gr.Button("发送", scale=1)
            restart_btn = gr.Button("下一关", scale=1)

        # 当用户点击下一关按钮时
        restart_btn.click(
            fn=restart_vocab_study_chatbot,
            inputs=None,
            outputs=vocab_study_chatbot,
        )

        # 处理词汇学习提交
        vocab_submit.click(
            fn=handle_vocab,
            inputs=[vocab_input, vocab_study_chatbot],
            outputs=[vocab_study_chatbot, vocab_input]
        )

        # 支持回车键提交
        vocab_input.submit(
            fn=handle_vocab,
            inputs=[vocab_input, vocab_study_chatbot],
            outputs=[vocab_study_chatbot, vocab_input]
        )
