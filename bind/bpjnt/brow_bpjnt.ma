//Maya ASCII 2023 scene
//Name: brow_bpjnt.ma
//Last modified: Fri, Dec 15, 2023 06:09:32 PM
//Codeset: 936
requires maya "2023";
requires -nodeType "RedshiftOptions" -nodeType "RedshiftPostEffects" "redshift4maya" "3.5.21";
requires "stereoCamera" "10.0";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "5.3.1";
requires -nodeType "renderSetup" "renderSetup.py" "1.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2023";
fileInfo "version" "2023";
fileInfo "cutIdentifier" "202211021031-847a9f9623";
fileInfo "osv" "Windows 10 Pro for Workstations v2009 (Build: 19045)";
fileInfo "UUID" "52727B14-4890-E3D0-2C70-E8AA621F672E";
createNode transform -s -n "persp";
	rename -uid "21816E19-4339-3745-DD8A-6BA93050C019";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -0.30684830998705354 43.952282943303949 2.2671021686504509 ;
	setAttr ".r" -type "double3" -88.538352729625998 3.400000000003335 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "9A59D31E-4435-1635-02E7-618D68EE3C21";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 11.636369642462748;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0.5978190769252909 32.985572684176901 1.9894093564256654 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "58711CEC-4753-6FF4-E669-28893090C8F3";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "EA005451-40F0-7A72-3795-74AF1AE238B3";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "2DF4F7C2-4B2F-C5D1-313C-95950CAA4932";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "B3E737AC-4D03-CBAD-8C6A-458F12A068CD";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "2F89A064-45AB-4C95-5DF9-D7AE5FDE7F67";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "FA17F74A-442F-6B6B-A9E8-E6872EA8E966";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "brow_bpjnt";
	rename -uid "470F47C3-4A6C-CB7F-2A7E-C0902281B0C6";
createNode joint -n "bpjnt_m_Brow_001" -p "brow_bpjnt";
	rename -uid "69457E54-4053-F719-D593-CDBE9ED22BF0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.5361250049750197e-09 32.949718475341797 2.1906836032867432 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.19919462502002716 32.955272674560547 2.1782350540161133 1;
createNode transform -n "bpcrv_l_Brow_001" -p "brow_bpjnt";
	rename -uid "266188E3-4161-6363-7303-82A299D09B88";
	setAttr ".rp" -type "double3" 1.865357246485956 32.936007869370073 1.5625987400923762 ;
	setAttr ".sp" -type "double3" 1.865357246485956 32.936007869370073 1.5625987400923762 ;
createNode nurbsCurve -n "bpcrv_l_Brow_001Shape" -p "bpcrv_l_Brow_001";
	rename -uid "1A3A5D6C-4C0F-8158-628A-98A869C7F89F";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".tw" yes;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "bpcrv_l_Brow_001ShapeOrig" -p "bpcrv_l_Brow_001";
	rename -uid "3A6DCA1E-4C2E-298F-A680-AB8CBC912601";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 0.16666666666666666 0.33333333333333331 0.5 0.66666666666666663 0.83333333333333337
		 1
		7
		0.45870462059974676 32.965999603271484 2.1782350540161133
		0.98420426976780706 32.947425672488556 2.1557094197839155
		1.4966145113181377 32.940981181321256 2.0668588014075917
		1.943940305774237 32.971023516864847 1.7852681110243582
		2.3822327866236512 32.963415889282928 1.4997317279302989
		2.8277108430060789 32.925592050631145 1.2235583608166978
		3.2720098723721653 32.886545063687841 0.94696242616863935
		;
	setAttr ".dcv" yes;
createNode transform -n "bpcrv_r_Brow_001" -p "brow_bpjnt";
	rename -uid "B53B202E-4507-1579-1E1B-D6A576983402";
createNode nurbsCurve -n "bpcrv_r_Brow_001Shape" -p "bpcrv_r_Brow_001";
	rename -uid "366A3581-44C7-5B2A-25F2-688F71DE7BD7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".tw" yes;
createNode nurbsCurve -n "bpcrv_r_Brow_001ShapeOrig" -p "bpcrv_r_Brow_001";
	rename -uid "83A831A6-44E9-F565-4DF1-72B1890AE60A";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		3 4 0 no 3
		9 0 0 0 1 2 3 4 4 4
		7
		0.4587046205997467 32.965999603271484 2.1782350540161133
		0.71181148290634155 32.975833892822266 2.1611809730529785
		0.96491837501525879 32.985668182373047 2.1441271305084229
		1.2126044034957886 32.99871826171875 2.0713198184967041
		1.4602904319763184 33.011772155761719 1.9985125064849854
		1.7484109401702881 32.976154327392578 1.7685985565185547
		2.0365314483642578 32.940532684326172 1.5386847257614136
		;
createNode nurbsCurve -n "bpcrv_r_Brow_001ShapeOrig1" -p "bpcrv_r_Brow_001";
	rename -uid "3B9CC37A-4755-1327-1CDD-7897946BEC7D";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 0.16666666666666663 0.33333333333333326 0.5 0.66666666666666652 0.83333333333333337
		 1
		7
		-0.45870462059974665 32.965999603271484 2.1782350540161133
		-0.97663225098107243 32.953515971330852 2.1226571460551495
		-1.4927653847170683 32.944075391480851 2.0318140768482715
		-1.9508617673403514 32.953001261509158 1.7812082960057347
		-2.3876174866943876 32.956162935418689 1.4960053452714828
		-2.8301682592930142 32.924716933269593 1.2214542815874438
		-3.2720098495483394 32.886543273925774 0.94696241617202803
		;
createNode transform -n "bpjnt_l_BrowGrp_001" -p "brow_bpjnt";
	rename -uid "3C7EA4E6-44B3-B5A9-A44C-4490F9EA0DDC";
createNode joint -n "bpjnt_l_Brow_001" -p "bpjnt_l_BrowGrp_001";
	rename -uid "C01E7AC2-4EE3-7DC4-351E-0BA075CF29FC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.45870462457795524 32.965999254865842 2.1782350540161133 1;
	setAttr ".radi" 0.3;
createNode parentConstraint -n "bpjnt_l_BrowSkin_001_parentConstraint1" -p "bpjnt_l_Brow_001";
	rename -uid "67901F5E-4C14-FF95-B111-07B347F55A43";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_001W0" -dv 1 -min 0 
		-at "double";
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
	setAttr ".rst" -type "double3" 0.45870462457795524 32.965999254865842 2.1782350540161133 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "bpjnt_l_BrowSkin_001_scaleConstraint1" -p "bpjnt_l_Brow_001";
	rename -uid "894D93AD-4923-184D-A4D6-C58D48611DA1";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_001W0" -dv 1 -min 0 
		-at "double";
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
	setAttr -k on ".w0";
createNode joint -n "bpjnt_l_Brow_002" -p "bpjnt_l_BrowGrp_001";
	rename -uid "F977B176-498A-E0D5-A87B-FD9C59772255";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.98420429229736328 32.947425842285156 2.1557095050811768 1;
	setAttr ".radi" 0.3;
createNode pointConstraint -n "bpjnt_l_BrowSkin_002_pointConstraint1" -p "bpjnt_l_Brow_002";
	rename -uid "536D5696-452F-4617-4A7A-D8AD37982DAC";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_002W0" -dv 1 -min 0 
		-at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "bpjnt_l_Brow_001W1" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 3.6002150149982981e-09 -7.9787238860262732e-07 -2.6418431886554572e-09 ;
	setAttr ".rst" -type "double3" 0.71181150339682198 32.975832920747052 2.1611810896204249 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode joint -n "bpjnt_l_Brow_003" -p "bpjnt_l_BrowGrp_001";
	rename -uid "F52EAD38-4D64-6E79-2AF5-0FB1D86BFF24";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.4966144561767578 32.940982818603516 2.0668587684631348 1;
	setAttr ".radi" 0.3;
createNode parentConstraint -n "bpjnt_l_BrowSkin_003_parentConstraint1" -p "bpjnt_l_Brow_003";
	rename -uid "E6A8A262-4F9D-2F05-1558-74A49240A710";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_002W0" -dv 1 -min 0 
		-at "double";
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
	setAttr ".rst" -type "double3" 0.96491837501525879 32.985668182373047 2.1441271305084229 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "bpjnt_l_BrowSkin_003_scaleConstraint1" -p "bpjnt_l_Brow_003";
	rename -uid "A3A94BB1-4E95-AAD1-6D4E-5399E4074BEC";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_002W0" -dv 1 -min 0 
		-at "double";
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
	setAttr -k on ".w0";
createNode joint -n "bpjnt_l_Brow_004" -p "bpjnt_l_BrowGrp_001";
	rename -uid "81B67494-4606-77F0-C6AA-29AEBDC63B90";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".r" -type "double3" 0 3.180554681463516e-15 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.9394236560325653 32.952197435614664 1.7832952573972474 1;
	setAttr ".radi" 0.3;
createNode pointConstraint -n "bpjnt_l_BrowSkin_004_pointConstraint1" -p "bpjnt_l_Brow_004";
	rename -uid "9167473A-446E-8A65-955F-68B020A926FB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_002W0" -dv 1 -min 0 
		-at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "bpjnt_l_Brow_003W1" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -2.427291567741463e-08 -2.500298421637126e-06 -1.638357538524815e-08 ;
	setAttr ".rst" -type "double3" 1.2126044034957886 32.99871826171875 2.0713198184967041 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode joint -n "bpjnt_l_Brow_005" -p "bpjnt_l_BrowGrp_001";
	rename -uid "03FE812A-45EE-F924-CBFC-9FB14F5EE762";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3822329044342041 32.963417053222656 1.4997317790985107 1;
	setAttr ".radi" 0.3;
