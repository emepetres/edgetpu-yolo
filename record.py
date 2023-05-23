import argparse
import logging
import time
import cv2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APP")


def record():  # generate frame by frame from camera
    logger.info("Opening stream on device: {}".format(device))

    camera = cv2.VideoCapture(device)
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    fps = int(camera.get(5))

    timestr = time.strftime("%Y%m%d_%H%M%S")
    out = cv2.VideoWriter(
        f"out_{timestr}.avi",
        cv2.VideoWriter_fourcc("M", "J", "P", "G"),
        fps,
        (frame_width, frame_height),
    )
    error = ""

    try:
        while True:
            res, image = camera.read()

            if res is False:
                error = "Empty image received"
                break
            else:
                out.write(image)

    except KeyboardInterrupt:
        pass

    camera.release()
    out.release()
    if error:
        logger.error(error)
        exit(-1)
    exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("EdgeTPU test runner")
    parser.add_argument(
        "--device",
        type=int,
        default=0,
        help="Image capture device to run live detection",
    )

    args = parser.parse_args()

    device = args.device

    record()
