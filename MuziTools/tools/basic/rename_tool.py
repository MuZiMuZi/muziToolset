# 批量重命名工具 (Maya 2023, 纯 cmds)
import maya.cmds as cmds
import re

WIN = "renameTool"

# ---------- 前缀/后缀（手动输入） ----------
def add_prefix(*_):
    pre = cmds.textField("preField", q=True, text=True)
    if not pre:
        cmds.warning("请输入前缀")
        return
    objs = cmds.ls(sl=True, sn=True)
    if not objs:
        cmds.warning("请先选中物体")
        return
    for obj in objs:
        new = pre + obj
        if new != obj:
            cmds.rename(obj, new)

def add_suffix(*_):
    suf = cmds.textField("sufField", q=True, text=True)
    if not suf:
        cmds.warning("请输入后缀")
        return
    objs = cmds.ls(sl=True, sn=True)
    if not objs:
        cmds.warning("请先选中物体")
        return
    for obj in objs:
        new = obj + suf
        if new != obj:
            cmds.rename(obj, new)

# ---------- 查找替换 ----------
def get_objects_by_scope():
    scope = cmds.radioButtonGrp("scopeRadio", q=True, select=True)
    if scope == 2:  # 层级
        objs = cmds.ls(sl=True, sn=True)
        if not objs:
            return []
        children = cmds.listRelatives(objs, ad=True, type='transform', f=True) or []
        objs.extend(children)
        seen = set()
        result = []
        for obj in objs:
            if obj not in seen:
                result.append(obj)
                seen.add(obj)
        return result
    elif scope == 3:  # 全部
        return cmds.ls(transforms=True, sn=True)
    else:  # 选中物体
        return cmds.ls(sl=True, sn=True)

def search_replace(*_):
    src = cmds.textField("srcField", q=True, text=True)
    dst = cmds.textField("dstField", q=True, text=True)
    if not src:
        cmds.warning("请输入查找内容")
        return

    objs = get_objects_by_scope()
    if not objs:
        cmds.warning("没有可操作的对象")
        return

    for obj in objs:
        new = obj.replace(src, dst)
        if new != obj:
            cmds.rename(obj, new)

# ---------- 自动编号 ----------
def number_to_alpha(n, uppercase=True):
    """将整数转换为 Excel 列字母 (0 -> A, 1 -> B, ...)"""
    result = []
    base = ord('A')
    while True:
        n, remainder = divmod(n, 26)
        result.append(chr(base + remainder))
        if n == 0:
            break
        n -= 1
    s = ''.join(reversed(result))
    return s if uppercase else s.lower()

def auto_number(*_):
    base = cmds.textField("baseField", q=True, text=True)
    start = cmds.intField("startInt", q=True, v=True)
    pad = cmds.intField("padInt", q=True, v=True)
    num_type = cmds.optionMenu("numTypeMenu", q=True, v=True)

    objs = cmds.ls(sl=True, sn=True)
    if not objs:
        cmds.warning("请先选中物体")
        return

    for i, obj in enumerate(objs):
        num = start + i
        if num_type == "Numbers":
            ns = str(num).zfill(pad) if pad > 0 else str(num)
        else:
            alpha_num = num - 1
            if alpha_num < 0:
                cmds.warning("起始数字不能为0或负数，已跳过")
                continue
            alpha = number_to_alpha(alpha_num, uppercase=(num_type == "Uppercase Letters"))
            fill_char = 'A' if num_type == "Uppercase Letters" else 'a'
            ns = alpha.rjust(pad, fill_char) if pad > len(alpha) else alpha

        nb = base if base else obj
        new = nb + "_" + ns
        if new != obj:
            cmds.rename(obj, new)

# ---------- 重命名（星号分组补零，使用同一数字） ----------
def pattern_rename(*_):
    pattern = cmds.textField("patternField", q=True, text=True)
    if not pattern:
        cmds.warning("请输入重命名模式")
        return

    if '*' not in pattern:
        objs = cmds.ls(sl=True, sn=True)
        if not objs:
            cmds.warning("请先选中物体")
            return
        for i, obj in enumerate(objs):
            num = 1 + i
            new = pattern + str(num)
            if new != obj:
                cmds.rename(obj, new)
        return

    star_blocks = re.findall(r'\*+', pattern)
    if not star_blocks:
        return
    block_lengths = [len(block) for block in star_blocks]
    parts = re.split(r'\*+', pattern)

    objs = cmds.ls(sl=True, sn=True)
    if not objs:
        cmds.warning("请先选中物体")
        return

    for i, obj in enumerate(objs):
        num = 1 + i
        num_strs = [str(num).zfill(length) for length in block_lengths]
        new = parts[0]
        for idx, ns in enumerate(num_strs):
            new += ns + parts[idx+1]
        if new != obj:
            cmds.rename(obj, new)

