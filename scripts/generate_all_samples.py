import os
import json

def generate_svg_for_style(item, style_id, prompt_text, out_path):
    theme = item.get("theme", "")
    title = item.get("title", "")
    subtheme = item.get("subtheme", "")
    source = item.get("source", "")
    
    if style_id == "fb-split-poster":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1066" width="800" height="1066">
  <defs>
    <linearGradient id="gradTop" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e293b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f172a;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradArt" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#fefce8;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#fef08a;stop-opacity:0.8" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.25"/>
    </filter>
  </defs>

  <rect width="800" height="1066" fill="#0b0f19"/>
  <!-- Upper Half: Photographic Subject -->
  <rect x="30" y="30" width="740" height="480" rx="12" fill="url(#gradTop)"/>
  <circle cx="400" cy="270" r="140" fill="#334155" opacity="0.4"/>
  <circle cx="400" cy="270" r="85" fill="#38bdf8" opacity="0.25"/>
  <text x="400" y="240" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="28" fill="#38bdf8" text-anchor="middle" font-weight="700">
    [ PHOTOGRAPHIC SUBJECT ]
  </text>
  <text x="400" y="280" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" fill="#f8fafc" text-anchor="middle">
    {theme}
  </text>
  <text x="400" y="320" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="16" fill="#94a3b8" text-anchor="middle">
    {title} • {subtheme}
  </text>

  <!-- Split Divider -->
  <line x1="40" y1="535" x2="760" y2="535" stroke="#f43f5e" stroke-width="3" stroke-dasharray="10 6"/>

  <!-- Lower Half: Abstract / Risograph Minimalist Interpretation -->
  <rect x="30" y="555" width="740" height="480" rx="12" fill="url(#gradArt)" filter="url(#shadow)"/>
  
  <circle cx="260" cy="760" r="120" fill="#f43f5e" opacity="0.85"/>
  <rect x="370" y="670" width="160" height="210" fill="#0284c7" opacity="0.85" rx="12" transform="rotate(12 450 775)"/>
  <polygon points="560,840 670,660 730,840" fill="#f59e0b" opacity="0.9"/>
  <path d="M 100 890 Q 400 700 700 890" stroke="#0f172a" stroke-width="6" fill="none" stroke-linecap="round"/>

  <!-- Editorial Typography -->
  <text x="60" y="605" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#e11d48" font-weight="900" letter-spacing="3">AI SPLIT POSTER SERIES</text>
  <text x="60" y="635" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" fill="#0f172a" font-weight="800">
    REINTERPRETED SILHOUETTE: {subtheme or theme}
  </text>
  <text x="60" y="990" font-family="Courier, monospace" font-size="13" fill="#334155" font-weight="600">
    SWISS EDITORIAL LAYOUT • RISOGRAPH PRINT AESTHETIC
  </text>
  <text x="60" y="1012" font-family="Courier, monospace" font-size="11" fill="#64748b">
    Source: {source} | Subject: {title}
  </text>
