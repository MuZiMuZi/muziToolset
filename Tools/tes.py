import maya.cmds as cmds
import maya.api.OpenMaya as api


def srfAndCrv_list (sortSrfAndCrv = None) :
    srfAndCrv = cmds.ls (sl = True , et = 'transform')
    transformList = []
    sortSrfAndCrv = []
    if len (srfAndCrv) == 2 :
        for transforms in srfAndCrv :
            relatives = cmds.listRelatives (transforms)
            if relatives and (cmds.objectType (relatives [0]) == 'nurbsCurve' or cmds.objectType (
                    relatives [0]) == 'nurbsSurface') :
                transformList.append (transforms)
        if cmds.objectType (cmds.listRelatives (transformList [0]) [0]) == 'nurbsSurface' and cmds.objectType (
                cmds.listRelatives (transformList [1]) [0]) == 'nurbsCurve' :
            sortSrfAndCrv.append (transformList [0])
            sortSrfAndCrv.append (transformList [1])
        elif cmds.objectType (cmds.listRelatives (transformList [0]) [0]) == 'nurbsCurve' and cmds.objectType (
                cmds.listRelatives (transformList [1]) [0]) == 'nurbsSurface' :
            sortSrfAndCrv.append (transformList [1])
            sortSrfAndCrv.append (transformList [0])
        return sortSrfAndCrv


if srfAndCrv_list () :
    def createAndConnect () :
        mSrfAndCrvSel_list = api.MSelectionList ()
        mSrfAndCrvSel_list.add (srfAndCrv_list () [0])
        mSrfAndCrvSel_list.add (srfAndCrv_list () [1])

        mfn_nurbsSurface = api.MFnNurbsSurface (mSrfAndCrvSel_list.getDagPath (0))
        mfn_nurbsCurve = api.MFnNurbsCurve (mSrfAndCrvSel_list.getDagPath (1))

        srfName = srfAndCrv_list () [0]
        crvName = srfAndCrv_list () [1]
        position_list = [[mPos [index] for index in range (3)] for mPos in
                         mfn_nurbsCurve.cvPositions (api.MSpace.kObject)]

        rootGrp = cmds.group (em = True , n = srfName.replace ('_srf' , 'Jnts_grp'))
        distanceCrvU = cmds.duplicateCurve (srfName + '.u[0]' , ch = False , rn = 0 , local = 0)
        distanceCrvV = cmds.duplicateCurve (srfName + '.v[0]' , ch = False , rn = 0 , local = 0)
        cmds.arclen (distanceCrvU) , cmds.arclen (distanceCrvV)

        for i , cvPoint in enumerate (position_list) :
            try :
                toleranse = mfn_nurbsSurface.distanceToPoint (api.MPoint (cvPoint) , api.MSpace.kWorld) + 0.01
                paramU , paramV = mfn_nurbsSurface.getParamAtPoint (api.MPoint (cvPoint) , False , toleranse ,
                                                                    api.MSpace.kWorld)
            except :
                try :
                    toleranse = mfn_nurbsSurface.distanceToPoint (api.MPoint (cvPoint) , api.MSpace.kWorld) + 0.02
                    paramU , paramV = mfn_nurbsSurface.getParamAtPoint (api.MPoint (cvPoint) , False , toleranse ,
                                                                        api.MSpace.kWorld)
                except :
                    try :
                        toleranse = mfn_nurbsSurface.distanceToPoint (api.MPoint (cvPoint) , api.MSpace.kWorld) + 0.03
                        paramU , paramV = mfn_nurbsSurface.getParamAtPoint (api.MPoint (cvPoint) , False , toleranse ,
                                                                            api.MSpace.kWorld)
                    except :
                        try :
                            toleranse = mfn_nurbsSurface.distanceToPoint (api.MPoint (cvPoint) ,
                                                                          api.MSpace.kWorld) + 0.04
                            paramU , paramV = mfn_nurbsSurface.getParamAtPoint (api.MPoint (cvPoint) , False ,
                                                                                toleranse , api.MSpace.kWorld)
                        except :
                            toleranse = mfn_nurbsSurface.distanceToPoint (api.MPoint (cvPoint) ,
                                                                          api.MSpace.kWorld) + 0.05
                            paramU , paramV = mfn_nurbsSurface.getParamAtPoint (api.MPoint (cvPoint) , False ,
                                                                                toleranse , api.MSpace.kWorld)

            psi = cmds.createNode ('pointOnSurfaceInfo' , n = srfName.replace ('_srf' , str (i + 1) + '_psi'))
            aim = cmds.createNode ('aimConstraint' , n = srfName.replace ('_srf' , str (i + 1) + '_aim'))
            cmds.select (cl = True)
            jnt = cmds.joint (n = srfName.replace ('_srf' , str (i + 1) + 'Skin_jnt'))
            grp = cmds.group (jnt , n = srfName.replace ('_srf' , str (i + 1) + 'Jnt_grp'))
            cmds.parent (aim , grp)

            cmds.connectAttr (cmds.listRelatives (srfName) [0] + '.worldSpace[0]' , psi + '.inputSurface')

            cmds.connectAttr (psi + '.normal' , aim + '.target[0].targetRotateTranslate')
            cmds.connectAttr (psi + '.tangentV' , aim + '.worldUpVector')

            cmds.connectAttr (psi + '.positionX' , grp + '.tx')
            cmds.connectAttr (psi + '.positionY' , grp + '.ty')
            cmds.connectAttr (psi + '.positionZ' , grp + '.tz')

            cmds.connectAttr (aim + '.constraintRotateX' , grp + '.rx')
            cmds.connectAttr (aim + '.constraintRotateY' , grp + '.ry')
            cmds.connectAttr (aim + '.constraintRotateZ' , grp + '.rz')

            cmds.setAttr (aim + '.aimVectorX' , 0)
            cmds.setAttr (aim + '.aimVectorY' , 1)
            cmds.setAttr (aim + '.aimVectorZ' , 0)

            cmds.setAttr (aim + '.upVectorX' , 0)
            cmds.setAttr (aim + '.upVectorY' , 0)
            cmds.setAttr (aim + '.upVectorZ' , 1)

            if cmds.arclen (distanceCrvU) > cmds.arclen (distanceCrvV) :
                cmds.setAttr (psi + '.parameterV' , paramV)
                cmds.setAttr (psi + '.parameterU' , mfn_nurbsSurface.knotDomainInU [1] / 2.0)
            elif cmds.arclen (distanceCrvU) < cmds.arclen (distanceCrvV) :
                cmds.setAttr (psi + '.parameterV' , mfn_nurbsSurface.knotDomainInV [1] / 2.0)
                cmds.setAttr (psi + '.parameterU' , paramU)
            cmds.parent (grp , rootGrp)
        cmds.delete (distanceCrvU , distanceCrvV)

createAndConnect ()
