# coding=utf-8
u"""
Face Shape Dictionary
=====================

Face Rig 正式修型名称和制作规范。

本模块只负责定义 Face Shape 数据，不创建 Maya 节点，不执行 BlendShape，
也不承担 Driver / Corrective 的构建逻辑。

命名规范
--------
1. 所有正式 Shape 名称统一使用 snake_case；
2. 全部使用小写字母，单词之间使用下划线分隔；
3. Left / Right 方向后缀统一使用 ``_left`` / ``_right``；
4. Primary Shape、Combination Shape 和 Corrective Shape 分开管理；
5. Corrective Shape 默认使用 ``*_corrective`` 后缀；
6. 本文件是 Face Shape 正式名称和制作要求的唯一数据来源。

设计边界
--------
- Shape 名称和制作规范保留在本模块；
- BlendShape 的通用创建 / 查询能力由 core.blendshape_utils 负责；
- Face Component 只消费本模块定义的数据，不重复硬编码 Shape 名称；
- UI、Driver、Corrective 和后续 FACS Layer 应从本模块读取统一名称。
"""

from __future__ import print_function


# =============================================================================
# Shape Type
# =============================================================================

primary_shape_type = "primary"
combination_shape_type = "combination"
corrective_shape_type = "corrective"

corrective_suffix = "_corrective"


# =============================================================================
# Region
# =============================================================================

brow_region = "brow"
eye_region = "eye"
nose_region = "nose"
cheek_region = "cheek"
mouth_region = "mouth"
lip_region = "lip"


# =============================================================================
# Primary Shape Names
# =============================================================================

brow_shape_names = [
    "brow_up",
    "brow_down",
    "brow_squeeze",
]

eye_shape_names = [
    "eye_up_wide",
    "eye_down_wide",
    "eye_up_close",
    "eye_down_close",
    "eye_up_mid",
    "eye_down_mid",
]

nose_shape_names = [
    "sneer",
    "squint",
]

cheek_shape_names = [
    "cheek_out",
    "cheek_in",
    "cheek_up",
    "cheek_down",
]

mouth_shape_names = [
    "mouth_smile",
    "mouth_frown",
    "mouth_stretch",
    "mouth_narrow",
    "mouth_narrow_up",
    "mouth_narrow_down",
    "mouth_corner_up",
    "mouth_corner_down",
    "mouth_side_left",
]

lip_shape_names = [
    "lip_roll_out",
    "lip_roll_in",
    "lip_pout",
    "lip_pout_left",
]

primary_shape_names = []

for shape_names in [
        brow_shape_names,
        eye_shape_names,
        nose_shape_names,
        cheek_shape_names,
        mouth_shape_names,
        lip_shape_names
]:
    for shape_name in shape_names:
        primary_shape_names.append(
            shape_name
        )


# =============================================================================
# Combination Shape Names
# =============================================================================

combination_shape_names = [
    "eye_expand",
    "eye_crush",
]


# =============================================================================
# Face Shape Dictionary
# =============================================================================

