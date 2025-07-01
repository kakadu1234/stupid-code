import customtkinter
import tkinter
import time
import math
import winsound

#Background Process -------------------------------------------->

def playAudio():
    filename = "RingTone.wav"
    winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)


def convertToSeconds(hour=0, minute=0, second=0):
    second1 = hour * 60 * 60
    second2 = minute * 60
    return second + second1 + second2

def runTimer(lenght, start_time=None):
    if start_time is None:
        start_time = time.time()
   
    current = time.time()
    elapsed = current - start_time #passed seconds
    progressed = elapsed / lenght #in percent for progressbar status
    ProgressBar.set(min(progressed, 1))

    if elapsed >= lenght:
        playAudio()
        Counter.configure(text="Ding Dong!")
        
    else: #update Label
        remaining = max(0, math.ceil(lenght - elapsed))
        hrs = remaining //  3600
        mins = (remaining % 3600) // 60
        secs = remaining % 60
        Counter.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}") #Set UI Timer Label

        #call function again after 100ms
        root.after(100, runTimer, lenght, start_time)

def start():
    try:
        hour = int(Hour.get()) if Hour.get() != "" else 0
        minute = int(Minute.get()) if Minute.get() != "" else 0
        second = int(Second.get()) if Second.get() != "" else 0
    except:
        Counter.configure(text= "Invalid input!!")
    
    howLong = convertToSeconds(hour, minute, second)
    if howLong <= 0:
        Counter.configure(text= "Enter positive time!!")
        return

    ProgressBar.set(0)
    runTimer(howLong)
    
def validate_integer_input(new_value): #Only Integer in Entry field
    if new_value == "" or new_value.isdigit():
        return True
    return False



#UI/Foreground Process --------------------------------------------->

currentTime = "00:00:00"

#Window default setting
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

#main window
root = customtkinter.CTk()
root.title("Timer")
root.resizable(False, False)

#Progressbar show time elapsed
ProgressBar = customtkinter.CTkProgressBar(root, width=400)
ProgressBar.grid(row=4, column=1, columnspan=3, pady= 10)

# Register the validation function
vcmd = root.register(validate_integer_input)


#Select Time
Hour = customtkinter.CTkEntry(root, width= 125,justify="center",
        validate="key", validatecommand=(vcmd, "%P"), font=("Courir", 20, "bold"))
Hour.grid(row=2, column=1, pady= 5, padx=6)

Minute = customtkinter.CTkEntry(root, width= 125,justify="center",
        validate="key", validatecommand=(vcmd, "%P"), font=("Courir", 20, "bold"))
Minute.grid(row=2, column=2, pady= 5, padx=6)

Second = customtkinter.CTkEntry(root, width= 125,justify="center",
        validate="key", validatecommand=(vcmd, "%P"), font=("Courir", 20, "bold"))
Second.grid(row=2, column=3, pady=5, padx=6)


#Label Countown
Counter = customtkinter.CTkLabel(root, text= currentTime, font=("Courir", 40, "bold"))
Counter.grid(row=5, column=1, columnspan= 3)

#Start Button
StartBtn = customtkinter.CTkButton(root, text= "Start", width=400, command=start)
StartBtn.grid(row=3, column=1, columnspan=3)

#Description Label
text1 = customtkinter.CTkLabel(root, text="Hours", font=("Courir", 23, "italic"))
text1.grid(row=1, column=1)
text2 = customtkinter.CTkLabel(root, text="Minutes", font=("Courir", 23, "italic"))
text2.grid(row=1, column=2)
text3 = customtkinter.CTkLabel(root, text="Seconds", font=("Courir", 23, "italic"))
text3.grid(row=1, column=3)
root.mainloop()