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
THREADS_QUEUE_PATH = os.path.join(ROOT_DIR, "threads_posts_ready.json")
THREADS_PUBLISHED_LOG = os.path.join(ROOT_DIR, "threads_published_log.json")
APP_URL = "https://studyhelperproject.github.io/ai-minukikun/"
MAIN_PAID_NOTE_URL = "https://note.com/safe_swift4998/n/na1af72c84723"


def _build_threads_text_for_topic(topic: dict) -> str:
    """トピックからThreads向け500文字以内の問題提起フック投稿文を生成"""
    slug = topic.get("slug", "")
    h1 = topic.get("h1", "")
    checklist = topic.get("checklist", [])
    point1 = checklist[0] if checklist else topic.get("desc", "")
    point2 = checklist[1] if len(checklist) > 1 else ""
    cta_query = f"?tab={topic.get('cta_tab', 'messenger')}&sample={topic.get('sample_key', 'scam_dm')}"
    tool_url = f"{APP_URL}{cta_query}"

    if slug == "topic-zh-japanese-ai-audit.html":
        header = "⚠️ 日本亚马逊跨境电商・游戏出海团队注意：如何识破外包日文写手用ChatGPT/DeepL敷衍交稿？\n\n"
        body = (
            f"✅ 关键特征：\n・{point1[:90]}\n"
            + (f"・{point2[:75]}\n" if point2 else "")
            + "\n🔍 无需懂日语，3秒免费检测Word保存1次铁证👇\n"
        )
        footer = f"{APP_URL}topic-zh-japanese-ai-audit.html\n\n#跨境电商 #日语翻译"
    elif slug == "topic-en-japanese-ai-audit.html":
        header = "⚠️ Outsourcing Japanese articles or game localization? Spot ChatGPT/DeepL copy-paste in 3 seconds.\n\n"
        body = (
            f"✅ Red Flags:\n• {point1[:95]}\n"
            + (f"• {point2[:80]}\n" if point2 else "")
            + "\n🔍 Zero-trust browser detector (no Japanese fluency needed)👇\n"
        )
        footer = f"{APP_URL}topic-en-japanese-ai-audit.html\n\n#Localization #Japan"
    else:
        header = f"【3秒AI見抜きチェック】{h1[:68]}\n\n"
        body = (
            "こんな特徴があればChatGPT丸投げ・業者の可能性大👇\n"
            f"・{point1[:85]}\n"
            + (f"・{point2[:70]}\n" if point2 else "")
            + "\n🔒 登録不要・端末内解析で今すぐチェック：\n"
        )
        tags = "#AI見抜きくん #ChatGPT"
        if any(k in slug for k in ("crowdworks", "lancers", "youtube", "tiktok", "kindle", "seo", "pr-", "translation")):
            tags = "#Webライター #クラウドワークス"
        elif any(k in slug for k in ("pairs", "konkatsu", "romance", "openchat", "instagram", "giveaway")):
            tags = "#マッチングアプリ #詐欺対策"
        elif any(k in slug for k in ("gakuchika", "univ", "book", "scholarship", "nursing", "civil", "programming")):
            tags = "#就活 #ガクチカ"
        footer = f"{tool_url}\n{tags}"

    full = header + body + footer
    if len(full) <= 495:
        return full

    # 500文字上限超過時はpoint2を削るなどして必ずURLとハッシュタグを残す
    compact_body = (
        f"・{point1[:75]}\n\n🔍 3秒チェック👇\n"
        if not slug.startswith("topic-en-")
        else f"• {point1[:80]}\n\n🔍 Check here👇\n"
    )
    compact = header + compact_body + footer
    if len(compact) <= 495:
        return compact

    max_head_len = max(20, 480 - len(compact_body) - len(footer) - 5)
    return header[:max_head_len] + "...\n\n" + compact_body + footer


