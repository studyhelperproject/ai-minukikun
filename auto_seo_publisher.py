import os
import shutil
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
BASE_URL = "https://studyhelperproject.github.io/ai-minukikun"
NOTE_URL = "https://note.com/safe_swift4998/n/na1af72c84723"

# ロングテール日本語SEOキーワード記事データベース（検索上位を獲りやすい具体的悩みキーワード群）
SEO_TOPICS = [
    {
        "slug": "topic-apology-mail.html",
        "title": "ChatGPTで書いた謝罪メール・ビジネスお詫び文がバレる理由とAI見抜き方 | AI見抜きくん Pro",
        "h1": "「この謝罪メール、ChatGPT丸投げ？」ビジネスお詫び文のAI作成を3秒で見抜く方法",
        "desc": "取引先や部下から届いた謝罪メール・始末書・遅刻連絡がChatGPTで自動生成されたものか判定。AI特有の「第一に〜」「一方で〜」「総じて〜」構文と本人文体とのズレを検出します。",
        "kw": "謝罪メール ChatGPT バレる, ビジネスメール AI 判定, 始末書 AI 見分け方",
        "body": "ビジネスの現場で急増しているのが、ミスや遅延に対する謝罪メールをChatGPTに丸投げして作成するケースです。一見すると丁寧な敬語に見えますが、『主な要因としては以下の点が挙げられます』『今後は〜が不可欠であると考えております』といった抽象的なAI定型句が並び、当事者としての具体的な反省や現場感が欠如しているのが特徴です。『AI見抜きくん Pro』では、普段の本人メールと今回の謝罪文の文体指紋（句読点リズム・漢字比率）を比較し、AI代筆確率を秒速で算出します。",
    },
    {
        "slug": "topic-pairs-line.html",
        "title": "ペアーズ・with・タップルで「すぐLINE交換」を誘うAI業者・投資詐欺の見分け方 | AI見抜きくん Pro",
        "h1": "マッチングアプリで「普段アプリ見ないのでLINE交換しよう」と言われたら？AI業者＆詐欺診断",
        "desc": "ペアーズやタップル、withでマッチング直後にLINE誘導してくる業者の定型文とAI自動返信ボットを無料診断。ロマンス詐欺・暗号資産レクチャー勧誘の危険度を数値化します。",
        "kw": "ペアーズ すぐLINE交換 業者, マッチングアプリ 普段アプリ見ない, ロマンス詐欺 LINE 見分け方",
        "body": "マッチングアプリで3〜5通やり取りしただけで『普段あまりこのアプリを開かないので、LINEで話しませんか？』と誘導してくるアカウントの約8割は、業者またはAI自動応答ボットを用いた投資・ロマンス詐欺グループです。さらに近年はChatGPTを使って相手のプロフィールに合わせた自然な褒め言葉を自動生成するため、一見すると普通の利用者と見分けがつきません。『AI見抜きくん Pro』にメッセージ全文を貼り付けると、業者特有の誘導アルゴリズムとAI構文を即座に検知し、相手が人間かボットかを一発で試せる『カマかけ返信テンプレート』を出力します。",
    },
    {
        "slug": "topic-lancers-seo.html",
        "title": "クラウドワークス・ランサーズでWebライターのChatGPTコピペ納品を見抜く検収マニュアル | AI見抜きくん Pro",
        "h1": "外注Webライターの「ChatGPT丸投げ記事」を検収前に3秒で見破る方法と差し戻しテンプレ",
        "desc": "文字単価発注したSEO記事やブログ原稿がAI生成のコピペか判定。Word(.docx)の保存リビジョン回数1回検知と、普段のチャット文面との乖離グラフで確実な証拠を取得。",
        "kw": "クラウドワークス AI記事 検収, ランサーズ ライター ChatGPT 見分け方, Webライター AI コピペ 判定",
        "body": "クラウドソーシングで『AI使用禁止・一次情報必須』として発注しても、ChatGPTやClaudeで出力した文章をそのまま納品する悪質ライターが後を絶ちません。しかし感覚だけで『AIで書きましたよね？』と指摘するとトラブルに発展します。『AI見抜きくん Pro』は、①Wordファイルの編集保存回数（リビジョンが1回のみ＝コピペ貼り付けの証拠）、②チャットワークやメッセージ欄での本人文体と納品記事の漢字率・文長分散のズレ、③文単位のAI構文ハイライトを監査証明書PDFとして出力し、角を立てずに修正・差し戻しを求めるメッセージ文面を自動生成します。",
    },
    {
        "slug": "topic-gakuchika-es.html",
        "title": "就活ES（ガクチカ・自己PR・志望動機）のChatGPT作成率は人事に見抜かれる？AI判定ツール | AI見抜きくん Pro",
        "h1": "就活エントリーシート（ガクチカ・志望動機）のAI生成チェック＆面接深掘り質問ジェネレーター",
        "desc": "新卒採用・中途採用のエントリーシート（ES）がChatGPTで量産された文章か3秒で監査。人事が面接でAI代筆を見破るための深掘り質問テンプレートも自動生成。",
        "kw": "就活 ES ChatGPT バレる, ガクチカ AI 判定ツール, 志望動機 AI 見分け方 人事",
        "body": "就職活動のエントリーシート（ガクチカ・自己PR）において、ChatGPTが出力する文章には『課題が存在していました』『多岐にわたる〜』『この経験から〜の重要性を学びました』『再現性を持って貴社に貢献〜』といった特有の骨格があります。企業の採用担当者（人事）も、学生自身が応募前に自分のESが『AI量産型で無機質な文章になっていないか』をセルフチェックする用途でも『AI見抜きくん Pro』が活用されています。",
    },
    {
        "slug": "topic-univ-report.html",
        "title": "大学の課題レポート・卒論・読書感想文のAIコピペ判定！紙のスマホ撮影にも対応 | AI見抜きくん Pro",
        "h1": "大学レポート・課題論文のChatGPT代筆をスマホカメラ撮影＆PDF/Wordから即座に監査",
        "desc": "提出されたレポートや小論文の文長揺らぎ（Burstiness）と語尾の単調さからAI使用率を判定。過去の本人提出物との文体指紋比較で代筆を客観的に証明します。",
        "kw": "大学レポート ChatGPT バレる 仕組み, 課題 AI判定 ツール 無料, 読書感想文 AI チェッカー",
        "body": "大学や高校・社内研修のレポート課題において、人間が書いた文章は『短い強調文』と『長い説明文』が混ざり合う（高バースト性）のに対し、LLM（大規模言語モデル）が出力する文章は1文あたりの文字数が45〜65文字前後に均一化される統計的性質があります。『AI見抜きくん Pro』は日本語の助詞分布と文長変動係数（CV値）を解析し、さらに紙で提出されたレポートのスマホ撮影画像からのレイアウト検査にも対応しています。",
    },
    {
        "slug": "topic-mercari-fake.html",
        "title": "メルカリ・ヤフオク出品画像やSNS写真のAI生成・無断加工を見破るELAヒートマップ検査 | AI見抜きくん Pro",
        "h1": "その写真、本物の実写？AI生成画像や加工フェイクをブラウザ内で暴く画像フォレンジック",
        "desc": "Stable DiffusionやMidjourneyの隠しメタデータ署名検出、iPhone/AndroidカメラEXIF検査、およびELA（圧縮誤差ヒートマップ）でAI生成画像を3秒で見抜きます。",
        "kw": "AI生成画像 見分け方 サイト, メルカリ 写真 加工 判定, SNS アイコン AI 見抜く",
        "body": "画像生成AI（Stable Diffusion XL / Midjourney / Flux等）で生成された人物アイコンや商品画像は、パッと見では実写と区別がつきません。しかし画像ファイルのバイナリ内部には生成パラメータ（Steps / Sampler / CFG scale）のチャンクが残存していたり、iPhone等の光学カメラセンサー固有のEXIF情報や微細なセンサーノイズが欠落しています。『AI見抜きくん Pro』は画像を外部サーバーに送信することなく、ブラウザ内でELA（Error Level Analysis）ヒートマップを生成してAI特有の異常な平滑化領域を可視化します。",
    },
]


