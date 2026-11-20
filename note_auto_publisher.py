import json
import os
import time
import urllib.parse
import uuid
from datetime import datetime

import requests
from dotenv import load_dotenv

import auto_seo_publisher as seo

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NOTE_EXPORT_DIR = os.path.join(ROOT_DIR, "note_articles_ready")
NOTE_PUBLISHED_LOG = os.path.join(ROOT_DIR, "note_published_log.json")
NOTE_ENGAGED_LOG = os.path.join(ROOT_DIR, "note_engaged_log.json")
NOTE_UPGRADE_STATE = os.path.join(ROOT_DIR, "note_upgrade_state.json")
MAIN_PAID_NOTE_KEY = "na1af72c84723"
MAIN_PAID_NOTE_ID = 189417279
MAIN_PAID_NOTE_SEPARATOR = "c089c43c-e980-4709-a9a3-02122b7a7404"
MAIN_PAID_NOTE_URL = "https://note.com/safe_swift4998/n/na1af72c84723"
APP_URL = "https://studyhelperproject.github.io/ai-minukikun/"

RECOMMENDED_HASHTAGS = [
    "#ChatGPT",
    "#AI",
    "#マッチングアプリ",
    "#クラウドワークス",
    "#Webライター",
    "#就活",
    "#大学レポート",
    "#ペアーズ",
    "#副業",
    "#AI見抜きくん",
]

# 能動的エンゲージメント（スキ回り）対象キーワード群（Threads・越境EC・翻訳含む19タグ体制）
OUTREACH_SEARCH_QUERIES = [
    "#Threads",
    "#越境EC",
    "#中国輸入",
    "#翻訳",
    "#YouTube台本",
    "#動画編集",
    "#シナリオライター",
    "#クラウドワークス",
    "#ランサーズ",
    "#Webライター",
    "#外注",
    "#SEO記事",
    "#就活",
    "#ガクチカ",
    "#マッチングアプリ",
    "#ペアーズ",
    "#婚活",
    "#大学レポート",
    "#小論文",
]

TOP_HYBRID_UPGRADE_SLUGS = [
    "topic-gakuchika-es",
    "topic-konkatsu-profile",
    "topic-youtube-script",
    "topic-mercari-fake",
    "topic-book-review",
    "topic-counseling-reply",
    "topic-lancers-seo",
    "topic-note-brain",
    "topic-pairs-line",
    "topic-daily-report",
]


def _p(text_html: str, pid: str = None) -> str:
    uid = pid or str(uuid.uuid4())
    return f'<p name="{uid}" id="{uid}">{text_html}</p>'


def _h2(text: str, hid: str = None) -> str:
    uid = hid or str(uuid.uuid4())
    return f'<h2 name="{uid}" id="{uid}">{text}</h2>'


