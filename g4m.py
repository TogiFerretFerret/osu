import os
import time
import pygame

def load_timings(file_path):
    with open(file_path, "r") as f:
        timings = f.readlines()
    return [float(t.strip()) for t in timings]

def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

def train_tapping(timing_files):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("osu! Tapping Trainer")

    for timing_file in timing_files:
        beatmap_id = timing_file.split('/')[1]
        audio_path = f"beatmaps/{beatmap_id}/audio.mp3"
        timings = load_timings(timing_file)
        
        print(f"Training for {timing_file}...")
        play_audio(audio_path)
        
        start_time = time.time()
        timing_index = 0
        while pygame.mixer.music.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z or event.key == pygame.K_x:
                        current_time = time.time() - start_time
                        if timing_index < len(timings) and abs(current_time - timings[timing_index]) < 0.1:
                            print("Good!")
                            timing_index += 1
                        else:
                            print("Miss!")
            
            if timing_index < len(timings) and time.time() - start_time >= timings[timing_index]:
                print("Miss!")
                timing_index += 1
        
        pygame.mixer.music.stop()
        input("Press Enter to continue to the next beatmap...")

if __name__ == "__main__":
    timing_files = []
    for root, dirs, files in os.walk("beatmaps"):
        for file in files:
            if file.endswith(".txt"):
                timing_files.append(os.path.join(root, file))
    
    train_tapping(timing_files)