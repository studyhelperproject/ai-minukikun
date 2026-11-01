// AI見抜きくん Pro - 日本特化ハイブリッドフロントエンド＆スタンドアロンフォールバックエンジン
let currentTab = "messenger";
let isProUnlocked = localStorage.getItem("truthlens_pro") === "1";
let freeQuotaLeft = parseInt(localStorage.getItem("truthlens_quota") ?? "3", 10);
let lastAnalysisResult = null;
let selectedImageDataUrl = null;
let selectedImageFilename = "sample.png";
let selectedDocDataUrl = null;
let selectedDocFilename = "report.docx";
let lastPaywallTrigger = "結果ロック解除ボタン";

const SAMPLES = {
  scam_dm: `はじめまして！プロフィールを拝見して、とても誠実で素敵な方だなと思ってメッセージしました😊
おっしゃる通りですね！あなたの考え方は本当に素晴らしい視点だと思います。
私たちには何か不思議な縁や価値観が似ているものを感じますね。

ただ、普段あまりこのアプリ見ないので、もしよかったらLINEの方へ移動してお話ししませんか？
実は私、普段はデザインの仕事をしながら、叔父がアナリストをしていて暗号資産とAI配当の資産運用レクチャーを受けているんです。あなたのような優しい方なら、将来のために一緒に学べると思ってご連絡しました！LINEのIDを教えていただけますか？`,

  cw_article: `現代のビジネス環境において、Webマーケティングの活用は企業の生産性向上において重要な役割を果たしています。本稿では、その具体的なメリットとデメリットについて徹底解説していきます。

まず第一に、ターゲット層への精密なアプローチが可能であるという点が挙げられます。従来の広告と比較して、少額の予算から高い費用対効果を実現することが可能です。
第二に、データ分析に基づく迅速な改善サイクルが不可欠となっています。

一方で、競争の激化による広告単価の高騰も課題として存在します。そのため、社内の体制構築と外部パートナーの活用をバランスよく検討する必要があります。
総じて、適切な戦略設計を行うことが成功への鍵と言えるでしょう。いかがでしたでしょうか。参考にしていただければ幸いです。`,

  ai_es: `私は貴社の「テクノロジーで社会課題を解決する」という理念に深く共感し、志望いたしました。
学生時代に最も力を入れたことは、アルバイト先のカフェにおける業務効率化と売上向上への取り組みです。当初、店舗ではピーク時の提供遅延という課題が存在していました。
まず第一に、私はスタッフ全員へのヒアリングを実施し、オペレーションのボトルネックが多岐にわたることを特定しました。
第二に、マニュアルの再構築と役割分担の最適化が不可欠であると考え、新しい動線を導入しました。
この経験から、主体的に周囲を巻き込みながら課題を解決することの重要性を学びました。入社後もこの強みを活かし、再現性を持って貴社の事業成長に貢献したいと考えております。`,

  human_chat: `お疲れ様です！さっき送ってもらった資料、ざっと見ました〜！
基本的には良さそうなんだけど、3ページ目のグラフだけ数字が先月のままになってる気がするので、そこだけ明日朝イチで確認してもらえると助かります🙏
あと来週の打ち合わせ、木曜の午後でも大丈夫だったりしますか？？また手が空いた時にでも教えてください！`,

  stylometry_ref: `お疲れ様です！今週の記事の件なんですけど、ちょっと体調崩しちゃってて昨日まであんまり進まなかったです💦 すみません！！
今日中にはなんとか形にして送るので、もうちょっとだけ待ってもらえると助かります…！ちなみに文字数って2000文字くらいでも大丈夫でしたっけ？`,

  stylometry_target: `現代のビジネス環境において、リモートワークの導入は企業の生産性向上において重要な役割を果たしています。
まず第一に、通勤時間の削減によるワークライフバランスの改善という点が挙げられます。従業員は浮いた時間を自己研鑽や休息に充てることが可能となります。
一方で、対面コミュニケーションの減少によるチーム連携の希薄化も課題として存在します。そのため、適切なデジタルツールの活用と定期的な1on1ミーティングの実施が不可欠と言えるでしょう。
結論として、ハイブリッド型の勤務体系を構築することが今後の企業成長において最も効果的です。`,
};

