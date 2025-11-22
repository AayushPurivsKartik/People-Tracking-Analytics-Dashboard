# heatmap.py - FIXED & IMPROVED
import cv2
import numpy as np

class HeatmapGenerator:
    def __init__(self, width, height, decay=0.95, intensity=18):
        self.width = width
        self.height = height
        self.decay = decay
        self.intensity = intensity
        self.heatmap = np.zeros((height, width), dtype=np.float32)

    def update(self, tracks):
        # Create a temporary layer for current frame
        temp = np.zeros_like(self.heatmap)

        if tracks is not None and len(tracks) > 0:
            for i in range(len(tracks)):
                if int(tracks.cls[i]) != 0:  # Only person
                    continue
                x1, y1, x2, y2 = map(int, tracks.xyxy[i].cpu().numpy())
                center_x = (x1 + x2) // 2
                center_y = y2  # Feet position

                # Add heat at feet (bigger radius = more area)
                cv2.circle(temp, (center_x, center_y), 30, self.intensity, -1)

        # Decay old heat + add new
        self.heatmap = self.heatmap * self.decay + temp
        self.heatmap = np.clip(self.heatmap, 0, 255)

    def get_overlay(self, frame):
        # Convert to 8-bit for color mapping
        heat = np.uint8(self.heatmap)
        heat_color = cv2.applyColorMap(heat, cv2.COLORMAP_JET)

        # Resize to frame size (in case of mismatch)
        heat_color = cv2.resize(heat_color, (frame.shape[1], frame.shape[0]))

        # Create mask where there is actual heat
        mask = heat > 12  # Threshold to avoid noise
        mask = mask.astype(bool)

        overlay = frame.copy()

        # Only apply overlay where mask is True
        if mask.any():  # This prevents the TypeError!
            overlay[mask] = cv2.addWeighted(overlay[mask], 0.6, heat_color[mask], 0.4, 0)

        # Save latest heatmap for dashboard
        cv2.imwrite("static/heatmap.png", heat_color)

        return overlay