import streamlit as st
import openai
# OpenAI APIキーの設定
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    st.write("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
openai.api_key = openai_api_key

# セッション状態の初期化
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {'role': 'system', 'content': '100文字程度で端的に回答して'}
    ]
if 'reset_flag' not in st.session_state:
    st.session_state.reset_flag = False
st.title("ChatGPTスタイルのチャットボット")
# リセットフラグがTrueの場合、メッセージを表示してフラグをリセット
if st.session_state.reset_flag:
    st.warning("会話をリセットしました。")
    st.session_state.reset_flag = False
# ユーザー入力
user_input = st.text_input("メッセージを入力してください（数字を入力すると特別な処理を行います）:")
if user_input:
    try:
        # 数字の入力をチェック
        x = int(user_input)
        
        # 数字が入力された場合の特別な処理
        
        for i in range(x):
            prompt = 'この出力を60点とします。これを60点としたときに100点とはどのようなものですか？100点になるために足りないものを列挙し、その後に100点の回答を生成してください'
            st.session_state.messages.append({'role': 'user', 'content': prompt})
            
            response = openai.chat.completions.create(model='gpt-4o',
                messages=st.session_state.messages
            )
            
            res = response.choices[0].message.content
            st.session_state.messages.append({'role': 'assistant', 'content': res})
            
            st.write(f"回答 {i+1}:")
            st.write(res)
    
    except ValueError:
        # 数字でない場合は通常の処理
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        response = openai.chat.completions.create(model='gpt-4o',
            messages=st.session_state.messages
        )
        assistant_response = response.choices[0].message.content
        st.session_state.messages.append({'role': 'assistant', 'content': assistant_response})
    # メッセージ数のチェックとリセット
    if len(st.session_state.messages) >= 11:
        st.session_state.messages = [
            {'role': 'system', 'content': '100文字程度で端的に回答して'}
        ]
        st.session_state.reset_flag = True
        st.experimental_rerun()
# チャット履歴の表示（全ての対話を含む）
for message in st.session_state.messages[1:]:  # システムメッセージをスキップ
    if message['role'] == 'user':
        st.write("You: " + message['content'])
    else:
        st.write("Assistant: " + message['content'])
