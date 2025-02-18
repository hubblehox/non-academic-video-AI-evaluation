import requests
import traceback

from typing import List, Dict
from fastapi import FastAPI, HTTPException

from app.main import main


app = FastAPI()


@app.get("/")
def home():
    return {'message': "Welcome to the home page"}


@app.post("/predict")
def predict(data: List[Dict]):
    """_summary_
    Args:
        video (VideoItem): class

    Returns:
        return_lst: list
    """
    return_lst = []
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    for entry in data:
        processed_entry = entry.copy()
        try:
            video_path = 'app/data/video.mp4'
            ref_image_path = 'app/data/ref_image.jpeg'
            response_ref_image = requests.get(entry['RefImage'])
            response = requests.get(entry['VideoPath'])
            if response.status_code == 200:
                with open(video_path, 'wb') as f:
                    f.write(response.content)
                if response_ref_image.status_code == 200:
                    with open(ref_image_path, 'wb') as f:
                        f.write(response_ref_image.content)
                print("Download successful.")
                processed_entry['message'] = main(video_path, 'app/data/audio.mp3', entry, ref_image_path)
            else:
                raise Exception
        except:
            print(traceback.format_exc())
            processed_entry['message'] = "Couldn't download video"
        return_lst.append(processed_entry)
    return return_lst
