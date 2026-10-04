#!/usr/bin/env python3
"""
AI Photo Gallery Generator
===========================
自動批次讀取 20 張主題照片（10 張 Flickr + 10 張 Unsplash），
結合使用者給予的 Prompt 與指定 AI Agent，自動生成 20 張套用該 Prompt 的風格照片，
並建立視覺化 Before / After 對比藝廊（index.html）。

支援 AI Agent:
  - gemini : 使用 Google Gemini / Imagen 3 API
  - openai : 使用 OpenAI DALL-E 3 API
  - agy    : 調用 Antigravity (agy) CLI / 本地 Agent
  - mock   : 模擬生成測試模式（無需 API Key，快速驗證流程）
"""

import os
import sys
import json
import base64
import argparse
import urllib.request
import urllib.parse
import subprocess
from datetime import datetime

# 內建風格 Prompt 預設範本（參考 FB AI 攝影社團熱門指令風格）
STYLE_PRESETS = {
    "fb_split_poster": (
        "Vertical 3:4 modern editorial poster with split composition. "
        "The upper half faithfully preserves the original photo's mood, texture, and natural subject: {subject}. "
        "The lower half reinterprets the core silhouette and emotional memory of the scene into "
        "minimalist geometric shapes, risograph block print, textured paper collage, and elegant line art. "
        "Exhibition poster aesthetic, Swiss typography layout, artistic contrast between realism and abstraction."
    ),
    "cinematic_film": (
        "Cinematic film photography shot on 35mm Kodak Portra 400, "
        "capturing {subject}. Subtle analog grain, soft golden hour halation, rich shadow depth, "
        "natural skin tones and authentic color grading. Directed by Wong Kar-wai aesthetic."
    ),
    "cyberpunk_neon": (
        "Cyberpunk aesthetic reinterpretation of {subject}. "
        "Vibrant neon lighting, moody wet street reflections, magenta and cyan volumetric fog, "
        "futuristic high-tech atmosphere with cinematic depth of field."
    ),
    "ghibli_watercolor": (
        "Studio Ghibli anime landscape art style, re-imagining {subject}. "
        "Lush hand-painted watercolor textures, warm emotional lighting, whimsical clouds, "
        "vibrant nature tones, Hayao Miyazaki inspired aesthetic."
    )
}

def load_manifest(manifest_path):
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)

def encode_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ================= Agent 實作 =================

def call_gemini_agent(prompt, image_path, api_key):
    """
    透過 Google Gemini API 呼叫 Imagen 3 / Gemini 多模態生成
    """
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("請設定 GEMINI_API_KEY 環境變數或透過 --api-key 傳入。")

    # 嘗試調用 Imagen 3 generateImages API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "outputMimeType": "image/jpeg"
        }
    }
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            predictions = data.get("predictions", [])
            if predictions and "bytesBase64Encoded" in predictions[0]:
                return base64.b64decode(predictions[0]["bytesBase64Encoded"])
            raise ValueError(f"Gemini 回傳格式異常: {data}")
    except Exception as e:
        # 若 Imagen 不可用，可退回 Gemini 2.5 Flash 多模態描述或處理
        print(f"  [Gemini API 訊息] {e}")
        raise

def call_openai_agent(prompt, image_path, api_key):
    """
    透過 OpenAI DALL-E 3 API 依據 prompt 生成圖像
    """
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("請設定 OPENAI_API_KEY 環境變數或透過 --api-key 傳入。")

    url = "https://api.openai.com/v1/images/generations"
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        b64_img = data["data"][0]["b64_json"]
        return base64.b64decode(b64_img)

