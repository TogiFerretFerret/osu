import slider
import requests
import zipfile
import os
from pick import pick

def get_beatmap(beatmap_id):
    url = f"https://catboy.best/d/{beatmap_id}"
    r = requests.get(url)
    with open(f"beatmaps/{beatmap_id}.zip", "wb") as f:
        f.write(r.content)
    # Unzip the file
    with zipfile.ZipFile(f"beatmaps/{beatmap_id}.zip", 'r') as zip_ref:
        zip_ref.extractall(f"beatmaps/{beatmap_id}")
    # Delete the zip file
    os.remove(f"beatmaps/{beatmap_id}.zip")

def generate_timings():
    # First, iterate through all the beatmaps
    for beatmap_id in os.listdir("beatmaps"):
        # Open beatmap with slider
        bms = []
        for file in os.listdir(f"beatmaps/{beatmap_id}"):
            if file.endswith(".osu"):
                bms.append(slider.Beatmap.from_path(f"beatmaps/{beatmap_id}/{file}"))
        # Get the timings
        for bm in bms:
            with open(f"beatmaps/{beatmap_id}/{bm.display_name} ({bm.stars()} stars).txt", "wt") as f:
                f.write("\n".join(bm.timing_points))

if __name__ == "__main__":
    ids = input("Enter the beatmap ids: ").split()
    for id in ids:
        get_beatmap(id)
    generate_timings()