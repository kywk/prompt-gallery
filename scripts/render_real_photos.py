import os
import json
import subprocess

FONT_SANS = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/liberation/LiberationMono-Bold.ttf"

def process_fb_split_poster(orig_path, out_path, item):
    title = item.get("title", "SUBJECT")[:22].replace("'", "").replace('"', '').replace("$", "")
    theme = item.get("theme", "").split()[0].replace("'", "").replace('"', '')
    subtheme = item.get("subtheme", "")[:25].replace("'", "").replace('"', '')
    
    cmd = f"""
    magick "{orig_path}" -resize 800x533^ -gravity center -extent 800x533 /tmp/top.jpg
    magick "{orig_path}" -resize 800x533^ -gravity center -extent 800x533 \\
      -colorspace gray -edge 2 -negate -threshold 65% \\
      -fill "#faf5eb" -opaque white -fill "#c2410c" -opaque black \\
      -font "{FONT_SANS}" -pointsize 26 -fill "#1c1917" -gravity South -annotate +0+60 "SILHOUETTE: {title}" \\
      -font "{FONT_SANS}" -pointsize 18 -fill "#78350f" -gravity South -annotate +0+30 "{theme} • {subtheme}" \\
      -font "{FONT_MONO}" -pointsize 14 -fill "#9a3412" -gravity North -annotate +0+25 "SWISS EDITORIAL RISOGRAPH POSTER" \\
      /tmp/bottom.jpg
    magick -size 800x6 xc:"#f43f5e" /tmp/div.jpg
    magick /tmp/top.jpg /tmp/div.jpg /tmp/bottom.jpg -append "{out_path}"
    """
    subprocess.run(cmd, shell=True, check=True)

def process_cinematic_portra(orig_path, out_path, item):
    title = item.get("title", "SUBJECT")[:25].replace("'", "").replace('"', '')
    cmd = f"""
    magick "{orig_path}" -resize 740x940^ -gravity center -extent 740x940 \\
      -modulate 102,115,100 -level 3%,97%,1.05 \\
      -color-matrix "1.08 0 0  0 1.02 0  0 0 0.92" \\
      -bordercolor "#0a0705" -border 30x63 \\
      -font "{FONT_MONO}" -pointsize 16 -fill "#d97706" -gravity NorthWest -annotate +40+35 "KODAK PORTRA 400 >> 24A" \\
      -font "{FONT_MONO}" -pointsize 16 -fill "#d97706" -gravity NorthEast -annotate +40+35 "SAFETY FILM" \\
      -font "{FONT_MONO}" -pointsize 14 -fill "#a16207" -gravity SouthWest -annotate +40+35 "WONG KAR-WAI CINEMATIC COLOR" \\
      -font "{FONT_MONO}" -pointsize 14 -fill "#a16207" -gravity SouthEast -annotate +40+35 "35MM EXP 24" \\
      "{out_path}"
    """
    subprocess.run(cmd, shell=True, check=True)

def process_cyberpunk_neon(orig_path, out_path, item):
    title = item.get("title", "SUBJECT")[:25].replace("'", "").replace('"', '')
    cmd = f"""
    magick "{orig_path}" -resize 800x1066^ -gravity center -extent 800x1066 \\
      -modulate 95,145,100 -level 10%,92%,0.9 \\
      -color-matrix "0.85 0 0.4  0 0.95 0.2  0.3 0 1.2" \\
      -font "{FONT_MONO}" -pointsize 18 -fill "#06b6d4" -gravity NorthWest -annotate +40+40 "NEO-TOKYO PROTOCOL // 2049" \\
      -font "{FONT_MONO}" -pointsize 18 -fill "#ec4899" -gravity NorthEast -annotate +40+40 "CYBERPUNK CHROMATIC" \\
      -font "{FONT_SANS}" -pointsize 24 -fill "#f8fafc" -gravity SouthWest -annotate +40+45 "{title}" \\
      "{out_path}"
    """
    subprocess.run(cmd, shell=True, check=True)

def process_ghibli_watercolor(orig_path, out_path, item):
    title = item.get("title", "SUBJECT")[:25].replace("'", "").replace('"', '')
    theme = item.get("theme", "").split()[0].replace("'", "").replace('"', '')
    cmd = f"""
    magick "{orig_path}" -resize 800x1066^ -gravity center -extent 800x1066 \\
      -blur 0x1.2 -sharpen 0x1.5 -modulate 110,135,100 \\
      -color-matrix "1.02 0.05 0  0.03 1.05 0.02  0 0.05 1.02" \\
      -bordercolor "#fbfaf5" -border 24x24 \\
      -font "{FONT_SANS}" -pointsize 22 -fill "#1e3a8a" -gravity South -annotate +0+55 "{theme} • {title}" \\
      -font "{FONT_SANS}" -pointsize 15 -fill "#047857" -gravity South -annotate +0+30 "STUDIO GHIBLI WATERCOLOR INSPIRED" \\
      "{out_path}"
    """
    subprocess.run(cmd, shell=True, check=True)

def main():
    base_dir = "/home/kywk/Projects/prompt-gallery"
    manifest_path = os.path.join(base_dir, "photos_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        photos = json.load(f)
        
    styles = {
        "fb-split-poster": process_fb_split_poster,
        "cinematic-portra": process_cinematic_portra,
        "cyberpunk-neon": process_cyberpunk_neon,
        "ghibli-watercolor": process_ghibli_watercolor
    }
    
    for style_id, func in styles.items():
        out_dir = os.path.join(base_dir, "prompts", style_id, "generated")
        os.makedirs(out_dir, exist_ok=True)
        print(f"Generating photographic JPEG renders for {style_id}...")
        for p in photos:
            orig_filename = p["filename"]
            base_name = os.path.splitext(orig_filename)[0]
            gen_filename = f"gen_{base_name}.jpg"
            out_path = os.path.join(out_dir, gen_filename)
            
            # If subagent already generated this file as a high-res AI image, don't overwrite it!
            if os.path.exists(out_path) and os.path.getsize(out_path) > 500000:
                print(f"  Keeping high-res AI image: {gen_filename}")
                continue
                
            orig_source = "flickr" if "flickr" in p["id"] else "unsplash"
            orig_path = os.path.join(base_dir, "photos", orig_source, orig_filename)
            func(orig_path, out_path, p)
            
        print(f"  ✓ Finished {style_id}")

if __name__ == "__main__":
    main()
