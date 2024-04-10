import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai

# NLTKリソースのダウンロード
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# コンテンツ収集関数
import requests
from bs4 import BeautifulSoup

def scrape_all_text(url):
    # ウェブサイトからHTMLを取得
    response = requests.get(url)
    if response.status_code == 200:
        # HTMLをBeautifulSoupで解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # <script>と<style>タグを削除
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # <body>タグからテキストを取得し、余分な空白を削除
        body_text = soup.body.get_text(separator=' ', strip=True)
        return body_text
    else:
        # ウェブサイトの内容の取得に失敗した場合
        return "Error: Unable to fetch the content from the website."

# テキストの要約
def text_explanation(text):
    model = genai.GenerativeModel('gemini-pro')
    # 2つの文章の組み合わせを作成
    combined_text = f"以下の文章を1フレーズに要約してください:\n1. {text}"

    # テキストの類似度とその根拠をリクエスト
    response = model.generate_content(combined_text)

    # 応答のテキスト部分を返す
    return response.text
#テキストを分割し、TF-IDFベクトルに変換後、文間の類似度を計算
def split_and_vectorize_text(text):
    embedding = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="SEMANTIC_SIMILARITY",)
    return embedding

def calculate_semantic_similarity(embedding1, embedding2):
    similarity_score = cosine_similarity([embedding1], [embedding2])[0][0]
    return similarity_score

#テキスト間を類似度を根拠に比較
def get_similarity_explanation_with_score(text1, text2, similarity_score):
    model = genai.GenerativeModel('gemini-pro')
    # 2つの文章の組み合わせを作成
    combined_text = f"""
以下の2つのテキストの類似度スコアは{similarity_score}です。このスコアの背後にある理由を、類似点と相違点を含めて詳しく説明してください。また、その説明を以下のテンプレートに従ってください。
**類似度スコアの根拠:**
[類似度の根拠についての説明]

**相違点:**
[相違点についての説明]
* **範囲:**
[相違点の範囲について]
* **詳細:**
[相違点の詳細について]
* **目的:**
[相違点の目的について]

**類似点:**
[類似点についての説明]
* **共通主題:**
[共通している主題について]

**まとめ**
[全体のまとめ]

1. {text1}
2. {text2}
"""
    # テキストの類似度とその根拠をリクエスト
    response = model.generate_content(combined_text)
    # 応答のテキスト部分を返す
    return response.text

#テキスト表示
def display_similar_documents(text1, text2, score):
    """
    Display pairs of similar documents using Streamlit.

    :param sentences: List of sentences/documents.
    :param similar_documents: List of tuples with the format (index1, index2, similarity_score).
    """
    with st.container():
        st.write(f"文章 {1}と文章 {2}の比較")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"文章 {1}")
            st.write(f"{text_explanation(text1)}")
        with col2:
            st.subheader(f"文章 {2}")
            st.write(f"{text_explanation(text2)}")

        st.write(f"類似度スコア: {score:.2f}")
        # Assuming get_similarity_explanation_with_score is a predefined function that takes two texts and a similarity score
        explanation = get_similarity_explanation_with_score(text1, text2, score)
        with st.expander("類似度の詳細分析"):
            st.write(explanation)

# This function is designed to work within a Streamlit app.
# It iterates over each pair of similar documents, displays their content side by side, and shows their similarity score.
# Additionally, it provides a detailed analysis of their similarity using an expandable Streamlit expander.

# Streamlitアプリのメイン部分
def main():
    # APIキー入力部分
    api_key = st.text_input("APIキーを入力してください:", value="", type="password")

    genai.configure(api_key=api_key)
    st.title('ウェブページテキストスクレイピングと類似度分析アプリ')

    # ユーザー入力部分
    user_input_url1 = st.text_input("分析するウェブページのURL1を入力してください:")
    user_input_url2 = st.text_input("分析するウェブページのURL2を入力してください:")

    # 分析ボタン
    if st.button('テキスト抽出と類似度分析'):
        # コンテンツ収集
        text1 = scrape_all_text(user_input_url1)
        text2 = scrape_all_text(user_input_url2)
        #テキストを分割し、TF-IDFベクトルに変換後、文間の類似度を計算
        result1 = split_and_vectorize_text(text1[:1000])
        result2 = split_and_vectorize_text(text2[:1000])
        # result1とresult2から埋め込みベクトルを抽出する
        embedding1 = result1['embedding']
        embedding2 = result2['embedding']

        # それらの埋め込みベクトルを用いて類似度を計算する
        similarity = calculate_semantic_similarity(embedding1, embedding2)
        display_similar_documents(text1, text2, similarity)

    else:
        st.error("URLが入力されていません。")

if __name__ == '__main__':
    main()