createNode parentConstraint -n "bpjnt_l_BrowSkin_005_parentConstraint1" -p "bpjnt_l_Brow_005";
	rename -uid "DB9D044E-4D9C-B1E1-D852-F9B88DFD84F3";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_003W0" -dv 1 -min 0 
		-at "double";
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
	setAttr ".tg[0].tot" -type "double3" 2.2204460492503131e-16 0 0 ;
	setAttr ".tg[0].tor" -type "double3" 0 9.5416640443905519e-15 0 ;
	setAttr ".rst" -type "double3" 1.4602904805221499 33.011773341661304 1.9985125392521357 ;
	setAttr ".rsrr" -type "double3" 0 -29.319538085954989 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "bpjnt_l_BrowSkin_005_scaleConstraint1" -p "bpjnt_l_Brow_005";
	rename -uid "1BC09C94-4501-AA78-C0AB-E1A50AB457F3";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_003W0" -dv 1 -min 0 
		-at "double";
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
	setAttr -k on ".w0";
createNode joint -n "bpjnt_l_Brow_006" -p "bpjnt_l_BrowGrp_001";
	rename -uid "40CA7C74-45A1-9411-7E82-E1BD13ACC254";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".r" -type "double3" 0 -1.2722218725854067e-14 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.8271214073035482 32.924981103725855 1.2233470938788651 1;
	setAttr ".radi" 0.3;
createNode pointConstraint -n "bpjnt_l_BrowSkin_006_pointConstraint1" -p "bpjnt_l_Brow_006";
	rename -uid "977FF6BE-4B34-DCD4-E8F7-109BA579320E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_004W0" -dv 1 -min 0 
		-at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "bpjnt_l_Brow_003W1" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 2.2204460492503131e-16 -2.8421709430404007e-14 -4.4408920985006262e-16 ;
	setAttr ".rst" -type "double3" 1.7484109691592284 32.97615305826433 1.7685986122181623 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode joint -n "bpjnt_l_Brow_007" -p "bpjnt_l_BrowGrp_001";
	rename -uid "57BF51CA-4427-EB7F-5047-54A5AED54A1E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.2720099101728919 32.886545154229097 0.9469624086592201 1;
	setAttr ".radi" 0.3;
createNode parentConstraint -n "bpjnt_l_BrowSkin_007_parentConstraint1" -p "bpjnt_l_Brow_007";
	rename -uid "E0D7782C-42FD-F04A-9132-D19F6FF0AA13";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_004W0" -dv 1 -min 0 
		-at "double";
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
	setAttr ".tg[0].tot" -type "double3" -2.1510571102112408e-16 -7.1054273576010019e-15 
		-4.4408920985006262e-16 ;
	setAttr ".tg[0].tor" -type "double3" 0 3.1805546814635168e-15 0 ;
	setAttr ".rst" -type "double3" 2.0365314577963063 32.940532774867407 1.5386846851841895 ;
	setAttr ".rsrr" -type "double3" 0 -52.060430143834296 0 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "bpjnt_l_BrowSkin_007_scaleConstraint1" -p "bpjnt_l_Brow_007";
	rename -uid "31B1DCC6-4AE6-04EC-DB53-CA9061DEEA97";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "bpjnt_l_Brow_004W0" -dv 1 -min 0 
		-at "double";
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
	setAttr -k on ".w0";
createNode transform -n "bpjnt_r_BrowGrp_001" -p "brow_bpjnt";
	rename -uid "612011FA-4A7E-AD66-DCF8-39AC5FA86026";
createNode joint -n "bpjnt_r_Brow_001" -p "bpjnt_r_BrowGrp_001";
	rename -uid "8D21E965-4676-5214-6AEB-869841BABB0E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.4587046205997467 32.965999603271484 2.1782350540161133 1;
	setAttr ".radi" 0.3;
createNode joint -n "bpjnt_r_Brow_002" -p "bpjnt_r_BrowGrp_001";
	rename -uid "99A2FF33-4835-644C-32BF-3ABF3940B20E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 0.98609894315350766 0 -0.16615918365090501 0 0 1 0 0
		 0.16615918365090501 0 0.98609894315350766 0 -0.71181148290634155 32.975833892822266 2.1611809730529785 1;
	setAttr ".radi" 0.3;
createNode joint -n "bpjnt_r_Brow_003" -p "bpjnt_r_BrowGrp_001";
	rename -uid "00D142DE-4F6C-F6D8-A484-E18446DEBDE7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 0.78522700503371967 0 -0.61920800266612741 0 0 1 0 0
		 0.61920800266612741 0 0.78522700503371967 0 -0.96491837501525879 32.985668182373047 2.1441271305084229 1;
	setAttr ".radi" 0.3;
createNode joint -n "bpjnt_r_Brow_004" -p "bpjnt_r_BrowGrp_001";
	rename -uid "6A3177FE-4E73-D6A1-0604-DF9635456D45";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 0.72713193342838289 0 -0.68649774317815626 0 0 1 0 0
		 0.68649774317815626 0 0.72713193342838289 0 -1.2126044034957886 32.99871826171875 2.0713198184967041 1;
	setAttr ".radi" 0.3;
createNode joint -n "bpjnt_r_Brow_005" -p "bpjnt_r_BrowGrp_001";
	rename -uid "77E94379-4FF6-1B21-8E7C-9FBECE4CDD06";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 0.52042738236415831 0 -0.85390593140321391 0 0 1 0 0
		 0.85390593140321391 0 0.52042738236415831 0 -1.4602904319763184 33.011772155761719 1.9985125064849854 1;
	setAttr ".radi" 0.3;
createNode joint -n "bpjnt_r_Brow_006" -p "bpjnt_r_BrowGrp_001";
	rename -uid "1E1FA5B0-4358-8E3A-A8A8-94AB0B0E28BF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7484109401702881 32.976154327392578 1.7685985565185547 1;
	setAttr ".radi" 0.3;
createNode joint -n "bpjnt_r_Brow_007" -p "bpjnt_r_BrowGrp_001";
	rename -uid "8E4642BE-47CD-085D-F53C-2E844BAD9D3C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".bps" -type "matrix" -0.24396810731694041 0 -0.96978325548144517 0 0 1 0 0
		 0.96978325548144517 0 -0.24396810731694041 0 -2.0365314483642578 32.940532684326172 1.5386847257614136 1;
	setAttr ".radi" 0.3;
createNode transform -n "bpjnt_r_BrowFollowGrp_001" -p "brow_bpjnt";
	rename -uid "4A65DFA5-46E9-FD4B-8E9E-F98DACACF2F7";
createNode joint -n "bpjnt_r_BrowFollow_001" -p "bpjnt_r_BrowFollowGrp_001";
	rename -uid "45327556-4612-1DAF-023A-F9922B1360A2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -1.2246467991473532e-16 0 0 1.2246467991473532e-16 -1 0
		 -0.45870499999999997 32.966000000000001 2.1782400000000002 1;
createNode joint -n "bpjnt_r_BrowFollow_002" -p "bpjnt_r_BrowFollowGrp_001";
	rename -uid "DDDB6E70-4D81-2C0F-D4B2-E9B2EABB48F9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.94478225137692962 -4.0131527522153002e-17 0.32769879078681408 0
		 3.081487911019578e-33 -1 -1.2246467991473535e-16 0 0.32769879078681408 1.1570245600399869e-16 -0.94478225137692995 0
		 -0.96491800000000005 32.985700000000001 2.1441300000000001 1;
createNode joint -n "bpjnt_r_BrowFollow_003" -p "bpjnt_r_BrowFollowGrp_001";
	rename -uid "F07BA4C1-43E5-11CC-1B86-2A8F2F678B5E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.87190234039259185 -5.9968480254051293e-17 0.48967980233814096 0
		 0 -1 -1.2246467991473532e-16 0 0.48967980233814096 1.0677724103308737e-16 -0.87190234039259185 0
		 -1.4602900000000001 33.011800000000001 1.99851 1;
createNode joint -n "bpjnt_r_BrowFollow_004" -p "bpjnt_r_BrowFollowGrp_001";
	rename -uid "82225608-48C5-00C7-B08D-038B27BF3AF4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.61483001418402605 -9.6582952384671316e-17 0.78865965641616931 0
		 -6.1629758220391547e-33 -1 -1.224646799147353e-16 0 0.78865965641616931 7.529496088901892e-17 -0.61483001418402594 0
		 -2.03653 32.9405 1.53868 1;
createNode transform -n "bpjnt_l_BrowFollowGrp_001" -p "brow_bpjnt";
	rename -uid "5502D028-48B5-28A4-3781-66BB32AF887C";
createNode joint -n "bpjnt_l_BrowFollow_001" -p "bpjnt_l_BrowFollowGrp_001";
	rename -uid "504C915F-47C0-A126-DCAA-72A7240977A7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 1.5712441947865683 32.965999254865842 2.1782350540161133 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.19919462502002716 32.955272674560547 2.1782350540161133 1;
createNode joint -n "bpjnt_l_BrowFollow_002" -p "bpjnt_l_BrowFollowGrp_001";
	rename -uid "509D887F-4C36-D540-4D85-8CBEFAEF7BBC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.8620511857054596 32.918172277334897 1.9386139747896665 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.94478225137692962 0 -0.32769879078681408 0 0 1 0 0
		 0.32769879078681408 0 0.94478225137692962 0 0.48069290145496241 33.022665506379518 2.1441271252247365 1;
createNode joint -n "bpjnt_l_BrowFollow_003" -p "bpjnt_l_BrowFollowGrp_001";
	rename -uid "E33426BE-44A1-078B-B101-97B770C703BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.8871204070741001 32.887958150111587 1.4616729080573978 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.87190234039259185 0 -0.48967980233814096 0 0 1 0 0
		 0.48967980233814096 0 0.87190234039259185 0 0.76909813658598547 33.017352660330893 2.0081801459216706 1;
createNode joint -n "bpjnt_l_BrowFollow_004" -p "bpjnt_l_BrowFollowGrp_001";
	rename -uid "C3DCF7AB-4FB7-3F65-FAFB-AB96116F1ABA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.7768974128127972 32.811086251118034 0.9089035376181076 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.61483001418402605 0 -0.78865965641616931 0 0 1 0 0
		 0.78865965641616931 0 0.61483001418402605 0 1.0180069049165605 32.932854891936728 1.7790202827492114 1;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "A73B003F-48AC-A103-E156-CDAA72AB9C0B";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode RedshiftOptions -s -n "redshiftOptions";
	rename -uid "9610CBF4-4FAC-99D0-CDAA-29858E6BAC68";
	setAttr ".version" 5;
	setAttr ".primaryGIEngine" 4;
	setAttr ".secondaryGIEngine" 2;
	setAttr ".numGIBounces" 4;
