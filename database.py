import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "truthlens.db")

STRIPE_FEE_RATE = 0.036  # 3.6%
API_COST_PER_PAID_SCAN_YEN = 0.08  # Gemini 2.5 Flash ハイブリッド平均原価


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            mode TEXT NOT NULL,
            input_preview TEXT NOT NULL,
            ai_probability INTEGER NOT NULL,
            verdict_badge TEXT NOT NULL,
            result_json TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            plan_id TEXT NOT NULL,
            plan_name TEXT NOT NULL,
            amount_yen INTEGER NOT NULL,
            stripe_fee_yen INTEGER NOT NULL,
            estimated_api_cost_yen INTEGER NOT NULL,
            net_profit_yen INTEGER NOT NULL,
            channel TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            key TEXT PRIMARY KEY,
            val INTEGER NOT NULL
        )
        """
    )

    # 初期カウンター設定
    for k, default_v in [
        ("free_scans_total", 142),
        ("paywall_views", 64),
        ("share_clicks", 28),
    ]:
        cur.execute("INSERT OR IGNORE INTO metrics (key, val) VALUES (?, ?)", (k, default_v))

    # 初回起動時にリアルな初期トランザクションサンプルが0件ならシードを作成（いつでもリセット・追加可能）
    cur.execute("SELECT COUNT(*) as cnt FROM orders")
    if cur.fetchone()["cnt"] == 0:
        seed_orders = [
            ("2026-11-01 09:15:00", "pass_980", "7日間・徹底監査パス（買い切り）", 980, "X(Twitter) AI見抜き方診断シェア経由"),
            ("2026-11-01 12:40:00", "pass_980", "7日間・徹底監査パス（買い切り）", 980, "マッチングアプリLINE疑惑検索経由"),
            ("2026-11-01 16:05:00", "pro_1480", "Pro月額プラン（無制限＋証明書出力）", 1480, "クラウドソーシング発注者note記事経由"),
        ]
        for dt, pid, pname, amt, ch in seed_orders:
            fee = int(round(amt * STRIPE_FEE_RATE))
            api_cost = 4
            net = amt - fee - api_cost
            cur.execute(
                """
                INSERT INTO orders (created_at, plan_id, plan_name, amount_yen, stripe_fee_yen, estimated_api_cost_yen, net_profit_yen, channel)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (dt, pid, pname, amt, fee, api_cost, net, ch),
            )

    conn.commit()
    conn.close()


def record_scan(mode: str, input_preview: str, result: Dict[str, Any]) -> int:
    conn = get_conn()
    cur = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        """
        INSERT INTO scans (created_at, mode, input_preview, ai_probability, verdict_badge, result_json)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            now_str,
            mode,
            input_preview[:120],
            int(result.get("ai_probability", 50)),
            str(result.get("verdict_badge", "")),
            json.dumps(result, ensure_ascii=False),
        ),
    )
    scan_id = cur.lastrowid
    cur.execute("UPDATE metrics SET val = val + 1 WHERE key = 'free_scans_total'")
    conn.commit()
    conn.close()
    return int(scan_id or 0)


def increment_metric(key: str, amount: int = 1) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO metrics (key, val) VALUES (?, 0)", (key,))
    cur.execute("UPDATE metrics SET val = val + ? WHERE key = ?", (amount, key))
    conn.commit()
    conn.close()


def record_order(plan_id: str, channel: str = "アプリ内ペイウォール直課金") -> Dict[str, Any]:
    plan_catalog = {
        "pass_980": ("7日間・徹底監査パス（50回＋証明書出力）", 980, 4),
        "pro_1480": ("Pro月額プラン（無制限＋文体比較＋証明書）", 1480, 8),
        "biz_3980": ("ビジネス監査パック（外注・教育機関向け一括監査）", 3980, 18),
    }
    pname, amt, api_cost = plan_catalog.get(plan_id, plan_catalog["pass_980"])
    fee = int(round(amt * STRIPE_FEE_RATE))
    net = amt - fee - api_cost
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO orders (created_at, plan_id, plan_name, amount_yen, stripe_fee_yen, estimated_api_cost_yen, net_profit_yen, channel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (now_str, plan_id, pname, amt, fee, api_cost, net, channel),
    )
    conn.commit()
    conn.close()
    return get_revenue_dashboard()


def reset_orders(mode: str = "zero") -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders")
    if mode == "goal_reached":
        # 月利1万円突破シミュレーションデータを投入
        sample_plan = [
            ("pass_980", "X(Twitter) バズ投稿経由"),
            ("pass_980", "マッチングアプリLINE疑惑検索経由"),
            ("pro_1480", "外注ライター検収note記事経由"),
            ("pass_980", "アプリ内『文体乖離グラフ』ロック解除"),
            ("biz_3980", "採用・研修レポート監査法人導入"),
            ("pass_980", "フリマ出品画像真贋チェック経由"),
            ("pro_1480", "大学・専門学校レポートチェック経由"),
            ("pass_980", "アプリ内『確認メッセージテンプレ』解除"),
            ("pass_980", "X(Twitter) 診断結果カード経由"),
        ]
        conn.commit()
        conn.close()
        for pid, ch in sample_plan:
            record_order(pid, ch)
        return get_revenue_dashboard()
    conn.commit()
    conn.close()
    return get_revenue_dashboard()


def get_recent_scans(limit: int = 12) -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, created_at, mode, input_preview, ai_probability, verdict_badge FROM scans ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_revenue_dashboard() -> Dict[str, Any]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT key, val FROM metrics")
    metrics_map = {r["key"]: r["val"] for r in cur.fetchall()}
    conn.close()

    gross_revenue = sum(o["amount_yen"] for o in orders)
    total_fees = sum(o["stripe_fee_yen"] for o in orders)
    total_api_cost = sum(o["estimated_api_cost_yen"] for o in orders)
    net_profit = sum(o["net_profit_yen"] for o in orders)

    goal_yen = 10000
    remaining_yen = max(goal_yen - net_profit, 0)
    progress_pct = round(min(net_profit / goal_yen * 100.0, 100.0), 1)
    passes_needed = int((remaining_yen + 940) // 941) if remaining_yen > 0 else 0

    free_scans = max(metrics_map.get("free_scans_total", 1), 1)
    paywall_views = max(metrics_map.get("paywall_views", 1), 1)
    paid_count = len(orders)

    return {
        "goal_profit_yen": goal_yen,
        "gross_revenue_yen": gross_revenue,
        "stripe_fees_yen": total_fees,
        "api_cost_yen": total_api_cost,
        "fixed_server_cost_yen": 0,
        "net_profit_yen": net_profit,
        "remaining_to_goal_yen": remaining_yen,
        "progress_pct": progress_pct,
        "passes_980_needed": passes_needed,
        "paid_orders_count": paid_count,
        "free_scans_total": free_scans,
        "paywall_views": paywall_views,
        "conversion_rate_pct": round(paid_count / free_scans * 100.0, 2),
        "orders": orders[:20],
    }
