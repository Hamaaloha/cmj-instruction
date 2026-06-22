"""
post.html 用ナレーション音声を VOICEVOX で生成し media/ に保存するスクリプト。

事前準備:
  1. VOICEVOX を起動しておく (http://127.0.0.1:50021 で待ち受け)
  2. pip install requests

実行:
  python generate_post_narration.py

生成物:
  media/post_00.wav ~ media/post_04.wav (スライド0〜4)
"""

import requests
import os

VOICEVOX_URL = "http://127.0.0.1:50021"
SPEAKER_ID   = 2  # 四国めたん (ノーマル)

NARRATIONS = [
    "測定お疲れ様でした。最後にスマホから測定結果を登録してください。",
    "職員から滞空時間をお伝えします。画面の数字をそのままメモしておいてください。",
    "スマホでフォームを開いてください。下のボタンをタップするとフォームが開きます。フォームを開いたら、次へボタンを押してください。",
    "フォームに入力してください。滞空時間は、職員から受け取った数字をそのまま入力します。氏名、学籍番号、性別、所属部活動も入力してください。入力できたら次へボタンを押してください。",
    "すべて入力できたら、送信ボタンを押してください。以上で測定は完了です。ありがとうございました。",
]

def generate(text: str, speaker_id: int) -> bytes:
    r = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": speaker_id},
    )
    r.raise_for_status()
    query = r.json()
    r = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        params={"speaker": speaker_id},
        json=query,
    )
    r.raise_for_status()
    return r.content

if __name__ == "__main__":
    os.makedirs("media", exist_ok=True)
    print(f"スピーカーID: {SPEAKER_ID}\n")
    for i, text in enumerate(NARRATIONS):
        path = f"media/post_{i:02d}.wav"
        print(f"[{i:02d}] {text[:40]}...")
        wav = generate(text, SPEAKER_ID)
        with open(path, "wb") as f:
            f.write(wav)
        print(f"      → {path} ({len(wav):,} bytes)")
    print("\n完了！ post.html をブラウザで開いてください。")
