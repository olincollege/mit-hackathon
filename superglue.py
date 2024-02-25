from pathlib import Path
import argparse
import cv2
import torch

from third_party.SuperGluePretrainedNetwork.models.matching import Matching
from third_party.SuperGluePretrainedNetwork.models.utils import (
    AverageTimer,
    VideoStreamer,
    make_matching_plot_fast,
    frame2tensor,
    process_resize,
)

IMAGE_DIR = Path(__file__).parent / "images"


def load_image(impath):
    """Read image as grayscale and resize to img_size.
    Inputs
        impath: Path to input image.
    Returns
        grayim: uint8 numpy array sized H x W.
    """
    grayim = cv2.imread(impath, 0)
    if grayim is None:
        raise Exception("Error reading image %s" % impath)
    w, h = grayim.shape[1], grayim.shape[0]
    w_new, h_new = process_resize(w, h, [640, 480])
    grayim = cv2.resize(grayim, (w_new, h_new), interpolation=cv2.INTER_AREA)
    return grayim


def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    config = {
        "superpoint": {
            "nms_radius": 4,
            "keypoint_threshold": 0.005,
            "max_keypoints": -1,
        },
        "superglue": {
            "weights": "indoor",
            "sinkhorn_iterations": 20,
            "match_threshold": 0.2,
        },
    }

    matching = Matching(config).eval().to(device)
    
    return matching, device


def get_matching_keypoints(
    matching,
    device,
    image0_path: Path,
    image1_path: Path,
):
    image = load_image(str(image0_path))
    frame_tensor = frame2tensor(image, device)

    last_data = matching.superpoint({"image": frame_tensor})
    keys = ["keypoints", "scores", "descriptors"]
    last_data = {k + "0": last_data[k] for k in keys}
    last_data["image0"] = frame_tensor

    image = load_image(str(image1_path))
    frame_tensor = frame2tensor(image, device)

    pred = matching({**last_data, "image1": frame_tensor})
    kpts0 = last_data["keypoints0"][0].cpu().numpy()
    kpts1 = pred["keypoints1"][0].cpu().numpy()
    matches = pred["matches0"][0].cpu().numpy()

    valid = matches > -1
    confidence = pred["matching_scores0"][0].cpu()[valid]
    mkpts0 = kpts0[valid]
    mkpts1 = kpts1[matches[valid]]

    return mkpts0, mkpts1, confidence


if __name__ == "__main__":
    image0_path = IMAGE_DIR / "IMG_2279.PNG"
    image1_path = IMAGE_DIR / "test3.jpg"
    mkpts0, mkpts1, confidence = get_matching_keypoints(image0_path, image1_path)
    print(f"Resolved {len(mkpts0)} keypoints")
