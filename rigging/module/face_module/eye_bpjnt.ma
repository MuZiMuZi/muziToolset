//Maya ASCII 2023 scene
//Name: eye_bpjnt.ma
//Last modified: Mon, May 15, 2023 04:31:33 PM
//Codeset: 936
requires maya "2023";
requires "stereoCamera" "10.0";
requires "mtoa" "5.2.1.1";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2023";
fileInfo "version" "2023";
fileInfo "cutIdentifier" "202211021031-847a9f9623";
fileInfo "osv" "Windows 10 Pro for Workstations v2009 (Build: 19044)";
fileInfo "UUID" "1183894D-4355-96C8-DB29-9DB94CA6E6D6";
createNode joint -n "bpjnt_l_EyeBall_001";
	rename -uid "1E3BA125-4622-A297-BA67-4BAFC61C8A5A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	setAttr ".t" -type "double3" 0.56634339690208413 32.72411727905272 1.5263134241104126 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.996283595602279 -81.885365226278395 -0.0036791944032349283 ;
	setAttr ".pa" -type "double3" 9.7062825972397362e-20 0 0 ;
	setAttr ".bps" -type "matrix" 6.9374659078524914e-06 0 0.99999999997593592 0 -6.9348500582585756e-06 0.9999999999759539 4.8110265040239035e-11 0
		 -0.99999999995188982 -6.9348500584254572e-06 6.9374659076304468e-06 0 -3.6603161841630931 163.24769544601438 2.6889507770538303 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "EyeBall001";
	setAttr ".liw" yes;
	setAttr -l on -k on ".MeshPosInfo" -type "string" (
		"[u'mesh_r_high_eyeballInnerSpans_001.vtx[244]', u'mesh_r_high_eyeballInnerSpans_001.vtx[245]', u'mesh_r_high_eyeballInnerSpans_001.vtx[246]', u'mesh_r_high_eyeballInnerSpans_001.vtx[254]', u'mesh_r_high_eyeballInnerSpans_001.vtx[255]', u'mesh_r_high_eyeballInnerSpans_001.vtx[278]', u'mesh_r_high_eyeballInnerSpans_001.vtx[279]', u'mesh_r_high_eyeballInnerSpans_001.vtx[285]', u'mesh_r_high_eyeballInnerSpans_001.vtx[286]', u'mesh_r_high_eyeballInnerSpans_001.vtx[376]', u'mesh_r_high_eyeballInnerSpans_001.vtx[377]', u'mesh_r_high_eyeballInnerSpans_001.vtx[383]', u'mesh_r_high_eyeballInnerSpans_001.vtx[384]', u'mesh_r_high_eyeballInnerSpans_001.vtx[404]', u'mesh_r_high_eyeballInnerSpans_001.vtx[405]', u'mesh_r_high_eyeballInnerSpans_001.vtx[411]', u'mesh_r_high_eyeballInnerSpans_001.vtx[412]', u'mesh_r_high_eyeballInnerSpans_001.vtx[707]', u'mesh_r_high_eyeballInnerSpans_001.vtx[708]', u'mesh_r_high_eyeballInnerSpans_001.vtx[714]', u'mesh_r_high_eyeballInnerSpans_001.vtx[715]', u'mesh_r_high_eyeballInnerSpans_001.vtx[735]', u'mesh_r_high_eyeballInnerSpans_001.vtx[736]', u'mesh_r_high_eyeballInnerSpans_001.vtx[742]', u'mesh_r_high_eyeballInnerSpans_001.vtx[743]', u'mesh_r_high_eyeballInnerSpans_001.vtx[826]', u'mesh_r_high_eyeballInnerSpans_001.vtx[827]', u'mesh_r_high_eyeballInnerSpans_001.vtx[833]', u'mesh_r_high_eyeballInnerSpans_001.vtx[834]', u'mesh_r_high_eyeballInnerSpans_001.vtx[853]', u'mesh_r_high_eyeballInnerSpans_001.vtx[854]', u'mesh_r_high_eyeballInnerSpans_001.vtx[860]']");
