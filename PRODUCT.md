# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

純前端靜態網站 (HTML5 + 現代 CSS3 + 模組化 Vanilla JS)，無需複雜後端或建置打包工具，可直接本機雙擊開啟或無縫部署至 GitHub Pages / Cloudflare Pages。Prompt 採用獨立子資料夾組織，各子資料夾內以 Markdown (`prompt.md` 包含 YAML Frontmatter 與正文) 描述中繼資料，並存放該組生成之照片。

## Users

探索 AI 影像生成、攝影後製風格轉移的創作者、設計師與攝影愛好者。當他們在社群（如 Facebook、X 等）發現精彩的 Prompt，卻發現「不同照片套用相同 Prompt 效果不一」時，需要對比不同攝影題材在該 Prompt 下的具體表現與參數設定。

## Product Purpose

建立一個精美、具現代藝廊質感的 Prompt Showcase 展示網站。解決 Prompt 實驗「跨題材效果難以預期」的痛點，以視覺化、直觀的方式呈現同一組 Prompt 在多種不同攝影題材（人像、風景、街拍、食物、運動紀實、微距特寫、建築、星空等）上的具體生成效果與詳細設定。

## Positioning

以「**一組 Prompt，跨題材全景展示**」為核心的視覺化藝廊。不同於一般只放單張美圖的 Prompt 分享庫，本站以「Prompt 資料夾」為單位，每個 Prompt 都是一份完整包含跨主題實測對比、原始來源、LLM/擴散模型、標籤與完整提示詞的活體展覽。

## Operating Context

- **首頁 (Showcase Home)**：
  - 全景隨機展覽牆：針對系統收錄的每個 Prompt 專案，動態從該組生成圖片中隨機抽取一張作為封面卡片展示。
  - 支援隨機重刷 (Shuffle / Randomize) 激發探索靈感，並支援 Tags 與模型即時篩選。
- **子頁面 / 詳情頁 (Prompt Detail View)**：
  - 點選卡片可進入該 Prompt 的詳情頁面，展示完整的 Prompt 主文（附帶一鍵複製功能）、來源網址 (URL)、關聯標籤 (Tags)、使用之 LLM / 影像模型、作者與創作脈絡。
  - 提供該 Prompt 套用在 20 張不同主題照片上的完整生成結果，並支援與原始照片（原相）並排或拖曳對比。
- **資料組織結構**：
  - 每個 Prompt 擁有專屬子資料夾（如 `prompts/<slug>/`）。
  - 資料夾內包含 `prompt.md`（YAML frontmatter 記錄標題、來源 url、tags、模型、日期等，正文記錄 Prompt 完整內容與建議情境）以及生成照片圖檔。

## Capabilities and Constraints

- **零建置門檻 (Zero-build)**：原生 Web 標準，無需 Node.js 編譯流程即可執行。
- **Markdown 中繼資料驅動**：利用結構化 `prompt.md`，可手動維護、Git 版控，或透過掃描腳本輸出清單供前端高速渲染。
- **動態隨機探索 (Serendipitous Discovery)**：首頁每次載入或點擊按鈕時隨機抽取不同封面，讓每次造訪都有新鮮感。
- **實用工具機制**：一鍵複製 Prompt、直接連往原始來源社群貼文、支援 Before / After 視覺比較。

## Brand Commitments

- **視覺風格**：沉浸式暗色藝廊體驗（Deep Obsidian & Neutral Dark 藝廊基底，高對比度文字與精緻微光 Accent，突出攝影作品本身的質感，堅拒缺乏美感的 AI Slop）。
- **產品識別**：Prompt Showcase Gallery。

## Evidence on Hand

- 已下載 20 張精選代表照片（10 張 kywk Flickr 攝影作品 + 10 張 Unsplash 高品質攝影），已分類整理於 `photos/flickr/` 與 `photos/unsplash/`。
- 已建立 `generate_gallery.py` 批次 AI 調用管線。
- 現有真實題材涵蓋：京都和服人像、北大武雲海、香港街拍、富士山馬拉松、日光古蹟、奔跑毛孩、台中書店、手沖咖啡、河口湖、薄荷島海岸等。

## Product Principles

1. **作品主導，介面後退 (Gallery-First)**：介面排版以高畫質影像為絕對主角，以克制、精準、優雅的排版襯托作品。
2. **脈絡透明完整 (Transparent Context)**：清楚呈現提示詞主文、來源出處、適用題材與模型，絕不遺漏技術細節。
3. **偶遇與探索趣味 (Serendipitous Discovery)**：透過首頁隨機封面機制打破固定死板的陳列，激發點擊探索慾望。
4. **即取即用的實用性 (Utilitarian Simplicity)**：點擊即可複製 Prompt，方便使用者將靈感無縫帶入自己的工作流。

## Accessibility & Inclusion

- 嚴格維持文字與背景足夠對比度（WCAG AA 標準）。
- 所有影像元件具備清楚的 `alt` 屬性與語意標籤。
- 支援鍵盤 Tab 與焦點導覽。
