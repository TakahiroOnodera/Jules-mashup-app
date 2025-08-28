# 1. ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 2. 作業ディレクトリを設定
WORKDIR /code

# 3. ポートを設定（Cloud RunはPORT環境変数を自動で設定する）
# デフォルトとして8000番ポートを公開
EXPOSE 8000

# 4. 環境変数を設定
#    - PYTHONUNBUFFERED: Pythonの出力をバッファリングせず、ログがリアルタイムで表示されるようにする
#    - PYTHONDONTWRITEBYTECODE: .pycファイルを生成しないようにする
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 5. 依存関係をインストール
#    - まずrequirements.txtだけをコピーしてインストールすることで、
#      コードの変更時に毎回ライブラリを再インストールするのを防ぎ、ビルドキャッシュを効率化する
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 6. アプリケーションのコードをコピー
COPY ./app /code/app

# 7. セキュリティ向上のため、非rootユーザーで実行
RUN useradd --create-home appuser
USER appuser

# 8. アプリケーションの起動コマンド
#    - Cloud Runが提供する`PORT`環境変数を尊重する
#    - `0.0.0.0`でリッスンし、コンテナ外部からのリクエストを受け付ける
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
