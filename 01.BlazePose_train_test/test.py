'''
@Author  : 1180300204-陶冶
@File    : test.py
@Software: IntelliJ IDEA
'''
import cv2, os
import tensorflow as tf
import numpy as np
import pathlib
from model import BlazePose
from config import epoch_to_test, eval_mode, dataset
from data import data, label

def Eclidian2(a, b):
# Calculate the square of Eclidian distance
    assert len(a)==len(b)
    summer = 0
    for i in range(len(a)):
        summer += (a[i] - b[i]) ** 2
    return summer

checkpoint_path_regression = "checkpoints_regression"
loss_func_mse = tf.keras.losses.MeanSquaredError()
loss_func_bce = tf.keras.losses.BinaryCrossentropy()
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

model = BlazePose().call()
model.compile(optimizer, loss=[loss_func_bce, loss_func_mse, loss_func_bce])

print("Load regression weights", os.path.join(checkpoint_path_regression, "models/model_ep{}.h5".format(epoch_to_test)))
model.load_weights(os.path.join(checkpoint_path_regression, "models/model_ep{}.h5".format(epoch_to_test)))

if dataset == "lsp":
    number_images = 2000
    coordinates = np.zeros((200, 14, 2)).astype(np.uint8)
    visibility = np.zeros((200, 14, 1)).astype(np.uint8)
    batch_size = 20
    for i in range(number_images - 200, number_images, batch_size):
        if i + batch_size >= number_images:
            # last batch
            _, coordinates[(i - 1800):(number_images - 1800)], visibility[(i - 1800):(number_images - 1800)] = model.predict(data[i:number_images])
        else:
            # other batches
            _, coordinates[(i - 1800):(i - 1800 + batch_size)], visibility[(i - 1800):(i - 1800 + batch_size)] = model.predict(data[i:(i + batch_size)])
        print("=", end="")
    print(">")

    if eval_mode:
        # CALCULATE PCK SCORE
        y = coordinates.astype(float)
        label = label[:, :, 0:2].astype(float)
        score_j = np.zeros(14)
        pck_metric = 0.5
        for i in range(number_images - 200, number_images):
            # validation part
            pck_h = Eclidian2(label[i][12], label[i][13])
            for j in range(14):
                pck_j = Eclidian2(y[i - 1800][j], label[i][j])
                # pck_j <= pck_h * 0.5 --> True
                if pck_j <= pck_h * pck_metric:
                    # True estimation
                    score_j[j] += 1
        # convert to percentage
        score_j = score_j * 0.1
        score_avg = sum(score_j) / 14
        print(score_j)
        print("Average = %f%%" % score_avg)
    else:
        pathlib.Path("result").mkdir(parents=True, exist_ok=True)
        # GENERATE RESULT IMAGES
        for t in range(number_images - 200, number_images):
            skeleton = coordinates[t - 1800]
            img = data[t].astype(np.uint8)
            # draw the joints
            for i in range(14):
                cv2.circle(img, center=tuple(skeleton[i][0:2]), radius=2, color=(0, 255, 0), thickness=2)
            # draw the lines
            for j in ((13, 12), (12, 8), (12, 9), (8, 7), (7, 6), (9, 10), (10, 11), (2, 3), (2, 1), (1, 0), (3, 4), (4, 5)):
                cv2.line(img, tuple(skeleton[j[0]][0:2]), tuple(skeleton[j[1]][0:2]), color=(0, 0, 255), thickness=1)
            # solve the mid point of the hips
            cv2.line(img, tuple(skeleton[12][0:2]), tuple(skeleton[2][0:2] // 2 + skeleton[3][0:2] // 2), color=(0, 0, 255), thickness=1)

            cv2.imwrite("./result/lsp_%d.jpg"%t, img)
else:
    number_images = 10000
    coordinates = np.zeros((1000, 14, 2)).astype(np.uint8)
    visibility = np.zeros((1000, 14, 1)).astype(np.uint8)
    batch_size = 20
    for i in range(number_images - 1000, number_images, batch_size):
        if i + batch_size >= number_images:
            # last batch
            _, coordinates[(i - 9000):(number_images - 9000)], visibility[(i - 9000):(number_images - 9000)] = model.predict(data[i:number_images])
        else:
            # other batches
            _, coordinates[(i - 9000):(i - 9000 + batch_size)], visibility[(i - 9000):(i - 9000 + batch_size)] = model.predict(data[i:(i + batch_size)])
        print("=", end="")
    print(">")

    if eval_mode:
        # CALCULATE PCK SCORE
        y = coordinates.astype(float)
        label = label[:, :, 0:2].astype(float)
        score_j = np.zeros(14)
        pck_metric = 0.5
        for i in range(number_images - 1000, number_images):
            # validation part
            pck_h = Eclidian2(label[i][12], label[i][13])
            for j in range(14):
                pck_j = Eclidian2(y[i - 9000][j], label[i][j])
                # pck_j <= pck_h * 0.5 --> True
                if pck_j <= pck_h * pck_metric:
                    # True estimation
                    score_j[j] += 1
        # convert to percentage
        score_j = score_j * 0.1
        score_avg = sum(score_j) / 14
        print(score_j)
        print("Average = %f%%" % score_avg)
    else:
        pathlib.Path("result").mkdir(parents=True, exist_ok=True)
        # GENERATE RESULT IMAGES
        for t in range(number_images - 1000, number_images):
            skeleton = coordinates[t - 9000]
            img = data[t].astype(np.uint8)
            # draw the joints
            for i in range(14):
                cv2.circle(img, center=tuple(skeleton[i][0:2]), radius=2, color=(0, 255, 0), thickness=2)
            # draw the lines
            for j in ((13, 12), (12, 8), (12, 9), (8, 7), (7, 6), (9, 10), (10, 11), (2, 3), (2, 1), (1, 0), (3, 4), (4, 5)):
                cv2.line(img, tuple(skeleton[j[0]][0:2]), tuple(skeleton[j[1]][0:2]), color=(0, 0, 255), thickness=1)
            # solve the mid point of the hips
            cv2.line(img, tuple(skeleton[12][0:2]), tuple(skeleton[2][0:2] // 2 + skeleton[3][0:2] // 2), color=(0, 0, 255), thickness=1)

            cv2.imwrite("./result/lsp_%d.jpg"%t, img)
