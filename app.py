import argparse
import json
import logging
import cv2
import numpy as np
from edgetpumodel import EdgeTPUModel
from helpers import annotate_image
from utils import get_image_tensor
from flask import Flask, abort, render_template, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APP")

device = 0
model_name = ""
data_window = {}
WINDOW_SIZE = 6000  # 20 FPS x 60 x 5, approx five minutes

app = Flask("APP")


def detect():  # generate frame by frame from camera
    global model_name, device, data_window
    model = EdgeTPUModel(
        model_name, args.names, conf_thresh=args.conf_thresh, iou_thresh=args.iou_thresh
    )
    input_size = model.get_image_size()
    x = (255 * np.random.random((3, *input_size))).astype(np.uint8)
    model.forward(x)

    logger.info("Opening stream on device: {}".format(device))

    camera = cv2.VideoCapture(device)
    error = ""

    while True:
        res, image = camera.read()

        if res is False:
            error = "Empty image received"
            break
        else:
            full_image, net_image, pad = get_image_tensor(image, input_size[0])
            pred = model.forward(net_image)

            annotated_image, data = annotate_image(model, pred[0], full_image, pad)
            for label, num in data.items():
                if label in data_window:
                    data_window[label] = np.append(data_window[label], num)
                    if len(data_window[label]) > WINDOW_SIZE:
                        data_window[label] = np.delete(data_window[label], 0)
                else:
                    data_window[label] = np.array([num])

            # # tinference, tnms = model.get_last_inference_time()
            # # logger.info("Frame done in {}".format(tinference + tnms))

            _, annotated_frame = cv2.imencode(".jpg", annotated_image)
            frame = annotated_frame.tobytes()
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )  # concat frame one by one and show result

    camera.release()
    if error:
        logger.error(error)
        abort(500, error)
    exit(0)


def compute_statistics():
    global model_name, device, data_window
    stats = {label: window.mean() for label, window in data_window.items()}
    return str(json.dumps(stats, indent=1))


@app.route("/video_feed")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(detect(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/statistics")
def statistics():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(compute_statistics(), mimetype="text/plain")


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("EdgeTPU test runner")
    # # parser.add_argument("--model", "-m", help="weights file", required=True)
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        choices=["224", "192", "96"],
        default="224",
        help="input size to choose weights file",
    )
    parser.add_argument(
        "--conf_thresh", type=float, default=0.25, help="model confidence threshold"
    )
    parser.add_argument(
        "--iou_thresh", type=float, default=0.45, help="NMS IOU threshold"
    )
    parser.add_argument(
        "--names", type=str, default="data/coco.yaml", help="Names file"
    )
    parser.add_argument(
        "--device",
        type=int,
        default=0,
        help="Image capture device to run live detection",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Disable logging (except errors)"
    )

    args = parser.parse_args()

    if args.quiet:
        logging.disable(logging.CRITICAL)
        logger.disabled = True

    device = args.device
    model_name = f"yolov5s-int8-{args.input}_edgetpu.tflite"

    app.run(host="0.0.0.0", debug=True)
