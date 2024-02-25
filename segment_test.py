from fastsam import FastSAM, FastSAMPrompt
import numpy as np
import torch
import cv2
from PIL import Image

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)
text_prompt = "black trashcan in the corner"
input = cv2.imread("images/test3.jpg")
print(input.shape)
input = cv2.resize(input, (640, 480))
model = FastSAM("./model/FastSAM-x.pt")
everything_results = model(
    input,
    device=device,
    retina_masks=True,
    imgsz=640,
    conf=0.8,
    iou=0.9,
)

prompt_process = FastSAMPrompt(input, everything_results, device=device)
ann = prompt_process.text_prompt(text=text_prompt)
if isinstance(ann, list):
    ann = np.array(ann)
mask = ann.squeeze()

input[~mask] = 0
cv2.imwrite("images/test_seg.jpg", input)
cv2.imshow("d", input)
cv2.waitKey(0)
cv2.destroyAllWindows()
# prompt_process.plot(
#     annotations=ann,
#     output_path="test.jpg",
#     # withContours=args.withContours,
#     # better_quality=args.better_quality,
# )