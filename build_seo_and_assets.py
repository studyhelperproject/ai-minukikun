import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
BASE_URL = "https://studyhelperproject.github.io/ai-minukikun"


def generate_og_image() -> None:
    """1200x630 の高インパクトな日本語OGPアイキャッチ画像を生成"""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), color=(9, 13, 22))
    draw = ImageDraw.Draw(img)

    # 背景グラデーション風装飾
    draw.rectangle((0, 0, w, 14), fill=(99, 102, 241))
    draw.rectangle((0, h - 14, w, h), fill=(6, 182, 212))
    draw.rounded_rectangle((45, 45, w - 45, h - 45), radius=24, fill=(18, 24, 38), outline=(59, 76, 114), width=3)

    # スコアゲージ風サークル描画
    cx, cy, r = 960, 315, 145
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(45, 18, 28), outline=(239, 68, 68), width=12)

    # 日本語フォントロード（Windows標準Meiryo / YuGothic）
    font_paths = [
        r"C:\Windows\Fonts\meiryob.ttc",
        r"C:\Windows\Fonts\YuGothB.ttc",
        r"C:\Windows\Fonts\msgothic.ttc",
    ]
    font_path = next((p for p in font_paths if os.path.exists(p)), None)

    if font_path:
        f_huge = ImageFont.truetype(font_path, 62)
        f_title = ImageFont.truetype(font_path, 42)
        f_sub = ImageFont.truetype(font_path, 26)
        f_badge = ImageFont.truetype(font_path, 24)
        f_score = ImageFont.truetype(font_path, 76)
    else:
        f_huge = f_title = f_sub = f_badge = f_score = ImageFont.load_default()

    draw.rounded_rectangle((85, 85, 540, 135), radius=10, fill=(30, 58, 138))
    draw.text((105, 94), "日本特化・ゼロトラストAI監査ツール", fill=(56, 189, 248), font=f_badge)

    draw.text((85, 160), "AI見抜きくん Pro", fill=(255, 255, 255), font=f_huge)
    draw.text((85, 255), "そのLINE・外注記事・レポート、", fill=(241, 245, 249), font=f_title)
    draw.text((85, 315), "ChatGPT丸投げかも？", fill=(251, 191, 36), font=f_title)

    draw.text((85, 405), "✓ ペアーズ・LINEのAI業者＆ロマンス詐欺検知", fill=(148, 163, 184), font=f_sub)
    draw.text((85, 450), "✓ クラウドワークス記事のWord一括コピペ検知", fill=(148, 163, 184), font=f_sub)
    draw.text((85, 495), "✓ 普段の本人文体とのズレ＆画像ELAヒートマップ", fill=(52, 211, 153), font=f_sub)

    draw.text((cx - 88, cy - 55), "92%", fill=(248, 113, 113), font=f_score)
    draw.text((cx - 82, cy + 40), "AI疑惑【極高】", fill=(255, 255, 255), font=f_badge)

    out_path = os.path.join(STATIC_DIR, "og-image.png")
    img.save(out_path, format="PNG", optimize=True)
    print("Generated OGP image:", out_path)


