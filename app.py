import base64
import hashlib
import io
import json
import mimetypes
import os
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

import analyzer
import database

PORT = int(os.environ.get("PORT", "8080"))
# ローカルPC実行時は外部からのアクセスを完全遮断するため 127.0.0.1 のみにバインド（クラウドコンテナ環境のみ 0.0.0.0）
BIND_HOST = "0.0.0.0" if os.environ.get("CLOUD_CONTAINER") == "1" else "127.0.0.1"
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

LICENSE_SALT = "MINUKI_SALT_2026_JP#"

# 平文のシリアルコードをソースコード内に保持せず、ソルト付きSHA-256ハッシュ値のみで照合
VALID_LICENSE_HASHES = {
    "96ed3b24dcbfa81c18504db99d02b45e6f86d76e650c287c60ab0c5739d905de": ("pass_980", "シリアルコード認証（980円パス）"),
    "992af19703ea5c7fe08d225a227040ca0baab7603077897bd55fbcf8401ac678": ("pro_1480", "Proプラン シリアルコード認証"),
    "468f3568f6c56524d53a6eba46f5923aa244822e6959791afd5f576a6aeacf25": ("biz_3980", "法人パック シリアルコード認証"),
    "5f1012ab89c3544e32e901b7248691f16f0e752bf1b4af5e34c5e383480c25c0": ("pass_980", "個別発行シリアルコード認証 #1"),
    "a260d78beb8f7f306bd14d0d129a96ef48ff3dd03b15daa063f4271daa466e06": ("pass_980", "個別発行シリアルコード認証 #2"),
    "2f966cff15668df267453cd8fd7602f6c78f64425775c871ad0987b14f4439bc": ("pass_980", "個別発行シリアルコード認証 #3"),
    "0b74516e5e92a7f33b57d187278c076228b939150ac74d3dbb5487f58952bab5": ("pass_980", "個別発行シリアルコード認証 #4"),
    "6958bcb68945dfd363643f7ddf62c59e3aed250821bc51319f52bb06c11d05d0": ("pass_980", "個別発行シリアルコード認証 #5"),
}


def hash_license_code(code: str) -> str:
    return hashlib.sha256((LICENSE_SALT + code.strip().upper()).encode("utf-8")).hexdigest()


def create_demo_image_bytes(kind: str) -> bytes:
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

    def _add_security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self' https://generativelanguage.googleapis.com; frame-ancestors 'none';",
        )

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._add_security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 15 * 1024 * 1024:  # 15MB上限（DoS防御）
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/dashboard":
            data = database.get_revenue_dashboard()
            data["recent_scans"] = database.get_recent_scans(10)
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

        # ディレクトリトラバーサル完全防止
        if path in ("/", "", "/tokushoho", "/privacy"):
            file_path = os.path.join(STATIC_DIR, "index.html")
        else:
            safe_name = os.path.basename(path.lstrip("/"))
            file_path = os.path.join(STATIC_DIR, safe_name)

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
            self._add_security_headers()
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
                text = body.get("text", "")[:20000]
                mode = body.get("mode", "messenger")
                reference_text = body.get("reference_text", "")[:20000]
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
                self._send_json(res)
                return

            if path == "/api/analyze/image":
                data_url = body.get("image_base64", "")
                filename = os.path.basename(body.get("filename", "upload.png"))
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
                self._send_json(res)
                return

            if path == "/api/analyze/document":
                data_url = body.get("file_base64", "")
                filename = os.path.basename(body.get("filename", "report.pdf"))
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
                self._send_json(res)
                return

            if path == "/api/verify-license":
                code = (body.get("code") or "").strip().upper()
                digest = hash_license_code(code)
                if digest in VALID_LICENSE_HASHES:
                    plan_id, channel = VALID_LICENSE_HASHES[digest]
                    dash = database.record_order(plan_id, channel)
                    self._send_json({"ok": True, "plan_id": plan_id, "dashboard": dash})
                    return
                self._send_json(
                    {"ok": False, "error": "無効なシリアルコードです。購入完了ページに記載されたコードをご確認ください。"},
                    status=400,
                )
                return

            if path == "/api/order/simulate":
                action = body.get("action", "buy")
                if action == "reset":
                    reset_mode = body.get("reset_mode", "zero")
                    dash = database.reset_orders(reset_mode)
                else:
                    plan_id = body.get("plan_id", "pass_980")
                    channel = body.get("channel", "アプリ内課金")
                    dash = database.record_order(plan_id, channel)
                self._send_json(dash)
                return

            if path == "/api/metric":
                key = body.get("key", "paywall_views")
                if key in ("paywall_views", "share_clicks", "free_scans_total"):
                    database.increment_metric(key, 1)
                self._send_json({"ok": True})
                return

            self._send_json({"error": "Unknown endpoint"}, status=404)

        except Exception:
            self._send_json({"error": "リクエスト処理中にエラーが発生しました。"}, status=500)


def run_server() -> None:
    database.init_db()
    server = ThreadingHTTPServer((BIND_HOST, PORT), TruthLensRequestHandler)
    print(f"AI見抜きくん Pro Server running on {BIND_HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
