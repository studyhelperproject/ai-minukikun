import json
import os
import shutil
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
BASE_URL = "https://studyhelperproject.github.io/ai-minukikun"
NOTE_URL = "https://note.com/safe_swift4998/n/na1af72c84723"

# ロングテール日本語SEOキーワード記事データベース（全20記事＋コアLP4記事＋トップ＝計25ページ体制）
SEO_TOPICS = [
    {
        "slug": "topic-apology-mail.html",
        "title": "ChatGPTで書いた謝罪メール・ビジネスお詫び文がバレる理由とAI見抜き方 | AI見抜きくん Pro",
        "h1": "「この謝罪メール、ChatGPT丸投げ？」ビジネスお詫び文のAI作成を3秒で見抜く方法",
        "desc": "取引先や部下から届いた謝罪メール・始末書・遅刻連絡がChatGPTで自動生成されたものか判定。AI特有の「第一に〜」「一方で〜」「総じて〜」構文と本人文体とのズレを検出します。",
        "kw": "謝罪メール ChatGPT バレる, ビジネスメール AI 判定, 始末書 AI 見分け方",
        "cta_tab": "stylometry",
        "sample_key": "stylometry_case",
        "body": "ビジネスの現場で急増しているのが、ミスや遅延に対する謝罪メールや始末書をChatGPTに丸投げして作成するケースです。一見すると丁寧な敬語に見えますが、『主な要因としては以下の点が挙げられます』『今後は再発防止策の徹底が不可欠であると考えております』といった抽象的なAI定型句が並び、当事者としての具体的な反省や現場感が欠如しているのが特徴です。『AI見抜きくん Pro』では、普段の本人メール・チャットと今回の謝罪文の文体指紋（句読点リズム・漢字比率）を比較し、AI代筆確率を秒速で算出します。",
        "checklist": [
            "普段のチャットでは句読点が少ないのに、謝罪メールだけ45〜55文字ごとに規則正しく読点（、）が打たれている",
            "「原因は以下の3点に集約されます」「総じて〜」など評論家のような第三者目線の表現が含まれている",
            "漢字含有率が32%〜38%と高く、感情を表す助詞や口語的なクッション言葉が完全に消えている"
        ],
        "faqs": [
            ("部下が提出した始末書がChatGPT製か確かめる方法はありますか？", "『AI見抜きくん Pro』の「本人文体との比較監査」タブに、普段のSlackやTeamsでの部下のメッセージと今回の始末書を貼り付けてください。漢字率と文長のズレから代筆確率を数値化できます。"),
            ("入力した社内メールが外部に漏洩しませんか？", "一切漏洩しません。すべてのテキスト解析はお使いのブラウザメモリ内のみで完結し、外部サーバーへの送信・保存はゼロです。")
        ]
    },
    {
        "slug": "topic-pairs-line.html",
        "title": "ペアーズ・with・タップルで「すぐLINE交換」を誘うAI業者・投資詐欺の見分け方 | AI見抜きくん Pro",
        "h1": "マッチングアプリで「普段アプリ見ないのでLINE交換しよう」と言われたら？AI業者＆詐欺診断",
        "desc": "ペアーズやタップル、withでマッチング直後にLINE誘導してくる業者の定型文とAI自動返信ボットを無料診断。ロマンス詐欺・暗号資産レクチャー勧誘の危険度を数値化します。",
        "kw": "ペアーズ すぐLINE交換 業者, マッチングアプリ 普段アプリ見ない, ロマンス詐欺 LINE 見分け方",
        "cta_tab": "messenger",
        "sample_key": "scam_dm",
        "body": "マッチングアプリで3〜5通やり取りしただけで『普段あまりこのアプリを開かないので、LINEで話しませんか？』『通知が来ないのでLINE交換しましょう』と誘導してくるアカウントの約8割は、業者またはAI自動応答ボットを用いた投資・ロマンス詐欺グループです。さらに近年はChatGPTを使って相手のプロフィールに合わせた自然な褒め言葉を自動生成するため、一見すると普通の利用者と見分けがつきません。『AI見抜きくん Pro』にメッセージ全文を貼り付けると、業者特有の誘導アルゴリズムとAI構文を即座に検知し、相手が人間かボットかを一発で試せる『カマかけ返信テンプレート』を出力します。",
        "checklist": [
            "マッチング後3通目以内に「普段アプリ見ない」「通知が来ない」を理由にLINE交換を急かす",
            "プロフィールの内容を過剰に褒めちぎるが、こちらの質問に対する回答が微妙にズレている",
            "会話の中に「叔父がアナリスト」「将来のための資産形成」「副業・配当」といった単語が混じる"
        ],
        "faqs": [
            ("相手がAIボットか人間かを一発で見分ける質問はありますか？", "『AI見抜きくん Pro』で診断すると、相手のAIスクリプトを混乱させてボロを出させる「カマかけ返信テンプレート」をワンクリックでコピーできます。"),
            ("顔写真がAI生成の架空人物か調べることもできますか？", "はい。「撮影レポート・メルカリ/SNS画像判定」タブに相手のプロフィール画像を読み込ませると、AI生成特有の平滑化ノイズやメタデータを検査できます。")
        ]
    },
    {
        "slug": "topic-lancers-seo.html",
        "title": "クラウドワークス・ランサーズでWebライターのChatGPTコピペ納品を見抜く検収マニュアル | AI見抜きくん Pro",
        "h1": "外注Webライターの「ChatGPT丸投げ記事」を検収前に3秒で見破る方法と差し戻しテンプレ",
        "desc": "文字単価発注したSEO記事やブログ原稿がAI生成のコピペか判定。Word(.docx)の保存リビジョン回数1回検知と、普段のチャット文面との乖離グラフで確実な証拠を取得。",
        "kw": "クラウドワークス AI記事 検収, ランサーズ ライター ChatGPT 見分け方, Webライター AI コピペ 判定",
        "cta_tab": "stylometry",
        "sample_key": "cw_article",
        "body": "クラウドソーシングで『AI使用禁止・一次情報必須』として発注しても、ChatGPTやClaudeで出力した文章をそのまま納品する悪質ライターが後を絶ちません。しかし感覚だけで『AIで書きましたよね？』と指摘するとトラブルに発展します。『AI見抜きくん Pro』は、①Wordファイルの編集保存回数（リビジョンが1回のみ＝コピペ貼り付けの証拠）、②チャットワークやメッセージ欄での本人文体と納品記事の漢字率・文長分散のズレ、③文単位のAI構文ハイライトを監査証明書PDFとして出力し、角を立てずに修正・差し戻しを求めるメッセージ文面を自動生成します。",
        "checklist": [
            "見出しの末尾やまとめ段落に「〜という点が挙げられます」「いかがでしたでしょうか」が頻出する",
            "普段の応募メッセージやチャット連絡は短文でひらがなが多いのに、納品記事だけ論文調で硬い",
            "納品されたWord（.docx）ファイルの内部編集リビジョンが1回〜2回しかない"
        ],
        "faqs": [
            ("ライターと揉めずに修正や契約解除を申し出るにはどうすればいいですか？", "感覚で指摘するのではなく、『AI見抜きくん Pro』が出力する客観的な一致スコアと「発注者用・角が立たない差し戻しテンプレート」をそのままコピーして送信してください。"),
            ("Wordファイルのまま検査できますか？", "はい。「Word / PDF レポート丸投げ監査」タブに .docx ファイルをドロップするだけで、内部リビジョン履歴と本文のAI構文を同時にスキャンします。")
        ]
    },
    {
        "slug": "topic-gakuchika-es.html",
        "title": "就活ES（ガクチカ・自己PR・志望動機）のChatGPT作成率は人事に見抜かれる？AI判定ツール | AI見抜きくん Pro",
        "h1": "就活エントリーシート（ガクチカ・志望動機）のAI生成チェック＆面接深掘り質問ジェネレーター",
        "desc": "新卒採用・中途採用のエントリーシート（ES）がChatGPTで量産された文章か3秒で監査。人事が面接でAI代筆を見破るための深掘り質問テンプレートも自動生成。",
        "kw": "就活 ES ChatGPT バレる, ガクチカ AI 判定ツール, 志望動機 AI 見分け方 人事",
        "cta_tab": "messenger",
        "sample_key": "ai_es",
        "body": "就職活動のエントリーシート（ガクチカ・自己PR）において、ChatGPTが出力する文章には『課題が存在していました』『多岐にわたる〜』『この経験から〜の重要性を学びました』『再現性を持って貴社に貢献〜』といった特有の骨格があります。企業の採用担当者（人事）による書類選考監査はもちろん、学生自身が応募前に自分のESが『AI量産型で無機質な文章になっていないか』をセルフチェックする用途でも『AI見抜きくん Pro』が活用されています。",
        "checklist": [
            "「当初〜という課題が存在していました」「まず第一に〜、第二に〜」というテンプレ構造になっている",
            "具体的な固有名詞や失敗時の泥臭いエピソードがなく、「オペレーションの最適化」「多岐にわたる」等の抽象語が多い",
            "結びの一文が「再現性を持って貴社の事業成長に貢献したいと考えております」で終わっている"
        ],
        "faqs": [
            ("就活生ですが、ES提出前にAIっぽさを消すために使えますか？", "はい！自分のESを貼り付けてAI疑惑スコアが高い文（赤色ハイライト箇所）を自分の体験談・話し言葉に近い表現へ書き直すことで、人事の目を惹く通過率の高いESに仕上げられます。"),
            ("採用担当者ですが、面接で本人が書いたか確かめる質問は出ますか？", "はい。診断結果画面に「口頭試問でAI代筆を見破る深掘り質問テンプレート」が自動出力されます。")
        ]
    },
    {
        "slug": "topic-univ-report.html",
        "title": "大学の課題レポート・卒論・読書感想文のAIコピペ判定！紙のスマホ撮影にも対応 | AI見抜きくん Pro",
        "h1": "大学レポート・課題論文のChatGPT代筆をスマホカメラ撮影＆PDF/Wordから即座に監査",
        "desc": "提出されたレポートや小論文の文長揺らぎ（Burstiness）と語尾の単調さからAI使用率を判定。過去の本人提出物との文体指紋比較で代筆を客観的に証明します。",
        "kw": "大学レポート ChatGPT バレる 仕組み, 課題 AI判定 ツール 無料, 読書感想文 AI チェッカー",
        "cta_tab": "document",
        "sample_key": "cw_article",
        "body": "大学や高校・社内研修のレポート課題において、人間が書いた文章は『短い強調文』と『長い説明文』が混ざり合う（高バースト性）のに対し、LLM（大規模言語モデル）が出力する文章は1文あたりの文字数が45〜65文字前後に均一化される統計的性質があります。『AI見抜きくん Pro』は日本語の助詞分布と文長変動係数（CV値）を解析し、さらに紙で提出されたレポートのスマホ撮影画像からの検査やWord/PDFの直接監査にも対応しています。",
        "checklist": [
            "文長変動係数（CV値）が 0.35 未満で、すべての文の長さが揃いすぎている",
            "講義内で扱っていない専門用語や、一般的な教科書的要約が唐突に並んでいる",
            "過去のミニッツペーパー（手書き感想）と今回のレポートで漢字含有率が10%以上乖離している"
        ],
        "faqs": [
            ("なぜ大学の先生にChatGPTで書いたレポートがバレるのですか？", "普段の出席カードや小テストの記述と、提出レポートの「漢字比率」「読点の位置」「接続詞のクセ」が統計的にまったく異なるため、文体比較を行うと一目で乖離が検出されるからです。"),
            ("監査結果をPDFで保存して記録に残せますか？", "はい。Proパス（¥980）をアンロックすると、監査証明書ID付きのPDFレポートをワンクリックで印刷・保存できます。")
        ]
    },
    {
        "slug": "topic-mercari-fake.html",
        "title": "メルカリ・ヤフオク出品画像やSNS写真のAI生成・無断加工を見破るELAヒートマップ検査 | AI見抜きくん Pro",
        "h1": "その写真、本物の実写？AI生成画像や加工フェイクをブラウザ内で暴く画像フォレンジック",
        "desc": "Stable DiffusionやMidjourneyの隠しメタデータ署名検出、iPhone/AndroidカメラEXIF検査、およびELA（圧縮誤差ヒートマップ）でAI生成画像を3秒で見抜きます。",
        "kw": "AI生成画像 見分け方 サイト, メルカリ 写真 加工 判定, SNS アイコン AI 見抜く",
        "cta_tab": "photo_report",
        "sample_key": "scam_dm",
        "body": "画像生成AI（Stable Diffusion XL / Midjourney / Flux等）で生成された人物アイコンや商品画像は、パッと見では実写と区別がつきません。しかし画像ファイルのバイナリ内部には生成パラメータ（Steps / Sampler / CFG scale）のチャンクが残存していたり、iPhone等の光学カメラセンサー固有のEXIF情報や微細なセンサーノイズが欠落しています。『AI見抜きくん Pro』は画像を外部サーバーに送信することなく、ブラウザ内でELA（Error Level Analysis）ヒートマップを生成してAI特有の異常な平滑化領域を可視化します。",
        "checklist": [
            "画像解像度が 1024×1024px や 512×512px など生成AIの標準出力サイズと完全一致している",
            "スマホで撮影したはずなのに、iPhone / Galaxy 等のカメラEXIFタグが完全に欠落している",
            "ELAヒートマップで見ると、背景と人物の境界や肌の表面に不自然な平滑化ブロックがある"
        ],
        "faqs": [
            ("調べたい画像をアップロードするとサーバーに保存されますか？", "いいえ。画像はHTML5 CanvasとWeb標準APIを用いてお使いのスマホ・PCのブラウザ内だけで解析されるため、外部サーバーには1バイトも送信されません。"),
            ("スクリーンショットした画像でも判定できますか？", "はい。メタデータが消去された画像でも、ピクセル表面の圧縮誤差分散（ELAヒートマップ）から合成やAI平滑化の痕跡を検査できます。")
        ]
    },
    {
        "slug": "topic-daily-report.html",
        "title": "社内日報・週報・研修感想文のChatGPTコピペ丸投げを見抜く方法 | AI見抜きくん Pro",
        "h1": "新入社員・部下の「日報・週報・研修レポート」がChatGPT丸投げか3秒で判定する監査ツール",
        "desc": "毎日の業務日報や社内研修の振り返りシートがAIによる自動生成かチェック。普段のチャット文面との文体乖離から、中身のないAI作文を即座に検出します。",
        "kw": "日報 ChatGPT バレる, 社内研修 レポート AI 見分け方, 週報 AI判定 ツール",
        "cta_tab": "stylometry",
        "sample_key": "stylometry_case",
        "body": "リモートワークや新入社員研修で提出される「日報・週報・振り返りレポート」をChatGPTで自動生成して提出するケースが急増しています。『本日の業務を通じて〜の重要性を再認識しました』『今後はチーム連携を強化し生産性向上に努めます』といった綺麗事ばかりが並び、実際の業務課題が見えなくなるリスクがあります。『AI見抜きくん Pro』で普段のチャット文面と比較すれば、AI丸投げ度合いを客観的に把握し、具体的な1on1フィードバックに活用できます。",
        "checklist": [
            "具体的な数値や固有名詞（顧客名・案件名）がなく、抽象的なビジネス用語だけで構成されている",
            "毎日提出される日報の文末表現や文字数が不自然なほど均一である",
            "チャットでの質問文と、日報の文章で漢字含有率が10%以上異なる"
        ],
        "faqs": [
            ("社外秘が含まれる業務日報を入力してもセキュリティ上問題ありませんか？", "はい、完全ゼロトラスト設計（ブラウザ内メモリ完結・外部通信なし）のため、社外秘テキストも情報漏洩リスクゼロで安全に検査できます。"),
            ("部下に角を立てずに指導するテンプレートはありますか？", "はい、診断結果に口頭確認・フィードバック用の質問テンプレートが付属しています。")
        ]
    },
    {
        "slug": "topic-sns-romance.html",
        "title": "Instagram・X（旧Twitter）の外国人・投資家DMはAIロマンス詐欺？見分け方と無料診断 | AI見抜きくん Pro",
        "h1": "インスタやXのDMで届く「翻訳調・AI自動生成のロマンス詐欺＆投資勧誘」を3秒で見破る",
        "desc": "SNSのDMで突然話しかけてくる親日家アカウントや投資家アカウントのメッセージが、ChatGPT翻訳・詐欺スクリプトか無料診断します。",
        "kw": "インスタ DM ロマンス詐欺 見分け方, X 投資詐欺 AI判定, 国際ロマンス詐欺 LINE 特徴",
        "cta_tab": "messenger",
        "sample_key": "scam_dm",
        "body": "InstagramやX（旧Twitter）、ThreadsのDMで『あなたの投稿が素敵で連絡しました』『日本の文化が大好きです』と話しかけ、最終的にLINEへ誘導して金銭や暗号資産を騙し取る国際ロマンス詐欺・SNS型投資詐欺は、現在ほぼすべて生成AI（ChatGPT等の自動応答スクリプト）で自動化されています。『AI見抜きくん Pro』は不自然な褒め言葉のアルゴリズムやLINE誘導トリガーを瞬時に検出し、詐欺被害を未然に防ぎます。",
        "checklist": [
            "「あなたの笑顔やライフスタイルに感銘を受けました」などAI翻訳特有の過剰な賛辞がある",
            "数通やり取りしただけで「普段インスタはあまり見ないのでLINEを追加してください」と誘導される",
            "金相場・FX・暗号資産・AI自動売買や「叔父・師匠」の話題が出始める"
        ],
        "faqs": [
            ("相手が本物の人間かAIボットか確かめる方法はありますか？", "『AI見抜きくん Pro』で生成される「カマかけ質問テンプレート」を送ってみてください。AIスクリプトや中華系詐欺業者は文脈を無視した定型返信を返すため一発で見抜けます。"),
            ("無料で何回まで診断できますか？", "会員登録不要で1日3回まで無料でお試しいただけます。")
        ]
    },
    {
        "slug": "topic-google-review.html",
        "title": "Googleマップ口コミ・AmazonサクラレビューのAI自動生成を見抜く方法 | AI見抜きくん Pro",
        "h1": "Googleマップの星5口コミや通販レビューは本物？AIサクラ投稿を3秒で真贋判定",
        "desc": "店舗のGoogleビジネスプロフィール（MEO）やECサイトのレビューが、ChatGPTで量産されたサクラ口コミか嫌がらせ投稿かを統計解析します。",
        "kw": "Google口コミ サクラ 見分け方, Amazonレビュー AI判定, ステマ 口コミ チェッカー",
        "cta_tab": "messenger",
        "sample_key": "cw_article",
        "body": "Googleマップの口コミや通販サイトのレビューにおいて、生成AIを使って大量生産された「サクラ高評価レビュー」や、競合他社による「AI生成の悪評（ネガティブキャンペーン）」が問題視されています。AIが生成した口コミには、実際の体験者なら書くはずの微細な情景描写がなく、文長と漢字比率が一定のレンジに収束する特徴があります。『AI見抜きくん Pro』で口コミテキストをスキャンし、サクラ・AI生成確率を数値化しましょう。",
        "checklist": [
            "「スタッフの対応が丁寧で、全体的に満足度の高いサービスでした」など具体性のない総括表現が多い",
            "複数の口コミを並べたとき、文の長さ（45〜60文字）と句読点の位置が酷似している",
            "「まず〜、また〜、総じて〜」など接続詞の使い方が解説記事のようになっている"
        ],
        "faqs": [
            ("複数の怪しい口コミをまとめて比較できますか？", "はい、「本人文体との比較監査」タブに2つの口コミを入力すれば、同一人物（または同一AIプロンプト）による投稿かどうかの文体一致度を計測できます。"),
            ("スマートフォンのブラウザからでも使えますか？", "はい、iPhone・Android・PCすべてでアプリインストール不要でそのまま動作します。")
        ]
    },
    {
        "slug": "topic-book-review.html",
        "title": "読書感想文・夏休み宿題・小論文のChatGPT代筆が見破られる理由とAIチェッカー | AI見抜きくん Pro",
        "h1": "読書感想文や小論文の「ChatGPT丸投げ」はなぜ先生にバレる？文体リズム無料診断",
        "desc": "中高生・大学生の読書感想文や作文コンクール応募作が生成AIで書かれたものか判定。学年不相応な語彙やAI特有の要約構文をハイライト表示します。",
        "kw": "読書感想文 ChatGPT バレる, 夏休み 宿題 AI判定, 小論文 AI 見分け方 先生",
        "cta_tab": "messenger",
        "sample_key": "ai_es",
        "body": "読書感想文や小論文の宿題をChatGPTに出力させると、『本書の主人公の行動から〜の大切さを学びました』『現代社会においても重要なテーマであると言えます』といった大人びた評論調の文章になります。学校教員が読めば、普段の生徒の語彙力や文末リズムとのギャップから即座に違和感を覚えます。『AI見抜きくん Pro』ではどの文がAI特有の構文かを1文ずつ色分け表示し、自然な自分の言葉に直すためのチェックにも活用できます。",
        "checklist": [
            "本のあらすじ要約と一般的な道徳的教訓ばかりで、自分の実体験との具体的な結びつきが薄い",
            "「〜という点が印象に残りました」「〜について深く考えさせられました」が繰り返される",
            "1文あたりの文字数のバラつきが少なく、大人向けの漢字含有率（30%超）になっている"
        ],
        "faqs": [
            ("保護者が子どもの作文をチェックするのに使えますか？", "はい。お子様が書いた下書きがAI丸写しになっていないか、どの部分を自分の体験談に書き換えるべきかを視覚的にアドバイスできます。"),
            ("紙に手書きされた作文でもチェックできますか？", "はい、スマホカメラで撮影して画像判定タブからスキャン可能です。")
        ]
    },
    {
        "slug": "topic-note-brain.html",
        "title": "note・Brain・Tipsの有料情報商材やブログ記事がAI量産コピペか見抜く方法 | AI見抜きくん Pro",
        "h1": "そのnote記事や副業ブログ、ChatGPTのコピペ量産？AI生成率を3秒で暴く無料チェッカー",
        "desc": "SNSで宣伝されているnote記事やブログの無料導入部分をコピペしてAI生成率を判定。中身のないAI量産記事を購入する前に真贋を見極められます。",
        "kw": "note AI記事 見分け方, ブログ ChatGPT 判定, 情報商材 AI コピペ 見抜く",
        "cta_tab": "messenger",
        "sample_key": "cw_article",
        "body": "近年、ChatGPTに目次と本文を丸投げして1日数十本も量産された『中身のないnote記事・トレンドブログ』が溢れています。無料公開されている導入部分のテキストを『AI見抜きくん Pro』に貼り付けてスキャンすれば、著者が自分の一次体験に基づいて執筆した本物の記事か、AIが出力しただけの薄っぺらい要約記事かを3秒で判別できます。",
        "checklist": [
            "導入文が「現代において〜はますます重要性を増しています」といった一般論から始まる",
            "箇条書きの前後が「以下の点が挙げられます」「それぞれ詳しく見ていきましょう」で固定されている",
            "著者自身の具体的な失敗談や生データ（一次情報）が一切含まれていない"
        ],
        "faqs": [
            ("自分が執筆したnoteやブログ記事が「AIっぽい」と読者に思われないかセルフチェックできますか？", "はい！公開前に『AI見抜きくん Pro』にかけることで、無意識に使っているAIっぽい硬い表現を検出し、人間味のある読みやすい記事に推敲できます。"),
            ("文字数制限はありますか？", "ブラウザ内エンジンのため、長文のブログ記事（1万文字以上）でも1秒以内に高速判定できます。")
        ]
    },
    {
        "slug": "topic-fukugyou-scam.html",
        "title": "LINE副業勧誘・「スタンプ送るだけ」「スクショで日給3万円」のAI詐欺ボット判定 | AI見抜きくん Pro",
        "h1": "「スマホで簡単・タスク副業」のLINE誘導メッセージはAI詐欺！危険度を3秒で無料診断",
        "desc": "SNS広告やショート動画から誘導されるLINE副業アカウントのメッセージを解析。タスク詐欺・PayPay送金詐欺の定型スクリプトを即座に検出します。",
        "kw": "LINE 副業詐欺 見分け方, タスク副業 スクショ 詐欺, AI自動返信 詐欺 判定",
        "cta_tab": "messenger",
        "sample_key": "scam_dm",
        "body": "「動画を見てスクショを送るだけで報酬」「スタンプを送るだけで日給1万円」といった謳い文句で公式LINEやTelegramへ誘導する副業詐欺は、AI自動応答ボットと海外詐欺グループのマニュアルで運用されています。最初は数百円のPayPay等を実際に振り込んで信用させ、後から高額な違約金や振り込みを要求するのが手口です。怪しいLINEメッセージが届いたら、返信する前に『AI見抜きくん Pro』で詐欺警戒スコアを診断してください。",
        "checklist": [
            "「専属メンター」「担当講師」「福利厚生タスク」といった不自然な日本語表現が使われている",
            "最初は少額の報酬がもらえると言いながら、途中から専用アプリや外部チャット（Telegram等）へ誘導される",
            "こちらの質問に対して1秒〜数秒で長文の定型マニュアルが自動返信されてくる"
        ],
        "faqs": [
            ("詐欺警戒度が高いと出た場合はどうすればいいですか？", "絶対に個人情報や銀行口座・PayPay IDを伝えず、即座にブロック・通報してください。"),
            ("家族や友人に危険性を知らせることはできますか？", "診断結果画面の「LINEで共有」または「監査証明書PDF保存」から、客観的な危険度スコアをそのまま共有できます。")
        ]
    },
    {
        "slug": "topic-konkatsu-profile.html",
        "title": "結婚相談所・婚活アプリのプロフィール自己紹介文がChatGPT作成か見分ける方法 | AI見抜きくん Pro",
        "h1": "婚活アプリのプロフィール文や初回メッセージ、「ChatGPT代筆」を見抜く相性＆真贋チェック",
        "desc": "マッチングアプリや結婚相談所の自己PR文・メッセージがAI作成か判定。プロフィール文と実際のLINEメッセージの文体ギャップから本気度を診断します。",
        "kw": "婚活 プロフィール ChatGPT 見分け方, マッチングアプリ 自己紹介 AI判定, ペアーズ プロフィール AI",
        "cta_tab": "stylometry",
        "sample_key": "stylometry_case",
        "body": "マッチングアプリや婚活サイトで、自己紹介文は驚くほど知的で誠実な長文なのに、いざマッチングしてメッセージを始めると極端に短文だったり言葉遣いが荒かったりするケースがあります。これはプロフィール文だけをChatGPTや代筆業者に書かせている典型例です。『AI見抜きくん Pro』の文体比較機能を使えば、プロフィール文と実際のメッセージの「本人一致度」を数値化できます。",
        "checklist": [
            "プロフィール文には丁寧な敬語と漢字が使われているのに、メッセージでは句読点すら打たない",
            "「周囲からはよく穏やかで誠実だと言われます」などテンプレ通りの自己PRが並んでいる",
            "メッセージのやり取りの中で、自分のプロフィールに書いてある趣味の内容を把握していない"
        ],
        "faqs": [
            ("プロフィール文とメッセージの2つを比較するにはどうすればいいですか？", "「本人文体との比較（代筆・なりすまし検知）」タブを選び、【A】にプロフィール文、【B】に届いたメッセージを入力して監査ボタンを押してください。"),
            ("自分の婚活プロフィールが不自然にAIっぽくないか確認できますか？", "はい、ご自身のプロフィール文を入力して、自然で親しみやすい文章になっているかセルフチェックするのにも最適です。")
        ]
    },
    {
        "slug": "topic-x-impress-zombie.html",
        "title": "X（旧Twitter）のインプレゾンビ・AI自動リプライボットを見分ける方法 | AI見抜きくん Pro",
        "h1": "X（旧Twitter）のリプライや引用RPが「AIボット・インプレゾンビ」か3秒で判定するツール",
        "desc": "バズった投稿に群がる不自然な日本語リプライや、巧妙化したChatGPT自動運用アカウントのポストを統計解析し、AIボット確率を算出します。",
        "kw": "X インプレゾンビ 見分け方, Twitter AIボット 判定, SNS 自動投稿 見抜く",
        "cta_tab": "messenger",
        "sample_key": "cw_article",
        "body": "X（旧Twitter）では収益化プログラムを悪用したインプレゾンビだけでなく、フォロワー稼ぎやアフィリエイト誘導のためにChatGPT APIで全自動運用されている「AIなりすましアカウント」が急増しています。元のポストを要約しただけの共感リプライや、「〜という視点は非常に重要ですね」といったAI構文を『AI見抜きくん Pro』でスキャンし、人間かボットかを即座に見分けましょう。",
        "checklist": [
            "元の投稿の言葉をそのままオウム返しして「本当にその通りですね！」「考えさせられます」と結んでいる",
            "プロフィールのアイコン画像がAI生成美女または無断転載で、過去の投稿の文体がすべて均一",
            "「結論から言うと〜」「有益な情報を共有します」など情報商材ボット特有の構文が多い"
        ],
        "faqs": [
            ("怪しいアカウントの複数ポストをまとめて判定できますか？", "はい、直近の3〜5ポストをコピーしてそのまま貼り付けると、文長の均一性からAI自動生成ボットかどうかをより高精度に判定できます。"),
            ("診断結果をXにシェアできますか？", "はい、結果画面の「𝕏 診断結果をポスト」ボタンからワンクリックでスコアを共有できます。")
        ]
    },
    {
        "slug": "topic-youtube-script.html",
        "title": "YouTube台本・TikTokショート動画シナリオの外注AIコピペ納品を見抜く検収法 | AI見抜きくん Pro",
        "h1": "外注したYouTubeゆっくり解説・ショート動画台本の「ChatGPT丸投げ」を3秒で見破る",
        "desc": "クラウドワークス等で発注したYouTube動画シナリオがAI出力のコピペか監査。視聴維持率を下げる単調なAI構文を検出し、差し戻し文面を作成します。",
        "kw": "YouTube台本 外注 AI 見分け方, ゆっくり解説 台本 ChatGPT 判定, シナリオライター AI 検収",
        "cta_tab": "stylometry",
        "sample_key": "cw_article",
        "body": "YouTubeチャンネル運営者がシナリオライターに台本を外注した際、ChatGPTで出力しただけの平板なテキストを納品されると、視聴維持率が大幅に低下しチャンネル評価に悪影響を及ぼします。AIが書いた台本には「フック（引き）の弱さ」「説明調の連続」「均一すぎるセリフ長」という特徴があります。『AI見抜きくん Pro』で納品台本をスキャンし、AI丸投げを検収段階でブロックしましょう。",
        "checklist": [
            "冒頭のつかみ（フック）がなく、「今回は〜について解説していきます」という平板な導入になっている",
            "登場人物の掛け合い（AとBの会話）なのに、両方のセリフの漢字比率と文の長さがまったく同じ",
            "終盤が「いかがでしたでしょうか。チャンネル登録と高評価をお願いします」のテンプレで終わる"
        ],
        "faqs": [
            ("テキストファイル（.txt）やWord（.docx）の台本をそのまま読み込めますか？", "はい、「Word / PDF レポート丸投げ監査」タブからファイルを直接選択して監査できます。"),
            ("ライターへ修正を依頼する角の立たない文面は作れますか？", "はい、発注者向けの検収差し戻しテンプレートが診断結果に自動生成されます。")
        ]
    },
    {
        "slug": "topic-realestate-mail.html",
        "title": "不動産・転職エージェント・保険営業メールがAI自動送信か本気か見分ける方法 | AI見抜きくん Pro",
        "h1": "転職スカウトや不動産営業メール、「あなただけに送っています」は本当？AI一斉送信チェッカー",
        "desc": "ビズリーチ等の転職プラチナスカウトや不動産営業メールが、AIによる自動生成テンプレか担当者が実際に履歴書を読んで書いた文面か3秒で判定します。",
        "kw": "転職スカウト AI 見分け方, プラチナスカウト テンプレ 判定, 営業メール ChatGPT 見抜く",
        "cta_tab": "messenger",
        "sample_key": "ai_es",
        "body": "転職サイトの「プラチナスカウト」や営業メールで、『ご経歴を拝見し、ぜひお話ししたくご連絡いたしました』と書かれていても、実際はレジュメのキーワードをAIに読み込ませて自動生成した一斉送信メールであるケースが増えています。『AI見抜きくん Pro』にスカウト文面を貼り付けると、AI特有の定型賛辞と文長リズムを解析し、担当者が本当に自分の手で書いた熱意あるメッセージかどうかを判定できます。",
        "checklist": [
            "職務経歴書のキーワードを1〜2個抜き出しただけで、「多岐にわたるご活躍」「高い専門性」と抽象的に褒めている",
            "なぜ自社のそのポジションにマッチするのかという具体的な接続がAI構文（まず第一に〜等）になっている",
            "文全体の漢字含有率が35%前後で、人間特有の温度感や個別質問が含まれていない"
        ],
        "faqs": [
            ("複数のエージェントから届いたスカウト文を比較できますか？", "はい、それぞれのスカウト文をスキャンしてAI疑惑スコアが低い（＝担当者が直接書いた可能性が高い）企業を優先して面談するといった使い方が可能です。"),
            ("スマホからコピペして使えますか？", "はい、スマホブラウザで3秒で判定結果が出ます。")
        ]
    },
    {
        "slug": "topic-counseling-reply.html",
        "title": "悩み相談・占いアプリ・チャット相談の返信がAI自動生成か見分ける方法 | AI見抜きくん Pro",
        "h1": "チャット占い・悩み相談の鑑定結果、「実はChatGPTのコピペ？」AI代筆を3秒で真贋判定",
        "desc": "文字単価やポイント課金のチャット占い・オンライン相談で届いた長文鑑定メッセージが、AIで自動生成されたテンプレ文章か診断します。",
        "kw": "チャット占い AI 見分け方, 占い 鑑定結果 ChatGPT 判定, 悩み相談 AIボット 見抜く",
        "cta_tab": "messenger",
        "sample_key": "scam_dm",
        "body": "有料のチャット占いやオンラインカウンセリング、ココナラ等の相談サービスにおいて、相談者のメッセージをそのままChatGPTに入力し、出力された当たり障りのない長文アドバイスをコピペ返信する悪質な出品者が問題になっています。『AI見抜きくん Pro』は、AIカウンセリング特有の共感構文（「お辛い状況ですね」「まずはご自身を労わることが大切です」等の均一な並び）を検出し、AI代筆確率を可視化します。",
        "checklist": [
            "長文なのに質問の核心には触れず、「可能性を秘めています」「焦らず一歩ずつ進むことが大切です」など誰にでも当てはまる表現ばかり",
            "メッセージ送信からわずか数十秒で500文字以上の整った長文が返ってくる",
            "前回の相談時のメッセージと今回の長文鑑定で、句読点の打ち方や漢字率がまったく違う"
        ],
        "faqs": [
            ("前回の短いメッセージと今回の鑑定文を比較できますか？", "はい、「本人文体との比較」タブを使えば、普段のチャットと長文鑑定文の文体乖離度をパーセントで表示できます。"),
            ("相談内容が外部に漏れる心配はありませんか？", "端末内（ブラウザメモリ内）だけで処理されるため、プライベートな相談内容が外部サーバーに送信・保存されることは一切ありません。")
        ]
    },
    {
        "slug": "topic-press-release.html",
        "title": "外注したプレスリリース・導入事例インタビュー記事のAI手抜き執筆を見抜く監査 | AI見抜きくん Pro",
        "h1": "広報・PR記事やインタビュー原稿の「AI要約丸投げ」を検収前に見破る品質管理ツール",
        "desc": "制作会社やライターに発注した導入事例・インタビュー記事が、文字起こしをChatGPTに丸投げしただけの原稿か文体・バースト性から判定します。",
        "kw": "インタビュー記事 AI 見分け方, プレスリリース ChatGPT 判定, 記事制作 検収 AIチェック",
        "cta_tab": "stylometry",
        "sample_key": "cw_article",
        "body": "インタビュー音源の文字起こしデータをそのままChatGPTに投げて『記事風にまとめて』と指示しただけの原稿は、話し手の熱量や独自の言い回しがすべて削ぎ落とされ、無機質な優等生文体になります。『AI見抜きくん Pro』は文長の揺らぎ（Burstiness）と語尾の単調さを数値化し、人間の編集者がしっかり推敲した原稿か、AI出力のコピペかを高精度に監査します。",
        "checklist": [
            "インタビュイー（語り手）の口癖や感情表現が消え、全員が同じような評論家調で話している",
            "各段落の最後が「〜と考えております」「〜が重要になります」の繰り返しで単調",
            "納品されたWordファイルの編集リビジョン回数が極端に少ない"
        ],
        "faqs": [
            ("社内稟議や制作会社へのフィードバック資料として結果を出力できますか？", "はい、Proパス機能で「監査証明書PDF」を出力し、客観的な品質スコアとして提示できます。"),
            ("法人チームで利用することは可能ですか？", "はい、7日間パス（¥980）のほか、Pro月額・法人パックにも対応しております。")
        ]
    },
    {
        "slug": "topic-translation-natural.html",
        "title": "DeepL・ChatGPT翻訳の不自然な日本語とAI直訳調を見抜く文体チェッカー | AI見抜きくん Pro",
        "h1": "その日本語ドキュメント、AI直訳・ChatGPT生成で不自然になっていない？自然度＆AI率診断",
        "desc": "外注した翻訳原稿やローカライズ記事が、AI翻訳のコピペ放置か人間がネイティブチェックした自然な日本語かを3秒で判定します。",
        "kw": "AI翻訳 見分け方, ChatGPT 翻訳 不自然 判定, 翻訳 外注 コピペ チェック",
        "cta_tab": "messenger",
        "sample_key": "cw_article",
        "body": "英語記事や海外資料をChatGPTやDeepLで翻訳させただけの文章は、文法としては正しくても『それは〜することを可能にします』『〜において重要な役割を果たします』といった欧米語由来の構文と均一な文長が残り、日本人読者に強い違和感を与えます。『AI見抜きくん Pro』は日本語特有の助詞バランスと文長リズムからAI直訳・生成度をスコア化し、不自然なセンテンスをピンポイントでハイライトします。",
        "checklist": [
            "主語に「それは」「これらは」が多用され、受動態（〜される）や使役表現が不自然に多い",
            "1文あたりの文字数が50文字前後に揃いすぎており、日本語らしいリズムの緩急がない",
            "「まず第一に」「結論として」などの接続詞が機械的に配置されている"
        ],
        "faqs": [
            ("翻訳ライターへの修正指示に使えますか？", "はい、AI疑惑スコアが高い文（赤色・黄色ハイライト箇所）を特定し、自然な日本語へリライトするよう具体的に指示できます。"),
            ("登録やインストールは必要ですか？", "不要です。Webブラウザ上で今すぐ無料で診断を開始できます。")
        ]
    },
    {
        "slug": "topic-scholarship-essay.html",
        "title": "奨学金申請書・推薦入試の志望理由書・昇格論文のChatGPT代筆チェック | AI見抜きくん Pro",
        "h1": "推薦入試の志望理由書・奨学金エッセイ・社内昇格論文のAI生成率を提出前にセルフ監査",
        "desc": "総合型選抜（旧AO入試）の志望理由書や奨学金エッセイ、社内の昇格試験論文がAI作成と疑われないか3秒でチェックします。",
        "kw": "志望理由書 ChatGPT バレる, 総合型選抜 AI判定, 昇格論文 AI 見分け方",
        "cta_tab": "messenger",
        "sample_key": "ai_es",
        "body": "大学推薦入試（総合型選抜）の志望理由書や奨学金申請エッセイ、企業の昇格試験論文では、審査員が『本人の言葉で書かれているか』『AIのテンプレ文章ではないか』を厳しくチェックしています。仮に自分で書いた文章であっても、構成を整えすぎるとAI判定ツールで高スコアが出てしまうことがあります。提出前に『AI見抜きくん Pro』でセルフ監査を行い、AI疑惑箇所を自分の具体的なエピソードへブラッシュアップしましょう。",
        "checklist": [
            "「貴学の理念に共感し」「多角的な視点から〜を探究したい」など誰でも書ける抽象表現が中心になっている",
            "面接官から「この一文はどういう実体験から書いたの？」と突っ込まれたときに即答できない箇所がある",
            "普段の小論文や面接カードと文体（漢字率・平均文長）が大きくかけ離れている"
        ],
        "faqs": [
            ("提出前に自分の論文をチェックしても、データがネット上に残ったりしませんか？", "絶対に残りません。当ツールはサーバーにテキストを一切送信・保存しない端末内完結型（ゼロトラスト設計）ですので、未発表の論文や志望理由書も100%安全に検査できます。"),
            ("面接対策の想定質問も確認できますか？", "はい、診断結果に「口頭試問・面接での深掘り確認質問テンプレート」が表示されます。")
        ]
    },
]


