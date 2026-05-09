# SopoCursor

そぽたんの macOS / Windows 用カーソルテーマです。

## ファイル構成

```text
assets/        カーソル画像 (PNG)
scripts/       配布用ファイル生成スクリプト
web/           Webサイト
wrangler.jsonc Cloudflare Workers 設定
```

## Webサイトのデプロイ

Cloudflare Workers + Wrangler でデプロイします。

### 初回セットアップ

1. Cloudflare ダッシュボードで `sopocursor` プロジェクトを作成します
2. GitHub リポジトリの Secrets に以下を追加します

| Secret 名 | 内容 |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API トークン |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare アカウント ID |

### 手動デプロイ

```bash
python3 scripts/build_windows.py --copy-to-web
cp -r assets/ web/sopocursor/assets/
npx wrangler deploy
```

## カーソルのインストール

### macOS

1. [Cursor Pro](https://cursor.pro) をインストールします
2. `.cape` ファイルを Cursor Pro で開きます
3. メニューバーから SopoCursor を選択して適用します

### Windows

1. Windows版 ZIP をダウンロードして展開します
2. `install.inf` を右クリックして「インストール」を選びます
3. Windows の「マウスのプロパティ」>「ポインター」で `SopoCursor` を選択して適用します

## Windows版の生成

```bash
python3 scripts/build_windows.py
```

生成されたZIPとWindows用カーソル一式は `dist/` に出力され、Git管理には含めません。
