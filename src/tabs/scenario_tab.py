# tabs/scenario_tab.py

import gradio as gr
from agents.scenario_agent import ScenarioAgent
from utils.logger import LOG

# 初始化场景代理
agents = {
    "job_interview": ScenarioAgent("job_interview"),
    "hotel_checkin": ScenarioAgent("hotel_checkin"),
    # 可以根据需要添加更多场景代理
}

def get_page_desc(scenario):
    try:
        with open(f"content/page/{scenario}.md", "r", encoding="utf-8") as file:
            scenario_intro = file.read().strip()
        return scenario_intro
    except FileNotFoundError:
        LOG.error(f"场景介绍文件 content/page/{scenario}.md 未找到！")
        return "场景介绍文件未找到。"

# 场景代理处理函数，根据选择的场景调用相应的代理
def handle_scenario(user_input, chat_history, scenario):
    if chat_history is None:
        chat_history = []
    if scenario is None:
        return chat_history + [{"role": "assistant", "content": "请先选择一个场景！"}], ""
    bot_message = agents[scenario].chat_with_history(user_input)
    LOG.info(f"[ChatBot]: {bot_message}")
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": bot_message})
    return chat_history, ""

# 当场景选择变化时，更新场景介绍并重置聊天
def update_scenario(scenario):
    if scenario is None:
        return "", []
    desc = get_page_desc(scenario)
    initial_message = agents[scenario].start_new_session()
    return desc, [{"role": "assistant", "content": initial_message}]

def create_scenario_tab():
    with gr.Tab("场景"):
        gr.Markdown("## 选择一个场景完成目标和挑战")

        # 创建单选框组件
        scenario_radio = gr.Radio(
            choices=[
                ("求职面试", "job_interview"),
                ("酒店入住", "hotel_checkin"),
            ],
            label="场景"
        )

        scenario_intro = gr.Markdown()
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",
            height=600,
        )

        with gr.Row():
            scenario_input = gr.Textbox(
                placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",
                show_label=False,
                scale=9
            )
            scenario_submit = gr.Button("发送", scale=1)
            scenario_clear = gr.Button("清除历史记录", scale=1)

        # 当场景选择变化时，更新场景介绍并重置聊天
        scenario_radio.change(
            fn=update_scenario,
            inputs=scenario_radio,
            outputs=[scenario_intro, scenario_chatbot]
        )

        # 处理场景对话提交
        scenario_submit.click(
            fn=handle_scenario,
            inputs=[scenario_input, scenario_chatbot, scenario_radio],
            outputs=[scenario_chatbot, scenario_input]
        )

        # 支持回车键提交
        scenario_input.submit(
            fn=handle_scenario,
            inputs=[scenario_input, scenario_chatbot, scenario_radio],
            outputs=[scenario_chatbot, scenario_input]
        )

        # 清除历史记录
        scenario_clear.click(
            fn=lambda: [],
            outputs=scenario_chatbot
        )
