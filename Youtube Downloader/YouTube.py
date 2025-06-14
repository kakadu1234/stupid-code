from pytubefix import YouTube
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
import customtkinter as tk
import os 
import pyperclip
import threading

DestinationFolder = "C:/Users/" #your location
check = False
url = ""
global_progress = 0

def Check_streams(link):
    global itag_vid
    global itag_aud
    global title

    if only_Video or Full_Video == True:
        video = YouTube(link)
        title = video.title
        video = video.streams.filter(resolution= '1080p', mime_type='video/mp4')
        print(video)
        itag_vid = int(input("Itag video, only number!: "))

    if only_Audio or Full_Video == True:
        audio = YouTube(link)
        audio = audio.streams.filter( only_audio= True, mime_type= 'audio/mp4')
        print(audio)
        itag_aud = int(input("Itag audio, only number!: "))

def Download_Video(link, itag_vid):
    yt = YouTube(link, on_progress_callback=progress_callback_video)
    yt = yt.streams.get_by_itag(itag_vid)
    print("Video download started...")
    yt.download(output_path= DestinationFolder)
    print("Video download completed")
    dateiVidEnd = ".mp4"
    new_name = "video.mp4"
    dateien = [f for f in os.listdir(DestinationFolder) if f.endswith(dateiVidEnd)]
    if dateien:
       old_file = os.path.join(DestinationFolder,dateien[0]) 
        new_file = os.path.join(DestinationFolder,new_name)
        os.rename(old_file, new_file)
    
def Download_Audio(link, itag_aud):
    tube = YouTube(link, on_progress_callback= progress_callback_audio)
    tube = tube.streams.get_by_itag(itag_aud)
    print("Audio download started...")
    tube.download(output_path= DestinationFolder)
    print("donwload completed")
    dateiAudEnd = '.m4a'
    newName = "audio.m4a"
    data = [f for f in os.listdir(DestinationFolder) if f.endswith(dateiAudEnd)]
    if data:
        old_data = os.path.join(DestinationFolder, data[0])
        new_data = os.path.join(DestinationFolder, newName)
        os.rename(old_data, new_data)

def progress_callback_video(stream, chunk, bytes_remaining):
    #calculates video progress
    total_size = stream.filesize
    percent = 50 + ((total_size - bytes_remaining) / total_size) * 50
    update_progressbar(percent)

def progress_callback_audio(stream, chunk, bytes_remaining):
    #calculates audo progress
    total_size = stream.filesize
    percent = ((total_size - bytes_remaining) / total_size) * 50
    update_progressbar(percent)


def update_progressbar(percent):
    global global_progress
    global_progress = percent
    app.after(0, lambda: Progress.set(global_progress / 100))
    app.after(0, lambda: Progress_Info.configure(text=f"Downdload-progress: {global_progress:.1f}%"))
    app.update_idletasks()

def callback(progress):
    app.after(0, update_progress, progress) 

def concatenate_func():
    # Open the video and audio
    video_clip = VideoFileClip('output/video.mp4')
    audio_clip = AudioFileClip('output/audio.m4a')
  
    # Concatenate the video clip with the audio clip
    final_video = video_clip.with_audio(audio_clip)
    
    # Export the final video with audio
    final_video.write_videofile("output/final.mp4",
     codec="libx264", audio_codec="aac", preset= 'ultrafast', threads= 4)
    
    video_clip.close()
    audio_clip.close()
    final_video.close()
        #delete audio and video files
    if os.path.exists('output/video.mp4'):
        os.remove('output/video.mp4')
    if os.path.exists('output/audio.m4a'):
        os.remove('output/audio.m4a')
    update_progressbar(100)

def Paste():
    try:
        clipboard_text = app.clipboard_get()  # get Clipboard
        LinkEntry.insert(tk.END, clipboard_text)   # paste text into entry field
    except tk.TclError:
        pass

def Dropdown_command(choice):
    global res
    res = choice
      

def checkbox_Video():
    if check_var1.get() == "on":
        return True
    else:
        return False 

def checkbox_Audio():
    if check_var2.get() == "on":
        return True
    else:
        return False 

def checkbox_Full():
    if check_var3.get() == "on":
        return True
    else:
        return False 

