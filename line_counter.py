# line_counter.py - FIXED VERSION
import cv2

class LineCounter:
    def __init__(self, line_x1, line_y1, line_x2, line_y2):
        self.line = [(line_x1, line_y1), (line_x2, line_y2)]
        self.entries = 0
        self.exits = 0
        self.tracked_ids_up = set()
        self.tracked_ids_down = set()
        # Store previous Y positions for each track ID
        self.prev_positions = {}

    def update(self, tracks):
        if tracks is None:
            return self.entries, self.exits

        # Loop over each detection in the frame
        for i in range(len(tracks)):
            # Only process person class (cls=0)
            if tracks.cls[i] != 0:
                continue

            bbox = tracks.xyxy[i].cpu().numpy()
            track_id = int(tracks.id[i].cpu().numpy())
            conf = tracks.conf[i].cpu().numpy()  # Optional: filter low conf

            x1, y1, x2, y2 = bbox
            center_x = int((x1 + x2) / 2)
            center_y = int(y2)  # Bottom center for crossing detection

            # Get previous Y position for this track ID
            prev_y = self.prev_positions.get(track_id)

            if prev_y is not None:
                # Assume horizontal line at line_y
                line_y = self.line[0][1]

                # Crossed from top to bottom → Entry
                if prev_y < line_y and center_y > line_y:
                    if track_id not in self.tracked_ids_down:
                        self.entries += 1
                        self.tracked_ids_down.add(track_id)
                        print(f"Entry detected! ID: {track_id}")

                # Crossed from bottom to top → Exit
                elif prev_y > line_y and center_y < line_y:
                    if track_id not in self.tracked_ids_up:
                        self.exits += 1
                        self.tracked_ids_up.add(track_id)
                        print(f"Exit detected! ID: {track_id}")

            # Update current position
            self.prev_positions[track_id] = center_y

        return self.entries, self.exits

    def draw(self, frame):
        # Draw the line
        cv2.line(frame, self.line[0], self.line[1], (0, 255, 0), 3)
        
        # Draw counts
        cv2.putText(frame, f"Entries: {self.entries}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(frame, f"Exits: {self.exits}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
        
        return frame