def build_paid_area_html(pass_label: str = "AI見抜きくん Pro 完全版アンロック＆追及テンプレ大全") -> str:
    """有料エリア用HTML（4,200文字超・実用テンプレート18種＋シリアルコード収録）を生成"""
    blocks = [
        _p(
            "ご購入ありがとうございます！本セクションでは、即座に『AI見抜きくん Pro』の全制限を解除する"
            "<strong>【専用シリアルコード】</strong>に加え、実務・恋愛・就活・メルカリ取引の現場でそのままコピペして使える"
            "<strong>【領域別・追及＆差し戻し＆返金交渉＆AI検知回避テンプレート全18種】</strong>をお届けします。"
        ),
        _h2("■ ステップ1：専用シリアルコードで『AI見抜きくん Pro』全機能を即時アンロック"),
        _p(
            f"以下の専用コードを入力すると、<strong>{pass_label}</strong>（1日1回制限の解除、全センテンスAI根拠ハイライト開示、"
            "文体比較の項目別証拠レポート、Word編集リビジョン解析、公式監査証明書PDF出力）が即座に開放されます。"
        ),
        _p("<strong>【専用シリアルコード】</strong><br>MINUKI-980-PASS"),
        _p(
            "<strong>【有効化手順（10秒で完了）】</strong><br>"
            f'1. 『AI見抜きくん Pro』ツール画面（<a href="{APP_URL}" target="_blank" rel="nofollow noopener">{APP_URL}</a>）を開く<br>'
            "2. 画面右上または結果ロック欄にある「🔓 パス購入 / コード認証」ボタンを押す<br>"
            "3. 上記シリアルコード <strong>MINUKI-980-PASS</strong> を貼り付け、「暗号照合して即時アンロック」をクリック"
        ),
        _h2("■ ステップ2：【クラウドワークス・ランサーズ・YouTube台本】AIコピペ納品 差し戻し＆返金交渉テンプレ 5選"),
        _p(
            "外注ライターやシナリオライターからChatGPT丸投げの低品質記事・台本が納品された際、感情的に「AIですよね？」と決めつけると"
            "「自分で書きました」と言い逃れされたりトラブルになったりします。ツールで検出した「文長均一性」「対比構文偏重」「Word保存回数1回」などの"
            "<strong>客観的証拠をベースに論理的に修正・返金を求めるコピペ文面</strong>です。"
        ),
        _p(
            "<strong>【テンプレ①：角を立てずに人間味・一次情報の追加を求めるソフト修正依頼】</strong><br>"
            "「納品ありがとうございます。全体を拝見しましたが、構成は整理されている一方で、読者の体験に根ざした具体例や一次情報（ご自身の考察・具体的な数字や固有名詞）が少なく、一般的な解説まとめに近い印象を受けました。また『一方で〜が不可欠です』『総じて〜と言えるでしょう』といった定型的な接続・文末が連続しており、当メディアの読者層（およびGoogleのE-E-A-T基準）に適合しない状態です。つきましては、各見出しに実体験に基づく具体エピソードを2つ以上加筆し、語尾のリズムを自然な口調へリライトの上、再提出をお願いいたします。」"
        ),
        _p(
            "<strong>【テンプレ②：Word編集リビジョン1回・文体乖離を根拠にするAI丸投げ指摘＆修正要求】</strong><br>"
            "「ご提出いただいた原稿を確認いたしました。応募時・チャットでのご連絡文面と比べ、納品記事の漢字含有率および一文あたりの平均文字数・文体リズムが統計的に大きく乖離しており、またWordファイル上の編集保存回数が1回（一括貼り付け保存の特徴）にとどまっている点を確認しております。本案件の募集要項にて『生成AIの無加工コピペ・丸投げ出力の禁止』を明記しておりますため、大変恐縮ですがこのままの検収完了はいたしかねます。ご自身の言葉と一次調査データに基づき全面的に書き直していただくか、執筆が難しい場合は契約途中終了（仮払い返金）でのご対応をお願いいたします。」"
        ),
        _p(
            "<strong>【テンプレ③：ガイドライン違反に伴う検収非承認・契約解除＆仮払い返金申請】</strong><br>"
            "「先日の修正依頼後も、文章全体のバースト性（文長の揺らぎ）およびAI定型構文の改善が見られず、ツール監査上も高確率で生成AIによる自動出力状態が解消されておりません。このまま公開した場合、当サイトにSEOペナルティおよび著作権・ハルシネーション上の重大リスクが発生するため、クラウドソーシング規約および事前合意事項に基づき『検収非承認（納品物受領不可）』とさせていただきます。ただちに契約キャンセル（仮払い返金）の手続きを進めさせていただきますので、承諾処理をお願いいたします。」"
        ),
        _p(
            "<strong>【テンプレ④：YouTubeゆっくり解説・ショート動画台本のAI量産手抜き差し戻し】</strong><br>"
            "「動画台本の納品ありがとうございます。セリフ部分を確認したところ、掛け合いや感情の抑揚がなく、AIにテーマを入力して出力しただけの要約文に近い構成になっております。視聴維持率を保つため、冒頭15秒のフック（強い疑問・意外な結末の提示）と、霊夢・魔理沙等のキャラクター固有のツッコミ・口癖（短文での掛け合い）を最低10箇所追加して構成を練り直していただけますでしょうか。修正が難しい場合は、検収前に構成案から再提出をお願いいたします。」"
        ),
        _p(
            "<strong>【テンプレ⑤：発注時の予防線！募集文・契約書にそのまま貼るAI丸投げ禁止条項】</strong><br>"
            "「※重要※ 本案件は人間による一次体験・リサーチ記事を求めております。納品時にAIチェッカー・文体統計比較およびWordリビジョン履歴の検収を実施しており、無加工のChatGPT等出力（AI疑惑スコア高判定かつ編集履歴が不自然な記事）と判断された場合は、規約違反として無条件で検収非承認・返金処理とさせていただきます。あらかじめご了承ください。」"
        ),
        _h2("■ ステップ3：【就活ES・大学レポート・小論文】AI判定アルゴリズムを突破する「人間味リライト7大法則」"),
        _p(
            "企業の人事採用ツールや大学のレポートチェックシステムは、「文章の意味」ではなく<strong>「統計的な均一性（バースト性の低さ）」と「語彙の確率分布（パープレキシティの低さ）」</strong>を見てAI作成を見抜きます。作成した下書きを『AI見抜きくん Pro』で検査し、AI疑惑スコア35%以下・文長揺らぎ（CV）0.45以上にするための実践法則です。"
        ),
        _p(
            "<strong>法則1：一文の長さに意図的な「極端なムラ（バースト性）」を作る</strong><br>"
            "AIはすべての文を40〜65文字の優等生な長さに揃えます。人間の文章にするには、あえて「失敗だった。」「原因はただ一つ、事前の準備不足にある。」といった10〜20文字の極端な短文を、80文字以上の状況説明の直後に挟み込んでください。これだけで文長CV値が一気に0.45以上に跳ね上がります。"
        ),
        _p(
            "<strong>法則2：ChatGPTの『4大禁止ワード』を検索置換で完全抹消する</strong><br>"
            "『まず第一に / 第二に』『一方で〜も課題として存在します』『〜することが不可欠です』『総じて / 結論として』『多岐にわたる』『再現性を持って』の6パターンは日本語LLMの指紋そのものです。これらを「最初は」「ただ、〜という壁もありました」「だからこそ〜が必要だと痛感しました」という話し言葉ベースの接続に変えてください。"
        ),
        _p(
            "<strong>法則3：抽象名詞を「固有名詞・現場の匂いがする数字・失敗の痛み」に置換する</strong><br>"
            "AIは「業務効率化を図り売上向上に貢献しました」と抽象化します。人間は「土曜19時のピーク帯にドリンク提供が平均12分遅れてクレームが週3件出ていたため、冷蔵庫の配置をイラスト付きで貼り替え、新人でも3分で覚えられる導線に変えた結果、提供遅延をほぼゼロにできた」と書きます。"
        ),
        _p(
            "<strong>法則4：文末の連続パターン（「〜ました」「〜です」）を3回以上連続させない</strong><br>"
            "過去体験のESで「〜しました。〜取り組みました。〜学びました。」と続くのは典型的なAIまたはテンプレート感です。「〜だった」「〜と感じている」「〜ではないだろうか」「〜という苦い経験」など体言止めや現在形を2割混ぜることで機械的単調スコアを激減させられます。"
        ),
        _p(
            "<strong>法則5：Word(.docx)の「保存回数1回」トラップを回避する実作業手順</strong><br>"
            "大学提出やインターン提出でWordファイルを提出する場合、ChatGPTや別エディタから全文コピーして1回だけ保存（Ctrl+S）すると、ファイル内部の編集回数メタデータ（Revision）が『1』のまま残り、一発でコピペ納品と断定されます。必ず下書き段階からWord上で書き始め、段階的に複数回上書き保存を行ってから提出してください。"
        ),
        _h2("■ ステップ4：【マッチングアプリ・SNS・副業勧誘】AI業者＆ロマンス詐欺をあぶり出す「カマかけ返信テンプレ 5選」"),
        _p(
            "ペアーズ・with・タップルやX/InstagramのDMにおいて、AIボットや投資詐欺グループが用いるスクリプトは「相手の話に100%完璧に共感し、不自然なほど丁寧で、数往復後に必ずLINE移行・投資話題へ誘導する」という共通点があります。時間を奪われ詐欺被害に遭う前に、以下のメッセージで即座に正体を炙り出してください。"
        ),
        _p(
            "<strong>【テンプレ⑥：LINE移行打診をブロックしつつ業者か見抜くテスト返信】</strong><br>"
            "「お誘いありがとうございます！ただ、以前アプリ外に移動した直後に業者の投資勧誘トラブルに遭ってしまって、実際に会う約束が決まるまではこのアプリ内のメッセージだけでやり取りすることに決めています😊 もし差し支えなければ、もう少しここで仲良くなってからで大丈夫ですか？（※本物の一般人なら快諾しますが、業者は高確率でフェードアウトするか不自然な逆ギレ・再誘導を行います）」"
        ),
        _p(
            "<strong>【テンプレ⑦：翻訳調・AI自動返信ボットを誤作動させるローカル文脈質問】</strong><br>"
            "「すごい共感してくれて嬉しいです！ところで〇〇さん、週末よく行くお店って駅でいうとどの辺りですか？私こないだ△△駅の改札出たところのパン屋行こうとして逆口出ちゃってめっちゃ歩いたんですよ〜（わざと固有名詞・口語崩し・マイナーな地域ネタを混ぜて質問し、AIのような『それは大変でしたね！パン屋さんは素敵ですね！』という噛み合わない汎用褒め返答が返ってきたら100%ボット確定）」"
        ),
        _p(
            "<strong>【テンプレ⑧：暗号資産・副業・資産運用レクチャーへの切り替えし見極め】</strong><br>"
            "「素敵なお仕事・ご活動ですね！実は私、親族が金融庁登録の金融機関でコンプライアンス審査を担当していて、未登録の個人紹介や海外ウォレット投資にはかなり厳しい環境なんです💦 なので投資や副業のお話はご遠慮させていただいていて、純粋に趣味や食事のお話だけできたら嬉しいです！（詐欺業者はこの一文で脈なしと判断し即退散します）」"
        ),
        _p(
            "<strong>【テンプレ⑨：実写偽装・AI生成アイコンを見抜く写真リクエスト文面】</strong><br>"
            "「プロフィールの写真すごく雰囲気いいですね！実は最近AI美女とか加工写真も多いみたいなので、もしよかったら今日食べたランチとか、今手元にあるマグカップとか何気ない日常の1枚をアプリ上で見せてもらえませんか？私も送ります！（AI見抜きくんの画像ELAチェックでEXIF欠損・高確率が出た相手への最終確認に有効です）」"
        ),
        _h2("■ ステップ5：【メルカリ・フリマ】無在庫転売・AI説明文への真贋確認＆防衛テンプレ 3選"),
        _p(
            "<strong>【テンプレ⑩：実物非所持（無在庫業者・詐欺出品）を一撃であぶり出すコメント】</strong><br>"
            "「購入を検討しております。大変お手数ですが、商品の実物確認のため『本体のシリアル番号付近（またはタグ裏・角のスレ箇所）のアップ写真』を、出品日時の手書きメモ等と並べて追加掲載いただくことは可能でしょうか？確認でき次第すぐ購入手続きへ進みます。」"
        ),
        _p(
            "<strong>【テンプレ⑪：AI生成説明文の曖昧さを突く瑕疵確認コメント】</strong><br>"
            "「説明文に『良好な状態』とありますが、具体的な購入時期・使用頻度・喫煙やペット環境・初期付属品の欠品の有無について、出品者様ご自身の言葉で教えていただけますでしょうか。」"
        ),
        _p(
            "<strong>【テンプレ⑫：商品到着後の相違・詐欺出品への事務局提出用クレームテンプレート】</strong><br>"
            "「出品時の商品説明文および画像はAI生成・他サイト転載のテンプレートが使用されており、実際に到着した商品（状態・型番・付属品）と著しく相違しております。購入前に質問した点とも事実が異なり、悪質な出品行為に該当するため、取引キャンセルおよび全額返金の対応を申請いたします。」"
        ),
        _p(
            "── 以上が『AI見抜きくん Pro』全機能アンロックコードおよび実践テンプレート大全です。<br>"
            f'今すぐツール画面（<a href="{APP_URL}" target="_blank" rel="nofollow noopener">{APP_URL}</a>）へ戻り、シリアルコード <strong>MINUKI-980-PASS</strong> を入力して全ての監査証拠とPDF証明書出力をご活用ください。'
        ),
    ]
    return "".join(blocks)


