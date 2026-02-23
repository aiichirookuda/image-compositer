from pathlib import Path
from PIL import Image

A_DIR = Path("a")
B_DIR = Path("b")
C_DIR = Path("c")
OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

def list_images(dir_path: Path):
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    return sorted([p for p in dir_path.iterdir() if p.suffix.lower() in exts])

a_files = list_images(A_DIR)
b_files = list_images(B_DIR)
c_files = list_images(C_DIR)

if not a_files or not b_files or not c_files:
    raise SystemExit("a/b/c の各フォルダに画像が入っているか確認してください。")

count = 0

for a_path in a_files:
    a_img = Image.open(a_path).convert("RGBA")
    base_w, base_h = a_img.size

    for b_path in b_files:
        b_img = Image.open(b_path).convert("RGBA")
        if b_img.size != (base_w, base_h):
            b_img = b_img.resize((base_w, base_h), Image.Resampling.LANCZOS)

        for c_path in c_files:
            c_img = Image.open(c_path).convert("RGBA")
            if c_img.size != (base_w, base_h):
                c_img = c_img.resize((base_w, base_h), Image.Resampling.LANCZOS)

            # 合成（順番：a の上に b、さらに c）
            out = Image.alpha_composite(a_img, b_img)
            out = Image.alpha_composite(out, c_img)

            # ファイル名（例：a1_b2_c3.png）
            out_name = f"a{a_path.stem}_b{b_path.stem}_c{c_path.stem}.png"
            out.save(OUT_DIR / out_name)

            count += 1

print(f"Done: {count} files -> {OUT_DIR.resolve()}")