def generate_threads_post_queue(topics: list = None) -> list:
    """全SEOトピックのThreads投稿キュー（500文字以内）を生成し threads_posts_ready.json に保存"""
    if topics is None:
        topics = list(seo.SEO_TOPICS)
        if len(topics) <= 20:
            try:
                import daily_pdca_engine as pdca_mod

                existing = {t["slug"] for t in topics}
                for cand in pdca_mod.EXPANSION_POOL:
                    if cand["slug"] not in existing:
                        topics.append(cand)
                        existing.add(cand["slug"])
            except Exception:
                pass

    queue = []
    for idx, t in enumerate(topics, 1):
        slug_base = t["slug"].replace(".html", "")
        text = _build_threads_text_for_topic(t)
        queue.append(
            {
                "index": idx,
                "slug": slug_base,
                "title": t.get("h1", ""),
                "char_count": len(text),
                "text": text,
                "target_url": f"{APP_URL}{t['slug']}",
                "checkout_url": MAIN_PAID_NOTE_URL,
            }
        )

    with open(THREADS_QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

    return queue


def _parse_threads_cookie_str(raw_cookie: str) -> dict:
    cookies = {}
    raw = (raw_cookie or "").strip()
    if not raw:
        return cookies
    if "=" not in raw:
        cookies["sessionid"] = raw
        return cookies
    for part in raw.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            if k.strip():
                cookies[k.strip()] = v.strip()
    return cookies


def has_threads_auth() -> dict:
    access_token = os.getenv("THREADS_ACCESS_TOKEN", "").strip()
    user_id = os.getenv("THREADS_USER_ID", "").strip()
    raw_cookie = os.getenv("THREADS_SESSION_COOKIE", "").strip()
    if access_token and user_id:
        return {"configured": True, "auth_type": "official_api"}
    if raw_cookie:
        cookies = _parse_threads_cookie_str(raw_cookie)
        if cookies.get("sessionid"):
            return {"configured": True, "auth_type": "session_cookie"}
    return {"configured": False, "auth_type": None}


def post_to_threads(post_text: str) -> dict:
    """
    Meta公式Threads API（方式A）またはブラウザセッションCookie API（方式B）でThreadsへ投稿
    """
    text = post_text[:495]
    access_token = os.getenv("THREADS_ACCESS_TOKEN", "").strip()
    user_id = os.getenv("THREADS_USER_ID", "").strip()

    # 方式A: Meta公式 Threads Publishing API
    if access_token and user_id:
        try:
            r_create = requests.post(
                f"https://graph.threads.net/v1.0/{user_id}/threads",
                data={
                    "media_type": "TEXT",
                    "text": text,
                    "access_token": access_token,
                },
                timeout=15,
            )
            if r_create.status_code not in (200, 201):
                return {"ok": False, "method": "official_api", "step": "create", "status": r_create.status_code, "error": r_create.text[:250]}
            creation_id = r_create.json().get("id")
            if not creation_id:
                return {"ok": False, "method": "official_api", "step": "no_creation_id", "error": r_create.text[:250]}

            r_pub = requests.post(
                f"https://graph.threads.net/v1.0/{user_id}/threads_publish",
                data={
                    "creation_id": creation_id,
                    "access_token": access_token,
                },
                timeout=15,
            )
            if r_pub.status_code in (200, 201):
                return {"ok": True, "method": "official_api", "post_id": r_pub.json().get("id"), "status_code": r_pub.status_code}
            return {"ok": False, "method": "official_api", "step": "publish", "status": r_pub.status_code, "error": r_pub.text[:250]}
        except Exception as e:
            return {"ok": False, "method": "official_api", "error": str(e)}

    # 方式B: WebセッションCookie API (threads.net configure_text_only_post)
    raw_cookie = os.getenv("THREADS_SESSION_COOKIE", "").strip()
    cookies = _parse_threads_cookie_str(raw_cookie)
    if not cookies.get("sessionid"):
        return {"ok": False, "method": "none", "error": "THREADS_ACCESS_TOKEN or THREADS_SESSION_COOKIE not configured"}

    csrf_token = cookies.get("csrftoken", "")
    ds_user_id = cookies.get("ds_user_id", "")
    if not ds_user_id and "%3A" in cookies["sessionid"]:
        ds_user_id = cookies["sessionid"].split("%3A", 1)[0]
    elif not ds_user_id and ":" in cookies["sessionid"]:
        ds_user_id = cookies["sessionid"].split(":", 1)[0]

    upload_id = str(int(time.time() * 1000))
    payload_dict = {
        "text_post_app_info": json.dumps({"reply_control": 0}),
        "timezone_offset": "32400",
        "source_type": "4",
        "caption": text,
        "upload_id": upload_id,
        "publish_mode": "text_post",
    }
    if ds_user_id:
        payload_dict["_uid"] = ds_user_id

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-IG-App-ID": "238260118697367",
        "X-CSRFToken": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.threads.net",
        "Referer": "https://www.threads.net/",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        signed_body = f"SIGNATURE.{json.dumps(payload_dict, ensure_ascii=False)}"
        r_web = requests.post(
            "https://www.threads.net/api/v1/media/configure_text_only_post/",
            cookies=cookies,
            headers=headers,
            data={"signed_body": signed_body},
            timeout=15,
        )
        if r_web.status_code in (200, 201):
            resp_json = r_web.json()
            media = resp_json.get("media", {})
            return {
                "ok": resp_json.get("status") == "ok" or bool(media.get("pk")),
                "method": "session_cookie",
                "post_id": media.get("pk") or media.get("id"),
                "code": media.get("code"),
                "status_code": r_web.status_code,
            }
        return {"ok": False, "method": "session_cookie", "status_code": r_web.status_code, "error": r_web.text[:250]}
    except Exception as e:
        return {"ok": False, "method": "session_cookie", "error": str(e)}


def run_threads_auto_syndication(max_posts_per_run: int = 1, topics: list = None) -> dict:
    queue = generate_threads_post_queue(topics=topics)

    published_log = {}
    if os.path.exists(THREADS_PUBLISHED_LOG):
        try:
            with open(THREADS_PUBLISHED_LOG, "r", encoding="utf-8") as f:
                published_log = json.load(f)
        except Exception:
            published_log = {}

    auth = has_threads_auth()
    if not auth["configured"]:
        return {
            "mode": "queue_ready_awaiting_auth",
            "api_authenticated": False,
            "queued_total": len(queue),
            "published_total": len(published_log),
            "newly_published": 0,
            "message": f"Threads認証待ち（投稿キュー全{len(queue)}本生成済 / 公開済 {len(published_log)}本・THREADS_SESSION_COOKIE または Meta公式API設定待ち）",
        }

    results = []
    posted_count = 0
    for item in queue:
        if item["slug"] in published_log:
            continue
        res = post_to_threads(item["text"])
        results.append({"slug": item["slug"], **res})
        if res.get("ok"):
            published_log[item["slug"]] = {
                "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "method": res.get("method"),
                "post_id": res.get("post_id"),
                "code": res.get("code"),
                "title": item["title"],
            }
            with open(THREADS_PUBLISHED_LOG, "w", encoding="utf-8") as f:
                json.dump(published_log, f, ensure_ascii=False, indent=2)
            posted_count += 1
            if posted_count >= max_posts_per_run:
                break
            time.sleep(2.0)
        else:
            break

    return {
        "mode": f"threads_{auth['auth_type']}_live",
        "api_authenticated": True,
        "queued_total": len(queue),
        "published_total": len(published_log),
        "newly_published": posted_count,
        "results": results,
        "message": f"Threads自動投稿稼働中（公開済: {len(published_log)}本 / 今回新規: {posted_count}本 / キュー全{len(queue)}本）",
    }


if __name__ == "__main__":
    out = run_threads_auto_syndication(max_posts_per_run=1)
    print(json.dumps(out, ensure_ascii=False, indent=2))
