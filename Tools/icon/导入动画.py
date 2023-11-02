import json
import maya.cmds as cmds




# 从文本文件中读取动画数据并赋予 blendshape B
fpath1 = r"D:\animation.json"

# Open the file and read the JSON data
with open(fpath1, "r") as f:
    data = f.read()

# Load the JSON data into a Python dictionary
animData = json.loads(data)


# 遍历字典中的每个属性
for attr, keyframeInfo in animData.items():
    # 使用 keyframe 命令将关键帧数据添加到控制器中
    if keyframeInfo == None:
        continue

    for i in range((int(len(keyframeInfo)/2))):
     #   print(len(keyframeInfo))
        x = attr.split('.',1)
        ctrl = x[0]
        attrX = x[1]
        if i == 0:
            cmds.setKeyframe(ctrl,at = attrX, time=(keyframeInfo[0],keyframeInfo[0]), value = keyframeInfo[1])
        else:
            cmds.setKeyframe(ctrl,at = attrX, time=(int(keyframeInfo[i*2]),int(keyframeInfo[i*2])), value = keyframeInfo[i*2+1])

   # 获取第 10 帧到第 20 帧之间的关键帧信息

  #  keyframeInfo = cmds.keyframe(ctrl, attribute=attr, query=True, time=(keyframeInfo[0], keyframeInfo[2]), timeChange=True, valueChange=True)