import pyttsx3 as tt
import PyPDF2 as py
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser

bgc = "#F2F3F4"
tk = Tk()
tk.geometry("320x700")
tk.title("AudioBook")
tk.config(bg=bgc)

path = None
voice = StringVar(value=" ")
speaker = None
settings = {
    "rate": 150,
    "volume": 1.0,
    "pitch": 1.0
}

def open_file():
    global path
    try:
        path = filedialog.askopenfilename(filetypes=[("PDF Files", ".pdf"), ("Text Files", ".txt")])
        if not path:
            show_error("No file selected or file selection canceled.")
        else:
            if not path.lower().endswith(('.pdf', '.txt')):
                show_error("Unsupported file format. Please select a PDF or TXT file.")
            else:
                if path.lower().endswith('.pdf'):
                    with open(path, "rb") as book:
                        read = py.PdfReader(book)
                        total_pages = len(read.pages)
                        show_info(f"Total number of pages: {total_pages}")
                page_entry.config(state="normal")
    except Exception as e:
        show_error(f"Error: {e}")

def change_voice(selected_voice):
    try:
        global voice
        voice.set(selected_voice)
    except Exception as e:
        show_error(f"Error: {e}")

def change_settings():
    def save_settings():
        try:
            global settings
            settings["rate"] = int(rate_scale.get())
            settings["volume"] = float(volume_scale.get())
            settings["pitch"] = float(pitch_scale.get())
            settings_window.destroy()
        except Exception as e:
            show_error(f"Error: {e}")

    try:
        settings_window = Toplevel(tk)
        settings_window.title("User Settings")
        settings_window.geometry("300x200")
        settings_window.config(bg="sky blue")

        rate_label = Label(settings_window, text="Speed Rate:", bg="sky blue", font=("Comic Sans MS", 10))
        rate_label.grid(row=0, column=0, padx=10, pady=5)
        rate_scale = Scale(settings_window, from_=50, to=300, orient=HORIZONTAL, bg="sky blue")
        rate_scale.set(settings["rate"])
        rate_scale.grid(row=0, column=1, padx=10, pady=5)

        volume_label = Label(settings_window, text="Volume:", bg="sky blue", font=("Comic Sans MS", 10))
        volume_label.grid(row=1, column=0, padx=10, pady=5)
        volume_scale = Scale(settings_window, from_=0.0, to=1.0, resolution=0.1, orient=HORIZONTAL, bg="sky blue")
        volume_scale.set(settings["volume"])
        volume_scale.grid(row=1, column=1, padx=10, pady=5)

        pitch_label = Label(settings_window, text="Pitch:", bg="sky blue", font=("Comic Sans MS", 10))
        pitch_label.grid(row=2, column=0, padx=10, pady=5)
        pitch_scale = Scale(settings_window, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL, bg="sky blue")
        pitch_scale.set(settings["pitch"])
        pitch_scale.grid(row=2, column=1, padx=10, pady=5)

        save_button = Button(settings_window, text="Save Settings", command=save_settings, bg="light blue", font=("Comic Sans MS", 10), border=1,relief=RIDGE)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

        settings_window.transient(tk)
        settings_window.grab_set()
        tk.wait_window(settings_window)
    except Exception as e:
        show_error(f"Error: {e}")

import threading

def talk_file():
    global path, voice, speaker, settings
    try:
        page_n = page_entry.get()
        if not path:
            show_error("Please select a file.")
            return
        if not page_n.isdigit() or int(page_n) <= 0:
            show_error("Please enter a valid page number.")
            return

        if voice.get() == " ":
            show_error("Please select a voice type.")
            return

        if voice.get() == "male":
            voice_token = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
        else:
            voice_token = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

        if path.lower().endswith('.pdf'):
            with open(path,"rb") as book:
                read = py.PdfReader(book)
                if int(page_n) > len(read.pages):
                    show_error("Page number exceeds total pages.")
                    return
                page = read.pages[int(page_n) - 1]
                text = page.extract_text()
        elif path.lower().endswith('.txt'):
            with open(path, "r") as file:
                text = file.read()

        speaker = tt.init()
        speaker.setProperty('rate', settings["rate"])
        speaker.setProperty('volume', settings["volume"])
        speaker.setProperty('pitch', settings["pitch"])
        speaker.setProperty('voice', voice_token)

        def play_audio():
            speaker.say(text)
            speaker.save_to_file(text, "output_audio.mp3")
            speaker.runAndWait()
            speaker.stop()

            tk.grab_release()
            show_info("Audio file saved as 'output_audio.mp3'")

        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

    except Exception as e:
        show_error(f"Error: {e}")

def show_error(message):
    err = Label(tk, text=message, bd=0, bg=bgc, font=("Comic Sans MS", 10), foreground="red")
    err.pack(pady=(70, 0))
    tk.after(3000, err.destroy)

def show_info(message):
    info = Label(tk, text=message, bd=0, bg=bgc, font=("Comic Sans MS", 10), foreground="green")
    info.pack(pady=(70, 0))
    tk.after(3000, info.destroy)

def download_pdf():
    try:
        webbrowser.open("https://www.infobooks.org/free-pdf-books/short-stories/")
    except Exception as e:
        show_error(f"Error: {e}")

def handle_option(option):
    if option == "Yes, I Have a File":
        open_file()
    elif option == "No, Download One":
        download_pdf()

img = Image.open(r"C:\Users\ACER\Downloads\WhatsApp Image 2024-02-20 at 08.34.28_bc2e5450.png")
size = (180, 130)
res = img.resize(size)
img1 = ImageTk.PhotoImage(res)

logo = Label(tk, image=img1, bg=bgc)
logo.pack()

title = Label(tk, text="AudioBook", bg=bgc, foreground="dark blue", font=("Comic Sans MS", 20, "bold"))
title.pack(pady=(10, 10))

option_menu_frame = Frame(tk, bg=bgc)
option_menu_frame.pack()

option_var = StringVar()
option_var.set("Do You Have a File?")

option_menu = OptionMenu(option_menu_frame, option_var, "Yes, I Have a File", "No, Download One", command=handle_option)
option_menu.config(font=("Comic Sans MS", 10), bg="sky blue", relief=RIDGE, border=1)
option_menu.pack(pady=(10, 0))

page_no = Label(tk, text="Enter The Page Number", bd=0, bg=bgc, foreground="dark red", font=("Comic Sans MS", 10))
page_no.pack(pady=(50,0))

page_entry = Entry(tk, bg=bgc, state="disabled", borderwidth=2, relief=RIDGE)
page_entry.pack(pady=(10, 0))

talk = Button(tk, text="Read PDF", font=("Comic Sans MS", 10), activebackground="black", activeforeground="white",
              bd=0, bg="sky blue", width=17, command=talk_file, border=1,relief=RIDGE)
talk.pack(pady=(20, 0))

voice_label = Label(tk, text="Choose the voice:", bg=bgc, foreground="dark red", font=("Comic Sans MS", 10))
voice_label.pack(pady=(20, 0))

male_button = Radiobutton(tk, text="Male", variable=voice, value="male", bg=bgc, font=("Comic Sans MS", 10),
                          command=lambda: change_voice("male"))
male_button.pack()

female_button = Radiobutton(tk, text="Female", variable=voice, value="female", bg=bgc, font=("Comic Sans MS", 10),
                            command=lambda: change_voice("female"))
female_button.pack()

settings_button = Button(tk, text="User Settings",bg="sky blue",command=change_settings, font=("Comic Sans MS", 10), border=1,relief=RIDGE)
settings_button.pack(pady=(20, 0))

tk.mainloop()