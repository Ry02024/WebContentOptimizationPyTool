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
def split_and_vectorize_text(text, min_length=20):
    """
    指定されたテキストを文に分割し、TF-IDFベクトルに変換後、文間の類似度を計算します。

    Parameters:
    - text: 分割とベクトル化を行う長いテキスト。
    - min_length: 分割された各文の最小長。この値以下の長さの文は無視されます。

    Returns:
    - cosine_similarity_matrix: 各文間のコサイン類似度行列。
    """

    # 文書の分割
    sentences = re.split(r"[。\.]", text)
    long_sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) >= min_length]

    if len(long_sentences) > 1:
        # TF-IDFベクトル化
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(long_sentences)

        # 類似度計算
        cosine_similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        return long_sentences, cosine_similarity_matrix
    else:
        return None
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

#類似度行列をもとに、各文書に対して最も類似度が高い文書を見つけます。
def find_most_similar_documents(similarity_matrix, threshold=0.3):
    """
    与えられた類似度行列をもとに、各文書に対して最も類似度が高い文書を見つけます。

    Parameters:
    - similarity_matrix: 文書間の類似度行列
    - threshold: この類似度スコア以上の文書を考慮する

    Returns:
    - similar_documents: 各文書に対して最も類似度が高い文書のインデックスと類似度スコアを含むリスト
    """

    similar_documents = []
    for i in range(similarity_matrix.shape[0]):
        similarity_scores = similarity_matrix[i]
        similarity_scores[i] = 0  # 自分自身のスコアを0に設定

        # 最も類似度が高い文書のインデックスを取得
        most_similar_doc_index = np.argmax(similarity_scores)
        most_similar_doc_score = similarity_scores[most_similar_doc_index]

        if most_similar_doc_score >= threshold:
            similar_documents.append((i, most_similar_doc_index, most_similar_doc_score))

    return similar_documents
#テキスト表示
def display_similar_documents(sentences, similar_documents):
    """
    Display pairs of similar documents using Streamlit.

    :param sentences: List of sentences/documents.
    :param similar_documents: List of tuples with the format (index1, index2, similarity_score).
    """
    for i, (doc_idx1, doc_idx2, score) in enumerate(similar_documents):
        with st.container():
            st.write(f"文章 {doc_idx1 + 1}と文章 {doc_idx2 + 1}の比較")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"文章 {doc_idx1 + 1}")
                st.write(f"{text_explanation(sentences[doc_idx1])}")
            with col2:
                st.subheader(f"文章 {doc_idx2 + 1}")
                st.write(f"{text_explanation(sentences[doc_idx2])}")

            st.write(f"類似度スコア: {score:.2f}")
            # Assuming get_similarity_explanation_with_score is a predefined function that takes two texts and a similarity score
            explanation = get_similarity_explanation_with_score(sentences[doc_idx1], sentences[doc_idx2], score)
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
    user_input_url = st.text_input("分析するウェブページのURLを入力してください:")

    # 分析ボタン
    if st.button('テキスト抽出と類似度分析'):
        if user_input_url:
            # コンテンツ収集
            all_text = scrape_all_text(user_input_url)
            if not all_text.startswith("Error"):
                #テキストを分割し、TF-IDFベクトルに変換後、文間の類似度を計算
                long_sentences, cosine_sim = split_and_vectorize_text(all_text, min_length=20)
                # 類似度が高い文書のインデックスと類似度スコアを含むリストを取得
                similar_documents = find_most_similar_documents(cosine_sim, threshold=0.3)
                # 類似度スコアが0.3以上の場合に結果を表示
                display_similar_documents(long_sentences, similar_documents)

            else:
                st.error(all_text)
        else:
            st.error("URLが入力されていません。")

if __name__ == '__main__':
    main()