createNode RedshiftPostEffects -n "defaultRedshiftPostEffects";
	rename -uid "F6798EA3-4FB5-8FD4-8DFB-16A5BCE71AF0";
	setAttr ".v" 2;
	setAttr -s 2 ".cr[1]" -type "float2" 1 1;
	setAttr -s 2 ".cg[1]" -type "float2" 1 1;
	setAttr -s 2 ".cb[1]" -type "float2" 1 1;
	setAttr -s 2 ".cl[1]" -type "float2" 1 1;
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "0FD49595-4704-0FC8-B6A1-B0AF01BB60AB";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "45F42D1A-4D4F-E642-785B-C1B58B54227E";
createNode displayLayerManager -n "layerManager";
	rename -uid "ECB437B8-4A78-779F-C264-40AB6069B3BB";
createNode displayLayer -n "defaultLayer";
	rename -uid "DF55F378-4632-70DC-C972-808E743093BC";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "0CFDEFE9-4AC4-C254-742E-C595D4CC3142";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "64C5288B-45FD-D918-1848-25A5F53B9091";
	setAttr ".g" yes;
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "D09DCCF6-483F-0556-4197-CCBEF114D9E0";
	setAttr ".version" -type "string" "5.3.1";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "B3AE03BD-4E8E-18C4-190B-DD997776D39A";
	setAttr ".ai_translator" -type "string" "gaussian";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "4D58CF17-470C-8C6C-5366-0CAE194EDE25";
	setAttr ".ai_translator" -type "string" "exr";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "0AE70C6D-41BA-0028-A78C-4BAEB837C30F";
	setAttr ".output_mode" 0;
	setAttr ".ai_translator" -type "string" "maya";
createNode renderSetup -n "renderSetup";
	rename -uid "BCCA9D27-42F9-38D3-E567-BE9F54D4F66D";
