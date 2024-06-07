# LangGraphを使ってみよう（パワーアップ）

## 環境設定

```
# 仮想環境
python3 -m venv .venv
source .venv/bin/activate
# パッケージインストール
pip install langchain langchain-community langchain-openai langgraph json5 python-dotenv
```

## API Key

### 方法１

環境変数でのエクスポート

```
% export OPENAI_API_KEY=ここにOPENAIのAPIキー
% export TAVILY_API_KEY=ここにTavilyのAPIキー
% expoet VERBOSE=1
```

### 方法２

`.env`ファイル作成後、下記の内容を記載

```
OPENAI_API_KEY=ここにOPENAIのAPIキー
TAVILY_API_KEY=ここにTavilyのAPIキー
VERBOSE=1
```
