# BlazePose 虚拟机器人的姿态模仿代码

首先值得注意的是，本项目的代码大量使用了mediapipe库，但是将官方模型替换成了我们训练好的模型。

因此需要将训练的`.h5`模型用`tf`工具转换成`.tflite`模型，并重命名为`pose_landmark_full.tflite`，将其复制替换到`Python39/Lib/site-packages/mediapipe/modules/pose_landmark`下。

该部分有2部分代码，包括`./MotionCapture.py`、`./PoseModule.py`、`./unity.rar`。

## Requirements
```
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
windows10
python3.9
IntelliJ IDEA 2021.3 (Ultimate Edition)
Unity 2022.1.0f1c1
```

本部分使用unity创建了一个拥有33个关键点的虚拟机器人。

由python程序获得每个点的相对位置/角度，从而使得机器人能够姿态跟踪。

## MotionCapture.py

代码使用的是UDP，创建了在本机"127.0.0.1"上的5052端口，此端口用于将数据传到虚拟机器人端（unity）。

## unity.rar

将本压缩包解压得到`./unity`，再将`./unity`导入到`Unity 2022.1.0f1c1`即可得到拥有33个关键点的机器人。

## 结果

![image](../piture/result_unity.gif)




