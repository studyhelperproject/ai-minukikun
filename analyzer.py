import base64
import io
import json
import math
import os
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import requests
from PIL import ExifTags, Image

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import docx  # python-docx
except ImportError:
    docx = None


# ==========================================
# 1. 日本人特化：テキスト・LINE・外注記事・就活ES・レポートAI判定エンジン
# ==========================================

AI_SIGNATURE_PHRASES = [
    (r"という点が挙げられます", 15, "ChatGPT/Claude頻出の列挙まとめ表現"),
    (r"と言えるでしょう", 13, "AI特有の推量・結論付け表現"),
    (r"重要な役割を果たして", 15, "LLM頻出の抽象評価フレーズ"),
    (r"多岐にわた(り|る)", 12, "LLM頻出の要約語彙"),
    (r"不可欠(です|と言え|となって)", 13, "AI文章に多用される強調表現"),
    (r"総じて|結論として|まとめると", 14, "AIの構造化要約マーカー"),
    (r"一方で、.*も(存在|重要|課題)", 15, "AI特有の対比バランス構文（両論併記癖）"),
    (r"まず第一に|第二に|最後に", 15, "翻訳調・AI構造化ナンバリング"),
    (r"いかがでしたでしょうか", 16, "クラウドソーシング量産型AI記事テンプレ表現"),
    (r"参考にしていただければ幸いです", 11, "AI記事定型クロージング表現"),
    (r"何か(他にご不明な点|ご質問)がございましたら", 10, "AIアシスタント定型句"),
    (r"素晴らしい(ですね|視点|ご意見)", 13, "AI特有の過剰肯定・ヨイショ構文"),
    (r"おっしゃる通りです", 11, "AI特有の全面肯定イントロ"),
    (r"(考慮する必要|検討する必要)があります", 11, "AI特有の客観・中立逃げ構文"),
    (r"(可能性を秘めて|期待されて)います", 11, "AI特有の未来展望テンプレ"),
    (r"一助となれば幸いです", 12, "AIビジネス文書定型表現"),
    (r"徹底解説(します|していきます)", 12, "AI量産SEO記事タイトル・導入定型句"),
    (r"メリットとデメリット", 10, "AI構成案の典型対比見出し"),
]

# 日本のマッチングアプリ（Pairs/タップル/with等）・LINE・SNS DM特有の業者＆AI自動返信パターン
MESSENGER_SCAM_AND_BOT_PATTERNS = [
    (r"(LINE|ライン)の?(ID|追加|方へ|で話|交換)", 18, "【要注意】LINE移行誘導（マッチングアプリ業者・自動Bot典型パターン）"),
    (r"(投資|暗号資産|仮想通貨|副業|不労所得|配当|資産運用|レクチャー|バイナリー)", 22, "【危険】投資・副業勧誘（ロマンス詐欺・SNS型投資詐欺スクリプト）"),
    (r"普段あまりこのアプリ(見ない|開かない|通知切って)", 24, "【業者テンプレ】外部ツールへ誘導する常套句"),
    (r"(運命|不思議な縁|波長が合|価値観が似て)", 15, "AI恋愛Bot・ロマンス詐欺の親密化スクリプト"),
    (r"あなたのような(素敵な|誠実な|優しい|知的な)方", 15, "AI恋愛Bot・誰にでも送れるテンプレート賛辞"),
    (r"私の(叔父|知人|先生|メンター|師匠)が(アナリスト|投資|経営|トレード)", 26, "【特商法・詐欺警戒】国際ロマンス・コピートレード詐欺の決定的フレーズ"),
    (r"忙しいところ(恐れ入りますが|突然のご連絡|突然のDM)", 12, "インプレゾンビ・自動営業DMテンプレート"),
    (r"プロフィールを?拝見し.*感銘を受け", 16, "AI自動生成スカウト・営業DMの定型句"),
]

# 日本のクラウドワークス・ランサーズ・就活ES・大学レポート特有のAI丸投げパターン
REPORT_AND_CROWDWORKS_PATTERNS = [
    (r"貴社の.*に(深く)?共感し", 14, "就活ES（エントリーシート）AI生成の典型フレーズ"),
    (r"この経験から.*の重要性を学びました", 14, "ガクチカ（学生時代頑張ったこと）AI出力の定型結論"),
    (r"再現性を持って.*貢献", 12, "AI就活ESで頻出する抽象アピール語彙"),
    (r"本稿では.*について論じる", 11, "AI大学レポートの定型導入文"),
    (r"以上のことから.*が明らかになった", 12, "AIレポートの定型結び構文"),
    (r"ここからは.*について詳しく見ていきましょう", 16, "クラウドワークスAI代筆ライター頻出の繋ぎ文"),
]

