import base64
import io
import json
import mimetypes
import os
import re
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

import analyzer
import database

PORT = int(os.environ.get("PORT", "8080"))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# 外部決済プラットフォームURL（Stripe Payment Links / note有料記事 / PayPay決済リンク等）
PAYMENT_CONFIG = {
    "stripe_pass_980_url": os.environ.get("STRIPE_PASS_980_URL", ""),
    "stripe_pro_1480_url": os.environ.get("STRIPE_PRO_1480_URL", ""),
    "stripe_biz_3980_url": os.environ.get("STRIPE_BIZ_3980_URL", ""),
    "note_article_url": os.environ.get("NOTE_ARTICLE_URL", ""),
}

VALID_LICENSE_CODES = {
    "MINUKI-980-PASS": ("pass_980", "note/BOOTH シリアルコード認証（980円パス）"),
    "MINUKI-1480-PRO": ("pro_1480", "Proプラン シリアルコード認証"),
    "MINUKI-3980-BIZ": ("biz_3980", "法人パック シリアルコード認証"),
}


def create_demo_image_bytes(kind: str) -> bytes:
    """ワンクリック検証用のテスト画像（AIメタデータ埋め込み画像 or 撮影レポート風画像）を動的生成"""
    if kind == "ai_art":
        import numpy as np

        y, x = np.ogrid[:1024, :1024]
        r = np.clip((x * 0.22 + y * 0.05), 20, 240).astype(np.uint8)
        g = np.clip((x * 0.02 + y * 0.20 + 40), 30, 220).astype(np.uint8)
        b = np.clip(220 - (x * 0.12 + y * 0.12), 40, 250).astype(np.uint8)
        arr = np.stack([r, g, b], axis=2)
        img = Image.fromarray(arr, mode="RGB")
        draw = ImageDraw.Draw(img)
        draw.ellipse((280, 240, 744, 780), fill=(245, 222, 205), outline=(255, 255, 255), width=4)

        meta = PngInfo()
        meta.add_text(
            "parameters",
            "masterpiece, ultra-detailed portrait, photorealistic, japanese woman, 8k\nSteps: 28, Sampler: DPM++ 2M Karras, CFG scale: 7.0, Model: sd_xl_base_1.0",
        )
        buf = io.BytesIO()
        img.save(buf, format="PNG", pnginfo=meta)
        return buf.getvalue()
    else:
        img = Image.new("RGB", (900, 1200), color=(248, 247, 242))
        draw = ImageDraw.Draw(img)
        draw.rectangle((60, 60, 840, 1140), outline=(210, 210, 210), width=2)
        y_pos = 110
        for line_idx in range(22):
            line_w = 720 if line_idx % 5 != 4 else 460
            draw.rectangle((100, y_pos, 100 + line_w, y_pos + 14), fill=(55, 55, 60))
            y_pos += 42
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=92)
        return buf.getvalue()


def create_demo_docx_bytes() -> bytes:
    """クラウドワークス納品記事・大学レポート風のデモWordファイル（リビジョン1回＝コピペ保存）を生成"""
    import docx

    doc = docx.Document()
    doc.core_properties.author = "CrowdWorks_Writer_Sample"
    doc.core_properties.revision = 1
    doc.add_heading("AI時代におけるWebマーケティングの重要性と今後の展望について", level=1)
    paragraphs = [
        "現代のビジネス環境において、デジタルマーケティングの活用は企業の持続的な成長において重要な役割を果たしています。本稿では、その具体的なメリットとデメリットについて徹底解説していきます。",
        "まず第一に、ターゲット層への精密なアプローチが可能であるという点が挙げられます。従来のマス広告と比較して、少額の予算から高い費用対効果を実現することが可能です。",
        "第二に、データ分析に基づく迅速な改善サイクルを回せる点が不可欠となっています。リアルタイムで顧客の反応を計測できるため、施策の最適化が多岐にわたり容易になります。",
        "一方で、競争の激化による広告単価の高騰や、専門知識を持った人材の不足も課題として存在します。そのため、社内の体制構築と外部パートナーの活用をバランスよく検討する必要があります。",
        "総じて、適切な戦略設計と継続的な改善を行うことが成功への鍵と言えるでしょう。いかがでしたでしょうか。本記事が貴社のマーケティング施策の一助となれば幸いです。",
    ]
    for p in paragraphs:
        doc.add_paragraph(p)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


class TruthLensRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/dashboard":
            data = database.get_revenue_dashboard()
            data["recent_scans"] = database.get_recent_scans(10)
            data["payment_config"] = PAYMENT_CONFIG
            self._send_json(data)
            return

        if path == "/api/demo-image":
            qs = parse_qs(parsed.query)
            kind = qs.get("kind", ["ai_art"])[0]
            img_bytes = create_demo_image_bytes(kind)
            b64 = base64.b64encode(img_bytes).decode("ascii")
            mime = "image/png" if kind == "ai_art" else "image/jpeg"
            fname = "mercari_icon_sdxl.png" if kind == "ai_art" else "report_camera_photo.jpg"
            self._send_json(
                {
                    "filename": fname,
                    "mime": mime,
                    "data_url": f"data:{mime};base64,{b64}",
                }
            )
            return

        if path == "/api/demo-docx":
            docx_bytes = create_demo_docx_bytes()
            b64 = base64.b64encode(docx_bytes).decode("ascii")
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            self._send_json(
                {
                    "filename": "外注納品記事_AIコピペ検証用サンプル.docx",
                    "mime": mime,
                    "data_url": f"data:{mime};base64,{b64}",
                }
            )
            return

        # 静的ファイルの配信
        if path in ("/", "", "/tokushoho", "/privacy", "/lp/matching", "/lp/crowdworks", "/lp/report"):
            file_path = os.path.join(STATIC_DIR, "index.html")
        else:
            rel_path = path.lstrip("/").replace("/", os.sep)
            file_path = os.path.join(STATIC_DIR, rel_path)

        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or "application/octet-stream"
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header(
                "Content-Type",
                f"{mime_type}; charset=utf-8"
                if mime_type.startswith("text/") or mime_type in ("application/javascript", "application/json", "application/xml")
                else mime_type,
            )
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            body = self._read_json_body()

            if path == "/api/analyze/text":
                text = body.get("text", "")
                mode = body.get("mode", "messenger")
                reference_text = body.get("reference_text", "")
                api_key = body.get("api_key", "")

                res = analyzer.analyze_text(
                    text=text,
                    mode=mode,
                    reference_text=reference_text,
                    api_key=api_key,
                )
                if "error" in res:
                    self._send_json(res, status=400)
                    return

                scan_id = database.record_scan(mode, text[:80], res)
                res["scan_id"] = scan_id
                self._send_json(res)
                return

            if path == "/api/analyze/image":
                data_url = body.get("image_base64", "")
                filename = body.get("filename", "upload.png")
                mode = body.get("mode", "image_forensics")
                api_key = body.get("api_key", "")

                if "," in data_url:
                    _, b64_part = data_url.split(",", 1)
                else:
                    b64_part = data_url

                img_bytes = base64.b64decode(b64_part)
                res = analyzer.analyze_image(
                    image_bytes=img_bytes,
                    filename=filename,
                    mode=mode,
                    api_key=api_key,
                )
                if "error" in res:
                    self._send_json(res, status=400)
                    return

                scan_id = database.record_scan(mode, f"[画像] {filename}", res)
                res["scan_id"] = scan_id
                self._send_json(res)
                return

            if path == "/api/analyze/document":
                data_url = body.get("file_base64", "")
                filename = body.get("filename", "report.pdf")
                api_key = body.get("api_key", "")

                if "," in data_url:
                    _, b64_part = data_url.split(",", 1)
                else:
                    b64_part = data_url

                file_bytes = base64.b64decode(b64_part)
                res = analyzer.analyze_document_file(
                    file_bytes=file_bytes,
                    filename=filename,
                    api_key=api_key,
                )
                if "error" in res:
                    self._send_json(res, status=400)
                    return

                scan_id = database.record_scan("document", f"[書類] {filename}", res)
                res["scan_id"] = scan_id
                self._send_json(res)
                return

            if path == "/api/verify-license":
                code = (body.get("code") or "").strip().upper()
                if code in VALID_LICENSE_CODES:
                    plan_id, channel = VALID_LICENSE_CODES[code]
                    dash = database.record_order(plan_id, channel)
                    self._send_json({"ok": True, "plan_id": plan_id, "dashboard": dash})
                    return
                if re.match(r"^AI-2026-[A-Z0-9]{4}$", code):
                    dash = database.record_order("pass_980", f"シリアルコード認証 ({code})")
                    self._send_json({"ok": True, "plan_id": "pass_980", "dashboard": dash})
                    return
                self._send_json(
                    {"ok": False, "error": "無効なシリアルコードです。購入完了メールまたはnote有料エリアに記載されたコードをご確認ください。"},
                    status=400,
                )
                return

            if path == "/api/payment-config":
                for k in ("stripe_pass_980_url", "stripe_pro_1480_url", "stripe_biz_3980_url", "note_article_url"):
                    if k in body:
                        PAYMENT_CONFIG[k] = str(body[k]).strip()
                self._send_json({"ok": True, "payment_config": PAYMENT_CONFIG})
                return

            if path == "/api/order/simulate":
                action = body.get("action", "buy")
                if action == "reset":
                    reset_mode = body.get("reset_mode", "zero")
                    dash = database.reset_orders(reset_mode)
                else:
                    plan_id = body.get("plan_id", "pass_980")
                    channel = body.get("channel", "アプリ内ペイウォール直課金")
                    dash = database.record_order(plan_id, channel)
                self._send_json(dash)
                return

            if path == "/api/metric":
                key = body.get("key", "paywall_views")
                database.increment_metric(key, 1)
                self._send_json({"ok": True})
                return

            self._send_json({"error": "Unknown endpoint"}, status=404)

        except Exception as e:
            traceback.print_exc()
            self._send_json({"error": f"サーバー処理エラー: {str(e)}"}, status=500)


def run_server() -> None:
    database.init_db()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), TruthLensRequestHandler)
    print(f"AI見抜きくん Pro Server running at http://127.0.0.1:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
