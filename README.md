# AI Prompt Showcase Gallery — 跨題材攝影風格展示網站

本專案是一個專為 AI 影像生成與風格轉換設計的 **Showcase 展示網站**。  
為了解決「在社群中看到精彩的 Prompt，但套用在不同照片上效果不一致」的痛點，本專案精選 **20 張不同攝影主題的代表照片**（10 張取自您的 Flickr 相簿，10 張精選自 Unsplash 高畫質圖庫），全方位實測與對比同一組 Prompt 在各題材下的表現。

---

## 🌟 核心特色

1. **獨立資料夾與 Markdown 結構**：
   - 每個 Prompt 擁有專屬子資料夾（如 `prompts/<slug>/`）。
   - 以 `prompt.md`（YAML frontmatter + Markdown 正文）記錄中繼資訊（包含 Prompt 主文、來源貼文 URL、標籤 Tags、使用模型 LLM/Diffusion、創作脈絡與適用建議）。
   - 同資料夾存放該 Prompt 套用在 20 張照片上的生成成果。
2. **首頁隨機探索機制 (Dynamic Cover Discovery)**：
   - 首頁展示各 Prompt 專案卡片，**每次造訪或點擊「🎲 隨機換封面」時，自動隨機抽取一張該組照片作為封面**，打破固定陳列的死板感。
   - 支援 Tags 標籤、LLM 模型與關鍵字即時搜尋篩選。
3. **Prompt 詳情與 20 張照片全景對比 (Detail View)**：
   - 點擊任一 Prompt 即可進入專屬詳情（支援 URL Hash 錨點直連分享，如 `#prompt=fb-split-poster`）。
   - 提供 **📋 一鍵複製 Prompt** 與原始社群出處連結。
   - 展示 20 張代表照片的 **Before / After（原圖 vs 生成圖）並排對比**，並支援點擊圖片 Lightbox 高解析度放大檢視。
4. **極致輕量與零建置門檻 (Zero-Build)**：
   - 純靜態原生 Web 架構（HTML5 + 現代 CSS3 + 模組化 Vanilla JS），無須 Node.js 打包或後端服務。
   - 通過 **Impeccable UI/UX 設計標準**（無障礙 WCAG AA、對比度檢驗、純粹無 AI Slop 質感）。
   - 支援直接以瀏覽器雙擊開啟（`file://` 相容），亦可直接部署至 GitHub Pages 或 Cloudflare Pages。

---

## 📂 專案目錄結構

```text
prompt-gallery/
├── index.html                    # Showcase 藝廊首頁（含隨機封面、篩選、詳情對比視圖）
├── prompts_data.js               # 前端中繼資料快取（支援 file:// 協定）
├── prompts_index.json            # 完整 JSON 索引
├── photos_manifest.json          # 20 張代表照片之規格與標籤清單
├── PRODUCT.md                    # Impeccable 產品認知與架構定義文件
├── photos/                       # 原始 20 張代表照片
│   ├── flickr/                   # 10 張 Flickr 代表作（人像、高山、街拍、馬拉松、日光、毛孩等）
│   └── unsplash/                 # 10 張 Unsplash 代表作（時尚肖像、山川、雨夜街拍、美食等）
├── prompts/                      # 每個 Prompt 的獨立資料夾
│   ├── fb-split-poster/          # 範例 1：FB 分割海報風格（上下分割、極簡幾何拓印）
│   │   ├── prompt.md
│   │   └── generated/
│   ├── cinematic-portra/         # 範例 2：經典電影底片（Kodak Portra 400 35mm）
│   │   ├── prompt.md
│   │   └── generated/
│   ├── cyberpunk-neon/           # 範例 3：賽博龐克雨夜霓虹
│   │   ├── prompt.md
│   │   └── generated/
│   └── ghibli-watercolor/        # 範例 4：吉卜力溫暖手繪水彩
│       ├── prompt.md
│       └── generated/
└── scripts/
    ├── build_manifest.py         # 掃描 prompts/*/prompt.md 並自動更新前端索引
    └── generate_all_samples.py   # 批次生成範例圖像腳本
```

---

## 🛠️ 如何新增一組 Prompt？

當您在社群上發現新的 Prompt 時，僅需 2 個步驟即可將其收錄至網站：

### 步驟 1：建立 Prompt 子資料夾與 `prompt.md`
在 `prompts/` 底下新增資料夾（如 `prompts/my-new-prompt/`），並新增 `prompt.md`：

```markdown
---
id: "my-new-prompt"
title: "我的全新風格 Prompt"
author: "作者名稱"
source_url: "https://www.facebook.com/... 原始出處"
model: "Midjourney v6 / Imagen 3"
tags: ["風格標籤1", "風格標籤2"]
date: "2026-10-04"
summary: "這組 Prompt 的核心特色一句話簡述。"
---

## Prompt 提示詞

\`\`\`text
Your awesome prompt here... {subject}
\`\`\`

## 創作原理與適配建議
說明這組 Prompt 適合哪些照片題材，以及使用時的注意事項。
```

### 步驟 2：放入生成的 20 張照片並更新索引
將套用此 Prompt 生成的 20 張照片放入 `prompts/my-new-prompt/generated/`，然後在終端機執行：

```bash
python3 scripts/build_manifest.py
```

重新整理 `index.html`，新 Prompt 即可出現在網站展示牆中！

---

## 🌐 本地預覽

直接在瀏覽器開啟 [`index.html`](file:///home/kywk/Projects/prompt-gallery/index.html)，或使用 Python 簡易伺服器：

```bash
python3 -m http.server 8000
```
瀏覽器訪問 `http://localhost:8000` 即可體驗完整功能。