</svg>"""

    elif style_id == "cinematic-portra":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1066" width="800" height="1066">
  <defs>
    <radialGradient id="halation" cx="50%" cy="40%" r="60%">
      <stop offset="0%" style="stop-color:#f59e0b;stop-opacity:0.35" />
      <stop offset="60%" style="stop-color:#78350f;stop-opacity:0.1" />
      <stop offset="100%" style="stop-color:#000000;stop-opacity:0" />
    </radialGradient>
    <linearGradient id="filmBase" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#291e13;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#120c07;stop-opacity:1" />
    </linearGradient>
  </defs>

  <rect width="800" height="1066" fill="#0a0705"/>
  
  <!-- Film Sprocket Border Top & Bottom -->
  <rect x="0" y="0" width="800" height="70" fill="#000"/>
  <rect x="0" y="996" width="800" height="70" fill="#000"/>
  
  <!-- Film negative Frame -->
  <rect x="35" y="85" width="730" height="895" rx="6" fill="url(#filmBase)" stroke="#78350f" stroke-width="2"/>
  <circle cx="400" cy="450" r="320" fill="url(#halation)"/>
  
  <!-- Atmosphere silhouette -->
  <ellipse cx="400" cy="520" rx="200" ry="180" fill="#451a03" opacity="0.6"/>
  <circle cx="400" cy="480" r="110" fill="#d97706" opacity="0.3"/>

  <!-- Grain & Typography -->
  <text x="400" y="340" font-family="'Courier New', Courier, monospace" font-size="14" fill="#d97706" letter-spacing="4" text-anchor="middle">
    35MM ANALOG COLOR NEGATIVE • 400 ISO
  </text>
  <text x="400" y="420" font-family="Georgia, serif" font-size="34" fill="#fef3c7" text-anchor="middle" font-weight="bold">
    {theme}
  </text>
  <text x="400" y="470" font-family="Georgia, serif" font-size="20" fill="#fde68a" text-anchor="middle" font-style="italic">
    {subtheme}
  </text>
  <text x="400" y="520" font-family="-apple-system, sans-serif" font-size="15" fill="#a16207" text-anchor="middle">
    Original: {title} ({source})
  </text>

  <!-- Film Edge markings -->
  <text x="45" y="50" font-family="'Courier New', Courier, monospace" font-size="16" fill="#d97706" font-weight="bold">
    KODAK PORTRA 400 &gt;&gt; 24A
  </text>
  <text x="620" y="50" font-family="'Courier New', Courier, monospace" font-size="16" fill="#d97706" font-weight="bold">
    SAFETY FILM
  </text>
  <text x="45" y="1040" font-family="'Courier New', Courier, monospace" font-size="14" fill="#a16207">
    WONG KAR-WAI AESTHETIC • GOLDEN HOUR HALATION
  </text>
  <text x="640" y="1040" font-family="'Courier New', Courier, monospace" font-size="14" fill="#a16207">
    f/1.4 PRIME
  </text>
</svg>"""

    elif style_id == "cyberpunk-neon":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1066" width="800" height="1066">
  <defs>
    <radialGradient id="cyberGlow" cx="50%" cy="45%" r="65%">
      <stop offset="0%" style="stop-color:#ec4899;stop-opacity:0.4" />
      <stop offset="50%" style="stop-color:#06b6d4;stop-opacity:0.25" />
      <stop offset="100%" style="stop-color:#020617;stop-opacity:0" />
    </radialGradient>
  </defs>

  <rect width="800" height="1066" fill="#020617"/>
  <!-- Perspective Cyber Grid -->
  <line x1="0" y1="850" x2="800" y2="850" stroke="#06b6d4" stroke-width="2" opacity="0.4"/>
  <line x1="0" y1="920" x2="800" y2="920" stroke="#06b6d4" stroke-width="3" opacity="0.6"/>
  <line x1="0" y1="1000" x2="800" y2="1000" stroke="#ec4899" stroke-width="4" opacity="0.8"/>
  <line x1="400" y1="780" x2="0" y2="1066" stroke="#06b6d4" stroke-width="2" opacity="0.5"/>
  <line x1="400" y1="780" x2="250" y2="1066" stroke="#06b6d4" stroke-width="2" opacity="0.5"/>
  <line x1="400" y1="780" x2="550" y2="1066" stroke="#06b6d4" stroke-width="2" opacity="0.5"/>
  <line x1="400" y1="780" x2="800" y2="1066" stroke="#06b6d4" stroke-width="2" opacity="0.5"/>

  <!-- Neon Core -->
  <circle cx="400" cy="450" r="280" fill="url(#cyberGlow)"/>
  <circle cx="400" cy="420" r="140" fill="none" stroke="#ec4899" stroke-width="4" opacity="0.8"/>
  <polygon points="400,280 500,480 300,480" fill="none" stroke="#06b6d4" stroke-width="3" opacity="0.9"/>

  <!-- Cyber Glitch Texts -->
  <text x="400" y="240" font-family="'Courier New', monospace" font-size="14" fill="#06b6d4" letter-spacing="6" text-anchor="middle" font-weight="bold">
    SYSTEM // NEO-TOKYO PROTOCOL
  </text>
  <text x="400" y="550" font-family="-apple-system, sans-serif" font-size="30" fill="#f8fafc" text-anchor="middle" font-weight="900" letter-spacing="2">
    {theme}
  </text>
  <text x="400" y="590" font-family="-apple-system, sans-serif" font-size="20" fill="#ec4899" text-anchor="middle" font-weight="bold">
    {subtheme}
  </text>
  <text x="400" y="630" font-family="'Courier New', monospace" font-size="14" fill="#94a3b8" text-anchor="middle">
    REF: {title} [{source}]
  </text>
  
  <text x="40" y="70" font-family="'Courier New', monospace" font-size="13" fill="#ec4899">VOLUMETRIC FOG // CHROMATIC</text>
  <text x="610" y="70" font-family="'Courier New', monospace" font-size="13" fill="#06b6d4">BLADE RUNNER 2049</text>