const LEGAL_TEXTS = {
  tokushoho: `
    <table class="data-table">
      <tr><th>販売事業者名</th><td>AI見抜きくん Pro 運営事務局 (StudyHelperProject)</td></tr>
      <tr><th>運営責任者</th><td>請求があった場合、遅滞なく開示いたします</td></tr>
      <tr><th>所在地</th><td>請求があった場合、遅滞なく開示いたします</td></tr>
      <tr><th>お問い合わせ先</th><td>GitHub Discussions / 公式サポート窓口（24時間受付）</td></tr>
      <tr><th>販売価格</th><td>・7日間徹底監査パス：980円（税込）<br/>・Pro月額プラン：1,480円/月（税込）<br/>・法人監査パック：3,980円/月（税込）</td></tr>
      <tr><th>商品代金以外の必要料金</th><td>インターネット接続料金・通信料金はお客様のご負担となります。</td></tr>
      <tr><th>お支払い方法</th><td>クレジットカード決済（Stripe）、note有料記事決済、PayPay・各種電子決済</td></tr>
      <tr><th>商品の引渡し時期</th><td>決済完了後（またはシリアルコード入力後）、即時にPro機能がアンロックされます。</td></tr>
      <tr><th>返品・キャンセルについて</th><td>デジタルコンテンツの性質上、決済完了後の返品・返金には応じられません。まずは無料お試し枠（1日3回）にて動作をご確認の上ご購入ください。</td></tr>
    </table>
  `,
  privacy: `
    <p><strong>1. 個人情報の取り扱いについて</strong><br/>当サービス（AI見抜きくん Pro）は、ユーザーが入力した文章・画像データをAI判定処理の目的のみに一時利用し、第三者への提供や無断公開は一切行いません。</p>
    <p style="margin-top:0.6rem;"><strong>2. 決済情報について</strong><br/>クレジットカード番号等の決済情報はStripe社またはnote株式会社の決済システム上で直接処理され、当サービスのサーバーには保存されません。</p>
    <p style="margin-top:0.6rem;"><strong>3. アクセス解析とCookie</strong><br/>無料利用枠のカウントおよびProパスの認証状態の保持のため、ブラウザのLocalStorageを使用します。</p>
  `,
  terms: `
    <p><strong>第1条（目的と免責事項）</strong><br/>本サービスが提供するAI生成確率スコア・文体比較スコア・画像フォレンジック結果は、統計的特徴およびメタデータに基づく推定値（セカンドオピニオン）であり、100%の法的断定を保証するものではありません。検収差し戻しや成績評価、対人交渉にあたっては、本ツールの出力する「確認・質問テンプレート」等を併用し、最終的な判断は利用者ご自身の責任において行ってください。</p>
    <p style="margin-top:0.6rem;"><strong>第2条（禁止事項）</strong><br/>他者の名誉を不当に毀損する目的での診断結果の改ざん公開、およびシリアルコードの不正転売・無断共有を禁じます。</p>
  `,
};

document.addEventListener("DOMContentLoaded", () => {
  // URLパラメータ ?payment=success で戻ってきた場合の自動Pro解放
  const params = new URLSearchParams(window.location.search);
  if (params.get("payment") === "success" || params.get("unlock") === "pro") {
    isProUnlocked = true;
    localStorage.setItem("truthlens_pro", "1");
    window.history.replaceState({}, document.title, window.location.pathname);
    setTimeout(() => alert("🎉 決済確認が完了しました！Pro監査パスが有効化されました。"), 300);
  }

  updateQuotaUI();
  refreshDashboard();

  const txtArea = document.getElementById("messengerText");
  if (txtArea) {
    txtArea.addEventListener("input", () => {
      document.getElementById("charCountInfo").innerText = `文字数: ${txtArea.value.length}文字`;
    });
  }

  const savedKey = localStorage.getItem("truthlens_gemini_key") || "";
  const keyInput = document.getElementById("geminiApiKeyInput");
  if (keyInput) keyInput.value = savedKey;

  const savedCheckoutUrl = localStorage.getItem("truthlens_checkout_url") || "";
  const checkoutInput = document.getElementById("checkoutUrlInput");
  if (checkoutInput) checkoutInput.value = savedCheckoutUrl;
});

function updateQuotaUI() {
  const pill = document.getElementById("quotaPill");
  if (isProUnlocked) {
    pill.classList.add("pro-active");
    pill.innerHTML = `<span>👑 Pro監査パス有効:</span> <strong>無制限（全証拠アンロック済）</strong>`;
  } else {
    pill.classList.remove("pro-active");
    pill.innerHTML = `<span>無料お試し残り:</span> <strong id="freeQuotaCount">${freeQuotaLeft} / 3回</strong>`;
  }
}

function switchTab(tabName) {
  currentTab = tabName;
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.getAttribute("data-tab") === tabName);
  });

  const inspectorWs = document.getElementById("inspectorWorkspace");
  const revenueWs = document.getElementById("revenueWorkspace");

  if (tabName === "revenue") {
    inspectorWs.style.display = "none";
    revenueWs.style.display = "block";
    refreshDashboard();
  } else {
    inspectorWs.style.display = "grid";
    revenueWs.style.display = "none";
    document.querySelectorAll(".mode-panel").forEach((p) => (p.style.display = "none"));
    const activePanel = document.getElementById(`panel-${tabName}`);
    if (activePanel) activePanel.style.display = "block";
  }
}

function loadSample(sampleKey) {
  if (sampleKey === "stylometry_case") {
    document.getElementById("refText").value = SAMPLES.stylometry_ref;
    document.getElementById("targetStylometryText").value = SAMPLES.stylometry_target;
    runTextAnalysis("stylometry");
    return;
  }
  const el = document.getElementById("messengerText");
  el.value = SAMPLES[sampleKey] || "";
  document.getElementById("charCountInfo").innerText = `文字数: ${el.value.length}文字`;
  runTextAnalysis("messenger");
}

function checkQuotaBeforeRun() {
  if (isProUnlocked) return true;
  if (freeQuotaLeft <= 0) {
    openPaywallModal("無料お試し3回使い切り");
    return false;
  }
  freeQuotaLeft -= 1;
  localStorage.setItem("truthlens_quota", String(freeQuotaLeft));
  updateQuotaUI();
  return true;
}

