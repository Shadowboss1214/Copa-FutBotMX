import os
import shutil
import random

IMAGES_DIR = "C:/blender_synthetic/images"
LABELS_DIR = "C:/blender_synthetic/labels_regression"
OUTPUT_DIR = "C:/blender_synthetic/dataset"

TRAIN_RATIO = 0.8

for split in ["train", "val"]:
    os.makedirs(f"{OUTPUT_DIR}/images/{split}", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/labels_regression/{split}", exist_ok=True)

imgs = [f for f in os.listdir(IMAGES_DIR)
        if f.endswith(".jpg") and
        os.path.exists(f"{LABELS_DIR}/{f.replace('.jpg','.txt')}")]

random.shuffle(imgs)
split_idx  = int(len(imgs) * TRAIN_RATIO)
train_imgs = imgs[:split_idx]
val_imgs   = imgs[split_idx:]

for split, files in [("train", train_imgs), ("val", val_imgs)]:
    for fname in files:
        shutil.copy(f"{IMAGES_DIR}/{fname}",
                    f"{OUTPUT_DIR}/images/{split}/{fname}")
        shutil.copy(f"{LABELS_DIR}/{fname.replace('.jpg','.txt')}",
                    f"{OUTPUT_DIR}/labels_regression/{split}/{fname.replace('.jpg','.txt')}")

print(f"✅ Train: {len(train_imgs)} | Val: {len(val_imgs)}")