def Mainstart_DownloadButton(): 
    global url  
    global check  
    check = True 
    url = LinkEntry.get()
    instruction()

def resolution():
    global itag_vid
    global itag_aud

    if res == '1080p':
        itag_vid = 399
        itag_aud = 140
    elif res == '720p':
        itag_vid = 398
        itag_aud = 140
    elif res == '480p':
        itag_vid = 397
        itag_aud = 140
    elif res == '360p':
        itag_vid = 396
        itag_aud = 140
    elif res == '240p':
        itag_vid = 395
        itag_aud = 140
    elif res == '144p':
        itag_vid = 394
        itag_aud = 140
    else:
        Print('Resolution unavailable!!')

def instruction():
    resolution()
    if checkbox_Video() == True:
        threading.Thread(target=Download_Video, args=(url, itag_vid), daemon= True).start()
    if checkbox_Audio() == True:
        threading.Thread(target=Download_Audio, args=(url, itag_vid), daemon=True).start()
    if checkbox_Full() == True:
        video_thread = threading.Thread(target=Download_Video, args=(url, itag_vid), daemon=True)
        audio_thread = threading.Thread(target=Download_Audio, args=(url, itag_aud), daemon=True)
        video_thread.start()
        audio_thread.start()
        # Checks if both threads finished before putting together
        def check_downloads():
            if not video_thread.is_alive() and not audio_thread.is_alive():
                threading.Thread(target=concatenate_func, daemon=True).start()
            else:
                app.after(1000, check_downloads)  # checks every second
        
        check_downloads()
        

def Close():
    app.destroy()




app = tk.CTk()
app.title("YouTube Downloader")

# Paste Link
PasteButton = tk.CTkButton(app, text="Paste", command=Paste)
PasteButton.grid(padx=5, pady=5,row= 1, column= 5)


DownButton = tk.CTkButton(app, text="Download", command=Mainstart_DownloadButton)
DownButton.grid(padx=5,  pady=5,row= 2, column= 5)

# Close window
CloseButton = tk.CTkButton(app, text="Close", command= Close)
CloseButton.grid(padx=5,  pady=5,row= 3, column= 5)

# entry filed from youtube link
LinkEntry = tk.CTkEntry(app, width= 450, placeholder_text= 'https://www.youtube.com/watch?')
LinkEntry.grid(padx=5,  pady=5,row= 1, column= 1, columnspan= 4)


#select resolution
combobox = tk.CTkComboBox(app,dropdown_hover_color= 'darkgrey', values=["1080p", "720p", "480p", "360p", "240p", "144p"],state= 'readonly',
                                                 command=Dropdown_command)
combobox.set("1080p") #preset => direkt ausgewählt
Dropdown_command("1080p")
combobox.grid(padx=5,  pady=5,row= 2, column= 1)

# download progress viewer

Progress = tk.CTkProgressBar(app, orientation= 'horizontal', width= 300)
Progress.set(0)
Progress.grid(padx=5,  pady=5,row= 3, column= 2, columnspan= 3)

# download label in percent
Progress_Info = tk.CTkLabel(app, text= 'Download-Fortschritt: 0%')
Progress_Info.grid(padx=5,  pady=5,row= 3, column= 1)

# Checkbox
check_var3 = tk.StringVar(value="on")
checkbox_all = tk.CTkCheckBox(app, text="Full Video", command=checkbox_Full,
                                         variable=check_var3, onvalue="on", offvalue="off")
checkbox_all.grid(padx=1,  pady=5,row= 2, column=2)


check_var1 = tk.StringVar(value="off")
checkbox_Vid = tk.CTkCheckBox(app, text="Only Video", command=checkbox_Video,
                                     variable=check_var1, onvalue="on", offvalue="off")
checkbox_Vid.grid(padx=1,  pady=5,row= 2, column=3)


check_var2 = tk.StringVar(value="off")
checkbox_Aud = tk.CTkCheckBox(app, text="Only Audio", command=checkbox_Audio,
                                     variable=check_var2, onvalue="on", offvalue="off")
checkbox_Aud.grid(padx=1,  pady=5,row= 2, column= 4)

app.mainloop()