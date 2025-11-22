# main.py - FINAL VERSION
from ultralytics import YOLO
import cv2
import time
from line_counter import LineCounter
from heatmap import HeatmapGenerator
from dwell_time import DwellTimeTracker
from database import init_db, start_session, end_session

init_db()
session_id = start_session()
print(f"New analytics session started: {session_id}")

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("videos/input2.mp4")
width = int(cap.get(3))
height = int(cap.get(4))

line_counter = LineCounter(0, height//2, width, height//2)
heatmap_gen = HeatmapGenerator(width, height)
dwell_tracker = DwellTimeTracker(session_id)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('static/video_output.mp4', fourcc, 30, (width, height))

start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True, classes=0, tracker="bytetrack.yaml", verbose=False)
    tracks = results[0].boxes if results[0].boxes and results[0].boxes.id is not None else None

    # Update all modules
    line_counter.update(tracks)
    heatmap_gen.update(tracks)
    peak = dwell_tracker.update(tracks)
    cv2.putText(frame, f"Peak: {peak}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 3)

    # Draw
    frame = line_counter.draw(frame)
    frame = heatmap_gen.get_overlay(frame)
    frame = results[0].plot()

    # FPS & Peak display
    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.putText(frame, f"FPS: {fps:.1f} | Peak: {peak}", (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    cv2.imshow("Full Analytics System", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# Finalize session
end_session(session_id, line_counter.entries, line_counter.exits, dwell_tracker.peak_count)
print("Session ended. Analytics saved to analytics.db")