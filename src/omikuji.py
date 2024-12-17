# -*- coding: utf-8 -*-
"""おみくじ"""

# ライブラリのインポート
import random
from dataclasses import dataclass
from enum import Enum
from typing import Dict


class FortuneLevel(Enum):
    """おみくじの運勢レベル"""

    DAIKICHI = "大吉"
    CHUKICHI = "中吉"
    SHOKICHI = "小吉"
    KICHI = "吉"
    KYO = "凶"
    DAIKYO = "大凶"

@dataclass
class Fortune:
    """おみくじの結果を表すデータクラス"""

    result: FortuneLevel  # 結果
    advice: str  # アドバイス


class Omikuji:
    """おみくじの定数を管理するクラス"""

    # おみくじの結果と確率の重み付け
    FORTUNE_WEIGHTS: Dict[FortuneLevel, float] = {
        FortuneLevel.DAIKICHI: 0.1,  # 10%
        FortuneLevel.CHUKICHI: 0.2,  # 20%
        FortuneLevel.SHOKICHI: 0.25,  # 25%
        FortuneLevel.KICHI: 0.25,  # 25%
        FortuneLevel.KYO: 0.15,  # 15%
        FortuneLevel.DAIKYO: 0.05,  # 5%
    }

    # おみくじの結果に対応するアドバイス
    FORTUNE_ADVICE: Dict[FortuneLevel, str] = {
        FortuneLevel.DAIKICHI: "明日は非常に良い日です。\n自信を持って行動しましょう！",
        FortuneLevel.CHUKICHI: "明日は良い日ですが、\n慎重さも忘れずに。",
        FortuneLevel.SHOKICHI: "まあまあの運勢です。\nちょっとしたラッキーがあります。",
        FortuneLevel.KICHI: "運勢は良いですが、\n油断は禁物。",
        FortuneLevel.KYO: "明日は気をつけて行動しましょう。\n無理をしないのが吉。",
        FortuneLevel.DAIKYO: "注意が必要な日です。\n心も体も休めて。",
    }


def draw() -> Fortune:
    """おみくじを引く

    Returns:
        Fortune: おみくじの結果
    """
    result = random.choices(list(Omikuji.FORTUNE_WEIGHTS.keys()), weights=list(Omikuji.FORTUNE_WEIGHTS.values()))[0]
    return Fortune(result, Omikuji.FORTUNE_ADVICE[result])


if __name__ == "__main__":
    fortune = draw()
    print(f"結果: {fortune.result.value}")
    print(f"アドバイス: {fortune.advice}")
