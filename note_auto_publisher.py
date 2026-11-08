import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

import auto_seo_publisher as seo

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NOTE_EXPORT_DIR = os.path.join(ROOT_DIR, "note_articles_ready")
NOTE_PUBLISHED_LOG = os.path.join(ROOT_DIR, "note_published_log.json")
MAIN_PAID_NOTE_KEY = "na1af72c84723"
MAIN_PAID_NOTE_ID = 189417279
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


def build_note_html_for_topic(topic: dict) -> str:
    """noteのエディタ仕様（p / h2 / ul / hr / a のみ有効、CSSは無視される仕様）に完全準拠した記事HTMLを生成"""
    cta_query = f"?tab={topic.get('cta_tab', 'messenger')}&sample={topic.get('sample_key', 'scam_dm')}"
    direct_tool_url = f"{APP_URL}{cta_query}"
    lp_url = f"{APP_URL}{topic['slug']}"

    checklist_li = "".join(f"<li><p>{item}</p></li>" for item in topic.get("checklist", []))
    faq_blocks = "".join(
        f"<p><strong>Q. {q}</strong><br>A. {a}</p>" for q, a in topic.get("faqs", [])
    )

    html = (
        f"<p>{topic['desc']}</p>"
        f"<p>▼ <strong>今すぐ無料でAI真贋・代筆チェックを試す（登録不要・1日3回無料）</strong><br>"
        f'<a href="{direct_tool_url}" target="_blank" rel="nofollow noopener">{direct_tool_url}</a></p>'
        f"<hr>"
        f"<h2>1. なぜ今「{topic['h1'][:22]}...」が問題になっているのか？</h2>"
        f"<p>{topic['body']}</p>"
        f"<h2>2. 3秒で見分けるAI生成・業者スクリプトの典型チェックリスト</h2>"
        f"<ul>{checklist_li}</ul>"
        f"<h2>3. よくある質問（FAQ）</h2>"
        f"{faq_blocks}"
        f"<hr>"
        f"<h2>4. 相手に言い逃れさせない「監査証明書PDF」と「追及・差し戻しテンプレート」</h2>"
        f"<p>『AI見抜きくん Pro』では、入力データを外部サーバーへ一切送信しないゼロトラスト設計（ブラウザ内完結）で以下の4大監査機能を提供しています。</p>"
        f"<ol>"
        f"<li><p><strong>文単位のAI根拠ハイライト</strong>（どの文がChatGPT構文かを色分け可視化）</p></li>"
        f"<li><p><strong>普段の本人文体との比較監査</strong>（過去のLINE・チャットと今回の文章の漢字率・平均文長のズレを証明）</p></li>"
        f"<li><p><strong>Word(.docx)の保存回数1回検知</strong>（一括コピペ納品の決定的証拠を取得）</p></li>"
        f"<li><p><strong>画像ELA（圧縮誤差ヒートマップ）＆EXIF検査</strong>（AI生成アイコン・加工出品画像を検出）</p></li>"
        f"</ol>"
        f"<p>▼ <strong>特設解説ページ＆無料診断ツールはこちら</strong><br>"
        f'<a href="{lp_url}" target="_blank" rel="nofollow noopener">{lp_url}</a></p>'
        f"<p>▼ <strong>全機能アンロック・専用返信テンプレ3選・監査証明書PDF出力が使える『7日間・徹底監査パス（¥980）』はこちら</strong><br>"
        f'<a href="{MAIN_PAID_NOTE_URL}" target="_blank" rel="nofollow noopener">{MAIN_PAID_NOTE_URL}</a></p>'
    )
    return html


def generate_local_note_packages() -> list:
    """全SEOトピックのnote投稿用HTML・Markdownパッケージを生成"""
    os.makedirs(NOTE_EXPORT_DIR, exist_ok=True)
    generated = []
    for idx, t in enumerate(seo.SEO_TOPICS, 1):
        html_body = build_note_html_for_topic(t)
        slug_base = t["slug"].replace(".html", "")
        out_file = os.path.join(NOTE_EXPORT_DIR, f"{idx:02d}_{slug_base}.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(
                f"<!-- Title: {t['h1']} -->\n"
                f"<!-- Hashtags: {' '.join(RECOMMENDED_HASHTAGS)} -->\n"
                f"{html_body}\n"
            )
        generated.append({"slug": slug_base, "title": t["h1"], "file": out_file, "html": html_body})
    return generated