LP_PAGES = [
    {
        "filename": "lp-matching.html",
        "title": "マッチングアプリ（ペアーズ・タップル・with）のAI業者・ロマンス詐欺LINEを見抜く方法【無料診断】 | AI見抜きくん Pro",
        "h1": "マッチングアプリやLINEの「AI業者・投資ロマンス詐欺」を3秒で見抜く無料チェッカー",
        "desc": "ペアーズ、タップル、with、東カレデートやLINEで「返信は丁寧だけどAIっぽい」「すぐLINE交換を求められる」と感じたら要注意。AI見抜きくんProで業者の定型スクリプトとChatGPT自動返信を即座に判定します。",
        "keywords": "マッチングアプリ AI業者 見分け方, ペアーズ 業者 LINE誘導, ロマンス詐欺 AI 判定, LINE AI返信 チェッカー",
        "problem_points": [
            "「普段あまりこのアプリ見ないのでLINEで話しませんか？」と3通目以内に言われる",
            "こちらのプロフィールを過剰に褒めるが、具体的な質問への回答が噛み合わない（ChatGPT自動応答ボット）",
            "「叔父がアナリスト」「AI配当・暗号資産の勉強」など投資・副業の話題が突然出る",
            "最初の短文メッセージと、長文メッセージで「文体のクセ（句読点や漢字率）」が別人のように変わる",
        ],
        "solution_text": "『AI見抜きくん Pro』は、日本のマッチングアプリで横行する業者テンプレートとChatGPT特有の構文リズムを同時にスキャンします。さらに、相手がAIボットか人間かを一発で炙り出す「カマかけ質問テンプレート」を自動生成します。",
        "cta_tab": "messenger",
    },
    {
        "filename": "lp-crowdworks.html",
        "title": "クラウドワークス・ランサーズ外注記事のChatGPT丸投げ・コピペ見抜き方【Wordリビジョン監査】 | AI見抜きくん Pro",
        "h1": "クラウドワークス・ランサーズ納品記事の「ChatGPT丸投げ・一括コピペ」を証拠付きで見抜く監査ツール",
        "desc": "Webライターへ外注したSEO記事やYouTube台本がChatGPTのコピペか3秒で判定。Wordファイル(.docx)の保存リビジョン回数（1回のみ＝コピペの証拠）と、普段のチャット文体との乖離スコアから検収差し戻し文面まで自動作成。",
        "keywords": "クラウドワークス AI記事 見抜き方, ランサーズ ChatGPT 丸投げ 判定, 外注ライター AI チェッカー, Word リビジョン コピペ検知",
        "problem_points": [
            "「AI使用禁止」で発注したのに、「〜という点が挙げられます」「いかがでしたでしょうか」ばかりの無機質な記事が納品された",
            "チャットワークやメッセージ欄での連絡文はくだけた短文なのに、納品された記事だけ急に論文のようなAI構文になっている",
            "感覚だけで「AIですよね？」と指摘するとライターとトラブルになるため、客観的な数値データと監査証明書が欲しい",
            "Wordファイル（.docx）が本当に人間が推敲して書いたものか、ChatGPTから一括貼り付けして1回保存しただけか知りたい",
        ],
        "solution_text": "『AI見抜きくん Pro』の「本人文体との比較監査」および「Word内部リビジョン検査」を使えば、普段のチャット文面と納品原稿の統計的乖離を数値化し、角を立てずに修正・差し戻しを要求できる検収メッセージ文面とPDF監査証明書を即座に出力できます。",
        "cta_tab": "stylometry",
    },
    {
        "filename": "lp-report.html",
        "title": "大学レポート・就活ES（ガクチカ）のAI代筆・ChatGPT使用率がバレる理由と無料チェッカー | AI見抜きくん Pro",
        "h1": "大学課題レポート・就活ES（エントリーシート）のChatGPT作成率＆本人文体一致度チェッカー",
        "desc": "提出された紙の撮影レポート、PDF、Word課題、就活ES（ガクチカ・志望動機）のAI生成確率をハイブリッド判定。文長の均一性（Burstiness）や漢字含有率、普段のメール文体とのズレを3秒で可視化します。",
        "keywords": "大学レポート AI バレる 判定, 就活ES ChatGPT チェッカー, ガクチカ AI判定 ツール, レポート AI 見分け方 日本語",
        "problem_points": [
            "「まず第一に〜」「一方で〜」「この経験から〜の重要性を学びました」など、ChatGPT特有の対比・要約構文が多用されている",
            "1文ごとの文字数のばらつき（Burstiness）が極端に少なく、漢字含有率が常に30%前後に張り付いている",
            "紙で提出されたレポートやPC画面をスマホカメラで撮影して、その場でAI代筆疑惑をスキャンしたい",
            "採用面接や口頭試問で、応募者・学生が本当に自分で書いたかを確かめる「深掘り質問」を用意したい",
        ],
        "solution_text": "『AI見抜きくん Pro』は英語直訳の海外製AIチェッカーと異なり、日本語の助詞分布・読点リズム・漢字比率に特化した統計エンジンを搭載。入力データはサーバーに一切保存されないゼロトラスト設計のため、教育機関や人事採用の現場でも安全にご利用いただけます。",
        "cta_tab": "messenger",
    },
    {
        "filename": "lp-mercari.html",
        "title": "メルカリ出品画像・SNSアイコンのAI生成・加工フェイクを見破るELAヒートマップ解析ツール | AI見抜きくん Pro",
        "h1": "メルカリ・ヤフオク出品画像やSNSアイコンの「AI生成・無断加工・フェイク写真」を見破る真贋チェッカー",
        "desc": "画像のバイナリ内部に残されたStable Diffusion / Midjourney / C2PAの生成署名と、iPhone/AndroidカメラEXIFの有無、さらにELA（圧縮誤差ヒートマップ）でAI生成画像や加工箇所をブラウザ内で即座に可視化します。",
        "keywords": "AI画像 見分け方 ツール, メルカリ AI生成画像 判定, SNSアイコン AI チェッカー, Stable Diffusion メタデータ 確認",
        "problem_points": [
            "マッチングアプリやSNSのプロフィール写真が実在する人物か、AI生成（Stable Diffusion / Midjourney）の架空人物か見分けたい",
            "フリマアプリ（メルカリ・ヤフオク）の商品写真が実物をスマホで撮影したものか、AI生成・過度な加工画像か調べたい",
            "提出された証拠写真にiPhoneや実機カメラの光学EXIF情報が残っているか、合成による圧縮誤差（ELA）がないか確認したい",
        ],
        "solution_text": "『AI見抜きくん Pro』の画像フォレンジック機能は、画像を外部サーバーへアップロードすることなくお使いのブラウザ内でバイナリチャンク走査とELA（Error Level Analysis）ヒートマップ生成を実行し、AI生成の決定的証拠を検出します。",
        "cta_tab": "photo_report",
    },
]


