import json
import os
import time
import urllib.parse
from datetime import datetime

import requests
from dotenv import load_dotenv

import auto_seo_publisher as seo

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NOTE_EXPORT_DIR = os.path.join(ROOT_DIR, "note_articles_ready")
NOTE_PUBLISHED_LOG = os.path.join(ROOT_DIR, "note_published_log.json")
NOTE_ENGAGED_LOG = os.path.join(ROOT_DIR, "note_engaged_log.json")
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

# 能動的エンゲージメント（スキ回り）対象キーワード群
OUTREACH_SEARCH_QUERIES = [
    "#クラウドワークス",
    "#Webライター",
    "#マッチングアプリ",
    "#ペアーズ",
    "#ガクチカ",
    "#就活",
    "#ChatGPT",
    "#SEO記事",
]


def build_note_html_for_topic(topic: dict) -> str:
    """noteのエディタ仕様（p / h2 / ul / ol / hr / a のみ有効）に完全準拠した記事HTMLを生成"""
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
    """全SEOトピックのnote投稿用HTMLパッケージを生成"""
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
        generated.append({"slug": slug_base, "title": t["h1"], "file": out_file, "html": html_body, "kw": t.get("kw", "")})
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


def post_and_publish_note_article(cookies: dict, title: str, html_body: str, tags: list = None) -> dict:
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
    r_pub = requests.put(
        f"https://note.com/api/v1/text_notes/{article_id}",
        cookies=cookies,
        headers=headers,
        json={
            "body": html_body,
            "free_body": html_body,
            "name": title,
            "status": "published",
            "hashtags": use_tags,
            "price": 0,
            "send_notifications_flag": True,
        },
        timeout=15,
    )

    return {
        "ok": r_pub.status_code in (200, 201),
        "id": article_id,
        "key": article_key,
        "url": f"https://note.com/safe_swift4998/n/{article_key}",
        "status_code": r_pub.status_code,
    }


def run_proactive_target_engagement(cookies: dict, max_likes_per_run: int = 8) -> dict:
    """
    ターゲット層（#クラウドワークス, #マッチングアプリ, #ガクチカ, #Webライター 等）の最新記事を検索し、
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
                    time.sleep(1.8)
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


def run_note_auto_syndication(max_posts_per_run: int = 2, max_likes_per_run: int = 8) -> dict:
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

    results = []
    posted_count = 0
    for pkg in packages:
        if pkg["slug"] in published_log:
            continue
        res = post_and_publish_note_article(
            cookies=cookies,
            title=pkg["title"],
            html_body=pkg["html"],
        )
        results.append(res)
        if res.get("ok"):
            published_log[pkg["slug"]] = {
                "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "id": res.get("id"),
                "key": res.get("key"),
                "title": pkg["title"],
                "url": res.get("url"),
            }
            with open(NOTE_PUBLISHED_LOG, "w", encoding="utf-8") as f:
                json.dump(published_log, f, ensure_ascii=False, indent=2)
            posted_count += 1
            if posted_count >= max_posts_per_run:
                break
            time.sleep(2.5)
        else:
            break

    # 能動的アウトリーチ（スキ回り）の実行
    outreach_res = run_proactive_target_engagement(cookies, max_likes_per_run=max_likes_per_run)

    return {
        "mode": "unofficial_api_live",
        "packages_count": len(packages),
        "published_total": len(published_log),
        "newly_published": posted_count,
        "api_authenticated": True,
        "results": results,
        "outreach": outreach_res,
        "message": f"note自動投稿稼働中（累計公開済: {len(published_log)}本 / 今回新規公開: {posted_count}本 / ターゲット見込み客への能動スキ営業: {outreach_res.get('liked_count', 0)}件完了・累計{outreach_res.get('total_engaged_cumulative', 0)}件）",
    }


if __name__ == "__main__":
    out = run_note_auto_syndication(max_posts_per_run=2, max_likes_per_run=8)
    print(json.dumps(out, ensure_ascii=False, indent=2))