createNode joint -n "bpjnt_l_Eye_002" -p "bpjnt_l_EyeBall_001";
	rename -uid "8A0EFB7C-47AD-A7B4-06AB-D48B69CED3F1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.42085884208364899 0 0 ;
	setAttr ".r" -type "double3" -1.0276926444028873e-41 2.4265706493099341e-20 -4.8531412986198681e-20 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 6.9374659073562461e-06 -2.3813023242238175e-16 0.99999999997593614 -1.0587908905616274e-22
		 -6.9348500582407354e-06 0.99999999997595346 4.8110254632803509e-11 -4.0793191187539693e-18
		 -0.99999999995189082 -6.9348500543259067e-06 6.9374659078899506e-06 1.2448055362706402e-23
		 -3.6603222555935986 163.24770688996708 4.6960461214089877 0.99999999999999967;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Eye002";
	setAttr ".radi" 0.492;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_EyeIris_001" -p "bpjnt_l_EyeBall_001";
	rename -uid "1998B6DA-4D91-BE41-3CB9-738E12F9AA00";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".s" -type "double3" 1.0000000000000002 1 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1.0631207227407435 7.3725828060650132e-06 3.0530094479137236e-06 -7.0351428106687753e-24
		 -7.3725828062425954e-06 1.0631207227451269 5.1147016832756174e-11 -9.2211023779387422e-19
		 -2.871742956706281e-06 -6.8025630780064348e-11 0.99999999999587663 6.4912091853874129e-29
		 -3.6603222555935977 163.24770688996711 4.6960461214089868 0.99999999999999989;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "EyeIris001";
	setAttr ".radi" 0.39999999999999991;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_EyeIris_002" -p "bpjnt_l_EyeIris_001";
	rename -uid "F25CE1C6-4CF3-DB68-DB9A-09B0D1E548AA";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1.6971228122233111 1.1769292233267426e-05 4.873700483074127e-06 -1.1230616707813355e-23
		 -1.1769292233550913e-05 1.6971228122303093 8.164902365957196e-11 -1.4720193920312444e-18
		 -2.871742956706281e-06 -6.8025630780064348e-11 0.99999999999587663 6.4912091853874129e-29
		 -3.6603208197221195 163.24770689000113 4.1960461214110483 0.99999999999999989;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "EyeIris002";
	setAttr ".radi" 0.5;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_l_EyeBall_001', u'jnt_l_EyeIris_001']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_EyeIris_003" -p "bpjnt_l_EyeIris_002";
	rename -uid "461654C0-429E-4356-DE5F-10AC312161E5";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".s" -type "double3" 1 1.0000000000000002 1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 2.2090020179126273 1.5319097772678002e-05 6.3436859868193677e-06 -1.4617949149751108e-23
		 -1.5319097773046993e-05 2.2090020179217356 1.0627566651367228e-10 -1.9160038295305596e-18
		 -2.871742956706281e-06 -6.8025630780064348e-11 0.99999999999587663 6.4912091853874129e-29
		 -3.6603177206918143 163.24770045276912 3.1960461214158244 0.99999999999999989;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "EyeIris004";
	setAttr ".radi" 0.5;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_l_EyeBall_001', u'jnt_l_EyeIris_001']";
	setAttr ".liw" yes;
