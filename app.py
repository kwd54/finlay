import streamlit as st
import openai
import fitz # PyMuPDF

st.title("📊 FinLay - 決算書AI要約ツール改")

def get_api_key():
    """
    Sidebarにキー入力欄を出す。
    入力値はst.session_stateだけに保持し、どこにも保存しない。
    """
    return st.sidebar.text_input("OpenAI API Key", type="password", key="OPENAI_API_KEY").strip()

def extract_and_summarize(uploaded_file):
    # PDFからテキスト抽出
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    # GPTで要約
    prompt = f"""
{st.secrets["PROMPT"]}

{text[:1000]}"""  # ※API制限あるので最初は1000字程度でカット
    
    print(prompt)

    # response = openai.ChatCompletion.create(
    #     model="gpt-4.1-nano",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.2,
    # )

    # return response["choices"][0]["message"]["content"]
    return prompt


uploaded_file = st.file_uploader("決算書PDFをアップロード", type="pdf")

user_key = get_api_key()
if not user_key:
    st.info("まずはご自身の OpenAI API Key を入力してください。")
    st.stop()
openai.api_key = user_key

if uploaded_file:
    with st.spinner("要約中..."):
        summary = extract_and_summarize(uploaded_file)
        st.success("要約完了！")
        st.markdown(summary)