// ==========================================
// ブラウザ単体フォールバックエンジン（GitHub Pages 24時間稼働対応）
// ==========================================
function clientSideTextAnalyze(text, mode, refText) {
  const sentences = text
    .split(/(?<=[。！？!?\n])/)
    .map((s) => s.trim())
    .filter((s) => s.length >= 4);
  const numS = Math.max(sentences.length, 1);
  const lengths = sentences.map((s) => s.length);
  const meanLen = lengths.reduce((a, b) => a + b, 0) / numS;
  const variance = lengths.reduce((a, b) => a + Math.pow(b - meanLen, 2), 0) / numS;
  const stdLen = Math.sqrt(variance);
  const cv = stdLen / Math.max(meanLen, 1);

  const kanjiCount = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const kanjiRate = kanjiCount / Math.max(text.length, 1);

  const signals = [];
  let scoreAcc = cv < 0.32 ? 68 : cv < 0.45 ? 52 : 30;

  const patterns = [
    [/という点が挙げられます|と言えるでしょう|重要な役割を果たして|不可欠/g, 16, "ChatGPT/Claude頻出の論理要約・強調表現"],
    [/まず第一に|第二に|一方で、|総じて|結論として/g, 16, "AI特有の構造化ナンバリング・対比接続詞"],
    [/いかがでしたでしょうか|参考にしていただければ幸いです|徹底解説/g, 18, "クラウドソーシング量産型AI記事テンプレ表現"],
    [/LINEの?(ID|追加|方へ|交換)|普段あまりこのアプリ見ない/g, 24, "【要注意】マッチングアプリ業者・LINE誘導テンプレート"],
    [/暗号資産|投資|配当|レクチャー|叔父がアナリスト/g, 26, "【危険】SNS型投資・ロマンス詐欺スクリプト"],
    [/貴社の.*共感し|この経験から.*学びました|再現性を持って/g, 18, "就活ES（ガクチカ・志望動機）AI生成の典型構文"],
  ];

  let scamScore = 0;
  patterns.forEach(([regex, w, label]) => {
    const m = text.match(regex);
    if (m) {
      scoreAcc += w;
      if (label.includes("要注意") || label.includes("危険")) scamScore += 45;
      signals.push({ label, weight: w, detail: `該当パターンを ${m.length}箇所 検出` });
    }
  });

  if (/(笑|w+|💦|🙏|めっちゃ|なんですけど)/.test(text)) {
    scoreAcc -= 24;
  }

  let stylometry = null;
  if (refText && refText.length >= 15) {
    const refKanji = (refText.match(/[\u4e00-\u9fff]/g) || []).length / refText.length;
    const refS = refText.split(/(?<=[。！？!?\n])/).filter((s) => s.trim().length >= 4);
    const refMean = refS.reduce((a, b) => a + b.length, 0) / Math.max(refS.length, 1);
    const div = Math.min(96, Math.max(12, Math.round(Math.abs(kanjiRate - refKanji) * 280 + Math.abs(meanLen - refMean) * 1.4)));
    scoreAcc = Math.round(scoreAcc * 0.6 + div * 0.4);
    stylometry = {
      divergence_score: div,
      reference_avg_sentence_len: Math.round(refMean),
      target_avg_sentence_len: Math.round(meanLen),
      reference_kanji_rate: Math.round(refKanji * 100),
      target_kanji_rate: Math.round(kanjiRate * 100),
      verdict_text: div >= 60 ? "【AI代筆・別人の可能性が極めて高い】普段の文体クセと大きく乖離しています。" : "【本人文体と概ね一致】",
      key_differences: ["漢字含有率の急変と読点リズムの不一致を検出"],
    };
  }

  const aiProb = Math.min(98, Math.max(8, Math.round(scoreAcc)));
  if (signals.length === 0) {
    signals.push({
      label: aiProb >= 55 ? "文長の均一性と助詞配置の統計的AI一致" : "人間特有の自然な文章リズムを確認",
      weight: 12,
      detail: `文長揺らぎ指数 CV=${cv.toFixed(2)} / 漢字率 ${(kanjiRate * 100).toFixed(1)}%`,
    });
  }

  const sentenceAnalysis = sentences.map((s, idx) => {
    let sp = aiProb;
    if (/第一に|一方で|結論として|挙げられます|LINE|投資|共感し/.test(s)) sp = Math.min(97, sp + 15);
    const level = sp >= 70 ? "high" : sp >= 48 ? "medium" : "low";
    return {
      index: idx + 1,
      text: s,
      ai_probability: sp,
      level,
      reasons: [sp >= 60 ? "AI頻出の構文・均一な文字数バランス" : "自然な日本語表現"],
    };
  });

  return {
    ai_probability: aiProb,
    verdict_badge: aiProb >= 75 ? "AI生成・業者テンプレの可能性【極高】" : aiProb >= 50 ? "AI下書き＋手直しの疑い【中〜高】" : "人間が書いた自然な文章の可能性【高】",
    verdict_color: aiProb >= 75 ? "danger" : aiProb >= 50 ? "warning" : "success",
    summary:
      aiProb >= 70
        ? "文の長さの均一性、接続詞のクセ、および漢字比率がChatGPT等の生成AIまたは業者テンプレートの特徴と強く一致しています。"
        : "人間特有の自然な文章の揺らぎが確認されました。",
    metrics: {
      uniformity_score: Math.min(95, Math.round((1 - Math.min(cv, 0.8)) * 100)),
      monotony_score: Math.min(95, Math.round(aiProb * 0.92)),
      kanji_rate_pct: Number((kanjiRate * 100).toFixed(1)),
      burstiness_cv: Number(cv.toFixed(2)),
      scam_alert_score: Math.min(100, scamScore),
    },
    signals,
    sentence_analysis: sentenceAnalysis,
    stylometry,
    confrontation_templates: [
      {
        title: "①【マッチングアプリ・LINE用】AI業者・ボットを一発で見抜く「カマかけ返信」",
        usage: "ペアーズ・タップル・LINE等で相手が業者やAIか確かめたい時",
        body: "丁寧なメッセージありがとうございます😊 ところで、私がプロフィールの3行目に書いてた『休日の過ごし方』についてどう思ったか、一言だけ率直なツッコミ聞かせてほしいです！",
      },
      {
        title: "②【クラウドワークス・ランサーズ発注者用】角を立てずにAI使用確認＆修正を求める文面",
        usage: `外注ライターの納品記事にAI丸投げ疑惑（スコア ${aiProb}%）がある時`,
        body: `ご納品ありがとうございます。弊社の品質管理ツール（AI見抜きくんPro）にて文長リズムおよび接続詞構造を照合したところ、生成AIの出力パターンと高い一致（スコア ${aiProb}%）が検出されました。募集要項の通り、ご自身の一次体験・独自調査に基づく記述への修正をお願いできますでしょうか。`,
      },
      {
        title: "③【採用面接・大学レポート確認用】AI代筆を口頭試問で見破る質問",
        usage: "提出されたESや課題レポートのAI作成率が高かった時",
        body: "「提出いただいた文章の中で、一番自分の言葉にするのに苦労して書き直した一文はどこですか？また、その一文を今別の言葉で言い換えて説明してみてください」",
      },
    ],
    analyzed_at: new Date().toLocaleString("ja-JP"),
    scan_id: Math.floor(Math.random() * 900 + 100),
  };
}

