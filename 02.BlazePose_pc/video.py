'''
@Author  : 1180300204-陶冶
@File    : 04.video.py
@Software: IntelliJ IDEA
'''
import cv2
import mediapipe as mp
from tqdm import tqdm
import time

mp_pose = mp.solutions.pose

# 导入绘图函数
mp_drawing = mp.solutions.drawing_utils

# 导入模型
pose = mp_pose.Pose(static_image_mode=False,        # 是静态图片还是连续视频帧
                    model_complexity=1,            # 选择人体姿态关键点检测模型，选1
                    smooth_landmarks=True,         # 是否平滑关键点
                    min_detection_confidence=0.5,  # 置信度阈值
                    min_tracking_confidence=0.5)   # 追踪阈值

def process_frame(img):
    start_time = time.time()

    h, w = img.shape[0], img.shape[1]

    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 结果
    results = pose.process(img_RGB)

    if results.pose_landmarks: 

        # 可视化关键点和连线
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        for i in range(33): 

            # 获取关键点的三维坐标
            cx = int(results.pose_landmarks.landmark[i].x * w)
            cy = int(results.pose_landmarks.landmark[i].y * h)
            cz = results.pose_landmarks.landmark[i].z

            radius = 10
            
            # 着色，美观
            if i == 0: # 鼻
                img = cv2.circle(img,(cx,cy), radius, (0,0,255), -1)
            elif i in [11,12]: # 肩
                img = cv2.circle(img,(cx,cy), radius, (223,155,6), -1)
            elif i in [23,24]: # 髋
                img = cv2.circle(img,(cx,cy), radius, (1,240,255), -1)
            elif i in [13,14]: # 胳膊肘
                img = cv2.circle(img,(cx,cy), radius, (140,47,240), -1)
            elif i in [25,26]: # 膝
                img = cv2.circle(img,(cx,cy), radius, (0,0,255), -1)
            elif i in [15,16,27,28]: # 手腕、脚腕
                img = cv2.circle(img,(cx,cy), radius, (223,155,60), -1)
            elif i in [17,19,21]: # 左手
                img = cv2.circle(img,(cx,cy), radius, (94,218,121), -1)
            elif i in [18,20,22]: # 右手
                img = cv2.circle(img,(cx,cy), radius, (16,144,247), -1)
            elif i in [27,29,31]: # 左脚
                img = cv2.circle(img,(cx,cy), radius, (29,123,243), -1)
            elif i in [28,30,32]: # 右脚
                img = cv2.circle(img,(cx,cy), radius, (193,182,255), -1)
            elif i in [9,10]: # 嘴
                img = cv2.circle(img,(cx,cy), radius, (205,235,255), -1)
            elif i in [1,2,3,4,5,6,7,8]: # 眼、脸颊
                img = cv2.circle(img,(cx,cy), radius, (94,218,121), -1)
            else: # 其它关键点
                img = cv2.circle(img,(cx,cy), radius, (0,255,0), -1)

    else:
        scaler = 1
        failure_str = 'No Person!'
        img = cv2.putText(img, failure_str, (25 * scaler, 100 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)

    # 记录该帧处理完毕的时间
    end_time = time.time()
    # 计算每秒处理图像帧数FPS
    FPS = 1/(end_time - start_time)

    scaler = 1
    # 显示FPS数值
    img = cv2.putText(img, 'FPS  '+str(int(FPS)), (25 * scaler, 50 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)
    return img


#生成输出视频
def generate_video(input_path='./'):
    filehead = input_path.split('/')[-1]
    output_path = "result-" + filehead

    print('开始',input_path)

    # 获取视频总帧数
    cap = cv2.VideoCapture(input_path)
    frame_count = 0
    while(cap.isOpened()):
        success, frame = cap.read()
        frame_count += 1
        if not success:
            break
    cap.release()
    print('总帧数为',frame_count)

    cap = cv2.VideoCapture(input_path)
    frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, fourcc, fps, (int(frame_size[0]), int(frame_size[1])))

    # 进度条
    with tqdm(total=frame_count-1) as pbar:
        try:
            while(cap.isOpened()):
                success, frame = cap.read()
                if not success:
                    break
                try:
                    frame = process_frame(frame)
                except:
                    print('error')
                    pass
                if success == True:
                    out.write(frame)
                    # 进度条更新一帧
                    pbar.update(1)
        except:
            print('中断')
            pass

    cv2.destroyAllWindows()
    out.release()
    cap.release()
    print('视频已保存', output_path)

generate_video(input_path='./sport01.mp4')