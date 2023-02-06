from pytube import YouTube
import PySimpleGUI as sg
import threading
import time
from PIL import Image
import requests
import io

#theme
sg.theme('DarkAmber')

# create layout
layout = [
    [sg.Image(data=None,key='-THUMBNAIL-',visible=True)],
    [sg.Input(key='-URL-')],
    [sg.Button('Download'),sg.Button('Thumbnail'),sg.Button('Exit')],
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
    try:
        # url value from the gui that will be inputted
        url = values['-URL-']

        # Create the YouTube object first
        yt_obj = YouTube(url)
            
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

        def download_progress():
            # Download the video, getting back the file path the video was downloaded to
            file_path = yt_obj.streams.filter(progressive=True).get_highest_resolution().download()
            downloading_task(file_path)

            window['-PATH-'].update(file_path)
            window['-PATH-'].update(visible=True)
            print(f"file_path is {file_path}")

        def display_image():
            # get thumbnail image url
            thumbnail_url = yt_obj.thumbnail_url
            # GET request the content
            pil_image = Image.open(io.BytesIO(requests.get(thumbnail_url).content)).resize((400,300))
            # convert the image into bytes of data
            png_bio = io.BytesIO()
            # save the image into png
            pil_image.save(png_bio, format="PNG")
            # get the value of the image bytes
            png_data = png_bio.getvalue()

            window['-THUMBNAIL-'].update(data=png_data)
            
        # thread for downloading
        def downloading_task():
            threading.Thread(target=download_progress).start()
        # thread for image display
        def image_display_task():
            threading.Thread(target=display_image).start()
    
        # Then register the callback
        yt_obj.register_on_progress_callback(progress)

        if event == 'Download':
            sg.popup_auto_close('Downloading', auto_close_duration=0.5)
            downloading_task()
        
        if event == 'Thumbnail':
            sg.popup_auto_close('Processing', auto_close_duration=0.5)
            image_display_task()

    except:
        #if input of url is null it will not display the image
        window['-THUMBNAIL-'].update(data=None)

window.close()

#example url
#https://youtu.be/dQw4w9WgXcQ