createNode multiplyDivide -n "transjnt_l_Brow_001";
	rename -uid "019EAAAC-4AB8-7409-903E-4FB668A32255";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_Brow_001";
	rename -uid "38CADF0E-4D4D-BB48-EA23-59B49D0AA54B";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion1";
	rename -uid "E6F67509-41FD-5829-0056-CBB2B14959D9";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion2";
	rename -uid "E36A46FA-4EA8-9B53-3687-65B9E45397BA";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_Brow_002";
	rename -uid "7617D3B3-4623-54E6-91EE-B1BD5590AB16";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_Brow_002";
	rename -uid "C71C5CA9-44D2-9899-CC0D-368CC1EA0AB1";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion3";
	rename -uid "ECD63ED8-4AE0-832B-D842-D79E6ACA0C81";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion4";
	rename -uid "B2E4139F-4CC5-0DB1-8500-B981DA35FF3C";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_Brow_003";
	rename -uid "66B8B2CB-42F2-A1CC-3C3C-A7AB22AE4244";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_Brow_003";
	rename -uid "E43CA83B-41D9-9186-9AA7-4C8782356442";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion5";
	rename -uid "0829F702-4877-1D9A-691D-4FA94CF3429E";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion6";
	rename -uid "25490BA2-4AFA-6949-8142-1ABA1BD528C6";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_Brow_004";
	rename -uid "78F750AB-4AB2-47AF-95F6-24898BDB0805";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_Brow_004";
	rename -uid "4FA7A81E-4E2B-8915-647E-B7B1D8EA16C7";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion7";
	rename -uid "FCE271C7-413F-55F9-ABED-8EB908FF6C3C";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion8";
	rename -uid "8AE6B6D3-4857-8013-F0E7-DA863C67E644";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_BrowSkin_001";
	rename -uid "DD212CBC-44FE-B3C1-3B5C-2099263F29BD";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_BrowSkin_001";
	rename -uid "180385CC-4EEF-F8D1-23CD-EAB1CD1EFE56";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion9";
	rename -uid "C2C5BBE8-4ABD-6565-5A5D-518520D116B3";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion10";
	rename -uid "CCC667F2-4189-6322-0BDD-2BAF18BE53CB";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_BrowSkin_002";
	rename -uid "150AA63D-4A03-7E99-68AF-BBAFF8A0F805";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_BrowSkin_002";
	rename -uid "E3739DF9-4273-2235-F60F-979D6C929DFF";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion11";
	rename -uid "DCA8CC88-499B-98B1-788A-82B7AF9FE344";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion12";
	rename -uid "B4AEC8B1-4D15-37EC-4684-3BA46E441058";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_BrowSkin_003";
	rename -uid "C701DBBA-4827-D90F-4918-D5AA2C6027BA";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_BrowSkin_003";
	rename -uid "F5095767-4481-9111-010C-F7B62C8816F1";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion13";
	rename -uid "81942BBE-46AD-AB83-F49C-D2B1816EA5C9";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion14";
	rename -uid "EDB3DC32-4474-D188-0F80-D687CD58A664";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_BrowSkin_004";
	rename -uid "944635BE-4CDA-57D3-589D-A58AE71E9F31";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_BrowSkin_004";
	rename -uid "DC1DB030-41AD-AD34-DC4D-299D4EB7DC68";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion15";
	rename -uid "C52CC990-4986-4A21-2CF7-C6BC1C6FD589";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion16";
	rename -uid "D53A1A0A-4FC2-9873-A63B-FCA12CE09944";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_BrowSkin_005";
	rename -uid "447CCB7A-46CF-A46E-287B-BA8E060FF032";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_BrowSkin_005";
	rename -uid "8A69D154-4BBF-2335-A29B-0DBD5A0202A5";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion17";
	rename -uid "E1BE33EB-4383-CA3E-E59C-81AFFD3FB8F0";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion18";
	rename -uid "31168546-4F45-7583-CF02-13A65104AC37";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_BrowSkin_006";
	rename -uid "42772998-4FAD-D39E-F527-69AFAE5193C8";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_BrowSkin_006";
	rename -uid "A0915506-42B5-D49E-E48B-E3B6B357F0C8";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion19";
	rename -uid "C3063173-4C0C-CD0D-2941-E38D77D5FC82";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion20";
	rename -uid "F61461DA-4B77-15B3-F2AF-D188263A9FAF";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "transjnt_l_BrowSkin_007";
	rename -uid "688B201A-4ED1-8B86-2C3C-4E8112A6578A";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "rotatejnt_l_BrowSkin_007";
	rename -uid "0A663D57-4BAA-570A-0992-28BA7ACE268D";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion21";
	rename -uid "0BBC2CE9-4650-B667-9E0A-668CDFB6473F";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion22";
	rename -uid "B1285C32-43F0-2DF5-CE57-D2B0EB7A92E0";
	setAttr ".cf" 0.017453292519943295;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "2313971C-41B7-8329-F621-D68200ADD596";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 150 -ast 1 -aet 250 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "B41DEA3A-4FAD-58FA-0F0D-769FB876B4E7";
	setAttr ".tgi[0].tn" -type "string" "Œﬁ±ÍÃ‚_1";
	setAttr ".tgi[0].vl" -type "double2" -395.23807953274508 -307.24243730026893 ;
	setAttr ".tgi[0].vh" -type "double2" 542.857121285939 391.7662434654041 ;
	setAttr -s 61 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 1145.7142333984375;
	setAttr ".tgi[0].ni[0].y" -1110;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" -277.14285278320312;
	setAttr ".tgi[0].ni[1].y" 38.571430206298828;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" -90;
	setAttr ".tgi[0].ni[2].y" 144.28572082519531;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" -90;
	setAttr ".tgi[0].ni[3].y" 144.28572082519531;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 224.28572082519531;
	setAttr ".tgi[0].ni[4].y" -221.42857360839844;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 218.57142639160156;
	setAttr ".tgi[0].ni[5].y" 180;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 364.28570556640625;
	setAttr ".tgi[0].ni[6].y" 611.4285888671875;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" -58.571430206298828;
	setAttr ".tgi[0].ni[7].y" 210;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" -277.14285278320312;
	setAttr ".tgi[0].ni[8].y" -482.85714721679688;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 40;
	setAttr ".tgi[0].ni[9].y" 265.71429443359375;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" 1145.7142333984375;
	setAttr ".tgi[0].ni[10].y" 1264.2857666015625;
	setAttr ".tgi[0].ni[10].nvs" 18306;
	setAttr ".tgi[0].ni[11].x" -705.71429443359375;
	setAttr ".tgi[0].ni[11].y" -274.28570556640625;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" 167.14285278320312;
	setAttr ".tgi[0].ni[12].y" -152.85714721679688;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 761.4285888671875;
	setAttr ".tgi[0].ni[13].y" 1091.4285888671875;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" -398.57144165039062;
	setAttr ".tgi[0].ni[14].y" 107.14286041259766;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" -277.14285278320312;
	setAttr ".tgi[0].ni[15].y" -274.28570556640625;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" -277.14285278320312;
	setAttr ".tgi[0].ni[16].y" 142.85714721679688;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" -277.14285278320312;
	setAttr ".tgi[0].ni[17].y" -691.4285888671875;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" -584.28570556640625;
	setAttr ".tgi[0].ni[18].y" 15.714285850524902;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" -277.14285278320312;
	setAttr ".tgi[0].ni[19].y" -378.57144165039062;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" -277.14285278320312;
	setAttr ".tgi[0].ni[20].y" 247.14285278320312;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" -277.14285278320312;
	setAttr ".tgi[0].ni[21].y" 664.28570556640625;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" 761.4285888671875;
	setAttr ".tgi[0].ni[22].y" 531.4285888671875;
	setAttr ".tgi[0].ni[22].nvs" 18304;
	setAttr ".tgi[0].ni[23].x" 364.28570556640625;
	setAttr ".tgi[0].ni[23].y" 402.85714721679688;
	setAttr ".tgi[0].ni[23].nvs" 18304;
	setAttr ".tgi[0].ni[24].x" -277.14285278320312;
	setAttr ".tgi[0].ni[24].y" -65.714286804199219;
	setAttr ".tgi[0].ni[24].nvs" 18304;
	setAttr ".tgi[0].ni[25].x" -705.71429443359375;
	setAttr ".tgi[0].ni[25].y" 288.57144165039062;
	setAttr ".tgi[0].ni[25].nvs" 18304;
	setAttr ".tgi[0].ni[26].x" 40;
	setAttr ".tgi[0].ni[26].y" -284.28570556640625;
	setAttr ".tgi[0].ni[26].nvs" 18304;
	setAttr ".tgi[0].ni[27].x" 1145.7142333984375;
	setAttr ".tgi[0].ni[27].y" 574.28570556640625;
	setAttr ".tgi[0].ni[27].nvs" 18304;
	setAttr ".tgi[0].ni[28].x" 40;
	setAttr ".tgi[0].ni[28].y" -75.714286804199219;
	setAttr ".tgi[0].ni[28].nvs" 18304;
	setAttr ".tgi[0].ni[29].x" -1018.5714111328125;
	setAttr ".tgi[0].ni[29].y" -25.714284896850586;
	setAttr ".tgi[0].ni[29].nvs" 18304;
	setAttr ".tgi[0].ni[30].x" -705.71429443359375;
	setAttr ".tgi[0].ni[30].y" 392.85714721679688;
	setAttr ".tgi[0].ni[30].nvs" 18304;
	setAttr ".tgi[0].ni[31].x" -1325.7142333984375;
	setAttr ".tgi[0].ni[31].y" -187.14285278320312;
	setAttr ".tgi[0].ni[31].nvs" 18304;
	setAttr ".tgi[0].ni[32].x" 40;
	setAttr ".tgi[0].ni[32].y" 37.142856597900391;
	setAttr ".tgi[0].ni[32].nvs" 18304;
	setAttr ".tgi[0].ni[33].x" -77.142860412597656;
	setAttr ".tgi[0].ni[33].y" 11.428571701049805;
	setAttr ".tgi[0].ni[33].nvs" 18304;
	setAttr ".tgi[0].ni[34].x" 40;
	setAttr ".tgi[0].ni[34].y" 517.14288330078125;
	setAttr ".tgi[0].ni[34].nvs" 18304;
	setAttr ".tgi[0].ni[35].x" 761.4285888671875;
	setAttr ".tgi[0].ni[35].y" 750;
	setAttr ".tgi[0].ni[35].nvs" 18304;
	setAttr ".tgi[0].ni[36].x" 18.571428298950195;
	setAttr ".tgi[0].ni[36].y" -55.714286804199219;
	setAttr ".tgi[0].ni[36].nvs" 18304;
	setAttr ".tgi[0].ni[37].x" 761.4285888671875;
	setAttr ".tgi[0].ni[37].y" -58.571430206298828;
	setAttr ".tgi[0].ni[37].nvs" 18304;
	setAttr ".tgi[0].ni[38].x" 40;
	setAttr ".tgi[0].ni[38].y" 161.42857360839844;
	setAttr ".tgi[0].ni[38].nvs" 18304;
	setAttr ".tgi[0].ni[39].x" 40;
	setAttr ".tgi[0].ni[39].y" 392.85714721679688;
	setAttr ".tgi[0].ni[39].nvs" 18304;
	setAttr ".tgi[0].ni[40].x" -277.14285278320312;
	setAttr ".tgi[0].ni[40].y" 351.42855834960938;
	setAttr ".tgi[0].ni[40].nvs" 18304;
	setAttr ".tgi[0].ni[41].x" -584.28570556640625;
	setAttr ".tgi[0].ni[41].y" -367.14285278320312;
	setAttr ".tgi[0].ni[41].nvs" 18304;
	setAttr ".tgi[0].ni[42].x" -277.14285278320312;
	setAttr ".tgi[0].ni[42].y" -170;
	setAttr ".tgi[0].ni[42].nvs" 18304;
	setAttr ".tgi[0].ni[43].x" 297.14285278320312;
	setAttr ".tgi[0].ni[43].y" 44.285713195800781;
	setAttr ".tgi[0].ni[43].nvs" 18304;
	setAttr ".tgi[0].ni[44].x" -77.142860412597656;
	setAttr ".tgi[0].ni[44].y" 11.428571701049805;
	setAttr ".tgi[0].ni[44].nvs" 18304;
	setAttr ".tgi[0].ni[45].x" 761.4285888671875;
	setAttr ".tgi[0].ni[45].y" 274.28570556640625;
	setAttr ".tgi[0].ni[45].nvs" 18304;
	setAttr ".tgi[0].ni[46].x" -277.14285278320312;
	setAttr ".tgi[0].ni[46].y" 560;
	setAttr ".tgi[0].ni[46].nvs" 18304;
	setAttr ".tgi[0].ni[47].x" -398.57144165039062;
	setAttr ".tgi[0].ni[47].y" -205.71427917480469;
	setAttr ".tgi[0].ni[47].nvs" 18304;
	setAttr ".tgi[0].ni[48].x" 761.4285888671875;
	setAttr ".tgi[0].ni[48].y" 1195.7142333984375;
	setAttr ".tgi[0].ni[48].nvs" 18304;
	setAttr ".tgi[0].ni[49].x" 1145.7142333984375;
	setAttr ".tgi[0].ni[49].y" 274.28570556640625;
	setAttr ".tgi[0].ni[49].nvs" 18304;
	setAttr ".tgi[0].ni[50].x" -277.14285278320312;
	setAttr ".tgi[0].ni[50].y" 455.71429443359375;
	setAttr ".tgi[0].ni[50].nvs" 18304;
	setAttr ".tgi[0].ni[51].x" -705.71429443359375;
	setAttr ".tgi[0].ni[51].y" -378.57144165039062;
	setAttr ".tgi[0].ni[51].nvs" 18304;
	setAttr ".tgi[0].ni[52].x" 1145.7142333984375;
	setAttr ".tgi[0].ni[52].y" -995.71429443359375;
	setAttr ".tgi[0].ni[52].nvs" 18304;
	setAttr ".tgi[0].ni[53].x" 761.4285888671875;
	setAttr ".tgi[0].ni[53].y" -162.85714721679688;
	setAttr ".tgi[0].ni[53].nvs" 18304;
	setAttr ".tgi[0].ni[54].x" -705.71429443359375;
	setAttr ".tgi[0].ni[54].y" -170;
	setAttr ".tgi[0].ni[54].nvs" 18304;
	setAttr ".tgi[0].ni[55].x" 211.42857360839844;
	setAttr ".tgi[0].ni[55].y" -88.571426391601562;
	setAttr ".tgi[0].ni[55].nvs" 18304;
	setAttr ".tgi[0].ni[56].x" -277.14285278320312;
	setAttr ".tgi[0].ni[56].y" -587.14288330078125;
	setAttr ".tgi[0].ni[56].nvs" 18304;
	setAttr ".tgi[0].ni[57].x" 364.28570556640625;
	setAttr ".tgi[0].ni[57].y" 507.14285278320312;
	setAttr ".tgi[0].ni[57].nvs" 18304;
	setAttr ".tgi[0].ni[58].x" -398.57144165039062;
	setAttr ".tgi[0].ni[58].y" -310;
	setAttr ".tgi[0].ni[58].nvs" 18304;
	setAttr ".tgi[0].ni[59].x" 40;
	setAttr ".tgi[0].ni[59].y" -180;
	setAttr ".tgi[0].ni[59].nvs" 18304;
	setAttr ".tgi[0].ni[60].x" -705.71429443359375;
	setAttr ".tgi[0].ni[60].y" 184.28572082519531;
	setAttr ".tgi[0].ni[60].nvs" 18304;
createNode skinCluster -n "skinCluster3";
	rename -uid "7D05D957-4C9D-012E-3D24-AA9D54E052D3";
	setAttr -s 7 ".wl";
	setAttr ".wl[0:6].w"
		1 0 1
		1 1 1
		1 2 1
		5 1 1.2791726228477509e-07 2 1.8255166942330977e-06 3 0.99999601285992801 
		4 1.9147170118975568e-06 5 1.1898910353667868e-07
		1 4 1
		1 5 1
		1 6 1;
	setAttr -s 7 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.45870462457795524 -32.965999254865842 -2.1782350540161133 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.98420429229736328 -32.947425842285156 -2.1557095050811768 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4966144561767578 -32.940982818603516 -2.0668587684631348 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.9394236560325653 -32.952197435614664 -1.7832952573972474 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3822329044342041 -32.963417053222656 -1.4997317790985107 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.8271214073035482 -32.924981103725855 -1.2233470938788651 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2720099101728919 -32.886545154229097 -0.9469624086592201 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 7 ".ma";
	setAttr -s 7 ".dpf[0:6]"  4 4 4 4 4 4 4;
	setAttr -s 7 ".lw";
	setAttr -s 7 ".lw";
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 7 ".ifcl";
	setAttr -s 7 ".ifcl";
createNode dagPose -n "bindPose5";
	rename -uid "6639E01B-4704-A4A8-2144-56965E94F5AD";
	setAttr -s 9 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 9 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.45870462457795524 32.965999254865842
		 2.1782350540161133 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.98420429229736328 32.947425842285156
		 2.1557095050811768 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.4966144561767578 32.940982818603516
		 2.0668587684631348 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 5.5511151231257815e-17 0 0 1.9394236560325653
		 32.952197435614664 1.7832952573972474 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.3822329044342041 32.963417053222656
		 1.4997317790985107 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 -2.2204460492503131e-16 0 0 2.8271214073035482
		 32.924981103725855 1.2233470938788651 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.2720099101728919 32.886545154229097
		 0.9469624086592201 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 9 ".m";
	setAttr -s 9 ".p";
	setAttr -s 9 ".g[0:8]" yes yes no no no no no no no;
	setAttr ".bp" yes;