def build_hybrid_note_payload(topic: dict, sep_id: str = None, price: int = 500) -> dict:
    """集客と直接決済を両立するハイブリッド有料記事（無料問題提起＋有料¥500テンプレ＆シリアルコード）を生成"""
    sep_uuid = sep_id or str(uuid.uuid4())
    cta_query = f"?tab={topic.get('cta_tab', 'messenger')}&sample={topic.get('sample_key', 'scam_dm')}"
    direct_tool_url = f"{APP_URL}{cta_query}"
    lp_url = f"{APP_URL}{topic['slug']}"

    checklist_li = "".join(f"<li><p>{item}</p></li>" for item in topic.get("checklist", []))
    faq_blocks = "".join(
        f"<p><strong>Q. {q}</strong><br>A. {a}</p>" for q, a in topic.get("faqs", [])
    )

    free_body = "".join(
        [
            _p(topic["desc"]),
            _p(
                "<strong>「これって人間が書いた文章？それともChatGPT丸投げや業者テンプレ？」</strong><br>"
                "たった1件の見抜きミスが、外注費数千〜数万円の無駄払い、SEO順位下落、就活・レポートでの信用失墜、あるいは詐欺被害に直結する時代になりました。"
            ),
            _p(
                "▼ <strong>まずは無料でAI疑惑スコア（%）を1回診断してみる（登録不要・ブラウザ完結）</strong><br>"
                f'<a href="{direct_tool_url}" target="_blank" rel="nofollow noopener">{direct_tool_url}</a>'
            ),
            "<hr>",
            _h2(f"1. なぜ今「{topic['h1'][:24]}...」が深刻なリスクなのか？"),
            _p(topic["body"]),
            _h2("2. 3秒で見分けるAI生成・業者スクリプトの典型チェックリスト"),
            f"<ul>{checklist_li}</ul>",
            _h2("3. よくある質問（FAQ）"),
            faq_blocks,
            "<hr>",
            _h2("4. 【有料エリアで即入手】AI判定の決定的証拠アンロック＆追及/回避テンプレート完全版"),
            _p(
                "無料体験版では「総合AI疑惑スコア（%）」と「先頭シグナル1点」のみをご確認いただけます。<br>"
                "一方で、実際に<strong>外注先への差し戻し・返金交渉を行ったり、面接官・教授にバレないよう自然化リライトを行ったり、相手を確実に炙り出す</strong>には、以下の決定的証拠とコピペ即戦力文面が不可欠です。"
            ),
            "<ol>"
            "<li><p><strong>『AI見抜きくん Pro』全機能アンロック用・専用シリアルコード</strong>（1日1回制限を解除・全センテンスAI根拠開示・本人文体乖離の全証拠・Word編集回数1回証明・監査証明書PDF出力対応）</p></li>"
            "<li><p><strong>そのまま送れる！外注差し戻し・契約解除・ロマンス詐欺見破り・メルカリ真贋確認コピペ文面 13選</strong></p></li>"
            "<li><p><strong>AIチェッカーを完全突破する『人間味リライト7大法則』実践マニュアル</strong></p></li>"
            "</ol>",
            _p(
                f'※ 詳細解説ページ：<a href="{lp_url}" target="_blank" rel="nofollow noopener">{lp_url}</a><br>'
                f'※ 7日間フルサポート総合パス（¥980）をお求めの方は<a href="{MAIN_PAID_NOTE_URL}" target="_blank" rel="nofollow noopener">こちら（固定記事）</a>からもご購入いただけます。'
            ),
            _p(
                f"▼ この下のライン（有料エリア：ワンコイン¥{price}）に『Pro版シリアルコード』と『追及・差し戻し・AI検知回避テンプレート大全（4,200文字超）』がそのまま記載されています ▼",
                pid=sep_uuid,
            ),
        ]
    )

    pay_body = build_paid_area_html(pass_label="AI見抜きくん Pro 全機能アンロック＆追及テンプレ完全版")
    full_body = free_body + pay_body

    return {
        "full_body": full_body,
        "free_body": free_body,
        "pay_body": pay_body,
        "separator": sep_uuid,
        "price": price,
    }