face_shape_dictionary = {
    # -------------------------------------------------------------------------
    # Brow
    # -------------------------------------------------------------------------
    "brow_up": {
        "region": brow_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"眉毛整体向上抬起。",
        "sculpt_notes": [
            u"抬眉时需要表现额头纹。",
            u"额头褶皱应该偏宽、偏厚，不要雕得过于锋利。",
            u"褶皱之间需要保持柔和过渡。",
            u"从头部外围观察时，额头轮廓应该保持圆弧。",
            u"眉毛抬起时需要保持眉弓和额头本身的体积感。",
            u"不能只把眉毛位置简单向上移动。",
        ],
    },
    "brow_down": {
        "region": brow_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"眉毛整体向下挤压。",
        "sculpt_notes": [
            u"眉毛向下挤压时需要产生明显的肌肉挤压感。",
            u"眉头区域会鼓起，并产生宽厚褶皱。",
            u"眉毛整体尽量保持比较平直的下压趋势。",
            u"极限状态的下压幅度可以覆盖接近半个眼睛。",
            u"角色存在鱼尾纹时，可以适当加强对应动态。",
            u"眉弓、眉间和眼眶上方需要形成连续的肉感变化。",
        ],
    },
    "brow_squeeze": {
        "region": brow_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"左右眉毛向眉心方向挤压。",
        "sculpt_notes": [
            u"两侧眉毛向眉心收缩，并在眉间形成肌肉堆积。",
            u"两侧动态需要平滑地向中间过渡。",
            u"褶皱不要求完全左右镜像。",
            u"褶皱尽量宽厚，不要雕成锋利刻痕。",
            u"从侧面观察眉间区域应该保持圆弧。",
            u"需要表现肌肉向中央并略向下挤压的感觉。",
        ],
    },

    # -------------------------------------------------------------------------
    # Eye
    # -------------------------------------------------------------------------
    "eye_up_wide": {
        "region": eye_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"上眼睑沿眼球表面向上打开。",
        "sculpt_notes": [
            u"上眼睑需要沿眼球表面向上滑动。",
            u"睁大后应该明显露出更多瞳孔区域。",
            u"动作范围可以较大，但不要带动眉弓。",
            u"眼皮始终需要保持与眼球之间合理的包裹距离。",
            u"从侧面观察需要形成贴合眼球的干净圆弧。",
        ],
    },
    "eye_down_wide": {
        "region": eye_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"下眼睑沿眼球表面向下打开。",
        "sculpt_notes": [
            u"下眼睑需要沿眼球表面向下滑动。",
            u"不能简单沿世界坐标垂直向下拉低。",
            u"需要保持下眼睑与眼球之间的距离。",
            u"眼角结构不能因为 Wide 动作被拉坏。",
            u"与 eye_up_wide 组合后形成完整的睁眼动作。",
        ],
    },
    "eye_up_close": {
        "region": eye_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"上眼睑沿眼球表面向下闭合。",
        "sculpt_notes": [
            u"上眼睑需要沿眼球球面向下运动。",
            u"从侧面观察必须形成干净的弧形。",
            u"不能直接沿世界 Y 方向向下移动。",
            u"极限状态需要真正与下眼睑闭合。",
            u"闭合过程中需要保持眼睑厚度。",
            u"眼睑不能穿入眼球。",
        ],
    },
    "eye_down_close": {
        "region": eye_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"下眼睑沿眼球表面向上辅助闭合。",
        "sculpt_notes": [
            u"下眼睑沿眼球表面向上运动。",
            u"运动量通常小于上眼睑。",
            u"需要保留眼袋和卧蚕区域的体积。",
            u"与 eye_up_close 共同完成完整闭眼。",
        ],
    },
    "eye_up_mid": {
        "region": eye_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"上眼睑 Wide / Close 过程中的中间状态修型。",
        "sculpt_notes": [
            u"用于改善 Neutral 到 Wide 或 Close 之间的非线性眼皮运动。",
            u"需要保证中间状态仍然沿眼球形成合理弧线。",
            u"用于减少单纯线性 BlendShape 产生的机械感。",
        ],
    },
    "eye_down_mid": {
        "region": eye_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"下眼睑 Wide / Close 过程中的中间状态修型。",
        "sculpt_notes": [
            u"用于改善下眼睑线性 BlendShape 产生的机械运动。",
            u"需要保持下眼睑体积和眼球包裹关系。",
        ],
    },

    # -------------------------------------------------------------------------
    # Nose / Central Face
    # -------------------------------------------------------------------------
    "sneer": {
        "region": nose_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"鼻翼和鼻根附近肌肉向上、向内挤压。",
        "sculpt_notes": [
            u"靠近眉头的区域需要表现向外挤压的感觉。",
            u"鼻翼两侧肌肉整体向上并向内收缩。",
            u"鼻翼周围必须保持圆润并做好过渡。",
            u"褶皱允许左右存在轻微不对称。",
            u"褶皱尽量宽厚，不要雕成尖锐细线。",
            u"从侧面观察鼻翼和上唇区域需要保持圆弧肉感。",
        ],
    },
    "squint": {
        "region": nose_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"下眼睑、鼻翼和脸颊向眼睛区域挤压。",
        "sculpt_notes": [
            u"主要表现眼皮下方肌肉向上挤压。",
            u"肌肉同时向鼻翼和脸颊内侧聚拢。",
            u"下眼睑会被推高并产生变厚的肌肉感。",
            u"卧蚕区域需要形成明显圆弧。",
            u"鼻翼两侧从侧面观察需要保持柔软的圆弧肉感。",
            u"不能把 Squint 简化成单纯把眼睛闭小。",
        ],
    },

    # -------------------------------------------------------------------------
    # Cheek
    # -------------------------------------------------------------------------
    "cheek_out": {
        "region": cheek_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"脸颊向外鼓起。",
        "sculpt_notes": [
            u"整体需要保持圆润并有明显体积。",
            u"保持苹果肌原有结构，避免局部形成尖锐凸起。",
            u"可以使用辅助球体和 ShrinkWrap 帮助建立基础体积。",
        ],
        "build_notes": [
            u"创建一个辅助球体并放到脸颊区域。",
            u"先选择头部，再选择辅助球体创建 ShrinkWrap。",
            u"刷出需要影响的脸颊范围。",
            u"Projection 使用 Vertex Normal。",
            u"根据投射方向需要开启 Reverse。",
            u"移动球体调整脸颊鼓出体积，最后人工修整体过渡。",
        ],
    },
    "cheek_in": {
        "region": cheek_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"脸颊向内收缩。",
        "sculpt_notes": [
            u"可以参考 cheek_out 的反向运动趋势建立基础形状。",
            u"不能简单把 cheek_out 的结果做数值反向。",
            u"需要重新检查苹果肌、法令纹、嘴角、眼袋和鼻翼的体积关系。",
        ],
    },
    "cheek_up": {
        "region": cheek_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"脸颊和苹果肌整体向上运动。",
        "sculpt_notes": [
            u"苹果肌向上移动并保持鼓起体积。",
            u"通常会影响下眼睑、卧蚕、法令纹和嘴角。",
            u"需要保持脸颊到眼眶之间连续的肌肉过渡。",
        ],
    },
    "cheek_down": {
        "region": cheek_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"脸颊肌肉整体向下运动。",
        "sculpt_notes": [
            u"需要保持脸颊本身的体积。",
            u"保持鼻唇沟结构和下颌区域的自然过渡。",
        ],
    },

    # -------------------------------------------------------------------------
    # Mouth
    # -------------------------------------------------------------------------
    "mouth_smile": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"整个嘴部形成自然微笑。",
        "sculpt_notes": [
            u"整个嘴唇趋势向上，嘴角向上并向外运动。",
            u"苹果肌需要同时向上并鼓起。",
            u"整体嘴部轮廓保持圆弧。",
            u"法令纹会更加明显。",
            u"嘴角不能形成锋利尖角，也不能向脸部内部陷得太深。",
            u"嘴角区域需要保持平滑肉感并清理坑洼。",
        ],
    },
    "mouth_frown": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"嘴角向下形成 Frown。",
        "sculpt_notes": [
            u"嘴角向下的整体形状需要保持圆弧。",
            u"从人中到嘴角的下降趋势需要逐渐过渡。",
            u"嘴角两侧会发生肌肉堆叠，需要表现肉感挤压。",
            u"鼻翼可以产生轻微向下的跟随。",
            u"褶皱需要有自然的深浅过渡。",
        ],
    },
    "mouth_stretch": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"嘴部沿牙齿外轮廓向两侧拉宽。",
        "sculpt_notes": [
            u"嘴角沿牙齿外轮廓向两侧移动。",
            u"运动轨迹需要是沿表面的弧形，而不是简单沿世界 X 轴拉开。",
            u"法令纹会更加明显。",
            u"嘴唇因为向外拉伸会变薄、变长。",
            u"拉伸后仍然需要保存嘴唇结构线。",
        ],
    },
    "mouth_narrow": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"嘴部两侧沿牙齿轮廓向中央挤压。",
        "sculpt_notes": [
            u"嘴唇两侧沿牙齿外轮廓向内运动。",
            u"嘴唇需要保持饱满的肉感。",
            u"可以带有轻微向前突出的运动量，但不能过度突出。",
            u"整体嘴唇需要修得更圆、更厚实。",
        ],
    },
    "mouth_narrow_up": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"以上嘴唇区域为主的 Narrow 修型。",
        "sculpt_notes": [
            u"保持 mouth_narrow 的整体弧形运动逻辑。",
            u"主要控制上嘴唇向中央挤压的形变。",
        ],
    },
    "mouth_narrow_down": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"以下嘴唇区域为主的 Narrow 修型。",
        "sculpt_notes": [
            u"保持 mouth_narrow 的整体弧形运动逻辑。",
            u"主要控制下嘴唇向中央挤压的形变。",
        ],
    },
    "mouth_corner_up": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"嘴角局部向上运动。",
        "sculpt_notes": [
            u"中间嘴唇仍然需要保持自然圆弧。",
            u"唇珠不能因为嘴角上提而变尖。",
            u"中央嘴唇不要受到过度影响。",
        ],
    },
    "mouth_corner_down": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"嘴角局部向下运动。",
        "sculpt_notes": [
            u"中央唇形需要保持稳定和圆弧。",
            u"唇珠不能因为嘴角下压而变尖。",
            u"嘴角附近可以形成适当的肌肉堆积。",
        ],
    },
    "mouth_side_left": {
        "region": mouth_region,
        "shape_type": primary_shape_type,
        "side": "lf",
        "description": u"整个嘴部沿牙齿表面向左侧弧形滑动。",
        "sculpt_notes": [
            u"动作不能只是沿世界 X 轴平移。",
            u"嘴唇需要顺着牙齿外表面产生弧形运动。",
            u"从下方观察应该看到明显的弧形运动轨迹。",
            u"鼻部需要产生一定程度的跟随。",
            u"受压侧法令纹会更加明显并产生肉感堆积。",
            u"对侧法令纹会被拉长。",
            u"避免整个脸颊被过度向外带动。",
        ],
    },

    # -------------------------------------------------------------------------
    # Lip
    # -------------------------------------------------------------------------
    "lip_roll_out": {
        "region": lip_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"上下嘴唇向外翻转。",
        "sculpt_notes": [
            u"必须明确表现嘴唇向外翻面的结构。",
            u"嘴唇原有结构线在翻转后仍然需要保留。",
            u"唇线需要保持清晰。",
            u"越靠近嘴角，翻转幅度需要逐渐减小。",
            u"嘴角区域需要平滑过渡。",
            u"翻出后仍然保持嘴唇本身的弧度和饱满肉感。",
        ],
    },
    "lip_roll_in": {
        "region": lip_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"上下嘴唇向内卷，形成抿嘴动作。",
        "sculpt_notes": [
            u"需要有明确的抿嘴和向内收的感觉。",
            u"外部嘴唇轮廓仍然保持圆弧。",
            u"中间唇缝尽量保持平整。",
            u"唇缝阴影宽度尽量保持稳定。",
            u"最好仍然保留少量唇缘在外部。",
            u"内卷过程中不能让嘴唇本身的肉感消失。",
            u"需要修补内卷产生的坑洼区域。",
        ],
    },
    "lip_pout": {
        "region": lip_region,
        "shape_type": primary_shape_type,
        "side": "md",
        "description": u"整个嘴唇向前并略向上推出。",
        "sculpt_notes": [
            u"整体需要表现向前推出并略向上提的感觉。",
            u"嘴唇运动需要沿牙齿和口腔外轮廓。",
            u"保持上下嘴唇原有的饱满体积。",
            u"不能只是简单沿世界 Z 轴推出。",
        ],
    },
    "lip_pout_left": {
        "region": lip_region,
        "shape_type": primary_shape_type,
        "side": "lf",
        "description": u"嘴唇向左侧沿牙齿表面滑动。",
        "sculpt_notes": [
            u"以下嘴唇横向运动更加明显。",
            u"以嘴角作为运动终点。",
            u"从中央到嘴角的运动量需要逐渐减小。",
            u"保持沿牙齿表面的弧形运动轨迹。",
        ],
    },

    # -------------------------------------------------------------------------
    # Combination
    # -------------------------------------------------------------------------
    "eye_expand": {
        "region": eye_region,
        "shape_type": combination_shape_type,
        "side": "md",
        "description": u"惊讶、吃惊时眼睛明显扩大并伴随眉毛上挑。",
        "inputs": [
            "brow_up",
            "eye_up_wide",
            "eye_down_wide",
        ],
        "sculpt_notes": [
            u"瞳孔需要产生放大的表现。",
            u"眉毛明显向上挑。",
            u"上下眼睑同时打开。",
            u"不能只把基础 Shape 做线性相加，需要保留自然的整体表情关系。",
        ],
    },
    "eye_crush": {
        "region": eye_region,
        "shape_type": combination_shape_type,
        "side": "md",
        "description": u"眯眼时脸部中央区域产生强烈的肌肉挤压。",
        "inputs": [
            "brow_down",
            "sneer",
            "squint",
            "eye_up_close",
        ],
        "sculpt_notes": [
            u"眉毛向下压。",
            u"上眼睑压低，下眼睑和脸颊向上挤压。",
            u"鼻翼向上并向内收缩。",
            u"眉间、眼下和鼻翼之间需要形成连续的肌肉堆积。",
            u"最终效果不能只是基础 Shape 的线性叠加，需要额外 Corrective 处理。",
        ],
    },
}


# =============================================================================
# Deprecated / Normalized Names
# =============================================================================

shape_name_aliases = {
    "borwDown": "brow_down",
    "cheekUP": "cheek_up",
    "lipPount": "lip_pout",
    "mouthPount": "lip_pout",
    "lipPountleft": "lip_pout_left",
    "mouthWide": "mouth_stretch",
    "mouthRollOut": "lip_roll_out",
    "rollIN": "lip_roll_in",
}


# =============================================================================
# Public Data
# =============================================================================

all_shape_names = []

for shape_name in primary_shape_names:
    all_shape_names.append(
        shape_name
    )

for shape_name in combination_shape_names:
    all_shape_names.append(
        shape_name
    )


__all__ = [
    "primary_shape_type",
    "combination_shape_type",
    "corrective_shape_type",
    "corrective_suffix",
    "brow_region",
    "eye_region",
    "nose_region",
    "cheek_region",
    "mouth_region",
    "lip_region",
    "brow_shape_names",
    "eye_shape_names",
    "nose_shape_names",
    "cheek_shape_names",
    "mouth_shape_names",
    "lip_shape_names",
    "primary_shape_names",
    "combination_shape_names",
    "face_shape_dictionary",
    "shape_name_aliases",
    "all_shape_names",
]
