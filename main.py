import streamlit as st
import random
import os
import json

# ファイルパスの設定
QUESTIONS_FILE = 'questions.json'
DEFAULT_FILE = 'default.json'

# アプリのタイトル
st.title("インタビュー対策アプリ")

# 質問リストの読み込み
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error(f"{QUESTIONS_FILE} の内容が無効です。正しいJSON形式に修正してください。")
            return []
    else:
        st.error("質問ファイルが見つかりません。`questions.json`を作成してください。")
        return []

# デフォルトリストの読み込み
def load_default_list():
    if not os.path.exists(DEFAULT_FILE):
        with open(DEFAULT_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    try:
        with open(DEFAULT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error(f"{DEFAULT_FILE} の内容が無効です。正しいJSON形式に修正してください。")
        return []

# デフォルトリストの保存
def save_default_list(data):
    with open(DEFAULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# セッションステートの初期化
if 'unconfident_questions' not in st.session_state:
    st.session_state.unconfident_questions = load_default_list()

if 'current_question' not in st.session_state:
    st.session_state.current_question = None

# サイドバーのメニュー
st.sidebar.title("メニュー")
options = ["質問に答える", "対策すべき質問を見る", "対策リストをクリア"]
choice = st.sidebar.radio("選択してください", options)

# 質問に答えるページ
if choice == "質問に答える":
    st.header("質問に答えてください")

    questions = load_questions()
    if not questions:
        st.stop()

    if st.button("次の質問を表示"):
        available_questions = list(set(questions) - set(st.session_state.unconfident_questions))
        if available_questions:
            st.session_state.current_question = random.choice(available_questions)
        else:
            st.session_state.current_question = None
            st.info("これ以上の質問がありません。対策リストを見直してください。")

    if st.session_state.current_question:
        st.subheader("質問：")
        st.write(st.session_state.current_question)

        if st.button("自信がない"):
            st.write(st.session_state.current_question)
            if st.session_state.current_question not in st.session_state.unconfident_questions:
                st.session_state.unconfident_questions.append(st.session_state.current_question)
                save_default_list(st.session_state.unconfident_questions)
                st.success("この質問を対策リストに追加しました。")
            else:
                st.info("この質問はすでに対策リストに含まれています。")
            # 質問をリセット（ボタンが押された場合のみ）
            st.session_state.current_question = None
    else:
        st.info("質問を表示するには「次の質問を表示」ボタンをクリックしてください。")

# 対策すべき質問を見るページ
elif choice == "対策すべき質問を見る":
    st.header("対策すべき質問リスト")
    if st.session_state.unconfident_questions:
        for idx, q in enumerate(st.session_state.unconfident_questions, 1):
            st.write(f"{idx}. {q}")

        if st.button("全ての対策リストを削除"):
           
            st.session_state.unconfident_questions = []
            save_default_list(st.session_state.unconfident_questions)
            st.success("全ての対策リストを削除しました。")
    else:
        st.info("現在、対策すべき質問はありません。")


       