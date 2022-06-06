# 2022本科生毕业论文源码

题目：**基于 BlazePose 算法的机器人人体姿势识别与模仿**

本仓库分五部分：

- `01.BlazePose_train_test`

    这是BlazePose的复现工作，具体操作可以查看[这里](01.BlazePose_train_test/train.md)。

- `02.BlazePose_pc`
    
    本文件夹主要是 BlazePose PC端的姿态识别代码，具体操作可以查看[这里](02.BlazePose_pc/pc.md)。

- `03.BlazePose_app`
    
    该部分主要是 BlazePose 移动端的姿态识别代码，主要使用[TNN](https://github.com/Tencent/TNN)开发。具体信息查看[这里](03.BlazePose_app/app.md)

- `04.BlazePose_unity`

    本文件夹主要是 BlazePose 虚拟机器人的姿态模仿代码，具体操作可以查看[这里](04.BlazePose_unity/unity.md)。

- `05.BlazePose_robot`

    该部分主要是 BlazePose 真实机器人的姿态模仿代码，具体操作可以查看[这里](05.BlazePose_robot/robot.md)。



## Requirements
```
tensorflow
pathlib
scipy

cv2
mediapipe
numpy
matplotlib
open3d
time
tqdm
socket
serial
math
```

## 环境

```
Linux (Ubuntu 18.04 LTS)
RTX 3090ti
windows10
python3.9
IntelliJ IDEA 2021.3 (Ultimate Edition)
Android Studio Bumblebee | 2021.1.1 Patch 2
Unity 2022.1.0f1c1
arduino 1.8.19
```


## 参考文献

```tex
@article{Bazarevsky2020BlazePoseOR,
  title={BlazePose: On-device Real-time Body Pose tracking},
  author={Valentin Bazarevsky and I. Grishchenko and K. Raveendran and Tyler Lixuan Zhu and Fangfang Zhang and M. Grundmann},
  journal={ArXiv},
  year={2020},
  volume={abs/2006.10204}
}
```

## 联系方式
QQ：1563233274

邮箱：[tyzq1563233274@outlook.com](mailto:tyzq1563233274@outlook.com)