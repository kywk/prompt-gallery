#!/bin/bash
mkdir -p prompts/second-life/generated

for f in photos/flickr/*.jpg photos/unsplash/*.jpg; do
    base=$(basename "$f")
    target="prompts/second-life/generated/gen_${base}"
    
    if [ ! -f "$target" ]; then
        echo "Missing $target, generating placeholder..."
        # Extract title from manifest or just use filename
        name="${base%.*}"
        
        # Create a 900x1200 split image: 
        # Top half (900x600): The original photo resized/cropped
        # Bottom half (900x600): A minimalist abstract gradient/solid with text
        
        # 1. Top half: Original image, resize and crop to 900x600
        convert "$f" -resize 900x600^ -gravity center -extent 900x600 /tmp/top_$$.jpg
        
        # 2. Bottom half: Minimalist geometric placeholder
        convert -size 900x600 canvas:"#f4f4f5" \
            -fill "#e2b17a" -draw "circle 450,300 450,150" \
            -fill "#121316" -pointsize 48 -gravity center -annotate +0+200 "API RATE LIMIT REACHED" \
            -pointsize 24 -fill "#555" -annotate +0+250 "Placeholder for $name" \
            /tmp/bottom_$$.jpg
            
        # 3. Append them vertically
        convert /tmp/top_$$.jpg /tmp/bottom_$$.jpg -append "$target"
        
        rm -f /tmp/top_$$.jpg /tmp/bottom_$$.jpg
    fi
done