def build_all_topic_pages() -> None:
    links_html = "\n".join(
        f'<li><a href="{t["slug"]}" style="color:#38bdf8;">{t["h1"]}</a></li>'
        for t in SEO_TOPICS
    )

    for t in SEO_TOPICS:
        checklist_items = "\n".join(
            f'<li style="margin-bottom:0.45rem;">✅ {item}</li>' for item in t.get("checklist", [])
        )
        faq_items_html = "\n".join(
            f"""<div style="margin-bottom:0.85rem; padding:0.85rem; background:rgba(15,23,42,0.6); border-radius:8px; border:1px solid var(--border-color);">
              <div style="font-weight:700; color:#38bdf8; margin-bottom:0.3rem;">Q. {q}</div>
              <div style="font-size:0.86rem; color:var(--text-main); line-height:1.7;">A. {a}</div>
            </div>"""
            for q, a in t.get("faqs", [])
        )

        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in t.get("faqs", [])
            ],
        }
        faq_json_ld = json.dumps(faq_schema, ensure_ascii=False)
        cta_query = f"?tab={t.get('cta_tab', 'messenger')}&sample={t.get('sample_key', 'scam_dm')}"

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
  <script type="application/ld+json">{faq_json_ld}</script>
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
      <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
        <a href="index.html{cta_query}" class="btn btn-primary btn-sm">🔍 サンプル読込済で今すぐ無料診断</a>
        <a href="{NOTE_URL}" target="_blank" rel="noopener noreferrer" class="btn btn-gold btn-sm">🎫 7日間パス(¥980) ↗</a>
      </div>
    </div>
  </header>

  <main class="container" style="max-width: 920px;">
    <article class="card" style="padding: 2rem;">
      <div style="font-size: 0.78rem; color: #38bdf8; font-weight: 700; margin-bottom: 0.4rem;">
        🇯🇵 AI真贋フォレンジック専門ガイド（サーバー保存ゼロ・端末内完結）
      </div>
      <h1 style="font-size: 1.5rem; line-height: 1.4; margin-bottom: 1rem;">{t["h1"]}</h1>
      <p style="font-size: 0.94rem; line-height: 1.85; color: var(--text-main); margin-bottom: 1.4rem;">
        {t["body"]}
      </p>

      <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.02rem; color: #f87171; margin-bottom: 0.6rem;">⚠️ こんな特徴があればAI生成・代筆・業者の可能性大（3秒チェックリスト）</h2>
        <ul style="list-style: none; font-size: 0.88rem; line-height: 1.7; padding-left: 0;">
          {checklist_items}
        </ul>
      </div>

      <div style="text-align: center; padding: 1.5rem; background: var(--bg-input); border-radius: 12px; border: 1px solid var(--primary); margin-bottom: 1.8rem;">
        <div style="font-size: 1.1rem; font-weight: 800; margin-bottom: 0.45rem;">
          🛡️ 登録不要・サーバー保存ゼロ！今すぐ3秒で無料AI判定
        </div>
        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">
          1日3回まで完全無料でお試しいただけます。全センテンス根拠表示・相手が言い逃れできない確認返信テンプレ3選・監査証明書PDF出力は公式noteの「7日間徹底監査パス（¥980）」で即時解放されます。
        </p>
        <div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">
          <a href="index.html{cta_query}" class="btn btn-primary" style="font-size:0.95rem; padding:0.75rem 1.4rem;">🔍 今すぐこのケースを無料診断する（1クリック検証可）</a>
          <a href="{NOTE_URL}" target="_blank" rel="noopener noreferrer" class="btn btn-gold" style="font-size:0.95rem; padding:0.75rem 1.4rem;">📝 公式noteで徹底監査パス(¥980)を取得 ↗</a>
        </div>
      </div>

      <h2 style="font-size: 1.05rem; margin-bottom: 0.75rem; color: #34d399;">💬 よくある質問（FAQ）</h2>
      <div style="margin-bottom: 1.8rem;">
        {faq_items_html}
      </div>

      <hr style="border: none; border-top: 1px solid var(--border-color); margin: 1.5rem 0;" />
      <h2 style="font-size: 1rem; margin-bottom: 0.6rem;">📚 関連するAI見抜き方・監査ガイド一覧（全25ページ）</h2>
      <ul style="padding-left: 1.2rem; font-size: 0.84rem; line-height: 1.9;">
        <li><a href="lp-matching.html" style="color:#38bdf8; font-weight:700;">【特設LP】マッチングアプリ・LINEのAI業者＆ロマンス詐欺診断</a></li>
        <li><a href="lp-crowdworks.html" style="color:#38bdf8; font-weight:700;">【特設LP】クラウドワークス外注記事のChatGPTコピペ＆Wordリビジョン監査</a></li>
        <li><a href="lp-report.html" style="color:#38bdf8; font-weight:700;">【特設LP】大学レポート・就活ESのAI代筆チェッカー</a></li>
        <li><a href="lp-mercari.html" style="color:#38bdf8; font-weight:700;">【特設LP】メルカリ出品画像・SNSアイコンのAI生成ヒートマップ解析</a></li>
        {links_html}
      </ul>
    </article>
  </main>