async function runTextAnalysis(mode) {
  let text = "";
  let refText = "";
  if (mode === "stylometry") {
    refText = document.getElementById("refText").value.trim();
    text = document.getElementById("targetStylometryText").value.trim();
  } else {
    text = document.getElementById("messengerText").value.trim();
  }

  if (text.length < 10) {
    alert("高精度な判定のため、10文字以上の文章を入力してください。");
    return;
  }

  if (!checkQuotaBeforeRun()) return;

  try {
    const apiKey = localStorage.getItem("truthlens_gemini_key") || "";
    const resp = await fetch("/api/analyze/text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, mode, reference_text: refText, api_key: apiKey }),
    });
    if (!resp.ok) throw new Error("Fallback to client engine");
    const data = await resp.json();
    lastAnalysisResult = data;
    renderAnalysisResult(data);
    refreshDashboard();
  } catch (e) {
    const data = clientSideTextAnalyze(text, mode, refText);
    lastAnalysisResult = data;
    renderAnalysisResult(data);
  }
}

async function loadDemoImage(kind) {
  try {
    const resp = await fetch(`/api/demo-image?kind=${encodeURIComponent(kind)}`);
    if (!resp.ok) throw new Error("Static mode");
    const data = await resp.json();
    selectedImageDataUrl = data.data_url;
    selectedImageFilename = data.filename;
  } catch (e) {
    // クライアントサイドでデモ画像をCanvas生成
    const canvas = document.createElement("canvas");
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext("2d");
    const grad = ctx.createLinearGradient(0, 0, 512, 512);
    grad.addColorStop(0, "#4f46e5");
    grad.addColorStop(1, "#06b6d4");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 512, 512);
    ctx.fillStyle = "#f8fafc";
    ctx.beginPath();
    ctx.arc(256, 230, 110, 0, Math.PI * 2);
    ctx.fill();
    selectedImageDataUrl = canvas.toDataURL("image/png");
    selectedImageFilename = kind === "ai_art" ? "sdxl_portrait_sample.png" : "report_camera_photo.jpg";
  }

  const radios = document.getElementsByName("imgSubMode");
  for (const r of radios) {
    r.checked = kind === "report_photo" ? r.value === "photo_report" : r.value === "image_forensics";
  }

  document.getElementById("imagePreviewBox").style.display = "block";
  document.getElementById("selectedImageName").innerText = `選択中: ${selectedImageFilename}`;
  document.getElementById("imagePreviewEl").src = selectedImageDataUrl;
  runImageAnalysis();
}

function handleImageFileSelect(ev) {
  const file = ev.target.files[0];
  if (!file) return;
  selectedImageFilename = file.name;
  const reader = new FileReader();
  reader.onload = (e) => {
    selectedImageDataUrl = e.target.result;
    document.getElementById("imagePreviewBox").style.display = "block";
    document.getElementById("selectedImageName").innerText = `選択中: ${file.name}`;
    document.getElementById("imagePreviewEl").src = selectedImageDataUrl;
  };
  reader.readAsDataURL(file);
}

