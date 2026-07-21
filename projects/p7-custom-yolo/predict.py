# predict.py
# Run our trained model on new images and webcam
# Built by: Mohammed Haroon Khan

from ultralytics import YOLO
import cv2

# ── LOAD YOUR TRAINED MODEL ───────────────────
# best.pt = weights at the epoch with highest mAP
# NOT last.pt — best.pt is always better to use
model = YOLO(r"C:\Users\haroo\Desktop\ai-engineer-journey\runs\detect\bottle_phone_v1\weights\best.pt")

# ── OPTION 1: Predict on a single image ───────
def predict_image(image_path):
    """
    Run model on one image and show result.
    Draws bounding boxes with class names and confidence.
    """
    results = model(image_path)

    for result in results:
        boxes = result.boxes

        for box in boxes:
            # Class ID — 0=phone, 1=water_bottle
            class_id = int(box.cls.item())

            # Class name from model
            class_name = model.names[class_id]

            # Confidence score — 0 to 1
            confidence = box.conf.item()

            # Bounding box coordinates in pixels
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            print(f"Detected: {class_name}")
            print(f"  Confidence : {confidence:.2%}")
            print(f"  Box        : ({x1:.0f},{y1:.0f}) → ({x2:.0f},{y2:.0f})")
            print()

        # Save annotated image
        result.save(filename="prediction_result.jpg")
        print("Saved: prediction_result.jpg")

# ── OPTION 2: Live webcam detection ───────────
def predict_webcam():
    """
    Run model on live webcam feed.
    Press Q to quit, S to save screenshot.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No webcam found!")
        return

    print("Webcam started — press Q to quit, S to save")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run model on current frame
        # verbose=False stops it printing every detection
        results = model(frame, verbose=False)

        # results[0].plot() draws boxes on the frame
        annotated_frame = results[0].plot()

        # Show FPS and detection count
        n_detections = len(results[0].boxes)
        cv2.putText(annotated_frame,
                    f"Detections: {n_detections}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        cv2.imshow("Bottle & Phone Detector — Mohammed Haroon Khan",
                   annotated_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('Q'):
            break
        elif key == ord('S'):
            cv2.imwrite("webcam_detection.jpg", annotated_frame)
            print("Screenshot saved!")

    cap.release()
    cv2.destroyAllWindows()

# ── OPTION 3: Evaluate on test set ────────────
def evaluate():
    """
    Run model on test images and print detailed metrics.
    This is what you show in interviews — real numbers.
    """
    metrics = model.val(
        data=r"C:\Users\haroo\Desktop\ai-engineer-journey\water-bottle-phone-detector-1\data.yaml",
        split="test"
    )

    print("\n" + "="*50)
    print("  Model Evaluation Results")
    print("="*50)
    print(f"  mAP50     : {metrics.box.map50:.4f}  ({metrics.box.map50*100:.1f}%)")
    print(f"  mAP50-95  : {metrics.box.map:.4f}  ({metrics.box.map*100:.1f}%)")
    print(f"  Precision : {metrics.box.mp:.4f}  ({metrics.box.mp*100:.1f}%)")
    print(f"  Recall    : {metrics.box.mr:.4f}  ({metrics.box.mr*100:.1f}%)")
    print("="*50)
    print("\nPer-class results:")
    for i, name in model.names.items():
        print(f"  {name:<15}: AP = {metrics.box.ap[i]:.4f}")

# ── MAIN ──────────────────────────────────────
if __name__ == "__main__":
    print("Choose mode:")
    print("1 = Webcam detection")
    print("2 = Evaluate on test set")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        predict_webcam()
    elif choice == "2":
        evaluate()
    else:
        print("Invalid choice")