def build_all_topic_pages() -> None:
    links_html = "\n".join(
        f'<li><a href="{t["slug"]}" style="color:#38bdf8;">{t["h1"]}</a></li>'
        for t in SEO_TOPICS
    )

    for t in SEO_TOPICS:
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t["title"]}</title>
  <meta name="description" content="{t["desc"]}" />
  <meta name="keywords" content="{t["kw"]}" />
  <meta property="og:title" content="{t["title"]}" />
  <meta property="og:description" content="{t["desc"]}" />
  <meta property="og:image" content="{BASE_URL}/og-image.png" />
  <meta property="og:url" content="{BASE_URL}/{t["slug"]}" />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{BASE_URL}/og-image.png" />
  <link rel="canonical" href="{BASE_URL}/{t["slug"]}" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header class="app-header">
    <div class="header-inner">
      <a href="index.html" class="brand" style="text-decoration:none; color:inherit;">
        <div class="brand-icon">🔍</div>
        <div>
          <div class="brand-title">AI見抜きくん Pro <span class="brand-badge">公式ナレッジ＆無料監査</span></div>
          <div class="brand-sub">LINE・外注記事・レポート・画像のAI真贋チェッカー</div>
        </div>
      </a>
      <div style="display:flex; gap:0.5rem;">
        <a href="index.html" class="btn btn-primary btn-sm">🔍 無料診断ツールを開く</a>
        <a href="{NOTE_URL}" target="_blank" rel="noopener noreferrer" class="btn btn-gold btn-sm">🎫 7日間パス(¥980) ↗</a>
      </div>
    </div>
  </header>

  <main class="container" style="max-width: 900px;">
    <article class="card" style="padding: 2rem;">
      <div style="font-size: 0.78rem; color: #38bdf8; font-weight: 700; margin-bottom: 0.4rem;">
        🇯🇵 AI真贋フォレンジック専門ガイド
      </div>
      <h1 style="font-size: 1.5rem; line-height: 1.4; margin-bottom: 1rem;">{t["h1"]}</h1>
      <p style="font-size: 0.94rem; line-height: 1.85; color: var(--text-main); margin-bottom: 1.5rem;">
        {t["body"]}
      </p>

      <div style="text-align: center; padding: 1.5rem; background: var(--bg-input); border-radius: 12px; border: 1px solid var(--primary); margin-bottom: 1.8rem;">
        <div style="font-size: 1.08rem; font-weight: 800; margin-bottom: 0.45rem;">
          🛡️ 登録不要・サーバー保存ゼロ！今すぐ3秒で無料AI判定
        </div>
        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">
          1日3回まで無料でお試しいただけます。全センテンス根拠表示・確認返信テンプレ3選・監査証明書PDF出力は公式noteの「7日間徹底監査パス（¥980）」で即時解放されます。
        </p>
        <div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">
          <a href="index.html" class="btn btn-primary">🔍 今すぐ無料で文章・画像を判定する</a>
          <a href="{NOTE_URL}" target="_blank" rel="noopener noreferrer" class="btn btn-gold">📝 公式noteで徹底監査パス(¥980)を取得 ↗</a>
        </div>
      </div>

      <hr style="border: none; border-top: 1px solid var(--border-color); margin: 1.5rem 0;" />
      <h2 style="font-size: 1rem; margin-bottom: 0.6rem;">📚 関連するAI見抜き方・監査ガイド一覧</h2>
      <ul style="padding-left: 1.2rem; font-size: 0.85rem; line-height: 1.9;">
        {links_html}
        <li><a href="lp-matching.html" style="color:#38bdf8;">マッチングアプリ・LINEのAI業者＆ロマンス詐欺診断</a></li>
        <li><a href="lp-crowdworks.html" style="color:#38bdf8;">クラウドワークス外注記事のChatGPTコピペ＆Wordリビジョン監査</a></li>
        <li><a href="lp-report.html" style="color:#38bdf8;">大学レポート・就活ESのAI代筆チェッカー</a></li>
        <li><a href="lp-mercari.html" style="color:#38bdf8;">メルカリ出品画像・SNSアイコンのAI生成ヒートマップ解析</a></li>
      </ul>
    </article>
  </main>
</body>
</html>"""
        for folder in (STATIC_DIR, DOCS_DIR):
            if os.path.exists(folder):
                with open(os.path.join(folder, t["slug"]), "w", encoding="utf-8") as f:
                    f.write(html)

    # Sitemap 全11ページ更新
    today = datetime.now().strftime("%Y-%m-%d")
    all_pages = (
        ["", "lp-matching.html", "lp-crowdworks.html", "lp-report.html", "lp-mercari.html"]
        + [t["slug"] for t in SEO_TOPICS]
    )
    items = []
    for u in all_pages:
        loc = f"{BASE_URL}/{u}" if u else f"{BASE_URL}/"
        prio = "1.0" if not u else "0.85"
        items.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(items)
        + "\n</urlset>\n"
    )
    for folder in (STATIC_DIR, DOCS_DIR):
        if os.path.exists(folder):
            with open(os.path.join(folder, "sitemap.xml"), "w", encoding="utf-8") as f:
                f.write(sitemap_xml)

    print(f"Published {len(all_pages)} SEO pages and updated sitemap.xml!")


if __name__ == "__main__":
    build_all_topic_pages()