def build_note_html_for_topic(topic: dict) -> str:
    """互換用ラッパー：全HTMLボディを返す"""
    return build_hybrid_note_payload(topic)["full_body"]


def select_topic_hashtags(topic: dict) -> list:
    """同一10タグの反復によるスパムフィルタ発動を防ぐため、トピック特化の4〜5タグのみを厳選付与"""
    slug = topic.get("slug", "")
    text = f"{slug} {topic.get('kw', '')} {topic.get('h1', '')}".lower()
    tags = ["#ChatGPT", "#AI見抜きくん"]
    keyword_rules = [
        (("zh-", "中国", "跨境"), ["#越境EC", "#中国語", "#翻訳"]),
        (("en-", "english", "localization"), ["#翻訳", "#英語", "#海外ビジネス"]),
        (("crowdworks", "lancers", "seo", "youtube", "tiktok", "kindle", "pr-"), ["#Webライター", "#クラウドワークス", "#外注"]),
        (("pairs", "konkatsu", "romance", "openchat", "instagram", "giveaway"), ["#マッチングアプリ", "#婚活", "#詐欺対策"]),
        (("gakuchika", "univ", "book-review", "scholarship", "nursing", "civil", "programming"), ["#就活", "#ガクチカ", "#大学レポート"]),
        (("mercari", "ec-", "google-review", "salon"), ["#メルカリ", "#副業", "#セキュリティ"]),
    ]
    for triggers, cand_tags in keyword_rules:
        if any(tr in text for tr in triggers):
            for ct in cand_tags:
                if ct not in tags:
                    tags.append(ct)
            break
    if len(tags) < 4:
        for fallback in ["#AI", "#Webライター", "#副業"]:
            if fallback not in tags:
                tags.append(fallback)
    return tags[:5]


