import gradio as gr  # 导入 Gradio 库，用于构建用户界面
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from config import ConfigManager  # 导入配置管理器
from agents.conversation_agent import ConversationAgent  # 导入对话代理类
from agents.scenario_agent import ScenarioAgent  # 导入场景代理类
from utils.logger import LOG  # 导入日志记录工具

# 初始化配置管理器
config_manager = ConfigManager()

# 获取配置的模型提供商
model_provider = config_manager.get_model_provider()
LOG.info(f"Using model provider: {model_provider}")

# 创建 LLM 实例
if model_provider == "ollama":
    config = config_manager.get_ollama_config()
    llm = ChatOllama(
        model=config["model"],
        max_tokens=config.get("max_tokens", 8192),
        temperature=config.get("temperature", 0.8),
    )
elif model_provider == "siliconflow":
    config = config_manager.get_siliconflow_config()
    llm = ChatOpenAI(
        model=config["model"],
        api_key=config["api_key"],
        base_url="https://api.siliconflow.cn/v1",
        max_tokens=config.get("max_tokens", 8192),
        temperature=config.get("temperature", 0.8),
    )
else:
    raise ValueError(f"Unsupported model provider: {model_provider}")

# 创建对话代理实例，注入 LLM
conversation_agent = ConversationAgent(llm)

# 定义场景代理的选择与调用，注入 LLM
agents = {
    "job_interview": ScenarioAgent("job_interview", llm),  # 求职面试场景代理
    "hotel_checkin": ScenarioAgent("hotel_checkin", llm),  # 酒店入住场景代理
    "pet_medical_care": ScenarioAgent("pet_medical_care", llm),  # 宠物看病场景代理
    "renting": ScenarioAgent("renting", llm)  # 租房场景代理
}

# 处理用户对话的函数
def handle_conversation(user_input, chat_history):
    bot_message = conversation_agent.chat_with_history(user_input)  # 获取聊天机器人的回复
    LOG.info(f"[user]: {user_input}")  # 记录聊天机器人的回复
    LOG.info(f"[ChatBot]: {bot_message}")  # 记录聊天机器人的回复
    chat_history = chat_history + [(user_input, bot_message)]
    return chat_history, ""  # 返回更新后的聊天历史和清空输入框

# 获取场景介绍的函数
def get_scenario_intro(scenario):
    with open(f"content/page/{scenario}.md", "r") as file:  # 打开对应场景的介绍文件
        scenario_intro = file.read().strip()  # 读取文件内容并去除多余空白
    return scenario_intro  # 返回场景介绍内容

# 场景切换函数：更新介绍并启动新会话
def change_scenario(scenario):
    intro = get_scenario_intro(scenario)  # 获取场景介绍
    initial_ai_message = agents[scenario].start_new_session()  # 启动新会话并获取初始AI消息
    chat_history = [(None, initial_ai_message)]  # 创建新的聊天历史，包含初始AI消息
    LOG.info(f"[场景切换]: {scenario}, [初始消息]: {initial_ai_message}")
    return intro, chat_history  # 返回场景介绍和新的聊天历史

# 场景代理处理函数，根据选择的场景调用相应的代理
def handle_scenario(user_input, chat_history, scenario):
    bot_message = agents[scenario].chat_with_history(user_input)  # 获取场景代理的回复
    LOG.info(f"[ChatBot]: {bot_message}")  # 记录场景代理的回复
    chat_history = chat_history + [(user_input, bot_message)]
    return chat_history, ""  # 返回更新后的聊天历史和清空输入框

# Gradio 界面构建
with gr.Blocks(title="LanguageMentor 英语私教") as language_mentor_app:
    with gr.Tab("场景训练"):  # 场景训练标签
        gr.Markdown("## 选择一个场景完成目标和挑战")  # 场景选择说明

        # 创建单选框组件
        scenario_radio = gr.Radio(
            choices=[
                ("求职面试", "job_interview"),  # 求职面试选项
                ("酒店入住", "hotel_checkin"),  # 酒店入住选项
                ("租房", "renting"),  # 租房选项（注释掉）
                ("宠物看病", "pet_medical_care")  # 宠物看病选项
            ],
            value="pet_medical_care",  # 默认选中租房
            label="场景"  # 单选框标签
        )

        scenario_intro = gr.Markdown()  # 场景介绍文本组件

        # 存储当前场景的默认值
        scenario_default = gr.Textbox(value="pet_medical_care", visible=False)

        # 场景聊天组件
        scenario_chatbot = gr.Chatbot(
            label="对话历史",
            height=600,  # 聊天窗口高度
        )

        with gr.Row():
            scenario_input = gr.Textbox(
                placeholder="在这里输入你的回复...",
                show_label=False,
                scale=9
            )
            scenario_submit = gr.Button("发送", scale=1)
            scenario_clear = gr.Button("清除历史记录", scale=1)

        # 当场景选择变化时，更新场景介绍并重置聊天
        scenario_radio.change(
            fn=change_scenario,
            inputs=scenario_radio,
            outputs=[scenario_intro, scenario_chatbot]
        )

        # 页面加载时自动加载默认场景
        language_mentor_app.load(
            fn=change_scenario,
            inputs=scenario_default,
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

    with gr.Tab("对话练习"):  # 对话练习标签
        gr.Markdown("## 练习英语对话 ")  # 对话练习说明

        # 对话练习聊天组件
        conversation_chatbot = gr.Chatbot(
            label="对话历史",
            height=800,  # 聊天窗口高度
        )

        with gr.Row():
            conversation_input = gr.Textbox(
                placeholder="在这里输入你的回复...",
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

# 启动应用
if __name__ == "__main__":
    language_mentor_app.launch(share=True, server_name="0.0.0.0")  # 启动 Gradio 应用并共享
