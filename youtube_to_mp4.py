import subprocess
import os
import tkinter
from tkinter.filedialog import askdirectory
from tkinter import *
from pytube import YouTube


def get_resolutions(raws: list):
    x = []
    for i in raws:
        if i not in x:
            x.append(i)
    return x


def mime_type_simplifier(mime_type: str):
    x = '.'
    s = mime_type.split('/')
    x += (s[-1])
    return x


def cleanup(item: str):
    invalid = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '?']
    for char in item:
        if char in invalid:
            item = item.replace(char, '')
    return item


def folder_select():
    path = askdirectory(title='Please Select a Download Folder')
    os.chdir(path)
    tkinter.Tk().withdraw()
    return path


def to_mp4(link):
    youtube = YouTube(link)
    raw_resolutions = [stream.resolution for stream in youtube.streams.filter(is_dash=True)]
    label.configure(text=f"Available Resolutions: , {get_resolutions(raw_resolutions)[:-1]}")
    # print("Available Resolutions: ", get_resolutions(raw_resolutions)[:-1])
    label2.update()
    # resolution = input("Type in a resolution from the list: ")
    resolution = tkinter.Entry()
    resolution.pack()
    enter_button = Button(root, text='Enter', command=lambda: enter_buttons(enter_button, resolution, youtube))
    enter_button.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.1, relheight=0.1)
    label2.configure(text=f"Please Type in a Resolution")


def to_mp4_part2(value, youtube):
    streams = youtube.streams.filter(resolution=value)[0]
    stream_type = youtube.streams.filter(resolution=value)[0].mime_type
    final_type = mime_type_simplifier(stream_type)
    path = folder_select()
    streams.download(path)
    os.rename(f"{streams.default_filename}", f"video_{streams.default_filename}")
    audio = youtube.streams.filter(only_audio=True)[0]
    audio.download(path)
    os.rename(f'{audio.default_filename}', f'audio_{audio.default_filename}')

    video_file = f"\"{path}\"\\video_\"{streams.default_filename}\""
    audio_file = f"\"{path}\"\\audio_\"{audio.default_filename}\""

    video_file_to_remove = f"{path}/video_{streams.default_filename}"
    audio_file_to_remove = f"{path}/audio_{audio.default_filename}"

    title = streams.default_filename.strip(f'{final_type}')
    cmd_final = f'ffmpeg -i {video_file} -i {audio_file} -c copy \"{title}\"_merged.mp4'
    subprocess.run(cmd_final, shell=True)
    os.remove(fr'{video_file_to_remove}')
    os.remove(fr'{audio_file_to_remove}')

    label.update()
    label.configure(text="Download Finished, Enjoy the Video!")
    root.after(5000, lambda: root.destroy())


def to_mp3(link):
    youtube = YouTube(link)
    path = folder_select()
    audio = youtube.streams.get_audio_only()
    audio.download(path)
    audio_type = mime_type_simplifier(audio.mime_type)
    os.rename(f'{audio.default_filename}', f'audio_{audio.default_filename}')

    audio_file = f"\"{path}\"\\audio_\"{audio.default_filename}\""

    audio_file_to_remove = f"{path}/audio_{audio.default_filename}"

    title = audio.default_filename.strip(f'{audio_type}')
    cmd_final = f'ffmpeg -i {audio_file} \"{title}\".mp3'
    subprocess.run(cmd_final, shell=True)
    os.remove(fr'{audio_file_to_remove}')
    label.update()
    label.configure(text="Download Finished, Enjoy the Music!")
    root.after(5000, lambda: root.destroy())


def mp3():
    mp3_button.destroy()
    mp4_button.destroy()
    label.update()
    label.pack()
    label.configure(text="Please Enter the Video Link: ")
    user_input = tkinter.Entry()
    user_input.pack()
    enter_button = Button(root, text="Enter", command=lambda: enter(enter_button, user_input, mp3))
    enter_button.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.1, relheight=0.1)


def mp4():
    mp4_button.destroy()
    mp3_button.destroy()
    label.update()
    label.pack()
    label.configure(text="Please Enter the Video Link: ")
    user_input = tkinter.Entry()
    user_input.pack()
    enter_button = Button(root, text="Enter", command=lambda: enter(enter_button, user_input, mp4))
    enter_button.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.1, relheight=0.1)


def enter_buttons(button, resolution, youtube):
    value = resolution.get()
    resolution.destroy()
    button.destroy()
    to_mp4_part2(value, youtube)


def enter(button, user_input, type1):
    button.destroy()
    result = user_input.get()
    user_input.destroy()
    if type1 == mp4:
        to_mp4(result)
    elif type1 == mp3:
        to_mp3(result)


root = tkinter.Tk()
frame = tkinter.Frame()
frame.pack()
root.option_add("*font", "Times 15")
root.title("Youtube to Mp4/Mp3 Converter")
root.geometry("900x600")

mp3_button = Button(root, text="mp3", command=mp3)
mp4_button = Button(root, text="mp4", command=mp4)
mp3_button.place(relx=0.45, rely=0.5, anchor=CENTER, relwidth=0.1, relheight=0.1)
mp4_button.place(relx=0.55, rely=0.5, anchor=CENTER, relwidth=0.1, relheight=0.1)
label = Label(root, text='')
label2 = Label(root, text='', anchor=CENTER)

root.mainloop()
exit()
