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
python3 -m pip install Pillow
python3 scripts/build_windows.py --copy-to-web
cp -r assets/ web/sopocursor/assets/
npx wrangler deploy
```

## カーソルのインストール

### macOS

1. [Mousecape](https://github.com/alexzielenski/Mousecape/releases) をインストールします
2. `.cape` ファイルをダブルクリックするか、Mousecape の `File` > `Import Cape` から読み込みます
3. Mousecape で `SopoCursor` を選択し、`Capes` > `Apply Cape` を実行します

### Windows

1. Windows版 ZIP をダウンロードして展開します
2. `install.inf` を右クリックして「インストール」を選びます
3. Windows の「マウスのプロパティ」>「ポインター」で `SopoCursor` を選択して適用します

## Windows版の生成

```bash
python3 -m pip install Pillow
python3 scripts/build_windows.py
```

生成されたZIPとWindows用カーソル一式は `dist/` に出力され、Git管理には含めません。Windows用カーソルは元画像を32x32に縮小して生成します。
