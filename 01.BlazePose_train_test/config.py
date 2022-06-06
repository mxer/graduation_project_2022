'''
@Author  : 1180300204-陶冶
@File    : config.py
@Software: IntelliJ IDEA
'''
num_joints = 14     

batch_size = 128
total_epoch = 200
dataset = "lsp" # 或者lspet

# 0-热图, 1-回归
train_mode = 0

# Eval mode: 0-output image, 1-pck score
eval_mode = 0

continue_train = 0

best_pre_train = 115 

# for test only
epoch_to_test = 106