import argparse
import logging
import cv2
import numpy as np
from edgetpumodel import EdgeTPUModel
from helpers import annotate_image
from utils import get_image_tensor
from flask import Flask, abort, jsonify, render_template, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APP")

device = 0
model_name = ""
coco_classes = []
data_window = {}
WINDOW_SIZE = 600  # 20 FPS x 30, approx thirty seconds

app = Flask("APP")


def register_annotations(data):
    global data_window

    # first, remove first item from window
    for label, window in data_window.items():
        data_window[label] = np.delete(window, 0)

    # update values of already registered classes
    common_labels = [label for label in data.keys() if label in data_window]
    for label in common_labels:
        data_window[label] = np.append(data_window[label], data[label])

    # create window for new classes
    new_labels = [label for label in data.keys() if label not in data_window]
    for label in new_labels:
        data_window[label] = np.zeros(WINDOW_SIZE)
        data_window[label][WINDOW_SIZE - 1] = data[label]

    # update already registered classes not being registered at the moment
    old_labels = [label for label in data_window.keys() if label not in data]
    for label in old_labels:
        if np.all(data_window[label] == 0):
            del data_window[label]
        else:
            data_window[label] = np.append(data_window[label], 0)


def detect():  # generate frame by frame from camera
    model = EdgeTPUModel(
        model_name,
        coco_classes,
        conf_thresh=args.conf_thresh,
        iou_thresh=args.iou_thresh,
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
            register_annotations(data)

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
    stats = {
        label: round(window.sum() / WINDOW_SIZE, 2)
        for label, window in data_window.items()
        if round(window.sum() / WINDOW_SIZE, 2) > 0
    }
    return stats


@app.route("/video_feed")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(detect(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/statistics")
def statistics():
    return jsonify(compute_statistics())


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("EdgeTPU test runner")
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
    coco_classes = args.names

    app.run(host="0.0.0.0", debug=True)