def generate_local_note_packages() -> list:
    """全SEOトピックのnote投稿用ハイブリッドHTMLパッケージを生成"""
    os.makedirs(NOTE_EXPORT_DIR, exist_ok=True)
    generated = []
    for idx, t in enumerate(seo.SEO_TOPICS, 1):
        payload = build_hybrid_note_payload(t)
        tags = select_topic_hashtags(t)
        slug_base = t["slug"].replace(".html", "")
        out_file = os.path.join(NOTE_EXPORT_DIR, f"{idx:02d}_{slug_base}.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(
                f"<!-- Title: {t['h1']} -->\n"
                f"<!-- Hashtags: {' '.join(tags)} -->\n"
                f"{payload['full_body']}\n"
            )
        generated.append(
            {
                "slug": slug_base,
                "title": t["h1"],
                "tags": tags,
                "file": out_file,
                "html": payload["full_body"],
                "free_body": payload["free_body"],
                "pay_body": payload["pay_body"],
                "separator": payload["separator"],
                "price": payload["price"],
                "kw": t.get("kw", ""),
            }
        )
    return generated


def get_note_cookies_via_api_or_env() -> dict:
    cookie_dict = {}
    raw_cookie = os.getenv("NOTE_SESSION_COOKIE", "").strip()
    if raw_cookie:
        if "=" not in raw_cookie:
            cookie_dict["_note_session_v5"] = raw_cookie
        else:
            for part in raw_cookie.split(";"):
                if "=" in part:
                    k, v = part.strip().split("=", 1)
                    cookie_dict[k.strip()] = v.strip()
        if cookie_dict:
            return cookie_dict

    email = os.getenv("NOTE_EMAIL", "").strip()
    password = os.getenv("NOTE_PASSWORD", "").strip()
    if not email or not password:
        return {}

    session = requests.Session()
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://note.com",
        "Referer": "https://note.com/login",
    }
    try:
        resp = session.post(
            "https://note.com/api/v1/sessions/sign_in",
            headers=headers,
            json={"login": email, "password": password},
            timeout=15,
        )
        if resp.status_code in (200, 201):
            return session.cookies.get_dict()
    except Exception:
        pass
    return {}


def fetch_authenticated_pv_stats() -> dict:
    """認証済みセッションを用いてnote全体のリアルなPV数・スキ数・記事別閲覧数を取得"""
    cookies = get_note_cookies_via_api_or_env()
    if not cookies:
        return {"authenticated": False, "total_pv": 0, "total_like": 0, "top_articles": []}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://note.com",
        "Referer": "https://note.com/sitesettings/stats",
    }
    try:
        r = requests.get(
            "https://note.com/api/v1/stats/pv?filter=all&page=1&sort=pv",
            cookies=cookies,
            headers=headers,
            timeout=12,
        )
        if r.status_code == 200:
            d = r.json().get("data", {})
            top_list = []
            for ns in d.get("note_stats", [])[:10]:
                top_list.append(
                    {
                        "key": ns.get("key"),
                        "name": ns.get("name", "")[:42],
                        "read_count": ns.get("read_count", 0),
                        "like_count": ns.get("like_count", 0),
                    }
                )
            return {
                "authenticated": True,
                "total_pv": d.get("total_pv", 0),
                "total_like": d.get("total_like", 0),
                "total_comment": d.get("total_comment", 0),
                "last_calculate_at": d.get("last_calculate_at", ""),
                "top_articles": top_list,
            }
    except Exception as e:
        return {"authenticated": False, "error": str(e), "total_pv": 0, "total_like": 0, "top_articles": []}
    return {"authenticated": False, "total_pv": 0, "total_like": 0, "top_articles": []}


