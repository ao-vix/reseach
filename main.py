import streamlit as st
st.set_page_config(page_title="Virtual Family", layout="wide")  # これを一番上に移動

from st_chat import chat_app
from st_fish import fish_app

# ページのタイトル
st.title("バーチャルファミリー")

# 画面レイアウト：左3分の1に水槽、右3分の2にチャット
col1, col2 = st.columns([1, 2])

# 左側（3分の1）に水槽のイラストを表示
with col1:
    fish_app()

# 右側（3分の2）にチャットアプリを表示
with col2:
    chat_app()




#streamlit run main.py
