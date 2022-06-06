'''
@Author  : 1180300204-陶冶
@File    : mask&cloud_3d.py
@Software: IntelliJ IDEA
'''
import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import open3d


def look_img(img):
    '''opencv读入图像格式为BGR，matplotlib可视化格式为RGB，因此需将BGR转RGB'''
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_RGB)
    plt.show()

def get_x(each):
    return each.x
def get_y(each):
    return each.y
def get_z(each):
    return each.z

mp_pose = mp.solutions.pose

# 导入绘图函数
mp_drawing = mp.solutions.drawing_utils

# 导入模型
pose = mp_pose.Pose(static_image_mode=True,        # 是静态图片还是连续视频帧
                    model_complexity=1,            # 选择人体姿态关键点检测模型，选1
                    smooth_landmarks=True,         # 是否平滑关键点
                    enable_segmentation=True,      # 是否人体抠图
                    min_detection_confidence=0.5,  # 置信度阈值
                    min_tracking_confidence=0.5)   # 追踪阈值

img = cv2.imread('sport02.jpg')

img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 结果
results = pose.process(img_RGB)

# 蒙版
mask = results.segmentation_mask

print(mask)

mask = mask > 0.5

plt.imshow(mask)

plt.show()


# 单通道转三通道
mask_3 = np.stack((mask,mask,mask), axis=-1)

MASK_COLOR = [0,200,0]
fg_image = np.zeros(img.shape, dtype=np.uint8)
fg_image[:] = MASK_COLOR

# 前景人像
FG_img = np.where(mask_3, img, fg_image)

# 背景
BG_img = np.where(~mask_3, img, fg_image)

look_img(FG_img)
look_img(BG_img)

coords = np.array(results.pose_landmarks.landmark)

# 分别获取所有关键点的XYZ坐标
points_x = np.array(list(map(get_x, coords)))
points_y = np.array(list(map(get_y, coords)))
points_z = np.array(list(map(get_z, coords)))

# 将三个方向的坐标合并
points = np.vstack((points_x, points_y, points_z)).T

# 3d云图
point_cloud = open3d.geometry.PointCloud()
point_cloud.points = open3d.utility.Vector3dVector(points)
open3d.visualization.draw_geometries([point_cloud])