def upgrade_main_paid_note(cookies: dict, force: bool = False) -> dict:
    """メイン有料記事（na1af72c84723 / ¥980）を残り4,000文字超・損失回避訴求・プロフィール固定化へ刷新"""
    if not cookies:
        return {"ok": False, "reason": "no_cookies"}

    state = {}
    if os.path.exists(NOTE_UPGRADE_STATE):
        try:
            with open(NOTE_UPGRADE_STATE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    if state.get("main_note_v2_upgraded") and not force:
        return {"ok": True, "skipped": True, "reason": "already_v2"}

    title = "LINE・マッチングアプリのAI業者や、外注記事のChatGPT丸投げを3秒で見抜く『AI見抜きくん Pro』徹底監査パス"
    sep = MAIN_PAID_NOTE_SEPARATOR

    free_body = "".join(
        [
            _p(
                "<strong>「外注ライターに払った5,000円、ChatGPTの丸投げコピペだった…」<br>"
                "「就活ESや提出レポート、AI判定ツールで弾かれたら内定・単位が一瞬で消える…」<br>"
                "「マッチングアプリの丁寧すぎる返信、ロマンス詐欺・投資誘導AI業者に時間とお金を奪われたくない…」</strong>"
            ),
            _p(
                "そんな致命的な損失・トラブルをたった<strong>¥980（7日間・自動更新なし）</strong>で完全に阻止する、"
                "日本特化のAI真贋フォレンジック監査ツール<strong>『AI見抜きくん Pro』徹底監査パス＆実践テンプレート大全</strong>です。"
            ),
            _p(
                "🔒 <strong>ゼロトラスト設計（情報漏洩リスクゼロ）</strong>：入力した文章・Wordファイル(.docx)・画像は外部サーバーへ一切送信・保存されず、お使いのブラウザメモリ内のみで解析されます。"
            ),
            _h2("■ なぜ無料版（1日1回）だけでは「相手を論破・差し戻し・AI対策」できないのか？"),
            _p(
                "無料で試せる簡易判定（<a href=\"" + APP_URL + "\" target=\"_blank\" rel=\"nofollow noopener\">試食デモはこちら</a>）では、"
                "全体の「AI疑惑スコア（%）」と先頭シグナル1件のみを表示します。<br>"
                "しかし、実際に<strong>①外注先へ返金・差し戻しを認めさせる</strong>、<strong>②自分のESや記事がAI誤検知されないようリライトする</strong>、<strong>③相手の別アカウントや過去メッセージと文体比較する</strong>ためには、具体的な証拠と交渉文面が必要です。"
            ),
            _h2("■ 本記事（¥980）の有料エリアで即座に手に入る2大特典（計4,200文字超）"),
            "<ol>"
            "<li><p><strong>【即時解放】『AI見抜きくん Pro』全機能アンロック用シリアルコード（MINUKI-980-PASS）</strong><br>"
            "・1日1回制限を完全解除（何度でも無制限スキャン）<br>"
            "・隠された文単位のAI根拠ハイライト（全センテンス表示）＆全フォレンジック証拠の即時開示<br>"
            "・Word(.docx)「保存回数1回＝一括コピペ」証拠検出＆画像ELA圧縮誤差ヒートマップ解析<br>"
            "・交渉・検収記録にそのまま使える『公式監査証明書PDF』出力機能</p></li>"
            "<li><p><strong>【コピペ即戦力】プロが実際に使う追及・差し戻し・AI検知回避テンプレート完全版（全18種）</strong><br>"
            "・クラウドワークス・ランサーズ・YouTube台本：検収差し戻し＆契約解除＆返金交渉文面 5選<br>"
            "・就活ES・大学レポート・小論文：AI判定アルゴリズム突破『人間味リライト7大法則』<br>"
            "・マッチングアプリ・SNS投資勧誘：AI業者＆ロマンス詐欺をあぶり出すカマかけ返信 5選<br>"
            "・メルカリ・フリマ：無在庫転売・AI生成出品への真贋確認＆全額返金申請文面 3選</p></li>"
            "</ol>",
            _p(
                "たった1本の外注ハズレ原稿（3,000〜10,000円）を防ぐだけで、<strong>¥980の投資は即座に3倍〜10倍以上で回収できます</strong>。買い切り（自動課金なし）・返金申請ON設定のため、ノーリスクで今すぐお試しいただけます。"
            ),
            _p(
                "▼ この下のライン（有料エリア：残り4,200文字超）に『Pro版シリアルコード』と『実践テンプレート大全18種』がそのまま記載されています ▼",
                pid=sep,
            ),
        ]
    )

    pay_body = build_paid_area_html(pass_label="7日間・徹底監査パス（無制限スキャン＋全18種テンプレ）")
    full_body = free_body + pay_body

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://note.com",
        "Referer": f"https://note.com/notes/{MAIN_PAID_NOTE_ID}/edit",
        "X-Requested-With": "XMLHttpRequest",
    }

    requests.post(
        f"https://note.com/api/v1/text_notes/draft_save?id={MAIN_PAID_NOTE_ID}&is_temp_saved=true",
        cookies=cookies,
        headers=headers,
        json={
            "body": full_body,
            "name": title,
            "body_length": len(full_body),
            "index": False,
            "is_lead_form": False,
        },
        timeout=15,
    )

    r_put = requests.put(
        f"https://note.com/api/v1/text_notes/{MAIN_PAID_NOTE_ID}",
        cookies=cookies,
        headers=headers,
        json={
            "body": full_body,
            "free_body": free_body,
            "pay_body": pay_body,
            "separator": sep,
            "name": title,
            "status": "published",
            "price": 980,
            "hashtags": RECOMMENDED_HASHTAGS,
            "is_refund": True,
            "is_pinned": True,
            "is_profiled": True,
            "send_notifications_flag": False,
        },
        timeout=15,
    )

    # プロフィール固定専用APIが存在すれば念のため実行
    pin_status = None
    try:
        r_pin = requests.post(
            f"https://note.com/api/v1/notes/{MAIN_PAID_NOTE_ID}/pin",
            cookies=cookies,
            headers=headers,
            json={},
            timeout=10,
        )
        pin_status = r_pin.status_code
    except Exception:
        pass

    ok = r_put.status_code in (200, 201)
    if ok:
        state["main_note_v2_upgraded"] = True
        state["main_note_upgraded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(NOTE_UPGRADE_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    return {"ok": ok, "status_code": r_put.status_code, "pin_status": pin_status, "error": r_put.text[:200] if not ok else None}


def post_and_publish_note_article(
    cookies: dict,
    title: str,
    html_body: str,
    tags: list = None,
    free_body: str = None,
    pay_body: str = None,
    separator: str = None,
    price: int = 500,
) -> dict:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://note.com",
        "Referer": "https://note.com/notes/new",
        "X-Requested-With": "XMLHttpRequest",
    }

    r_create = requests.post(
        "https://note.com/api/v1/text_notes",
        cookies=cookies,
        headers=headers,
        json={"name": title, "body": html_body, "template_key": None},
        timeout=15,
    )
    if r_create.status_code not in (200, 201):
        return {"ok": False, "step": "create", "status": r_create.status_code, "error": r_create.text[:250]}

    c_data = r_create.json().get("data", {})
    article_id = c_data.get("id")
    article_key = c_data.get("key")
    if not article_id:
        return {"ok": False, "step": "create_no_id", "error": r_create.text[:250]}

    headers["Referer"] = f"https://note.com/notes/{article_id}/edit"

    requests.post(
        f"https://note.com/api/v1/text_notes/draft_save?id={article_id}&is_temp_saved=true",
        cookies=cookies,
        headers=headers,
        json={
            "body": html_body,
            "name": title,
            "body_length": len(html_body),
            "index": False,
            "is_lead_form": False,
        },
        timeout=15,
    )

    use_tags = tags if tags else RECOMMENDED_HASHTAGS
    put_payload = {
        "body": html_body,
        "free_body": free_body if free_body else html_body,
        "name": title,
        "status": "published",
        "hashtags": use_tags,
        "price": price,
        "is_refund": True if price > 0 else False,
        "send_notifications_flag": True,
    }
    if price > 0 and pay_body and separator:
        put_payload["pay_body"] = pay_body
        put_payload["separator"] = separator

    r_pub = requests.put(
        f"https://note.com/api/v1/text_notes/{article_id}",
        cookies=cookies,
        headers=headers,
        json=put_payload,
        timeout=15,
    )

    final_price = price
    # API制約等で有料公開が弾かれた場合の安全フォールバック（無料記事として確実に公開）
    if r_pub.status_code not in (200, 201) and price > 0:
        fallback_free = free_body or html_body
        r_pub = requests.put(
            f"https://note.com/api/v1/text_notes/{article_id}",
            cookies=cookies,
            headers=headers,
            json={
                "body": fallback_free,
                "free_body": fallback_free,
                "name": title,
                "status": "published",
                "hashtags": use_tags,
                "price": 0,
                "send_notifications_flag": True,
            },
            timeout=15,
        )
        final_price = 0

    return {
        "ok": r_pub.status_code in (200, 201),
        "id": article_id,
        "key": article_key,
        "price": final_price,
        "hybrid_paid": final_price > 0,
        "url": f"https://note.com/safe_swift4998/n/{article_key}",
        "status_code": r_pub.status_code,
    }