createNode skinCluster -n "skinCluster4";
	rename -uid "C5A12531-463B-4014-918E-91B1E889B18A";
	setAttr -s 7 ".wl";
	setAttr ".wl[0:6].w"
		1 6 1
		1 5 1
		5 2 1.3583682045374757e-06 3 2.2969918973032213e-05 4 0.99995340664601096 
		5 2.0947622857539581e-05 6 1.3174439540355913e-06
		5 1 1.5822941609079343e-08 2 2.6189771449058169e-07 3 0.99999948365829239 
		4 2.2231273306854492e-07 5 1.6308318427410454e-08
		5 0 7.6986451609658575e-09 1 1.2653410437896428e-07 2 0.99999974495879074 
		3 1.1353738619675284e-07 4 7.2710735485606227e-09
		4 0 2.2609365203189944e-09 1 0.99999999546284324 2 2.1403930502850341e-09 
		3 1.3582716485002277e-10
		1 0 1;
	setAttr -s 7 ".pm";
	setAttr ".pm[0]" -type "matrix" -0.24396810731694035 0 0.96978325548144495 0 0 1 0 0
		 -0.96978325548144495 0 -0.24396810731694035 0 0.12008224465718861 -32.886543273925774 3.4041689922361082 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.8271214962005615 -32.924980163574219 -1.2233470678329468 1;
	setAttr ".pm[2]" -type "matrix" 0.5204273823641582 0 0.85390593140321369 0 0 1 0 0
		 -0.85390593140321369 0 0.5204273823641582 0 2.5204090963225716 -32.963417053222649 1.2537013230356922 1;
	setAttr ".pm[3]" -type "matrix" 0.72713193342838289 0 0.68649774317815626 0 0 1 0 0
		 -0.68649774317815626 0 0.72713193342838289 0 2.6344450712681216 -32.952198028564453 0.034719039298039656 1;
	setAttr ".pm[4]" -type "matrix" 0.78522700503371967 0 0.61920800266612741 0 0 1 0 0
		 -0.61920800266612741 0 0.78522700503371967 0 2.4549975769268739 -32.940982818603516 -0.69623767241752688 1;
	setAttr ".pm[5]" -type "matrix" 0.98609894315350788 0 0.16615918365090504 0 0 1 0 0
		 -0.16615918365090504 0 0.98609894315350788 0 1.3167496849069085 -32.9534912109375 -1.930594157655988 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.4587046205997467 -32.965999603271484 -2.1782350540161133 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 7 ".ma";
	setAttr -s 7 ".dpf[0:6]"  4 4 4 4 4 4 4;
	setAttr -s 7 ".lw";
	setAttr -s 7 ".lw";
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 7 ".ifcl";
	setAttr -s 7 ".ifcl";
createNode dagPose -n "bindPose6";
	rename -uid "36C4A609-4F67-9E3A-7716-B5B8AEF08AB4";
	setAttr -s 9 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" -0.24396810731694041 0 -0.96978325548144517 0 0 1 0 0
		 0.96978325548144517 0 -0.24396810731694041 0 -3.2720098495483398 32.886543273925781 0.94696241617202759 1;
	setAttr ".wm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.8271214962005615 32.924980163574219 1.2233470678329468 1;
	setAttr ".wm[4]" -type "matrix" 0.52042738236415831 0 -0.85390593140321391 0 0 1 0 0
		 0.85390593140321391 0 0.52042738236415831 0 -2.3822329044342041 32.963417053222656 1.4997317790985107 1;
	setAttr ".wm[5]" -type "matrix" 0.72713193342838289 0 -0.68649774317815626 0 0 1 0 0
		 0.68649774317815626 0 0.72713193342838289 0 -1.939423680305481 32.952198028564453 1.7832952737808228 1;
	setAttr ".wm[6]" -type "matrix" 0.78522700503371967 0 -0.61920800266612741 0 0 1 0 0
		 0.61920800266612741 0 0.78522700503371967 0 -1.4966144561767578 32.940982818603516 2.0668587684631348 1;
	setAttr ".wm[7]" -type "matrix" 0.98609894315350766 0 -0.16615918365090501 0 0 1 0 0
		 0.16615918365090501 0 0.98609894315350766 0 -0.97765952348709106 32.9534912109375 2.122546911239624 1;
	setAttr ".wm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.4587046205997467 32.965999603271484 2.1782350540161133 1;
	setAttr -s 9 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.2720098495483398 32.886543273925781
		 0.94696241617202759 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.78865965641616931 0 0.61483001418402616 1
		 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 2.2204460492503131e-16 0 0 -2.8271214962005615
		 32.924980163574219 1.2233470678329468 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.3822329044342041 32.963417053222656
		 1.4997317790985107 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.48967980233814101 0 0.87190234039259196 1
		 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 -5.5511151231257827e-17 0 0 -1.939423680305481
		 32.952198028564453 1.7832952737808228 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.36936977852256475 0 0.92928250102656695 1
		 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.4966144561767578 32.940982818603516
		 2.0668587684631348 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.32769879078681408 0 0.94478225137692962 1
		 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.97765952348709106 32.9534912109375
		 2.122546911239624 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0.083369829214447522 0 0.99651867597991051 1
		 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.4587046205997467 32.965999603271484
		 2.1782350540161133 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 9 ".m";
	setAttr -s 9 ".p";
	setAttr -s 9 ".g[0:8]" yes yes no no no no no no no;
	setAttr ".bp" yes;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1.25;
	setAttr -av -k on ".unw" 1.25;
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
	setAttr -av ".ta" 5;
	setAttr -av -k on ".tq" 1;
	setAttr -av ".etmr";
	setAttr -av ".tmr";
	setAttr -av ".aoon";
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -av ".aosm";
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
	setAttr -av ".aasc";
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
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
	setAttr -s 5 ".s";
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
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
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
	setAttr -cb on ".rsMaterialId";
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
	setAttr -av -k on ".exrc";
	setAttr -av -k on ".expt";
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
	setAttr -av -cb on ".sosl";
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
	setAttr ".cfp" -type "string" "L:/Technology/yhkt_pipeline/YHKT/configs/OCIO_config/aces_1.2/config.ocio";
	setAttr ".vtn" -type "string" "sRGB (ACES)";
	setAttr ".vn" -type "string" "sRGB";
	setAttr ".dn" -type "string" "ACES";
	setAttr ".wsn" -type "string" "ACES - ACEScg";
	setAttr ".ovt" no;
	setAttr ".povt" no;
	setAttr ".otn" -type "string" "sRGB (ACES)";
	setAttr ".potn" -type "string" "sRGB (ACES)";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
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
	setAttr -av -k on ".hwcc";
	setAttr -av -k on ".hwdp";
	setAttr -av -k on ".hwql";
	setAttr -av -k on ".hwfr";
	setAttr -av -k on ".soll";
	setAttr -av -k on ".sosl";
	setAttr -av -k on ".bswa";
	setAttr -av -k on ".shml";
	setAttr -av -k on ".hwel";
connectAttr "skinCluster3.og[0]" "bpcrv_l_Brow_001Shape.cr";
connectAttr "skinCluster4.og[0]" "bpcrv_r_Brow_001Shape.cr";
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.ctx" "bpjnt_l_Brow_001.tx";
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.cty" "bpjnt_l_Brow_001.ty";
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.ctz" "bpjnt_l_Brow_001.tz";
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.crx" "bpjnt_l_Brow_001.rx";
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.cry" "bpjnt_l_Brow_001.ry";
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.crz" "bpjnt_l_Brow_001.rz";
connectAttr "bpjnt_l_BrowSkin_001_scaleConstraint1.csx" "bpjnt_l_Brow_001.sx";
connectAttr "bpjnt_l_BrowSkin_001_scaleConstraint1.csy" "bpjnt_l_Brow_001.sy";
connectAttr "bpjnt_l_BrowSkin_001_scaleConstraint1.csz" "bpjnt_l_Brow_001.sz";
connectAttr "bpjnt_l_Brow_001.ro" "bpjnt_l_BrowSkin_001_parentConstraint1.cro";
connectAttr "bpjnt_l_Brow_001.pim" "bpjnt_l_BrowSkin_001_parentConstraint1.cpim"
		;
connectAttr "bpjnt_l_Brow_001.rp" "bpjnt_l_BrowSkin_001_parentConstraint1.crp";
connectAttr "bpjnt_l_Brow_001.rpt" "bpjnt_l_BrowSkin_001_parentConstraint1.crt";
connectAttr "bpjnt_l_Brow_001.jo" "bpjnt_l_BrowSkin_001_parentConstraint1.cjo";
connectAttr "bpjnt_l_BrowFollow_001.t" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_BrowFollow_001.rp" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_BrowFollow_001.rpt" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_BrowFollow_001.r" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tr"
		;
connectAttr "bpjnt_l_BrowFollow_001.ro" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tro"
		;
connectAttr "bpjnt_l_BrowFollow_001.s" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_001.pm" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowFollow_001.jo" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tjo"
		;
connectAttr "bpjnt_l_BrowFollow_001.ssc" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tsc"
		;
connectAttr "bpjnt_l_BrowFollow_001.is" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tis"
		;
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.w0" "bpjnt_l_BrowSkin_001_parentConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_Brow_001.pim" "bpjnt_l_BrowSkin_001_scaleConstraint1.cpim";
connectAttr "bpjnt_l_BrowFollow_001.s" "bpjnt_l_BrowSkin_001_scaleConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_001.pm" "bpjnt_l_BrowSkin_001_scaleConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_001_scaleConstraint1.w0" "bpjnt_l_BrowSkin_001_scaleConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_BrowSkin_002_pointConstraint1.ctx" "bpjnt_l_Brow_002.tx";
connectAttr "bpjnt_l_BrowSkin_002_pointConstraint1.cty" "bpjnt_l_Brow_002.ty";
connectAttr "bpjnt_l_BrowSkin_002_pointConstraint1.ctz" "bpjnt_l_Brow_002.tz";
connectAttr "bpjnt_l_Brow_002.pim" "bpjnt_l_BrowSkin_002_pointConstraint1.cpim";
connectAttr "bpjnt_l_Brow_002.rp" "bpjnt_l_BrowSkin_002_pointConstraint1.crp";
connectAttr "bpjnt_l_Brow_002.rpt" "bpjnt_l_BrowSkin_002_pointConstraint1.crt";
connectAttr "bpjnt_l_BrowFollow_002.t" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_BrowFollow_002.rp" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_BrowFollow_002.rpt" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_BrowFollow_002.pm" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_002_pointConstraint1.w0" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_BrowFollow_001.t" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[1].tt"
		;