createNode parentConstraint -n "bpjnt_l_EyeIris_003_parentConstraint1" -p "bpjnt_l_EyeIris_003";
	rename -uid "39F4D723-4E2E-0037-72E8-4C8B785B6D00";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_EyeBall_001W0" -dv 1 -min 
		0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "bpjnt_l_Eye_002W1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".tg[0].tot" -type "double3" 0.4208588420836501 -5.5511151231257827e-17 
		1.4210854715202004e-14 ;
	setAttr ".tg[0].tor" -type "double3" 6.2784797791767321e-14 -4.8603239477418219e-15 
		-4.7708320221952815e-15 ;
	setAttr ".tg[1].tot" -type "double3" 4.4408920985006262e-16 -5.5511151231257827e-17 
		1.4210854715202004e-14 ;
	setAttr ".rst" -type "double3" 0.21769839547404213 1.6653345369377348e-16 -2.8421709430404007e-14 ;
	setAttr ".rsrr" -type "double3" -3.4986101496098688e-14 3.1805546814635176e-15 -9.7105938557103516e-31 ;
	setAttr -k on ".w0" 0;
	setAttr -k on ".w1";
createNode parentConstraint -n "bpjnt_l_EyeIris_002_parentConstraint1" -p "bpjnt_l_EyeIris_002";
	rename -uid "2C7E8179-4E0D-6C5E-C5A0-0EB2400F5FC0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_EyeBall_001W0" -dv 1 -min 
		0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "bpjnt_l_Eye_002W1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".tg[0].tot" -type "double3" 0.20316044660960775 -2.7755575615628914e-16 
		4.2632564145606011e-14 ;
	setAttr ".tg[0].tor" -type "double3" 6.2784797791767321e-14 -4.8603239477418219e-15 
		-4.7708320221952815e-15 ;
	setAttr ".tg[1].tot" -type "double3" -0.21769839547404168 -5.5511151231257827e-17 
		4.2632564145606011e-14 ;
	setAttr ".lr" -type "double3" -1.5902773407317584e-14 0 0 ;
	setAttr ".rst" -type "double3" 0.20316044660960864 2.2204460492503131e-16 1.4210854715202004e-14 ;
	setAttr ".rsrr" -type "double3" -3.4986101496098688e-14 3.1805546814635176e-15 -9.7105938557103516e-31 ;
	setAttr -k on ".w0" 0.5;
	setAttr -k on ".w1" 0.5;
createNode parentConstraint -n "bpjnt_l_EyeIris_001_parentConstraint1" -p "bpjnt_l_EyeIris_001";
	rename -uid "C4D7B411-444C-A5C1-2063-B095133FEC3D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_EyeBall_001W0" -dv 1 -min 
		0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "bpjnt_l_Eye_002W1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".tg[0].tot" -type "double3" -4.4408920985006262e-16 -4.4408920985006262e-16 
		2.8421709430404007e-14 ;
	setAttr ".tg[0].tor" -type "double3" 6.2784797791767321e-14 -4.8603239477418219e-15 
		-4.7708320221952815e-15 ;
	setAttr ".tg[1].tot" -type "double3" -0.42085884208364988 -2.2204460492503131e-16 
		2.8421709430404007e-14 ;
	setAttr ".lr" -type "double3" -3.1805546814635168e-14 0 0 ;
	setAttr ".rst" -type "double3" -8.8817841970012523e-16 -3.8857805861880479e-16 2.8421709430404007e-14 ;
	setAttr ".rsrr" -type "double3" -3.4986101496098688e-14 3.1805546814635176e-15 -9.7105938557103516e-31 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1" 0;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av -k on ".unw";
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -k on ".hwi";
	setAttr -av ".ta";
	setAttr -av -k on ".tq";
	setAttr -av ".etmr";
	setAttr -av ".tmr";
	setAttr -av ".aoon";
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -k on ".hff";
	setAttr -av -k on ".hfd";
	setAttr -av -k on ".hfs";
	setAttr -av -k on ".hfe";
	setAttr -av ".hfc";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av -k on ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr -k on ".blen";
	setAttr -k on ".blat";
	setAttr -av ".msaa";
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 14 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 17 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".u";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :defaultTextureList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3 ".tx";
select -ne :standardSurface1;
	setAttr ".b" 0.80000001192092896;
	setAttr ".bc" -type "float3" 1 1 1 ;
	setAttr ".s" 0.20000000298023224;
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -s 12 ".dsm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -s 12 ".gn";
	setAttr -cb on ".ai_override";
	setAttr -k on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -k on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".ai_override";
	setAttr -k on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -k on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