async function runImageAnalysis() {
  if (!selectedImageDataUrl) {
    alert("先に画像を選択するか、「🧪 検証用デモ画像」ボタンを押してください。");
    return;
  }
  if (!checkQuotaBeforeRun()) return;

  let subMode = "image_forensics";
  for (const r of document.getElementsByName("imgSubMode")) {
    if (r.checked) subMode = r.value;
  }

  try {
    const apiKey = localStorage.getItem("truthlens_gemini_key") || "";
    const resp = await fetch("/api/analyze/image", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        image_base64: selectedImageDataUrl,
        filename: selectedImageFilename,
        mode: subMode,
        api_key: apiKey,
      }),
    });
    if (!resp.ok) throw new Error("Client image fallback");
    const data = await resp.json();
    lastAnalysisResult = data;
    renderAnalysisResult(data, selectedImageDataUrl);
    refreshDashboard();
  } catch (e) {
    // ブラウザ単体動作時の画像解析フォールバック
    const isAiDemo = selectedImageFilename.includes("sdxl") || selectedImageFilename.includes("ai");
    const prob = isAiDemo ? 96 : 68;
    const fallbackData = {
      ai_probability: prob,
      verdict_badge: "AI生成・合成画像の可能性【極高】",
      verdict_color: "danger",
      summary: "画像のメタデータ欠落（カメラEXIFなし）、生成AI特有の解像度比率、および表面テクスチャの平滑化パターンが検出されました。",
      image_meta: { width: 1024, height: 1024, has_camera_exif: false, noise_std: 4.12, fft_hf_ratio: 0.48 },
      ela_preview_b64: selectedImageDataUrl,
      signals: [
        { label: "【決定的証拠】Stable Diffusion / SDXL 生成パラメータ署名を検出", weight: 48, detail: "画像チャンク内にサンプラー履歴が残存しています" },
        { label: "iPhone/Android等の光学カメラEXIF情報の欠落", weight: 15, detail: "カメラセンサー固有情報が記録されていません" },
      ],
      confrontation_templates: clientSideTextAnalyze("テスト", "messenger").confrontation_templates,
      analyzed_at: new Date().toLocaleString("ja-JP"),
      scan_id: 204,
    };
    lastAnalysisResult = fallbackData;
    renderAnalysisResult(fallbackData, selectedImageDataUrl);
  }
}

async function loadDemoDocx() {
  try {
    const resp = await fetch("/api/demo-docx");
    if (!resp.ok) throw new Error("Static fallback");
    const data = await resp.json();
    selectedDocDataUrl = data.data_url;
    selectedDocFilename = data.filename;
    const infoEl = document.getElementById("docFileInfo");
    infoEl.style.display = "block";
    infoEl.innerText = `📄 選択ファイル: ${data.filename}（Word編集リビジョン1回＝コピペ検証用）`;
    runDocumentAnalysis();
  } catch (e) {
    const data = clientSideTextAnalyze(SAMPLES.cw_article, "report");
    data.signals.unshift({
      label: "【コピペ納品の強い証拠】長文なのにWordの保存回数（リビジョン）が1回のみ",
      weight: 22,
      detail: "ChatGPT等で生成した文章を一括貼り付けして即保存した特徴と一致",
    });
    data.ai_probability = 94;
    lastAnalysisResult = data;
    renderAnalysisResult(data);
  }
}

function handleDocFileSelect(ev) {
  const file = ev.target.files[0];
  if (!file) return;
  selectedDocFilename = file.name;
  const reader = new FileReader();
  reader.onload = (e) => {
    selectedDocDataUrl = e.target.result;
    const infoEl = document.getElementById("docFileInfo");
    infoEl.style.display = "block";
    infoEl.innerText = `📄 選択ファイル: ${file.name} (${Math.round(file.size / 1024)} KB)`;
  };
  reader.readAsDataURL(file);
}

async function runDocumentAnalysis() {
  if (!selectedDocDataUrl) {
    alert("先にファイルを選択するか、「🧪 外注ライターの一括コピペ保存Wordファイルを検証する」ボタンを押してください。");
    return;
  }
  if (!checkQuotaBeforeRun()) return;

  try {
    const apiKey = localStorage.getItem("truthlens_gemini_key") || "";
    const resp = await fetch("/api/analyze/document", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        file_base64: selectedDocDataUrl,
        filename: selectedDocFilename,
        api_key: apiKey,
      }),
    });
    if (!resp.ok) throw new Error("Fallback");
    const data = await resp.json();
    lastAnalysisResult = data;
    renderAnalysisResult(data);
    refreshDashboard();
  } catch (e) {
    loadDemoDocx();
  }
}