</svg>"""

    elif style_id == "ghibli-watercolor":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1066" width="800" height="1066">
  <defs>
    <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#38bdf8;stop-opacity:1" />
      <stop offset="60%" style="stop-color:#bae6fd;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#fef08a;stop-opacity:0.9" />
    </linearGradient>
    <linearGradient id="hillGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#4ade80;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#166534;stop-opacity:1" />
    </linearGradient>
  </defs>

  <rect width="800" height="1066" fill="#fefce8"/>
  <!-- Sky -->
  <rect x="25" y="25" width="750" height="1016" rx="16" fill="url(#skyGrad)"/>
  
  <!-- Fluffy Anime Cumulus Clouds -->
  <circle cx="220" cy="380" r="140" fill="#ffffff" opacity="0.95"/>
  <circle cx="360" cy="310" r="170" fill="#ffffff" opacity="0.98"/>
  <circle cx="520" cy="360" r="150" fill="#ffffff" opacity="0.95"/>
  <circle cx="620" cy="420" r="120" fill="#ffffff" opacity="0.9"/>
  <circle cx="370" cy="230" r="110" fill="#ffffff" opacity="0.95"/>

  <!-- Rolling Green Hills -->
  <path d="M 25 780 Q 200 660 450 730 T 775 750 L 775 1041 L 25 1041 Z" fill="url(#hillGrad)"/>
  <path d="M 25 860 Q 300 770 580 820 T 775 840 L 775 1041 L 25 1041 Z" fill="#15803d" opacity="0.7"/>

  <!-- Warm Title Card -->
  <rect x="120" y="470" width="560" height="170" rx="14" fill="#ffffff" opacity="0.9" stroke="#fed7aa" stroke-width="2"/>
  <text x="400" y="520" font-family="'PingFang TC', 'Microsoft JhengHei', sans-serif" font-size="28" fill="#1e3a8a" text-anchor="middle" font-weight="bold">
    {theme}
  </text>
  <text x="400" y="565" font-family="'PingFang TC', 'Microsoft JhengHei', sans-serif" font-size="20" fill="#047857" text-anchor="middle" font-weight="600">
    {subtheme}
  </text>
  <text x="400" y="605" font-family="Courier, monospace" font-size="13" fill="#64748b" text-anchor="middle">
    Original: {title} ({source})
  </text>

  <text x="50" y="70" font-family="sans-serif" font-size="14" fill="#0369a1" font-weight="bold">GHIBLI WATERCOLOR SERIES</text>
  <text x="50" y="1000" font-family="sans-serif" font-size="13" fill="#ffffff" font-weight="bold">HAYAO MIYAZAKI INSPIRED • SUMMER NOSTALGIA</text>
</svg>"""
    else:
        svg = "<svg></svg>"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    base_dir = "/home/kywk/Projects/prompt-gallery"
    manifest_path = os.path.join(base_dir, "photos_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        photos = json.load(f)
        
    styles = ["fb-split-poster", "cinematic-portra", "cyberpunk-neon", "ghibli-watercolor"]
    
    for style_id in styles:
        out_dir = os.path.join(base_dir, "prompts", style_id, "generated")
        os.makedirs(out_dir, exist_ok=True)
        print(f"Generating 20 images for {style_id}...")
        for p in photos:
            gen_filename = f"gen_{os.path.splitext(p['filename'])[0]}.svg"
            gen_path = os.path.join(out_dir, gen_filename)
            generate_svg_for_style(p, style_id, "", gen_path)
        print(f"  ✓ 20 images generated for {style_id}")

if __name__ == "__main__":
    main()
