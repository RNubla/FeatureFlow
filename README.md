# FeatureFlow

[Paper](https://github.com/CM-BF/FeatureFlow/blob/master/paper/FeatureFlow.pdf) | [Supp](https://github.com/CM-BF/FeatureFlow/blob/master/paper/Supp.pdf)

A state-of-the-art Video Frame Interpolation Method using deep semantic flows blending.

FeatureFlow: Robust Video Interpolation via Structure-to-texture Generation (IEEE Conference on Computer Vision and Pattern Recognition 2020)

## To Do List

- [x] Preprint
- [x] Training code
- [x] Remove Duplicate Frames
- [x] High Resolution Mode For Video 1280x720
  - [x] Split video into 4 sections and each section must be 640x360
  - [x] Allow for video auto detect of resolution.
    - [ ] If resolution is 640x360, split video would not be run
- [x] Remane output file
- [x] Change output file location
- [x] Refactor for paths to work with Windows
- [x] Change terminal commands to work with Windows
- [x] Create UI using wxPython
- [x] Added Multi-Thread so GUI would not freeze
  - [ ] Add multo-thread for splitting videos and stitching videos
- [ ] Add Progress Bar GUI

## Table of Contents

1. [Requirements](#requirements)
1. [Demos](#video-demos)
1. [Installation](#installation)
1. [Pre-trained Model](#pre-trained-model)
1. [Download Results](#download-results)
1. [Evaluation](#evaluation)
1. [Test your video](#test-your-video)
1. [Training](#training)
1. [Citation](#citation)

## Requirements

- Ubuntu
- Python 3.7
- Anaconda
- PyTorch (>=1.1)
- Cuda (>=10.0) & Cudnn (>=7.0)
- mmdet 1.0rc (from https://github.com/open-mmlab/mmdetection.git)
- visdom (not necessary)
- NVIDIA GPU

## Video demos

Click the picture to Download one of them or click [Here(Google)](https://drive.google.com/open?id=1QUYoplBNjaWXJZPO90NiwQwqQz7yF7TX) or [Here(Baidu)](https://pan.baidu.com/s/1J9seoqgC2p9zZ7pegMlH1A)(key: oav2) to download **360p demos**.

**360p demos**(including comparisons):

[<img width="320" height="180" src="https://github.com/CM-BF/FeatureFlow/blob/master/data/figures/youtube.png"/>](https://github.com/CM-BF/storage/tree/master/videos/youtube.mp4 "video1")
[<img width="320" height="180" src="https://github.com/CM-BF/FeatureFlow/blob/master/data/figures/check_all.png"/>](https://github.com/CM-BF/storage/tree/master/videos/check_all.mp4 "video2")
[<img width="320" height="180" src="https://github.com/CM-BF/FeatureFlow/blob/master/data/figures/tianqi_all.png"/>](https://github.com/CM-BF/storage/tree/master/videos/tianqi_all.mp4 "video3")
[<img width="320" height="180" src="https://github.com/CM-BF/FeatureFlow/blob/master/data/figures/video.png"/>](https://github.com/CM-BF/storage/tree/master/videos/video.mp4 "video4")
[<img width="320" height="180" src="https://github.com/CM-BF/FeatureFlow/blob/master/data/figures/shana.png"/>](https://github.com/CM-BF/storage/tree/master/videos/shana.mp4 "video5")

**720p demos**:

[<img width="320" height="180" src="https://github.com/CM-BF/FeatureFlow/blob/master/data/figures/SYA_1.png"/>](https://github.com/CM-BF/storage/tree/master/videos/SYA_1.mp4 "video6")
[<img width="320" height="180" src="https://github.com/CM-BF/FeatureFlow/blob/master/data/figures/SYA_2.png"/>](https://github.com/CM-BF/storage/tree/master/videos/SYA_2.mp4 "video7")

## Installation

- clone this repo
- git clone https://github.com/open-mmlab/mmdetection.git

## Install mmdetection:

```bash
$ git clone https://github.com/open-mmlab/mmdetection.git
$ conda create -n open-mmlab python=3.7 -y
$ conda activate open-mmlab
$ conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=10.0 -c pytorch -y
$ conda install x264=='1!152.20180717' ffmpeg=4.0.2 -c conda-forge -y   # windows conda install -c groakat x264 ffmpeg=4.0.2 -c conda-forge -y
$ cd mmdetection
$ git checkout tags/v1.0rc1
$ pip install -r requirements.txt         #windows use pycocotools-windows
$ pip install mmcv
$ pip install -v -e .  # or "python setup.py develop"
$ pip install scikit-image visdom tqdm prefetch-generator
$ pip list | grep mmdet
```

## Building File !!(WARNING: If when building, dont use conda to install packages. Use pip for torchvision and pytorch)

```bash
$ conda create -n open-mmlab python=3.7 -y
$ conda activate open-mmlab
$ conda install cudatoolkit=10.0 -c pytorch -y
$ pip install https://download.pytorch.org/whl/cu100/torchvision-0.3.0-cp37-cp37m-win_amd64.whl #pytorch 1.1.0
$ pip install torchvision==0.2.2.post3
$ conda install -c groakat x264 ffmpeg=4.0.2 -c conda-forge -y
$ cd mmdetection
$ git checkout tags/v1.0rc1
$ pip install -r requirements.txt     # windows use pycocotools-windows
$ pip install mmcv
$ pip install -v -e .  # or "python setup.py develop"
$ pip install scikit-image visdom tqdm prefetch-generator wxPython


```

## BUILD

```bash
$ pyinstaller feflow_ui.py --distpath D:\Programming\Python\FeatureFlow-Build -n FeatureFlow-App -y --clean --add-data .\checkpoints\FeFlow.ckpt;.\checkpoints\ --add-data .\models\bdcn\final-model\bdcn_pretrained_on_bsds500.pth;.\models\bdcn\final-model\ --add-data .\formbuilder\noname.xrc;.\formbuilder\ --add-binary .\ffmpeg\bin\ffmpeg.exe;.
```

## Checkpoint

[Google Drive](https://drive.google.com/open?id=1S8C0chFV6Bip6W9lJdZkog0T3xiNxbEx)

[Baidu Cloud](https://pan.baidu.com/s/1LxVw-89f3GX5r0mZ6wmsJw): ae4x

Place FeFlow.ckpt to ./checkpoints/.

## Pre-trained Model

[Google Drive](https://drive.google.com/file/d/1CmDMypSlLM6EAvOt5yjwUQ7O5w-xCm1n/view)

Download BDCN's pre-trained model:bdcn_pretrained_on_bsds500.pth to ./model/bdcn/final-model/

## Download Results

[Google Drive](https://drive.google.com/open?id=1OtrExUiyIBJe0D6_ZwDfztqJBqji4lmt)

[Baidu Cloud](https://pan.baidu.com/s/1BaJJ82nSKagly6XZ8KNtAw): pc0k

## Evaluation

```bash
$ CUDA_VISIBLE_DEVICES=0 python eval_Vimeo90K.py --checkpoint ./checkpoints/FeFlow.ckpt --dataset_root ~/datasets/videos/vimeo_interp_test --visdom_env test --vimeo90k --imgpath ./results/
```

## Test your video

```bash
$ CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ./yourvideo.mp4 --t_interp 4 --slow_motion
```

`--t_interp` sets frame multiples, only power of 2(2,4,8...) are supported. Use flag `--slow_motion` to slow down the video which maintains the original fps.

The output video will be saved as output.mp4 in your working diractory.

## Training

Training Code **train.py** is available now. I can't run it for comfirmation now because I've left the Lab, but I'm sure it will work with right argument settings.

```bash
$ CUDA_VISIBLE_DEVICES=0,1 python train.py <arguments>
```

- Please read the **arguments' help** carefully to fully control the **two-step training**.
- Pay attention to the `--GEN_DE` which is the flag to set the model to Stage-I or Stage-II.
- 2 GPUs is necessary for training or the small batch_size will cause training process crash.
- Deformable CNN is not stable enough so that you may face training crash sometimes(I didn't fix the random seed), but it can be detected soon after the beginning of running by visualizing results using Visdom.
- Visdom visualization codes[line 75, 201-216 and 338-353] are included which is good for viewing training process and checking crash.

## Citation

```
@InProceedings{Gui_2020_CVPR,
author = {Gui, Shurui and Wang, Chaoyue and Chen, Qihua and Tao, Dacheng},
title = {FeatureFlow: Robust Video Interpolation via Structure-to-Texture Generation},
booktitle = {The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2020}
}
```

## Contact

[Shurui Gui](mailto:citrinegui@gmail.com); [Chaoyue Wang](mailto:chaoyue.wang@sydney.edu.au)

## License

See [MIT License](https://github.com/CM-BF/FeatureFlow/blob/master/LICENSE)