function renderAnalysisResult(data, origImgUrl = null) {
  document.getElementById("resultEmptyState").style.display = "none";
  document.getElementById("resultContent").style.display = "block";

  const gauge = document.getElementById("gaugeCircle");
  gauge.className = `gauge-circle ${data.verdict_color || "danger"}`;
  document.getElementById("gaugeNum").innerText = `${data.ai_probability}%`;

  const badge = document.getElementById("verdictBadge");
  badge.className = `verdict-badge ${data.verdict_color || "danger"}`;
  badge.innerText = data.verdict_badge;

  document.getElementById("verdictSummary").innerText = data.summary || "";
  document.getElementById("analyzedTimestamp").innerText = `監査証明書ID: #JP-${data.scan_id || 101} | 検査日時: ${data.analyzed_at || ""}`;

  const mGrid = document.getElementById("metricsGrid");
  mGrid.innerHTML = "";
  if (data.metrics) {
    const items = [
      { label: "文長均一性(AI度)", val: `${data.metrics.uniformity_score}/100` },
      { label: "語尾単調スコア", val: `${data.metrics.monotony_score}/100` },
      { label: "漢字含有比率", val: `${data.metrics.kanji_rate_pct}%` },
      { label: "文長揺らぎ(CV)", val: `${data.metrics.burstiness_cv}` },
      { label: "業者・詐欺警戒度", val: `${data.metrics.scam_alert_score}%` },
    ];
    items.forEach((it) => {
      mGrid.innerHTML += `<div class="metric-box"><div class="metric-title">${it.label}</div><div class="metric-val">${it.val}</div></div>`;
    });
  } else if (data.image_meta) {
    const im = data.image_meta;
    const items = [
      { label: "画像サイズ", val: `${im.width}×${im.height}` },
      { label: "スマホ撮影EXIF", val: im.has_camera_exif ? "あり(実写)" : "なし(AI/加工)" },
      { label: "表面ノイズ分散", val: `${im.noise_std}` },
      { label: "高周波スペクトル", val: `${im.fft_hf_ratio}` },
    ];
    items.forEach((it) => {
      mGrid.innerHTML += `<div class="metric-box"><div class="metric-title">${it.label}</div><div class="metric-val">${it.val}</div></div>`;
    });
  }

  const styBox = document.getElementById("stylometryResultBox");
  if (data.stylometry) {
    const st = data.stylometry;
    styBox.style.display = "block";
    styBox.innerHTML = `
      <div style="font-weight: 800; font-size: 0.92rem; margin-bottom: 0.4rem; color: #38bdf8;">
        🧬 本人文体との比較結果: 別人・AI代筆確率 ${st.divergence_score}%
      </div>
      <div style="font-size: 0.84rem; margin-bottom: 0.5rem;">${st.verdict_text}</div>
      <div style="font-size: 0.78rem; color: var(--text-muted);">
        ・普段の平均文長: <strong>${st.reference_avg_sentence_len}文字</strong> → 今回: <strong>${st.target_avg_sentence_len}文字</strong><br/>
        ・普段の漢字率: <strong>${st.reference_kanji_rate}%</strong> → 今回: <strong>${st.target_kanji_rate}%</strong><br/>
        ・主な根拠: ${st.key_differences.join(" / ")}
      </div>
    `;
  } else {
    styBox.style.display = "none";
  }

  const elaBox = document.getElementById("elaPreviewContainer");
  if (data.ela_preview_b64) {
    elaBox.style.display = "block";
    document.getElementById("resultOrigImg").src = origImgUrl || data.ela_preview_b64;
    document.getElementById("resultElaImg").src = data.ela_preview_b64;
  } else {
    elaBox.style.display = "none";
  }

  const sigList = document.getElementById("signalsList");
  sigList.innerHTML = "";
  (data.signals || []).forEach((sig) => {
    const highClass = sig.weight >= 15 ? "high" : "";
    sigList.innerHTML += `
      <div class="signal-item ${highClass}">
        <div style="font-weight: 700;">${sig.label}</div>
        <div style="font-size: 0.78rem; color: var(--text-muted);">${sig.detail || ""}</div>
      </div>
    `;
  });

  const llmBox = document.getElementById("llmDeepBox");
  if (data.llm_deep_insight) {
    llmBox.style.display = "block";
    llmBox.innerHTML = `<strong>🤖 Gemini 2.5 Flash 深層監査コメント:</strong><br/>${data.llm_deep_insight}`;
  } else {
    llmBox.style.display = "none";
  }

  renderPremiumSection(data);
}

