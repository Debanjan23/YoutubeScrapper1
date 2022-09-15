from pytube import YouTube

class Download:

     def download(url):
         try:
             SAVE_PATH = r"C:\Users\dchakrab.COMPUTACENTER\Downloads"
             yt = YouTube(url)
             d_video = yt.streams.get_by_resolution("480p")
             d_video.download(SAVE_PATH)

         except Exception as e:
             print(e)