connectAttr "bpjnt_l_BrowFollow_001.rp" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[1].trp"
		;
connectAttr "bpjnt_l_BrowFollow_001.rpt" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[1].trt"
		;
connectAttr "bpjnt_l_BrowFollow_001.pm" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[1].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_002_pointConstraint1.w1" "bpjnt_l_BrowSkin_002_pointConstraint1.tg[1].tw"
		;
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.ctx" "bpjnt_l_Brow_003.tx";
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.cty" "bpjnt_l_Brow_003.ty";
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.ctz" "bpjnt_l_Brow_003.tz";
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.crx" "bpjnt_l_Brow_003.rx";
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.cry" "bpjnt_l_Brow_003.ry";
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.crz" "bpjnt_l_Brow_003.rz";
connectAttr "bpjnt_l_BrowSkin_003_scaleConstraint1.csx" "bpjnt_l_Brow_003.sx";
connectAttr "bpjnt_l_BrowSkin_003_scaleConstraint1.csy" "bpjnt_l_Brow_003.sy";
connectAttr "bpjnt_l_BrowSkin_003_scaleConstraint1.csz" "bpjnt_l_Brow_003.sz";
connectAttr "bpjnt_l_Brow_003.ro" "bpjnt_l_BrowSkin_003_parentConstraint1.cro";
connectAttr "bpjnt_l_Brow_003.pim" "bpjnt_l_BrowSkin_003_parentConstraint1.cpim"
		;
connectAttr "bpjnt_l_Brow_003.rp" "bpjnt_l_BrowSkin_003_parentConstraint1.crp";
connectAttr "bpjnt_l_Brow_003.rpt" "bpjnt_l_BrowSkin_003_parentConstraint1.crt";
connectAttr "bpjnt_l_Brow_003.jo" "bpjnt_l_BrowSkin_003_parentConstraint1.cjo";
connectAttr "bpjnt_l_BrowFollow_002.t" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_BrowFollow_002.rp" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_BrowFollow_002.rpt" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_BrowFollow_002.r" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tr"
		;
connectAttr "bpjnt_l_BrowFollow_002.ro" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tro"
		;
connectAttr "bpjnt_l_BrowFollow_002.s" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_002.pm" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowFollow_002.jo" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tjo"
		;
connectAttr "bpjnt_l_BrowFollow_002.ssc" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tsc"
		;
connectAttr "bpjnt_l_BrowFollow_002.is" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tis"
		;
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.w0" "bpjnt_l_BrowSkin_003_parentConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_Brow_003.pim" "bpjnt_l_BrowSkin_003_scaleConstraint1.cpim";
connectAttr "bpjnt_l_BrowFollow_002.s" "bpjnt_l_BrowSkin_003_scaleConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_002.pm" "bpjnt_l_BrowSkin_003_scaleConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_003_scaleConstraint1.w0" "bpjnt_l_BrowSkin_003_scaleConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_BrowSkin_004_pointConstraint1.ctx" "bpjnt_l_Brow_004.tx";
connectAttr "bpjnt_l_BrowSkin_004_pointConstraint1.cty" "bpjnt_l_Brow_004.ty";
connectAttr "bpjnt_l_BrowSkin_004_pointConstraint1.ctz" "bpjnt_l_Brow_004.tz";
connectAttr "bpjnt_l_Brow_004.pim" "bpjnt_l_BrowSkin_004_pointConstraint1.cpim";
connectAttr "bpjnt_l_Brow_004.rp" "bpjnt_l_BrowSkin_004_pointConstraint1.crp";
connectAttr "bpjnt_l_Brow_004.rpt" "bpjnt_l_BrowSkin_004_pointConstraint1.crt";
connectAttr "bpjnt_l_BrowFollow_002.t" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_BrowFollow_002.rp" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_BrowFollow_002.rpt" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_BrowFollow_002.pm" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_004_pointConstraint1.w0" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_BrowFollow_003.t" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[1].tt"
		;
connectAttr "bpjnt_l_BrowFollow_003.rp" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[1].trp"
		;
connectAttr "bpjnt_l_BrowFollow_003.rpt" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[1].trt"
		;
connectAttr "bpjnt_l_BrowFollow_003.pm" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[1].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_004_pointConstraint1.w1" "bpjnt_l_BrowSkin_004_pointConstraint1.tg[1].tw"
		;
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.ctx" "bpjnt_l_Brow_005.tx";
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.cty" "bpjnt_l_Brow_005.ty";
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.ctz" "bpjnt_l_Brow_005.tz";
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.crx" "bpjnt_l_Brow_005.rx";
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.cry" "bpjnt_l_Brow_005.ry";
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.crz" "bpjnt_l_Brow_005.rz";
connectAttr "bpjnt_l_BrowSkin_005_scaleConstraint1.csx" "bpjnt_l_Brow_005.sx";
connectAttr "bpjnt_l_BrowSkin_005_scaleConstraint1.csy" "bpjnt_l_Brow_005.sy";
connectAttr "bpjnt_l_BrowSkin_005_scaleConstraint1.csz" "bpjnt_l_Brow_005.sz";
connectAttr "bpjnt_l_Brow_005.ro" "bpjnt_l_BrowSkin_005_parentConstraint1.cro";
connectAttr "bpjnt_l_Brow_005.pim" "bpjnt_l_BrowSkin_005_parentConstraint1.cpim"
		;
connectAttr "bpjnt_l_Brow_005.rp" "bpjnt_l_BrowSkin_005_parentConstraint1.crp";
connectAttr "bpjnt_l_Brow_005.rpt" "bpjnt_l_BrowSkin_005_parentConstraint1.crt";
connectAttr "bpjnt_l_Brow_005.jo" "bpjnt_l_BrowSkin_005_parentConstraint1.cjo";
connectAttr "bpjnt_l_BrowFollow_003.t" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_BrowFollow_003.rp" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_BrowFollow_003.rpt" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_BrowFollow_003.r" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tr"
		;
connectAttr "bpjnt_l_BrowFollow_003.ro" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tro"
		;
connectAttr "bpjnt_l_BrowFollow_003.s" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_003.pm" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowFollow_003.jo" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tjo"
		;
connectAttr "bpjnt_l_BrowFollow_003.ssc" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tsc"
		;
connectAttr "bpjnt_l_BrowFollow_003.is" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tis"
		;
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.w0" "bpjnt_l_BrowSkin_005_parentConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_Brow_005.pim" "bpjnt_l_BrowSkin_005_scaleConstraint1.cpim";
connectAttr "bpjnt_l_BrowFollow_003.s" "bpjnt_l_BrowSkin_005_scaleConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_003.pm" "bpjnt_l_BrowSkin_005_scaleConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_005_scaleConstraint1.w0" "bpjnt_l_BrowSkin_005_scaleConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_BrowSkin_006_pointConstraint1.ctx" "bpjnt_l_Brow_006.tx";
connectAttr "bpjnt_l_BrowSkin_006_pointConstraint1.cty" "bpjnt_l_Brow_006.ty";
connectAttr "bpjnt_l_BrowSkin_006_pointConstraint1.ctz" "bpjnt_l_Brow_006.tz";
connectAttr "bpjnt_l_Brow_006.pim" "bpjnt_l_BrowSkin_006_pointConstraint1.cpim";
connectAttr "bpjnt_l_Brow_006.rp" "bpjnt_l_BrowSkin_006_pointConstraint1.crp";
connectAttr "bpjnt_l_Brow_006.rpt" "bpjnt_l_BrowSkin_006_pointConstraint1.crt";
connectAttr "bpjnt_l_BrowFollow_004.t" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_BrowFollow_004.rp" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_BrowFollow_004.rpt" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_BrowFollow_004.pm" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_006_pointConstraint1.w0" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_BrowFollow_003.t" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[1].tt"
		;
connectAttr "bpjnt_l_BrowFollow_003.rp" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[1].trp"
		;
connectAttr "bpjnt_l_BrowFollow_003.rpt" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[1].trt"
		;
connectAttr "bpjnt_l_BrowFollow_003.pm" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[1].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_006_pointConstraint1.w1" "bpjnt_l_BrowSkin_006_pointConstraint1.tg[1].tw"
		;
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.ctx" "bpjnt_l_Brow_007.tx";
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.cty" "bpjnt_l_Brow_007.ty";
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.ctz" "bpjnt_l_Brow_007.tz";
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.crx" "bpjnt_l_Brow_007.rx";
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.cry" "bpjnt_l_Brow_007.ry";
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.crz" "bpjnt_l_Brow_007.rz";
connectAttr "bpjnt_l_BrowSkin_007_scaleConstraint1.csx" "bpjnt_l_Brow_007.sx";
connectAttr "bpjnt_l_BrowSkin_007_scaleConstraint1.csy" "bpjnt_l_Brow_007.sy";
connectAttr "bpjnt_l_BrowSkin_007_scaleConstraint1.csz" "bpjnt_l_Brow_007.sz";
connectAttr "bpjnt_l_Brow_007.ro" "bpjnt_l_BrowSkin_007_parentConstraint1.cro";
connectAttr "bpjnt_l_Brow_007.pim" "bpjnt_l_BrowSkin_007_parentConstraint1.cpim"
		;
