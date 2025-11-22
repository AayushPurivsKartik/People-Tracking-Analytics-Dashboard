# dwell_time.py - FIXED & FINAL
from datetime import datetime
import time
from database import log_track

class DwellTimeTracker:
    def __init__(self, session_id):
        self.session_id = session_id
        self.active_tracks = {}      # track_id → entry timestamp (float)
        self.peak_count = 0

    def update(self, tracks):
        current_time = time.time()
        current_count = 0
        seen_ids = set()  # ← This line was missing outside the if block!

        if tracks is not None and len(tracks) > 0:
            current_count = len([i for i in range(len(tracks)) if int(tracks.cls[i]) == 0])

            for i in range(len(tracks)):
                if int(tracks.cls[i]) != 0:  # Only person
                    continue
                track_id = int(tracks.id[i].cpu().numpy())

                seen_ids.add(track_id)

                # New person entered
                if track_id not in self.active_tracks:
                    entry_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.active_tracks[track_id] = current_time
                    log_track(track_id, entry_time=entry_str, session_id=self.session_id)

        # Update peak concurrent people
        if current_count > self.peak_count:
            self.peak_count = current_count

        # Detect lost tracks (people who left the scene)
        lost_ids = set(self.active_tracks.keys()) - seen_ids
        for track_id in lost_ids:
            entry_time = self.active_tracks[track_id]
            dwell_seconds = round(current_time - entry_time, 2)
            exit_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_track(track_id, exit_time=exit_str, dwell=dwell_seconds, session_id=self.session_id)
            del self.active_tracks[track_id]

        return self.peak_count