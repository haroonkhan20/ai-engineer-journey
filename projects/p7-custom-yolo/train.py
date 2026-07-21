# train.py
# Train YOLO11 on custom water bottle + phone dataset
# Built by: Mohammed Haroon Khan

from ultralytics import YOLO

# ── LOAD PRETRAINED MODEL ─────────────────────
# yolo11n.pt = YOLO11 Nano
# Downloads automatically on first run (~6MB)
# Pretrained on COCO dataset — 80 classes
# We're doing TRANSFER LEARNING:
# Instead of learning from scratch (random weights)
# we START from weights that already understand
# edges, shapes, textures — then fine-tune for
# our specific classes (phone, water_bottle)
model = YOLO("yolo11n.pt")

# ── TRAIN ─────────────────────────────────────
results = model.train(

    # Path to your data.yaml
    # Use raw string r"..." to handle Windows backslashes
    data=r"C:\Users\haroo\Desktop\ai-engineer-journey\water-bottle-phone-detector-1\data.yaml",

    # 50 passes through entire dataset
    epochs=50,

    # Resize all images to 640x640
    # YOLO always needs fixed size input
    imgsz=640,

    # Process 8 images at once
    # Reduced to 8 for CPU training — less RAM usage
    batch=8,

    # Stop training if no improvement for 15 epochs
    # Saves time — no point continuing if stuck
    patience=15,

    # Save results here:
    # runs/detect/bottle_phone_v1/
    name="bottle_phone_v1",

    # CPU training — change to 0 if you have NVIDIA GPU
    device="cpu",

    # ── AUGMENTATION ──────────────────────────
    # Randomly flip left-right — 50% chance
    # Bottle looks same mirrored — valid augmentation
    fliplr=0.5,

    # Never flip upside down — bottle upside down
    # is not a real scenario we want to detect
    flipud=0.0,

    # Random rotation up to ±10 degrees
    # Handles slightly tilted camera angles
    degrees=10.0,

    # Random brightness variation up to 40%
    # Handles different lighting conditions
    # Bright room, dim room, near window etc.
    hsv_v=0.4,

    # Mosaic augmentation — combines 4 images into 1
    # Forces model to detect objects at different scales
    # and positions — very powerful for small datasets
    mosaic=1.0,
)

print("\nTraining complete!")
print(f"Best weights saved to: {results.save_dir}/weights/best.pt")
print(f"Last weights saved to: {results.save_dir}/weights/last.pt")