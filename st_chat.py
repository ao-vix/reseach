import streamlit as st
import torch
from transformers import AutoTokenizer
from model import load_model, generate_response

@st.cache_resource
def get_model_and_tokenizer(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = load_model(model_name)
    return model, tokenizer

# 定数の定義
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = "あなたは日本の心理カウンセラーです.悩みに強く優しく共感をしてください．文末は読点で終わるようにしてください．"

# モデルのロード
model_name = "elyza/ELYZA-japanese-Llama-2-7b-instruct"
model, tokenizer = get_model_and_tokenizer(model_name)

# プロンプトのフォーマット
def format_prompt(system_prompt, user_input):
    return "{bos_token}{b_inst} {system}{prompt} {e_inst} ".format(
        bos_token=tokenizer.bos_token,
        b_inst=B_INST,
        system=f"{B_SYS}{system_prompt}{E_SYS}",
        prompt=user_input,
        e_inst=E_INST,
    )

def chat_app():
    st.title("")
    st.write("なんでも相談してみてください．終了するには 'ありがとうございました' と入力してください．")

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # サイズ変更の初期化
    if 'size_scale' not in st.session_state:
        st.session_state.size_scale = 0.5

    system_prompt = DEFAULT_SYSTEM_PROMPT
    user_input = st.text_input("あなた: ")
    send_button = st.button("送信")

    # チャット送信ボタンが押された場合
    if send_button and user_input:
        # サイズの増加
        #st.session_state.size_scale += 0.05  # チャット送信ごとにサイズを増加
        st.session_state.size_scale += 0.5



        if user_input.lower() == "ありがとうございました":
            st.session_state.conversation.append(("あなた", user_input))
            st.session_state.conversation.append(("バーチャルファミリー", "こちらこそありがとうございました"))
        else:
            prompt = format_prompt(system_prompt, user_input)
            response = generate_response(model, tokenizer, prompt)
            st.session_state.conversation.append(("あなた", user_input))
            st.session_state.conversation.append(("バーチャルファミリー", response))

    def format_message(speaker, message, align_right=False):
        if align_right:
            st.markdown(f"""
            <div style='display: flex; justify-content: flex-end;'>
                <div style='background-color: #DCF8C6; color: black; padding: 10px; border-radius: 10px; max-width: 60%;'>
                    <strong>{speaker}:</strong> {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='display: flex; justify-content: flex-start;'>
                <div style='background-color: #E0E0E0; color: black; padding: 10px; border-radius: 10px; max-width: 60%;'>
                    <strong>{speaker}:</strong> {message}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # チャット履歴の表示
    if st.session_state.conversation:
        for speaker, message in st.session_state.conversation:
            if speaker == "あなた":
                format_message(speaker, message, align_right=True)
            else:
                format_message(speaker, message, align_right=False)
