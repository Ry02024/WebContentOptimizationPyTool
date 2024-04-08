# WebContentOptimizationPyTool
ウェブページテキストスクレイピングと類似度分析アプリ

## 目次
- [プロジェクト概要](##プロジェクト概要)
- [特徴](##特徴)
- [技術スタック](##技術スタック)
- [アプリの使用方法](##アプリの使用方法)
  - [Streamlit Cloudを使用する](##streamlit-cloudを使用する)
  - [Google Colabとngrokを使用する](###google-colabとngrokを使用する)
- [セットアップ](##セットアップ)
  - [前提条件](###前提条件)
  - [インストール手順](###インストール手順)
- [注意](##注意)
- [コントリビューション](##コントリビューション)

## プロジェクト概要
このプロジェクトは、指定されたウェブページのテキストをスクレイピングし、その内容を基にテキスト間の類似度分析を行うWebアプリです。Streamlitを利用して構築され、Streamlit Cloudを通じて公開されます。

## 特徴
- 指定されたウェブページからテキストを抽出します。
- 抽出したテキストの類似度を分析し、類似している文書のペアを特定します。
- 文書間の類似度スコアと、その根拠に関する詳細な分析を提供します。
- Streamlitを利用したインタラクティブなウェブインターフェイスを通じて結果を表示します。

## 技術スタック
- Streamlit
- BeautifulSoup
- NLTK
- Scikit-learn
- Google-generativeai

## アプリの使用方法
### Streamlit Cloudを使用する
Streamlit Cloudでホストされているため、特別な実行手順は不要です。以下のURLからアクセスできます。
[https://webcontentoptimizationpytool-jl7w8ftyltzkvtv86nyhgh.streamlit.app/](https://webcontentoptimizationpytool-jl7w8ftyltzkvtv86nyhgh.streamlit.app/)

### Google Colabとngrokを使用する
Google Colabとngrokを使用してアプリを実行する方法については、セットアップ手順を参照してください。

## セットアップ
### 前提条件
- Python 3.8 以上がインストールされていること。
- ngrokのアカウントを持っていること（Google Colabとngrokを使用する場合）。

### インストール手順
1. リポジトリをクローンします。
    ```bash
    git clone このリポジトリのURL
    cd このリポジトリのディレクトリ
    ```
2. 必要なPythonパッケージをインストールします。
    ```bash
    pip install -r requirements.txt
    ```

Google Colabでの実行手順については、上記「Google Colabとngrokを使用する」セクションをご覧ください。

## 注意
このアプリは公開的なデモ用途に最適化されています。機密性の高いテキストを分析する場合は、プライバシーのリスクを十分に考慮してください。

## コントリビューション
プロジェクトへのコントリビューションに興味がある方は、Pull RequestやIssueを通じてご提案ください。
