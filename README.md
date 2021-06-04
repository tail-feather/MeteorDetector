# MeteorDetector

[![.github/workflows/main.yml](https://github.com/tail-feather/MeteorDetector/actions/workflows/main.yml/badge.svg)](https://github.com/tail-feather/MeteorDetector/actions/workflows/main.yml)

流星群画像の中から流星の流れている画像の抽出を試みるツール。

![index.png](https://raw.githubusercontent.com/tail-feathre/MeteorDetector/docs/img/index.png)

## Usage

```
pip install -r requirements.txt
python main.py
```

or

実行ファイルは [Releases](https://github.com/tail-feather/MeteorDetector/releases) 参照

1. Image/Add から画像をリストに追加（JPEG画像をリストにドラッグ＆ドロップでも追加可能）
2. Proc/Run で処理開始

### 設定

Proc/Config (Linux/Windows), Preferences... `Cmd+,` (Mac) から各パラメータを設定可能。

![config](https://raw.githubusercontent.com/tail-feathre/MeteorDetector/docs/img/config.png)

* cv2.threshold
    * Threshold: しきい値
    * MaxValue: 2値最大値
* FillArea
    * AreaThreshold: 面積判定しきい値
    * FillBuffer: 面拡張量
* MeteorDetection
    * LineThreshold: 直線判定しきい値

### 画像プレビュー

#### Original

オリジナル画像。

![original preview](https://raw.githubusercontent.com/tail-feathre/MeteorDetector/docs/img/original.png)

#### Threshold

しきい値処理を適用した画像。

![threshold preview](https://raw.githubusercontent.com/tail-feathre/MeteorDetector/docs/img/threshold.png)

#### Filled

検知した面積のある領域を塗りつぶした画像。

![filled preview](https://raw.githubusercontent.com/tail-feathre/MeteorDetector/docs/img/filled.png)
