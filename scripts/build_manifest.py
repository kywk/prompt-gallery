#!/usr/bin/env python3
"""
Scan all folders in prompts/*/prompt.md and compile prompts_index.json
for the static Showcase Gallery front-end.
"""

import os
import re
import json

def parse_markdown_frontmatter(content):
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_yaml = parts[1].strip()
            body = parts[2].strip()
            for line in raw_yaml.split("\n"):
                line = line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                # parse lists
                if v.startswith("[") and v.endswith("]"):
                    items = [it.strip().strip('"').strip("'") for it in v[1:-1].split(",") if it.strip()]
                    frontmatter[k] = items
                # parse booleans
                elif v.lower() == "true":
                    frontmatter[k] = True
                elif v.lower() == "false":
                    frontmatter[k] = False
                else:
                    frontmatter[k] = v.strip('"').strip("'")
                    
    # extract prompt code block
    prompt_match = re.search(r"```(?:text)?\s*(.*?)\s*```", body, re.DOTALL)
    prompt_text = prompt_match.group(1).strip() if prompt_match else ""
    
    return frontmatter, body, prompt_text

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_dir = os.path.join(base_dir, "prompts")
    photos_manifest_file = os.path.join(base_dir, "photos_manifest.json")
    
    with open(photos_manifest_file, "r", encoding="utf-8") as f:
        base_photos = json.load(f)

    prompts_list = []
    
    if os.path.exists(prompts_dir):
        for entry in sorted(os.listdir(prompts_dir)):
            p_folder = os.path.join(prompts_dir, entry)
            if not os.path.isdir(p_folder):
                continue
            md_file = os.path.join(p_folder, "prompt.md")
            if not os.path.exists(md_file):
                continue
                
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            meta, body, prompt_text = parse_markdown_frontmatter(content)
            slug = meta.get("id") or entry
            
            # Map generated photos
            gen_dir = os.path.join(p_folder, "generated")
            items = []
            for bp in base_photos:
                orig_file = bp["filename"]
                base_name = os.path.splitext(orig_file)[0]
                # Check for .png, .jpg, or .svg
                gen_file = None
                for ext in [".png", ".jpg", ".jpeg", ".svg"]:
                    candidate = f"gen_{base_name}{ext}"
                    if os.path.exists(os.path.join(gen_dir, candidate)):
                        gen_file = candidate
                        break
                        
                source_folder = "flickr" if "flickr" in bp["id"] else "unsplash"
                items.append({
                    "id": bp["id"],
                    "theme": bp["theme"],
                    "subtheme": bp["subtheme"],
                    "title": bp["title"],
                    "source": bp["source"],
                    "original_image": f"photos/{source_folder}/{orig_file}",
                    "generated_image": f"prompts/{entry}/generated/{gen_file}" if gen_file else None
                })
                
            prompts_list.append({
                "id": slug,
                "folder": entry,
                "title": meta.get("title", entry),
                "author": meta.get("author", "Unknown"),
                "source_url": meta.get("source_url", ""),
                "model": meta.get("model", "AI Diffusion"),
                "tags": meta.get("tags", []),
                "date": meta.get("date", ""),
                "summary": meta.get("summary", ""),
                "prompt_text": prompt_text,
                "markdown_body": body,
                "items": items
            })
            
    out_file = os.path.join(base_dir, "prompts_index.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(prompts_list, f, ensure_ascii=False, indent=2)
        
    js_file = os.path.join(base_dir, "prompts_data.js")
    with open(js_file, "w", encoding="utf-8") as f:
        f.write("window.PROMPTS_DATA = " + json.dumps(prompts_list, ensure_ascii=False, indent=2) + ";\n")
        
    print(f"✓ Scanned {len(prompts_list)} prompts. Index saved to {out_file} and {js_file}")

if __name__ == "__main__":
    main()