lockNode -l 0 -lu 1;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -av -cb on ".ren" -type "string" "arnold";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -k on ".exrc";
	setAttr -k on ".expt";
	setAttr -av -cb on ".an";
	setAttr -cb on ".ar";
	setAttr -av -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -av -cb on ".me";
	setAttr -cb on ".se";
	setAttr -av -k on ".be";
	setAttr -av -cb on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -av -cb on ".pff";
	setAttr -av -cb on ".peie";
	setAttr -av -cb on ".ifp";
	setAttr -k on ".rv";
	setAttr -av -k on ".comp";
	setAttr -av -k on ".cth";
	setAttr -av -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -av -k on ".rd";
	setAttr -av -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -av -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -av -k on ".uf";
	setAttr -av -k on ".oi";
	setAttr -av -k on ".rut";
	setAttr -av -k on ".mot";
	setAttr -av -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -av -k on ".pram";
	setAttr -av -k on ".poam";
	setAttr -av -k on ".prlm";
	setAttr -av -k on ".polm";
	setAttr -av -cb on ".prm";
	setAttr -av -cb on ".pom";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -av -k on ".tlwd";
	setAttr -av -k on ".tlht";
	setAttr -av -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -av -k on ".ope";
	setAttr -av -k on ".oppf";
	setAttr -av -k on ".rcp";
	setAttr -av -k on ".icp";
	setAttr -av -k on ".ocp";
	setAttr -cb on ".hbl";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya-legacy/config.ocio";
	setAttr ".vtn" -type "string" "sRGB gamma (legacy)";
	setAttr ".vn" -type "string" "sRGB gamma";
	setAttr ".dn" -type "string" "legacy";
	setAttr ".wsn" -type "string" "scene-linear Rec 709/sRGB";
	setAttr ".ovt" no;
	setAttr ".povt" no;
	setAttr ".otn" -type "string" "sRGB gamma (legacy)";
	setAttr ".potn" -type "string" "sRGB gamma (legacy)";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -av -k off -cb on ".fbfm";
	setAttr -av -k off -cb on ".ehql";
	setAttr -av -k off -cb on ".eams";
	setAttr -av -k off -cb on ".eeaa";
	setAttr -av -k off -cb on ".engm";
	setAttr -av -k off -cb on ".mes";
	setAttr -av -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -av -k off -cb on ".mbs";
	setAttr -av -k off -cb on ".trm";
	setAttr -av -k off -cb on ".tshc";
	setAttr -av -k off -cb on ".enpt";
	setAttr -av -k off -cb on ".clmt";
	setAttr -av -k off -cb on ".tcov";
	setAttr -av -k off -cb on ".lith";
	setAttr -av -k off -cb on ".sobc";
	setAttr -av -k off -cb on ".cuth";
	setAttr -av -k off -cb on ".hgcd";
	setAttr -av -k off -cb on ".hgci";
	setAttr -av -k off -cb on ".mgcs";
	setAttr -av -k off -cb on ".twa";
	setAttr -av -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "bpjnt_l_EyeBall_001.s" "bpjnt_l_Eye_002.is";
connectAttr "bpjnt_l_EyeBall_001.s" "bpjnt_l_EyeIris_001.is";
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.ctx" "bpjnt_l_EyeIris_001.tx"
		;
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.cty" "bpjnt_l_EyeIris_001.ty"
		;
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.ctz" "bpjnt_l_EyeIris_001.tz"
		;
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.crx" "bpjnt_l_EyeIris_001.rx"
		;
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.cry" "bpjnt_l_EyeIris_001.ry"
		;
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.crz" "bpjnt_l_EyeIris_001.rz"
		;