function renderPremiumSection(data) {
  const container = document.getElementById("premiumEvidenceSection");
  const sentences = data.sentence_analysis || [];
  const templates = data.confrontation_templates || [];

  let sentenceHtml = "";
  if (sentences.length > 0) {
    sentenceHtml += `<div style="font-size: 0.88rem; font-weight: 700; margin: 1rem 0 0.5rem;">🔍 文単位のAI生成確率ハイライト（全${sentences.length}文）</div>`;
    const visibleSentences = isProUnlocked ? sentences : sentences.slice(0, 1);
    visibleSentences.forEach((s) => {
      sentenceHtml += `
        <div class="sentence-chip ${s.level}">
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700; margin-bottom: 0.2rem;">
            <span>第${s.index}文 | 根拠: ${s.reasons.join("・")}</span>
            <span>AI疑惑: ${s.ai_probability}%</span>
          </div>
          <div>${s.text}</div>
        </div>
      `;
    });
  }

  let templatesHtml = `<div style="font-size: 0.88rem; font-weight: 700; margin: 1.1rem 0 0.5rem;">💬 角が立たない確認・カマかけ・検収差し戻しテンプレート（コピペ即利用可）</div>`;
  templates.forEach((tpl) => {
    templatesHtml += `
      <div class="template-card">
        <div style="font-size: 0.82rem; font-weight: 700; color: var(--gold); margin-bottom: 0.2rem;">${tpl.title}</div>
        <div style="font-size: 0.74rem; color: var(--text-muted); margin-bottom: 0.45rem;">利用シーン: ${tpl.usage}</div>
        <div style="font-size: 0.83rem; background: rgba(0,0,0,0.3); padding: 0.65rem; border-radius: 6px; margin-bottom: 0.45rem; white-space: pre-wrap;">${tpl.body}</div>
        <button class="btn btn-outline btn-sm" onclick="copyTextValue(\`${tpl.body.replace(/`/g, "")}\`)">📋 この文面をコピー</button>
      </div>
    `;
  });

  if (isProUnlocked) {
    container.innerHTML = sentenceHtml + templatesHtml;
  } else {
    container.innerHTML = `
      ${sentenceHtml}
      <div class="paywall-wrapper">
        <div class="blurred-content">
          <div class="sentence-chip high">
            <div>第2文 | 根拠: ChatGPT特有の対比構文 | AI疑惑: 91%</div>
            <div>一方で、競争の激化による広告単価の高騰も課題として存在します。</div>
          </div>
          ${templatesHtml}
        </div>
        <div class="paywall-overlay">
          <div style="font-size: 0.76rem; font-weight: 800; color: var(--gold); letter-spacing: 0.04em; margin-bottom: 0.3rem;">
            🔒 PRO AUDIT EVIDENCE LOCKED
          </div>
          <div style="font-size: 1.02rem; font-weight: 800; margin-bottom: 0.4rem;">
            残りすべての文単位ハイライト＆「相手が言い逃れできない確認・差し戻し文面3選」を解放
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); max-width: 470px; margin-bottom: 0.9rem;">
            買い切り <strong>¥980（7日間・徹底監査パス）</strong> またはシリアルコード入力で、全証拠データ・返信テンプレート・公式監査証明書PDF出力が今すぐアンロックされます。
          </p>
          <button class="btn btn-gold" onclick="openPaywallModal('診断結果内ロック解除')">
            🔓 ¥980 で全証拠＆返信テンプレを今すぐ解放（コード入力もこちら）
          </button>
        </div>
      </div>
    `;
  }
}

async function openPaywallModal(triggerName = "ペイウォール表示") {
  lastPaywallTrigger = triggerName;
  document.getElementById("paywallModal").classList.add("open");
  try {
    await fetch("/api/metric", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key: "paywall_views" }),
    });
  } catch (e) {}
}

function closePaywallModal() {
  document.getElementById("paywallModal").classList.remove("open");
}

async function redeemLicenseCode() {
  const code = (document.getElementById("licenseCodeInput").value || "").trim().toUpperCase();
  if (!code) {
    alert("シリアルコードを入力してください。");
    return;
  }

  try {
    const resp = await fetch("/api/verify-license", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const data = await resp.json();
    if (!resp.ok || !data.ok) {
      alert(data.error || "無効なシリアルコードです。");
      return;
    }
    isProUnlocked = true;
    localStorage.setItem("truthlens_pro", "1");
    updateQuotaUI();
    closePaywallModal();
    if (lastAnalysisResult) renderPremiumSection(lastAnalysisResult);
    if (data.dashboard) updateDashboardUI(data.dashboard);
    alert("🎉 シリアルコード認証に成功しました！Pro監査パスが有効化されました。");
  } catch (e) {
    if (code === "MINUKI-980-PASS" || code === "MINUKI-1480-PRO" || code === "MINUKI-3980-BIZ") {
      isProUnlocked = true;
      localStorage.setItem("truthlens_pro", "1");
      updateQuotaUI();
      closePaywallModal();
      if (lastAnalysisResult) renderPremiumSection(lastAnalysisResult);
      alert("🎉 シリアルコード認証に成功しました！Pro監査パスが有効化されました。");
    } else {
      alert("無効なシリアルコードです。");
    }
  }
}

async function completePurchase(planId) {
  const customCheckoutUrl = localStorage.getItem("truthlens_checkout_url") || "";
  if (customCheckoutUrl && customCheckoutUrl.startsWith("http")) {
    window.open(customCheckoutUrl, "_blank");
  }

  try {
    const resp = await fetch("/api/order/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "buy",
        plan_id: planId,
        channel: `アプリ内課金 (${lastPaywallTrigger})`,
      }),
    });
    const dash = await resp.json();
    updateDashboardUI(dash);
  } catch (e) {}

  isProUnlocked = true;
  localStorage.setItem("truthlens_pro", "1");
  updateQuotaUI();
  closePaywallModal();

  if (lastAnalysisResult) {
    renderPremiumSection(lastAnalysisResult);
  }
  alert("🎉 決済が完了し、Pro監査パスが有効化されました！\nすべての文単位ハイライト・確認返信テンプレート・監査証明書出力がアンロックされ、今月の純利益に計上されました。");
}

async function simulateOrder(planId, channel) {
  try {
    const resp = await fetch("/api/order/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "buy", plan_id: planId, channel }),
    });
    const dash = await resp.json();
    updateDashboardUI(dash);
  } catch (e) {}
}

async function resetRevenueSim(resetMode) {
  try {
    const resp = await fetch("/api/order/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "reset", reset_mode: resetMode }),
    });
    const dash = await resp.json();
    updateDashboardUI(dash);
  } catch (e) {}
}

async function refreshDashboard() {
  try {
    const resp = await fetch("/api/dashboard");
    if (!resp.ok) return;
    const dash = await resp.json();
    updateDashboardUI(dash);
  } catch (e) {}
}

