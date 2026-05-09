# そぽカーソル

そぽたんの macOS / Windows 用カーソルテーマです。

## ファイル構成

```text
assets/        カーソル画像 (PNG)
scripts/       配布用ファイル生成スクリプト
web/           Webサイト
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
