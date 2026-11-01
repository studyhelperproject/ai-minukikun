import os
import re
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def set_url(checkout_url: str) -> None:
    if not checkout_url.startswith("https://"):
        print("エラー: https:// から始まる決済URL（Stripe Payment Link または note記事URL）を指定してください。")
        sys.exit(1)

    for folder in ("static", "docs"):
        js_path = os.path.join(ROOT_DIR, folder, "app.js")
        if not os.path.exists(js_path):
            continue
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()

        replacement = f'''const DEFAULT_PAYMENT_URLS = {{
  pass_980: "{checkout_url}",
  pro_1480: "{checkout_url}",
  biz_3980: "{checkout_url}",
}};'''
        content = re.sub(
            r"const DEFAULT_PAYMENT_URLS = \{[\s\S]*?\};",
            replacement,
            content,
            count=1,
        )
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated payment URL in {js_path}")

    subprocess.run(["git", "add", "static/app.js", "docs/app.js"], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "Update live checkout URL"], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=ROOT_DIR, check=True)
    print("完了: 本番クラウド (https://studyhelperproject.github.io/ai-minukikun/) に決済URLを反映しました！")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python set_payment_url.py <https://note.com/... または https://buy.stripe.com/...>")
        sys.exit(1)
    set_url(sys.argv[1].strip())