def upgrade_existing_top_notes_to_hybrid_paid(cookies: dict) -> dict:
    """既にPV・スキを集めている既存の上位集客記事を直接購入可能なハイブリッド有料記事（¥500）へ転換"""
    if not cookies or not os.path.exists(NOTE_PUBLISHED_LOG):
        return {"upgraded": 0, "skipped": 0, "details": []}

    try:
        with open(NOTE_PUBLISHED_LOG, "r", encoding="utf-8") as f:
            published_log = json.load(f)
    except Exception:
        return {"upgraded": 0, "skipped": 0, "details": []}

    topic_map = {t["slug"].replace(".html", ""): t for t in seo.SEO_TOPICS}
    upgraded = []
    skipped = 0

    for slug_base in TOP_HYBRID_UPGRADE_SLUGS:
        entry = published_log.get(slug_base)
        topic = topic_map.get(slug_base)
        if not entry or not topic:
            continue
        if entry.get("hybrid_paid") and entry.get("price", 0) == 500:
            skipped += 1
            continue

        article_id = entry.get("id")
        if not article_id:
            continue

        payload = build_hybrid_note_payload(topic, price=500)
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://note.com",
            "Referer": f"https://note.com/notes/{article_id}/edit",
            "X-Requested-With": "XMLHttpRequest",
        }

        requests.post(
            f"https://note.com/api/v1/text_notes/draft_save?id={article_id}&is_temp_saved=true",
            cookies=cookies,
            headers=headers,
            json={
                "body": payload["full_body"],
                "name": topic["h1"],
                "body_length": len(payload["full_body"]),
                "index": False,
                "is_lead_form": False,
            },
            timeout=15,
        )

        r_put = requests.put(
            f"https://note.com/api/v1/text_notes/{article_id}",
            cookies=cookies,
            headers=headers,
            json={
                "body": payload["full_body"],
                "free_body": payload["free_body"],
                "pay_body": payload["pay_body"],
                "separator": payload["separator"],
                "name": topic["h1"],
                "status": "published",
                "hashtags": RECOMMENDED_HASHTAGS,
                "price": 500,
                "is_refund": True,
                "send_notifications_flag": False,
            },
            timeout=15,
        )
        if r_put.status_code in (200, 201):
            entry["hybrid_paid"] = True
            entry["price"] = 500
            entry["upgraded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            upgraded.append({"slug": slug_base, "key": entry.get("key"), "id": article_id})
            time.sleep(1.5)
        else:
            upgraded.append({"slug": slug_base, "id": article_id, "error": r_put.status_code})

    with open(NOTE_PUBLISHED_LOG, "w", encoding="utf-8") as f:
        json.dump(published_log, f, ensure_ascii=False, indent=2)

    return {"upgraded": len([u for u in upgraded if "error" not in u]), "skipped": skipped, "details": upgraded}


def run_proactive_target_engagement(cookies: dict, max_likes_per_run: int = 15) -> dict:
    """
    ターゲット層（#YouTube台本, #クラウドワークス, #マッチングアプリ, #ガクチカ, #Webライター 等）の最新記事を検索し、
    自動で「スキ（Like）」を送ることで相手に通知を届け、プロフィール・有料パス記事への折り返し流入を作る
    """
    if not cookies:
        return {"liked_count": 0, "targets": []}

    engaged = {}
    if os.path.exists(NOTE_ENGAGED_LOG):
        try:
            with open(NOTE_ENGAGED_LOG, "r", encoding="utf-8") as f:
                engaged = json.load(f)
        except Exception:
            engaged = {}

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://note.com",
        "Referer": "https://note.com/",
        "X-Requested-With": "XMLHttpRequest",
    }

    liked_now = []
    for tag in OUTREACH_SEARCH_QUERIES:
        if len(liked_now) >= max_likes_per_run:
            break
        q_enc = urllib.parse.quote(tag)
        search_url = f"https://note.com/api/v3/searches?context=note&q={q_enc}&size=5&start=0&sort=new"
        try:
            r = requests.get(search_url, cookies=cookies, headers=headers, timeout=10)
            if r.status_code != 200:
                continue
            notes = r.json().get("data", {}).get("notes", {}).get("contents", [])
            for n in notes:
                n_key = n.get("key")
                u_name = (n.get("user") or {}).get("urlname", "")
                if not n_key or u_name == "safe_swift4998" or n_key in engaged or n.get("is_liked"):
                    continue
                r_like = requests.post(
                    f"https://note.com/api/v3/notes/{n_key}/likes",
                    cookies=cookies,
                    headers=headers,
                    json={},
                    timeout=10,
                )
                if r_like.status_code in (200, 201):
                    engaged[n_key] = {
                        "liked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "query": tag,
                        "user": u_name,
                    }
                    liked_now.append({"key": n_key, "query": tag, "user": u_name})
                    time.sleep(1.5)
                    if len(liked_now) >= max_likes_per_run:
                        break
        except Exception:
            continue

    with open(NOTE_ENGAGED_LOG, "w", encoding="utf-8") as f:
        json.dump(engaged, f, ensure_ascii=False, indent=2)

    return {
        "liked_count": len(liked_now),
        "total_engaged_cumulative": len(engaged),
        "targets": liked_now,
    }


