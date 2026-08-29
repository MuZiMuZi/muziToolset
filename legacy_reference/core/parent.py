parent_grp = 'world'
for sel in sell:
    ctrl = cmds.circle(n = 'test')
    cmds.parent(ctrl ,parent_grp)
    parent_grp  = ctrl