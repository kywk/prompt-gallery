import os
import json
import urllib.request

FLICKR_PHOTOS = [
    {
        "id": "flickr_01_portrait",
        "theme": "人像攝影 (Portrait)",
        "subtheme": "和服少女・京都夢",
        "title": "0001_original",
        "source": "Flickr (kywk)",
        "album": "京都 夢 (17.12.07)",
        "url": "https://live.staticflickr.com/4593/25260619398_2726c79f8d_b.jpg",
        "filename": "flickr_01_portrait_kyoto.jpg"
    },
    {
        "id": "flickr_02_landscape",
        "theme": "高山風景 (Landscape)",
        "subtheme": "雲海雲瀑・聖境北大武",
        "title": "北大武",
        "source": "Flickr (kywk)",
        "album": "聖境．北大武 (15.03.22)",
        "url": "https://live.staticflickr.com/7716/17388580695_1e0d61e4eb_b.jpg",
        "filename": "flickr_02_landscape_dawu.jpg"
    },
    {
        "id": "flickr_03_street",
        "theme": "街頭紀實 (Street)",
        "subtheme": "香港夜行・FlashMob",
        "title": "141226-2139_0414",
        "source": "Flickr (kywk)",
        "album": "FlashMob HK",
        "url": "https://live.staticflickr.com/8605/15933468627_e3cf744a03_b.jpg",
        "filename": "flickr_03_street_hk.jpg"
    },
    {
        "id": "flickr_04_documentary",
        "theme": "運動紀實 (Documentary)",
        "subtheme": "富士山馬拉松賽事",
        "title": "141126-0129-0980",
        "source": "Flickr (kywk)",
        "album": "Mt.Fuji marathon, 2014",
        "url": "https://live.staticflickr.com/7574/16087639662_a2643dff5e_b.jpg",
        "filename": "flickr_04_documentary_marathon.jpg"
    },
    {
        "id": "flickr_05_travel",
        "theme": "文化旅遊 (Travel)",
        "subtheme": "日式歷史旅館・日光遺產",
        "title": "日光 東觀莊 141126",
        "source": "Flickr (kywk)",
        "album": "Nikko 日光 世界遺產",
        "url": "https://live.staticflickr.com/7535/15853719578_79043109b9_b.jpg",
        "filename": "flickr_05_travel_nikko.jpg"
    },
    {
        "id": "flickr_06_pet",
        "theme": "動物寵物 (Pet / Animal)",
        "subtheme": "草地狂奔的毛孩",
        "title": "141020_0759-569",
        "source": "Flickr (kywk)",
        "album": "奔跑 娜呀娜呀 (14.10.20)",
        "url": "https://live.staticflickr.com/8615/15213498153_2ee385e257_b.jpg",
        "filename": "flickr_06_pet_nayana.jpg"
    },
    {
        "id": "flickr_07_architecture",
        "theme": "建築人文 (Architecture & Interior)",
        "subtheme": "溫潤木質書香・台中魚麗書店",
        "title": "131019_1552-t351.jpg",
        "source": "Flickr (kywk)",
        "album": "台中 魚麗書店",
        "url": "https://live.staticflickr.com/3669/11973864205_7dba20e90f_b.jpg",
        "filename": "flickr_07_architecture_bookstore.jpg"
    },
    {
        "id": "flickr_08_food",
        "theme": "食物特寫 (Food & Macro)",
        "subtheme": "手沖烘焙咖啡豆靜物",
        "title": "13cafe",
        "source": "Flickr (kywk)",
        "album": "台中 13 咖啡",
        "url": "https://live.staticflickr.com/7070/6969869023_54b23b1b80_b.jpg",
        "filename": "flickr_08_food_coffee.jpg"
    },
    {
        "id": "flickr_09_nature",
        "theme": "自然光影 (Nature & Lake)",
        "subtheme": "西湖晨曦與秋色紅葉台",
        "title": "西湖 紅葉台露營區 141129",
        "source": "Flickr (kywk)",
        "album": "富士山．河口湖",
        "url": "https://live.staticflickr.com/7555/16021700536_04fb9cca47_b.jpg",
        "filename": "flickr_09_nature_lake_saiko.jpg"
    },
    {
        "id": "flickr_10_adventure",
        "theme": "海島探險 (Adventure & Coast)",
        "subtheme": "薄荷島白沙灘與蔚藍海岸",
        "title": "virgin island",
        "source": "Flickr (kywk)",
        "album": "Bohol holiday",
        "url": "https://live.staticflickr.com/8544/8674923710_2fd0626872_b.jpg",
        "filename": "flickr_10_adventure_bohol.jpg"
    }
]

