import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def fish_app():
    st.title('')

    try:
        kingyo_image = Image.open('kingyo.png')
    except FileNotFoundError:
        st.error('Error: "kingyo.png" が見つかりません。画像ファイルを同じディレクトリに配置してください。')
        st.stop()

    # size_scaleの初期化と取得
    if 'size_scale' not in st.session_state:
        st.session_state.size_scale = 0.5
    size_scale = st.session_state.size_scale

    # グラフの設定と背景
    fig, ax = plt.subplots(figsize=(6, 6))
    rect = plt.Rectangle((0, 0), 1, 0.6, linewidth=3, edgecolor='black', facecolor='lightblue')
    ax.add_patch(rect)

    # 波の描画
    x = np.linspace(0, 1, 100)
    y = 0.5 + 0.02 * np.sin(10 * np.pi * x)
    ax.fill_between(x, 0, y, color='blue', alpha=0.6)

    # 金魚画像の位置とサイズを調整
    center_x, center_y = 0.5, 0.2
    width, height = 0.2 * size_scale, 0.15 * size_scale

    # 金魚画像の描画
    ax.imshow(kingyo_image, aspect='auto', extent=(
        center_x - width / 2,
        center_x + width / 2,
        center_y - height / 2,
        center_y + height / 2
    ), zorder=10)
    
    # 軸の設定を非表示
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.6)
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # 画像を表示
    st.pyplot(fig)