connectAttr "bpjnt_l_EyeIris_001.s" "bpjnt_l_EyeIris_002.is";
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.ctx" "bpjnt_l_EyeIris_002.tx"
		;
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.cty" "bpjnt_l_EyeIris_002.ty"
		;
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.ctz" "bpjnt_l_EyeIris_002.tz"
		;
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.crx" "bpjnt_l_EyeIris_002.rx"
		;
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.cry" "bpjnt_l_EyeIris_002.ry"
		;
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.crz" "bpjnt_l_EyeIris_002.rz"
		;
connectAttr "bpjnt_l_EyeIris_002.s" "bpjnt_l_EyeIris_003.is";
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.ctx" "bpjnt_l_EyeIris_003.tx"
		;
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.cty" "bpjnt_l_EyeIris_003.ty"
		;
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.ctz" "bpjnt_l_EyeIris_003.tz"
		;
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.crx" "bpjnt_l_EyeIris_003.rx"
		;
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.cry" "bpjnt_l_EyeIris_003.ry"
		;
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.crz" "bpjnt_l_EyeIris_003.rz"
		;
connectAttr "bpjnt_l_EyeIris_003.ro" "bpjnt_l_EyeIris_003_parentConstraint1.cro"
		;
connectAttr "bpjnt_l_EyeIris_003.pim" "bpjnt_l_EyeIris_003_parentConstraint1.cpim"
		;
connectAttr "bpjnt_l_EyeIris_003.rp" "bpjnt_l_EyeIris_003_parentConstraint1.crp"
		;
connectAttr "bpjnt_l_EyeIris_003.rpt" "bpjnt_l_EyeIris_003_parentConstraint1.crt"
		;
connectAttr "bpjnt_l_EyeIris_003.jo" "bpjnt_l_EyeIris_003_parentConstraint1.cjo"
		;
connectAttr "bpjnt_l_EyeBall_001.t" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_EyeBall_001.rp" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_EyeBall_001.rpt" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_EyeBall_001.r" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tr"
		;
connectAttr "bpjnt_l_EyeBall_001.ro" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tro"
		;
connectAttr "bpjnt_l_EyeBall_001.s" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_EyeBall_001.pm" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_EyeBall_001.jo" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tjo"
		;
connectAttr "bpjnt_l_EyeBall_001.ssc" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tsc"
		;
connectAttr "bpjnt_l_EyeBall_001.is" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tis"
		;
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.w0" "bpjnt_l_EyeIris_003_parentConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_Eye_002.t" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tt"
		;
connectAttr "bpjnt_l_Eye_002.rp" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].trp"
		;
connectAttr "bpjnt_l_Eye_002.rpt" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].trt"
		;
connectAttr "bpjnt_l_Eye_002.r" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tr"
		;
connectAttr "bpjnt_l_Eye_002.ro" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tro"
		;
connectAttr "bpjnt_l_Eye_002.s" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].ts"
		;
connectAttr "bpjnt_l_Eye_002.pm" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tpm"
		;
connectAttr "bpjnt_l_Eye_002.jo" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tjo"
		;
connectAttr "bpjnt_l_Eye_002.ssc" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tsc"
		;
connectAttr "bpjnt_l_Eye_002.is" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tis"
		;
connectAttr "bpjnt_l_EyeIris_003_parentConstraint1.w1" "bpjnt_l_EyeIris_003_parentConstraint1.tg[1].tw"
		;
connectAttr "bpjnt_l_EyeIris_002.ro" "bpjnt_l_EyeIris_002_parentConstraint1.cro"
		;
connectAttr "bpjnt_l_EyeIris_002.pim" "bpjnt_l_EyeIris_002_parentConstraint1.cpim"
		;
connectAttr "bpjnt_l_EyeIris_002.rp" "bpjnt_l_EyeIris_002_parentConstraint1.crp"
		;
connectAttr "bpjnt_l_EyeIris_002.rpt" "bpjnt_l_EyeIris_002_parentConstraint1.crt"
		;
connectAttr "bpjnt_l_EyeIris_002.jo" "bpjnt_l_EyeIris_002_parentConstraint1.cjo"
		;
