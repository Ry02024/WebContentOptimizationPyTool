# WebContentOptimizationPyTool
ウェブページテキストスクレイピングと類似度分析アプリ

## 目次
- [プロジェクト概要](#プロジェクト概要)
- [特徴](#特徴)
- [技術スタック](#技術スタック)
- [アプリの使用方法](#アプリの使用方法)
  - [Streamlit Cloudを使用する](#streamlit-cloudを使用する)
  - [Google Colabとngrokを使用する](#google-colabとngrokを使用する)
- [セットアップ](#セットアップ)
  - [前提条件](#前提条件)
  - [インストール手順](#インストール手順)
- [注意](#注意)
- [コントリビューション](#コントリビューション)

## プロジェクト概要
このプロジェクトは、指定されたウェブページのテキストをスクレイピングし、その内容を基にテキスト間の類似度分析を行うWebアプリです。Streamlitを利用して構築され、Streamlit Cloudを通じて公開されます。

## 特徴
- 複数のウェブページ間での類似度を分析し、内容が重複しないようにリライトを提案します。
- GeminiのSEMANTIC_SIMILARITYに基づく高精度な類似度評価。
- Streamlitによる直感的なウェブインターフェースでの結果表示。
- 
## 技術スタック
- Streamlit
- BeautifulSoup
- NLTK
- Scikit-learn
- Google-generativeai

## APIの利用による利点

本プロジェクトでは、geminni APIを積極的に利用しています。このAPIの最大の利点の一つは、**ローカルで高度な演算を行う必要がなくなること**です。APIを通じて、サーバーやクラウド上でのデータ処理が可能になり、以下のようなメリットがあります：

- **ハードウェアの制約を超える**：開発者は、パーソナルコンピュータや限られたリソースしか持たない環境でも、複雑なデータ処理や機械学習タスクを実行できます。
- **コスト効率の向上**：高性能なローカルハードウェアに投資する必要がなく、使用した分だけの料金で処理能力を利用できるため、コストを効率的に管理できます。
- **スケーラビリティ**：プロジェクトのニーズに応じてリソースを柔軟に調整できるため、ユーザーベースの成長やデータ量の増加に対応しやすくなります。

このAPIの活用により、プロジェクトはリソースの制約を受けずに高度な機能を実装でき、開発者はよりイノベーティブなウェブアプリケーションの作成に集中できます。

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

## バージョンアップ情報
- **Version 1.0 (Yomi)**: 基本機能としてウェブページからのテキストスクレイピングと類似度分析を提供。

![Yomi Version 1.0](/images/YominoKuni_Thumb2.jpg "Yomi Version 1.0 Thumbnail")

- **Version 2.0 (Toyotama)**: テキスト比較とリライト提案機能を新たに追加。Gemini APIのSEMANTIC_SIMILARITYを利用した高度な類似度分析を実装し、テキスト間の深い関連性の探求と新しい文脈でのコンテンツ生成をサポート。
  
![Toyotama Version 2.0](/images/ToyotamaHime2_Thum.jpg "Toyotama Version 2.0 Thumbnail")