def get_note_cookies_via_api_or_env() -> dict:
    """
    1. 環境変数 NOTE_SESSION_COOKIE (_note_session_v5 等) があればそれを使用
    2. 環境変数 NOTE_EMAIL / NOTE_PASSWORD があれば APIログインを試行
    """
    cookie_dict = {}
    raw_cookie = os.getenv("NOTE_SESSION_COOKIE", "").strip()
    if raw_cookie:
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
    except Exception as e:
        print(f"[note auth] direct sign_in exception: {e}")

    return {}


def post_or_draft_note_via_unofficial_api(cookies: dict, title: str, html_body: str, publish: bool = False) -> dict:
    """
    note非公式API (/api/v1/text_notes, /api/v1/text_notes/draft_save, /api/v2/notes/{key}/publish) を用いて記事を自動作成・保存
    """
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://note.com",
        "Referer": "https://note.com/notes/new",
        "X-Requested-With": "XMLHttpRequest",
    }
    if "XSRF-TOKEN" in cookies:
        headers["X-XSRF-TOKEN"] = cookies["XSRF-TOKEN"]

    create_payload = {
        "body": html_body,
        "name": title,
        "template_key": None,
    }
    resp = requests.post(
        "https://note.com/api/v1/text_notes",
        cookies=cookies,
        headers=headers,
        json=create_payload,
        timeout=15,
    )
    if resp.status_code not in (200, 201):
        return {"ok": False, "status": resp.status_code, "error": resp.text[:300]}

    res_data = resp.json().get("data", {})
    article_id = res_data.get("id")
    article_key = res_data.get("key")

    # 下書き更新 & ハッシュタグ付与
    update_payload = {
        "body": html_body,
        "name": title,
        "status": "published" if publish else "draft",
        "hashtags": RECOMMENDED_HASHTAGS,
    }
    upd_resp = requests.put(
        f"https://note.com/api/v1/text_notes/{article_id}",
        cookies=cookies,
        headers=headers,
        json=update_payload,
        timeout=15,
    )

    return {
        "ok": upd_resp.status_code in (200, 201),
        "id": article_id,
        "key": article_key,
        "url": f"https://note.com/safe_swift4998/n/{article_key}",
        "status": "published" if publish else "draft",
    }


def run_note_auto_syndication() -> dict:
    packages = generate_local_note_packages()
    cookies = get_note_cookies_via_api_or_env()

    if not cookies:
        return {
            "mode": "local_html_ready",
            "packages_count": len(packages),
            "api_authenticated": False,
            "message": f"note投稿用HTMLパッケージ 全{len(packages)}本を note_articles_ready/ に自動生成完了（NOTE_EMAIL/NOTE_PASSWORD または NOTE_SESSION_COOKIE 設定時に非公式API自動投稿が即時発火します）",
        }

    # 認証情報がある場合は未投稿のトピックを1日1本ずつ自動でnoteへ投稿
    published_log = {}
    if os.path.exists(NOTE_PUBLISHED_LOG):
        try:
            with open(NOTE_PUBLISHED_LOG, "r", encoding="utf-8") as f:
                published_log = json.load(f)
        except Exception:
            published_log = {}

    results = []
    for pkg in packages:
        if pkg["slug"] in published_log:
            continue
        res = post_or_draft_note_via_unofficial_api(
            cookies=cookies,
            title=pkg["title"],
            html_body=pkg["html"],
            publish=True,
        )
        results.append(res)
        if res.get("ok"):
            published_log[pkg["slug"]] = {
                "published_at": datetime.now().isoformat(),
                "key": res.get("key"),
                "url": res.get("url"),
            }
            with open(NOTE_PUBLISHED_LOG, "w", encoding="utf-8") as f:
                json.dump(published_log, f, ensure_ascii=False, indent=2)
        break  # レート制限・スパム判定回避のため1回の実行につき1記事ずつ安全に自動投稿

    return {
        "mode": "unofficial_api_live",
        "packages_count": len(packages),
        "api_authenticated": True,
        "results": results,
    }


if __name__ == "__main__":
    out = run_note_auto_syndication()
    print(json.dumps(out, ensure_ascii=False, indent=2))
