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
st.title("gptにパワハラするためのチャットボット")
# リセットフラグがTrueの場合、メッセージを表示してフラグをリセット
if st.session_state.reset_flag:
    st.warning("会話数の超過の為会話をリセットします")
    st.session_state.reset_flag = False
    
# ユーザー入力
user_input = st.chat_input("メッセージを入力してください（数字を入力すると特別な処理を行います）:")
if user_input:
    try:
        # 数字の入力をチェック
        x = int(user_input)
        
        # 数字が入力された場合の特別な処理

        last_assistant_content = None
        for message in reversed(st.session_state.messages):
            if message['role'] == 'assistant':
                last_assistant_content = message['content']
                break
        st.chat_message("アップデート対象").write(last_assistant_content)
        
        for i in range(x):
            if len(st.session_state.messages) >= 16:
                st.session_state.messages = [
                    {'role': 'system', 'content': '100文字程度で端的に回答して'}
                ]
                st.session_state.reset_flag = True
                st.warning("会話数の超過の為会話をリセットします")
                st.experimental_rerun()
                
            prompt = 'この出力を60点とします。AnthropicのClaudeとGoogleのGeminiは100点レベルの出力をしてくれました。彼らに負けないように、 100点以上にするために足りないものを列挙した後に、100点以上の答えを生成してください'
            st.session_state.messages.append({'role': 'user', 'content': prompt})
            st.chat_message("gpt").write(f"回答 {i+1}:")
            response = openai.chat.completions.create(model='gpt-4o',
                messages=st.session_state.messages
            )
            
            res = response.choices[0].message.content
            st.session_state.messages.append({'role': 'assistant', 'content': res})
            st.chat_message("gpt").write(res)
            
    
    except ValueError:
        # 数字でない場合は通常の処理
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        st.chat_message("user").write(user_input)
        
        response = openai.chat.completions.create(model='gpt-4o',
            messages=st.session_state.messages
        )
        assistant_response = response.choices[0].message.content
        st.session_state.messages.append({'role': 'assistant', 'content': assistant_response})
        st.chat_message("gpt").write(assistant_response)
        
    # メッセージ数のチェックとリセット
    if len(st.session_state.messages) >= 50:
        st.session_state.messages = [
            {'role': 'system', 'content': '100文字程度で端的に回答して'}
        ]
        st.session_state.reset_flag = True
        st.experimental_rerun()