connectAttr "bpjnt_l_Brow_007.rp" "bpjnt_l_BrowSkin_007_parentConstraint1.crp";
connectAttr "bpjnt_l_Brow_007.rpt" "bpjnt_l_BrowSkin_007_parentConstraint1.crt";
connectAttr "bpjnt_l_Brow_007.jo" "bpjnt_l_BrowSkin_007_parentConstraint1.cjo";
connectAttr "bpjnt_l_BrowFollow_004.t" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tt"
		;
connectAttr "bpjnt_l_BrowFollow_004.rp" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].trp"
		;
connectAttr "bpjnt_l_BrowFollow_004.rpt" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].trt"
		;
connectAttr "bpjnt_l_BrowFollow_004.r" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tr"
		;
connectAttr "bpjnt_l_BrowFollow_004.ro" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tro"
		;
connectAttr "bpjnt_l_BrowFollow_004.s" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_004.pm" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowFollow_004.jo" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tjo"
		;
connectAttr "bpjnt_l_BrowFollow_004.ssc" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tsc"
		;
connectAttr "bpjnt_l_BrowFollow_004.is" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tis"
		;
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.w0" "bpjnt_l_BrowSkin_007_parentConstraint1.tg[0].tw"
		;
connectAttr "bpjnt_l_Brow_007.pim" "bpjnt_l_BrowSkin_007_scaleConstraint1.cpim";
connectAttr "bpjnt_l_BrowFollow_004.s" "bpjnt_l_BrowSkin_007_scaleConstraint1.tg[0].ts"
		;
connectAttr "bpjnt_l_BrowFollow_004.pm" "bpjnt_l_BrowSkin_007_scaleConstraint1.tg[0].tpm"
		;
connectAttr "bpjnt_l_BrowSkin_007_scaleConstraint1.w0" "bpjnt_l_BrowSkin_007_scaleConstraint1.tg[0].tw"
		;
connectAttr "transjnt_l_BrowSkin_001.o" "bpjnt_r_Brow_001.t";
connectAttr "unitConversion10.o" "bpjnt_r_Brow_001.r";
connectAttr "transjnt_l_BrowSkin_002.o" "bpjnt_r_Brow_002.t";
connectAttr "unitConversion12.o" "bpjnt_r_Brow_002.r";
connectAttr "transjnt_l_BrowSkin_003.o" "bpjnt_r_Brow_003.t";
connectAttr "unitConversion14.o" "bpjnt_r_Brow_003.r";
connectAttr "transjnt_l_BrowSkin_004.o" "bpjnt_r_Brow_004.t";
connectAttr "unitConversion16.o" "bpjnt_r_Brow_004.r";
connectAttr "transjnt_l_BrowSkin_005.o" "bpjnt_r_Brow_005.t";
connectAttr "unitConversion18.o" "bpjnt_r_Brow_005.r";
connectAttr "transjnt_l_BrowSkin_006.o" "bpjnt_r_Brow_006.t";
connectAttr "unitConversion20.o" "bpjnt_r_Brow_006.r";
connectAttr "transjnt_l_BrowSkin_007.o" "bpjnt_r_Brow_007.t";
connectAttr "unitConversion22.o" "bpjnt_r_Brow_007.r";
connectAttr "transjnt_l_Brow_001.o" "bpjnt_r_BrowFollow_001.t";
connectAttr "unitConversion2.o" "bpjnt_r_BrowFollow_001.r";
connectAttr "transjnt_l_Brow_002.o" "bpjnt_r_BrowFollow_002.t";
connectAttr "unitConversion4.o" "bpjnt_r_BrowFollow_002.r";
connectAttr "transjnt_l_Brow_003.o" "bpjnt_r_BrowFollow_003.t";
connectAttr "unitConversion6.o" "bpjnt_r_BrowFollow_003.r";
connectAttr "transjnt_l_Brow_004.o" "bpjnt_r_BrowFollow_004.t";
connectAttr "unitConversion8.o" "bpjnt_r_BrowFollow_004.r";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "defaultRedshiftPostEffects.msg" ":redshiftOptions.postEffects";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":defaultArnoldDisplayDriver.msg" ":defaultArnoldRenderOptions.drivers"
		 -na;
connectAttr ":defaultArnoldFilter.msg" ":defaultArnoldRenderOptions.filt";
connectAttr ":defaultArnoldDriver.msg" ":defaultArnoldRenderOptions.drvr";
connectAttr "bpjnt_l_BrowFollow_001.t" "transjnt_l_Brow_001.i1";
connectAttr "unitConversion1.o" "rotatejnt_l_Brow_001.i1";
connectAttr "bpjnt_l_BrowFollow_001.r" "unitConversion1.i";
connectAttr "rotatejnt_l_Brow_001.o" "unitConversion2.i";
connectAttr "bpjnt_l_BrowFollow_002.t" "transjnt_l_Brow_002.i1";
connectAttr "unitConversion3.o" "rotatejnt_l_Brow_002.i1";
connectAttr "bpjnt_l_BrowFollow_002.r" "unitConversion3.i";
connectAttr "rotatejnt_l_Brow_002.o" "unitConversion4.i";
connectAttr "bpjnt_l_BrowFollow_003.t" "transjnt_l_Brow_003.i1";
connectAttr "unitConversion5.o" "rotatejnt_l_Brow_003.i1";
connectAttr "bpjnt_l_BrowFollow_003.r" "unitConversion5.i";
connectAttr "rotatejnt_l_Brow_003.o" "unitConversion6.i";
connectAttr "bpjnt_l_BrowFollow_004.t" "transjnt_l_Brow_004.i1";
connectAttr "unitConversion7.o" "rotatejnt_l_Brow_004.i1";
connectAttr "bpjnt_l_BrowFollow_004.r" "unitConversion7.i";
connectAttr "rotatejnt_l_Brow_004.o" "unitConversion8.i";
connectAttr "bpjnt_l_Brow_001.t" "transjnt_l_BrowSkin_001.i1";
connectAttr "unitConversion9.o" "rotatejnt_l_BrowSkin_001.i1";
connectAttr "bpjnt_l_Brow_001.r" "unitConversion9.i";
connectAttr "rotatejnt_l_BrowSkin_001.o" "unitConversion10.i";
connectAttr "bpjnt_l_Brow_002.t" "transjnt_l_BrowSkin_002.i1";
connectAttr "unitConversion11.o" "rotatejnt_l_BrowSkin_002.i1";
connectAttr "bpjnt_l_Brow_002.r" "unitConversion11.i";
connectAttr "rotatejnt_l_BrowSkin_002.o" "unitConversion12.i";
connectAttr "bpjnt_l_Brow_003.t" "transjnt_l_BrowSkin_003.i1";
connectAttr "unitConversion13.o" "rotatejnt_l_BrowSkin_003.i1";
connectAttr "bpjnt_l_Brow_003.r" "unitConversion13.i";
connectAttr "rotatejnt_l_BrowSkin_003.o" "unitConversion14.i";
connectAttr "bpjnt_l_Brow_004.t" "transjnt_l_BrowSkin_004.i1";
connectAttr "unitConversion15.o" "rotatejnt_l_BrowSkin_004.i1";
connectAttr "bpjnt_l_Brow_004.r" "unitConversion15.i";
connectAttr "rotatejnt_l_BrowSkin_004.o" "unitConversion16.i";
connectAttr "bpjnt_l_Brow_005.t" "transjnt_l_BrowSkin_005.i1";
connectAttr "unitConversion17.o" "rotatejnt_l_BrowSkin_005.i1";
connectAttr "bpjnt_l_Brow_005.r" "unitConversion17.i";
connectAttr "rotatejnt_l_BrowSkin_005.o" "unitConversion18.i";
connectAttr "bpjnt_l_Brow_006.t" "transjnt_l_BrowSkin_006.i1";
connectAttr "unitConversion19.o" "rotatejnt_l_BrowSkin_006.i1";
connectAttr "bpjnt_l_Brow_006.r" "unitConversion19.i";
connectAttr "rotatejnt_l_BrowSkin_006.o" "unitConversion20.i";
connectAttr "bpjnt_l_Brow_007.t" "transjnt_l_BrowSkin_007.i1";
connectAttr "unitConversion21.o" "rotatejnt_l_BrowSkin_007.i1";
connectAttr "bpjnt_l_Brow_007.r" "unitConversion21.i";
connectAttr "rotatejnt_l_BrowSkin_007.o" "unitConversion22.i";
connectAttr "bpjnt_l_BrowSkin_001_scaleConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "transjnt_l_BrowSkin_004.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "bpjnt_l_BrowSkin_007_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "bpjnt_l_BrowSkin_005_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "bpjnt_l_BrowSkin_003_scaleConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "bpjnt_l_BrowSkin_006_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "bpjnt_l_BrowGrp_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "bpcrv_r_Brow_001ShapeOrig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "rotatejnt_l_BrowSkin_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "bpjnt_r_Brow_005.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "bpjnt_r_BrowFollow_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "transjnt_l_Brow_004.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "bpjnt_l_BrowSkin_004_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "rotatejnt_l_Brow_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "bpjnt_r_BrowFollow_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "rotatejnt_l_BrowSkin_003.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn"
		;
connectAttr "rotatejnt_l_BrowSkin_005.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "rotatejnt_l_BrowSkin_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn"
		;
connectAttr "bpjnt_l_Brow_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "transjnt_l_BrowSkin_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn"
		;
connectAttr "transjnt_l_BrowSkin_005.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "transjnt_l_BrowSkin_007.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "rotatejnt_l_BrowSkin_004.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn"
		;
connectAttr "rotatejnt_l_Brow_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn"
		;
connectAttr "bpjnt_r_BrowGrp_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn"
		;
connectAttr "bpjnt_r_Brow_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn"
		;
connectAttr "bpjnt_l_BrowSkin_002_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[29].dn"
		;
connectAttr "transjnt_l_Brow_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "bpjnt_l_BrowFollow_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn"
		;
connectAttr "bpjnt_r_Brow_003.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[32].dn"
		;
connectAttr "bpjnt_l_BrowSkin_007_scaleConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[33].dn"
		;
connectAttr "bpjnt_r_Brow_007.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[34].dn"
		;
connectAttr "bpcrv_r_Brow_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[36].dn"
		;
