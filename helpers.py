import logging
import numpy as np
from edgetpumodel import EdgeTPUModel
from utils import plot_one_box

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Helpers")


def annotate_image(
    model: EdgeTPUModel,
    det,
    input_image,
    pad,
    hide_labels=False,
    hide_conf=False,
    quiet=True,
):
    """
    Outputs image with annotations
    """
    if not len(det):
        return input_image, {}

    # Rescale boxes from img_size to im0 size
    # x1, y1, x2, y2=
    det[:, :4] = model.get_scaled_coords(det[:, :4], input_image, pad)

    # Print results
    if not quiet:
        s = ""
        for c in np.unique(det[:, -1]):
            n = (det[:, -1] == c).sum()  # detections per class
            s += f"{n} {model.names[int(c)]}{'s' * (n > 1)}, "  # add to string

        if s != "":
            s = s.strip()
            s = s[:-1]

        logger.info("Detected: {}".format(s))

    # Write results
    data = {}
    output_image = input_image
    for *xyxy, conf, cls in reversed(det):
        c = int(cls)  # integer class
        _label = model.names[c]
        label = (
            None if hide_labels else (_label if hide_conf else f"{_label} {conf:.2f}")
        )
        output_image = plot_one_box(
            xyxy, output_image, label=label, color=model.colors(c, True)
        )
        if _label in data:
            data[_label] += 1
        else:
            data[_label] = 1

    return output_image, data
