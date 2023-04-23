# edgetpuvision

Python API to run inference on image data coming from the camera.

Based on the work of [Josh Veitch-Michaelis](https://github.com/jveitchmichaelis/edgetpu-yolo/blob/main/edgetpumodel.py)

## Dev setup

### Requirements

#### Edge TPU runtime

The Edge TPU runtime is needed for running the demo locally.

On debian-based distros, go to <https://coral.ai/software/#debian-packages>.
On arch based distros, install it from AUR `yay -S libedgetpu-std`

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

## Edge setup (Debian based)

For debian based servers with a connected Edge TPU, copy and run the script `edge-setup.sh`

```bash
chmod +x edge-setup.sh
./edge-setup.sh
```

## Run

```bash
conda activate yolo-edgetpu
python3 app.py --device 3
```

```bash
conda activate yolo-edgetpu
python3 detect.py -m yolov5s-int8-224_edgetpu.tflite --stream --device 3
```
