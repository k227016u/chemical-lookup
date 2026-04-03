# Chemical Lookup

分析化学データから最も近い化合物名を返すWebアプリです。

## 機能

- 数値（波長・質量など）を入力
- 登録済みデータから最も近い値の化合物を表示
- 差分（どれだけずれているか）も表示

## 化合物データの編集

`app.py` の `COMPOUNDS` 辞書を編集してください：

```python
COMPOUNDS = {
    200: "ベンゼン",
    254: "ナフタレン",
    # ← ここに追加: 数値: "化合物名"
}
```

## ローカルで動かす

```bash
pip install -r requirements.txt
python app.py
```

→ http://localhost:5000 にアクセス

## Renderへのデプロイ手順

1. このフォルダをGitHubリポジトリにpush
2. [render.com](https://render.com) でアカウント作成
3. 「New +」→「Web Service」→ GitHubリポジトリを選択
4. 設定はそのまま「Deploy」をクリック
5. 数分後にURLが発行されて公開完了！
