# edgetpuvision

Python API to run inference on image data coming from the camera.

## Dev setup

### Requirements

#### Wayland

Wayland must be enabled on the OS system

#### Edge TPU runtime

The Edge TPU runtime is needed for running the demo locally.

On debian-based distros, go to <https://coral.ai/software/#debian-packages>.
On arch based distros, install it from AUR `yay -S libedgetpu-std`

#### Base python packages

This is necessary to be able to load GStreamer custom python plugins with Wayland backend

```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
```

#### Python environment

`conda env create -f environment.yml`

#### Coral USB Accelerator

```console
foo@bar:~$ lsusb -d 1a6e:089a
Bus 002 Device 004: ID 1a6e:089a Global Unichip Corp.
foo@bar:~$ echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="1a6e", ATTRS{idProduct}=="089a", MODE="0664", TAG+="uaccess"' | sudo tee -a /etc/udev/rules.d/71-edgetpu.rules > /dev/null
foo@bar:~$ echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="18d1", ATTRS{idProduct}=="9302", MODE="0664", TAG+="uaccess"' | sudo tee -a /etc/udev/rules.d/71-edgetpu.rules > /dev/null
foo@bar:~$ sudo udevadm control --reload-rules && sudo udevadm trigger
```

#### USB camera

```console
foo@bar:~$ v4l2-ctl --list-formats-ext --device /dev/video0
ioctl: VIDIOC_ENUM_FMT
    Type: Video Capture

    [0]: 'YUYV' (YUYV 4:2:2)
        Size: Discrete 640x480
            Interval: Discrete 0.033s (30.000 fps)
            Interval: Discrete 0.042s (24.000 fps)
            Interval: Discrete 0.050s (20.000 fps)
            Interval: Discrete 0.067s (15.000 fps)
            Interval: Discrete 0.100s (10.000 fps)
            Interval: Discrete 0.133s (7.500 fps)
            Interval: Discrete 0.200s (5.000 fps)
   ...
```

### Local runnining

```bash
conda activate coraldev
GST_PLUGIN_PATH=$PWD/plugins python -m edgetpuvision.detect_server --model demo_files/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite --labels demo_files/coco_labels.txt --source /dev/video0:YUY2:640x480:24/1
```