</body>
</html>"""
        for folder in (STATIC_DIR, DOCS_DIR):
            if os.path.exists(folder):
                with open(os.path.join(folder, t["slug"]), "w", encoding="utf-8") as f:
                    f.write(html)

    # Sitemap 全25ページ更新
    today = datetime.now().strftime("%Y-%m-%d")
    all_pages = (
        ["", "lp-matching.html", "lp-crowdworks.html", "lp-report.html", "lp-mercari.html"]
        + [t["slug"] for t in SEO_TOPICS]
    )
    items = []
    for u in all_pages:
        loc = f"{BASE_URL}/{u}" if u else f"{BASE_URL}/"
        prio = "1.0" if not u else ("0.9" if u.startswith("lp-") else "0.85")
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


def patch_frontend_conversion_and_sync() -> None:
    app_js_path = os.path.join(STATIC_DIR, "app.js")
    if os.path.exists(app_js_path):
        with open(app_js_path, "r", encoding="utf-8") as f:
            js = f.read()

        # 1. Deep-link ?tab=...&sample=... support
        if 'params.get("sample")' not in js:
            js = js.replace(
                "  initLocalLedgerIfEmpty();\n  refreshDashboard();",
                """  initLocalLedgerIfEmpty();
  refreshDashboard();

  const initTab = params.get("tab");
  if (initTab && ["messenger", "stylometry", "photo_report", "document"].includes(initTab)) {
    switchTab(initTab);
  }
  const initSample = params.get("sample");
  if (initSample && (SAMPLES[initSample] || initSample === "stylometry_case")) {
    setTimeout(() => loadSample(initSample), 120);
  }""",
                1,
            )

        # 2. High-converting dynamic paywall with direct note.com checkout + code input
        if "hiddenSentencesCount" not in js:
            old_target = """  } else {
    container.innerHTML = `
      ${sentenceHtml}
      <div class="paywall-wrapper">"""
            new_target = """  } else {
    const hiddenSentencesCount = Math.max(sentences.length - 1, 1);
    const highRiskCount = sentences.filter((s) => s.ai_probability >= 65).length || 1;
    const scoreVal = Number(data.ai_probability) || 85;
    container.innerHTML = `
      ${sentenceHtml}
      <div class="paywall-wrapper">"""
            js = js.replace(old_target, new_target, 1)

            old_overlay = """        <div class="paywall-overlay">
          <div style="font-size: 0.76rem; font-weight: 800; color: var(--gold); letter-spacing: 0.04em; margin-bottom: 0.3rem;">
            🔒 PRO AUDIT EVIDENCE LOCKED
          </div>
          <div style="font-size: 1.02rem; font-weight: 800; margin-bottom: 0.4rem;">
            残りすべての文単位ハイライト＆「相手が言い逃れできない確認・差し戻し文面3選」を解放
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); max-width: 470px; margin-bottom: 0.9rem;">
            買い切り <strong>¥980（7日間・徹底監査パス）</strong> またはシリアルコード認証で、全証拠データ・返信テンプレート・公式監査証明書PDF出力が今すぐアンロックされます。
          </p>
          <button class="btn btn-gold" onclick="openPaywallModal('診断結果内ロック解除')">
            🔓 ¥980 で全証拠＆返信テンプレを今すぐ解放（コード認証もこちら）
          </button>
        </div>"""
            new_overlay = """        <div class="paywall-overlay">
          <div style="font-size: 0.76rem; font-weight: 800; color: #f87171; background: rgba(239,68,68,0.16); padding: 0.25rem 0.65rem; border-radius: 999px; border: 1px solid rgba(239,68,68,0.4); margin-bottom: 0.45rem;">
            ⚠️ この入力データから「要注意AIシグナル ${highRiskCount}箇所（残り${hiddenSentencesCount}文）」が検出されました
          </div>
          <div style="font-size: 1.04rem; font-weight: 800; margin-bottom: 0.4rem;">
            AI疑惑スコア ${scoreVal}% の決定的証拠＆「相手が言い逃れできない確認・差し戻し文面3選」を今すぐ解放
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); max-width: 490px; margin-bottom: 0.85rem;">
            公式noteで <strong>¥980（7日間・徹底監査パス / 自動課金なし）</strong> を購入してシリアルコードを入力すると、隠された全${hiddenSentencesCount}文のAI根拠ハイライト・コピペ即利用可能な追及テンプレート・公式監査証明書PDF保存が<strong>10秒でアンロック</strong>されます。
          </p>
          <div style="display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap;">
            <a href="https://note.com/safe_swift4998/n/na1af72c84723" target="_blank" rel="noopener noreferrer" class="btn btn-gold" onclick="openPaywallModal('診断結果からnote直行')">
              📝 公式noteでシリアルコードを取得（¥980）↗
            </a>
            <button class="btn btn-primary" onclick="openPaywallModal('診断結果内ロック解除')">
              🔑 取得済みコードを入力してアンロック
            </button>
          </div>
        </div>"""
            js = js.replace(old_overlay, new_overlay, 1)

        with open(app_js_path, "w", encoding="utf-8") as f:
            f.write(js)

    # static/ から docs/ へ全アセット同期
    if os.path.exists(DOCS_DIR):
        for fname in os.listdir(STATIC_DIR):
            src = os.path.join(STATIC_DIR, fname)
            dst = os.path.join(DOCS_DIR, fname)
            if os.path.isfile(src):
                shutil.copy2(src, dst)


if __name__ == "__main__":
    build_all_topic_pages()
    patch_frontend_conversion_and_sync()
