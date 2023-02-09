from maya import cmds


bpjnt_lists = cmds.ls('l_*_rig')
print(bpjnt_lists)
for bpjnt_list in bpjnt_lists :
    print(bpjnt_list)
    bpjnt_list_jnts = cmds.listRelatives('{}'.format(bpjnt_list) , ad = True , c = True)
    bpjnt_list_jnts.reverse()
    for jnt in bpjnt_list_jnts :
        print(jnt)
        mirror_jnt = jnt.replace('_l_' , '_r_')
    cmds.setAttr(mirror_jnt + '.translateX' , cmds.getAttr(jnt + '.translateX') * -1)
    cmds.setAttr(mirror_jnt + '.jointOrientX' , cmds.getAttr(jnt + '.jointOrientX'))
    cmds.setAttr(mirror_jnt + '.jointOrientY' , cmds.getAttr(jnt + '.jointOrientY'))
    cmds.setAttr(mirror_jnt + '.jointOrientZ' , cmds.getAttr(jnt + '.jointOrientZ'))
    mirror_start_jnt = bpjnt_list_jnts[0].replace('_l_' , '_r_')
    cmds.setAttr(mirror_start_jnt + '.jointOrientX' , cmds.getAttr(bpjnt_list_jnts[0] + '.jointOrientX') * -1)
    cmds.setAttr(mirror_start_jnt + '.jointOrientY' , cmds.getAttr(bpjnt_list_jnts[0] + '.jointOrientY') * -1)
    cmds.setAttr(mirror_start_jnt + '.jointOrientZ' , cmds.getAttr(bpjnt_list_jnts[0] + '.jointOrientZ') * -1)