# ---------- 界面 ----------
def main():
    if cmds.window(WIN, exists=True):
        cmds.deleteUI(WIN)
    w = cmds.window(WIN, t="重命名工具", wh=(460, 580))
    main = cmds.columnLayout(adj=True, rs=10, columnAttach=('both', 10))

    # ---------- 1. 前缀 / 后缀 ----------
    frame1 = cmds.frameLayout(l="前缀 / 后缀", cll=True, bs='etchedIn', marginWidth=10, marginHeight=10)
    col1 = cmds.columnLayout(adj=True, rs=6)
    cmds.rowLayout(nc=3, adj=2, columnAttach=[(1,'both',0),(2,'both',0),(3,'both',0)])
    cmds.text(l="前缀：", w=50, align='right')
    cmds.textField("preField")
    cmds.button(l="执行", c=add_prefix, w=60, bgc=(0.3, 0.6, 0.9))
    cmds.setParent("..")
    cmds.rowLayout(nc=3, adj=2, columnAttach=[(1,'both',0),(2,'both',0),(3,'both',0)])
    cmds.text(l="后缀：", w=50, align='right')
    cmds.textField("sufField")
    cmds.button(l="执行", c=add_suffix, w=60, bgc=(0.3, 0.6, 0.9))
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    # ---------- 2. 查找与替换 ----------
    frame2 = cmds.frameLayout(l="查找与替换", cll=True, bs='etchedIn', marginWidth=10, marginHeight=10)
    col2 = cmds.columnLayout(adj=True, rs=6)
    cmds.rowLayout(nc=2, adj=2, columnAttach=[(1,'both',0),(2,'both',0)])
    cmds.text(l="查找：", w=50, align='right')
    cmds.textField("srcField")
    cmds.setParent("..")
    cmds.rowLayout(nc=2, adj=2, columnAttach=[(1,'both',0),(2,'both',0)])
    cmds.text(l="替换为：", w=50, align='right')
    cmds.textField("dstField")
    cmds.setParent("..")
    cmds.radioButtonGrp("scopeRadio", l="范围：", numberOfRadioButtons=3,
                        labelArray3=("选中物体", "层级", "全部"),
                        select=1, columnWidth4=[70, 80, 70, 70])
    cmds.button(l="执行", c=search_replace, h=28, bgc=(0.3, 0.6, 0.9))
    cmds.setParent("..")
    cmds.setParent("..")

    # ---------- 3. 自动编号 ----------
    frame3 = cmds.frameLayout(l="自动编号", cll=True, bs='etchedIn', marginWidth=10, marginHeight=10)
    col3 = cmds.columnLayout(adj=True, rs=6)
    cmds.rowLayout(nc=2, adj=2, columnAttach=[(1,'both',0),(2,'both',0)])
    cmds.text(l="起始：", w=70, align='right')
    cmds.intField("startInt", v=1)
    cmds.setParent("..")
    cmds.rowLayout(nc=2, adj=2, columnAttach=[(1,'both',0),(2,'both',0)])
    cmds.text(l="补零位数：", w=70, align='right')
    cmds.intField("padInt", v=2, min=0, max=10)
    cmds.setParent("..")
    cmds.rowLayout(nc=2, adj=2, columnAttach=[(1,'both',0),(2,'both',0)])
    cmds.text(l="编号类型：", w=70, align='right')
    cmds.optionMenu("numTypeMenu")
    cmds.menuItem(l="数字")
    cmds.menuItem(l="大写字母")
    cmds.menuItem(l="小写字母")
    cmds.setParent("..")
    cmds.rowLayout(nc=2, adj=2, columnAttach=[(1,'both',0),(2,'both',0)])
    cmds.text(l="基础名称：", w=70, align='right')
    cmds.textField("baseField", pht="留空则使用原名称")
    cmds.setParent("..")
    cmds.button(l="执行", c=auto_number, h=28, bgc=(0.3, 0.6, 0.9))
    cmds.setParent("..")
    cmds.setParent("..")

    # ---------- 4. 重命名 ----------
    frame4 = cmds.frameLayout(l="重命名", cll=True, bs='etchedIn', marginWidth=10, marginHeight=10)
    col4 = cmds.columnLayout(adj=True, rs=6)
    cmds.rowLayout(nc=3, adj=2, columnAttach=[(1,'both',0),(2,'both',0),(3,'both',0)])
    cmds.text(l="模式：", w=70, align='right')
    cmds.textField("patternField", pht="例如 leg**_** → leg01_01（每组*分别补零）")
    cmds.button(l="执行", c=pattern_rename, w=60, bgc=(0.3, 0.6, 0.9))
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    cmds.showWindow(w)