def call_agy_agent(prompt, image_path):
    """
    調用本地 Antigravity (agy) CLI / Agent 進行生成
    """
    cmd = ["agy", "--prompt", prompt, "--file", image_path]
    print(f"  執行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"agy agent 執行失敗: {result.stderr}")
    return result.stdout.encode("utf-8")

def call_mock_agent(item, prompt, output_path):
    """
    測試用 Mock Agent：生成帶有主題色塊與文字排版的 SVG 格式示意圖，
    模擬上下分割構圖（FB 分割海報視覺）或預覽效果，便於零成本驗證整體工作流程。
    """
    theme = item.get("theme", "Photo")
    title = item.get("title", "")
    subtheme = item.get("subtheme", "")
    
    # 建立現代感 SVG 海報
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1066" width="800" height="1066">
  <defs>
    <linearGradient id="gradTop" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e293b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f172a;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradArt" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#f8fafc;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e2e8f0;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="800" height="1066" fill="#0f172a"/>

  <!-- Upper Half: Photographic Subject Header -->
  <rect x="30" y="30" width="740" height="480" rx="12" fill="url(#gradTop)"/>
  <circle cx="400" cy="270" r="140" fill="#334155" opacity="0.4"/>
  <circle cx="400" cy="270" r="90" fill="#475569" opacity="0.5"/>
  <text x="400" y="240" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="28" fill="#38bdf8" text-anchor="middle" font-weight="600">
    [ ORIGINAL PHOTO MOOD ]
  </text>
  <text x="400" y="280" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" fill="#f8fafc" text-anchor="middle">
    {theme}
  </text>
  <text x="400" y="320" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="16" fill="#94a3b8" text-anchor="middle">
    {title} • {subtheme}
  </text>

  <!-- Divider Bar -->
  <line x1="40" y1="535" x2="760" y2="535" stroke="#38bdf8" stroke-width="2" stroke-dasharray="8 6"/>

  <!-- Lower Half: Abstract / Risograph Minimalist Interpretation -->
  <rect x="30" y="555" width="740" height="480" rx="12" fill="url(#gradArt)" filter="url(#shadow)"/>
  
  <!-- Minimalist Geometric Art elements -->
  <circle cx="280" cy="740" r="110" fill="#f43f5e" opacity="0.85"/>
  <rect x="360" y="660" width="160" height="200" fill="#0ea5e9" opacity="0.85" rx="8" transform="rotate(15 440 760)"/>
  <polygon points="560,820 660,650 720,820" fill="#f59e0b" opacity="0.85"/>
  <path d="M 120 880 Q 400 680 680 880" stroke="#0f172a" stroke-width="5" fill="none" stroke-linecap="round"/>

  <!-- Poster Typography / Applied Prompt Info -->
  <text x="60" y="605" font-family="Courier, monospace" font-size="14" fill="#64748b" font-weight="bold">AI AGENT: MOCK GENERATOR (SIMULATION)</text>
  <text x="60" y="630" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="20" fill="#0f172a" font-weight="bold">
    AI REINTERPRETATION: {subtheme or theme}
  </text>
  <text x="60" y="990" font-family="Courier, monospace" font-size="12" fill="#475569">
    Prompt Style: Split Composition / Minimalist Graphic Form
  </text>
  <text x="60" y="1010" font-family="Courier, monospace" font-size="11" fill="#94a3b8">
    Applied: {prompt[:80]}...
  </text>
</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return output_path

# ================= 藝廊 HTML 產生器 =================

def generate_gallery_html(manifest_items, output_dir, prompt, agent_name):
    html_file = os.path.join(output_dir, "index.html")
    
    cards_html = []
    for item in manifest_items:
        # 確保相對於 output_dir 的路徑正確，直接計算相對於 base_dir 的路徑
        orig_filename = item["filename"]
        source_folder = "flickr" if "flickr" in item["id"] else "unsplash"
        orig_rel = f"../../photos/{source_folder}/{orig_filename}"
        gen_file = item.get("generated_file")
        gen_rel = os.path.basename(gen_file) if gen_file else ""
        
        cards_html.append(f"""
        <div class="gallery-card" data-source="{item.get('source', '')}" data-theme="{item.get('theme', '')}">
            <div class="card-header">
                <span class="badge badge-source">{item.get('source', '')}</span>
                <span class="badge badge-theme">{item.get('theme', '')}</span>
            </div>
            <h3 class="card-title">{item.get('title', '')}</h3>
            <p class="card-subtitle">{item.get('subtheme', '')}</p>
            
            <div class="image-comparison">
                <div class="image-box">
                    <span class="image-tag">原始照片 (Original)</span>
                    <img src="{orig_rel}" alt="Original" loading="lazy">
                </div>
                <div class="image-box">
                    <span class="image-tag tag-generated">AI 生成 ({agent_name})</span>
                    <img src="{gen_rel}" alt="Generated" loading="lazy">
                </div>
            </div>
        </div>
        """)
        
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Prompt Gallery — 20 Photos Showcase</title>
    <style>
        :root {{
            --bg: #090d16;
            --card-bg: #131b2e;
            --border: #1e293b;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.2);
            --accent-green: #34d399;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 2rem;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 2.5rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border);
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.8rem;
        }}
        .prompt-banner {{
            background: #0f172a;
            border: 1px solid #1e293b;
            border-left: 4px solid var(--accent);
            padding: 1.2rem 1.5rem;
            border-radius: 8px;
            text-align: left;
            margin: 1.5rem auto;
            max-width: 900px;
        }}
        .prompt-banner strong {{ color: var(--accent); }}
        .prompt-banner p {{ font-family: monospace; font-size: 0.95rem; color: #cbd5e1; margin-top: 0.4rem; }}
        
        .filter-bar {{
            display: flex;
            justify-content: center;
            gap: 0.8rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }}
        .filter-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 0.5rem 1.2rem;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--accent);
            color: #090d16;
            font-weight: bold;
            box-shadow: 0 0 12px var(--accent-glow);
        }}
        
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 2rem;
        }}
        .gallery-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.2rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .gallery-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            border-color: #334155;
        }}
        .card-header {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.8rem;
        }}
        .badge {{
            font-size: 0.75rem;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-weight: 600;
        }}
        .badge-source {{ background: #1e293b; color: #38bdf8; }}
        .badge-theme {{ background: #312e81; color: #c7d2fe; }}
        .card-title {{ font-size: 1.15rem; margin-bottom: 0.2rem; }}
        .card-subtitle {{ font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem; }}
        
        .image-comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.8rem;
        }}
        .image-box {{
            position: relative;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            aspect-ratio: 3/4;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .image-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .image-tag {{
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(4px);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #fff;
        }}
        .tag-generated {{
            background: rgba(14, 165, 233, 0.85);
            color: #fff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AI Photo Reimagining Gallery</h1>
            <p style="color: var(--text-muted);">20 Photos (10 Flickr + 10 Unsplash) across 10 Distinct Themes</p>
            <div class="prompt-banner">
                <div><strong>調用 AI Agent:</strong> {agent_name.upper()} &nbsp;|&nbsp; <strong>生成時間:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                <strong>套用 Prompt:</strong>
                <p>{prompt}</p>
            </div>
            
            <div class="filter-bar">
                <button class="filter-btn active" onclick="filterGallery('all')">全部 (20)</button>
                <button class="filter-btn" onclick="filterGallery('Flickr')">我的 Flickr (10)</button>
                <button class="filter-btn" onclick="filterGallery('Unsplash')">Unsplash 代表作 (10)</button>
            </div>
        </header>
        
        <div class="gallery-grid" id="galleryGrid">
            {"".join(cards_html)}
        </div>
    </div>
    
    <script>
        function filterGallery(source) {{
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            
            const cards = document.querySelectorAll('.gallery-card');
            cards.forEach(card => {{
                if (source === 'all') {{
                    card.style.display = 'block';
                }} else {{
                    const s = card.getAttribute('data-source');
                    card.style.display = s.includes(source) ? 'block' : 'none';
                }}
            }});
        }}
    </script>
</body>
</html>"""
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✓ 視覺化比對藝廊已生成: {html_file}")
    return html_file

# ================= 主要入口 =================

def main():
    parser = argparse.ArgumentParser(description="批次使用 AI Agent 套用 Prompt 生成 20 張相片藝廊")
    parser.add_argument("--prompt", type=str, default="", help="欲套用的 AI Prompt 提示詞")
    parser.add_argument("--style", type=str, default="fb_split_poster", choices=list(STYLE_PRESETS.keys()),
                        help="內建風格預設範本 (fb_split_poster, cinematic_film, cyberpunk_neon, ghibli_watercolor)")
    parser.add_argument("--agent", type=str, default="mock", choices=["mock", "gemini", "openai", "agy"],
                        help="欲調用的 AI Agent (mock, gemini, openai, agy)")
    parser.add_argument("--api-key", type=str, default="", help="AI Agent API Key (可透過環境變數傳入)")
    parser.add_argument("--manifest", type=str, default="photos_manifest.json", help="照片清單檔案")
    parser.add_argument("--output-dir", type=str, default="", help="輸出成果資料夾")
    
    args = parser.parse_args()
    
    # 決定輸出資料夾
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = args.output_dir or os.path.join(base_dir, "generated", args.agent)
    os.makedirs(output_dir, exist_ok=True)
    
    # 讀取相片清單
    manifest_path = os.path.join(base_dir, args.manifest)
    items = load_manifest(manifest_path)
    print(f"載入 {len(items)} 張代表照片 (10 Flickr + 10 Unsplash)")
    
    # 決定 Prompt
    base_prompt = args.prompt or STYLE_PRESETS[args.style]
    print(f"\n=======================================================")
    print(f"AI Agent: {args.agent}")
    print(f"風格模式: {args.style}")
    print(f"基礎 Prompt: {base_prompt}")
    print(f"輸出目錄: {output_dir}")
    print(f"=======================================================\n")
    
    # 批次處理 20 張照片
    for idx, item in enumerate(items, 1):
        subject = f"{item['theme']} - {item['subtheme']} ({item['title']})"
        full_prompt = base_prompt.format(subject=subject) if "{subject}" in base_prompt else f"{base_prompt}, based on scene: {subject}"
        
        orig_filename = item["filename"]
        out_ext = ".svg" if args.agent == "mock" else ".png"
        gen_filename = f"gen_{os.path.splitext(orig_filename)[0]}{out_ext}"
        out_path = os.path.join(output_dir, gen_filename)
        
        print(f"[{idx}/20] 處理 [{item['theme']}] {item['title']}...")
        
        if args.agent == "mock":
            call_mock_agent(item, full_prompt, out_path)
            item["generated_file"] = out_path
        elif args.agent == "gemini":
            img_bytes = call_gemini_agent(full_prompt, item["local_path"], args.api_key)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            item["generated_file"] = out_path
        elif args.agent == "openai":
            img_bytes = call_openai_agent(full_prompt, item["local_path"], args.api_key)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            item["generated_file"] = out_path
        elif args.agent == "agy":
            img_bytes = call_agy_agent(full_prompt, item["local_path"])
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            item["generated_file"] = out_path
            
        print(f"  ✓ 生成完成 -> {gen_filename}")
        
    # 生成 HTML 藝廊
    generate_gallery_html(items, output_dir, base_prompt, args.agent)
    print("\n🎉 全部 20 張相片生成與比對藝廊已成功建立！")

if __name__ == "__main__":
    main()