connectAttr "bpjnt_l_EyeBall_001.t" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_EyeBall_001.rp" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_EyeBall_001.rpt" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_EyeBall_001.r" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tr"
		;
connectAttr "bpjnt_l_EyeBall_001.ro" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tro"
		;
connectAttr "bpjnt_l_EyeBall_001.s" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_EyeBall_001.pm" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_EyeBall_001.jo" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tjo"
		;
connectAttr "bpjnt_l_EyeBall_001.ssc" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tsc"
		;
connectAttr "bpjnt_l_EyeBall_001.is" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tis"
		;
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.w0" "bpjnt_l_EyeIris_002_parentConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_Eye_002.t" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tt"
		;
connectAttr "bpjnt_l_Eye_002.rp" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].trp"
		;
connectAttr "bpjnt_l_Eye_002.rpt" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].trt"
		;
connectAttr "bpjnt_l_Eye_002.r" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tr"
		;
connectAttr "bpjnt_l_Eye_002.ro" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tro"
		;
connectAttr "bpjnt_l_Eye_002.s" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].ts"
		;
connectAttr "bpjnt_l_Eye_002.pm" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tpm"
		;
connectAttr "bpjnt_l_Eye_002.jo" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tjo"
		;
connectAttr "bpjnt_l_Eye_002.ssc" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tsc"
		;
connectAttr "bpjnt_l_Eye_002.is" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tis"
		;
connectAttr "bpjnt_l_EyeIris_002_parentConstraint1.w1" "bpjnt_l_EyeIris_002_parentConstraint1.tg[1].tw"
		;
connectAttr "bpjnt_l_EyeIris_001.ro" "bpjnt_l_EyeIris_001_parentConstraint1.cro"
		;
connectAttr "bpjnt_l_EyeIris_001.pim" "bpjnt_l_EyeIris_001_parentConstraint1.cpim"
		;
connectAttr "bpjnt_l_EyeIris_001.rp" "bpjnt_l_EyeIris_001_parentConstraint1.crp"
		;
connectAttr "bpjnt_l_EyeIris_001.rpt" "bpjnt_l_EyeIris_001_parentConstraint1.crt"
		;
connectAttr "bpjnt_l_EyeIris_001.jo" "bpjnt_l_EyeIris_001_parentConstraint1.cjo"
		;
connectAttr "bpjnt_l_EyeBall_001.t" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_EyeBall_001.rp" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_EyeBall_001.rpt" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_EyeBall_001.r" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tr"
		;
connectAttr "bpjnt_l_EyeBall_001.ro" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tro"
		;
connectAttr "bpjnt_l_EyeBall_001.s" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_EyeBall_001.pm" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_EyeBall_001.jo" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tjo"
		;
connectAttr "bpjnt_l_EyeBall_001.ssc" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tsc"
		;
connectAttr "bpjnt_l_EyeBall_001.is" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tis"
		;
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.w0" "bpjnt_l_EyeIris_001_parentConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_Eye_002.t" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tt"
		;
connectAttr "bpjnt_l_Eye_002.rp" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].trp"
		;
connectAttr "bpjnt_l_Eye_002.rpt" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].trt"
		;
connectAttr "bpjnt_l_Eye_002.r" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tr"
		;
connectAttr "bpjnt_l_Eye_002.ro" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tro"
		;
connectAttr "bpjnt_l_Eye_002.s" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].ts"
		;
connectAttr "bpjnt_l_Eye_002.pm" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tpm"
		;
connectAttr "bpjnt_l_Eye_002.jo" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tjo"
		;
connectAttr "bpjnt_l_Eye_002.ssc" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tsc"
		;
connectAttr "bpjnt_l_Eye_002.is" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tis"
		;
connectAttr "bpjnt_l_EyeIris_001_parentConstraint1.w1" "bpjnt_l_EyeIris_001_parentConstraint1.tg[1].tw"
		;
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
// End of eye_bpjnt.ma