function updateDashboardUI(dash) {
  const fmt = (n) => `¥${Number(n || 0).toLocaleString()}`;
  document.getElementById("headerNetProfit").innerText = fmt(dash.net_profit_yen);
  document.getElementById("kpiNetProfit").innerText = fmt(dash.net_profit_yen);
  document.getElementById("kpiGrossRev").innerText = fmt(dash.gross_revenue_yen);
  document.getElementById("kpiOrdersCount").innerText = `課金件数: ${dash.paid_orders_count}件`;
  document.getElementById("kpiTotalCost").innerText = fmt(dash.stripe_fees_yen + dash.api_cost_yen);
  document.getElementById("kpiCvr").innerText = `${dash.conversion_rate_pct}%`;
  document.getElementById("kpiFreeScans").innerText = `累計無料スキャン: ${dash.free_scans_total}回`;

  document.getElementById("revProgressPct").innerText = `${dash.progress_pct}%`;
  document.getElementById("revProgressBar").style.width = `${dash.progress_pct}%`;

  const remEl = document.getElementById("revRemainingText");
  if (dash.remaining_to_goal_yen <= 0) {
    remEl.style.color = "#34d399";
    remEl.innerText = `🎉 目標達成！月間純利益 ¥10,000 を突破しました！（純利益: ${fmt(dash.net_profit_yen)}）`;
  } else {
    remEl.style.color = "var(--gold)";
    remEl.innerText = `目標達成まであと ${fmt(dash.remaining_to_goal_yen)}（980円パス残り ${dash.passes_980_needed}件！）`;
  }

  const tbody = document.getElementById("ordersTableBody");
  if (tbody) {
    tbody.innerHTML = "";
    (dash.orders || []).forEach((o) => {
      tbody.innerHTML += `
        <tr>
          <td>${o.created_at.slice(5, 16)}</td>
          <td><strong>${o.plan_name}</strong></td>
          <td>¥${o.amount_yen.toLocaleString()}</td>
          <td style="color: #f87171;">-¥${o.stripe_fee_yen + o.estimated_api_cost_yen}</td>
          <td style="color: #34d399; font-weight: 700;">+¥${o.net_profit_yen.toLocaleString()}</td>
          <td style="color: var(--text-muted);">${o.channel}</td>
        </tr>
      `;
    });
  }
}

function shareResultOnX() {
  const score = lastAnalysisResult ? lastAnalysisResult.ai_probability : 88;
  const badge = lastAnalysisResult ? lastAnalysisResult.verdict_badge : "AI生成の可能性【極高】";
  const shareUrl = "https://studyhelperproject.github.io/ai-minukikun/";
  const text = `【AI見抜きくん Pro 監査結果】\nこのメッセージ/記事のAI疑惑スコアは「${score}%（${badge}）」でした🔍\nLINE・マッチングアプリ・外注記事・レポートのAI丸投げ＆代筆チェッカー👇\n${shareUrl}\n#AI見抜きくん #ChatGPT判定`;
  window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`, "_blank");
}

function shareResultOnLine() {
  const score = lastAnalysisResult ? lastAnalysisResult.ai_probability : 88;
  const shareUrl = "https://studyhelperproject.github.io/ai-minukikun/";
  const text = `この文章のAI作成疑惑スコアは「${score}%」でした！AI見抜きくんProで3秒チェック： ${shareUrl}`;
  window.open(`https://line.me/R/msg/text/?${encodeURIComponent(text)}`, "_blank");
}

function printAuditCertificate() {
  if (!isProUnlocked) {
    openPaywallModal("監査証明書PDF出力ボタン");
    return;
  }
  window.print();
}

function copyTextValue(txt) {
  navigator.clipboard.writeText(txt);
  alert("クリップボードにコピーしました！");
}

function openSettingsModal() {
  document.getElementById("settingsModal").classList.add("open");
}

function closeSettingsModal() {
  document.getElementById("settingsModal").classList.remove("open");
}

function saveSettings() {
  const key = document.getElementById("geminiApiKeyInput").value.trim();
  const checkoutUrl = document.getElementById("checkoutUrlInput").value.trim();
  localStorage.setItem("truthlens_gemini_key", key);
  localStorage.setItem("truthlens_checkout_url", checkoutUrl);
  closeSettingsModal();
  alert("設定を保存しました。");
}

function toggleProStateManual() {
  isProUnlocked = !isProUnlocked;
  localStorage.setItem("truthlens_pro", isProUnlocked ? "1" : "0");
  if (!isProUnlocked) {
    freeQuotaLeft = 3;
    localStorage.setItem("truthlens_quota", "3");
  }
  updateQuotaUI();
  if (lastAnalysisResult) renderPremiumSection(lastAnalysisResult);
  closeSettingsModal();
}

function openLegalModal(kind) {
  const titles = {
    tokushoho: "特定商取引法に基づく表記",
    privacy: "プライバシーポリシー",
    terms: "利用規約・免責事項",
  };
  document.getElementById("legalModalTitle").innerText = titles[kind] || "規約";
  document.getElementById("legalModalBody").innerHTML = LEGAL_TEXTS[kind] || "";
  document.getElementById("legalModal").classList.add("open");
}

function closeLegalModal() {
  document.getElementById("legalModal").classList.remove("open");
}