UNSPLASH_PHOTOS = [
    {
        "id": "unsplash_01_portrait",
        "theme": "人像攝影 (Portrait)",
        "subtheme": "自然光時尚肖像",
        "title": "Natural Light Fashion Portrait",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_01_portrait.jpg"
    },
    {
        "id": "unsplash_02_landscape",
        "theme": "壯麗風景 (Landscape)",
        "subtheme": "優美勝地山川與峽灣湖泊",
        "title": "Yosemite Valley Lake & Mountains",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_02_landscape.jpg"
    },
    {
        "id": "unsplash_03_street",
        "theme": "街拍光影 (Street Photography)",
        "subtheme": "霓虹閃爍雨夜都市街頭",
        "title": "Rainy Neon City Night Street",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1514565131-fce0801e5785?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_03_street.jpg"
    },
    {
        "id": "unsplash_04_food",
        "theme": "精緻美食 (Food & Dessert)",
        "subtheme": "法式手作烘焙水果派",
        "title": "Artisan Fruit Tart & Pastry",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_04_food.jpg"
    },
    {
        "id": "unsplash_05_documentary",
        "theme": "職人紀實 (Documentary)",
        "subtheme": "木工陶藝手作工坊專注身影",
        "title": "Artisan Craftsman Workshop",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_05_documentary.jpg"
    },
    {
        "id": "unsplash_06_macro",
        "theme": "微距特寫 (Macro Close-up)",
        "subtheme": "綠葉上晶瑩晨露與光斑",
        "title": "Dew Drops on Emerald Green Leaf",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1533038590840-1cde6e668a91?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_06_macro.jpg"
    },
    {
        "id": "unsplash_07_architecture",
        "theme": "現代建築 (Architecture)",
        "subtheme": "摩天幾何玻璃帷幕光影",
        "title": "Modern Skyscraper Architectural Facade",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_07_architecture.jpg"
    },
    {
        "id": "unsplash_08_wildlife",
        "theme": "野生動物 (Wildlife)",
        "subtheme": "雪地中的紅狐特寫",
        "title": "Red Fox Close-up in Wilderness",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_08_wildlife.jpg"
    },
    {
        "id": "unsplash_09_travel",
        "theme": "旅行探險 (Travel & Adventure)",
        "subtheme": "海灘日落熱氣球壯觀遠眺",
        "title": "Tropical Ocean Beach Sunset Horizon",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_09_travel.jpg"
    },
    {
        "id": "unsplash_10_night",
        "theme": "夜景星空 (Night & Astrophotography)",
        "subtheme": "荒野高山之上的璀璨銀河",
        "title": "Milky Way Galaxy Night Sky",
        "source": "Unsplash",
        "url": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?auto=format&fit=crop&w=1200&q=80",
        "filename": "unsplash_10_night.jpg"
    }
]

def download_item(item, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, item["filename"])
    print(f"Downloading [{item['theme']}] {item['title']} -> {item['filename']}...")
    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        content = resp.read()
    with open(target_path, "wb") as f:
        f.write(content)
    item["local_path"] = os.path.relpath(target_path)
    item["size_bytes"] = len(content)
    print(f"  ✓ Saved {len(content)} bytes to {target_path}")

def main():
    base_dir = "/home/kywk/Projects/prompt-gallery"
    flickr_dir = os.path.join(base_dir, "photos", "flickr")
    unsplash_dir = os.path.join(base_dir, "photos", "unsplash")
    
    all_items = []
    print("=== Downloading 10 Flickr Photos ===")
    for item in FLICKR_PHOTOS:
        download_item(item, flickr_dir)
        all_items.append(item)
        
    print("\n=== Downloading 10 Unsplash Photos ===")
    for item in UNSPLASH_PHOTOS:
        download_item(item, unsplash_dir)
        all_items.append(item)
        
    manifest_path = os.path.join(base_dir, "photos_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Completed downloading 20 photos. Manifest saved to {manifest_path}")

if __name__ == "__main__":
    main()