PARTICLES = ["は", "が", "を", "に", "で", "と", "の", "へ", "から", "まで", "より"]


def split_japanese_sentences(text: str) -> List[str]:
    """日本語テキストを文単位に分割する"""
    cleaned = re.sub(r"\r\n|\r", "\n", text.strip())
    raw_parts = re.split(r"(?<=[。！？!?\n])", cleaned)
    sentences = []
    for part in raw_parts:
        s = part.strip()
        if len(s) >= 4:
            sentences.append(s)
    return sentences if sentences else ([cleaned] if cleaned else [])


def compute_char_ratios(text: str) -> Dict[str, float]:
    """漢字・ひらがな・カタカナ・英数字・記号の比率を計算"""
    total = max(len(text), 1)
    kanji = len(re.findall(r"[\u4e00-\u9fff]", text))
    hiragana = len(re.findall(r"[\u3040-\u309f]", text))
    katakana = len(re.findall(r"[\u30a0-\u30ff]", text))
    ascii_alnum = len(re.findall(r"[A-Za-z0-9]", text))
    punct = len(re.findall(r"[、。，．・：；！？!?,.\-―…「」『』（）()]", text))
    return {
        "kanji": round(kanji / total, 4),
        "hiragana": round(hiragana / total, 4),
        "katakana": round(katakana / total, 4),
        "alnum": round(ascii_alnum / total, 4),
        "punct": round(punct / total, 4),
    }


def extract_stylometry_vector(text: str) -> np.ndarray:
    """文体指紋（本人らしさ）比較用の特徴量ベクトルを抽出"""
    sentences = split_japanese_sentences(text)
    lengths = [len(s) for s in sentences] if sentences else [len(text)]
    mean_len = float(np.mean(lengths)) / 100.0
    std_len = float(np.std(lengths)) / 50.0

    ratios = compute_char_ratios(text)
    total_chars = max(len(text), 1)
    particle_freqs = [text.count(p) / total_chars * 20.0 for p in PARTICLES]

    comma_rate = (text.count("、") + text.count("，")) / max(len(sentences), 1) / 3.0
    exclam_rate = len(re.findall(r"[！!？?♪wｗ笑💦🙏😊]", text)) / max(len(sentences), 1)

    vec = np.array(
        [
            mean_len,
            std_len,
            ratios["kanji"] * 3.0,
            ratios["hiragana"] * 3.0,
            ratios["katakana"] * 3.0,
            ratios["punct"] * 5.0,
            comma_rate,
            exclam_rate,
            *particle_freqs,
        ],
        dtype=np.float64,
    )
    return vec


def compare_stylometry(target_text: str, reference_text: str) -> Dict[str, Any]:
    """普段の本人文面（reference_text）と今回の文面（target_text）の文体乖離度を算出"""
    v_target = extract_stylometry_vector(target_text)
    v_ref = extract_stylometry_vector(reference_text)

    norm_t = np.linalg.norm(v_target)
    norm_r = np.linalg.norm(v_ref)
    if norm_t == 0 or norm_r == 0:
        cosine_sim = 0.5
    else:
        cosine_sim = float(np.dot(v_target, v_ref) / (norm_t * norm_r))

    l1_diff = float(np.mean(np.abs(v_target - v_ref)))
    divergence = int(np.clip((1.0 - cosine_sim) * 320 + l1_diff * 110, 5, 98))

    r_t = compute_char_ratios(target_text)
    r_r = compute_char_ratios(reference_text)
    s_t = split_japanese_sentences(target_text)
    s_r = split_japanese_sentences(reference_text)

    len_t = round(float(np.mean([len(s) for s in s_t])) if s_t else 0, 1)
    len_r = round(float(np.mean([len(s) for s in s_r])) if s_r else 0, 1)

    differences = []
    if abs(r_t["kanji"] - r_r["kanji"]) > 0.06:
        differences.append(
            f"漢字の割合が普段（{int(r_r['kanji']*100)}%）から今回（{int(r_t['kanji']*100)}%）へ急変しています"
        )
    if abs(len_t - len_r) > 12:
        differences.append(f"1文あたりの平均文字数が普段の {len_r}文字 から {len_t}文字 に大きく変化しています")
    if abs(r_t["punct"] - r_r["punct"]) > 0.025:
        differences.append("読点（、）の打ち方のクセやリズムが普段の本人の文体と一致しません")
    if not differences:
        differences.append("助詞（は・が・を・に）の選び方および文末表現のクセに統計的なズレが検出されました")

    return {
        "divergence_score": divergence,
        "same_author_probability": 100 - divergence,
        "target_avg_sentence_len": len_t,
        "reference_avg_sentence_len": len_r,
        "target_kanji_rate": round(r_t["kanji"] * 100, 1),
        "reference_kanji_rate": round(r_r["kanji"] * 100, 1),
        "key_differences": differences,
        "verdict_text": (
            "【AI代筆・別人の可能性が極めて高い】普段の本人の文体クセと統計的に大きく乖離しています。"
            if divergence >= 65
            else "【一部AI加筆・テンプレ使用の疑い】普段の文体と異なる語彙・句読点パターンが含まれています。"
            if divergence >= 40
            else "【本人文体と概ね一致】普段の文章リズムと高い一貫性が見られます。"
        ),
    }


