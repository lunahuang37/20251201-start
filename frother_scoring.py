#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奶泡器評論自動評分系統 (Frother Review Scoring System)

這個程式用於分析奶泡器產品的英文評論，根據6個題型自動評分。

作者: Luna Huang
日期: 2024
"""

import pandas as pd
import numpy as np
import re
import os

# ==================== 評分函數 ====================

def score_motor_performance(comment):
    """
    評估馬達效能 (Motor Performance)
    
    關鍵字: motor, power, powerful, weak, strong, speed, fast, slow, performance, beast, mighty
    
    評分規則:
    - 極度正面 (very powerful, beast, mighty, super powerful) → 7分
    - 正面 (powerful, strong, fast, good performance) → 6分
    - 稍微正面 (decent power, works well) → 5分
    - 負面 (weak, slow, not powerful, not very fast) → 2-3分
    - 極度負面 (very weak, terrible motor, barely works) → 1分
    - 未提及 → 0
    """
    if not comment or pd.isna(comment):
        return 0
    
    comment_lower = str(comment).lower()
    
    # 先檢查負面模式（包括否定形式）- 必須在正面模式之前檢查
    # 極度負面 (1分)
    extremely_negative = [
        r'\bvery\s+weak\b', r'\bterrible\s+motor\b', r'\bbarely\s+works\b',
        r'\bbarely\s+froths\b', r'\bnot\s+powerful\s+at\s+all\b'
    ]
    for pattern in extremely_negative:
        if re.search(pattern, comment_lower):
            return 1
    
    # 負面 (2-3分) - 包含否定形式
    negative = [
        r'\bweak\b', r'\bnot\s+powerful\b', r'\bnot\s+very\s+fast\b',
        r'\bnot\s+fast\b', r'\bslow\b', r'\bnot\s+near\s+as\s+strong\b',
        r'\bnot\s+strong\b', r'wasn\'t\s+(even\s+)?very\s+fast',  # 處理 wasn't (even) very fast
        r'\bnot\s+impressed\b', r'\bdisappointing\s+power\b',
        r'wasn\'t.*fast', r'not\s+near\s+as\s+strong'  # 更寬鬆的否定匹配
    ]
    for pattern in negative:
        if re.search(pattern, comment_lower):
            return 2
    
    # 極度正面 (7分) - 在確認沒有否定後才檢查
    extremely_positive = [
        r'\bvery\s+powerful\b', r'\bsuper\s+powerful\b', r'\bextremely\s+powerful\b',
        r'\bbeast\b', r'\bmighty\b', r'\bincredibly\s+powerful\b',
        r'\bstrongest\b', r'\bsuper\s+fast\b', r'\bvery\s+fast\b'
    ]
    for pattern in extremely_positive:
        if re.search(pattern, comment_lower):
            return 7
    
    # 正面 (6分)
    positive = [
        r'\bpowerful\b', r'\bstrong\b', r'\bfast\b', r'\bgood\s+power\b',
        r'\bgood\s+performance\b', r'\befficient\b'
    ]
    for pattern in positive:
        if re.search(pattern, comment_lower):
            return 6
    
    # 稍微正面 (5分)
    slightly_positive = [
        r'\bdecent\s+power\b', r'\bworks\s+well\b', r'\bgood\s+overall\s+performance\b',
        r'\bquick\s+results\b', r'\bgets\s+the\s+job\s+done\s+in\s+seconds\b'
    ]
    for pattern in slightly_positive:
        if re.search(pattern, comment_lower):
            return 5
    
    # 檢查是否提及馬達相關關鍵字
    motor_keywords = [r'\bmotor\b', r'\bpower\b', r'\bspeed\b', r'\bperformance\b']
    for pattern in motor_keywords:
        if re.search(pattern, comment_lower):
            # 預設給5分如果提及但無明確情緒
            return 5
    
    return 0


def score_power_type(comment):
    """
    評估電源類型 (Power Type)
    
    關鍵字: rechargeable, battery, USB, charge, batteries, battery-operated, cordless
    
    評分規則:
    - 極度正面 (rechargeable + love it, USB rechargeable, charge lasts long) → 7分
    - 正面 (rechargeable, good battery life) → 6分
    - 稍微正面 (battery-operated, convenient) → 5分
    - 負面 (battery dies quickly, drains batteries, short battery life) → 2-3分
    - 極度負面 (terrible battery, batteries die immediately) → 1分
    - 未提及 → 0
    """
    if not comment or pd.isna(comment):
        return 0
    
    comment_lower = str(comment).lower()
    
    # 極度正面 (7分)
    extremely_positive = [
        r'rechargeable.*love', r'love.*rechargeable', r'usb\s+rechargeable.*love',
        r'charge\s+lasts\s+long', r'battery\s+lasts\s+a\s+long\s+time',
        r'battery\s+lasts\s+forever', r'long-lasting\s+rechargeable',
        r'love\s+the\s+usb\s+rechargeable', r'amazing.*rechargeable',
        r'rechargeable.*amazing', r'love\s+the\s+rechargeable',
        r'charge\s+lasts\s+a\s+long\s+time', r'long\s+battery\s+life',
        r'very\s+happy\s+with\s+battery', r'lasts\s+a\s+long\s+time',
        r'love\s+the\s+usb', r'usb\s+rechargeable\s+feature'
    ]
    for pattern in extremely_positive:
        if re.search(pattern, comment_lower):
            return 7
    
    # 極度負面 (1分)
    extremely_negative = [
        r'terrible\s+battery', r'batteries\s+die\s+immediately',
        r'dies\s+after\s+just\s+a\s+few', r'dies\s+too\s+quickly'
    ]
    for pattern in extremely_negative:
        if re.search(pattern, comment_lower):
            return 1
    
    # 負面 (2-3分)
    negative = [
        r'battery\s+dies\s+quickly', r'drains\s+batteries', r'short\s+battery\s+life',
        r'battery\s+drains\s+quickly', r'batteries\s+die\s+quickly',
        r'drains\s+batteries\s+like\s+crazy', r'have\s+to\s+charge.*every\s+other\s+day',
        r'constantly\s+buying\s+batteries', r'short\s+battery\s+life',
        r'dies\s+quickly', r'frustrating.*battery', r'battery.*frustrating'
    ]
    for pattern in negative:
        if re.search(pattern, comment_lower):
            return 2
    
    # 檢查是否在比較其他產品（如 "that was rechargeable" 表示其他產品是充電式）
    # 這種情況下不給高分
    if re.search(r'that\s+was\s+rechargeable', comment_lower):
        # 對比另一個產品的充電功能，這個產品可能不是充電式
        if re.search(r'this\s+one\s+is\s+battery\s+operated', comment_lower):
            return 4  # 中立，因為是比較性的陳述
    
    # 正面 (6分)
    positive = [
        r'usb\s+rechargeable', r'good\s+battery\s+life',
        r'usb\s+charging', r'easy\s+to\s+charge', r'convenient.*charge',
        r'charge.*convenient', r'good\s+battery', r'rechargeable\s+feature',
        r'rechargeable\s+battery', r'rechargeable.*convenient'
    ]
    for pattern in positive:
        if re.search(pattern, comment_lower):
            return 6
    
    # 單獨的 "rechargeable" 需要更多上下文
    if re.search(r'\brechargeable\b', comment_lower):
        # 檢查是否有正面情緒
        if re.search(r'love|great|amazing|convenient|nice|good', comment_lower):
            return 6
        # 檢查是否只是陳述
        return 5
    
    # 稍微正面 (5分)
    slightly_positive = [
        r'battery-operated', r'battery\s+operated'
    ]
    for pattern in slightly_positive:
        if re.search(pattern, comment_lower):
            # 檢查上下文是否負面
            if re.search(r'not\s+near\s+as|not\s+as|weak|poor', comment_lower):
                return 4  # 如果有負面比較，給中立分
            return 5
    
    # 中性提及 (4分)
    neutral = [
        r'battery\s+operated\s+which\s+means'
    ]
    for pattern in neutral:
        if re.search(pattern, comment_lower):
            return 4
    
    # 檢查是否提及電源相關關鍵字
    power_keywords = [r'\bbattery\b', r'\bbatteries\b', r'\brechargeable\b', 
                      r'\busb\b', r'\bcharge\b', r'\bcordless\b']
    for pattern in power_keywords:
        if re.search(pattern, comment_lower):
            return 5
    
    return 0


def score_switch_design(comment):
    """
    評估開關設計 (Switch Design)
    
    關鍵字: button, switch, on/off, press, hold down, one button, easy to use
    
    評分規則:
    - 正面 (easy button, simple one button, easy to use) → 5-6分
    - 負面 (hard to press, must hold down, awkward button, button in awkward spot) → 2-3分
    - 極度負面 (button broken, can't press) → 1分
    - 未提及 → 0
    """
    if not comment or pd.isna(comment):
        return 0
    
    comment_lower = str(comment).lower()
    
    # 極度負面 (1分)
    extremely_negative = [
        r'button\s+broken', r'can\'t\s+press', r'cannot\s+press'
    ]
    for pattern in extremely_negative:
        if re.search(pattern, comment_lower):
            return 1
    
    # 負面 (2-3分)
    negative = [
        r'hard\s+to\s+press', r'must\s+hold\s+down', r'have\s+to\s+hold.*down',
        r'awkward\s+button', r'button.*awkward', r'awkward.*button',
        r'hold\s+the\s+button\s+down', r'stiff.*button', r'button.*stiff',
        r'not\s+user\s+friendly', r'hand\s+gets\s+tired', r'bad\s+ergonomics',
        r'hard\s+to\s+operate', r'awkward\s+spot', r'awkward\s+position',
        r'awkward\s+placement'
    ]
    for pattern in negative:
        if re.search(pattern, comment_lower):
            return 2
    
    # 正面 (6分)
    positive = [
        r'easy\s+button', r'simple\s+one\s+button', r'one\s+button.*easy',
        r'easy\s+to\s+use.*button', r'button.*easy\s+to\s+use',
        r'easy\s+to\s+operate', r'simple\s+button', r'easy\s+one\s+button',
        r'simple\s+press\s+button', r'easy\s+button\s+operation',
        r'simple\s+and\s+intuitive', r'so\s+simple'
    ]
    for pattern in positive:
        if re.search(pattern, comment_lower):
            return 6
    
    # 稍微正面 (5分)
    slightly_positive = [
        r'easy\s+to\s+use', r'simple\s+design', r'works\s+great',
        r'easy\s+to\s+operate', r'one\s+button', r'simple'
    ]
    for pattern in slightly_positive:
        if re.search(pattern, comment_lower):
            # 只有在提及按鈕/開關的情況下
            if re.search(r'button|switch|press', comment_lower):
                return 5
    
    # 檢查是否提及開關相關關鍵字但無明確情緒
    switch_keywords = [r'\bbutton\b', r'\bswitch\b', r'\bon/off\b', r'\bpress\b']
    has_switch_mention = any(re.search(pattern, comment_lower) for pattern in switch_keywords)
    
    if has_switch_mention:
        # 檢查是否有正面詞彙
        if re.search(r'easy|simple|good|works', comment_lower):
            return 5
        # 檢查是否有負面詞彙
        if re.search(r'awkward|hard|difficult|stiff', comment_lower):
            return 3
    
    return 0


def score_failure_durability(comment):
    """
    評估故障/壽命 (Failure/Durability)
    
    關鍵字: broke, broken, stopped working, durability, reliable, last, died, flimsy, sturdy, solid
    
    評分規則:
    - 極度正面 (reliable, works perfectly for year+, very durable, solid, sturdy) → 7分
    - 正面 (durable, reliable, no issues) → 6分
    - 稍微正面 (works well, no problems so far) → 5分
    - 負面 (broke, stopped working, not durable, flimsy) → 1-2分
    - 未提及 → 0
    """
    if not comment or pd.isna(comment):
        return 0
    
    comment_lower = str(comment).lower()
    
    # 極度正面 (7分)
    extremely_positive = [
        r'works\s+perfectly\s+for.*year', r'very\s+durable', r'very\s+reliable',
        r'solid\b', r'sturdy\b', r'still\s+works\s+after', r'works\s+after.*year',
        r'survived\s+many', r'working\s+after\s+2\s+years', r'perfectly\s+for\s+years',
        r'lasts\s+forever', r'still\s+works\s+perfectly', r'works\s+perfectly'
    ]
    for pattern in extremely_positive:
        if re.search(pattern, comment_lower):
            return 7
    
    # 極度負面 (1分)
    extremely_negative = [
        r'broke\s+after', r'stopped\s+working', r'died\s+after',
        r'broke\s+within', r'completely\s+stopped', r'defective',
        r'terrible\s+durability', r'total\s+waste', r'flimsy\s+construction',
        r'broke\s+after.*month', r'stopped\s+working\s+after',
        r'broke\b', r'broken\b', r'died\b'
    ]
    for pattern in extremely_negative:
        if re.search(pattern, comment_lower):
            return 1
    
    # 負面 (2-3分)
    negative = [
        r'not\s+durable', r'flimsy', r'might\s+break', r'feels\s+cheap',
        r'cheap\s+and\s+plasticky', r'plasticky', r'poor\s+quality',
        r'not\s+confident\s+in\s+durability', r'expected\s+it\s+to\s+last\s+longer',
        r'flimsy\s+build'
    ]
    for pattern in negative:
        if re.search(pattern, comment_lower):
            return 3
    
    # 正面 (6分)
    positive = [
        r'durable', r'reliable', r'no\s+issues', r'no\s+problems',
        r'reliable\s+performance', r'still\s+working', r'well-made'
    ]
    for pattern in positive:
        if re.search(pattern, comment_lower):
            return 6
    
    # 稍微正面 (5分)
    slightly_positive = [
        r'works\s+well', r'no\s+problems\s+so\s+far', r'so\s+far.*no\s+problems',
        r'no\s+issues\s+after', r'no\s+complaints\s+so\s+far'
    ]
    for pattern in slightly_positive:
        if re.search(pattern, comment_lower):
            return 5
    
    # 檢查是否提及壽命相關關鍵字
    durability_keywords = [r'\bdurability\b', r'\breliable\b', r'\blast\b', 
                          r'\bsturdy\b', r'\bsolid\b', r'\bflimsy\b']
    for pattern in durability_keywords:
        if re.search(pattern, comment_lower):
            return 5
    
    return 0


def score_noise(comment):
    """
    評估噪音 (Noise)
    
    關鍵字: quiet, silent, noise, noisy, loud
    
    評分規則:
    - 極度正面 (super quiet, very quiet, silent) → 7分
    - 正面 (quiet) → 6分
    - 負面 (noisy, loud, louder than expected) → 2-3分
    - 未提及 → 0
    """
    if not comment or pd.isna(comment):
        return 0
    
    comment_lower = str(comment).lower()
    
    # 極度正面 (7分)
    extremely_positive = [
        r'super\s+quiet', r'very\s+quiet', r'silent\b', r'so\s+quiet',
        r'barely\s+hear', r'barely\s+makes\s+any\s+sound', r'barely\s+makes\s+noise'
    ]
    for pattern in extremely_positive:
        if re.search(pattern, comment_lower):
            return 7
    
    # 極度負面 (1分)
    extremely_negative = [
        r'extremely\s+loud', r'sounds\s+like\s+a.*helicopter', r'too\s+noisy'
    ]
    for pattern in extremely_negative:
        if re.search(pattern, comment_lower):
            return 1
    
    # 負面 (2-3分)
    negative = [
        r'noisy', r'loud\b', r'louder\s+than\s+expected', r'too\s+loud',
        r'quite\s+loud', r'a\s+bit\s+noisy', r'wakes\s+everyone'
    ]
    for pattern in negative:
        if re.search(pattern, comment_lower):
            # 區分 "loud" 和 "quite loud" 的嚴重程度
            if re.search(r'too\s+noisy|wakes', comment_lower):
                return 2
            return 3
    
    # 正面 (6分)
    positive = [
        r'quiet\b'
    ]
    for pattern in positive:
        if re.search(pattern, comment_lower):
            # 排除 "quite loud" 等負面用法
            if not re.search(r'quite\s+loud|quite\s+noisy', comment_lower):
                return 6
    
    # 檢查是否提及噪音相關關鍵字
    noise_keywords = [r'\bnoise\b', r'\bnoisy\b', r'\bquiet\b', r'\bsilent\b', r'\bloud\b']
    for pattern in noise_keywords:
        if re.search(pattern, comment_lower):
            return 5
    
    return 0


def score_neutral_opinion(comment):
    """
    評估中立意見 (Neutral Opinion)
    
    評估邏輯: 判斷整體評論是否沒有明確表達好或壞
    
    關鍵字: works, okay, decent, basic, nothing fancy, does the job, it's fine
    
    評分規則:
    - 完全中立（無明顯情緒，只陳述事實）→ 4分
    - 有明確正面或負面情緒 → 0
    """
    if not comment or pd.isna(comment):
        return 0
    
    comment_lower = str(comment).lower()
    
    # 強烈正面詞彙 - 如果有這些，不是中立
    strong_positive = [
        r'\blove\b', r'\bamazing\b', r'\bperfect\b', r'\bexcellent\b',
        r'\bgreat\b', r'\bbest\b', r'\bwonderful\b', r'\bfantastic\b',
        r'\bimpressed\b', r'\bsatisfied\b', r'\bhappy\b', r'\brecommend\b',
        r'\bpowerful\b', r'\bquiet\b', r'\bsilent\b', r'\bdurable\b',
        r'\breliable\b', r'\bstill\s+works\b', r'\bworks\s+perfectly\b'
    ]
    
    # 強烈負面詞彙 - 如果有這些，不是中立
    strong_negative = [
        r'\bhate\b', r'\bterrible\b', r'\bawful\b', r'\bbad\b',
        r'\bworst\b', r'\bdisappointed\b', r'\bfrustrating\b',
        r'\bbroke\b', r'\bbroken\b', r'\bweak\b', r'\bfailed\b',
        r'\bwaste\b', r'\bdefective\b', r'\bannoy\b', r'\bnoisy\b',
        r'\bnot\s+impressed\b', r'\bnot\s+a\s+fan\b', r'\bflimsy\b',
        r'\bloud\b', r'\bstiff\b', r'\bawkward\b', r'\bcheap\b',
        r'\bplasticky\b', r'\bpoor\b', r'\bnot\s+good\b'
    ]
    
    # 檢查是否有強烈情緒
    for pattern in strong_positive + strong_negative:
        if re.search(pattern, comment_lower):
            return 0
    
    # 中立表達
    neutral_phrases = [
        r'\bit\s+works\b', r'\bokay\b', r'\bfine\b', r'\bdecent\b',
        r'\bbasic\b', r'\bnothing\s+fancy\b', r'\bdoes\s+the\s+job\b',
        r'\bgets\s+the\s+job\s+done\b', r'\bnothing\s+special\b',
        r'\bnothing\s+more\b', r'\bnothing\s+less\b', r'\bjust\s+okay\b',
        r'\bmiddle\s+of\s+the\s+road\b', r'\bnothing\s+amazing\b',
        r'\bnothing\s+impressive\b', r'\bjust\s+works\b', r'\bstandard\b',
        r'\badequate\b', r'\bmediocre\b', r'\baverage\b', r'\bfair\b',
        r'\bno\s+major\s+complaints\b', r'\bfunctional\b'
    ]
    
    for pattern in neutral_phrases:
        if re.search(pattern, comment_lower):
            return 4
    
    return 0


def process_reviews(input_file, output_file):
    """
    處理評論檔案並產生評分結果
    
    Args:
        input_file: 輸入CSV檔案路徑
        output_file: 輸出CSV檔案路徑
    """
    print("=" * 60)
    print("奶泡器評論自動評分系統")
    print("=" * 60)
    
    # 檢查輸入檔案是否存在
    if not os.path.exists(input_file):
        print(f"錯誤: 找不到輸入檔案 '{input_file}'")
        print("請確保檔案存在於當前目錄中")
        return False
    
    print(f"\n正在讀取檔案: {input_file}")
    
    try:
        # 讀取CSV檔案
        df = pd.read_csv(input_file, encoding='utf-8')
        print(f"成功讀取 {len(df)} 筆評論資料")
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return False
    
    # 確認必要欄位存在
    if 'comment' not in df.columns:
        print("錯誤: 找不到 'comment' 欄位")
        return False
    
    print("\n開始評分處理...")
    print("-" * 40)
    
    # 建立新的評分欄位
    new_columns = {
        '馬達效能': [],
        '電源類型': [],
        '開關設計': [],
        '故障/壽命': [],
        '噪音': [],
        '中立意見': []
    }
    
    # 對每個評論進行評分
    total = len(df)
    for idx, row in df.iterrows():
        comment = row['comment']
        
        # 評分
        new_columns['馬達效能'].append(score_motor_performance(comment))
        new_columns['電源類型'].append(score_power_type(comment))
        new_columns['開關設計'].append(score_switch_design(comment))
        new_columns['故障/壽命'].append(score_failure_durability(comment))
        new_columns['噪音'].append(score_noise(comment))
        new_columns['中立意見'].append(score_neutral_opinion(comment))
        
        # 顯示進度
        if (idx + 1) % 10 == 0 or idx == 0 or idx == total - 1:
            progress = (idx + 1) / total * 100
            print(f"處理進度: {idx + 1}/{total} ({progress:.1f}%)")
    
    print("-" * 40)
    print("評分完成!")
    
    # 建立輸出DataFrame
    # 取得原始欄位列表
    original_columns = df.columns.tolist()
    
    # 找到 'comment' 欄位的位置
    comment_idx = original_columns.index('comment')
    
    # 建立新的欄位順序
    # comment 之後插入6個新欄位，然後是其餘原始欄位
    new_column_order = original_columns[:comment_idx + 1]  # 包含 comment
    new_column_order.extend(['馬達效能', '電源類型', '開關設計', '故障/壽命', '噪音', '中立意見'])
    new_column_order.extend(original_columns[comment_idx + 1:])  # 其餘欄位
    
    # 將新欄位加入DataFrame
    for col_name, values in new_columns.items():
        df[col_name] = values
    
    # 重新排列欄位順序
    df = df[new_column_order]
    
    # 儲存結果
    print(f"\n正在儲存結果至: {output_file}")
    try:
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"成功儲存 {len(df)} 筆評分結果")
    except Exception as e:
        print(f"儲存檔案時發生錯誤: {e}")
        return False
    
    # 顯示統計摘要
    print("\n" + "=" * 60)
    print("評分統計摘要")
    print("=" * 60)
    
    for col in ['馬達效能', '電源類型', '開關設計', '故障/壽命', '噪音', '中立意見']:
        scores = df[col]
        non_zero = scores[scores > 0]
        print(f"\n{col}:")
        print(f"  - 有評分的評論數: {len(non_zero)}")
        if len(non_zero) > 0:
            print(f"  - 平均分數: {non_zero.mean():.2f}")
            print(f"  - 最高分: {non_zero.max()}")
            print(f"  - 最低分: {non_zero.min()}")
    
    print("\n" + "=" * 60)
    print("處理完成!")
    print("=" * 60)
    
    return True


def main():
    """主程式入口點"""
    # 設定檔案路徑
    input_file = "奶泡器交易資料(luna) - 複製.csv"
    output_file = "奶泡器交易資料_已評分.csv"
    
    # 執行處理
    success = process_reviews(input_file, output_file)
    
    if success:
        print(f"\n✅ 程式執行成功!")
        print(f"📄 輸出檔案: {output_file}")
    else:
        print(f"\n❌ 程式執行失敗，請檢查錯誤訊息")


if __name__ == "__main__":
    main()
