from pytube import YouTube
import PySimpleGUI as sg
import threading
import time

#theme
sg.theme('DarkAmber')

# create layout
layout = [
    [sg.Input(key='-URL-')],
    [sg.Button('Download'),sg.Button('Exit')],
    [sg.ProgressBar(100, orientation='h', s=(24,20), key='-PROGRESS-')],
    [sg.Text('',key='-PATH-', visible=False)]
]

# create window
# use the layout
window = sg.Window('YTDL', layout)

while True:
    event, values = window.read() 
    
    print(event, values)       
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      
    
    #progress function
    def progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        
        #progress bar updates here
        time.sleep(0.1)
        window['-PROGRESS-'].update(int(percentage_of_completion))
        
        #debugger purpose only for progress
        print('Progress:',int(percentage_of_completion))

    # threading
    def downloading(file):
        threading.Thread(target=progress, args=(file,), daemon=True).start()


    url = values['-URL-']

    # Create the YouTube object first
    yt_obj = YouTube(url)

    # Then register the callback
    yt_obj.register_on_progress_callback(progress)
    if event == 'Download':
        sg.popup_auto_close('Downloading', auto_close_duration=0.5)

        # Download the video, getting back the file path the video was downloaded to
        file_path = yt_obj.streams.filter(progressive=True).get_highest_resolution().download()
        downloading(file_path)

        window['-PATH-'].update(file_path)
        window['-PATH-'].update(visible=True)
        print(f"file_path is {file_path}")
window.close()