connectAttr "bpjnt_r_BrowFollowGrp_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[37].dn"
		;
connectAttr "bpjnt_r_Brow_004.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[38].dn"
		;
connectAttr "bpjnt_r_Brow_006.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[39].dn"
		;
connectAttr "rotatejnt_l_BrowSkin_006.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[40].dn"
		;
connectAttr "bpjnt_l_Brow_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[41].dn"
		;
connectAttr "transjnt_l_BrowSkin_003.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[42].dn"
		;
connectAttr "brow_bpjnt.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[43].dn";
connectAttr "bpjnt_l_BrowSkin_005_scaleConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[44].dn"
		;
connectAttr "rotatejnt_l_BrowSkin_007.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[46].dn"
		;
connectAttr "bpjnt_r_BrowFollow_003.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[47].dn"
		;
connectAttr "transjnt_l_Brow_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[48].dn"
		;
connectAttr "bpcrv_r_Brow_001Shape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[49].dn"
		;
connectAttr "transjnt_l_BrowSkin_006.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[50].dn"
		;
connectAttr "rotatejnt_l_Brow_004.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[51].dn"
		;
connectAttr "bpjnt_l_BrowSkin_001_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[52].dn"
		;
connectAttr "bpjnt_l_BrowFollowGrp_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[53].dn"
		;
connectAttr "rotatejnt_l_Brow_003.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[54].dn"
		;
connectAttr "bpjnt_l_BrowSkin_003_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[55].dn"
		;
connectAttr "transjnt_l_BrowSkin_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[56].dn"
		;
connectAttr "bpjnt_r_BrowFollow_004.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[58].dn"
		;
connectAttr "bpjnt_r_Brow_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[59].dn"
		;
connectAttr "transjnt_l_Brow_003.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[60].dn"
		;
connectAttr "bpcrv_l_Brow_001ShapeOrig.ws" "skinCluster3.ip[0].ig";
connectAttr "bpcrv_l_Brow_001ShapeOrig.l" "skinCluster3.orggeom[0]";
connectAttr "bindPose5.msg" "skinCluster3.bp";
connectAttr "bpjnt_l_Brow_001.wm" "skinCluster3.ma[0]";
connectAttr "bpjnt_l_Brow_002.wm" "skinCluster3.ma[1]";
connectAttr "bpjnt_l_Brow_003.wm" "skinCluster3.ma[2]";
connectAttr "bpjnt_l_Brow_004.wm" "skinCluster3.ma[3]";
connectAttr "bpjnt_l_Brow_005.wm" "skinCluster3.ma[4]";
connectAttr "bpjnt_l_Brow_006.wm" "skinCluster3.ma[5]";
connectAttr "bpjnt_l_Brow_007.wm" "skinCluster3.ma[6]";
connectAttr "bpjnt_l_Brow_001.liw" "skinCluster3.lw[0]";
connectAttr "bpjnt_l_Brow_002.liw" "skinCluster3.lw[1]";
connectAttr "bpjnt_l_Brow_003.liw" "skinCluster3.lw[2]";
connectAttr "bpjnt_l_Brow_004.liw" "skinCluster3.lw[3]";
connectAttr "bpjnt_l_Brow_005.liw" "skinCluster3.lw[4]";
connectAttr "bpjnt_l_Brow_006.liw" "skinCluster3.lw[5]";
connectAttr "bpjnt_l_Brow_007.liw" "skinCluster3.lw[6]";
connectAttr "bpjnt_l_Brow_001.obcc" "skinCluster3.ifcl[0]";
connectAttr "bpjnt_l_Brow_002.obcc" "skinCluster3.ifcl[1]";
connectAttr "bpjnt_l_Brow_003.obcc" "skinCluster3.ifcl[2]";
connectAttr "bpjnt_l_Brow_004.obcc" "skinCluster3.ifcl[3]";
connectAttr "bpjnt_l_Brow_005.obcc" "skinCluster3.ifcl[4]";
connectAttr "bpjnt_l_Brow_006.obcc" "skinCluster3.ifcl[5]";
connectAttr "bpjnt_l_Brow_007.obcc" "skinCluster3.ifcl[6]";
connectAttr "brow_bpjnt.msg" "bindPose5.m[0]";
connectAttr "bpjnt_l_BrowGrp_001.msg" "bindPose5.m[1]";
connectAttr "bpjnt_l_Brow_001.msg" "bindPose5.m[2]";
connectAttr "bpjnt_l_Brow_002.msg" "bindPose5.m[3]";
connectAttr "bpjnt_l_Brow_003.msg" "bindPose5.m[4]";
connectAttr "bpjnt_l_Brow_004.msg" "bindPose5.m[5]";
connectAttr "bpjnt_l_Brow_005.msg" "bindPose5.m[6]";
connectAttr "bpjnt_l_Brow_006.msg" "bindPose5.m[7]";
connectAttr "bpjnt_l_Brow_007.msg" "bindPose5.m[8]";
connectAttr "bindPose5.w" "bindPose5.p[0]";
connectAttr "bindPose5.m[0]" "bindPose5.p[1]";
connectAttr "bindPose5.m[1]" "bindPose5.p[2]";
connectAttr "bindPose5.m[1]" "bindPose5.p[3]";
connectAttr "bindPose5.m[1]" "bindPose5.p[4]";
connectAttr "bindPose5.m[1]" "bindPose5.p[5]";
connectAttr "bindPose5.m[1]" "bindPose5.p[6]";
connectAttr "bindPose5.m[1]" "bindPose5.p[7]";
connectAttr "bindPose5.m[1]" "bindPose5.p[8]";
connectAttr "bpjnt_l_Brow_001.bps" "bindPose5.wm[2]";
connectAttr "bpjnt_l_Brow_002.bps" "bindPose5.wm[3]";
connectAttr "bpjnt_l_Brow_003.bps" "bindPose5.wm[4]";
connectAttr "bpjnt_l_Brow_004.bps" "bindPose5.wm[5]";
connectAttr "bpjnt_l_Brow_005.bps" "bindPose5.wm[6]";
connectAttr "bpjnt_l_Brow_006.bps" "bindPose5.wm[7]";
connectAttr "bpjnt_l_Brow_007.bps" "bindPose5.wm[8]";
connectAttr "bpcrv_r_Brow_001ShapeOrig1.ws" "skinCluster4.ip[0].ig";
connectAttr "bpcrv_r_Brow_001ShapeOrig1.l" "skinCluster4.orggeom[0]";
connectAttr "bindPose6.msg" "skinCluster4.bp";
connectAttr "bpjnt_r_Brow_007.wm" "skinCluster4.ma[0]";
connectAttr "bpjnt_r_Brow_006.wm" "skinCluster4.ma[1]";
connectAttr "bpjnt_r_Brow_005.wm" "skinCluster4.ma[2]";
connectAttr "bpjnt_r_Brow_004.wm" "skinCluster4.ma[3]";
connectAttr "bpjnt_r_Brow_003.wm" "skinCluster4.ma[4]";
connectAttr "bpjnt_r_Brow_002.wm" "skinCluster4.ma[5]";
connectAttr "bpjnt_r_Brow_001.wm" "skinCluster4.ma[6]";
connectAttr "bpjnt_r_Brow_007.liw" "skinCluster4.lw[0]";
connectAttr "bpjnt_r_Brow_006.liw" "skinCluster4.lw[1]";
connectAttr "bpjnt_r_Brow_005.liw" "skinCluster4.lw[2]";
connectAttr "bpjnt_r_Brow_004.liw" "skinCluster4.lw[3]";
connectAttr "bpjnt_r_Brow_003.liw" "skinCluster4.lw[4]";
connectAttr "bpjnt_r_Brow_002.liw" "skinCluster4.lw[5]";
connectAttr "bpjnt_r_Brow_001.liw" "skinCluster4.lw[6]";
connectAttr "bpjnt_r_Brow_007.obcc" "skinCluster4.ifcl[0]";
connectAttr "bpjnt_r_Brow_006.obcc" "skinCluster4.ifcl[1]";
connectAttr "bpjnt_r_Brow_005.obcc" "skinCluster4.ifcl[2]";
connectAttr "bpjnt_r_Brow_004.obcc" "skinCluster4.ifcl[3]";
connectAttr "bpjnt_r_Brow_003.obcc" "skinCluster4.ifcl[4]";
connectAttr "bpjnt_r_Brow_002.obcc" "skinCluster4.ifcl[5]";
connectAttr "bpjnt_r_Brow_001.obcc" "skinCluster4.ifcl[6]";
connectAttr "brow_bpjnt.msg" "bindPose6.m[0]";
connectAttr "bpjnt_r_BrowGrp_001.msg" "bindPose6.m[1]";
connectAttr "bpjnt_r_Brow_007.msg" "bindPose6.m[2]";
connectAttr "bpjnt_r_Brow_006.msg" "bindPose6.m[3]";
connectAttr "bpjnt_r_Brow_005.msg" "bindPose6.m[4]";
connectAttr "bpjnt_r_Brow_004.msg" "bindPose6.m[5]";
connectAttr "bpjnt_r_Brow_003.msg" "bindPose6.m[6]";
connectAttr "bpjnt_r_Brow_002.msg" "bindPose6.m[7]";
connectAttr "bpjnt_r_Brow_001.msg" "bindPose6.m[8]";
connectAttr "bindPose6.w" "bindPose6.p[0]";
connectAttr "bindPose6.m[0]" "bindPose6.p[1]";
connectAttr "bindPose6.m[1]" "bindPose6.p[2]";
connectAttr "bindPose6.m[1]" "bindPose6.p[3]";
connectAttr "bindPose6.m[1]" "bindPose6.p[4]";
connectAttr "bindPose6.m[1]" "bindPose6.p[5]";
connectAttr "bindPose6.m[1]" "bindPose6.p[6]";
connectAttr "bindPose6.m[1]" "bindPose6.p[7]";
connectAttr "bindPose6.m[1]" "bindPose6.p[8]";
connectAttr "defaultRedshiftPostEffects.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
// End of brow_bpjnt.ma
