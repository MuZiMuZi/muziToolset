import  pymel.core as pm

shapeNode = pm.selected()[0].getShape()

if shapeNode:
    materislSG = shapeNode.outputs(type = 'shadingEngine')[0]
    for f in materislSG.history(type = 'file'):
        print(f.fileTextureName.get())