def generate_lp_pages() -> None:
    for lp in LP_PAGES:
        problems_html = "\n".join(
            f"<li style='margin-bottom:0.55rem;'>✅ {p}</li>" for p in lp["problem_points"]
        )
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{lp["title"]}</title>
  <meta name="description" content="{lp["desc"]}" />
  <meta name="keywords" content="{lp["keywords"]}" />
  <meta property="og:title" content="{lp["title"]}" />
  <meta property="og:description" content="{lp["desc"]}" />
  <meta property="og:image" content="{BASE_URL}/og-image.png" />
  <meta property="og:url" content="{BASE_URL}/{lp["filename"]}" />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{BASE_URL}/og-image.png" />
  <link rel="canonical" href="{BASE_URL}/{lp["filename"]}" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header class="app-header">
    <div class="header-inner">
      <a href="index.html" class="brand" style="text-decoration:none; color:inherit;">
        <div class="brand-icon">🔍</div>
        <div>
          <div class="brand-title">AI見抜きくん Pro <span class="brand-badge">公式ガイド＆無料診断</span></div>
          <div class="brand-sub">日本特化・ゼロトラストAI真贋チェッカー</div>
        </div>
      </a>
      <a href="index.html" class="btn btn-primary btn-sm">🚀 今すぐ無料でAI判定する（登録不要）</a>
    </div>
  </header>

  <main class="container" style="max-width: 920px;">
    <article class="card" style="padding: 2rem;">
      <div style="font-size: 0.78rem; color: #38bdf8; font-weight: 700; margin-bottom: 0.5rem;">
        🇯🇵 日本語AIフォレンジック監査・公式解説コラム
      </div>
      <h1 style="font-size: 1.55rem; line-height: 1.4; margin-bottom: 1rem;">{lp["h1"]}</h1>
      <p style="font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1.5rem;">{lp["desc"]}</p>

      <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.05rem; color: #f87171; margin-bottom: 0.75rem;">⚠️ こんな特徴・違和感はありませんか？（AI生成・業者の典型サイン）</h2>
        <ul style="list-style: none; font-size: 0.9rem; line-height: 1.7;">
          {problems_html}
        </ul>
      </div>

      <h2 style="font-size: 1.15rem; margin-bottom: 0.75rem; color: #34d399;">🛡️ 解決策：『AI見抜きくん Pro』で3秒・外部保存ゼロの安全監査</h2>
      <p style="font-size: 0.92rem; margin-bottom: 1.5rem; line-height: 1.8;">{lp["solution_text"]}</p>

      <div style="text-align: center; padding: 1.5rem; background: var(--bg-input); border-radius: 12px; border: 1px solid var(--primary);">
        <div style="font-size: 1.1rem; font-weight: 800; margin-bottom: 0.5rem;">👇 1日3回まで完全無料・会員登録不要で今すぐチェック</div>
        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">入力された文章や画像は外部サーバーに一切保存されず、お使いの端末内のみで安全に解析されます。</p>
        <a href="index.html" class="btn btn-gold" style="font-size: 1.05rem; padding: 0.85rem 2rem;">
          🔍 AI見抜きくん Pro 無料診断ツールを開く
        </a>
      </div>

      <hr style="border: none; border-top: 1px solid var(--border-color); margin: 2rem 0;" />
      <div style="font-size: 0.85rem;">
        <strong>📚 関連するAI真贋チェック特化ページ：</strong>
        <ul style="margin-top: 0.5rem; padding-left: 1.2rem; line-height: 1.9;">
          <li><a href="lp-matching.html" style="color: #38bdf8;">マッチングアプリ（ペアーズ・タップル・LINE）のAI業者・ロマンス詐欺を見抜く方法</a></li>
          <li><a href="lp-crowdworks.html" style="color: #38bdf8;">クラウドワークス・ランサーズ外注記事のChatGPT丸投げ＆Wordリビジョン監査</a></li>
          <li><a href="lp-report.html" style="color: #38bdf8;">大学レポート・就活ES（ガクチカ）のAI代筆チェッカー＆本人文体比較</a></li>
          <li><a href="lp-mercari.html" style="color: #38bdf8;">メルカリ出品画像・SNSアイコンのAI生成ヒートマップ（ELA）真贋解析</a></li>
        </ul>
      </div>
    </article>
  </main>
</body>
</html>"""
        out_file = os.path.join(STATIC_DIR, lp["filename"])
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        print("Generated SEO LP:", out_file)


def update_sitemap() -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    urls = ["", "lp-matching.html", "lp-crowdworks.html", "lp-report.html", "lp-mercari.html"]
    items = []
    for u in urls:
        loc = f"{BASE_URL}/{u}" if u else f"{BASE_URL}/"
        prio = "1.0" if not u else "0.9"
        items.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(items) + "\n</urlset>\n"
    out_path = os.path.join(STATIC_DIR, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("Updated sitemap.xml with", len(urls), "URLs")


if __name__ == "__main__":
    generate_og_image()
    generate_lp_pages()
    update_sitemap()
