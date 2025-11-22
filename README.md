# People Tracking & Analytics Dashboard 🚀

A **real-time computer vision analytics system** that tracks people, counts entries/exits, generates heatmaps, calculates dwell time, and displays everything on a beautiful web dashboard.

Built with **pure Python** – no paid APIs, no cloud.

### Features
- People detection & tracking (YOLOv8 + ByteTrack)
- Entry/Exit counting with virtual line
- Real-time heatmap of movement & dwell zones
- Dwell time per person (seconds spent in scene)
- Peak concurrent people tracking
- All data saved to SQLite
- Live Flask dashboard with auto-refresh
- Works with any video file or webcam



### Quick Start

```bash
git clone https://github.com/AayushPurivsKartik/People-Tracking-Analytics-Dashboard.git
cd people-tracking-analytics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt




Step 1: Process a video (or use webcam)
Bashpython main.py
→ It will ask for video path or use webcam automatically
Step 2: View Dashboard
Bashpython app.py
→ Open http://127.0.0.1:5000
Example Videos
Put any video in videos/ folder or use live webcam.