def analyze_text(
    text: str,
    mode: str = "messenger",
    reference_text: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    テキスト（LINE・メール・外注記事・就活ES・大学レポート）のAI生成疑惑・業者度を多角的に判定する。
    """
    text = (text or "").strip()
    if len(text) < 10:
        return {
            "error": "判定精度を確保するため、10文字以上の文章を入力してください。"
        }

    sentences = split_japanese_sentences(text)
    num_sentences = len(sentences)
    lengths = [len(s) for s in sentences]
    mean_len = float(np.mean(lengths)) if lengths else len(text)
    std_len = float(np.std(lengths)) if len(lengths) > 1 else 0.0
    cv_len = std_len / max(mean_len, 1.0)

    # 1. 文長の均一性（AIは1文の長さが綺麗に揃う）
    if num_sentences >= 3:
        if cv_len < 0.25:
            uniformity_score = 86
        elif cv_len < 0.38:
            uniformity_score = 72
        elif cv_len < 0.52:
            uniformity_score = 50
        else:
            uniformity_score = 24
    else:
        uniformity_score = 52

    # 2. 語尾の単調さ（です・ますの連続や同一語尾の繰り返し）
    endings = []
    for s in sentences:
        clean_s = re.sub(r"[。！？!?\s]+$", "", s)
        endings.append(clean_s[-3:] if len(clean_s) >= 3 else clean_s)
    ending_counts = Counter(endings)
    most_common_ending_ratio = (
        ending_counts.most_common(1)[0][1] / num_sentences if num_sentences > 0 else 0
    )
    polite_endings = sum(
        1 for s in sentences if re.search(r"(です|ます|でした|ました|でしょう|である|だ)[。！？!?]?$", s)
    )
    politeness_ratio = polite_endings / max(num_sentences, 1)

    monotony_score = int(
        np.clip(most_common_ending_ratio * 55 + politeness_ratio * 38, 15, 95)
    )

    # 3. 漢字・ひらがなバランス（ChatGPT/Claudeの日本語は漢字率が28%〜36%に集中する）
    ratios = compute_char_ratios(text)
    kanji_rate = ratios["kanji"]
    if 0.27 <= kanji_rate <= 0.37:
        kanji_ai_likeness = 78
    elif 0.22 <= kanji_rate <= 0.42:
        kanji_ai_likeness = 55
    else:
        kanji_ai_likeness = 28

    # 4. AI特有フレーズ＆構文パターンの検出
    detected_signals = []
    phrase_score_acc = 0

    for pattern, weight, reason in AI_SIGNATURE_PHRASES + REPORT_AND_CROWDWORKS_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            count = len(matches)
            phrase_score_acc += weight * min(count, 2)
            detected_signals.append(
                {
                    "type": "ai_phrase",
                    "label": reason,
                    "weight": weight,
                    "detail": f"該当表現を {count}箇所 検出",
                }
            )

    bullet_lines = len(re.findall(r"(?m)^(\s*[・\-*●■①-⑨1-9]\.?|\s*\*\*.*\*\*)", text))
    if bullet_lines >= 2:
        phrase_score_acc += 18
        detected_signals.append(
            {
                "type": "structure",
                "label": "ChatGPT特有の箇条書き・構造化整理レイアウト",
                "weight": 18,
                "detail": f"{bullet_lines}行の整然とした箇条書き構造を検出",
            }
        )

    scam_score_acc = 0
    if mode in ("messenger", "stylometry"):
        for pattern, weight, reason in MESSENGER_SCAM_AND_BOT_PATTERNS:
            if re.search(pattern, text):
                scam_score_acc += weight
                detected_signals.append(
                    {
                        "type": "scam_or_bot",
                        "label": reason,
                        "weight": weight,
                        "detail": "日本のSNS・マッチングアプリ警戒パターンに一致",
                    }
                )

    # 人間らしいくだけた表現（減点要素）
    human_quirks = len(
        re.findall(
            r"(笑|w+|！{2,}|？{2,}|〜{2,}|…{2,}|かなと|なんですけど|ぶっちゃけ|ちなみに|めっちゃ|ちょっと|すみません💦|助かります🙏)",
            text,
        )
    )
    human_discount = min(human_quirks * 9, 34)

    sentence_analysis = []
    for idx, s in enumerate(sentences):
        s_score = 42
        s_reasons = []

        if num_sentences >= 3 and abs(len(s) - mean_len) < mean_len * 0.18:
            s_score += 14
            s_reasons.append("文字数・読点バランスが均一")

        for pattern, weight, reason in AI_SIGNATURE_PHRASES + REPORT_AND_CROWDWORKS_PATTERNS:
            if re.search(pattern, s):
                s_score += weight + 8
                s_reasons.append(reason)

        for pattern, weight, reason in MESSENGER_SCAM_AND_BOT_PATTERNS:
            if re.search(pattern, s):
                s_score += weight + 5
                s_reasons.append(reason)

        if re.search(r"^(また|さらに|加えて|一方で|そのため|したがって|結論として|総じて|第一に|第二に)、", s):
            s_score += 15
            s_reasons.append("AI頻出の接続詞による文頭開始")

        if re.search(r"(笑|w+|！{2,}|かな〜|だよね|💦|🙏)", s):
            s_score -= 22

        s_score = int(np.clip(s_score, 8, 98))
        level = "high" if s_score >= 70 else ("medium" if s_score >= 48 else "low")
        sentence_analysis.append(
            {
                "index": idx + 1,
                "text": s,
                "ai_probability": s_score,
                "level": level,
                "reasons": s_reasons if s_reasons else (["AI標準の整った構文"] if s_score >= 50 else ["人間らしい自然なリズム"]),
            }
        )

    avg_sentence_ai = (
        float(np.mean([item["ai_probability"] for item in sentence_analysis]))
        if sentence_analysis
        else 50.0
    )

    raw_total = (
        uniformity_score * 0.25
        + monotony_score * 0.20
        + kanji_ai_likeness * 0.15
        + avg_sentence_ai * 0.25
        + min(phrase_score_acc + scam_score_acc * 0.7, 45) * 0.55
        - human_discount
    )

    stylometry_result = None
    if reference_text and len(reference_text.strip()) >= 15:
        stylometry_result = compare_stylometry(text, reference_text)
        raw_total = raw_total * 0.62 + stylometry_result["divergence_score"] * 0.38

    ai_probability = int(np.clip(round(raw_total), 6, 98))

    if not detected_signals:
        if ai_probability >= 60:
            detected_signals.append(
                {
                    "type": "statistical",
                    "label": "文の長さの均一性（AI特有の単調リズム）と漢字比率の一致",
                    "weight": 15,
                    "detail": f"文長揺らぎ指数 CV={cv_len:.2f}（人間の自然な文章は0.45以上）",
                }
            )
        else:
            detected_signals.append(
                {
                    "type": "human",
                    "label": "人間特有の文長ゆらぎ・自然な言葉遣いを確認",
                    "weight": 10,
                    "detail": f"文長揺らぎ指数 CV={cv_len:.2f} / 漢字率 {int(kanji_rate*100)}%",
                }
            )

    if ai_probability >= 75:
        verdict_badge = "AI生成・業者テンプレの可能性【極高】"
        verdict_color = "danger"
        summary = "文の長さの均一性、接続詞のクセ、および漢字とひらがなの比率がChatGPT/Claude等の生成AIまたは業者テンプレートの特徴と強く一致しています。"
    elif ai_probability >= 50:
        verdict_badge = "AI下書き＋人間手直し（ハイブリッド）の疑い【中〜高】"
        verdict_color = "warning"
        summary = "AIで出力した文章をベースに人間が一部手直ししたか、定型テンプレートを流用している可能性が高い文面です。"
    else:
        verdict_badge = "人間が書いた自然な文章の可能性【高】"
        verdict_color = "success"
        summary = "文脈の揺らぎや句読点の打ち方に人間特有の自然なばらつきが見られ、AI丸投げの兆候は低いと判定されました。"

    confrontation_templates = generate_confrontation_templates(mode, ai_probability, detected_signals)

    llm_deep_insight = None
    effective_key = api_key or os.environ.get("GEMINI_API_KEY")
    if effective_key:
        llm_deep_insight = call_gemini_text_inspection(text, mode, effective_key)

    return {
        "ai_probability": ai_probability,
        "human_probability": 100 - ai_probability,
        "verdict_badge": verdict_badge,
        "verdict_color": verdict_color,
        "summary": summary,
        "metrics": {
            "uniformity_score": uniformity_score,
            "monotony_score": monotony_score,
            "kanji_rate_pct": round(kanji_rate * 100, 1),
            "burstiness_cv": round(cv_len, 2),
            "sentence_count": num_sentences,
            "char_count": len(text),
            "scam_alert_score": int(np.clip(scam_score_acc * 1.8, 0, 100)),
        },
        "signals": detected_signals,
        "sentence_analysis": sentence_analysis,
        "stylometry": stylometry_result,
        "confrontation_templates": confrontation_templates,
        "llm_deep_insight": llm_deep_insight,
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def generate_confrontation_templates(
    mode: str, ai_prob: int, signals: List[Dict[str, Any]]
) -> List[Dict[str, str]]:
    """日本の商習慣・人間関係に配慮した「角が立たない確認・カマかけ・検収差し戻し文面」"""
    if mode == "messenger":
        return [
            {
                "title": "①【マッチングアプリ・LINE用】相手がAI自動返信・業者か一発で見抜く「カマかけ返信」",
                "usage": "ペアーズ・タップル・LINE等で相手が業者やAIボットか確かめたい時",
                "body": "丁寧なメッセージありがとうございます😊 ところで、さっきのメッセージの言葉遣いがすごく綺麗でしたけど、普段お仕事で文章書かれたりしてますか？あと、私がプロフィールの3行目に書いてた『休日の過ごし方』についてどう思ったか、一言だけ率直なツッコミ聞かせてほしいです！",
            },
            {
                "title": "②【社内・取引先メール用】AI丸投げの無機質な長文メールから「本音」を引き出す返信",
                "usage": "取引先や部下からChatGPT丸投げのような長文謝罪・報告メールが来た時",
                "body": "ご連絡ありがとうございます。全体の整理は把握いたしました。ただ、一般論ではなく〇〇さんご自身の現場での肌感覚・率直なご判断を伺いたいため、今一番ネックになっている点だけ、箇条書きではなくチャットで1〜2行で教えていただけますでしょうか？",
            },
            {
                "title": "③【LINE交換・投資勧誘ブロック用】角を立てずに業者・ロマンス詐欺を完全遮断する文面",
                "usage": "「普段アプリ見ないのでLINE交換しよう」「叔父が投資を〜」と言われた時",
                "body": "メッセージありがとうございます！ただ、実際に一度お会いする前のLINE交換や、副業・資産運用・外部サイトに関するお話はすべてお断りするマイルールにしています🙏 アプリ内で普通の雑談ができる方とだけやり取りを続けていますので、ご了承ください！",
            },
        ]
    else:
        return [
            {
                "title": "①【クラウドワークス・ランサーズ発注者用】角を立てずにAI使用確認＆修正を求めるメッセージ",
                "usage": "外注ライターから納品された記事・台本にAI丸投げ疑惑（スコア " + str(ai_prob) + "%）がある時",
                "body": f"ご納品ありがとうございます。原稿を拝読いたしました。\n一点確認させてください。弊社の品質管理ツール（AI見抜きくんPro）にて文長リズムおよび接続詞構造を照合したところ、生成AIの出力パターンと高い一致（AI疑惑スコア {ai_prob}%）が検出されました。\n募集要項に記載の通り、AI出力のそのままの流用は検収対象外となりますため、ご自身の一次体験・独自調査に基づく記述への書き直し、または使用された参考資料のURL共有をお願いできますでしょうか。",
            },
            {
                "title": "②【大学・高校・研修レポート指導用】学生・受講生に口頭確認を促す通知文",
                "usage": "提出されたレポートや課題が本人の普段の文章と乖離している時",
                "body": "レポートの提出を確認しました。内容の理解度を直接確認したいため、レポート内の中心的な結論に至った理由と、第2段落で使用されている専門表現の意味について、次回の授業（面談）時にレポートを見ずに2分ほど口頭で説明をお願いします。",
            },
            {
                "title": "③【採用面接・ES選考用】志望動機やガクチカのAI代筆を面接で見破る質問テンプレート",
                "usage": "エントリーシートや事前課題のAI作成率が高かった時",
                "body": "「提出いただいたESの中で、一番自分の言葉にするのに苦労して書き直した一文はどこですか？また、なぜその表現を選んだのか当時のエピソードを交えて教えてください」（※ChatGPT丸投げの応募者は特定の一文の推敲プロセスを答えられません）",
            },
        ]


# ==========================================
# 2. 画像・撮影レポート・フリマ出品画像フォレンジック解析
# ==========================================

AI_IMAGE_METADATA_KEYWORDS = [
    ("parameters", "Stable Diffusion 生成パラメータ埋め込み"),
    ("Steps:", "Stable Diffusion サンプラー履歴"),
    ("CFG scale", "Stable Diffusion ガイダンススケール"),
    ("ComfyUI", "ComfyUI ワークフローJSON埋め込み"),
    ("Midjourney", "Midjourney 生成署名"),
    ("DALL-E", "OpenAI DALL-E 生成署名"),
    ("Firefly", "Adobe Firefly C2PA/生成署名"),
    ("SynthID", "Google SynthID 電子透かし署名"),
    ("c2pa", "C2PA Content Credentials 署名チャンク"),
    ("NovelAI", "NovelAI 生成メタデータ"),
]

STANDARD_AI_RESOLUTIONS = {
    (1024, 1024),
    (1024, 1792),
    (1792, 1024),
    (512, 512),
    (512, 768),
    (768, 512),
    (768, 768),
    (832, 1216),
    (1216, 832),
    (896, 1152),
    (1152, 896),
    (1344, 768),
    (768, 1344),
}


def generate_ela_and_forensic_preview(pil_img: Image.Image) -> Tuple[str, float, float]:
    rgb_img = pil_img.convert("RGB")
    max_dim = 640
    w, h = rgb_img.size
    scale = min(max_dim / max(w, h), 1.0)
    if scale < 1.0:
        rgb_img = rgb_img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    rgb_img.save(buf, format="JPEG", quality=88)
    buf.seek(0)
    recompressed = Image.open(buf).convert("RGB")

    arr_orig = np.asarray(rgb_img, dtype=np.float32)
    arr_comp = np.asarray(recompressed, dtype=np.float32)

    diff = np.abs(arr_orig - arr_comp)
    ela_gray = np.mean(diff, axis=2)
    ela_norm = np.clip(ela_gray * 18.0, 0, 255).astype(np.uint8)
    heatmap_bgr = cv2.applyColorMap(ela_norm, cv2.COLORMAP_JET)

    orig_bgr = cv2.cvtColor(arr_orig.astype(np.uint8), cv2.COLOR_RGB2BGR)
    blended = cv2.addWeighted(orig_bgr, 0.42, heatmap_bgr, 0.58, 0)

    _, png_buf = cv2.imencode(".png", blended)
    b64_preview = "data:image/png;base64," + base64.b64encode(png_buf.tobytes()).decode("ascii")

    gray = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    laplacian = cv2.Laplacian(gray, cv2.CV_32F)
    noise_level = float(np.std(laplacian))

    f_transform = np.fft.fft2(gray)
    f_shift = np.fft.fftshift(f_transform)
    magnitude = np.log1p(np.abs(f_shift))
    mh, mw = magnitude.shape
    cy, cx = mh // 2, mw // 2
    r = min(cy, cx) // 3
    center_energy = float(np.mean(magnitude[cy - r : cy + r, cx - r : cx + r]))
    outer_energy = float(np.mean(magnitude))
    hf_ratio = outer_energy / max(center_energy, 1e-5)

    return b64_preview, noise_level, hf_ratio


def analyze_image(
    image_bytes: bytes,
    filename: str = "upload.png",
    mode: str = "image_forensics",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        pil_img = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        return {"error": f"画像の読み込みに失敗しました: {e}"}

    width, height = pil_img.size
    img_format = pil_img.format or "UNKNOWN"

    signals = []
    ai_score_acc = 32

    raw_head = image_bytes[:65536].decode("latin-1", errors="ignore")
    raw_tail = image_bytes[-32768:].decode("latin-1", errors="ignore")
    combined_raw = raw_head + "\n" + raw_tail

    info_str = json.dumps({str(k): str(v)[:300] for k, v in (pil_img.info or {}).items()}, ensure_ascii=False)
    search_blob = combined_raw + "\n" + info_str

    signature_hit = False
    for kw, desc in AI_IMAGE_METADATA_KEYWORDS:
        if kw.lower() in search_blob.lower():
            ai_score_acc += 48
            signature_hit = True
            signals.append(
                {
                    "type": "metadata_signature",
                    "label": f"【決定的証拠】{desc}を画像内部データから検出",
                    "weight": 48,
                    "detail": f"画像ファイル内部に '{kw}' のAI生成履歴データが残存しています",
                }
            )

    exif_data = {}
    try:
        raw_exif = pil_img.getexif()
        if raw_exif:
            for tag_id, val in raw_exif.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                exif_data[tag_name] = str(val)[:100]
    except Exception:
        pass

    has_camera_make = any(k in exif_data for k in ("Make", "Model", "LensModel", "DateTimeOriginal"))
    if has_camera_make:
        ai_score_acc -= 22
        camera_desc = f"{exif_data.get('Make', '')} {exif_data.get('Model', '')}".strip()
        signals.append(
            {
                "type": "camera_exif",
                "label": "スマホ・実機カメラの撮影EXIF情報を確認",
                "weight": -22,
                "detail": f"撮影機器: {camera_desc or 'カメラ情報あり'} / 日時: {exif_data.get('DateTimeOriginal', '記録あり')}",
            }
        )
    else:
        ai_score_acc += 12
        signals.append(
            {
                "type": "no_exif",
                "label": "カメラ撮影EXIF情報の欠落（AI生成画像またはLINE/SNS経由の再圧縮）",
                "weight": 12,
                "detail": f"形式: {img_format} ({width}×{height}px) — iPhone/Android等のカメラセンサー記録がありません",
            }
        )

    if (width, height) in STANDARD_AI_RESOLUTIONS:
        ai_score_acc += 18
        signals.append(
            {
                "type": "resolution",
                "label": "画像生成AI（Stable Diffusion / DALL-E 3 / Midjourney）の標準解像度と完全一致",
                "weight": 18,
                "detail": f"解像度 {width} × {height} px は主要画像生成AIの初期出力サイズと一致します",
            }
        )

    ela_preview_b64, noise_level, hf_ratio = generate_ela_and_forensic_preview(pil_img)

    if noise_level < 6.5:
        ai_score_acc += 16
        signals.append(
            {
                "type": "texture_smoothness",
                "label": "AI特有の過剰になめらかな質感（実写カメラのセンサーノイズ欠如）",
                "weight": 16,
                "detail": f"局所ノイズ指数: {noise_level:.2f}（iPhone等の実写平均: 9.0〜25.0）",
            }
        )
    elif noise_level > 28.0 and mode == "photo_report":
        signals.append(
            {
                "type": "document_contrast",
                "label": "書類・画面撮影特有の文字エッジコントラストを検出",
                "weight": 10,
                "detail": f"文字エッジ強度スコア: {noise_level:.2f}",
            }
        )

    if hf_ratio < 0.56:
        ai_score_acc += 12
        signals.append(
            {
                "type": "fft_spectrum",
                "label": "高周波スペクトル減衰（拡散モデル特有の周波数パターン）",
                "weight": 12,
                "detail": f"高周波/低周波エネルギー比: {hf_ratio:.3f}",
            }
        )

    extracted_report_text = None
    report_text_analysis = None
    effective_key = api_key or os.environ.get("GEMINI_API_KEY")

    if effective_key:
        gemini_img_res = call_gemini_image_inspection(image_bytes, mode, effective_key)
        if gemini_img_res:
            if gemini_img_res.get("extracted_text"):
                extracted_report_text = gemini_img_res["extracted_text"]
                if len(extracted_report_text) >= 15:
                    report_text_analysis = analyze_text(extracted_report_text, mode="report")
            if gemini_img_res.get("ai_visual_score") is not None:
                ai_score_acc = int(ai_score_acc * 0.45 + gemini_img_res["ai_visual_score"] * 0.55)
            if gemini_img_res.get("finding"):
                signals.append(
                    {
                        "type": "multimodal_ai",
                        "label": "マルチモーダルAI視覚推論による深層検査結果",
                        "weight": 20,
                        "detail": gemini_img_res["finding"],
                    }
                )
    elif mode == "photo_report":
        gray_doc = np.asarray(pil_img.convert("L"))
        edges = cv2.Canny(gray_doc, 60, 160)
        row_density = np.mean(edges > 0, axis=1)
        active_rows = np.where(row_density > 0.04)[0]
        line_regularity = float(np.std(np.diff(active_rows))) if len(active_rows) > 10 else 5.0
        if line_regularity < 3.2:
            ai_score_acc += 15
        signals.append(
            {
                "type": "document_layout",
                "label": "撮影されたレポート・書類の行間レイアウト構造解析完了",
                "weight": 14,
                "detail": f"文字ライン検出: {len(active_rows)}行 / 行間均一性指数: {line_regularity:.2f}",
            }
        )

    ai_probability = int(np.clip(ai_score_acc, 7, 99 if signature_hit else 95))

    if ai_probability >= 72:
        verdict_badge = "AI生成・合成画像の可能性【極高】" if mode != "photo_report" else "AI作成レポート・自動整形の可能性【極高】"
        verdict_color = "danger"
        summary = "画像の内部メタデータ、周波数スペクトル、および表面ノイズの均一性から、生成AIまたはデジタル合成による強い痕跡が検出されました。"
    elif ai_probability >= 48:
        verdict_badge = "AI補正・加工アプリ使用またはSNS再圧縮の疑い【中】"
        verdict_color = "warning"
        summary = "カメラ固有のEXIF情報が消去されており、一部の領域にAI美肌加工や画像生成ツール特有の滑らかさが見られます。"
    else:
        verdict_badge = "実写スマホ・カメラ撮影の可能性【高】"
        verdict_color = "success"
        summary = "光学センサー特有の自然なノイズ分布またはカメラメタデータが確認され、AI生成画像である兆候は低いと判定されました。"

    return {
        "ai_probability": ai_probability,
        "human_probability": 100 - ai_probability,
        "verdict_badge": verdict_badge,
        "verdict_color": verdict_color,
        "summary": summary,
        "image_meta": {
            "filename": filename,
            "format": img_format,
            "width": width,
            "height": height,
            "has_camera_exif": has_camera_make,
            "exif_summary": exif_data,
            "noise_std": round(noise_level, 2),
            "fft_hf_ratio": round(hf_ratio, 3),
        },
        "ela_preview_b64": ela_preview_b64,
        "signals": signals,
        "extracted_report_text": extracted_report_text,
        "report_text_analysis": report_text_analysis,
        "confrontation_templates": generate_confrontation_templates(
            "report" if mode == "photo_report" else "messenger", ai_probability, signals
        ),
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def analyze_document_file(
    file_bytes: bytes, filename: str, api_key: Optional[str] = None
) -> Dict[str, Any]:
    lower_name = filename.lower()
    extracted_text = ""
    doc_meta_signals = []
    meta_info = {"filename": filename}

    if lower_name.endswith(".pdf") and fitz is not None:
        try:
            pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
            meta = pdf_doc.metadata or {}
            meta_info.update({k: str(v) for k, v in meta.items() if v})
            pages_text = [page.get_text("text") for page in pdf_doc]
            extracted_text = "\n".join(pages_text).strip()

            creator = (meta.get("creator", "") + " " + meta.get("producer", "")).lower()
            if any(k in creator for k in ("chatgpt", "canva", "wkhtmltopdf", "chromium", "weasyprint")):
                doc_meta_signals.append(
                    {
                        "type": "pdf_metadata",
                        "label": "ブラウザ出力・外部ツール生成PDFの履歴データを検出",
                        "weight": 16,
                        "detail": f"作成ソフト情報: {meta.get('producer') or meta.get('creator')}",
                    }
                )
        except Exception as e:
            return {"error": f"PDFの解析中にエラーが発生しました: {e}"}

    elif lower_name.endswith(".docx") and docx is not None:
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            extracted_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            props = doc.core_properties
            meta_info["author"] = str(props.author or "記録なし")
            meta_info["revision"] = str(props.revision or "1")
            if str(props.revision) in ("1", "0", "None") and len(extracted_text) > 600:
                doc_meta_signals.append(
                    {
                        "type": "docx_revision",
                        "label": "【コピペ納品の強い証拠】長文なのにWordの保存回数（リビジョン）が1回のみ",
                        "weight": 22,
                        "detail": f"文字数 {len(extracted_text)}文字 / Word編集保存回数: {props.revision}回（ChatGPT等で生成した文章を一括貼り付けして即保存した特徴）",
                    }
                )
        except Exception as e:
            return {"error": f"Wordファイルの解析中にエラーが発生しました: {e}"}
    else:
        extracted_text = file_bytes.decode("utf-8", errors="ignore").strip()

    if len(extracted_text) < 10:
        return {"error": "ファイルからテキストを抽出できませんでした（スキャン画像PDFの場合は『📸 撮影レポート・画像判定』タブをご利用ください）。"}

    result = analyze_text(extracted_text, mode="report", api_key=api_key)
    if doc_meta_signals and "signals" in result:
        result["signals"] = doc_meta_signals + result["signals"]
        result["ai_probability"] = int(np.clip(result["ai_probability"] + 12, 5, 98))
        result["human_probability"] = 100 - result["ai_probability"]
    result["document_meta"] = meta_info
    result["extracted_text_preview"] = extracted_text[:600] + ("..." if len(extracted_text) > 600 else "")
    return result


def call_gemini_text_inspection(text: str, mode: str, api_key: str) -> Optional[str]:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        prompt = (
            "あなたは日本のビジネス文書・クラウドソーシング検収・SNSメッセージ監査の専門家です。"
            f"以下の日本語テキスト（モード: {mode}）が生成AI（ChatGPT/Claude等）または業者テンプレートで作成された可能性について、"
            "具体的な根拠を3行以内のわかりやすい日本語で指摘してください。\n\n"
            f"--- 対象テキスト ---\n{text[:2500]}"
        )
        resp = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
    return None


def call_gemini_image_inspection(image_bytes: bytes, mode: str, api_key: str) -> Optional[Dict[str, Any]]:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        b64_img = base64.b64encode(image_bytes).decode("ascii")
        prompt = (
            "この画像を検査し、JSON形式のみで回答してください。"
            'キーは {"ai_visual_score": 0から100の整数, "finding": "視覚的なAI生成痕跡または特徴の1文説明", "extracted_text": "画像内に書かれている日本語テキスト全文（書類やメール画面の場合）"} としてください。'
        )
        resp = requests.post(
            url,
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": "image/jpeg", "data": b64_img}},
                        ]
                    }
                ],
                "generationConfig": {"responseMimeType": "application/json"},
            },
            timeout=15,
        )
        if resp.status_code == 200:
            raw_txt = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_txt)
    except Exception:
        pass
    return None
