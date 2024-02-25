from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path
from skimage import io
import base64
from typing import List
import tempfile
import torchvision.transforms.functional as TF
from PIL import Image, ImageDraw
from superglue import get_matching_keypoints, load_model
import numpy as np
from pygame import mixer
from tts import tts_play
import cv2

# you can start the server by running:
#   uvicorn anchor.backend.server.localizer:app --reload --host 10.76.135.81 --port 8000
app = FastAPI()

matching_model, device = load_model()

IMAGES_DIR = Path(__file__).parent / "images/navigation"
SEGMENTED_IMG = Path(__file__).parent / "images/navigation/segmented.png"

global SUPERGLUE_RUNNING
SUPERGLUE_RUNNING = False

IMG_CENTER = [320, 240]
THRESH = 0.5

mixer.init()

@app.get("/")
def read_root():
    return {"Hello": "World"}


class LocalizeImageReq(BaseModel):
    base64Jpg: str
    modelName: List[str]
    focal_length: float
    optical_x: float
    optical_y: float
    arkit_pose: List[float]


@app.post("/localize/")
def localizeImage(req: LocalizeImageReq, background_tasks: BackgroundTasks):
    img_bytes: bytes = base64.b64decode(req.base64Jpg)
    pil_image: Image

    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(img_bytes)
        sk_image = io.imread(tmp.name)
        pil_image = TF.to_pil_image(sk_image)
        pil_image = Image.Image.rotate(pil_image, -90, expand=True)
        temp_dir = IMAGES_DIR / "query.jpg"
        pil_image.save(temp_dir)
        # pil_image = Image.Image.resize(pil_image, [480, 640])
    grayim = cv2.imread(str(temp_dir))
    image = cv2.resize(grayim, (640, 480), interpolation=cv2.INTER_AREA)
    cv2.imwrite("images/navigation/query.jpg", image)
    
    _, mkpts, confidence = get_matching_keypoints(
        matching_model,
        device,
        SEGMENTED_IMG,
        temp_dir,
    )
    
    rel_mkpts = []
    for idx, conf in enumerate(confidence):
        if conf > THRESH:
            rel_mkpts.append(mkpts[idx])
    
    
    global SUPERGLUE_RUNNING
    SUPERGLUE_RUNNING = False
    
    if len(rel_mkpts) > 0:
        print(f"Min Confidence: {min(confidence)}")
        print(f"Max Confidence: {max(confidence)}")

        kpt_centroid = np.mean(mkpts, axis=0)
        print(f"Centroid: {kpt_centroid}")
        if np.abs(kpt_centroid[1] - IMG_CENTER[1]) < 10:
            print("Forward")
            tts_play("The trash can is in front of you. Walk forward.")
        elif kpt_centroid[1] > IMG_CENTER[1]:
            print("Right")
            tts_play("The trash can is to your right. Turn right.")
        else:
            print("Left")
            tts_play("The trash can is to your left. Turn left")
    else:
        print(f"{len(mkpts)} Keypoints matched")
        
    image = cv2.imread("images/navigation/query.jpg")
    print(mkpts)
    for x, y in mkpts:
        cv2.circle(image, (int(x), int(y)), 2, (0, 0, 0), 1 , lineType=cv2.LINE_AA)
        # break
    cv2.imwrite("images/navigation/query.jpg", image) 
    breakpoint()
    # with Image.open("images/navigation/query.jpg", "r") as im:
    #     print(im.size)
    #     cv2.circle()
    #     draw = ImageDraw.Draw(im)
    #     for kpt in mkpts:
    #         draw.ellipse([(kpt[1] - 1, kpt[0] - 1), (kpt[1] + 1, kpt[0] + 1)])

    #     im.save("images/navigation/query.jpg")
    # breakpoint()
    # print("Superglue ended")
    
    return {
        "pose": [0],
        "inlier_count": 0,
        "model": "test",
        "status": "ok",
    }