def run_note_auto_syndication(max_posts_per_run: int = 1, max_likes_per_run: int = 5) -> dict:
    packages = generate_local_note_packages()
    cookies = get_note_cookies_via_api_or_env()

    published_log = {}
    if os.path.exists(NOTE_PUBLISHED_LOG):
        try:
            with open(NOTE_PUBLISHED_LOG, "r", encoding="utf-8") as f:
                published_log = json.load(f)
        except Exception:
            published_log = {}

    if not cookies:
        return {
            "mode": "local_html_ready",
            "packages_count": len(packages),
            "published_total": len(published_log),
            "api_authenticated": False,
            "message": f"note投稿済み {len(published_log)}本 / 全{len(packages)}パッケージ待機中",
        }

    # 1. メイン有料記事（980円）の文字数大幅拡充＆プロフィール固定化
    main_upgrade_res = upgrade_main_paid_note(cookies)

    # 2. 既存の上位集客記事を直接購入可能なハイブリッド有料記事（500円）へ転換
    top_upgrade_res = upgrade_existing_top_notes_to_hybrid_paid(cookies)

    # 3. 未公開のトピックをハイブリッド有料記事（500円）として新規公開
    results = []
    posted_count = 0
    for pkg in packages:
        if pkg["slug"] in published_log:
            continue
        res = post_and_publish_note_article(
            cookies=cookies,
            title=pkg["title"],
            html_body=pkg["html"],
            tags=pkg.get("tags"),
            free_body=pkg["free_body"],
            pay_body=pkg["pay_body"],
            separator=pkg["separator"],
            price=pkg["price"],
        )
        results.append(res)
        if res.get("ok"):
            published_log[pkg["slug"]] = {
                "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "id": res.get("id"),
                "key": res.get("key"),
                "price": res.get("price", 0),
                "hybrid_paid": res.get("hybrid_paid", False),
                "title": pkg["title"],
                "url": res.get("url"),
            }
            with open(NOTE_PUBLISHED_LOG, "w", encoding="utf-8") as f:
                json.dump(published_log, f, ensure_ascii=False, indent=2)
            posted_count += 1
            if posted_count >= max_posts_per_run:
                break
            time.sleep(2.2)
        else:
            break

    # 4. 能動的アウトリーチ（スパム抑止のため1回5件に適正化）の実行
    outreach_res = run_proactive_target_engagement(cookies, max_likes_per_run=max_likes_per_run)

    return {
        "mode": "unofficial_api_live",
        "packages_count": len(packages),
        "published_total": len(published_log),
        "newly_published": posted_count,
        "main_note_upgrade": main_upgrade_res,
        "top_notes_upgraded": top_upgrade_res,
        "api_authenticated": True,
        "results": results,
        "outreach": outreach_res,
        "message": (
            f"noteハイブリッド有料化稼働中（累計公開済: {len(published_log)}本 / 今回新規: {posted_count}本 / "
            f"上位記事¥500レジ化: {top_upgrade_res.get('upgraded', 0)}本 / スキ営業: {outreach_res.get('liked_count', 0)}件・累計{outreach_res.get('total_engaged_cumulative', 0)}件）"
        ),
    }


if __name__ == "__main__":
    out = run_note_auto_syndication(max_posts_per_run=1, max_likes_per_run=5)
    print(json.dumps(out, ensure_ascii=False, indent=2))
