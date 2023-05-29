//Maya ASCII 2023 scene
//Name: face.ma
//Last modified: Mon, May 15, 2023 03:30:35 PM
//Codeset: 936
requires maya "2023";
requires "stereoCamera" "10.0";
requires "mtoa" "5.2.1.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2023";
fileInfo "version" "2023";
fileInfo "cutIdentifier" "202211021031-847a9f9623";
fileInfo "osv" "Windows 10 Pro for Workstations v2009 (Build: 19044)";
fileInfo "UUID" "5207350D-4C61-18D1-AD96-F2812BC123AF";
createNode transform -n "Face_Rig";
	rename -uid "5C2F48F4-4E04-F968-80C2-AFA0D481E4B6";
	setAttr ".t" -type "double3" 0 -127.56399361278946 1.4387255631020577 ;
	setAttr ".s" -type "double3" 0.25812079187722575 0.25812079187722575 0.25812079187722575 ;
	setAttr ".rp" -type "double3" -2.215473949192488e-07 160.45904252011707 -1.1533287494298223 ;
	setAttr ".sp" -type "double3" -2.215473949192488e-07 160.45904252011707 -1.1533287494298223 ;
createNode transform -n "Tougue_Rig" -p "Face_Rig";
	rename -uid "068C572A-4F3E-2E58-EDC0-2C88B8012AE4";
createNode transform -n "Tougue_Rig_Jnt" -p "Tougue_Rig";
	rename -uid "93B5F223-4D70-3320-A0E6-399BD4C0CAC8";
createNode joint -n "bpjnt_m_Tougue_001" -p "Tougue_Rig_Jnt";
	rename -uid "7D881972-4E35-C7B2-5834-9B81713B66BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.049113269631568569 155.14120020082348 0.4789029790489514 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0 154.48963928222656 -0.51328128576278687 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tougue001";
	setAttr ".radi" 2.0999999999999996;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeE_001" -p "bpjnt_m_Tougue_001";
	rename -uid "EF94C286-4DED-CF67-823D-63BE1BA026B6";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.64882954266869153 2.8421709430404001e-14 -1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.64882954266869275 154.48963928222656 -0.51328128576278687 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeE001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_001']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeE_002" -p "bpjnt_l_TougueSIdeE_001";
	rename -uid "0F4ABE0F-447B-2F52-8836-C6B0D209C49B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.64882954266869053 -1.4210854715202001e-14 4.4408920985006252e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7321894746634712e-17 0 0 0 1 0 1.2976590853373855 154.48963928222656 -0.51328128576278698 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeE002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeE_003" -p "bpjnt_l_TougueSIdeE_002";
	rename -uid "FE0A27C9-4273-799B-9CE8-848AF2F5E262";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.64882954266868997 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.8189256484623115e-17 0 0 0 1 0 1.9464886280060782 154.48963928222656 -0.51328128576278731 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeE003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeE_001" -p "bpjnt_m_Tougue_001";
	rename -uid "5C3EDCFE-42C1-6F21-D1B3-C1A3136334E5";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.64882999999999869 0.00036071777348922751 2.8576278587877368e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -9.5142785168100609e-17 0 0 1.2246467991473532e-16 -1 0
		 -0.64883000000000002 154.49000000000001 -0.51328099999999999 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeE001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_001']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeE_002" -p "bpjnt_r_TougueSIdeE_001";
	rename -uid "5F16E0CD-4695-9E32-DF3F-D0B54C2617D2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.6488299999999968 -9.9475983006414026e-14 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -9.5576466037094811e-17 0 0 1.2246467991473532e-16 -1 0
		 -1.29766 154.49000000000001 -0.51328099999999999 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeE002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeE_003" -p "bpjnt_r_TougueSIdeE_002";
	rename -uid "2D82D53D-4220-0129-7C19-3EBB28239A3D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.64882999999999802 2.8421709430404007e-14 -2.6645352591003757e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 -6.7981553672344566e-33 2.7437586863216651e-51 5.509304342552796e-52
		 1.125540632918032e-18 -1.0000000000000002 -9.5131265736858367e-17 -9.6296497219361793e-35
		 -2.0547185519838192e-34 1.2246467991473535e-16 -1 9.9246803936765924e-36 -1.9464900000000003 154.49000000000004 -0.51328099999999999 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeE003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_m_Tougue_002" -p "bpjnt_m_Tougue_001";
	rename -uid "94A24A28-4797-21BB-58C6-DFBECEA788B4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.9103390504542404e-16 0.20293551748903838 1.4766224473714797 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7321894746634712e-17 0 0 0 1 0 -3.0892743930417563e-23 154.91099616804553 0.96334116160869598 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tougue002";
	setAttr ".radi" 2.0999999999999996;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeD_001" -p "bpjnt_m_Tougue_002";
	rename -uid "662CBADD-4AB0-B43B-F39B-42AF83F90E85";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.68616062550560575 -1.7053025658242399e-13 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.68616062550560786 154.91099616804553 0.96334116160869598 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeD001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_002']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeD_002" -p "bpjnt_l_TougueSIdeD_001";
	rename -uid "A6E0B1B2-487B-D40A-751B-E78734648BB0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.6861606255056063 -5.6843418860808002e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 1.3723212510112157 154.91099616804553 0.96334116160869598 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeD002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeD_003" -p "bpjnt_l_TougueSIdeD_002";
	rename -uid "3788B179-4F54-1A47-5A74-BFBE90594AE2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.68616062550560331 -2.8421709430404001e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 2.058481876516824 154.91099616804553 0.96334116160869598 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeD003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeD_001" -p "bpjnt_m_Tougue_002";
	rename -uid "FF2BB234-4CFE-37D6-CC90-B7AF3CEAF3C1";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.68616099999999791 3.8319542596809697e-06 -1.6160869797943178e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -9.4709104299106407e-17 0 0 1.2246467991473532e-16 -1 0
		 -0.68616100000000002 154.91099999999997 0.963341 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeD001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_002']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeD_002" -p "bpjnt_r_TougueSIdeD_001";
	rename -uid "4EC46584-4420-CAA6-3D8C-FFBE1CC02FF2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.68615899999999741 -1.4210854715202004e-14 2.6645352591003757e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -9.5576466037094811e-17 0 0 1.2246467991473532e-16 -1 0
		 -1.37232 154.91099999999997 0.96334099999999989 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeD002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeD_003" -p "bpjnt_r_TougueSIdeD_002";
	rename -uid "444EBA27-4371-8E98-6F8E-5BBABB926A00";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.68615999999999455 0 1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 1.1102230246251565e-16 0 0 -1 -9.5576466037094811e-17 0
		 0 1.2246467991473532e-16 -1 0 -2.0584799999999999 154.91099999999997 0.96334099999999978 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeD003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_m_Tougue_003" -p "bpjnt_m_Tougue_002";
	rename -uid "D219E47F-49CF-0490-9197-3293B78A4C80";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.049152086805193937 0.029374560292893648 1.432720437084229 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 -1.3234889800848443e-23 155.00990295410156 2.5066187024116511 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tougue003";
	setAttr ".radi" 2.0999999999999996;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeC_001" -p "bpjnt_m_Tougue_003";
	rename -uid "6FE907DD-4161-95B1-F76D-6780AE45DE3B";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.66697811762161485 -7.1054273576010006e-14 -4.4408920985006254e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.66697811762161785 155.00990295410156 2.5066187024116511 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeC001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_003']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeC_002" -p "bpjnt_l_TougueSIdeC_001";
	rename -uid "C183E88D-4F32-6FBC-B3AA-43823FA15D56";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.66697811762161408 -4.2632564145605999e-14 8.8817841970012504e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 1.3339562352432357 155.00990295410156 2.5066187024116511 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeC002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeC_003" -p "bpjnt_l_TougueSIdeC_002";
	rename -uid "EE336857-4195-2033-A13A-669A6BC77BFA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.66697811762161574 -4.2632564145605999e-14 8.8817841970012504e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1.0000000000000002 1.7209556330455466e-14 -1.6579863011271772e-16 0
		 0 1 -2.7755575615628914e-17 0 0 0 1 0 2.0009343528648542 155.00990295410159 2.5066187024116515 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeC003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeC_001" -p "bpjnt_m_Tougue_003";
	rename -uid "DFA96D1D-407E-5BEE-995D-36ACDB845880";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.66697799999999707 9.7045898343139925e-05 1.2975883443289149e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -9.4709104299106407e-17 0 0 1.2246467991473532e-16 -1 0
		 -0.66697799999999996 155.00999999999999 2.5066199999999994 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeC001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_003']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeC_002" -p "bpjnt_r_TougueSIdeC_001";
	rename -uid "069CBC87-4630-A3F4-BB55-4997D3234F8E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.66698199999999719 1.7053025658242404e-13 -3.5527136788005009e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.1693345606653356e-50 -1 -9.4709104299106407e-17 0
		 0 1.2246467991473532e-16 -1 0 -1.33396 155.00999999999999 2.5066199999999994 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeC002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeC_003" -p "bpjnt_r_TougueSIdeC_002";
	rename -uid "CBA3B813-4E2C-4C34-B43F-FB8C7E745170";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.66696999999999051 1.2789769243681803e-13 -3.5527136788005009e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.99999999999999989 1.7209567104714547e-14 2.7829072379859053e-16 0
		 -2.3386691213306712e-50 -1 -9.4709104299106407e-17 0 0 1.2246467991473532e-16 -1 0
		 -2.0009299999999994 155.00999999999996 2.5066199999999985 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeC003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_m_Tougue_004" -p "bpjnt_m_Tougue_003";
	rename -uid "37BD3EF6-423A-4F21-92F6-B5A55E5C6958";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.1430879029786234e-16 0.23698348999027985 1.3560538923981174 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 -2.6469779601696886e-23 155.24688644409179 4.221682834625244 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tougue004";
	setAttr ".radi" 2.0999999999999996;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeB_001" -p "bpjnt_m_Tougue_004";
	rename -uid "AADCD0A5-4703-5E6F-6954-D29A61621222";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.58345282269788012 1.4210854715202001e-13 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.5834528226978839 155.24688644409181 4.221682834625244 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_004']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeB_002" -p "bpjnt_l_TougueSIdeB_001";
	rename -uid "D462CEE7-4563-38BB-9506-C49F1A881180";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.58345282269787979 1.4210854715202001e-14 -1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.7755575615628914e-17 0
		 0 0 1 0 1.1669056453957678 155.24688644409184 4.221682834625244 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeB_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_l_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002";
	rename -uid "5678C44B-429C-B521-425B-3383B18B6508";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.58345282269787935 2.8421709430404001e-14 -1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.99999999999999989 -1.7235866783159786e-14 -2.4611738716511772e-17 0
		 1.4476757067054944e-19 0.99999999999999978 -2.4093849454952548e-17 8.6736173798840355e-19
		 0 0 1 0 1.7503584680936517 155.24688644409187 4.2216828346252449 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeB_001" -p "bpjnt_m_Tougue_004";
	rename -uid "B0926A92-482D-C4D9-0F58-F18E97ADCFBD";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.58345299999999645 0.00011355590841333196 -2.8346252403110839e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -9.4709104299106407e-17 0 0 1.2246467991473532e-16 -1 0
		 -0.583453 155.24700000000001 4.2216800000000001 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_004']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeB_002" -p "bpjnt_r_TougueSIdeB_001";
	rename -uid "4182684F-4D3A-5CE2-2A95-F1AFA3DD99EA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.5834569999999949 -2.8421709430404007e-14 2.6645352591003757e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -9.1239657347152793e-17 0 0 1.2246467991473532e-16 -1 0
		 -1.1669099999999999 155.24700000000001 4.2216800000000001 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeB_003" -p "bpjnt_r_TougueSIdeB_002";
	rename -uid "C89A51F9-425D-B240-9E4F-10B2A8776E6F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.58344999999999536 -1.8474111129762605e-13 -8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 -5.4385242937875642e-32 0 0 0 -1 -9.4709104299106407e-17 0
		 0 1.2246467991473535e-16 -1 0 -1.7503599999999999 155.24700000000001 4.2216800000000019 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_m_Tougue_005" -p "bpjnt_m_Tougue_004";
	rename -uid "A834ED07-482B-7B1C-8FAB-549DE244B42C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.0657581468206416e-20 0.08296279907237647 1.309941840171807 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 -1.3234889800848443e-23 155.32984924316406 5.5316246747970581 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tougue005";
	setAttr ".radi" 2.0999999999999996;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_001" -p "bpjnt_m_Tougue_005";
	rename -uid "7D170D15-4C62-C407-3BE5-94959FE7CEE3";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147013 -1.4210854715202001e-13 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.44585654544147468 155.32984924316406 5.531624674797059 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_002" -p "bpjnt_l_TougueSIdeA_001";
	rename -uid "B21F089D-4EF3-0F71-30CF-339EE2E55664";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147008 -7.1054273576010006e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002";
	rename -uid "7AE103FA-49A3-2CAD-6171-B7B86F924B82";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544146902 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002";
	rename -uid "F868DA57-49F6-5410-6FAD-908F68F4F3EB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544146947 -1.4210854715202001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_003" -p "bpjnt_l_TougueSIdeA_001";
	rename -uid "5766A5C9-496C-E492-8813-C5AE4C209C13";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147041 -5.6843418860808002e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003";
	rename -uid "713F022B-4805-C908-9F38-CC961E3BA76C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 1.4210854715202001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002" -p "bpjnt_l_TougueSIdeA_001";
	rename -uid "E9732DBB-4A3C-ECD1-24E2-04B57204ED05";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147041 -5.6843418860808002e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "018DB0A7-4F25-BFFC-EDAF-ECA8E889199B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 1.4210854715202001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "F037122F-40A3-C65F-1384-42BC316AD209";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004" -p "bpjnt_l_TougueSIdeA_001";
	rename -uid "B91FD93B-4490-8AB6-7711-64A12902731F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147041 -5.6843418860808002e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "6B1CCB6B-4D9F-7094-1017-18A736A22299";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 1.4210854715202001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "FE1633E0-4F7D-590D-6FD7-8095D8680729";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006" -p "bpjnt_l_TougueSIdeA_001";
	rename -uid "7330CFE2-494C-17DD-64F0-79B35D521FA0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147041 -5.6843418860808002e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006";
	rename -uid "B5CAF0A6-4F09-DB4C-5474-C98CE08EFC85";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 1.4210854715202001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006";
	rename -uid "256AF454-4351-229A-B380-C6B4F4BB93BF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008" -p "bpjnt_l_TougueSIdeA_001";
	rename -uid "C8E10E89-43A1-4620-E2F6-EEBE58C19DFD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147041 -5.6843418860808002e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008";
	rename -uid "82732F47-48D7-61D1-2840-F58DC29059F9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 1.4210854715202001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008";
	rename -uid "884A6BC1-4026-8C57-8F55-349E54480618";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147058 4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeA_001" -p "bpjnt_m_Tougue_005";
	rename -uid "35FA3ACF-43E0-A6E0-8C2A-38BDA78E8308";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.44585699999999584 0.000150756835807897 -4.6747970579019693e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -1 -1.0164799820301364e-16 0 0 1.2246467991473532e-16 -1 0
		 -0.445857 155.33000000000001 5.5316200000000002 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeA_002" -p "bpjnt_r_TougueSIdeA_001";
	rename -uid "C957C82F-47B5-0FA4-F7F1-7A9A9B1C10A6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585599999999564 -1.4210854715202004e-14 -3.5527136788005009e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 -4.696156657990613e-20 -1 -9.9507019836197811e-17 -9.6296497219361793e-35
		 5.3735197055483061e-37 1.2246467991473532e-16 -1 9.9246803936765924e-36 -0.89171299999999998 155.33000000000001 5.5316199999999993 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_r_TougueSIdeA_003" -p "bpjnt_r_TougueSIdeA_002";
	rename -uid "7DE73032-4E3E-79F9-7739-7B8C77F28AD8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585699999999273 4.2632564145606011e-14 -1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 -9.3924000521550178e-20 -1 -9.2568125932290583e-17 -9.6296497219361793e-35
		 -8.8499665278865368e-36 1.2246467991473532e-16 -1 9.9246803936765924e-36 -1.3375699999999999 155.33000000000001 5.5316199999999993 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode transform -n "bpctrl_m_Tougue_005" -p "bpjnt_m_Tougue_005";
	rename -uid "3DB62218-468D-567C-75DD-2F912E33A894";
	addAttr -ci true -sn "Rolling" -ln "Rolling" -min 0 -max 1 -at "double";
	addAttr -ci true -sn "Squeeze" -ln "Squeeze" -min 0 -max 1 -at "double";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 2.0328790734103214e-20 -9.9475983006414051e-14 3.5527136788005017e-15 ;
	setAttr ".sp" -type "double3" 2.0328790734103214e-20 -9.9475983006414051e-14 3.5527136788005017e-15 ;
	setAttr -k on ".Rolling";
	setAttr -k on ".Squeeze";
createNode nurbsCurve -n "bpctrl_m_Tougue_005Shape" -p "bpctrl_m_Tougue_005";
	rename -uid "F89C1124-47E4-0B49-C4FF-64BC3FD8CE5A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.35540002905077711 0.85801157020205132 -2.6645352591003741e-15
		3.0281124875829981e-16 0.92870503134739035 -2.6645352591003741e-15
		-0.35540002905077733 0.85801157020205132 -2.6645352591003741e-15
		-0.65669362538785903 0.65669362538784459 -2.6645352591003741e-15
		-0.85801157020217866 0.35540002905059931 -2.6645352591003741e-15
		-0.92870503134746707 -1.5265566588595893e-16 -2.6645352591003741e-15
		-0.85801157020217811 -0.3554000290506848 -2.6645352591003741e-15
		-0.65669362538785903 -0.6566936253879303 -2.6645352591003741e-15
		-0.35540002905077728 -0.8580115702022223 -2.6645352591003741e-15
		1.5285931203997661e-16 -0.92870503134741922 -2.6645352591003741e-15
		0.35540002905077767 -0.8580115702022223 -2.6645352591003741e-15
		0.65669362538785903 -0.6566936253879303 -2.6645352591003741e-15
		0.85801157020217944 -0.3554000290506848 -2.6645352591003741e-15
		0.92870503134746707 -1.5265566588595893e-16 -2.6645352591003741e-15
		0.85801157020217889 0.35540002905059931 -2.6645352591003741e-15
		0.65669362538785858 0.65669362538784459 -2.6645352591003741e-15
		0.35540002905077711 0.85801157020205132 -2.6645352591003741e-15
		;
createNode joint -n "jntl_TougueSIdeA_001" -p "bpjnt_m_Tougue_005";
	rename -uid "F9E13797-441D-2005-F88C-4186166007FE";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147035 -9.9475983006414001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.44585654544147468 155.32984924316406 5.531624674797059 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_002" -p "jntl_TougueSIdeA_001";
	rename -uid "7304C9BC-4333-A5EA-14D3-B5B294DE4950";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147052 -7.1054273576010006e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002";
	rename -uid "3DAA6A7E-4FAC-9034-FAA3-C4B34893AB34";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147024 -4.2632564145605999e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002";
	rename -uid "2768673F-4EFD-BC1A-524F-779F403F33FE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147069 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002" -p "jntl_TougueSIdeA_001";
	rename -uid "13AEDDDD-4D16-FDE3-B50A-8DA14878C7C6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002";
	rename -uid "E1522A9B-4F57-52DC-D70A-DAB7F1FBE8D7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002" -p "jntl_TougueSIdeA_001";
	rename -uid "B8C1D451-4295-887B-EC4A-02AFF0CC6908";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "D066AAB4-478C-888D-8105-A6A74E5F1859";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003" 
		-p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "E7A6D187-4490-B9BF-D65D-8E881AA75D98";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_001";
	rename -uid "B48BBF33-4510-7C4E-3639-599F7E4BFF01";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003";
	rename -uid "7C0CCDE9-4152-D265-43C8-5FA0B1A8BAE7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003" 
		-p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003";
	rename -uid "70BFD472-4319-E9DE-7B0D-23BB3DE6CB27";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004" -p "jntl_TougueSIdeA_001";
	rename -uid "557DB851-4CCB-2B07-F526-4EAFB92FDCB8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "BC15A72C-4830-EA8B-39B6-6B94A0CEE8AA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003" 
		-p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "FF3F0122-435B-6948-0E4B-B3A021223964";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005" -p "jntl_TougueSIdeA_001";
	rename -uid "E44BC057-4AD0-4629-D519-89A8D5240CE5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005";
	rename -uid "B53C4AC2-44AC-3320-503B-63BBCE21723F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003" 
		-p "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005";
	rename -uid "38135A87-436E-FB60-B72E-26B7E6BCDFF2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_002" -p "bpjnt_m_Tougue_005";
	rename -uid "A71D497E-47CB-ED35-C9A8-C0A74FCBFCB2";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147035 -9.9475983006414001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.44585654544147468 155.32984924316406 5.531624674797059 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_002" -p "jntl_TougueSIdeA_002";
	rename -uid "46A7D400-4392-6627-B7F2-2488E09AE925";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147052 -7.1054273576010006e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002";
	rename -uid "4CDF4DB8-4C97-87B0-E42D-E1BDC23C6149";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147024 -4.2632564145605999e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_002" -p "jntl_TougueSIdeA_002";
	rename -uid "67B0F823-4963-5F70-7A96-579B9520306D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_002";
	rename -uid "B0F10F16-427D-FE0B-C18D-65AB2C162310";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_002";
	rename -uid "0A732873-49AB-1125-5D69-F4A43C0E51C2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_003";
	rename -uid "AE10ED82-41F9-9289-4143-36B45E1BDA1F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_004" -p "jntl_TougueSIdeA_002";
	rename -uid "188C4DDF-446F-C875-1704-BB9076DF934B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_004";
	rename -uid "D894E54A-4559-1ED4-ABAE-F1BA3A3319AF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_005" -p "jntl_TougueSIdeA_002";
	rename -uid "321BAF28-433F-19D0-3F88-25965A328684";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_005";
	rename -uid "1E9B2860-4B77-B7A4-37B2-D187DCB96A60";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001" -p "bpjnt_m_Tougue_005";
	rename -uid "5D40B6ED-4D52-2F29-9D26-BBB76DB30D3C";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147035 -9.9475983006414001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.44585654544147468 155.32984924316406 5.531624674797059 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_001";
	rename -uid "CDC7EF7C-4BD7-40BA-68CE-4096BEFA37B6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147052 -7.1054273576010006e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002";
	rename -uid "9A3A6690-45CE-C565-64D2-A19BED146CF4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147024 -4.2632564145605999e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002";
	rename -uid "86003995-48A0-8D10-CA6F-19B89F0D8A68";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147069 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_001";
	rename -uid "286B72E1-4280-8266-6F11-1B85086868D8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003";
	rename -uid "1223E3C4-441D-69A1-5CFE-40B4155EDBD2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_001";
	rename -uid "A9FE7571-46AE-56ED-A990-9F84028EB1FC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003";
	rename -uid "F2C62E50-4372-2839-4905-3E8EA08B19E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003";
	rename -uid "9E80DA96-44E5-C830-4442-56837BD4A0FC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005" -p "jnt_l_TougueSIdeA_001";
	rename -uid "C50CF04C-4065-B177-3336-E38DF48488EC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005";
	rename -uid "A2F650D1-4626-1502-90FE-77896AFE9264";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005";
	rename -uid "F27629FD-4142-E535-FA24-57B570374A17";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007" -p "jnt_l_TougueSIdeA_001";
	rename -uid "DEC21646-476F-6D59-0B6D-E4B1C7F9AE6A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007";
	rename -uid "8CDDCCC4-4F82-389F-5D85-C2AFE69DC180";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007";
	rename -uid "1A94E9F9-44E3-56FB-B5EE-A99F1DFCF5CA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_002" -p "bpjnt_m_Tougue_005";
	rename -uid "792B4E8C-45FB-6D9B-0D4F-E3A7B654EF95";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147035 -9.9475983006414001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.44585654544147468 155.32984924316406 5.531624674797059 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_002";
	rename -uid "570F19A4-487C-101B-DBFF-07B054F9E252";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147052 -7.1054273576010006e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002";
	rename -uid "290316AF-493F-4580-3BB2-B1A49A2E2D6B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147024 -4.2632564145605999e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002";
	rename -uid "1FAC2D40-4157-4E3F-391B-EB9660CBEBE5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147069 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_002";
	rename -uid "B91614DD-4511-8EB8-3A52-B39F52F264BB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003";
	rename -uid "2059A08C-46A5-9317-C185-B8BDC8853AB3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_002";
	rename -uid "86A5578D-4636-3187-3CB1-70812B0EC2C5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "5DE51E34-4679-F151-319B-8DA00AC19A72";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "B68B16D6-44BA-D1D8-B975-199AC2645657";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_002";
	rename -uid "6A664D1D-4732-AEA9-EBF1-6EB8F51D1BC1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002";
	rename -uid "BC43FCF9-4B76-EED8-F368-5096086A2E1B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002";
	rename -uid "F7F54681-4E68-8890-87A7-8F8F87721DA1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_002";
	rename -uid "B5F24214-4FED-EF69-A678-3494225E87E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003";
	rename -uid "C6B7D3AE-45ED-5DD8-1EE0-B38AB87A03AF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003";
	rename -uid "BCD17FE1-4022-2F7C-EB9E-3AB55A1E7F53";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_003" -p "bpjnt_m_Tougue_005";
	rename -uid "4F44699A-49D2-CC89-FC82-D680D0AF2CF1";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147035 -9.9475983006414001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.44585654544147468 155.32984924316406 5.531624674797059 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_003";
	rename -uid "A05635B1-42DA-4DEF-845F-C394ED996284";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147052 -7.1054273576010006e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_002";
	rename -uid "EFB30D64-44C6-E17C-4FAF-1E8A50300D6D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147024 -4.2632564145605999e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_002";
	rename -uid "C3C294CB-48CF-885F-C562-1CBAD9776426";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147069 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_003";
	rename -uid "3194374A-403F-41EE-2A90-D8B873B49930";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003";
	rename -uid "ABC83CAE-40E8-362F-0291-F3A346C17C78";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_003";
	rename -uid "3EC8071A-4787-71AE-87A3-A6AD16B06624";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "8F27FA71-4ACD-6AF3-FB98-4DBD6FA3AF47";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "7D834F2C-4DB0-ADDE-2230-84B21B7CA26D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004" -p "jnt_l_TougueSIdeA_003";
	rename -uid "A8B733DF-48F8-D3BB-3A59-9290F7C13849";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "9D0B4800-4B3B-6485-9110-AFB83DCC3E0B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "9657824C-4620-6247-02CD-D9AE52357BF5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_003";
	rename -uid "AC0BA1B5-4677-B92C-8405-D28EE1CE94FC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002";
	rename -uid "2EAD04D0-45AB-A85E-3372-CDB88A8F0F06";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002";
	rename -uid "3EF881AF-4523-49A4-C1FD-8F972B582C85";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_004" -p "bpjnt_m_Tougue_005";
	rename -uid "59C1887C-4672-A779-386B-6FB9C3C0D5CC";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147035 -9.9475983006414001e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.44585654544147468 155.32984924316406 5.531624674797059 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_005']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_004";
	rename -uid "0D597D36-4795-29BD-0420-EE9E46702B42";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147052 -7.1054273576010006e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_002";
	rename -uid "8BBED5E8-440F-BAA6-21F8-4AACF89DABA5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147024 -4.2632564145605999e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_002";
	rename -uid "3B3BA2A0-4F11-44FE-F9AE-0A88A05FACBE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147069 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_003" -p "jnt_l_TougueSIdeA_004";
	rename -uid "EA479157-460B-2F00-E841-318C190CB7A7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003";
	rename -uid "1B385A98-4470-E90C-DD5B-C989B4D538BD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002" -p "jnt_l_TougueSIdeA_004";
	rename -uid "12F87E76-426B-6711-3DB3-22AD93F8A424";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "1BF2E042-430C-2F04-5D19-C29929B041B2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002";
	rename -uid "94F5BC39-4DFC-11CD-E1D5-DF887E963BEA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004" -p "jnt_l_TougueSIdeA_004";
	rename -uid "8F50C2EE-41CA-4559-FF95-9BB52E62450E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "56DAFBB1-473D-9AD6-4CE0-F2948B22326A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004";
	rename -uid "AB921C48-47D2-AD75-964E-1684CED09677";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006" -p "jnt_l_TougueSIdeA_004";
	rename -uid "773F25DE-4F85-5290-1F04-98B86D162668";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147074 -4.2632564145605999e-14 3.5527136788005001e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.0816681711721685e-17 0
		 0 0 1 0 0.89171309088294937 155.32984924316406 5.5316246747970599 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeA_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006";
	rename -uid "B95651F0-4CC8-A95D-26A6-FC96A72A544D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 -2.8421709430404001e-14 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode joint -n "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004" 
		-p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006";
	rename -uid "EB0EA185-4752-3512-5637-22BCA5E3F82C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.44585654544147157 0 1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 1.7347234759768071e-18 1 -2.0816681711721685e-17 0
		 0 0 1 0 1.337569636324424 155.32984924316406 5.5316246747970608 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeA003";
	setAttr ".liw" yes;
createNode transform -n "bpctrl_m_Tougue_004" -p "bpjnt_m_Tougue_004";
	rename -uid "32912E59-4C98-62FE-CD90-088D0B868A90";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.1098164488104747e-16 1.4210854715202006e-13 5.329070518200753e-15 ;
	setAttr ".sp" -type "double3" 1.1098164488104747e-16 1.4210854715202006e-13 5.329070518200753e-15 ;
createNode nurbsCurve -n "bpctrl_m_Tougue_004Shape" -p "bpctrl_m_Tougue_004";
	rename -uid "86C5090B-41C1-68CC-AA8E-9DB4B378AF34";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.41463336722590577 1.0010134985691361 -1.3322676295501873e-15
		3.4666659216443262e-16 1.0834892032386558 -1.3322676295501873e-15
		-0.41463336722590627 1.0010134985691361 -1.3322676295501873e-15
		-0.76614256295250227 0.76614256295235306 -1.3322676295501873e-15
		-1.0010134985692081 0.41463336722594574 -1.3322676295501873e-15
		-1.0834892032387102 -2.8477220581635253e-14 -1.3322676295501873e-15
		-1.0010134985692078 -0.41463336722600258 -1.3322676295501873e-15
		-0.76614256295250227 -0.7661425629526375 -1.3322676295501873e-15
		-0.41463336722590605 -1.0010134985692214 -1.3322676295501873e-15
		1.7172379537031849e-16 -1.0834892032386558 -1.3322676295501873e-15
		0.4146333672259066 -1.0010134985692214 -1.3322676295501873e-15
		0.76614256295250249 -0.7661425629526375 -1.3322676295501873e-15
		1.0010134985692085 -0.41463336722600258 -1.3322676295501873e-15
		1.0834892032387105 -2.8477220581635253e-14 -1.3322676295501873e-15
		1.0010134985692085 0.41463336722594574 -1.3322676295501873e-15
		0.76614256295250227 0.76614256295235306 -1.3322676295501873e-15
		0.41463336722590577 1.0010134985691361 -1.3322676295501873e-15
		;
createNode joint -n "jntl_TougueSIdeB_001" -p "bpjnt_m_Tougue_004";
	rename -uid "21A07745-4AE2-67F8-28B1-63BDC2A36C8F";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.58345282269788046 1.7053025658242399e-13 5.3290705182007498e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -2.7755575615628914e-17 0 0 0 1 0 0.5834528226978839 155.24688644409181 4.221682834625244 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB001";
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'jnt_m_Tougue_004']";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeB_002" -p "jntl_TougueSIdeB_001";
	rename -uid "F4BEF1C9-4EB1-1D64-35A2-A58A22744E0B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.58345282269788012 0 -1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 4.3368086899420177e-19 1 -2.7755575615628914e-17 0
		 0 0 1 0 1.1669056453957678 155.24688644409184 4.221682834625244 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB002";
	setAttr ".liw" yes;
createNode joint -n "bpjnt_l_TougueSIdeB_003" -p "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|jntl_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002";
	rename -uid "74DC3F35-480C-DB58-3883-DD85A0FDFFA8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.58345282269787935 2.8421709430404001e-14 -1.7763568394002501e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.99999999999999989 -1.7235866783159786e-14 -2.4611738716511772e-17 0
		 1.4476757067054944e-19 0.99999999999999978 -2.4093849454952548e-17 8.6736173798840355e-19
		 0 0 1 0 1.7503584680936517 155.24688644409187 4.2216828346252449 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "TougueSIdeB003";
	setAttr ".liw" yes;
createNode transform -n "bpctrl_m_Tougue_003" -p "bpjnt_m_Tougue_003";
	rename -uid "C528AE26-4E11-A45F-50B7-9E93B850284B";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.3552527156068808e-20 -5.6843418860808027e-14 -2.6645352591003765e-15 ;
	setAttr ".sp" -type "double3" -1.3552527156068808e-20 -5.6843418860808027e-14 -2.6645352591003765e-15 ;
createNode nurbsCurve -n "bpctrl_m_Tougue_003Shape" -p "bpctrl_m_Tougue_003";
	rename -uid "FEB46912-40D9-6D34-7D28-F6B8F4CFE9AA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.5665846168439147 1.3678562662165061 -1.3322676295501875e-15
		3.3392749286195723e-16 1.4805569536738401 -1.3322676295501875e-15
		-0.56658461684391614 1.3678562662165061 -1.3322676295501875e-15
		-1.0469118618756865 1.0469118618755997 -1.3322676295501875e-15
		-1.3678562662165441 0.56658461684384054 -4.4408920985006252e-16
		-1.4805569536738639 8.5254719950356149e-14 -4.4408920985006252e-16
		-1.3678562662165432 -0.56658461684395423 -4.4408920985006252e-16
		-1.0469118618756865 -1.0469118618756565 4.4408920985006232e-16
		-0.5665846168439157 -1.3678562662167051 4.4408920985006232e-16
		9.4874466356059648e-17 -1.4805569536738969 4.4408920985006232e-16
		0.56658461684391648 -1.3678562662167051 4.4408920985006232e-16
		1.0469118618756863 -1.0469118618756565 4.4408920985006232e-16
		1.3678562662165443 -0.56658461684395423 -4.4408920985006252e-16
		1.4805569536738639 8.5254719950356149e-14 -4.4408920985006252e-16
		1.3678562662165439 0.56658461684384054 -4.4408920985006252e-16
		1.0469118618756861 1.0469118618755997 -1.3322676295501875e-15
		0.5665846168439147 1.3678562662165061 -1.3322676295501875e-15
		;
createNode transform -n "bpctrl_m_Tougue_002" -p "bpjnt_m_Tougue_002";
	rename -uid "26EEC365-46D6-BFAE-D712-59931FCB9F60";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.387778780781446e-17 -1.4210854715202006e-13 3.5527136788005017e-15 ;
	setAttr ".sp" -type "double3" 1.387778780781446e-17 -1.4210854715202006e-13 3.5527136788005017e-15 ;
createNode nurbsCurve -n "bpctrl_m_Tougue_002Shape" -p "bpctrl_m_Tougue_002";
	rename -uid "DE43BF40-408D-84CB-0DEB-83996A769657";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.69683246472376137 1.6823023870379643 -2.2204460492503128e-16
		1.0547118733938987e-15 1.8209109822631717 -2.2204460492503128e-16
		-0.69683246472376115 1.6823023870379643 -2.2204460492503128e-16
		-1.2875785034953517 1.2875785034953822 -2.2204460492503128e-16
		-1.6823023870379752 0.69683246472385463 2.2204460492503128e-16
		-1.8209109822631824 8.5265128291212022e-14 2.2204460492503128e-16
		-1.6823023870379743 -0.69683246472379778 2.2204460492503128e-16
		-1.2875785034953517 -1.2875785034952969 2.2204460492503128e-16
		-0.69683246472376092 -1.6823023870379359 6.6613381477509383e-16
		7.9103390504542413e-16 -1.8209109822631717 6.6613381477509383e-16
		0.69683246472376259 -1.6823023870379359 6.6613381477509383e-16
		1.2875785034953524 -1.2875785034952969 2.2204460492503128e-16
		1.682302387037977 -0.69683246472379778 2.2204460492503128e-16
		1.8209109822631824 8.5265128291212022e-14 2.2204460492503128e-16
		1.6823023870379765 0.69683246472385463 2.2204460492503128e-16
		1.2875785034953524 1.2875785034953822 -2.2204460492503128e-16
		0.69683246472376137 1.6823023870379643 -2.2204460492503128e-16
		;
createNode transform -n "bpctrl_m_Tougue_001" -p "bpjnt_m_Tougue_001";
	rename -uid "BF619175-4433-DBB6-F443-F69174D80B6C";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 2.1510571102112413e-16 2.8421709430404014e-14 -8.8817841970012543e-16 ;
	setAttr ".sp" -type "double3" 2.1510571102112413e-16 2.8421709430404014e-14 -8.8817841970012543e-16 ;
createNode nurbsCurve -n "bpctrl_m_Tougue_001Shape" -p "bpctrl_m_Tougue_001";
	rename -uid "7CE53B03-409B-2CFF-1EE1-038182BC92BD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.82172221209938712 1.9838129089533538 -1.1102230246251565e-16
		3.677613769070831e-16 2.1472636194906443 -2.7755575615628914e-16
		-0.82172221209938967 1.9838129089533538 -1.1102230246251565e-16
		-1.5183446663370486 1.5183446663370717 -1.1102230246251565e-16
		-1.9838129089535681 0.82172221209938812 0
		-2.1472636194907055 -8.5265128291212022e-14 1.1102230246251565e-16
		-1.9838129089535677 -0.82172221209953022 1.1102230246251565e-16
		-1.5183446663370486 -1.5183446663370717 2.2204460492503131e-16
		-0.82172221209938912 -1.983812908953638 2.2204460492503131e-16
		2.7755575615628914e-17 -2.1472636194907011 2.2204460492503131e-16
		0.82172221209938867 -1.983812908953638 2.2204460492503131e-16
		1.5183446663370488 -1.5183446663370717 2.2204460492503131e-16
		1.9838129089535685 -0.82172221209953022 1.1102230246251565e-16
		2.147263619490706 -8.5265128291212022e-14 1.1102230246251565e-16
		1.9838129089535677 0.82172221209938812 0
		1.5183446663370479 1.5183446663370717 -1.1102230246251565e-16
		0.82172221209938712 1.9838129089533538 -1.1102230246251565e-16
		;
createNode transform -n "Gum_Rig" -p "Face_Rig";
	rename -uid "70DCCF79-42FE-4FBD-EB3E-DA95756FB659";
createNode joint -n "bpjnt_m_gumUpper_001" -p "Gum_Rig";
	rename -uid "CE1F53A7-4C63-6115-88F2-7B80C75DEE57";
	setAttr ".t" -type "double3" 2.1175823681357508e-22 156.73228454589838 5.7590803304999003 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_m_gumUpper_001" -p "bpjnt_m_gumUpper_001";
	rename -uid "9B770A26-496F-8B38-4804-4681A09418F7";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 2.8421709430404014e-14 -3.0198066269804264e-14 ;
	setAttr ".sp" -type "double3" 0 2.8421709430404014e-14 -3.0198066269804264e-14 ;
createNode nurbsCurve -n "bpctrl_m_gumUpper_001Shape" -p "bpctrl_m_gumUpper_001";
	rename -uid "9DB282EE-4C06-E21C-58AE-03B1CF7AEE44";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 11 0 no 3
		12 0 1 2 3 4 5 6 7 8 9 10 11
		12
		5.6635756846986807 -2.8732574659173938e-14 -2.5999874715493223
		5.4693589445096293 -2.9004857993355209e-14 -1.3737323491913391
		4.6525122734077415 -2.9360827686843201e-14 0.22941262975635884
		3.3802465543059905 -2.9643327425800814e-14 1.5016783488581102
		1.7771015753582931 -2.9824703822169956e-14 2.3185250199599969
		-1.713877044929582e-07 -2.9887201041034328e-14 2.5999874715492663
		-1.7771015753582931 -2.9824703822169956e-14 2.3185250199599969
		-3.3802465543059905 -2.9643327425800814e-14 1.5016783488581102
		-4.6525122734077415 -2.9360827686843201e-14 0.22941262975635884
		-5.4693589445096293 -2.9004857993355209e-14 -1.3737323491913391
		-5.6635756846986807 -2.8732574659173938e-14 -2.5999874715493223
		5.6635756846986807 -2.8732574659173938e-14 -2.5999874715493223
		;
createNode joint -n "bpjnt_m_gumLower_001" -p "Gum_Rig";
	rename -uid "077BD7FD-4DD2-B2B9-0441-4E92A8DFCC57";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.1175823681357508e-22 154.36588872411284 5.7018810272291365 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 5.1000000000000005 0 0 0 0 2.2648549702353196e-15 -5.1000000000000005 0
		 0 5.1000000000000005 2.1233015345956123e-15 0 9.9226942456680812e-08 154.55132293701175 4.2368857860565186 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "gumLower001";
	setAttr ".radi" 0.5;
	setAttr ".liw" yes;
createNode transform -n "bpctrl_m_gumLower_001" -p "bpjnt_m_gumLower_001";
	rename -uid "68C34A8D-4C59-6127-2833-A1AEA6DCA963";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 2.8421709430404014e-14 3.1974423109204515e-14 ;
	setAttr ".sp" -type "double3" 0 2.8421709430404014e-14 3.1974423109204515e-14 ;
createNode nurbsCurve -n "bpctrl_m_gumLower_001Shape" -p "bpctrl_m_gumLower_001";
	rename -uid "1B0A4F2E-4783-DE64-14E6-359A04E92DBE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 11 0 no 3
		12 0 1 2 3 4 5 6 7 8 9 10 11
		12
		5.6635756846986807 -1.2925916973667973e-14 -2.5999874715492663
		5.4693589445096293 -1.3198200307849247e-14 -1.3737323491912834
		4.6525122734077415 -1.3554170001337236e-14 0.22941262975641458
		3.3802465543059905 -1.3836669740294846e-14 1.501678348858166
		1.7771015753582931 -1.4018046136663991e-14 2.3185250199600524
		-1.713877044929582e-07 -1.4080543355528362e-14 2.5999874715493223
		-1.7771015753582931 -1.4018046136663991e-14 2.3185250199600524
		-3.3802465543059905 -1.3836669740294846e-14 1.501678348858166
		-4.6525122734077415 -1.3554170001337236e-14 0.22941262975641458
		-5.4693589445096293 -1.3198200307849247e-14 -1.3737323491912834
		-5.6635756846986807 -1.2925916973667973e-14 -2.5999874715492663
		5.6635756846986807 -1.2925916973667973e-14 -2.5999874715492663
		;
createNode transform -n "Lip_Rig" -p "Face_Rig";
	rename -uid "379C11FF-4728-E054-EF6F-17A60166B342";
createNode joint -n "bpjnt_r_LipCorner_001" -p "Lip_Rig";
	rename -uid "C8F5C7FA-41AD-42C7-E016-DCB5DA94341F";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.2341098785400382 155.83387756347653 5.532587051391598 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.2341098785400391 155.83387756347656 5.5325870513916016 1;
	setAttr ".radi" 0.5;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'AlexBody_Rig:mesh_m_high_body_001.vtx[5087]']";
createNode transform -n "bpctrl_r_LipCorner_001" -p "bpjnt_r_LipCorner_001";
	rename -uid "4068637F-4C83-E24C-EAF0-689D4899D597";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" -4.4408920985006271e-16 -1.4210854715202007e-14 -8.8817841970012543e-16 ;
	setAttr ".sp" -type "double3" -4.4408920985006271e-16 -1.4210854715202007e-14 -8.8817841970012543e-16 ;
createNode nurbsCurve -n "bpctrl_r_LipCorner_001Shape" -p "bpctrl_r_LipCorner_001";
	rename -uid "7CA9CFAC-42AC-4F5F-AE13-3E96714E7181";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.14229795048362082 0.53444969501356354 -0.16958409370764826
		0 0.57848418133130508 4.0140403593465565e-18
		0.14229795048362082 0.53444969501356354 0.16958409370764826
		0.26293232794024401 0.40905008742851123 0.31335054643194482
		0.34353764195545278 0.22137631208079256 0.40941221899175417
		0.3718424641594229 0 0.44314459254107597
		0.34353764195545278 -0.22137631208076414 0.40941221899175417
		0.26293232794024401 -0.40905008742851123 0.31335054643194482
		0.14229795048362082 -0.53444969501353512 0.16958409370764826
		0 -0.57848418133130508 -4.0140403593465565e-18
		-0.14229795048362082 -0.53444969501353512 -0.16958409370764826
		-0.26293232794024401 -0.40905008742851123 -0.31335054643194482
		-0.34353764195545278 -0.22137631208076414 -0.40941221899175417
		-0.3718424641594229 0 -0.44314459254107774
		-0.34353764195545278 0.22137631208079256 -0.40941221899175417
		-0.26293232794024401 0.40905008742851123 -0.31335054643194482
		-0.14229795048362082 0.53444969501356354 -0.16958409370764826
		;
createNode transform -n "bpctrl_r_LipCornerDrv_001" -p "bpjnt_r_LipCorner_001";
	rename -uid "71CE5618-492B-ADD9-7611-D9B194CDFA02";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	setAttr ".rp" -type "double3" -0.006774643293430584 0.0018105373479215818 0.14464355366935247 ;
	setAttr ".sp" -type "double3" -0.006774643293430584 0.0018105373479215818 0.14464355366935247 ;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'AlexBody_Rig:mesh_m_high_body_001.vtx[3181]']";
createNode nurbsCurve -n "bpctrl_r_LipCornerDrv_00Shape1" -p "bpctrl_r_LipCornerDrv_001";
	rename -uid "3EBC21A7-4AF9-5934-6691-6187107C0E9C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 22 0 no 3
		27 0 0 0 1 1 1 2 2 2 3 3 3 4 4 4 5 5 5 6 6 6 7 7 7 8 8 8
		25
		0.4794492557287735 0.89655279548085787 0.6788624191653696
		0.36791148861959133 0.89655279548085787 0.5635223744009803
		-0.41286291964410671 0.89655279548085787 -0.2438683196575786
		-0.52440068675328888 0.89655279548085787 -0.35920836442196791
		-0.59081106907543823 0.89655279548085787 -0.42788264998803083
		-0.64329022229634036 0.81913047675058692 -0.48486956032898831
		-0.64161427557400064 0.72362487471542636 -0.48649025811513447
		-0.63879952439746335 0.56322329266561155 -0.48921221874763088
		-0.61909601283155613 -0.55960221796982523 -0.50826618815401048
		-0.61628126165501795 -0.72000380001964004 -0.51098814878650689
		-0.61460531493267867 -0.8155094020548006 -0.51260884657265304
		-0.55940892463778535 -0.89293172078504313 -0.4582495973927303
		-0.49299854231563511 -0.89293172078504313 -0.38957531182666738
		-0.38146077520645294 -0.89293172078504313 -0.27423526706227808
		0.3993136330572451 -0.89293172078504313 0.53315542699628171
		0.51085140016642727 -0.89293172078504313 0.64849547176067102
		0.57726272517513166 -0.89293172078504313 0.71717073214909366
		0.62974093570947964 -0.8155094020548006 0.77415666766769142
		0.62806498898713947 -0.72000380001964004 0.77577736545383758
		0.62525023781060174 -0.55960221796982523 0.77849932608633399
		0.60554672624469497 0.56322329266561155 0.79755329549271359
		0.60273197506815723 0.72362487471542636 0.80027525612521089
		0.60105602834581706 0.81913047675058692 0.80189595391135704
		0.5458605807374779 0.89655279548085787 0.74753767955379402
		0.4794492557287735 0.89655279548085787 0.6788624191653696
		;
createNode joint -n "bpjnt_l_LipCorner_001" -p "Lip_Rig";
	rename -uid "D28917CF-4416-C3A6-CC1C-278EDA02D9A9";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.9160954952239977 155.83422851562494 5.7186422348022443 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.916095495223999 155.834228515625 5.7186422348022461 1;
	setAttr ".radi" 0.5;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'AlexBody_Rig:mesh_m_high_body_001.vtx[1111]']";
createNode transform -n "bpctrl_l_LipCorner_001" -p "bpjnt_l_LipCorner_001";
	rename -uid "C2EAC704-421A-6E78-25D0-699670921528";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 0 -1.4210854715202007e-14 -2.6645352591003765e-15 ;
	setAttr ".sp" -type "double3" 0 -1.4210854715202007e-14 -2.6645352591003765e-15 ;
createNode nurbsCurve -n "bpctrl_l_LipCorner_001Shape" -p "bpctrl_l_LipCorner_001";
	rename -uid "061BA9AA-423B-55EF-9A19-64AA2D3AD118";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.17791066865751626 0.53444969501350659 -0.13173938487905895
		4.4007516949071606e-16 0.57848418133127655 9.765948576342031e-15
		-0.17791066865751803 0.53444969501350659 0.13173938487908912
		-0.32873605077615808 0.40905008742848276 0.24342264263082844
		-0.42951434916385045 0.22137631208073569 0.31804700967376853
		-0.4649029814486112 -2.8421709430404007e-14 0.34425160259719612
		-0.42951434916385178 -0.22137631208079253 0.31804700967376853
		-0.32873605077615808 -0.4090500874285396 0.24342264263082844
		-0.17791066865751803 -0.53444969501356343 0.13173938487908915
		4.4810325020940917e-16 -0.57848418133133339 9.7739766570607241e-15
		0.17791066865751626 -0.53444969501356343 -0.13173938487905892
		0.32873605077616075 -0.4090500874285396 -0.24342264263081245
		0.42951434916384645 -0.22137631208079253 -0.3180470096737561
		0.46490298144861031 -2.8421709430404007e-14 -0.34425160259719789
		0.42951434916384645 0.22137631208073569 -0.3180470096737561
		0.32873605077616075 0.40905008742848276 -0.24342264263081245
		0.17791066865751626 0.53444969501350659 -0.13173938487905895
		;
createNode transform -n "bpctrl_l_LipCornerDrv_001" -p "bpjnt_l_LipCorner_001";
	rename -uid "B1A6B759-4F9C-EEF2-1167-FA81EE9E2EAE";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	setAttr ".rp" -type "double3" 0.031690111796209404 -0.01312500480956658 -0.11422504239197909 ;
	setAttr ".sp" -type "double3" 0.031690111796209404 -0.01312500480956658 -0.11422504239197909 ;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'AlexBody_Rig:mesh_m_high_body_001.vtx[1111]']";
createNode nurbsCurve -n "bpctrl_l_LipCornerDrv_00Shape1" -p "bpctrl_l_LipCornerDrv_001";
	rename -uid "16047632-40D2-CAF1-BB98-7D8FA5B2D114";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 22 0 no 3
		27 0 0 0 1 1 1 2 2 2 3 3 3 4 4 4 5 5 5 6 6 6 7 7 7 8 8 8
		25
		0.57269894232628227 0.88161725333583252 -0.59288245798097006
		0.45580059361477288 0.88161725333364405 -0.48297897538612322
		-0.36249836832238591 0.88161725331832475 0.28635529419015177
		-0.47939671703389486 0.88161725331613627 0.39625877678499777
		-0.54899882788805998 0.88161725331482887 0.46169609444722959
		-0.6067186598266141 0.80419493458327895 0.51336804499854349
		-0.60831561065825079 0.70868933254783417 0.51166945537250552
		-0.61099768829968681 0.5482877504975362 0.50881667545735987
		-0.62977247317913987 -0.57453776014119728 0.48884695929857996
		-0.63245455082057545 -0.73493934219149526 0.48599417938343431
		-0.63405150165221302 -0.83044494422694004 0.48429558975739634
		-0.57892082958803126 -0.90786726295635833 0.42986969085924998
		-0.50931871873386614 -0.90786726295505094 0.36443237319701816
		-0.39242037002235719 -0.90786726295286246 0.25452889060217221
		0.42587859191480204 -0.90786726293754316 -0.51480537897410283
		0.54277694062631099 -0.90786726293535469 -0.62470886156894967
		0.61238003947319353 -0.90786726293404729 -0.69014710810521163
		0.67009888341903068 -0.83044494420249737 -0.74181812978249539
		0.67169583425066737 -0.73493934216705259 -0.74011954015645742
		0.67437791189210339 -0.57453776011678304 -0.73726676024131266
		0.69315269677155689 0.54828775052197887 -0.71729704408253181
		0.69583477441299246 0.70868933257224842 -0.71444426416738616
		0.69743172524463004 0.8041949346076932 -0.71274567454134907
		0.64230204117316525 0.88161725333713992 -0.6583207045172329
		0.57269894232628227 0.88161725333583252 -0.59288245798097006
		;
createNode transform -n "LipUpper_Rig" -p "Lip_Rig";
	rename -uid "9A638E09-4D6D-C38E-B35B-CEB445E81A6F";
createNode transform -n "LipUpper_Rig_Crv" -p "LipUpper_Rig";
	rename -uid "A6F4FC1A-48F2-F740-6BEE-B4A75113F9B6";
createNode transform -n "crv_m_LipUpper_001" -p "LipUpper_Rig_Crv";
	rename -uid "75F75FA4-4FE4-DCF9-AB07-E4B6B8C9B2F6";
	setAttr ".rp" -type "double3" -0.15900719165802002 156.74577224160419 6.5839207172393799 ;
	setAttr ".sp" -type "double3" -0.15900719165802002 156.74577224160419 6.5839207172393799 ;
createNode nurbsCurve -n "crv_m_LipUpper_00Shape1" -p "crv_m_LipUpper_001";
	rename -uid "FC8B146C-4457-B15F-FA2C-BF97A1CE81CA";
	setAttr -k off ".v";
createNode transform -n "crv_m_LipUpperAim_001" -p "LipUpper_Rig_Crv";
	rename -uid "112A4216-436D-D2B8-987B-40A71D036011";
	setAttr ".rp" -type "double3" -0.15900719165802002 156.16985321044922 7.3921596821192814 ;
	setAttr ".sp" -type "double3" -0.15900719165802002 156.16985321044922 7.3921596821192814 ;
createNode nurbsCurve -n "crv_m_LipUpperAim_00Shape1" -p "crv_m_LipUpperAim_001";
	rename -uid "7C183516-4702-1380-2C2E-0AB2C4518997";
	setAttr -k off ".v";
createNode transform -n "crv_m_LipUpperUP_001" -p "LipUpper_Rig_Crv";
	rename -uid "C3F61C14-417B-B270-02A1-029C3E717C87";
	setAttr ".rp" -type "double3" -0.15900719165802002 156.16985321044922 6.5839207172393799 ;
	setAttr ".sp" -type "double3" -0.15900719165802002 156.16985321044922 6.5839207172393799 ;
createNode nurbsCurve -n "crv_m_LipUpperUP_00Shape1" -p "crv_m_LipUpperUP_001";
	rename -uid "37CA45BF-4BC0-CBD4-46B2-F39B921E95B0";
	setAttr -k off ".v";
createNode transform -n "LipUpper_Rig_Jnt" -p "LipUpper_Rig";
	rename -uid "A2BB5AC1-4425-F365-17C9-FA94BBAD8CCB";
createNode joint -n "bpjnt_l_LipUpper_002" -p "LipUpper_Rig_Jnt";
	rename -uid "BAD06DFF-4B7D-D1CC-0E2A-48A766DEC56A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6589762339671563 156.37898254394528 6.9300105959608231 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6589762339671572 156.37898254394534 6.9300105959608231 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_l_LipUpper_002" -p "bpjnt_l_LipUpper_002";
	rename -uid "5621D3A0-4D40-2CB6-1EE6-5098F867BC3B";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 2.8421709430404014e-14 -5.329070518200753e-15 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 2.8421709430404014e-14 -5.329070518200753e-15 ;
createNode nurbsCurve -n "bpctrl_l_LipUpper_002Shape" -p "bpctrl_l_LipUpper_002";
	rename -uid "F1017CC7-4EFA-036A-A032-0483EAF215CD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.11896662681051426 0.3650363329099377 -0.093323570811707945
		-1.1095376137312033e-15 0.39511247956508549 2.6617936155245637e-15
		-0.11896662681051604 0.3650363329099377 0.093323570811686629
		-0.21982166312428814 0.27938671363187945 0.17243947394758496
		-0.28721084391572493 0.15120299985019867 0.22530303034268773
		-0.31087477729377799 -8.5265128291212022e-14 0.24386624274516766
		-0.28721084391572493 -0.15120299985034077 0.22530303034268773
		-0.21982166312428814 -0.27938671363199313 0.17243947394758496
		-0.11896662681051604 -0.36503633291005139 0.093323570811686629
		-1.1109084355191094e-15 -0.39511247956519918 2.6672769026761877e-15
		0.11896662681051426 -0.36503633291005139 -0.093323570811707945
		0.21982166312428592 -0.27938671363199313 -0.1724394739476045
		0.28721084391572449 -0.15120299985034077 -0.22530303034270904
		0.31087477729377755 -8.5265128291212022e-14 -0.24386624274517121
		0.28721084391572449 0.15120299985019867 -0.22530303034270904
		0.21982166312428592 0.27938671363187945 -0.1724394739476045
		0.11896662681051426 0.3650363329099377 -0.093323570811707945
		;
createNode joint -n "bpjnt_l_LipUpper_001" -p "LipUpper_Rig_Jnt";
	rename -uid "3532667D-45AE-4B97-8ADC-A8B6C2CD4490";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.85893625832235121 156.50582885742185 7.4359426065053089 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.85893625832235143 156.5058288574219 7.4359426065053107 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_l_LipUpper_001" -p "bpjnt_l_LipUpper_001";
	rename -uid "B799384D-458B-ED03-11FF-119F4B63A1FE";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" -1.1102230246251568e-16 2.8421709430404014e-14 -5.329070518200753e-15 ;
	setAttr ".sp" -type "double3" -1.1102230246251568e-16 2.8421709430404014e-14 -5.329070518200753e-15 ;
createNode nurbsCurve -n "bpctrl_l_LipUpper_001Shape" -p "bpctrl_l_LipUpper_001";
	rename -uid "ABDAE2E2-4E60-5C73-AB0B-96A9769615C2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.14032793695583212 0.36503633290996618 -0.056306458541092397
		-2.664877964547352e-15 0.39511247956511397 1.0660882679977315e-14
		-0.14032793695583456 0.36503633290996618 0.056306458541094173
		-0.2592922175860557 0.27938671363193635 0.10404076918860206
		-0.33878160857860617 0.15120299985022712 0.13593581585908154
		-0.36669457072799561 -2.8421709430404007e-14 0.14713586682625923
		-0.33878160857860617 -0.15120299985031238 0.13593581585908154
		-0.2592922175860557 -0.27938671363196477 0.10404076918860206
		-0.14032793695583456 -0.36503633291002302 0.056306458541094173
		-2.2201033438033364e-15 -0.39511247956514239 1.0655399392825691e-14
		0.14032793695583212 -0.36503633291002302 -0.056306458541092397
		0.25929221758605658 -0.27938671363196477 -0.10404076918861804
		0.33878160857860662 -0.15120299985031238 -0.13593581585908687
		0.36669457072799538 -2.8421709430404007e-14 -0.14713586682626101
		0.33878160857860662 0.15120299985022712 -0.13593581585908687
		0.25929221758605658 0.27938671363193635 -0.10404076918861804
		0.14032793695583212 0.36503633290996618 -0.056306458541092397
		;
createNode joint -n "bpjnt_m_LipUpper_001" -p "LipUpper_Rig_Jnt";
	rename -uid "7CB4A005-4A2B-7A4A-124C-CABC6C2EE8D4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 3.7645895645243283e-05 156.48207092285151 7.6352543830871547 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.7645895645243283e-05 156.48207092285156 7.6352543830871582 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_m_LipUpper_001" -p "bpjnt_m_LipUpper_001";
	rename -uid "7E03EF34-4436-BEDE-5868-3B9878A3D885";
	setAttr -k on ".ro";
createNode nurbsCurve -n "bpctrl_m_LipUpper_001Shape" -p "bpctrl_m_LipUpper_001";
	rename -uid "24696CA5-423D-9B55-FF9D-C59D429D3D5E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.12779001478722882 0.30851238683516158 -8.903191544204156e-16
		1.5518998846414389e-16 0.33393140120398357 -8.9049553426426275e-16
		-0.12779001478722884 0.30851238683516158 -8.903191544204156e-16
		-0.23612515824247085 0.23612515824245861 -1.6384474210877257e-18
		-0.30851238683518623 0.12779001478722307 -8.8672135458727674e-19
		-0.33393140120399556 0 0
		-0.30851238683518611 -0.12779001478725149 8.8672135458747396e-19
		-0.23612515824247085 -0.23612515824248703 1.6384474210879229e-18
		-0.12779001478722879 -0.30851238683519 2.1407347202905685e-18
		1.0126448291014611e-16 -0.33393140120398357 2.3171145641375205e-18
		0.12779001478722907 -0.30851238683519 2.1407347202905685e-18
		0.23612515824247093 -0.23612515824248703 1.6384474210879229e-18
		0.3085123868351865 -0.12779001478725149 8.8672135458747396e-19
		0.33393140120399556 0 0
		0.30851238683518634 0.12779001478722307 -8.8672135458727674e-19
		0.23612515824247088 0.23612515824245861 -1.6384474210877257e-18
		0.12779001478722882 0.30851238683516158 -8.903191544204156e-16
		;
createNode transform -n "bpctrl_m_LipUpperDrv_001" -p "bpjnt_m_LipUpper_001";
	rename -uid "EDB40696-48D6-B8C2-8399-BB86F906F1CA";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	setAttr -k on ".ro";
	setAttr ".mnrl" -type "double3" 0 -45 -45 ;
	setAttr ".mrxe" yes;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'AlexBody_Rig:mesh_m_high_body_001.vtx[77]']";
createNode nurbsCurve -n "bpctrl_m_LipUpperDrv_001Shape" -p "bpctrl_m_LipUpperDrv_001";
	rename -uid "52575F8C-44E5-B953-3F2E-C08087193E78";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538243 0.56380601922538176 -3.9121901497892031e-18
		-0.56380601922538243 -0.56380601922538176 3.9121901497892031e-18
		0.56380601922538243 -0.56380601922538176 3.9121901497892031e-18
		0.56380601922538243 0.56380601922538176 -3.9121901497892031e-18
		-0.56380601922538243 0.56380601922538176 -3.9121901497892031e-18
		;
createNode joint -n "bpjnt_r_LipUpper_001" -p "LipUpper_Rig_Jnt";
	rename -uid "ADF2F5C2-4182-B928-0B39-E3B57CC6160F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.2784904257868466 156.4469451904296 7.1944564370411168 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2784904257868466 156.44694519042966 7.1944564370411204 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_r_LipUpper_001" -p "bpjnt_r_LipUpper_001";
	rename -uid "320F7AB5-462C-5DC3-B593-B291B69E700B";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 4.4408920985006271e-16 8.5265128291212048e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 4.4408920985006271e-16 8.5265128291212048e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_LipUpper_001Shape" -p "bpctrl_r_LipUpper_001";
	rename -uid "E851B16B-4FBF-E37B-BC92-FDBD7E98B64A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.12537497369340131 0.36503633290999243 -0.084519010495252997
		8.8749300880617203e-16 0.39511247956511397 5.3290705182007522e-15
		0.12537497369340531 0.36503633290999676 0.084519010495267208
		0.23166274416895247 0.27938671363194034 0.15617076780935532
		0.30268196187278412 0.15120299985026078 0.20404694141601024
		0.32762059470030064 -2.2731234536628857e-14 0.22085881788220643
		0.3026819618727839 -0.15120299985027871 0.20404694141601024
		0.23166274416895247 -0.27938671363198919 0.15617076780935532
		0.12537497369340553 -0.36503633291002086 0.084519010495267208
		1.1109084355191096e-15 -0.39511247956514239 5.3290705182007522e-15
		-0.12537497369340131 -0.36503633291002519 -0.084519010495252997
		-0.23166274416895113 -0.27938671363199719 -0.1561707678093571
		-0.30268196187278135 -0.1512029998502892 -0.20404694141600313
		-0.32762059470029964 -3.4112184324179149e-14 -0.22085881788220821
		-0.30268196187278135 0.15120299985025029 -0.20404694141600313
		-0.23166274416895113 0.27938671363193235 -0.1561707678093571
		-0.12537497369340131 0.36503633290999243 -0.084519010495252997
		;
createNode joint -n "bpjnt_r_LipUpper_002" -p "LipUpper_Rig_Jnt";
	rename -uid "F8649820-44FB-DAB7-A9AC-79BA2E1BFDD2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0112141839126387 156.30789184570307 6.6170124246571671 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0112141839126387 156.30789184570312 6.6170124246571671 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_r_LipUpper_002" -p "bpjnt_r_LipUpper_002";
	rename -uid "56F67CD2-4B44-820C-BF49-3686675A33E3";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 0 1.4210854715202007e-14 0 ;
	setAttr ".sp" -type "double3" 0 1.4210854715202007e-14 0 ;
createNode nurbsCurve -n "bpctrl_r_LipUpper_002Shape" -p "bpctrl_r_LipUpper_002";
	rename -uid "D398F9A9-435D-B6F1-12BE-C581CEDD7C3D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.11790648514078139 0.3650363329099946 -0.094659431254706605
		0 0.39511247956511397 5.3290705182007514e-15
		0.11790648514078228 0.3650363329099946 0.094659431254715487
		0.21786277674382903 0.27938671363193635 0.17490782219078041
		0.28465143551861738 0.15120299985025554 0.22852808274165412
		0.30810449360738468 0 0.24735701430734011
		0.28465143551861738 -0.15120299985028396 0.2285280827416559
		0.21786277674382903 -0.27938671363196477 0.17490782219078041
		0.11790648514078228 -0.3650363329099946 0.094659431254715487
		8.8817841970012523e-16 -0.39511247956514239 5.3290705182007514e-15
		-0.11790648514078139 -0.3650363329099946 -0.094659431254706605
		-0.21786277674382859 -0.27938671363196477 -0.17490782219077153
		-0.28465143551861694 -0.15120299985028396 -0.22852808274163991
		-0.30810449360738446 0 -0.24735701430734011
		-0.28465143551861694 0.15120299985025554 -0.22852808274163991
		-0.21786277674382859 0.27938671363193635 -0.17490782219077153
		-0.11790648514078139 0.3650363329099946 -0.094659431254706605
		;
createNode transform -n "LipLower_Rig" -p "Lip_Rig";
	rename -uid "CA11E217-4D79-5DE9-1E5B-47929498F07E";
createNode transform -n "LipLower_Rig_Jnt" -p "LipLower_Rig";
	rename -uid "C7E48FB3-4F99-F427-A309-55BA575AEE80";
createNode joint -n "bpjnt_r_LipLower_002" -p "LipLower_Rig_Jnt";
	rename -uid "3D40A5B7-4423-0DE5-713E-299A0165A065";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0099461078643799 155.54370117187494 6.4493708610534632 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0099461078643799 155.543701171875 6.4493708610534668 1;
	setAttr ".radi" 0.5;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'AlexBody_Rig:mesh_m_high_body_001.vtx[4138]']";
createNode transform -n "bpctrl_r_LipLower_002" -p "bpjnt_r_LipLower_002";
	rename -uid "B855828E-41E2-5387-20DE-0D9C35A0161E";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 0 0 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 0 0 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_LipLower_002Shape" -p "bpctrl_r_LipLower_002";
	rename -uid "BD3F30B1-4D19-81E7-492D-FAACB3C8A54F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.1092077023288045 0.36503633291002302 -0.10457545082753761
		-8.8817841970012523e-16 0.39511247956511397 -3.5527136788005009e-15
		0.10920770232880361 0.36503633291002302 0.10457545082752873
		0.20178952194833499 0.27938671363190792 0.19323023724539823
		0.26365071607780388 0.15120299985025554 0.25246747167911998
		0.28537347868411933 2.8421709430404007e-14 0.27326882217301574
		0.26365071607780388 -0.15120299985025554 0.25246747167911998
		0.20178952194833499 -0.27938671363193635 0.19323023724539645
		0.10920770232880361 -0.36503633291002302 0.10457545082752873
		-8.8817841970012523e-16 -0.39511247956514239 -3.5527136788005009e-15
		-0.1092077023288045 -0.36503633291002302 -0.10457545082753938
		-0.20178952194833633 -0.27938671363193635 -0.19323023724540356
		-0.26365071607780477 -0.15120299985025554 -0.25246747167912176
		-0.28537347868411933 2.8421709430404007e-14 -0.27326882217301751
		-0.26365071607780433 0.15120299985025554 -0.25246747167911998
		-0.20178952194833633 0.27938671363190792 -0.19323023724540356
		-0.1092077023288045 0.36503633291002302 -0.10457545082753761
		;
createNode joint -n "bpjnt_r_LipLower_001" -p "LipLower_Rig_Jnt";
	rename -uid "F9D92C14-427B-17AB-62C5-6BB43192C8E5";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.302908658981323 155.47799682617182 7.0618438720703089 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3029086589813232 155.47799682617188 7.0618438720703125 1;
	setAttr ".radi" 0.5;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'AlexBody_Rig:mesh_m_high_body_001.vtx[4140]']";
createNode transform -n "bpctrl_r_LipLower_001" -p "bpjnt_r_LipLower_001";
	rename -uid "682D5AAE-4811-8D7B-4C6C-FEA98AEE398E";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 4.4408920985006271e-16 2.8421709430404014e-14 0 ;
	setAttr ".sp" -type "double3" 4.4408920985006271e-16 2.8421709430404014e-14 0 ;
createNode nurbsCurve -n "bpctrl_r_LipLower_001Shape" -p "bpctrl_r_LipLower_001";
	rename -uid "D700F203-4535-F0F3-0631-F48555110A4F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.13226420120277013 0.36503633290996385 -0.073270241189121052
		-6.6613381477509383e-16 0.39511247956511392 -3.555455322376313e-15
		0.13226420120277124 0.3650363329099684 0.073270241189121052
		0.24439237675039058 0.27938671363194051 0.1353857523535886
		0.31931402836017603 0.15120299985023261 0.17689000999713042
		0.34562301374099763 -2.2455729072504173e-14 0.19146436713053203
		0.31931402836017603 -0.15120299985027841 0.17689000999713042
		0.2443923767503908 -0.27938671363196049 0.1353857523535886
		0.13226420120277124 -0.36503633291002069 0.073270241189121052
		-2.2204460492503128e-16 -0.39511247956514234 -3.5499720352246889e-15
		-0.13226420120277013 -0.36503633291002524 -0.073270241189121052
		-0.24439237675038947 -0.27938671363196893 -0.1353857523535886
		-0.31931402836017492 -0.15120299985028945 -0.17689000999712864
		-0.34562301374099763 -3.4387689788303842e-14 -0.19146436713053203
		-0.31931402836017492 0.15120299985022156 -0.17689000999712864
		-0.24439237675038947 0.27938671363193207 -0.1353857523535886
		-0.13226420120277013 0.36503633290996385 -0.073270241189121052
		;
createNode joint -n "bpjnt_m_LipLower_001" -p "LipLower_Rig_Jnt";
	rename -uid "C8C7BABA-40ED-8A59-CA28-E7A120B26083";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 3.7656041968136262e-05 155.40374755859369 7.3999061584472656 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.7656041968136262e-05 155.40374755859375 7.3999061584472656 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_m_LipLower_001" -p "bpjnt_m_LipLower_001";
	rename -uid "3805C5C0-44D3-5B5B-4E27-A6B5B6E6B39F";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" -1.3552527156068808e-20 1.4210854715202007e-14 0 ;
	setAttr ".sp" -type "double3" -1.3552527156068808e-20 1.4210854715202007e-14 0 ;
createNode nurbsCurve -n "bpctrl_m_LipLower_001Shape" -p "bpctrl_m_LipLower_001";
	rename -uid "1861D2D4-4917-DD64-AAB5-1FA21297B286";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.12779001478722882 0.30851238683519 -2.1407347202905685e-18
		1.5519676472772193e-16 0.33393140120398357 -2.3171145641375205e-18
		-0.12779001478722884 0.30851238683519 -2.1407347202905685e-18
		-0.23612515824247085 0.23612515824248703 -1.6384474210879229e-18
		-0.30851238683518623 0.12779001478722307 -8.8672135458727674e-19
		-0.33393140120399556 0 0
		-0.30851238683518611 -0.12779001478722307 8.8672135458727674e-19
		-0.23612515824247085 -0.23612515824245861 1.6384474210877257e-18
		-0.12779001478722879 -0.30851238683516158 2.1407347202903713e-18
		1.0127125917372415e-16 -0.33393140120398357 2.3171145641375205e-18
		0.12779001478722907 -0.30851238683516158 2.1407347202903713e-18
		0.23612515824247093 -0.23612515824245861 1.6384474210877257e-18
		0.3085123868351865 -0.12779001478722307 8.8672135458727674e-19
		0.33393140120399556 0 0
		0.30851238683518634 0.12779001478722307 -8.8672135458727674e-19
		0.23612515824247088 0.23612515824248703 -1.6384474210879229e-18
		0.12779001478722882 0.30851238683519 -2.1407347202905685e-18
		;
createNode transform -n "bpctrl_m_LipLowerDrv_001" -p "bpjnt_m_LipLower_001";
	rename -uid "7765B89A-4C0E-1484-9578-0BBE2E12AF44";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" -1.3552527156068808e-20 1.4210854715202007e-14 0 ;
	setAttr ".sp" -type "double3" -1.3552527156068808e-20 1.4210854715202007e-14 0 ;
	setAttr ".mnrl" -type "double3" 0 -45 -45 ;
	setAttr ".mrxe" yes;
createNode nurbsCurve -n "bpctrl_m_LipLowerDrv_001Shape" -p "bpctrl_m_LipLowerDrv_001";
	rename -uid "34996350-42FE-33FB-4E1A-CA9AA1B400D5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538243 0.56380601922538176 -3.9121901497892031e-18
		-0.56380601922538243 -0.56380601922538176 3.9121901497892031e-18
		0.56380601922538243 -0.56380601922538176 3.9121901497892031e-18
		0.56380601922538243 0.56380601922538176 -3.9121901497892031e-18
		-0.56380601922538243 0.56380601922538176 -3.9121901497892031e-18
		;
createNode joint -n "bpjnt_l_LipLower_001" -p "LipLower_Rig_Jnt";
	rename -uid "E7B8FF21-47F3-B72B-7502-CD8E5954855B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.94069212269050362 155.42042479830195 7.2707904760190143 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.94069212269050406 155.42042479830201 7.2707904760190143 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_l_LipLower_001" -p "bpjnt_l_LipLower_001";
	rename -uid "A5166E53-4625-CA32-4C58-D7BA9FE9C565";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 2.2204460492503136e-16 0 -3.5527136788005017e-15 ;
	setAttr ".sp" -type "double3" 2.2204460492503136e-16 0 -3.5527136788005017e-15 ;
createNode nurbsCurve -n "bpctrl_l_LipLower_001Shape" -p "bpctrl_l_LipLower_001";
	rename -uid "CBECEF20-4D3F-3039-5292-0B88A4E6E01C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.14032793695583212 0.36503633291002302 -0.056306458541089732
		-4.4374650440308611e-16 0.39511247956514239 -1.1546319456101628e-14
		-0.14032793695583279 0.36503633291002302 0.056306458541084403
		-0.25929221758605436 0.27938671363193635 0.10404076918860294
		-0.33878160857860795 0.15120299985025554 0.13593581585908243
		-0.36669457072799649 -2.8421709430404007e-14 0.14713586682626012
		-0.33878160857860795 -0.15120299985022712 0.13593581585908243
		-0.25929221758605436 -0.27938671363190792 0.10404076918860294
		-0.14032793695583279 -0.3650363329099946 0.056306458541084403
		-4.4443191529703912e-16 -0.39511247956511397 -9.7699626167013776e-15
		0.14032793695583301 -0.3650363329099946 -0.056306458541089732
		0.25929221758605703 -0.27938671363190792 -0.10404076918861538
		0.3387816085786115 -0.15120299985022712 -0.13593581585909131
		0.36669457072799627 -2.8421709430404007e-14 -0.1471358668262619
		0.33878160857861062 0.15120299985025554 -0.13593581585909131
		0.25929221758605703 0.27938671363193635 -0.10404076918861538
		0.14032793695583212 0.36503633291002302 -0.056306458541089732
		;
createNode joint -n "bpjnt_l_LipLower_002" -p "LipLower_Rig_Jnt";
	rename -uid "14980FA8-418A-9AA1-A20A-16B8A6644E9A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.7024061312595871 155.51350402832023 6.7740456670091582 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7024061312595884 155.51350402832028 6.7740456670091618 1;
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_l_LipLower_002" -p "bpjnt_l_LipLower_002";
	rename -uid "2E9AEE74-4A46-70AB-0C30-529A9E6824D6";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 5.6843418860808027e-14 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 5.6843418860808027e-14 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_LipLower_002Shape" -p "bpctrl_l_LipLower_002";
	rename -uid "8DD88FE0-4AFD-B399-AAE4-70B80651C75D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.11896662681051628 0.36503633290999454 -0.093323570811703505
		-4.4477462074401563e-16 0.39511247956514234 -1.7790984829760625e-15
		-0.11896662681051584 0.36503633290999454 0.093323570811698175
		-0.2198216631242893 0.27938671363193629 0.17243947394759829
		-0.2872108439157266 0.15120299985028393 0.22530303034269394
		-0.31087477729377699 2.8421709430404004e-14 0.24386624274517033
		-0.2872108439157266 -0.15120299985025551 0.22530303034269394
		-0.21982166312428841 -0.27938671363193629 0.17243947394759829
		-0.11896662681051584 -0.36503633290999454 0.093323570811698175
		-4.4340379895610956e-16 -0.39511247956514234 -1.7736151958244382e-15
		0.11896662681051628 -0.36503633290999454 -0.093323570811703505
		0.21982166312428708 -0.27938671363193629 -0.17243947394758941
		0.28721084391572349 -0.15120299985025551 -0.22530303034269394
		0.31087477729377699 2.8421709430404004e-14 -0.24386624274516855
		0.28721084391572349 0.15120299985028393 -0.22530303034269394
		0.21982166312428708 0.27938671363193629 -0.17243947394758941
		0.11896662681051628 0.36503633290999454 -0.093323570811703505
		;
createNode transform -n "LipLower_Rig_Crv" -p "LipLower_Rig";
	rename -uid "3AA234BD-4474-E20A-7EC1-58AD22A3B6E1";
createNode transform -n "crv_m_LipLower_001" -p "LipLower_Rig_Crv";
	rename -uid "9398B4CE-49CD-006C-A10E-F5ABDE53401E";
	setAttr ".rp" -type "double3" -0.15900719165802002 155.61898803710938 6.4662466049194336 ;
	setAttr ".sp" -type "double3" -0.15900719165802002 155.61898803710938 6.4662466049194336 ;
createNode nurbsCurve -n "crv_m_LipLower_00Shape1" -p "crv_m_LipLower_001";
	rename -uid "0793027E-4525-206B-BD89-08BBAFCF2854";
	setAttr -k off ".v";
createNode transform -n "crv_m_LipLowerAim_001" -p "LipLower_Rig_Crv";
	rename -uid "F670DA2E-4693-9440-49DE-C1ABDCF75E5C";
	setAttr ".rp" -type "double3" -0.15900719165802002 155.61898803710938 7.2744855697993351 ;
	setAttr ".sp" -type "double3" -0.15900719165802002 155.61898803710938 7.2744855697993351 ;
createNode nurbsCurve -n "crv_m_LipLowerAim_00Shape1" -p "crv_m_LipLowerAim_001";
	rename -uid "45091960-49A8-2489-EDB8-6DB90A50D43B";
	setAttr -k off ".v";
createNode transform -n "crv_m_LipLowerUp_001" -p "LipLower_Rig_Crv";
	rename -uid "2DA202FD-4084-CB59-19D5-3192B51E1B57";
	setAttr ".rp" -type "double3" -0.15900719165802002 156.19490706826434 6.4662466049194336 ;
	setAttr ".sp" -type "double3" -0.15900719165802002 156.19490706826434 6.4662466049194336 ;
createNode nurbsCurve -n "crv_m_LipLowerUp_00Shape1" -p "crv_m_LipLowerUp_001";
	rename -uid "D7E06A7F-4F4B-E584-E983-FE98EE16F62D";
	setAttr -k off ".v";
createNode transform -n "Lid_Rig" -p "Face_Rig";
	rename -uid "8A46C156-4032-6416-BA88-C7B1B849F71B";
createNode transform -n "l_Lid_Rig" -p "Lid_Rig";
	rename -uid "24CADB23-4590-90A9-2C9B-0BA858C1B4E6";
createNode transform -n "l_EyeLidUpper_Rig" -p "l_Lid_Rig";
	rename -uid "B3774E07-4507-5727-AABE-078469636956";
createNode transform -n "l_EyeLidUpper_Rig_Jnt" -p "l_EyeLidUpper_Rig";
	rename -uid "61F1D27A-4534-9283-3F0B-8D8E2E9337BC";
createNode joint -n "bpjnt_l_EyeLidUpperOut_001" -p "l_EyeLidUpper_Rig_Jnt";
	rename -uid "942677DB-463E-8052-5571-95BD3DDC64A1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.2444472312927228 163.43992614746094 4.2666106224060059 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.2444472312927246 163.43992614746094 4.2666106224060059 1;
createNode transform -n "bpctrl_l_EyeLidUpperOut_001" -p "bpjnt_l_EyeLidUpperOut_001";
	rename -uid "62134327-42A8-40FC-404B-FD86E4549C8E";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.7763568394002509e-15 -5.6843418860808027e-14 0 ;
	setAttr ".sp" -type "double3" -1.7763568394002509e-15 -5.6843418860808027e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidUpperOut_001Shape" -p "bpctrl_l_EyeLidUpperOut_001";
	rename -uid "E209EF08-4EA1-A8D5-03D4-CCA32BF34A47";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929152 0.24932472707459302 -2.6189838378436026e-17
		-8.8817841970012513e-16 0.2698671399255943 -1.8725794520944801e-18
		-0.10327368338929507 0.24932472707459491 2.272976272085419e-17
		-0.19082488466084019 0.19082488466074382 4.3871704565365097e-17
		-0.24932472707465875 0.10327368338923518 5.8334577087790834e-17
		-0.26986713992564038 2.4484339788451497e-15 6.3916539052858609e-17
		-0.24932472707465875 -0.10327368338934437 5.976778735199881e-17
		-0.19082488466084019 -0.19082488466093933 4.6519931823138924e-17
		-0.10327368338929507 -0.24932472707473513 2.6189838378437643e-17
		-8.8817841970012513e-16 -0.26986713992570799 1.8725794520954793e-18
		0.10327368338929152 -0.24932472707473702 -2.2729762720852572e-17
		0.19082488466083708 -0.19082488466091435 -4.387170456536339e-17
		0.24932472707465342 -0.10327368338934886 -5.8334577087788997e-17
		0.26986713992563593 -2.4484339788451174e-15 -6.3916539052857771e-17
		0.24932472707465342 0.10327368338923068 -5.9767787351996973e-17
		0.19082488466083708 0.19082488466074038 -4.651993182313702e-17
		0.10327368338929152 0.24932472707459302 -2.6189838378436026e-17
		;
createNode joint -n "bpjnt_l_EyeLidUpperInn_002" -p "l_EyeLidUpper_Rig_Jnt";
	rename -uid "BECA0836-42A6-37B6-4C35-79A15A15D001";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3968136310577384 163.18923950195307 4.6095156669616664 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3968136310577393 163.18923950195312 4.6095156669616699 1;
createNode transform -n "bpctrl_l_EyeLidUpperInn_002" -p "bpjnt_l_EyeLidUpperInn_002";
	rename -uid "E26665F5-4E99-1B84-4B55-E5BCD3AC1494";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 5.6843418860808027e-14 0 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 5.6843418860808027e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidUpperInn_002Shape" -p "bpctrl_l_EyeLidUpperInn_002";
	rename -uid "FCB35609-4E41-5843-03E7-E3881F189222";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929331 0.24932472707473513 8.8381914434538871e-16
		-4.4408920985006262e-16 0.26986713992570799 8.8724212997407745e-16
		-0.10327368338929287 0.24932472707473702 8.9080765722606924e-16
		-0.190824884660838 0.19082488466091435 8.9397290689883364e-16
		-0.24932472707465655 0.10327368338934888 8.9625599842275192e-16
		-0.26986713992563821 2.4446785335547895e-15 8.9730935180958391e-16
		-0.24932472707465655 -0.10327368338923067 8.9697260355485591e-16
		-0.190824884660838 -0.1908248846607688 8.9529702052772065e-16
		-0.10327368338929287 -0.24932472707459302 8.9253769505486106e-16
		-4.4408920985006262e-16 -0.2698671399255943 8.8911470942617243e-16
		0.10327368338929331 -0.24932472707459491 8.8554918217418044e-16
		0.19082488466083888 -0.19082488466077224 8.8238393250141604e-16
		0.24932472707465789 -0.10327368338923519 8.8010084097749785e-16
		0.2698671399256391 -2.4446785335548052e-15 8.7904748759066636e-16
		0.24932472707465789 0.10327368338934435 8.7938423584539386e-16
		0.19082488466083888 0.19082488466091091 8.8105981887252913e-16
		0.10327368338929331 0.24932472707473513 8.8381914434538871e-16
		;
createNode joint -n "bpjnt_l_EyeLidUpperOut_002" -p "l_EyeLidUpper_Rig_Jnt";
	rename -uid "53909B4C-4C6D-4AA4-F7EA-17A741B42AD5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.7992749214172346 163.73420715332026 4.8013381958007795 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.7992749214172363 163.73420715332031 4.8013381958007812 1;
createNode transform -n "bpctrl_l_EyeLidUpperOut_002" -p "bpjnt_l_EyeLidUpperOut_002";
	rename -uid "DFEE1357-424E-F876-FC12-8AB01166C4E3";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 -5.6843418860808027e-14 0 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 -5.6843418860808027e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidUpperOut_002Shape" -p "bpctrl_l_EyeLidUpperOut_002";
	rename -uid "B123EEF4-4E65-CCD6-1AAC-D4A218B35AD1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929338 0.24932472707459488 2.6660289822227149e-17
		4.4315292012401532e-16 0.26986713992559425 -9.3628972604729265e-19
		-0.1032736833892916 0.24932472707459299 -2.8390327651018145e-17
		-0.19082488466083636 0.19082488466076877 -5.1522195550082862e-17
		-0.24932472707465492 0.10327368338923064 -6.6810276226512943e-17
		-0.26986713992563705 2.5968866935041164e-14 -7.1927097984119029e-17
		-0.24932472707465492 -0.10327368338932046 -6.6093671094409054e-17
		-0.19082488466083636 -0.19082488466091432 -5.0198081921195948e-17
		-0.1032736833892916 -0.24932472707470857 -2.6660289822226517e-17
		4.450254995761102e-16 -0.26986713992567951 9.3628972604758847e-19
		0.10327368338929516 -0.24932472707470668 2.8390327651019248e-17
		0.19082488466083991 -0.19082488466091088 5.1522195550084058e-17
		0.24932472707465891 -0.1032736833893159 6.6810276226514065e-17
		0.2698671399256406 3.0874551925766863e-14 7.1927097984119547e-17
		0.24932472707465891 0.10327368338923519 6.6093671094410175e-17
		0.19082488466083991 0.19082488466077221 5.0198081921197144e-17
		0.10327368338929338 0.24932472707459488 2.6660289822227149e-17
		;
createNode joint -n "bpjnt_l_EyeLidUpperInn_001" -p "l_EyeLidUpper_Rig_Jnt";
	rename -uid "E7150B6A-43A5-94C6-7F0E-4182D155E987";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.8170521259307844 163.74273681640619 4.7976574897766113 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.8170521259307861 163.74273681640625 4.7976574897766113 1;
createNode transform -n "bpctrl_l_EyeLidUpperInn_001" -p "bpjnt_l_EyeLidUpperInn_001";
	rename -uid "CBFA7E4C-460F-B45C-8024-AD9C8CB2D79B";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.3322676295501882e-15 5.6843418860808027e-14 0 ;
	setAttr ".sp" -type "double3" 1.3322676295501882e-15 5.6843418860808027e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidUpperInn_001Shape" -p "bpctrl_l_EyeLidUpperInn_001";
	rename -uid "5C61C527-49B0-B397-36B4-BA89A6C49F7D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929377 0.24932472707476544 2.8369226748405725e-17
		4.450254995761104e-16 0.26986713992573641 9.3628972604790394e-19
		-0.10327368338929244 0.24932472707476355 -2.6639188919612951e-17
		-0.19082488466083736 0.19082488466096775 -5.0159092537111698e-17
		-0.24932472707465658 0.10327368338937278 -6.6042729009141422e-17
		-0.26986713992563827 2.5968739155266537e-14 -7.1871958668358581e-17
		-0.24932472707465614 -0.10327368338917835 -6.6759334141245201e-17
		-0.19082488466083736 -0.1908248846607154 -5.1483206165998611e-17
		-0.10327368338929244 -0.24932472707453807 -2.8369226748404579e-17
		4.4315292012401552e-16 -0.26986713992553746 -9.3628972604697718e-19
		0.10327368338929377 -0.24932472707453618 2.6639188919614097e-17
		0.19082488466083891 -0.19082488466071196 5.0159092537112998e-17
		0.24932472707465747 -0.10327368338917382 6.6042729009142347e-17
		0.26986713992563915 3.0874679705541488e-14 7.1871958668359024e-17
		0.24932472707465747 0.1032736833893773 6.6759334141246236e-17
		0.19082488466083891 0.19082488466097119 5.1483206165999912e-17
		0.10327368338929377 0.24932472707476544 2.8369226748405725e-17
		;
createNode joint -n "bpjnt_l_EyeLidUpperMid_001" -p "l_EyeLidUpper_Rig_Jnt";
	rename -uid "099F48DD-44D2-32E0-6780-92BFC66EB70A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.6759846210479719 164.07983398437494 4.9178810119628906 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.6759846210479736 164.079833984375 4.9178810119628906 1;
createNode transform -n "bpctrl_l_EyeLidUpperMid_001" -p "bpjnt_l_EyeLidUpperMid_001";
	rename -uid "AC23ECEB-4D03-77B3-6C6A-C19455E98FEE";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -4.4408920985006271e-16 -2.8421709430404014e-14 0 ;
	setAttr ".sp" -type "double3" -4.4408920985006271e-16 -2.8421709430404014e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidUpperMid_001Shape" -p "bpctrl_l_EyeLidUpperMid_001";
	rename -uid "95CD0BAA-4793-7092-8C18-45934769EC20";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929155 0.24932472707453712 0
		-4.4408920985006262e-16 0.26986713992553746 0
		-0.10327368338929555 0.24932472707453712 0
		-0.19082488466083936 0.19082488466071368 0
		-0.2493247270746588 0.10327368338917609 0
		-0.26986713992564049 -5.6843418860808015e-14 0
		-0.2493247270746588 -0.10327368338940346 0
		-0.19082488466083936 -0.19082488466096947 0
		-0.10327368338929555 -0.2493247270747645 0
		-4.4408920985006262e-16 -0.26986713992573641 0
		0.10327368338929155 -0.2493247270747645 0
		0.19082488466083625 -0.19082488466096947 0
		0.24932472707465569 -0.10327368338940346 0
		0.26986713992563693 -5.6843418860808015e-14 0
		0.24932472707465436 0.10327368338917609 0
		0.19082488466083625 0.19082488466071368 0
		0.10327368338929155 0.24932472707453712 0
		;
createNode transform -n "bpctrl_l_EyeLidUpperMidDrv_001" -p "bpjnt_l_EyeLidUpperMid_001";
	rename -uid "5A535C5C-43C1-64D4-9282-D08B12E9A16A";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 2.8421709430404014e-14 0 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 2.8421709430404014e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidUpperMidDrv_001Shape" -p "bpctrl_l_EyeLidUpperMidDrv_001";
	rename -uid "D48DBBF1-4DF1-2D37-6C40-288F1FE67DC1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538309 0.56380601922535334 0
		-0.56380601922538309 -0.56380601922541018 0
		0.5638060192253822 -0.56380601922541018 0
		0.5638060192253822 0.56380601922535334 0
		-0.56380601922538309 0.56380601922535334 0
		;
createNode transform -n "l_EyeLidUpper_Rig_Crv" -p "l_EyeLidUpper_Rig";
	rename -uid "A6395B18-4BBF-5D71-D1D5-D2AE1D2437FB";
createNode transform -n "crv_l_EyeLidUpper_001" -p "l_EyeLidUpper_Rig_Crv";
	rename -uid "0C15FC0A-486B-6FDD-BC59-2E86F86F9978";
	setAttr ".rp" -type "double3" 3.7658772468566895 163.35515594482422 4.5256017294535935 ;
	setAttr ".sp" -type "double3" 3.7658772468566895 163.35515594482422 4.5256017294535935 ;
createNode nurbsCurve -n "crv_l_EyeLidUpper_00Shape1" -p "crv_l_EyeLidUpper_001";
	rename -uid "D23B926E-4AB7-239E-47D1-728777C659D1";
	setAttr -k off ".v";
	setAttr ".iog[0].og[0].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		2.1721820831298828 162.75773620605469 4.5605368614196777
		2.206670158772063 162.86480024277944 4.5663908847974986
		2.3117871476598428 163.02119503176579 4.5728718629861262
		2.4222935019992455 163.18974099409436 4.6087236920564409
		2.5698473865948785 163.37314714326234 4.6721338392438261
		2.7622158636973171 163.59319278268242 4.743097530708229
		3.0022528928910233 163.77136393295169 4.8296972276509935
		3.3442293186732477 163.90158534496925 4.9124028378744722
		3.7394161224365234 163.95257568359375 4.9050545692443848
		4.0871920585632324 163.91777038574219 4.858954906463623
		4.3557381629943848 163.86093139648438 4.8122949600219727
		4.6387801170349121 163.76695251464844 4.7445740699768066
		4.9389419555664062 163.61737060546875 4.5841851234436035
		5.1842331886291504 163.42143249511719 4.3546099662780762
		5.2726311683654785 163.3370361328125 4.2660331726074219
		5.3279886245727539 163.24891662597656 4.1809878349304199
		5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode transform -n "crv_l_EyeLidUpperDrv_001" -p "l_EyeLidUpper_Rig_Crv";
	rename -uid "67C8AE3C-4238-897C-C680-71A2AF265E53";
	setAttr ".rp" -type "double3" 3.7658772468566881 163.41878159650105 4.5283408944231329 ;
	setAttr ".sp" -type "double3" 3.7658772468566881 163.41878159650105 4.5283408944231329 ;
createNode nurbsCurve -n "crv_l_EyeLidUpperDrv_00Shape1" -p "crv_l_EyeLidUpperDrv_001";
	rename -uid "0E20FCD5-4F71-55F4-7AA0-75BFFAC36C20";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 0 no 3
		9 0 0 0 0.25 0.5 0.75 1 1 1
		7
		2.1721820831298846 162.75773620605472 4.5605368614196653
		2.3968137309617403 163.1892424550708 4.6095155124476435
		2.8170521286198684 163.74273515598722 4.7976574315613965
		3.6759845220744594 164.07982698694735 4.9178811678135625
		4.7992747218179987 163.73421389596032 4.801338107528875
		5.244447223638919 163.43992486230496 4.2666104539843888
		5.3595724105834917 163.14787292480474 4.1388006210327024
		;
	setAttr ".dcv" yes;
createNode transform -n "crv_l_EyeLidUpperBlink_001" -p "l_EyeLidUpper_Rig_Crv";
	rename -uid "2BDA165B-45EA-8A71-073F-988E76CE0D7D";
	setAttr ".rp" -type "double3" 3.7658772468566895 162.95326062519632 4.5115892847477213 ;
	setAttr ".sp" -type "double3" 3.7658772468566895 162.95326062519632 4.5115892847477213 ;
createNode nurbsCurve -n "crv_l_EyeLidUpperBlink_00Shape1" -p "crv_l_EyeLidUpperBlink_001";
	rename -uid "6B6876B3-42D1-A415-94E7-2E89C5EF2B99";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		2.1721820831298828 162.75773620605469 4.5605368614196777
		2.2384514998510716 162.78019624149158 4.5781895235999928
		2.3523599581133516 162.82140699712971 4.6131084490753107
		2.4813635669441827 162.87087008795609 4.6581216446153739
		2.643823773372969 162.93405886444981 4.7185775020627405
		2.8638729974731221 163.0121541725189 4.7942410117618035
		3.1193556215856395 163.07876963094947 4.8531915124855196
		3.4647710010542867 163.12931277369566 4.8843779484627285
		3.8541678129525723 163.14878504433793 4.8765547970664791
		4.1869313398581856 163.14493462471023 4.8431110456003577
		4.4356389947332486 163.13548289866418 4.7936708378512112
		4.688305284833949 163.12392896027899 4.7077357224295211
		4.9569419046738004 163.11482926245395 4.5478059130567052
		5.1884501880420126 163.11899564758997 4.3367605567683762
		5.2625678500868611 163.12651731206194 4.2547519788427461
		5.3188223525866523 163.13657246592467 4.1884009104876849
		5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode transform -n "l_EyeLidlower_Rig" -p "l_Lid_Rig";
	rename -uid "EBBE9B28-4C86-B674-59D7-D781C5E2A6A4";
createNode transform -n "l_EyeLidlower_Rig_Crv" -p "l_EyeLidlower_Rig";
	rename -uid "8F750C6F-4998-4859-F713-B399A9D5AAA0";
createNode transform -n "crv_l_EyeLidLower_001" -p "l_EyeLidlower_Rig_Crv";
	rename -uid "30716D80-4245-7015-2B00-45BA0C34D167";
	setAttr ".rp" -type "double3" 3.7658772468566895 162.73293304443359 4.5230139292509861 ;
	setAttr ".sp" -type "double3" 3.7658772468566895 162.73293304443359 4.5230139292509861 ;
createNode nurbsCurve -n "crv_l_EyeLidLower_00Shape1" -p "crv_l_EyeLidLower_001";
	rename -uid "5CC3B2F2-4F27-B7AD-083E-089277AA8E03";
	setAttr -k off ".v";
	setAttr ".iog[0].og[3].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		2.1721820831298828 162.75773620605469 4.5605368614196777
		2.2656403967015661 162.65984752553507 4.5770560003926217
		2.3887053193486878 162.61072064626359 4.6106776745736209
		2.5454270493641942 162.5591980960954 4.6734502761596959
		2.7121646809777227 162.49975621608991 4.7429727153736865
		2.9058608894695888 162.4344064730916 4.8240065193238468
		3.1372599710510882 162.38492605146544 4.8894676258767333
		3.4944369369747217 162.34174105838022 4.9072272374692565
		3.8972983360290527 162.3179931640625 4.8827762603759766
		4.3056414475481475 162.36732197945327 4.8439170585899802
		4.6718058906101145 162.45000934803591 4.7234135738051126
		4.9196012394268624 162.55215427548436 4.5800197947451418
		5.0680840332920001 162.65366037060659 4.4693815061212581
		5.1984634083086014 162.80438314241903 4.3423288063621603
		5.2833304501297373 162.93285034001295 4.2546177513142451
		5.3336207284930994 163.03810125308991 4.1787492332310547
		5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode transform -n "crv_l_EyeLidLowerDrv_001" -p "l_EyeLidlower_Rig_Crv";
	rename -uid "1B6B84DD-46E9-C232-C653-B9A3FEB62263";
	setAttr ".rp" -type "double3" 3.7658772468566855 162.70931481601647 4.5459143230986498 ;
	setAttr ".sp" -type "double3" 3.7658772468566855 162.70931481601647 4.5459143230986498 ;
createNode nurbsCurve -n "crv_l_EyeLidLowerDrv_00Shape1" -p "crv_l_EyeLidLowerDrv_001";
	rename -uid "DD1CF4AC-4441-BC71-FDC2-0F9DFDAD512E";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 0 no 3
		9 0 0 0 0.25 0.5 0.75 1 1 1
		7
		2.1721820831298775 162.75773620605474 4.5605368614196653
		2.5308225213331101 162.51839325688644 4.6575676305668763
		3.0335223969012266 162.41939679033899 4.9530280251645982
		3.9433993245172432 162.27075670722823 4.8954465372680955
		4.8956294499128612 162.48381295267876 4.7268503781361595
		5.2496076289899944 162.77993590960438 4.2865539034104501
		5.3595724105834934 163.14787292480472 4.1388006210327015
		;
	setAttr ".dcv" yes;
createNode transform -n "crv_l_EyeLidLowerBlink_001" -p "l_EyeLidlower_Rig_Crv";
	rename -uid "2BFBF1A4-42C9-09F8-57F8-57BE74351A6B";
	setAttr ".rp" -type "double3" 3.7658772468566895 162.95280456542969 4.5097262039587012 ;
	setAttr ".sp" -type "double3" 3.7658772468566895 162.95280456542969 4.5097262039587012 ;
createNode nurbsCurve -n "crv_l_EyeLidLowerBlink_00Shape1" -p "crv_l_EyeLidLowerBlink_001";
	rename -uid "0EE37DEA-4A69-C422-4C45-2CA89B47D1D5";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		2.1721820831298828 162.75773620605469 4.5605368614196777
		2.2599220983481998 162.78772911746958 4.5843497649329139
		2.3535221171326444 162.82184180906623 4.6134912476451939
		2.4818542220289039 162.8710614435638 4.6583006968895688
		2.6308800388034936 162.92909900748671 4.713762205934791
		2.8146242881256556 162.99601042946523 4.7787904055236163
		3.0350778412811219 163.06000781866447 4.837768399452635
		3.3777331079130595 163.1200586835719 4.8806517868846866
		3.7804492493148838 163.147474614652 4.8805782065044321
		4.2042604177277063 163.1444074334232 4.8404849822515139
		4.5998269686069708 163.12796106787894 4.7431874717881515
		4.8758437936496568 163.11673551310818 4.6054577101681007
		5.0381195560516323 163.11420779363579 4.4816922807668726
		5.1855220375168249 163.11879129043575 4.3398613953378486
		5.2711433542828221 163.12774933696176 4.2448459346814458
		5.3234269060121662 163.13764081512005 4.1828430045791558
		5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode transform -n "l_EyeLidlower_Rig_Jnt" -p "l_EyeLidlower_Rig";
	rename -uid "B33185D1-4F43-888E-CAA0-B486A708A5EB";
createNode joint -n "bpjnt_l_EyeLidLowerInn_001" -p "l_EyeLidlower_Rig_Jnt";
	rename -uid "129A7BCA-4E67-DAE6-98DC-D29A1801CA8B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 3.0335223674774152 162.41940307617182 4.9530282020568812 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.033522367477417 162.41940307617188 4.9530282020568848 1;
createNode transform -n "bpctrl_l_EyeLidLowerInn_001" -p "bpjnt_l_EyeLidLowerInn_001";
	rename -uid "9E6498B0-4749-F2EC-62D3-D2B5C4C884AC";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 2.2204460492503135e-15 -5.6843418860808027e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 2.2204460492503135e-15 -5.6843418860808027e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidLowerInn_001Shape" -p "bpctrl_l_EyeLidLowerInn_001";
	rename -uid "771984E1-436C-98A2-5C02-DBA9652F425F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929466 0.24932472707459397 -2.3796383141724317e-17
		0 0.2698671399255943 -9.3628972604729265e-19
		-0.10327368338929244 0.24932472707459397 2.2066345312932591e-17
		-0.19082488466083714 0.1908248846607421 4.1709579309937137e-17
		-0.24932472707465569 0.10327368338923293 5.5002907955281384e-17
		-0.26986713992563738 0 5.9922542467036295e-17
		-0.24932472707465569 -0.10327368338934662 5.5719513087385372e-17
		-0.19082488466083714 -0.19082488466091263 4.3033692938823952e-17
		-0.10327368338929244 -0.24932472707470765 2.3796383141724219e-17
		0 -0.26986713992570799 9.3628972604768708e-19
		0.10327368338929466 -0.24932472707470765 -2.2066345312932689e-17
		0.19082488466083847 -0.19082488466091263 -4.1709579309936841e-17
		0.24932472707465836 -0.10327368338934662 -5.5002907955281581e-17
		0.26986713992564004 0 -5.9922542467036886e-17
		0.24932472707465836 0.10327368338923293 -5.5719513087385569e-17
		0.19082488466083847 0.1908248846607421 -4.3033692938823656e-17
		0.10327368338929466 0.24932472707459397 -2.3796383141724317e-17
		;
createNode joint -n "bpjnt_l_EyeLidLowerInn_002" -p "l_EyeLidlower_Rig_Jnt";
	rename -uid "C2623929-4308-DA3A-A65E-5895FD53F5F9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.53082251548767 162.51838684082026 4.6575675010681117 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.5308225154876709 162.51838684082031 4.6575675010681152 1;
createNode transform -n "bpctrl_l_EyeLidLowerInn_002" -p "bpjnt_l_EyeLidLowerInn_002";
	rename -uid "692DA685-4A43-F25B-DFF0-278F051D68F0";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.3322676295501882e-15 0 8.8817841970012543e-16 ;
	setAttr ".sp" -type "double3" 1.3322676295501882e-15 0 8.8817841970012543e-16 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidLowerInn_002Shape" -p "bpctrl_l_EyeLidLowerInn_002";
	rename -uid "43C3FCAB-46A9-1E8A-A564-199E8AC51394";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929466 0.24932472707456554 -9.323111103259914e-16
		0 0.26986713992553746 -8.8630584024803075e-16
		-0.10327368338929244 0.24932472707456554 -8.4058565341667749e-16
		-0.19082488466083714 0.19082488466071368 -8.0211103382247841e-16
		-0.24932472707465658 0.10327368338920451 -7.7673939352535478e-16
		-0.26986713992563782 -5.6843418860808015e-14 -7.6833333476605254e-16
		-0.24932472707465614 -0.10327368338937504 1.1000581591056227e-16
		-0.19082488466083714 -0.19082488466096947 8.3419158619872992e-17
		-0.10327368338929244 -0.2493247270747645 4.4132690625864294e-17
		-4.4408920985006262e-16 -0.26986713992573641 -1.8725794520950783e-18
		0.10327368338929466 -0.2493247270747645 -4.7592766283449522e-17
		0.19082488466083847 -0.19082488466096947 -8.6067385877648594e-17
		0.24932472707465791 -0.10327368338937504 -1.1143902617477163e-16
		0.2698671399256396 -5.6843418860808015e-14 -1.0080235046341988e-15
		0.24932472707465791 0.10327368338920451 -9.9818423561068879e-16
		0.19082488466083847 0.19082488466071368 -9.715975783199999e-16
		0.10327368338929466 0.24932472707456554 -9.323111103259914e-16
		;
createNode joint -n "bpjnt_l_EyeLidLowerOut_001" -p "l_EyeLidlower_Rig_Jnt";
	rename -uid "8BF1AE64-4B56-BD48-DBB3-80858F288068";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.8956294059753418 162.48381042480463 4.7268505096435547 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.8956294059753418 162.48381042480469 4.7268505096435547 1;
createNode transform -n "bpctrl_l_EyeLidLowerOut_001" -p "bpjnt_l_EyeLidLowerOut_001";
	rename -uid "0323E470-4B3A-8998-AC4D-EBA5F853EE86";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.7763568394002509e-15 5.6843418860808027e-14 0 ;
	setAttr ".sp" -type "double3" 1.7763568394002509e-15 5.6843418860808027e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidLowerOut_001Shape" -p "bpctrl_l_EyeLidLowerOut_001";
	rename -uid "03C0E9B2-4EA6-4B2D-BE06-D790BF6B239B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929602 0.24932472707476497 8.8939686000766121e-16
		8.8817841970012523e-16 0.26986713992573641 8.8724212997407755e-16
		-0.10327368338929158 0.24932472707476402 8.8522994156379723e-16
		-0.1908248846608363 0.19082488466096861 8.8366663222175183e-16
		-0.24932472707465531 0.10327368338937391 8.8279020162383365e-16
		-0.2698671399256361 2.720465405160573e-14 8.8273407838371236e-16
		-0.24932472707465531 -0.10327368338917721 8.8350680675593754e-16
		-0.1908248846608363 -0.19082488466071454 8.8499074585063875e-16
		-0.10327368338929158 -0.24932472707453759 8.8695997939258886e-16
		8.8817841970012523e-16 -0.26986713992553746 8.8911470942617243e-16
		0.10327368338929602 -0.24932472707453665 8.9112689783645284e-16
		0.19082488466084074 -0.19082488466071282 8.9269020717849804e-16
		0.24932472707465975 -0.10327368338917496 8.9356663777641633e-16
		0.26986713992564143 2.9638764809202298e-14 8.936227610165382e-16
		0.24932472707465886 0.10327368338937616 8.9285003264431253e-16
		0.19082488466084074 0.19082488466097033 8.9136609354961103e-16
		0.10327368338929602 0.24932472707476497 8.8939686000766121e-16
		;
createNode joint -n "bpjnt_l_EyeLidLowerOut_002" -p "l_EyeLidlower_Rig_Jnt";
	rename -uid "CC2CBD39-4F3D-E258-26F3-EEAF141EF4DA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.2496075630187971 162.77993774414062 4.2865538597106934 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.2496075630187988 162.77993774414062 4.2865538597106934 1;
createNode transform -n "bpctrl_l_EyeLidLowerOut_002" -p "bpjnt_l_EyeLidLowerOut_002";
	rename -uid "68229519-4F03-67A9-D24F-6780D3F3186D";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 3.5527136788005017e-15 0 0 ;
	setAttr ".sp" -type "double3" 3.5527136788005017e-15 0 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidLowerOut_002Shape" -p "bpctrl_l_EyeLidLowerOut_002";
	rename -uid "7AB297F1-49E3-3D36-01AA-E2B9E4E5D1C9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929509 0.24932472707467876 -1.7771782232662223e-15
		0 0.26986713992565114 -1.7763568394002505e-15
		-0.10327368338929065 0.2493247270746797 -1.7755354555342788e-15
		-0.19082488466083622 0.19082488466085665 -1.7748391199160382e-15
		-0.24932472707465522 0.10327368338931932 -1.7743738433311073e-15
		-0.26986713992563688 1.2192734665318465e-15 -1.7742104599217994e-15
		-0.24932472707465522 -0.10327368338928865 -1.7743738433311073e-15
		-0.19082488466083622 -0.19082488466079808 1.517719484212263e-18
		-0.10327368338929065 -0.24932472707465034 8.2138386597155636e-19
		0 -0.26986713992562272 0
		0.10327368338929509 -0.24932472707465128 -8.2138386597155636e-19
		0.19082488466083977 -0.1908248846607998 -1.517719484212263e-18
		0.24932472707465878 -0.1032736833892909 -1.7783398354693936e-15
		0.26986713992564043 -1.2192734665318627e-15 -1.7785032188787011e-15
		0.24932472707465789 0.10327368338931707 -1.7783398354693936e-15
		0.19082488466083977 0.19082488466085493 -1.7778745588844629e-15
		0.10327368338929509 0.24932472707467876 -1.7771782232662223e-15
		;
createNode joint -n "bpjnt_l_EyeLidLowerMid_001" -p "l_EyeLidlower_Rig_Jnt";
	rename -uid "44A447D2-4843-123A-4E6E-5293862518A6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 3.9433994293212873 162.27075195312494 4.8954463005065918 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.9433994293212891 162.270751953125 4.8954463005065918 1;
createNode transform -n "bpctrl_l_EyeLidLowerMid_001" -p "bpjnt_l_EyeLidLowerMid_001";
	rename -uid "FBDEBDA4-412B-CCA5-62A0-E9BE77A4B24A";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 -2.8421709430404014e-14 0 ;
	setAttr ".sp" -type "double3" 0 -2.8421709430404014e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidLowerMid_001Shape" -p "bpctrl_l_EyeLidLowerMid_001";
	rename -uid "DC2973A2-4AFB-0BDC-19BB-5DAF5C55197E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.1032736833892911 0.24932472707459394 -9.8800206147065199e-32
		-4.4502549957610991e-16 0.2698671399255374 -9.8800206147065199e-32
		-0.10327368338929421 0.24932472707459394 -9.8800206147065199e-32
		-0.19082488466083936 0.19082488466074207 -9.8703909649845837e-32
		-0.24932472707465836 0.10327368338923291 -9.8703909649845837e-32
		-0.26986713992564004 -8.5265128291212022e-14 -9.8607613152626476e-32
		-0.24932472707465791 -0.10327368338937502 -9.8559464904016795e-32
		-0.19082488466083936 -0.19082488466094102 -9.8511316655407114e-32
		-0.10327368338929421 -0.24932472707476447 -9.8511316655407114e-32
		-4.4315292012401513e-16 -0.26986713992570793 -9.8415020158187752e-32
		0.1032736833892911 -0.24932472707476447 -9.8511316655407114e-32
		0.19082488466083669 -0.19082488466094102 -9.8511316655407114e-32
		0.24932472707465658 -0.10327368338937502 -9.8559464904016795e-32
		0.26986713992563738 -8.5265128291212022e-14 -9.8607613152626476e-32
		0.24932472707465569 0.10327368338923291 -9.8703909649845837e-32
		0.19082488466083669 0.19082488466074207 -9.8703909649845837e-32
		0.1032736833892911 0.24932472707459394 -9.8800206147065199e-32
		;
createNode transform -n "bpctrl_l_EyeLidLowerMidDrv_001" -p "bpjnt_l_EyeLidLowerMid_001";
	rename -uid "5EC215ED-4AF5-67B9-6941-BC807BF1FD22";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.3322676295501882e-15 0 0 ;
	setAttr ".sp" -type "double3" 1.3322676295501882e-15 0 0 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidLowerMidDrv_001Shape" -p "bpctrl_l_EyeLidLowerMidDrv_001";
	rename -uid "982B2804-470F-CAC6-3105-AEB74B336444";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538309 -0.56380601922543849 -9.8222427163749029e-32
		-0.56380601922538309 0.56380601922532481 -9.8992799141503923e-32
		0.5638060192253822 0.56380601922532481 -9.8992799141503923e-32
		0.5638060192253822 -0.56380601922543849 -9.8222427163749029e-32
		-0.56380601922538309 -0.56380601922543849 -9.8222427163749029e-32
		;
createNode transform -n "crv_l_EyeLidBlink_001" -p "l_Lid_Rig";
	rename -uid "B23FF00A-44AD-4785-C672-759ECB187558";
	setAttr ".rp" -type "double3" 3.7658772468566881 162.96651402657125 4.5227322367867719 ;
	setAttr ".sp" -type "double3" 3.7658772468566881 162.96651402657125 4.5227322367867719 ;
createNode nurbsCurve -n "crv_l_EyeLidBlink_00Shape1" -p "crv_l_EyeLidBlink_001";
	rename -uid "BF66D14D-44C9-D98E-61D8-BD843F29E62A";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 0 no 3
		9 0 0 0 0.25 0.5 0.75 1 1 1
		7
		2.1721820831298846 162.75773620605469 4.5605368614196777
		2.4638181261474248 162.8538178559786 4.6335415715072594
		2.9252872627605475 163.08106597316311 4.8753427283629973
		3.8096919232958513 163.17529184708781 4.906663852540829
		4.84745208586543 163.10901342431953 4.7640942428325177
		5.2470274263144567 163.10993038595467 4.2765821786974199
		5.3595724105834917 163.14787292480472 4.1388006210327148
		;
createNode joint -n "bpjnt_l_EyeLidCornerOut_001" -p "l_Lid_Rig";
	rename -uid "B59A42C5-4C7C-924D-49FF-55AAA52F0D09";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.3595724105834952 163.14787292480469 4.1388006210327113 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.3595724105834961 163.14787292480469 4.1388006210327148 1;
createNode transform -n "bpctrl_l_EyeLidCornerOut_001" -p "bpjnt_l_EyeLidCornerOut_001";
	rename -uid "0B9B41F9-4521-10AE-8D48-0BB76C1D7199";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 -5.6843418860808027e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 -5.6843418860808027e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidCornerOut_001Shape" -p "bpctrl_l_EyeLidCornerOut_001";
	rename -uid "A409DD0E-445D-9D54-215B-79BD8DF8BA0D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.1032736833892942 0.24932472707467923 0
		-8.8817841970012523e-16 0.26986713992562272 0
		-0.10327368338929331 0.24932472707467923 0
		-0.190824884660838 0.19082488466085579 0
		-0.249324727074657 0.10327368338928977 0
		-0.26986713992563777 -2.8421709430404007e-14 0
		-0.249324727074657 -0.10327368338931819 0
		-0.190824884660838 -0.19082488466082737 0
		-0.10327368338929331 -0.24932472707467923 0
		-8.8817841970012523e-16 -0.26986713992562272 0
		0.1032736833892942 -0.24932472707467923 0
		0.19082488466083888 -0.19082488466082737 0
		0.24932472707465789 -0.10327368338931819 0
		0.26986713992563865 -2.8421709430404007e-14 0
		0.249324727074657 0.10327368338928977 0
		0.19082488466083888 0.19082488466085579 0
		0.1032736833892942 0.24932472707467923 0
		;
createNode transform -n "bpctrl_l_EyeLidCornerOutDrv_001" -p "bpjnt_l_EyeLidCornerOut_001";
	rename -uid "5E58FE44-484C-4BF9-8E93-BABF42820B1E";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 -5.6843418860808027e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 0 -5.6843418860808027e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidCornerOutDrv_001Shape" -p "bpctrl_l_EyeLidCornerOutDrv_001";
	rename -uid "39C88CFC-4886-085B-9745-C68D0BD7E049";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538254 0.56380601922538176 0
		-0.56380601922538254 -0.56380601922538176 0
		0.56380601922538165 -0.56380601922538176 0
		0.56380601922538165 0.56380601922538176 0
		-0.56380601922538254 0.56380601922538176 0
		;
createNode joint -n "bpjnt_l_EyeLidCornerInn_001" -p "l_Lid_Rig";
	rename -uid "44BD977E-4727-A9D8-6EA5-F0991490904A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 2.1721820831298819 162.75773620605463 4.5605368614196777 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1721820831298828 162.75773620605469 4.5605368614196777 1;
createNode transform -n "bpctrl_l_EyeLidCornerInn_001" -p "bpjnt_l_EyeLidCornerInn_001";
	rename -uid "C3ED8CB0-49C3-3FE6-EF19-02A1025D79B1";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.3322676295501882e-15 0 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 1.3322676295501882e-15 0 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidCornerInn_001Shape" -p "bpctrl_l_EyeLidCornerInn_001";
	rename -uid "FF0EA367-45EA-461E-21EB-C7B2950A6A7F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.10327368338929555 0.24932472707467923 0
		4.4455735471308631e-16 0.26986713992562272 0
		-0.10327368338929199 0.24932472707467923 0
		-0.19082488466083669 0.19082488466085579 0
		-0.24932472707465569 0.10327368338928977 0
		-0.26986713992563649 -2.8421709430404007e-14 0
		-0.24932472707465569 -0.10327368338931819 0
		-0.19082488466083669 -0.19082488466082737 0
		-0.10327368338929199 -0.24932472707467923 0
		4.4362106498703892e-16 -0.26986713992562272 0
		0.10327368338929555 -0.24932472707467923 0
		0.19082488466084024 -0.19082488466082737 0
		0.24932472707465925 -0.10327368338931819 0
		0.26986713992564004 -2.8421709430404007e-14 0
		0.24932472707465836 0.10327368338928977 0
		0.19082488466084024 0.19082488466085579 0
		0.10327368338929555 0.24932472707467923 0
		;
createNode transform -n "bpctrl_l_EyeLidCornerInnDrv_001" -p "bpjnt_l_EyeLidCornerInn_001";
	rename -uid "F5365597-453D-0EF3-75CE-BCB88AEA0C10";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 0 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 0 0 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_EyeLidCornerInnDrv_001Shape" -p "bpctrl_l_EyeLidCornerInnDrv_001";
	rename -uid "4EA98F57-48FE-3B42-8018-EEB1A26EF01D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538198 0.56380601922538176 0
		-0.56380601922538198 -0.56380601922538176 0
		0.56380601922538265 -0.56380601922538176 0
		0.56380601922538265 0.56380601922538176 0
		-0.56380601922538198 0.56380601922538176 0
		;
createNode transform -n "r_Lid_Rig" -p "Lid_Rig";
	rename -uid "88A5C7C5-49E4-8F19-273A-9DAAAEE81560";
	setAttr ".rp" -type "double3" -3.7658772468566895 163.15597534179688 4.5459144115447998 ;
	setAttr ".sp" -type "double3" -3.7658772468566895 163.15597534179688 4.5459144115447998 ;
createNode transform -n "r_EyeLidUpper_Rig" -p "r_Lid_Rig";
	rename -uid "4E5ED9E5-40AB-296C-00A7-A6A33194F411";
createNode transform -n "r_EyeLidUpper_Rig_Crv" -p "r_EyeLidUpper_Rig";
	rename -uid "B596A6C4-4164-9873-DC95-848C0A1B1DAB";
createNode transform -n "crv_r_EyeLidUpper_001" -p "r_EyeLidUpper_Rig_Crv";
	rename -uid "12F89967-4C74-2006-6598-B19162246DD1";
	setAttr ".rp" -type "double3" -3.7658772468566895 163.35364414994888 4.5254012144299294 ;
	setAttr ".sp" -type "double3" -3.7658772468566895 163.35364414994888 4.5254012144299294 ;
createNode nurbsCurve -n "crv_r_EyeLidUpper_00Shape1" -p "crv_r_EyeLidUpper_001";
	rename -uid "2C8C0DF4-4487-C4CA-B083-DD8F55EC4CB7";
	setAttr -k off ".v";
	setAttr ".iog[0].og[5].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-2.1721820831298828 162.75773620605469 4.5605368614196777
		-2.1902806227611675 162.92535990700463 4.5610699845631881
		-2.2790117852307183 163.16118604656506 4.5612883745789254
		-2.3807995776121662 163.36661954381591 4.5939587700153179
		-2.5294671736922454 163.53747682435198 4.6577324598955858
		-2.7390824140505496 163.69626772897726 4.734887267016715
		-2.9945315947822975 163.81943829879503 4.8268137586697266
		-3.3430842332646202 163.91627811193496 4.9120018078271439
		-3.7394007442328863 163.9495520938431 4.9050543971453378
		-4.0871880308571704 163.90308560261326 4.8589553524538687
		-4.3557355889143237 163.84274631861277 4.8122955940947687
		-4.6385645933735944 163.75432990145768 4.744671819096455
		-4.9393003572346768 163.62435442559513 4.5839166095809816
		-5.1842513422788246 163.44319239160859 4.3545908404483553
		-5.2726755631637277 163.35625497664515 4.26598034694136
		-5.3283043973756081 163.259644369245 4.1805661991751695
		-5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode transform -n "crv_r_EyeLidUpperDrv_001" -p "r_EyeLidUpper_Rig_Crv";
	rename -uid "76DAB3BE-467E-876E-C446-F8850B6B599A";
	setAttr ".rp" -type "double3" -3.7658772468566881 163.40935422523262 4.5443174591261206 ;
	setAttr ".sp" -type "double3" -3.7658772468566881 163.40935422523262 4.5443174591261206 ;
createNode nurbsCurve -n "crv_r_EyeLidUpperDrv_00Shape1" -p "crv_r_EyeLidUpperDrv_001";
	rename -uid "272CDB0C-4BD4-0DCD-86DC-0E93D2CCED43";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 0 no 3
		9 0 0 0 0.25 0.5 0.75 1 1 1
		7
		-2.1721820831298846 162.75773620605472 4.5605368614196653
		-2.3151583628599539 163.44362215188238 4.5484632231050641
		-2.747738859776685 163.72880250497045 4.7951469204387305
		-3.6282773564662891 164.06097224441055 4.9498342972195388
		-4.7221906059152694 163.73631570121245 4.8577518451535155
		-5.239790512475575 163.5244505859514 4.3178336900531562
		-5.3595724105834917 163.14787292480474 4.1388006210327024
		;
	setAttr ".dcv" yes;
createNode transform -n "crv_r_EyeLidUpperBlink_001" -p "r_EyeLidUpper_Rig_Crv";
	rename -uid "FA98C485-493E-0E30-867C-209D3F750540";
	setAttr ".rp" -type "double3" -3.7658772468566895 162.95291975794873 4.516902159594065 ;
	setAttr ".sp" -type "double3" -3.7658772468566895 162.95291975794873 4.516902159594065 ;
createNode nurbsCurve -n "crv_r_EyeLidUpperBlink_00Shape1" -p "crv_r_EyeLidUpperBlink_001";
	rename -uid "78555938-4D3A-3C47-44D8-C9986371FA32";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-2.1721820831298828 162.75773620605469 4.5605368614196777
		-2.2158012296340401 162.81737496193151 4.5638143102752586
		-2.3045196566863289 162.90204824366936 4.5836756524921203
		-2.4231159515141103 162.97123004165275 4.6241087439388933
		-2.5950146384052202 163.0252380340105 4.6923751479266969
		-2.8479576841236978 163.06140340218806 4.7872055184347495
		-3.1352023414327759 163.08955709769617 4.8590197348195678
		-3.4936428714036718 163.1193350220112 4.8950036981554153
		-3.8802910145284168 163.13661122843374 4.8891752444888219
		-4.2153140477954549 163.13792162435442 4.8547281746453717
		-4.4671465202648948 163.13527457706155 4.8006673218221998
		-4.7185105265589513 163.13371432511025 4.7069886766397699
		-4.9787659817773182 163.13804460173833 4.5421156160978313
		-5.1993712116794875 163.14539228762678 4.3357160763423277
		-5.2685211906261546 163.14733800285535 4.2563978111533469
		-5.32121923996952 163.14810330984278 4.1903656916864565
		-5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode transform -n "r_EyeLidUpper_Rig_Jnt" -p "r_EyeLidUpper_Rig";
	rename -uid "DE3BBFC0-47C4-9B88-F365-1F915429F67F";
createNode joint -n "bpjnt_r_EyeLidUpperInn_002" -p "r_EyeLidUpper_Rig_Jnt";
	rename -uid "B3F147AB-499E-29E9-6DE8-6FA8339C0F4F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.3151583671569815 163.44361877441401 4.5484633445739728 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3151583671569824 163.44361877441406 4.5484633445739746 1;
createNode transform -n "bpctrl_r_EyeLidUpperInn_002" -p "bpjnt_r_EyeLidUpperInn_002";
	rename -uid "48ADE770-4CE3-68A7-23C7-C2A2EC25AFCA";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -8.8817841970012543e-16 2.8421709430404014e-14 -8.8817841970012543e-16 ;
	setAttr ".sp" -type "double3" -8.8817841970012543e-16 2.8421709430404014e-14 -8.8817841970012543e-16 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidUpperInn_002Shape" -p "bpctrl_r_EyeLidUpperInn_002";
	rename -uid "07490B5F-48ED-5004-9319-11A14A48D475";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026486 0.3650363329099946 2.5329483851341069e-18
		-1.3708217879060686e-18 0.39511247956508555 2.7416435758121373e-18
		-0.15120299985026442 0.3650363329099946 2.5329483851341069e-18
		-0.27938671363193324 0.27938671363190792 1.9386347640534163e-18
		-0.36503633291000526 0.15120299985022712 1.0491815739135223e-18
		-0.39511247956512774 -5.6843418860808015e-14 -9.8607613152626476e-32
		-0.36503633291000526 -0.15120299985028396 -1.0491815739133251e-18
		-0.27938671363193324 -0.27938671363193635 -1.9386347640530218e-18
		-0.15120299985026442 -0.36503633291005144 -2.5329483851339097e-18
		1.37082178790597e-18 -0.39511247956514239 -2.7416435758119401e-18
		0.15120299985026486 -0.36503633291005144 -2.5329483851339097e-18
		0.27938671363193279 -0.27938671363193635 -1.9386347640530218e-18
		0.3650363329100057 -0.15120299985028396 -1.0491815739133251e-18
		0.39511247956512796 -5.6843418860808015e-14 -9.8607613152626476e-32
		0.3650363329100057 0.15120299985022712 1.0491815739135223e-18
		0.27938671363193279 0.27938671363190792 1.9386347640534163e-18
		0.15120299985026486 0.3650363329099946 2.5329483851341069e-18
		;
createNode joint -n "bpjnt_r_EyeLidUpperOut_002" -p "r_EyeLidUpper_Rig_Jnt";
	rename -uid "AA1555AC-416A-85FB-450C-7E8F20EA72DF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.2397904396057093 163.52444458007807 4.3178339004516584 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.2397904396057129 163.52444458007812 4.3178339004516602 1;
createNode transform -n "bpctrl_r_EyeLidUpperOut_002" -p "bpjnt_r_EyeLidUpperOut_002";
	rename -uid "58841B4C-4DA6-4C42-B08D-5CA74963C70A";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -3.5527136788005017e-15 -2.8421709430404014e-14 0 ;
	setAttr ".sp" -type "double3" -3.5527136788005017e-15 -2.8421709430404014e-14 0 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidUpperOut_002Shape" -p "bpctrl_r_EyeLidUpperOut_002";
	rename -uid "E61D7805-485A-AA9F-9B88-C58F79370202";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026528 0.36503633290993776 8.7139151451750947e-16
		1.7763568394002505e-15 0.39511247956505713 8.8817841970012513e-16
		-0.1512029998502635 0.36503633290993776 9.04965324882741e-16
		-0.27938671363193274 0.2793867136318795 9.1919657592497792e-16
		-0.3650363329100052 0.15120299985019869 9.2870559386226739e-16
		-0.39511247956512724 -2.8421709430404014e-14 9.3204471691311943e-16
		-0.3650363329100052 -0.1512029998503408 9.2870559386226739e-16
		-0.27938671363193274 -0.27938671363199319 9.1919657592497792e-16
		-0.1512029998502635 -0.36503633291007986 9.04965324882741e-16
		8.8817841970012523e-16 -0.39511247956519924 8.8817841970012523e-16
		0.15120299985026528 -0.36503633291007986 8.7139151451750947e-16
		0.27938671363193363 -0.27938671363199319 8.5716026347527254e-16
		0.36503633291000609 -0.1512029998503408 8.4765124553798307e-16
		0.39511247956512813 -2.8421709430404007e-14 8.4431212248713113e-16
		0.36503633291000609 0.15120299985019869 8.4765124553798307e-16
		0.27938671363193274 0.2793867136318795 8.5716026347527264e-16
		0.15120299985026528 0.36503633290993776 8.7139151451750947e-16
		;
createNode joint -n "bpjnt_r_EyeLidUpperInn_001" -p "r_EyeLidUpper_Rig_Jnt";
	rename -uid "0E0B2792-4512-E126-4A62-F4A6EBF056C7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.7477388381957999 163.72880554199219 4.7951469421386683 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.7477388381958008 163.72880554199219 4.7951469421386719 1;
createNode transform -n "bpctrl_r_EyeLidUpperInn_001" -p "bpjnt_r_EyeLidUpperInn_001";
	rename -uid "525B4746-4E85-3FE0-2A00-E79B67C0F2A5";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 0 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 0 0 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidUpperInn_001Shape" -p "bpctrl_r_EyeLidUpperInn_001";
	rename -uid "D47FDE46-4F0B-FD5E-0C9C-F1A094CCED3E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026442 0.36503633290996618 3.4840284557798436e-17
		4.4408920985006262e-16 0.39511247956508555 1.370821787906118e-18
		-0.15120299985026397 0.36503633290996618 -3.2307336172664527e-17
		-0.27938671363193279 0.27938671363193635 -6.1066995067678618e-17
		-0.36503633291000481 0.15120299985022712 -8.0529757537327511e-17
		-0.39511247956512774 -2.8421709430404007e-14 -8.7732594425988295e-17
		-0.36503633291000481 -0.15120299985028396 -8.1578939111240935e-17
		-0.27938671363193279 -0.27938671363199319 -6.3005629831732133e-17
		-0.15120299985026397 -0.36503633291002302 -3.4840284557798338e-17
		4.4408920985006262e-16 -0.39511247956514239 -1.3708217879059207e-18
		0.15120299985026486 -0.36503633291002302 3.2307336172664724e-17
		0.27938671363193324 -0.27938671363199319 6.1066995067678717e-17
		0.36503633291000526 -0.15120299985028396 8.052975753732761e-17
		0.39511247956512774 -2.8421709430404007e-14 8.7732594425988295e-17
		0.36503633291000526 0.15120299985022712 8.1578939111241033e-17
		0.27938671363193324 0.27938671363193635 6.3005629831732232e-17
		0.15120299985026442 0.36503633290996618 3.4840284557798436e-17
		;
createNode joint -n "bpjnt_r_EyeLidUpperMid_001" -p "r_EyeLidUpper_Rig_Jnt";
	rename -uid "23912736-4E7F-32D8-E539-22BEA11878CC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.6282773017883292 164.06097412109369 4.9498343467712367 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.6282773017883301 164.06097412109375 4.9498343467712402 1;
createNode transform -n "bpctrl_r_EyeLidUpperMid_001" -p "bpjnt_r_EyeLidUpperMid_001";
	rename -uid "6AAF4C6F-4E32-7A60-F5A2-A6A48A8699C1";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 -2.8421709430404014e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 -2.8421709430404014e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidUpperMid_001Shape" -p "bpctrl_r_EyeLidUpperMid_001";
	rename -uid "FE5C9BCE-481F-DC69-B0BD-64ADEA89EA7F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026531 0.36503633290999454 8.8817841970012523e-16
		1.3708217879059207e-18 0.39511247956508549 8.8817841970012523e-16
		-0.15120299985026353 0.36503633290999454 8.8817841970012523e-16
		-0.27938671363193279 0.27938671363190787 8.8817841970012523e-16
		-0.36503633291000437 0.15120299985022709 8.8817841970012523e-16
		-0.39511247956512641 0 8.8817841970012523e-16
		-0.36503633291000437 -0.15120299985028393 8.8817841970012523e-16
		-0.27938671363193279 -0.27938671363196471 8.8817841970012523e-16
		-0.15120299985026353 -0.36503633291002296 8.8817841970012523e-16
		-1.370821787906118e-18 -0.39511247956514234 8.8817841970012523e-16
		0.15120299985026575 -0.36503633291002296 8.8817841970012523e-16
		0.27938671363193368 -0.27938671363196471 8.8817841970012523e-16
		0.36503633291000703 -0.15120299985028393 8.8817841970012523e-16
		0.39511247956512863 0 8.8817841970012523e-16
		0.36503633291000703 0.15120299985022709 8.8817841970012523e-16
		0.27938671363193368 0.27938671363190787 8.8817841970012523e-16
		0.15120299985026531 0.36503633290999454 8.8817841970012523e-16
		;
createNode transform -n "bpctrl_r_EyeLidUpperMidDrv_001" -p "bpjnt_r_EyeLidUpperMid_001";
	rename -uid "A86D087A-4E79-FC99-2166-93A42BECD40E";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 0 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 0 0 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidUpperMidDrv_001Shape" -p "bpctrl_r_EyeLidUpperMidDrv_001";
	rename -uid "4ACB3918-41FA-3B3B-E4B5-439384948955";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538265 0.56380601922538165 8.8817841970012523e-16
		-0.56380601922538265 -0.56380601922538165 8.8817841970012523e-16
		0.5638060192253822 -0.56380601922538165 8.8817841970012523e-16
		0.5638060192253822 0.56380601922538165 8.8817841970012523e-16
		-0.56380601922538265 0.56380601922538165 8.8817841970012523e-16
		;
createNode joint -n "bpjnt_r_EyeLidUpperOut_001" -p "r_EyeLidUpper_Rig_Jnt";
	rename -uid "805B2182-46E8-F236-7139-0C94AC2FD89A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.7221903800964338 163.73631286621088 4.8577518463134766 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.7221903800964355 163.73631286621094 4.8577518463134766 1;
createNode transform -n "bpctrl_r_EyeLidUpperOut_001" -p "bpjnt_r_EyeLidUpperOut_001";
	rename -uid "2943D4C3-456D-0D7A-44A1-53ACF777881A";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.6645352591003765e-15 -2.8421709430404014e-14 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" -2.6645352591003765e-15 -2.8421709430404014e-14 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidUpperOut_001Shape" -p "bpctrl_r_EyeLidUpperOut_001";
	rename -uid "9F42DB7B-4196-82FD-C04B-D3941B2CD442";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026353 0.3650363329099946 8.8944489389269214e-16
		-8.8954924148803125e-16 0.39511247956514239 8.8954924148803125e-16
		-0.15120299985026531 0.3650363329099946 8.8944489389269214e-16
		-0.27938671363193368 0.27938671363196477 8.8914773708215209e-16
		-0.36503633291000614 0.15120299985025554 8.8870301048708204e-16
		-0.39511247956512907 0 8.8817841970012523e-16
		-0.36503633291000614 -0.15120299985028396 8.8765382891316842e-16
		-0.27938671363193368 -0.27938671363193635 8.8720910231809857e-16
		-0.15120299985026531 -0.3650363329099946 8.8691194550755833e-16
		-8.8680759791221921e-16 -0.39511247956511397 8.8680759791221921e-16
		0.15120299985026442 -0.3650363329099946 8.8691194550755833e-16
		0.2793867136319319 -0.27938671363193635 8.8720910231809857e-16
		0.36503633291000526 -0.15120299985028396 8.8765382891316842e-16
		0.39511247956512552 0 8.8817841970012523e-16
		0.36503633291000526 0.15120299985025554 8.8870301048708204e-16
		0.27938671363193102 0.27938671363196477 8.8914773708215209e-16
		0.15120299985026353 0.3650363329099946 8.8944489389269214e-16
		;
createNode transform -n "r_EyeLidLower_Rig" -p "r_Lid_Rig";
	rename -uid "C6108656-4C3B-0E52-D2CE-9AB730DB3695";
createNode transform -n "r_EyeLidLower_Rig_Jnt" -p "r_EyeLidLower_Rig";
	rename -uid "282D28F8-47A5-618C-2874-088695EB8496";
createNode joint -n "bpjnt_r_EyeLidLowerInn_001" -p "r_EyeLidLower_Rig_Jnt";
	rename -uid "CE5A9887-4E67-9045-B04C-D98C1C801A97";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.3544106483459464 162.57978820800776 4.5731253623962402 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_EyeLidLowerInn_001" -p "bpjnt_r_EyeLidLowerInn_001";
	rename -uid "56FDAA21-45A0-0E58-9FD8-A49DC2B50894";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -8.8817841970012543e-16 0 0 ;
	setAttr ".sp" -type "double3" -8.8817841970012543e-16 0 0 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidLowerInn_001Shape" -p "bpctrl_r_EyeLidLowerInn_001";
	rename -uid "33C5CB61-4569-6D25-A469-BE8059049FBD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026353 0.36503633290996618 -8.1976432477709546e-16
		4.4340379895610961e-16 0.39511247956508555 -8.8680759791221882e-16
		-0.15120299985026486 0.36503633290996618 -9.5405956623802139e-16
		-0.27938671363193324 0.27938671363190792 -1.0112817272175093e-15
		-0.3650363329100057 0.15120299985022712 -1.0497625255617371e-15
		-0.39511247956512818 -5.6843418860808015e-14 -1.063643608552102e-15
		-0.3650363329100057 -0.15120299985031238 -1.0508117071356507e-15
		-0.27938671363193324 -0.27938671363199319 -1.0132203619815628e-15
		-0.15120299985026486 -0.36503633291005144 -9.565925146231552e-16
		4.4477462074401563e-16 -0.39511247956517082 -8.8954924148803086e-16
		0.15120299985026397 -0.36503633291005144 -8.2229727316222917e-16
		0.27938671363193279 -0.27938671363199319 -7.6507511218274104e-16
		0.36503633291000481 -0.15120299985031238 -7.265943138385134e-16
		0.39511247956512729 -5.6843418860808015e-14 -7.1271323084814874e-16
		0.36503633291000481 0.15120299985022712 -7.2554513226459988e-16
		0.27938671363193279 0.27938671363190792 -7.6313647741868762e-16
		0.15120299985026353 0.36503633290996618 -8.1976432477709546e-16
		;
createNode joint -n "bpjnt_r_EyeLidLowerOut_002" -p "r_EyeLidLower_Rig_Jnt";
	rename -uid "37BBB4A7-4606-6114-6E30-84846CDA2989";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.2303051948547346 162.77601623535151 4.3053255081176758 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_EyeLidLowerOut_002" -p "bpjnt_r_EyeLidLowerOut_002";
	rename -uid "7D88D269-48C0-8BBA-00CE-7192D3A4A92C";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.7763568394002509e-15 0 0 ;
	setAttr ".sp" -type "double3" -1.7763568394002509e-15 0 0 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidLowerOut_002Shape" -p "bpctrl_r_EyeLidLowerOut_002";
	rename -uid "C8266D22-4BAA-0A91-D2E0-F5BD1147F253";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026264 0.3650363329099946 8.8817841970012523e-16
		-1.7763568394002505e-15 0.39511247956514239 8.8817841970012513e-16
		-0.15120299985026531 0.3650363329099946 8.8817841970012523e-16
		-0.27938671363193368 0.27938671363196477 8.8817841970012523e-16
		-0.36503633291000614 0.15120299985028396 8.8817841970012523e-16
		-0.39511247956512818 0 8.8817841970012523e-16
		-0.36503633291000614 -0.15120299985025554 8.8817841970012523e-16
		-0.27938671363193368 -0.27938671363193635 8.8817841970012523e-16
		-0.15120299985026531 -0.3650363329099946 8.8817841970012523e-16
		-1.7763568394002505e-15 -0.39511247956511397 8.8817841970012523e-16
		0.15120299985026264 -0.3650363329099946 8.8817841970012523e-16
		0.2793867136319319 -0.27938671363193635 8.8817841970012523e-16
		0.36503633291000437 -0.15120299985025554 8.8817841970012523e-16
		0.39511247956512552 0 8.8817841970012523e-16
		0.36503633291000437 0.15120299985028396 8.8817841970012523e-16
		0.2793867136319319 0.27938671363196477 8.8817841970012523e-16
		0.15120299985026264 0.3650363329099946 8.8817841970012523e-16
		;
createNode joint -n "bpjnt_r_EyeLidLowerOut_001" -p "r_EyeLidLower_Rig_Jnt";
	rename -uid "0936341B-4207-404E-BAF1-35822862276A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.89562940597534 162.50459289550776 4.7268505096435547 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_EyeLidLowerOut_001" -p "bpjnt_r_EyeLidLowerOut_001";
	rename -uid "BF82A3EA-4B2C-385C-F934-129AEAF6BDD8";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 8.5265128291212048e-14 0 ;
	setAttr ".sp" -type "double3" 0 8.5265128291212048e-14 0 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidLowerOut_001Shape" -p "bpctrl_r_EyeLidLowerOut_001";
	rename -uid "7528CC98-4525-4758-2B17-9EB8F6A47F00";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026353 0.36503633291002302 3.4840284557798436e-17
		-1.3708217879062166e-18 0.39511247956517082 1.370821787906315e-18
		-0.15120299985026353 0.36503633291002302 -3.2307336172664231e-17
		-0.27938671363193546 0.27938671363196477 -6.1066995067679111e-17
		-0.36503633291000614 0.15120299985028396 -8.052975753732761e-17
		-0.39511247956512907 0 -8.7732594425988492e-17
		-0.36503633291000614 -0.15120299985025554 -8.1578939111241132e-17
		-0.27938671363193546 -0.27938671363190792 -6.3005629831732429e-17
		-0.15120299985026353 -0.36503633290996618 -3.4840284557798042e-17
		1.3708217879060193e-18 -0.39511247956511397 -1.3708217879059205e-18
		0.15120299985026353 -0.36503633290996618 3.2307336172664625e-17
		0.27938671363193368 -0.27938671363190792 6.1066995067679111e-17
		0.36503633291000437 -0.15120299985025554 8.0529757537327511e-17
		0.39511247956512685 0 8.7732594425988196e-17
		0.36503633291000437 0.15120299985028396 8.1578939111241033e-17
		0.27938671363193368 0.27938671363196477 6.3005629831732429e-17
		0.15120299985026353 0.36503633291002302 3.4840284557798436e-17
		;
createNode joint -n "bpjnt_r_EyeLidLowerInn_002" -p "r_EyeLidLower_Rig_Jnt";
	rename -uid "72C53D77-41EB-6FF7-D399-A18F94D77C72";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.0335223674774161 162.40063476562494 4.9530282020568812 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_EyeLidLowerInn_002" -p "bpjnt_r_EyeLidLowerInn_002";
	rename -uid "716BE8C5-4AE8-3BB0-6C80-C0AEA8C395AC";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -8.8817841970012543e-16 2.8421709430404014e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" -8.8817841970012543e-16 2.8421709430404014e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidLowerInn_002Shape" -p "bpctrl_r_EyeLidLowerInn_002";
	rename -uid "A17F4DC2-4C59-0187-BA6E-B58148A42530";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026353 0.36503633291002302 0
		0 0.39511247956514239 0
		-0.15120299985026531 0.36503633291002302 0
		-0.27938671363193368 0.27938671363199319 0
		-0.36503633291000526 0.15120299985028396 0
		-0.39511247956512818 2.8421709430404007e-14 0
		-0.36503633291000526 -0.15120299985025554 0
		-0.27938671363193368 -0.27938671363193635 0
		-0.15120299985026531 -0.3650363329099946 0
		0 -0.39511247956508555 0
		0.15120299985026397 -0.3650363329099946 0
		0.27938671363193235 -0.27938671363193635 0
		0.36503633291000481 -0.15120299985025554 0
		0.39511247956512729 2.8421709430404007e-14 0
		0.36503633291000437 0.15120299985028396 0
		0.27938671363193235 0.27938671363199319 0
		0.15120299985026353 0.36503633291002302 0
		;
createNode joint -n "bpjnt_r_EyeLidLowerMid_001" -p "r_EyeLidLower_Rig_Jnt";
	rename -uid "0E875306-4037-063D-D030-2694F3B5212F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.9433994293212868 162.2509765625 4.8954463005065918 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_EyeLidLowerMid_001" -p "bpjnt_r_EyeLidLowerMid_001";
	rename -uid "EA221758-4F9D-B39A-4220-D6A54D32118D";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.3322676295501882e-15 -5.6843418860808027e-14 0 ;
	setAttr ".sp" -type "double3" -1.3322676295501882e-15 -5.6843418860808027e-14 0 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidLowerMid_001Shape" -p "bpctrl_r_EyeLidLowerMid_001";
	rename -uid "4BC42C61-41C8-5B54-AD63-D5A40581725F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026353 0.36503633290996618 8.546046093348938e-16
		-4.4408920985006262e-16 0.39511247956508555 8.8817841970012523e-16
		-0.15120299985026575 0.36503633290996618 9.2175223006535696e-16
		-0.27938671363193412 0.2793867136318795 9.5021473214983081e-16
		-0.36503633291000659 0.15120299985019869 9.6923276802440975e-16
		-0.39511247956512774 0 9.7591101412611343e-16
		-0.36503633291000659 -0.15120299985028396 9.6923276802440975e-16
		-0.27938671363193412 -0.27938671363196477 9.5021473214983081e-16
		-0.15120299985026575 -0.36503633291005144 9.2175223006535696e-16
		-4.4408920985006262e-16 -0.39511247956517082 8.8817841970012523e-16
		0.15120299985026397 -0.36503633291005144 8.546046093348936e-16
		0.27938671363193235 -0.27938671363196477 8.2614210725041986e-16
		0.36503633291000481 -0.15120299985028396 8.0712407137584091e-16
		0.39511247956512685 0 8.0044582527413704e-16
		0.36503633291000481 0.15120299985019869 8.0712407137584091e-16
		0.27938671363193235 0.2793867136318795 8.2614210725041986e-16
		0.15120299985026353 0.36503633290996618 8.546046093348938e-16
		;
createNode transform -n "bpctrl_r_EyeLidLowerMidDrv_001" -p "bpjnt_r_EyeLidLowerMid_001";
	rename -uid "CF3A2D03-4E7E-7CC1-E077-A8A4C2C32193";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.3322676295501882e-15 0 0 ;
	setAttr ".sp" -type "double3" -1.3322676295501882e-15 0 0 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidLowerMidDrv_001Shape" -p "bpctrl_r_EyeLidLowerMidDrv_001";
	rename -uid "5C534E06-4974-C1D5-1A32-74A92E7AEE8D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538309 -0.56380601922538176 1.0133685044933799e-15
		-0.56380601922538309 0.56380601922538176 1.0133685044933799e-15
		0.5638060192253822 0.56380601922538176 7.6298833490687054e-16
		0.5638060192253822 -0.56380601922538176 7.6298833490687054e-16
		-0.56380601922538309 -0.56380601922538176 1.0133685044933799e-15
		;
createNode transform -n "r_EyeLidLower_Rig_Crv" -p "r_EyeLidLower_Rig";
	rename -uid "75CA0ED0-40FB-5D7E-F835-E0BE45981B1C";
createNode transform -n "crv_r_EyeLidLower_001" -p "r_EyeLidLower_Rig_Crv";
	rename -uid "E5080F0E-4A00-6AD8-71AF-3D9C7C03F5E6";
	setAttr ".rp" -type "double3" -3.7658772468566895 162.73293304443359 4.5223348140716553 ;
	setAttr ".sp" -type "double3" -3.7658772468566895 162.73293304443359 4.5223348140716553 ;
createNode nurbsCurve -n "crv_r_EyeLidLower_00Shape1" -p "crv_r_EyeLidLower_001";
	rename -uid "0950C862-46B1-FB52-D055-A39459BB806B";
	setAttr -k off ".v";
	setAttr ".iog[0].og[5].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-2.1721820831298828 162.75773620605469 4.5605368614196777
		-2.2370400428771973 162.6717529296875 4.5650172233581543
		-2.3409969806671143 162.63011169433594 4.5903224945068359
		-2.4845929145812988 162.5838623046875 4.647456169128418
		-2.6528940200805664 162.52378845214844 4.7176456451416016
		-2.8638091087341309 162.451416015625 4.8060564994812012
		-3.1178109645843506 162.39273071289062 4.8812456130981445
		-3.4912331104278564 162.34303283691406 4.9058690071105957
		-3.8972983360290527 162.3179931640625 4.8827762603759766
		-4.306492805480957 162.36851501464844 4.8430461883544922
		-4.6789984703063965 162.46110534667969 4.7153425216674805
		-4.9391307830810547 162.58314514160156 4.5575141906738281
		-5.0969715118408203 162.70002746582031 4.4358458518981934
		-5.2303051948547363 162.85560607910156 4.3053255081176758
		-5.3084053993225098 162.97319030761719 4.2254776954650879
		-5.3476080894470215 163.06088256835938 4.1624565124511719
		-5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode transform -n "crv_r_EyeLidLowerDrv_001" -p "r_EyeLidLower_Rig_Crv";
	rename -uid "9DAB5A29-43D4-FAD5-19FC-A2BAE9702200";
	setAttr ".rp" -type "double3" -3.7658772468566855 162.69942644586683 4.5459143215334024 ;
	setAttr ".sp" -type "double3" -3.7658772468566855 162.69942644586683 4.5459143215334024 ;
createNode nurbsCurve -n "crv_r_EyeLidLowerDrv_00Shape1" -p "crv_r_EyeLidLowerDrv_001";
	rename -uid "04F91B64-41FB-F39B-0486-45BFF6DC09CE";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 0 no 3
		9 0 0 0 0.25 0.5 0.75 1 1 1
		7
		-2.1721820831298775 162.75773620605474 4.5605368614196653
		-2.354410721980166 162.5797929655439 4.5731251429626862
		-3.0335223982099451 162.40063114967651 4.9530280220341014
		-3.9433993266984406 162.25097996692901 4.8954465320505998
		-4.8956294512215806 162.50459216972587 4.7268503750056619
		-5.2303051948547363 162.77602199772713 4.3053255081176642
		-5.3595724105834934 163.14787292480466 4.1388006210327024
		;
	setAttr ".dcv" yes;
createNode transform -n "crv_r_EyeLidLowerBlink_001" -p "r_EyeLidLower_Rig_Crv";
	rename -uid "488AD90B-406C-937E-84DC-66872E8EDC1E";
	setAttr ".rp" -type "double3" -3.7658772468566895 162.95293115079309 4.5168298676447787 ;
	setAttr ".sp" -type "double3" -3.7658772468566895 162.95293115079309 4.5168298676447787 ;
createNode nurbsCurve -n "crv_r_EyeLidLowerBlink_00Shape1" -p "crv_r_EyeLidLowerBlink_001";
	rename -uid "9B104386-46F4-F5F9-2996-7F80DEAB84E7";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-2.1721820831298828 162.75773620605469 4.5605368614196777
		-2.240612678322877 162.84513041479622 4.5679519499577301
		-2.3188154328873716 162.91251230954444 4.587937710707342
		-2.4356433389819259 162.97662699912721 4.6288691059937674
		-2.5806423206915707 163.02204872445057 4.686576688909879
		-2.7684495573578616 163.05277881217967 4.7596171227156034
		-2.9961459762307472 163.0760870969047 4.8298274934426058
		-3.3454041749791714 163.10821347160126 4.8861377403881239
		-3.7526441750615898 163.13305422778859 4.8948591142568425
		-4.1765864902908358 163.13817288507596 4.8605441636380089
		-4.5820416081046131 163.1341508775339 4.7640451302474114
		-4.8871395759253158 163.1357422822621 4.6093173395634102
		-5.0680303387232755 163.1408737244621 4.466532205287975
		-5.2159535612584005 163.14591625319881 4.3173996940472197
		-5.2901752061508382 163.14776064020157 4.2298915166151447
		-5.332125387217423 163.1481260955315 4.1760256020057387
		-5.3595724105834961 163.14787292480469 4.1388006210327148
		;
createNode joint -n "bpjnt_r_EyeLidCornerOut_001" -p "r_Lid_Rig";
	rename -uid "6B1B3C64-4CE2-FC23-B910-558A2CC43B39";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -5.3595724105834943 163.14787292480469 4.1388006210327113 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.3595724105834961 163.14787292480469 4.1388006210327148 1;
createNode transform -n "bpctrl_r_EyeLidCornerOut_001" -p "bpjnt_r_EyeLidCornerOut_001";
	rename -uid "214AFE9E-4BC1-C0DE-A123-E988D9DBCEC0";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 -1.1368683772161605e-13 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 0 -1.1368683772161605e-13 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidCornerOut_001Shape" -p "bpctrl_r_EyeLidCornerOut_001";
	rename -uid "1852CE6E-496F-1661-1129-AD875751F0EC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026528 0.36503633290996618 0
		8.8817841970012523e-16 0.39511247956508555 0
		-0.1512029998502635 0.36503633290996618 0
		-0.27938671363193274 0.2793867136318795 0
		-0.3650363329100052 0.15120299985022712 0
		-0.39511247956512724 0 0
		-0.3650363329100052 -0.15120299985028396 0
		-0.27938671363193274 -0.27938671363196477 0
		-0.1512029998502635 -0.36503633291005144 0
		8.8817841970012523e-16 -0.39511247956517082 0
		0.15120299985026528 -0.36503633291005144 0
		0.27938671363193274 -0.27938671363196477 0
		0.36503633291000609 -0.15120299985028396 0
		0.39511247956512813 0 0
		0.36503633291000609 0.15120299985022712 0
		0.27938671363193274 0.2793867136318795 0
		0.15120299985026528 0.36503633290996618 0
		;
createNode transform -n "bpctrl_r_EyeLidCornerOutDrv_001" -p "bpjnt_r_EyeLidCornerOut_001";
	rename -uid "481CE60D-447A-F254-5D87-59A1479BDADF";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 -5.6843418860808027e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 0 -5.6843418860808027e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidCornerOutDrv_001Shape" -p "bpctrl_r_EyeLidCornerOutDrv_001";
	rename -uid "ECE2F6C3-488A-DFE6-9CC6-9680ACCF68E2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538165 0.56380601922538176 0
		-0.56380601922538165 -0.56380601922538176 0
		0.56380601922538343 -0.56380601922538176 0
		0.56380601922538343 0.56380601922538176 0
		-0.56380601922538165 0.56380601922538176 0
		;
createNode joint -n "bpjnt_r_EyeLidCornerInn_001" -p "r_Lid_Rig";
	rename -uid "EAFF5615-48DA-E62B-7571-7BB89AEFF812";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -2.1721820831298828 162.75773620605463 4.5605368614196777 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1721820831298828 162.75773620605469 4.5605368614196777 1;
createNode transform -n "bpctrl_r_EyeLidCornerInn_001" -p "bpjnt_r_EyeLidCornerInn_001";
	rename -uid "53800A28-40DC-BF3E-99B5-33B038CB8CF3";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.3322676295501882e-15 2.8421709430404014e-14 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 1.3322676295501882e-15 2.8421709430404014e-14 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidCornerInn_001Shape" -p "bpctrl_r_EyeLidCornerInn_001";
	rename -uid "407DCF58-4311-5824-E3BF-4BBE44561045";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026528 0.36503633290999593 3.7012175744671215e-17
		4.4408920985006262e-16 0.39511247956514234 -1.3708217879062168e-18
		-0.15120299985026306 0.36503633290999316 -3.9545124129804885e-17
		-0.27938671363193229 0.27938671363193379 -7.1699039800384208e-17
		-0.36503633291000431 0.15120299985025221 -9.2937426614768908e-17
		-0.39511247956512724 -3.1991499045468453e-14 -1.0002693270692552e-16
		-0.36503633291000431 -0.15120299985028723 -9.1888245040855386e-17
		-0.27938671363193229 -0.27938671363193879 -6.976040503633089e-17
		-0.15120299985026306 -0.36503633290999593 -3.7012175744671074e-17
		4.4408920985006262e-16 -0.39511247956514234 1.3708217879060195e-18
		0.15120299985026572 -0.36503633290999316 3.9545124129805137e-17
		0.27938671363193363 -0.27938671363193379 7.1699039800384121e-17
		0.36503633291000609 -0.15120299985028063 9.2937426614769043e-17
		0.39511247956512813 -2.4851919815339562e-14 1.0002693270692552e-16
		0.36503633291000609 0.15120299985025881 9.1888245040855521e-17
		0.27938671363193363 0.27938671363193879 6.9760405036330804e-17
		0.15120299985026528 0.36503633290999593 3.7012175744671215e-17
		;
createNode transform -n "bpctrl_r_EyeLidCornerInnDrv_001" -p "bpjnt_r_EyeLidCornerInn_001";
	rename -uid "9003064A-43D1-ED8F-2695-9DA4D684C9B7";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 0 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 0 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_EyeLidCornerInnDrv_001Shape" -p "bpctrl_r_EyeLidCornerInnDrv_001";
	rename -uid "8644E049-4455-50BC-9855-838698D318E6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.56380601922538254 0.56380601922534812 -1.4468959417086796e-16
		-0.56380601922538254 -0.56380601922541518 -1.4077740402107875e-16
		0.56380601922538254 -0.56380601922540496 1.4468959417086773e-16
		0.56380601922538254 0.56380601922535833 1.4077740402107853e-16
		-0.56380601922538254 0.56380601922534812 -1.4468959417086796e-16
		;
createNode transform -n "crv_r_EyeLidBlink_001" -p "r_Lid_Rig";
	rename -uid "C27C20D6-4E2B-365B-A970-B08FACBF309D";
	setAttr ".rp" -type "double3" -3.7658772468566877 162.95685615586223 4.5307205178338954 ;
	setAttr ".sp" -type "double3" -3.7658772468566877 162.95685615586223 4.5307205178338954 ;
createNode nurbsCurve -n "crv_r_EyeLidBlink_00Shape1" -p "crv_r_EyeLidBlink_001";
	rename -uid "CE3498F5-498E-CB32-C9B7-6B81C159BFE5";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 4 0 no 3
		9 0 0 0 0.25 0.5 0.75 1 1 1
		7
		-2.1721820831298846 162.75773620605469 4.5605368614196777
		-2.3347845424200599 163.01170755871317 4.5607941830338756
		-2.890630628993315 163.06471682732348 4.8740874712364164
		-3.7858383415823651 163.15597610566977 4.922640414635076
		-4.808910028568425 163.12045393546916 4.7923011100795891
		-5.2350478536651552 163.15023629183924 4.3115795990854107
		-5.3595724105834908 163.14787292480469 4.1388006210327148
		;
createNode transform -n "CheekBones_Rig" -p "Face_Rig";
	rename -uid "F9465A38-4834-4AF7-01C7-A7B6745CE07C";
createNode transform -n "l_CheekBones_Rig" -p "CheekBones_Rig";
	rename -uid "0B509BF3-4461-BC7C-CF31-3C8CAF91AB77";
createNode transform -n "l_CheekBones_Rig_Crv" -p "l_CheekBones_Rig";
	rename -uid "8984595A-44B0-8BF6-C9E9-CCB1E6118EF8";
createNode transform -n "crv_l_CheekBonesAim_001" -p "l_CheekBones_Rig_Crv";
	rename -uid "627D8A0F-439A-59A2-14EB-2A82B6645C96";
	setAttr ".rp" -type "double3" 4.5088623085629527 160.69846919459221 4.6065434522080926 ;
	setAttr ".sp" -type "double3" 4.5088623085629527 160.69846919459221 4.6065434522080926 ;
createNode nurbsCurve -n "crv_l_CheekBonesAim_00Shape1" -p "crv_l_CheekBonesAim_001";
	rename -uid "571A2A10-460A-56AA-6F4D-9CBB76E3834F";
	setAttr -k off ".v";
createNode transform -n "crv_l_CheekBones_001" -p "l_CheekBones_Rig_Crv";
	rename -uid "1B3949D3-42F2-01AA-97B5-638C4571B929";
	setAttr ".rp" -type "double3" 4.5088623085629527 160.69846919459221 3.8370690976982509 ;
	setAttr ".sp" -type "double3" 4.5088623085629527 160.69846919459221 3.8370690976982509 ;
createNode nurbsCurve -n "crv_l_CheekBones_00Shape1" -p "crv_l_CheekBones_001";
	rename -uid "CCF78E2E-4C4D-0E1D-F696-5AA86E4DFD3F";
	setAttr -k off ".v";
createNode transform -n "l_CheekBones_Rig_Jnt" -p "l_CheekBones_Rig";
	rename -uid "1A104D09-4BC3-226B-E3E5-AA9A838A378D";
createNode joint -n "bpjnt_l_CheekBones_002" -p "l_CheekBones_Rig_Jnt";
	rename -uid "2AA867D3-4DFE-5AB1-F020-DDADF2257470";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 3.0633018954533804 160.02173594338132 6.1593864997804548 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.0633018954533822 160.02173594338137 6.1593864997804557 1;
createNode transform -n "bpctrl_l_CheekBones_002" -p "bpjnt_l_CheekBones_002";
	rename -uid "E7AAF710-4209-5EF0-DA63-9FAC3B6D7886";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 4.4408920985006271e-16 4.2632564145606024e-14 0 ;
	setAttr ".sp" -type "double3" 4.4408920985006271e-16 4.2632564145606024e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_CheekBones_002Shape" -p "bpctrl_l_CheekBones_002";
	rename -uid "872973A2-41B7-4543-7679-3FA66A23BCCF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.15120299985026442 0.3650363329099946 8.8817841970012523e-16
		4.4546003163796864e-16 0.39511247956511397 8.8817841970012523e-16
		-0.15120299985026397 0.3650363329099946 8.8817841970012523e-16
		-0.27938671363193279 0.27938671363196477 8.8817841970012523e-16
		-0.36503633291000481 0.15120299985025554 8.8817841970012523e-16
		-0.39511247956512729 0 8.8817841970012523e-16
		-0.36503633291000481 -0.15120299985025554 8.8817841970012523e-16
		-0.27938671363193279 -0.27938671363196477 8.8817841970012523e-16
		-0.15120299985026397 -0.3650363329099946 8.8817841970012523e-16
		4.427183880621566e-16 -0.39511247956511397 8.8817841970012523e-16
		0.15120299985026486 -0.3650363329099946 8.8817841970012523e-16
		0.27938671363193324 -0.27938671363196477 8.8817841970012523e-16
		0.36503633291000526 -0.15120299985025554 8.8817841970012523e-16
		0.39511247956512774 0 8.8817841970012523e-16
		0.36503633291000526 0.15120299985025554 8.8817841970012523e-16
		0.27938671363193324 0.27938671363196477 8.8817841970012523e-16
		0.15120299985026442 0.3650363329099946 8.8817841970012523e-16
		;
createNode joint -n "bpjnt_l_CheekBones_001" -p "l_CheekBones_Rig_Jnt";
	rename -uid "A2619B88-474E-8376-A9D5-76BCBC48505F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.7926734829489368 161.48035919738155 6.3164569490458149 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7926734829489381 161.4803591973816 6.316456949045814 1;
createNode transform -n "bpctrl_l_CheekBones_001" -p "bpjnt_l_CheekBones_001";
	rename -uid "C6A0CCAB-47F1-AAE5-6B08-4EA226348E2C";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 1.1102230246251567e-15 -5.6843418860808027e-14 -3.5527136788005017e-15 ;
	setAttr ".sp" -type "double3" 1.1102230246251567e-15 -5.6843418860808027e-14 -3.5527136788005017e-15 ;
createNode nurbsCurve -n "bpctrl_l_CheekBones_001Shape" -p "bpctrl_l_CheekBones_001";
	rename -uid "8184AF14-4222-52B3-6170-FA8D6B537B92";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.075601499925132654 0.3650363329099377 -0.13094563899874515
		0 0.39511247956505707 -1.7790984829760625e-15
		-0.075601499925131987 0.3650363329099377 0.13094563899874159
		-0.1396933568159664 0.27938671363185102 0.24195599148510022
		-0.18251816645500263 0.15120299985017024 0.3161307376043761
		-0.19755623978256365 -2.8421709430404007e-14 0.34217744465565858
		-0.18251816645500241 -0.15120299985031235 0.3161307376043761
		-0.1396933568159664 -0.27938671363199313 0.24195599148510022
		-0.075601499925131765 -0.36503633291007981 0.13094563899874159
		0 -0.39511247956519918 -1.773615195824438e-15
		0.075601499925132876 -0.36503633291007981 -0.13094563899874515
		0.13969335681596684 -0.27938671363199313 -0.24195599148510466
		0.18251816645500329 -0.15120299985031235 -0.31613073760438054
		0.19755623978256409 -2.8421709430404007e-14 -0.34217744465566213
		0.18251816645500307 0.15120299985017024 -0.31613073760438054
		0.13969335681596662 0.27938671363185102 -0.24195599148510466
		0.075601499925132654 0.3650363329099377 -0.13094563899874515
		;
createNode joint -n "bpjnt_l_CheekBones_003" -p "l_CheekBones_Rig_Jnt";
	rename -uid "AA8A35C7-4D31-79F5-6C0B-08AD571B4FF0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.854151324821439 159.67213633503036 5.1595272197400348 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.8541513248214407 159.67213633503042 5.1595272197400384 1;
createNode transform -n "bpctrl_l_CheekBones_003" -p "bpjnt_l_CheekBones_003";
	rename -uid "81B17731-4701-5D68-E072-3C8EB72B8EFB";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 3.5527136788005017e-15 4.2632564145606024e-14 0 ;
	setAttr ".sp" -type "double3" 3.5527136788005017e-15 4.2632564145606024e-14 0 ;
createNode nurbsCurve -n "bpctrl_l_CheekBones_003Shape" -p "bpctrl_l_CheekBones_003";
	rename -uid "7A89FC38-466A-32F0-4570-2392DDB6BE1C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.13094563899874512 0.3650363329099946 -0.075601499925133112
		0 0.39511247956514239 -8.8817841970012523e-16
		-0.13094563899874156 0.3650363329099946 0.075601499925130447
		-0.24195599148510105 0.27938671363196477 0.13969335681596554
		-0.31613073760437693 0.15120299985025554 0.18251816645500088
		-0.34217744465565936 0 0.19755623978256145
		-0.31613073760437693 -0.15120299985025554 0.18251816645500088
		-0.24195599148510105 -0.27938671363193635 0.13969335681596554
		-0.13094563899874156 -0.3650363329099946 0.075601499925131335
		0 -0.39511247956511397 -8.8817841970012523e-16
		0.13094563899874601 -0.3650363329099946 -0.075601499925133112
		0.24195599148510283 -0.27938671363193635 -0.1396933568159682
		0.31613073760437871 -0.15120299985025554 -0.18251816645500443
		0.34217744465566202 0 -0.1975562397825659
		0.31613073760437871 0.15120299985025554 -0.18251816645500443
		0.24195599148510283 0.27938671363196477 -0.1396933568159682
		0.13094563899874512 0.3650363329099946 -0.075601499925133112
		;
createNode joint -n "bpjnt_l_CheekBones_004" -p "l_CheekBones_Rig_Jnt";
	rename -uid "6573C8D8-4FB0-D3AC-12FF-09A6BA8423FD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.2382294268763081 161.37451486272025 3.2632240772133509 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 7.2382294268763099 161.3745148627203 3.2632240772133532 1;
createNode transform -n "bpctrl_l_CheekBones_004" -p "bpjnt_l_CheekBones_004";
	rename -uid "443EBAB1-4AA8-3E87-46DC-48B1A453335C";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 1.7763568394002509e-15 -2.8421709430404014e-14 8.8817841970012543e-16 ;
	setAttr ".sp" -type "double3" 1.7763568394002509e-15 -2.8421709430404014e-14 8.8817841970012543e-16 ;
createNode nurbsCurve -n "bpctrl_l_CheekBones_004Shape" -p "bpctrl_l_CheekBones_004";
	rename -uid "678691CB-4CFB-17CD-FDAE-7897C58438CD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.075601499925132196 0.36503633290993803 -0.13094563899874379
		-8.8817841970012513e-16 0.39511247956505707 -4.4546003163796844e-16
		-0.075601499925132196 0.36503633290993737 0.13094563899874334
		-0.13969335681596548 0.27938671363185041 0.2419559914851015
		-0.1825181664550026 0.15120299985016944 0.31613073760437782
		-0.19755623978256318 -2.9306572234350357e-14 0.34217744465566025
		-0.1825181664550026 -0.15120299985031316 0.31613073760437782
		-0.13969335681596548 -0.27938671363199374 0.24195599148510194
		-0.075601499925132196 -0.36503633291008014 0.13094563899874334
		-8.8817841970012513e-16 -0.39511247956519918 -4.4271838806215635e-16
		0.075601499925132196 -0.36503633291007948 -0.13094563899874423
		0.13969335681596637 -0.27938671363199252 -0.24195599148510238
		0.18251816645500349 -0.15120299985031155 -0.31613073760437871
		0.19755623978256406 -2.7536846626457648e-14 -0.34217744465566113
		0.18251816645500349 0.15120299985017105 -0.31613073760437871
		0.13969335681596637 0.27938671363185164 -0.24195599148510238
		0.075601499925132196 0.36503633290993803 -0.13094563899874379
		;
createNode transform -n "bpctrl_l_CheekBonesDrv_003" -p "l_CheekBones_Rig_Jnt";
	rename -uid "83D59316-4F86-661D-A5CC-17ABB7011161";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 5.854151324821439 159.67213633503042 5.1595272197400366 ;
	setAttr ".sp" -type "double3" 5.854151324821439 159.67213633503042 5.1595272197400366 ;
createNode nurbsCurve -n "bpctrl_l_CheekBonesDrv_003Shape" -p "bpctrl_l_CheekBonesDrv_003";
	rename -uid "40E956A2-4828-BE6E-CC59-D289031352E7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		5.1392747266806618 160.49760472777831 5.5722614161139772
		5.1392747266806618 158.84666794228252 5.5722614161139772
		6.569027922962217 158.84666794228252 4.746793023366096
		6.569027922962217 160.49760472777831 4.746793023366096
		5.1392747266806618 160.49760472777831 5.5722614161139772
		;
createNode transform -n "r_CheekBones_Rig" -p "CheekBones_Rig";
	rename -uid "501FE10E-4F1B-23F2-2DCA-63885E21D457";
createNode transform -n "r_CheekBones_Rig_Jnt" -p "r_CheekBones_Rig";
	rename -uid "569C56DB-4FE4-5886-1918-DD82F56B4A3C";
createNode joint -n "bpjnt_r_CheekBones_001" -p "r_CheekBones_Rig_Jnt";
	rename -uid "B055E8C9-42FE-E953-5BDD-B08CEC7E9E7F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.7929611828263761 161.4803591973816 6.3164569490458096 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7929611828263761 161.48035919738166 6.3164569490458096 1;
createNode transform -n "bpctrl_r_CheekBones_001" -p "bpjnt_r_CheekBones_001";
	rename -uid "24EC3908-4BF3-6A2C-E3E2-ED99EBE495FA";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" 4.4408920985006271e-16 2.8421709430404014e-14 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 4.4408920985006271e-16 2.8421709430404014e-14 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_r_CheekBones_001Shape" -p "bpctrl_r_CheekBones_001";
	rename -uid "F61835DA-4040-1216-21F0-4F9B3AA6799C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.097191414851186098 0.36503633291002302 -0.11582821781821284
		-2.2204460492503131e-16 0.39511247956517082 0
		0.097191414851185431 0.36503633291002302 0.11582821781821639
		0.17958631783364742 0.27938671363196477 0.21402263945901634
		0.23464083187996199 0.15120299985028396 0.27963405436223976
		0.25397340629698983 0 0.30267371937782883
		0.23464083187996199 -0.15120299985022712 0.27963405436223976
		0.17958631783364742 -0.27938671363190792 0.21402263945901634
		0.097191414851185431 -0.36503633290996618 0.11582821781821639
		-2.2204460492503131e-16 -0.39511247956508555 0
		-0.097191414851186098 -0.36503633290996618 -0.11582821781821284
		-0.17958631783364831 -0.27938671363190792 -0.21402263945901456
		-0.23464083187996265 -0.15120299985022712 -0.27963405436223798
		-0.25397340629698983 0 -0.30267371937782528
		-0.23464083187996265 0.15120299985028396 -0.27963405436223798
		-0.17958631783364831 0.27938671363196477 -0.21402263945901456
		-0.097191414851186098 0.36503633291002302 -0.11582821781821284
		;
createNode joint -n "bpjnt_r_CheekBones_002" -p "r_CheekBones_Rig_Jnt";
	rename -uid "4B5BDA83-4076-EAFA-2E63-22B96C1D191F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.0629611828263741 160.02173594338143 6.1593864997804584 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.062961182826375 160.02173594338143 6.1593864997804584 1;
createNode transform -n "bpctrl_r_CheekBones_002" -p "bpjnt_r_CheekBones_002";
	rename -uid "70EA6ED2-4E0B-C982-4737-468F75CCFCFC";
	setAttr -k on ".ro";
createNode nurbsCurve -n "bpctrl_r_CheekBones_002Shape" -p "bpctrl_r_CheekBones_002";
	rename -uid "1B80C293-493C-4B37-B72D-F4ABE8C9EFEB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.1393713517551762 0.3650363329099946 0.058634234655650097
		9.8607613152626476e-32 0.39511247956511397 4.3790577010150533e-47
		0.13937135175517754 0.3650363329099946 -0.058634234655648321
		0.25752467861007883 0.27938671363193635 -0.10834193860563524
		0.33647220761362101 0.15120299985025554 -0.14155556452503415
		0.36419489313614578 -1.1832913578315177e-30 -0.15321863894988397
		0.33647220761362057 -0.15120299985025554 -0.14155556452503504
		0.25752467861007883 -0.27938671363196477 -0.10834193860563524
		0.13937135175517754 -0.3650363329099946 -0.058634234655648321
		9.8607613152626476e-32 -0.39511247956514239 4.3790577010150533e-47
		-0.13937135175517665 -0.3650363329099946 0.058634234655650097
		-0.25752467861007794 -0.27938671363196477 0.1083419386056379
		-0.33647220761361968 -0.15120299985025554 0.14155556452503504
		-0.36419489313614534 1.1832913578315177e-30 0.15321863894988486
		-0.33647220761361968 0.15120299985025554 0.14155556452503504
		-0.25752467861007794 0.27938671363193635 0.1083419386056379
		-0.1393713517551762 0.3650363329099946 0.058634234655650097
		;
createNode joint -n "bpjnt_r_CheekBones_003" -p "r_CheekBones_Rig_Jnt";
	rename -uid "5FB4EF48-4813-4632-F3D1-A6A741DA45BB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.8539611828263736 159.67213633503042 5.1595272197400366 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.8539611828263771 159.67213633503047 5.1595272197400401 1;
createNode transform -n "bpctrl_r_CheekBones_003" -p "bpjnt_r_CheekBones_003";
	rename -uid "ACA64231-44ED-C930-E88A-E2A95C651BD8";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" -2.6645352591003765e-15 1.4210854715202007e-14 8.8817841970012543e-16 ;
	setAttr ".sp" -type "double3" -2.6645352591003765e-15 1.4210854715202007e-14 8.8817841970012543e-16 ;
createNode nurbsCurve -n "bpctrl_r_CheekBones_003Shape" -p "bpctrl_r_CheekBones_003";
	rename -uid "3EE47B94-4C2F-98DB-4EDD-798493DF74C4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.13094563899874243 0.3650363329099946 -0.075601499925133112
		0 0.39511247956511397 0
		0.13094563899874509 0.3650363329099946 0.075601499925131335
		0.2419559914851028 0.27938671363196477 0.13969335681596465
		0.31613073760437865 0.15120299985025554 0.18251816645500177
		0.34217744465566197 0 0.19755623978256234
		0.31613073760437865 -0.15120299985025554 0.18251816645500177
		0.2419559914851028 -0.27938671363196477 0.13969335681596465
		0.13094563899874509 -0.3650363329099946 0.075601499925131335
		0 -0.39511247956511397 0
		-0.13094563899874331 -0.3650363329099946 -0.075601499925133112
		-0.24195599148510191 -0.27938671363196477 -0.13969335681596731
		-0.31613073760437777 -0.15120299985025554 -0.18251816645500443
		-0.34217744465566019 0 -0.19755623978256501
		-0.31613073760437777 0.15120299985025554 -0.18251816645500443
		-0.24195599148510191 0.27938671363196477 -0.13969335681596731
		-0.13094563899874243 0.3650363329099946 -0.075601499925133112
		;
createNode joint -n "bpjnt_r_CheekBones_004" -p "r_CheekBones_Rig_Jnt";
	rename -uid "42501733-45A9-2A21-9F9A-448D6BEA1980";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.237961182826373 161.37451486272033 3.2632240772133527 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -7.2379611828263766 161.37451486272033 3.2632240772133541 1;
createNode transform -n "bpctrl_r_CheekBones_004" -p "bpjnt_r_CheekBones_004";
	rename -uid "C63151C8-4C08-96F4-92D9-3D821D02834B";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" -1.7763568394002509e-15 5.6843418860808027e-14 -8.8817841970012543e-16 ;
	setAttr ".sp" -type "double3" -1.7763568394002509e-15 5.6843418860808027e-14 -8.8817841970012543e-16 ;
createNode nurbsCurve -n "bpctrl_r_CheekBones_004Shape" -p "bpctrl_r_CheekBones_004";
	rename -uid "DB5C9F5F-47F0-AA4E-F7CB-6B9AB7A513E6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.07560149992513307 0.36503633291002302 -0.13094563899874467
		8.8817841970012513e-16 0.39511247956514239 -8.8680759791221902e-16
		0.075601499925131294 0.36503633291002302 0.1309456389987429
		0.13969335681596545 0.27938671363193635 0.2419559914851015
		0.18251816645500168 0.15120299985025554 0.31613073760437738
		0.19755623978256315 -2.8421709430404007e-14 0.3421774446556598
		0.18251816645500168 -0.15120299985022712 0.31613073760437738
		0.13969335681596545 -0.27938671363190792 0.24195599148510105
		0.075601499925132182 -0.3650363329099946 0.13094563899874245
		8.8817841970012513e-16 -0.39511247956511397 -8.8954924148803125e-16
		-0.07560149992513307 -0.3650363329099946 -0.13094563899874467
		-0.13969335681596634 -0.27938671363190792 -0.24195599148510283
		-0.18251816645500346 -0.15120299985022712 -0.3161307376043796
		-0.19755623978256492 -2.8421709430404007e-14 -0.34217744465566158
		-0.18251816645500346 0.15120299985025554 -0.31613073760437915
		-0.13969335681596634 0.27938671363193635 -0.24195599148510283
		-0.07560149992513307 0.36503633291002302 -0.13094563899874467
		;
createNode transform -n "bpctrl_r_CheekBonesDrv_003" -p "r_CheekBones_Rig_Jnt";
	rename -uid "D5EE7912-42C7-9DC4-743D-D9A21D9F39EB";
	setAttr -k on ".ro";
	setAttr ".rp" -type "double3" -5.8539611828263762 159.6721363350305 5.1595272197400401 ;
	setAttr ".sp" -type "double3" -5.8539611828263762 159.6721363350305 5.1595272197400401 ;
createNode nurbsCurve -n "bpctrl_r_CheekBonesDrv_003Shape" -p "bpctrl_r_CheekBonesDrv_003";
	rename -uid "F559EAC1-4AF2-2794-7CAD-1CA8F932FAC0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-5.139084584685599 160.49760472777837 5.5722614161139807
		-5.139084584685599 158.84666794228264 5.5722614161139807
		-6.5688377809671534 158.84666794228264 4.7467930233660987
		-6.5688377809671534 160.49760472777837 4.7467930233660987
		-5.139084584685599 160.49760472777837 5.5722614161139807
		;
createNode transform -n "r_CheekBones_Rig_Crv" -p "r_CheekBones_Rig";
	rename -uid "8C0573A4-4C10-CAC8-054E-E4A211EB43D5";
createNode transform -n "crv_r_CheekBonesAim_001" -p "r_CheekBones_Rig_Crv";
	rename -uid "08A039AD-4597-C25E-A065-259D490DED5A";
	setAttr ".rp" -type "double3" -4.5088623085629527 160.69846919459218 4.6065434522080917 ;
	setAttr ".sp" -type "double3" -4.5088623085629527 160.69846919459218 4.6065434522080917 ;
createNode nurbsCurve -n "crv_r_CheekBonesAim_00Shape1" -p "crv_r_CheekBonesAim_001";
	rename -uid "FD244927-48B3-B6A4-162C-749718FF1CD3";
	setAttr -k off ".v";
createNode transform -n "crv_r_CheekBones_001" -p "r_CheekBones_Rig_Crv";
	rename -uid "9AF5EE62-4981-6EE3-69F1-CABC2FEAA2B5";
	setAttr ".rp" -type "double3" -4.5088623085629527 160.69846919459218 3.8370690976982509 ;
	setAttr ".sp" -type "double3" -4.5088623085629527 160.69846919459218 3.8370690976982509 ;
createNode nurbsCurve -n "crv_r_CheekBones_00Shape1" -p "crv_r_CheekBones_001";
	rename -uid "C00371C5-48C7-369C-0E36-D98E107CA1C3";
	setAttr -k off ".v";
createNode transform -n "Brow_Rig" -p "Face_Rig";
	rename -uid "8A87451A-41DC-950C-70F0-1A8F9319A9C7";
createNode transform -n "Brow_Rig_Jnt" -p "Brow_Rig";
	rename -uid "90C3DBD0-4EF9-F1E4-20B5-498E9B74CDA7";
createNode transform -n "zero_l_BrowInnY_001" -p "Brow_Rig_Jnt";
	rename -uid "4A5BB664-4B21-7974-D6FB-18AD3C43F15C";
	setAttr ".t" -type "double3" 1.7017547488212585 165.37956237792969 6.7807900905609131 ;
	setAttr ".r" -type "double3" -7.0000000000000018 0 0 ;
createNode transform -n "loc_l_BrowInnY_001" -p "zero_l_BrowInnY_001";
	rename -uid "7F318A89-4D0B-763C-DF23-038B069BD47B";
	setAttr ".t" -type "double3" 0 8.5265128291212022e-14 0 ;
	setAttr ".rp" -type "double3" 0.088415348568436913 -0.034491316922015125 0.32816295970187526 ;
	setAttr ".sp" -type "double3" 0.088415348568436913 -0.034491316922015125 0.32816295970187526 ;
createNode locator -n "loc_l_BrowInnY_00Shape1" -p "loc_l_BrowInnY_001";
	rename -uid "9A0E54AA-48E2-A5C2-1B9D-0EA7ABEDED42";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -2.2204460492503131e-16 2.8421709430404007e-14 -3.5527136788005009e-15 ;
createNode transform -n "zero_l_BrowInnX_001" -p "loc_l_BrowInnY_001";
	rename -uid "4EB0817A-43D0-6455-A1FA-0CACEB236C52";
	setAttr ".t" -type "double3" -4.4408920985006262e-16 0 0 ;
	setAttr ".r" -type "double3" 6.2100311918653004 14.915914679729724 1.6043389449783447 ;
	setAttr ".s" -type "double3" 1 1.0000000000000004 1.0000000000000004 ;
createNode transform -n "loc_l_BrowInnX_001" -p "zero_l_BrowInnX_001";
	rename -uid "F46AB774-4393-A2AA-03BF-229A4B09B502";
	setAttr ".t" -type "double3" 3.7470027081099033e-15 0 -7.9936057773011271e-15 ;
	setAttr ".rp" -type "double3" -3.8857805861880479e-16 -2.8421709430404007e-14 0.34161067449041038 ;
	setAttr ".sp" -type "double3" -3.8857805861880479e-16 -2.8421709430404007e-14 0.34161067449041038 ;
createNode locator -n "loc_l_BrowInnX_00Shape1" -p "loc_l_BrowInnX_001";
	rename -uid "C198C364-4147-257F-FF03-BE89120A8136";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -3.3306690738754696e-16 -2.8421709430404007e-14 1.7763568394002505e-15 ;
createNode joint -n "bpjnt_l_BrowInn_001" -p "loc_l_BrowInnX_001";
	rename -uid "BDEEB3F5-47F4-F39F-A678-EA8E522A9FFA";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.2204460492503131e-15 -2.8421709430404007e-14 1.7763568394002505e-15 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 -2.6020852139652106e-18 -2.7755575615628914e-17 0
		 1.5612511283791264e-17 1.0000000000000004 -3.4694469519536142e-18 0 2.4980018054066022e-16 2.0816681711721685e-17 1.0000000000000004 0
		 1.7017547488212637 165.37956237792977 6.7807900905608998 1;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[6]', u'crv_m_BrowSpans_001.cv[7]']";
createNode transform -n "bpctrl_l_BrowInn_001" -p "bpjnt_l_BrowInn_001";
	rename -uid "2570587D-4F9A-9FE5-DBDC-3DA6278DB276";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0.2551164831025281 -0.014387985918403956 0.77806114855885511 ;
	setAttr ".sp" -type "double3" 0.2551164831025281 -0.014387985918403956 0.77806114855885511 ;
createNode nurbsCurve -n "bpctrl_l_BrowInn_001Shape" -p "bpctrl_l_BrowInn_001";
	rename -uid "A51E1498-49F0-F81C-5B81-84A795BBC158";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.35489657301215771 0.58996793445462015 0.79994501088272862
		-0.34940940936517284 -0.6246234982312836 0.7794666373627358
		0.86512953921721525 -0.61874390629134279 0.75617728623497193
		0.85964237557023038 0.59584752639456096 0.77665565975496476
		-0.35489657301215771 0.58996793445462015 0.79994501088272862
		;
createNode transform -n "zero_l_BrowMidY_001" -p "Brow_Rig_Jnt";
	rename -uid "3678F432-434F-3F5F-0D22-39991CB39BE9";
	setAttr ".t" -type "double3" 3.9642400741577148 165.50798034667969 5.9961657524108887 ;
	setAttr ".r" -type "double3" -5 25.000000000000028 1.0966730642436331e-16 ;
createNode transform -n "loc_l_BrowMidY_001" -p "zero_l_BrowMidY_001";
	rename -uid "132377FC-4972-7AB4-9982-5793006C8A8E";
	setAttr ".rp" -type "double3" 2.1094237467877974e-15 -0.029711634738784354 0.3396055390648467 ;
	setAttr ".sp" -type "double3" 2.1094237467877974e-15 -0.029711634738784354 0.3396055390648467 ;
createNode locator -n "loc_l_BrowMidY_00Shape1" -p "loc_l_BrowMidY_001";
	rename -uid "0E4D1F37-48B7-D37D-C2AB-6EABBD1CDFDD";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -2.2204460492503131e-16 0 0 ;
createNode transform -n "zero_l_BrowMidX_001" -p "loc_l_BrowMidY_001";
	rename -uid "57416F75-4B58-116D-F4D7-60B350FDEB38";
	setAttr ".t" -type "double3" -4.4408920985006262e-16 0 0 ;
	setAttr ".r" -type "double3" 5 -2.5394207389025938e-14 -1.7056571794041157e-15 ;
	setAttr ".s" -type "double3" 1 1.0000000000000004 1.0000000000000004 ;
createNode transform -n "loc_l_BrowMidX_001" -p "zero_l_BrowMidX_001";
	rename -uid "F872E707-4798-E907-7AF5-4DAA0E901288";
	setAttr ".t" -type "double3" 5.1070259132757201e-15 0 -7.9936057773011271e-15 ;
	setAttr ".rp" -type "double3" -2.2204460492503131e-16 0 0.34090277705290317 ;
	setAttr ".sp" -type "double3" -2.2204460492503131e-16 0 0.34090277705290317 ;
createNode locator -n "loc_l_BrowMidX_00Shape1" -p "loc_l_BrowMidX_001";
	rename -uid "A254110B-426E-B7AA-4DBB-C9AA2DAC0F4A";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -2.2204460492503131e-16 0 -2.6645352591003757e-15 ;
createNode joint -n "bpjnt_l_BrowMid_001" -p "loc_l_BrowMidX_001";
	rename -uid "689684BB-4217-AFAE-FE6C-8EB4C7E83BA5";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.8318679906315083e-15 8.5265128291212022e-14 5.3290705182007514e-15 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 -1.1102230246251565e-16 0 -6.9388939039072284e-18 1.0000000000000004 -1.3877787807814457e-17 0
		 4.4408920985006262e-16 0 1.0000000000000004 0 3.9642400741577171 165.50798034667969 5.9961657524108798 1;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[5]']";
createNode transform -n "bpctrl_l_BrowMid_001" -p "bpjnt_l_BrowMid_001";
	rename -uid "D36E55E6-42C2-8014-AB0C-628BCA472A32";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0.45487637046246099 0.00034732234607304235 0.68802949950691072 ;
	setAttr ".sp" -type "double3" 0.45487637046246099 0.00034732234607304235 0.68802949950691072 ;
createNode nurbsCurve -n "bpctrl_l_BrowMid_001Shape" -p "bpctrl_l_BrowMid_001";
	rename -uid "F6249C85-48FD-5B26-539C-6A85581324D9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.016970540286910307 0.4727603858551106 0.71115081846114103
		-0.016970540286910307 -0.47206574116276556 0.71115081846114103
		0.92672328121183178 -0.47206574116276556 0.66490818055268452
		0.92672328121183178 0.4727603858551106 0.66490818055268452
		-0.016970540286910307 0.4727603858551106 0.71115081846114103
		;
createNode transform -n "zero_l_BrowOutY_001" -p "Brow_Rig_Jnt";
	rename -uid "4891BC80-4E52-4F52-8122-0DA84F5C3938";
	setAttr ".t" -type "double3" 5.8498179912567139 165.44327545166016 4.6453540325164795 ;
	setAttr ".r" -type "double3" -4 50.000000000000057 3.0925404378657673e-16 ;
createNode transform -n "loc_l_BrowOutY_001" -p "zero_l_BrowOutY_001";
	rename -uid "900B2870-4A1F-A0C8-DC3D-C7B2C7D1088A";
	setAttr ".t" -type "double3" 0 5.6843418860808015e-14 0 ;
	setAttr ".rp" -type "double3" 1.7763568394002505e-15 -0.023560250836954344 0.33692728414370066 ;
	setAttr ".sp" -type "double3" 1.7763568394002505e-15 -0.023560250836954344 0.33692728414370066 ;
createNode locator -n "loc_l_BrowOutY_00Shape1" -p "loc_l_BrowOutY_001";
	rename -uid "C4B83708-405D-BD8C-69E1-57A2D788A7E1";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -2.4980018054066022e-16 -2.8421709430404007e-14 3.5527136788005009e-15 ;
createNode transform -n "zero_l_BrowOutX_001" -p "loc_l_BrowOutY_001";
	rename -uid "807F3807-4188-14B6-3B8A-ADA4C6E87EDC";
	setAttr ".t" -type "double3" -4.4408920985006262e-16 0 0 ;
	setAttr ".r" -type "double3" 3.9999999999999991 -4.4417390610608536e-14 -3.9379594867655006e-15 ;
	setAttr ".s" -type "double3" 1 1.0000000000000004 1.0000000000000004 ;
createNode transform -n "loc_l_BrowOutX_001" -p "zero_l_BrowOutX_001";
	rename -uid "AC55BF22-4930-C139-959C-468E42F1D45D";
	setAttr ".t" -type "double3" 4.0245584642661925e-15 0 -8.8817841970012523e-15 ;
	setAttr ".rp" -type "double3" 2.2204460492503131e-16 0 0.33775002623235451 ;
	setAttr ".sp" -type "double3" 2.2204460492503131e-16 0 0.33775002623235451 ;
createNode locator -n "loc_l_BrowOutX_00Shape1" -p "loc_l_BrowOutX_001";
	rename -uid "098BD978-4DD1-9E21-ED3B-C994565E623B";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 1.9428902930940239e-16 0 0 ;
createNode joint -n "bpjnt_l_BrowOut_001" -p "loc_l_BrowOutX_001";
	rename -uid "C89941DB-4888-8E55-D200-8D8F8CCCD31A";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -6.6613381477509392e-16 -2.8421709430404007e-14 0 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 -6.9388939039072284e-18 1.0000000000000004 0 0
		 2.7755575615628914e-16 0 1.0000000000000002 0 5.8498179912567076 165.44327545166018 4.6453540325164671 1;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[3]', u'crv_m_BrowSpans_001.cv[4]']";
createNode transform -n "bpctrl_l_BrowOut_001" -p "bpjnt_l_BrowOut_001";
	rename -uid "3F263DE1-4399-F65C-7209-C2B2468804AD";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0.69056886651543326 -0.0070772350082108915 0.43637059186062288 ;
	setAttr ".sp" -type "double3" 0.69056886651543326 -0.0070772350082108915 0.43637059186062288 ;
createNode nurbsCurve -n "bpctrl_l_BrowOut_001Shape" -p "bpctrl_l_BrowOut_001";
	rename -uid "00C348F9-48F5-4372-7788-D98A50CB514F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		0.083649450522534807 0.60031098950327078 0.4125110494073092
		0.083649450522534807 -0.61446545951986309 0.4125110494073092
		1.297488282508328 -0.61446545951986309 0.46023013431394133
		1.297488282508328 0.60031098950327078 0.46023013431394133
		0.083649450522534807 0.60031098950327078 0.4125110494073092
		;
createNode transform -n "zero_r_BrowInnY_001" -p "Brow_Rig_Jnt";
	rename -uid "DF2E44B1-4486-EB5C-A0FB-22A84B03B64D";
	setAttr ".t" -type "double3" -1.702 165.37956237792969 6.7807900905609131 ;
	setAttr ".r" -type "double3" -7 -15.000000000000002 0 ;
createNode transform -n "loc_r_BrowInnY_001" -p "zero_r_BrowInnY_001";
	rename -uid "63AA0C90-47E8-91F5-522A-8B875656D5EF";
	setAttr ".t" -type "double3" 0 5.6843418860808015e-14 0 ;
	setAttr ".rp" -type "double3" -1.8873791418627661e-15 -0.041649755224625107 0.33921003518969206 ;
	setAttr ".sp" -type "double3" -1.8873791418627661e-15 -0.041649755224625107 0.33921003518969206 ;
createNode locator -n "loc_r_BrowInnY_00Shape1" -p "loc_r_BrowInnY_001";
	rename -uid "6F10223B-427D-DC7A-9B72-E5B794B87DD8";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 3.8857805861880479e-16 -2.8421709430404007e-14 -7.1054273576010019e-15 ;
createNode transform -n "zero_r_BrowInnX_001" -p "loc_r_BrowInnY_001";
	rename -uid "779CA47E-422E-84CD-8363-7B8EB547A2EF";
	setAttr ".t" -type "double3" -4.4408920985006262e-16 0 0 ;
	setAttr ".r" -type "double3" 7.0000000000000009 3.1018092240220258e-15 1.3846515829087174e-15 ;
	setAttr ".s" -type "double3" 1 1.0000000000000004 1.0000000000000004 ;
createNode transform -n "loc_r_BrowInnX_001" -p "zero_r_BrowInnX_001";
	rename -uid "EE815316-41EC-4524-525E-36A0BED76329";
	setAttr ".t" -type "double3" -4.1910919179599659e-15 0 -1.3322676295501878e-14 ;
	setAttr ".rp" -type "double3" 4.4408920985006262e-16 0 0.34175744334786962 ;
	setAttr ".sp" -type "double3" 4.4408920985006262e-16 0 0.34175744334786962 ;
createNode locator -n "loc_r_BrowInnX_00Shape1" -p "loc_r_BrowInnX_001";
	rename -uid "3EF55697-4BB5-9296-73B4-70A2B9338A47";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 3.8857805861880479e-16 0 -6.2172489379008766e-15 ;
createNode joint -n "bpjnt_r_BrowInn_001" -p "loc_r_BrowInnX_001";
	rename -uid "A2B1541F-4067-BE4D-DBF9-9A8B44A4AEFD";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00023689444747565513 -8.5265128291212022e-14 -6.3475675888824412e-05 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 6.9430642023858262e-18 5.5511151231257827e-17 0 -6.9388939039072284e-18 1.0000000000000004 2.7755575615628914e-17 0
		 -2.2204460492503131e-16 -1.2506954708189052e-17 1.0000000000000004 0 -1.7017547488212579 165.37956237792972 6.7807900905608918 1;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[9]', u'crv_m_BrowSpans_001.cv[10]']";
createNode transform -n "bpctrl_r_BrowInn_001" -p "bpjnt_r_BrowInn_001";
	rename -uid "8E2A13A1-4D92-0133-EC3D-4AB6ED5EE677";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -0.25511648310252877 -0.014387985918290269 0.77806114855885333 ;
	setAttr ".sp" -type "double3" -0.25511648310252877 -0.014387985918290269 0.77806114855885333 ;
createNode nurbsCurve -n "bpctrl_r_BrowInn_001Shape" -p "bpctrl_r_BrowInn_001";
	rename -uid "A63682CB-4A14-6763-1B4E-8AA0BEBF9334";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.86237567693352457 0.5930002385931914 0.7905802053510318
		-0.86237567693352457 -0.62177621042980036 0.7905802053510318
		0.3521427107284677 -0.62177621042980036 0.76554209176666665
		0.3521427107284677 0.5930002385931914 0.76554209176666665
		-0.86237567693352457 0.5930002385931914 0.7905802053510318
		;
createNode transform -n "zero_r_BrowMidY_001" -p "Brow_Rig_Jnt";
	rename -uid "869278FD-488B-4018-2443-FA8309ADBF83";
	setAttr ".t" -type "double3" -3.964 165.50798034667969 5.9961657524108887 ;
	setAttr ".r" -type "double3" -5 -25 -2.1933461284872663e-16 ;
createNode transform -n "loc_r_BrowMidY_001" -p "zero_r_BrowMidY_001";
	rename -uid "1B72E0C2-438B-2082-03C6-38B414DD5A13";
	setAttr ".rp" -type "double3" -2.7755575615628914e-15 -0.029716056137608415 0.33965607588400881 ;
	setAttr ".sp" -type "double3" -2.7755575615628914e-15 -0.029716056137608415 0.33965607588400881 ;
createNode locator -n "loc_r_BrowMidY_00Shape1" -p "loc_r_BrowMidY_001";
	rename -uid "8DA2AF1D-4777-5410-EFB3-2AB9D42D7158";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 4.4408920985006262e-16 -2.8421709430404007e-14 -3.5527136788005009e-15 ;
createNode transform -n "zero_r_BrowMidX_001" -p "loc_r_BrowMidY_001";
	rename -uid "85BE69D6-41B1-92B7-59B8-37AB8C3EEDE5";
	setAttr ".t" -type "double3" -1.7763568394002505e-15 -2.8421709430404007e-14 3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" 4.9999999999999982 -4.3354327089809347e-17 9.9297734317499307e-16 ;
createNode transform -n "loc_r_BrowMidX_001" -p "zero_r_BrowMidX_001";
	rename -uid "143C7C5C-4747-1373-EE5A-D2A076B3AE31";
	setAttr ".t" -type "double3" -4.6629367034256575e-15 0 -1.4210854715202004e-14 ;
	setAttr ".rp" -type "double3" 4.4408920985006262e-16 -2.8421709430404007e-14 0.34095350691450976 ;
	setAttr ".sp" -type "double3" 4.4408920985006262e-16 -2.8421709430404007e-14 0.34095350691450976 ;
createNode locator -n "loc_r_BrowMidX_00Shape1" -p "loc_r_BrowMidX_001";
	rename -uid "BDC64090-4442-8F31-E350-95B98D84D2AA";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 4.4408920985006262e-16 -2.8421709430404007e-14 -1.7763568394002505e-15 ;
createNode joint -n "bpjnt_r_BrowMid_001" -p "loc_r_BrowMidX_001";
	rename -uid "5BA86B45-4857-B532-93E1-D091FB5FFEDA";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.00021758107860307685 -2.8421709430404007e-14 0.00010145972321318197 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 -2.0739406469700583e-17 -5.5511151231257827e-17 0
		 2.0816681711721685e-17 1 -2.7755575615628914e-17 0 0 3.6266389831157357e-17 1 0 -3.9642400741577135 165.50798034667969 5.9961657524108736 1;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[11]']";
createNode transform -n "bpctrl_r_BrowMid_001" -p "bpjnt_r_BrowMid_001";
	rename -uid "E3A91F5C-4241-87E9-E83E-5E81CDC2517D";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -0.45487637046246104 0.00034732234618672925 0.68802949950691439 ;
	setAttr ".sp" -type "double3" -0.45487637046246104 0.00034732234618672925 0.68802949950691439 ;
createNode nurbsCurve -n "bpctrl_r_BrowMid_001Shape" -p "bpctrl_r_BrowMid_001";
	rename -uid "14A86D40-4A14-6005-556E-34B5508811CA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.92609675096457278 0.4727603858551106 0.72157730976853274
		-0.92609675096457389 -0.47206574116276556 0.72157730976853507
		0.016344010039652634 -0.47206574116276556 0.65448168924528538
		0.016344010039652634 0.4727603858551106 0.65448168924528538
		-0.92609675096457278 0.4727603858551106 0.72157730976853274
		;
createNode transform -n "zero_r_BrowOutY_001" -p "Brow_Rig_Jnt";
	rename -uid "C5BB4BA0-4262-CA74-2184-87A01627285B";
	setAttr ".t" -type "double3" -5.85 165.44327545166016 4.6453540325164795 ;
	setAttr ".r" -type "double3" -5 -50.000000000000036 0 ;
createNode transform -n "loc_r_BrowOutY_001" -p "zero_r_BrowOutY_001";
	rename -uid "F4793918-4CC2-5152-068F-5CB7914182DB";
	setAttr ".t" -type "double3" -4.145989107584569e-16 2.8421709430404007e-14 3.3818434164167854e-15 ;
	setAttr ".rp" -type "double3" -3.9968028886505635e-15 -0.02943077847675768 0.33639533730032301 ;
	setAttr ".sp" -type "double3" -3.9968028886505635e-15 -0.02943077847675768 0.33639533730032301 ;
createNode locator -n "loc_r_BrowOutY_00Shape1" -p "loc_r_BrowOutY_001";
	rename -uid "F0C3E702-465F-FF28-29AB-CB88B371D889";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -4.7184478546569153e-16 0 3.5527136788005009e-15 ;
createNode transform -n "zero_r_BrowOutX_001" -p "loc_r_BrowOutY_001";
	rename -uid "710BC2F0-4BE1-B3EC-89CB-2EA29F06C791";
	setAttr ".t" -type "double3" -4.4408920985006262e-16 0 0 ;
	setAttr ".r" -type "double3" 5.0000000000000018 3.8095646516247891e-14 2.4591880347886756e-15 ;
	setAttr ".s" -type "double3" 1 1.0000000000000004 1.0000000000000004 ;
createNode transform -n "loc_r_BrowOutX_001" -p "zero_r_BrowOutX_001";
	rename -uid "04623AC8-4689-DABC-E13F-7DB87376B767";
	setAttr ".t" -type "double3" -7.1331829332166308e-15 0 -7.1054273576010019e-15 ;
	setAttr ".rp" -type "double3" 0 0 0.33768031283915678 ;
	setAttr ".sp" -type "double3" 0 0 0.33768031283915678 ;
createNode locator -n "loc_r_BrowOutX_00Shape1" -p "loc_r_BrowOutX_001";
	rename -uid "D7A20075-422B-D98A-899D-DD8C54608F21";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -2.7755575615628914e-17 0 0 ;
createNode joint -n "bpjnt_r_BrowOut_001" -p "loc_r_BrowOutX_001";
	rename -uid "60BEC7CA-47D2-DD03-F987-82B0B80D828D";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00011699296503508982 -1.4210854715202004e-13 -0.00013942678639722317 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1.0000000000000004 6.1707672065995459e-18 2.2204460492503131e-16 0
		 -1.3877787807814457e-17 1.0000000000000004 6.9388939039072284e-18 0 -6.6613381477509392e-16 -1.4235971169202336e-17 1.0000000000000002 0
		 -5.8498179912567121 165.4432754516601 4.6453540325164671 1;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[12]', u'crv_m_BrowSpans_001.cv[13]']";
createNode transform -n "bpctrl_r_BrowOut_001" -p "bpjnt_r_BrowOut_001";
	rename -uid "B16BAA02-4113-4A21-6B73-3E8215878073";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -0.69056886651543015 -0.0070772350082677349 0.43637059186062821 ;
	setAttr ".sp" -type "double3" -0.69056886651543015 -0.0070772350082677349 0.43637059186062821 ;
createNode nurbsCurve -n "bpctrl_r_BrowOut_001Shape" -p "bpctrl_r_BrowOut_001";
	rename -uid "6B7A5213-43F0-14C0-CE96-3491CFAF8996";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-1.2978354471914542 0.60031098950324235 0.44852605438959031
		-1.2978354471914542 -0.61446545951989151 0.44852605438959031
		-0.083302285839412238 -0.61446545951989151 0.42421512933165967
		-0.083302285839412238 0.60031098950324235 0.42421512933165967
		-1.2978354471914542 0.60031098950324235 0.44852605438959031
		;
createNode transform -n "zero_m_BrowInnY_001" -p "Brow_Rig_Jnt";
	rename -uid "3E7B8860-486E-F28A-2615-5097FBFE0BCC";
	setAttr ".t" -type "double3" 1.6125067908396671e-19 165.36941528320312 7.0148272514343262 ;
	setAttr ".r" -type "double3" -9.8292072823602084 0 0 ;
createNode transform -n "loc_m_BrowInnY_001" -p "zero_m_BrowInnY_001";
	rename -uid "561E9DA2-4AD9-0BE1-2D40-D695A39D1797";
	setAttr ".t" -type "double3" 0 2.8421709430404007e-14 0 ;
	setAttr ".rp" -type "double3" -6.6613381477509392e-16 -0.057919207063959366 0.33430032758793271 ;
	setAttr ".sp" -type "double3" -6.6613381477509392e-16 -0.057919207063959366 0.33430032758793271 ;
createNode locator -n "loc_m_BrowInnY_00Shape1" -p "loc_m_BrowInnY_001";
	rename -uid "5718179A-47C6-52BA-E7E9-DC9D5707C7AF";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -2.2204460492503131e-16 2.8421709430404007e-14 -3.5527136788005009e-15 ;
createNode transform -n "zero_m_BrowInnX_001" -p "loc_m_BrowInnY_001";
	rename -uid "5B2C71F3-4C0C-FA42-DA5C-428EE07101CF";
	setAttr ".t" -type "double3" -4.4408920985006262e-16 0 0 ;
	setAttr ".r" -type "double3" 9.8292072823602084 0 0 ;
	setAttr ".s" -type "double3" 1 1.0000000000000004 1.0000000000000004 ;
createNode transform -n "loc_m_BrowInnX_001" -p "zero_m_BrowInnX_001";
	rename -uid "1F6AE6B3-4AC7-3582-EBB6-A5B82A32DDFA";
	setAttr ".t" -type "double3" -1.2874223171907562e-16 0 -9.7699626167013776e-15 ;
	setAttr ".rp" -type "double3" -3.8857805861880479e-16 -2.8421709430404007e-14 0.33928062657971414 ;
	setAttr ".sp" -type "double3" -3.8857805861880479e-16 -2.8421709430404007e-14 0.33928062657971414 ;
createNode locator -n "loc_m_BrowInnX_00Shape1" -p "loc_m_BrowInnX_001";
	rename -uid "8E199187-41FC-D06C-ACAB-8D85EDFA568B";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" -3.3306690738754696e-16 -2.8421709430404007e-14 1.7763568394002505e-15 ;
createNode joint -n "bpjnt_m_BrowInn_001" -p "loc_m_BrowInnX_001";
	rename -uid "0B7B30E1-417C-7F26-6AA8-91A3729451AA";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.440889980918258e-16 -5.6843418860808015e-14 -5.3290705182007514e-15 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1.0000000000000004 2.7755575615628914e-17 0
		 0 -2.7755575615628914e-17 1.0000000000000004 0 -1.2858098103999155e-16 165.3694152832031 7.0148272514343102 1;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[8]']";
createNode transform -n "bpctrl_m_BrowInn_001" -p "bpjnt_m_BrowInn_001";
	rename -uid "CF55664D-4A1F-4C51-3E09-56A4A4251463";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 3.8817173624750012e-05 -0.0051120691611856728 0.81256125315942818 ;
	setAttr ".sp" -type "double3" 3.8817173624750012e-05 -0.0051120691611856728 0.81256125315942818 ;
createNode nurbsCurve -n "bpctrl_m_BrowInn_001Shape" -p "bpctrl_m_BrowInn_001";
	rename -uid "691E31D0-4176-F664-CEC4-B699AD6334F9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.78928960974191098 0.784216357754417 0.81256125315942818
		-0.78928960974191098 -0.79444049607670308 0.81256125315942818
		0.78936724408916048 -0.79444049607670308 0.81256125315942818
		0.78936724408916048 0.784216357754417 0.81256125315942818
		-0.78928960974191098 0.784216357754417 0.81256125315942818
		;
createNode joint -n "bpjnt_l_BrowOutCrv_002" -p "Brow_Rig_Jnt";
	rename -uid "6F909A5E-4500-7FE9-A9CB-14B7455A5F31";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.5703611373901349 165.96333312988267 -0.19052010774612249 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 7.5703611373901376 165.96333312988276 -0.19052010774612249 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "BrowOutCrv002";
	setAttr ".radi" 2.4;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[0]']";
createNode joint -n "bpjnt_r_BrowOutCrv_002" -p "Brow_Rig_Jnt";
	rename -uid "6D053CC4-4FE3-4258-9B93-71A65E3BFE59";
	addAttr -ci true -sn "MeshPosInfo" -ln "MeshPosInfo" -dt "string";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -7.5703611373901314 165.9633331298827 -0.19052010774612427 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -7.5703611373901349 165.96333312988276 -0.1905201077461243 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "BrowOutCrv002";
	setAttr ".radi" 2.4;
	setAttr -l on -k on ".MeshPosInfo" -type "string" "[u'crv_m_BrowSpans_001.cv[16]']";
createNode transform -n "bpctrl_l_BrowInnDrv_001" -p "Brow_Rig_Jnt";
	rename -uid "73773AFB-4F62-6F16-DCC5-D7B716230603";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.9134288620189404 165.39000262215794 7.5782692996409109 ;
	setAttr ".sp" -type "double3" 1.9134288620189404 165.39000262215794 7.5782692996409109 ;
createNode nurbsCurve -n "bpctrl_l_BrowInnDrv_001Shape" -p "bpctrl_l_BrowInnDrv_001";
	rename -uid "24CF4563-45CF-FA57-3575-13A5E4020BCE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		2.3448286669056779 166.4314938819206 7.5782692996409109
		1.9134288620189408 166.51730463839775 7.5782692996409109
		1.4820290571322028 166.4314938819206 7.5782692996409109
		1.1163059618905014 166.18712552228638 7.5782692996409109
		0.87193760225627193 165.82140242704469 7.5782692996409109
		0.78612684577912773 165.39000262215794 7.5782692996409109
		0.87193760225627215 164.95860281727118 7.5782692996409109
		1.1163059618905014 164.59287972202949 7.5782692996409109
		1.482029057132203 164.34851136239527 7.5782692996409109
		1.9134288620189406 164.26270060591813 7.5782692996409109
		2.3448286669056788 164.34851136239527 7.5782692996409109
		2.7105517621473796 164.59287972202949 7.5782692996409109
		2.9549201217816101 164.95860281727121 7.5782692996409109
		3.0407308782587528 165.39000262215794 7.5782692996409109
		2.9549201217816092 165.82140242704469 7.5782692996409109
		2.7105517621473796 166.18712552228638 7.5782692996409109
		2.3448286669056779 166.4314938819206 7.5782692996409109
		;
createNode transform -n "bpctrl_l_Brow_001" -p "Brow_Rig_Jnt";
	rename -uid "2EBA6FED-4C8B-B203-3ADD-3799A1FD8123";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 4.1819268649525583 167.79598383364942 6.3676026504934864 ;
	setAttr ".sp" -type "double3" 4.1819268649525583 167.79598383364942 6.3676026504934864 ;
createNode nurbsCurve -n "bpctrl_l_Brow_001Shape" -p "bpctrl_l_Brow_001";
	rename -uid "16E77CF7-4579-179D-C1C0-F88569F0D45E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		1.5534203218548752 168.0301103387589 7.422825628204933
		1.5534203218548757 167.56185732853993 7.4228256282049347
		6.8104334080502422 167.56185732853993 5.3123796727820398
		6.8104334080502404 168.0301103387589 5.312379672782038
		1.5534203218548752 168.0301103387589 7.422825628204933
		;
createNode transform -n "bpctrl_l_BrowOutDrv_001" -p "Brow_Rig_Jnt";
	rename -uid "6C92D4D9-4744-D96D-6632-20B362C15540";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 6.4504248678861789 165.45371569588846 5.1569360013460663 ;
	setAttr ".sp" -type "double3" 6.4504248678861789 165.45371569588846 5.1569360013460663 ;
createNode nurbsCurve -n "bpctrl_l_BrowOutDrv_001Shape" -p "bpctrl_l_BrowOutDrv_001";
	rename -uid "351E7576-4594-5264-4B6A-819E6464B201";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		6.7277233172885644 166.49520695565113 4.8264645780499693
		6.4504248678861797 166.58101771212827 5.1569360013460654
		6.1731264184837942 166.49520695565113 5.4874074246421625
		5.9380441442862173 166.25083859601691 5.7675675694723401
		5.7809671905139108 165.88511550077519 5.9547645934442421
		5.7258090994725732 165.45371569588846 6.0204994466033952
		5.7809671905139108 165.02231589100171 5.9547645934442421
		5.9380441442862173 164.65659279576002 5.7675675694723409
		6.1731264184837942 164.4122244361258 5.4874074246421625
		6.4504248678861797 164.32641367964865 5.1569360013460654
		6.7277233172885653 164.4122244361258 4.8264645780499684
		6.9628055914861413 164.65659279576002 4.5463044332197908
		7.1198825452584487 165.02231589100171 4.3591074092478888
		7.1750406362997854 165.45371569588846 4.2933725560887366
		7.1198825452584478 165.88511550077519 4.3591074092478888
		6.9628055914861404 166.25083859601691 4.5463044332197908
		6.7277233172885644 166.49520695565113 4.8264645780499693
		;
createNode transform -n "bpctrl_r_BrowInnDrv_001" -p "Brow_Rig_Jnt";
	rename -uid "7AD2BB81-420E-E764-E5BD-26B6D8307198";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.9101856674147641 165.39000262215791 7.5655399780679549 ;
	setAttr ".sp" -type "double3" -1.9101856674147641 165.39000262215791 7.5655399780679549 ;
createNode nurbsCurve -n "bpctrl_r_BrowInnDrv_001Shape" -p "bpctrl_r_BrowInnDrv_001";
	rename -uid "38315E4D-4A72-542C-8730-D6869DA079DF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-1.4787858625280266 166.43149388192057 7.5655399780679549
		-1.9101856674147635 166.51730463839772 7.5655399780679549
		-2.3415854723015013 166.43149388192057 7.5655399780679549
		-2.7073085675432029 166.18712552228635 7.5655399780679549
		-2.9516769271774326 165.82140242704466 7.5655399780679549
		-3.037487683654577 165.39000262215791 7.5655399780679549
		-2.9516769271774326 164.95860281727116 7.5655399780679549
		-2.7073085675432029 164.59287972202947 7.5655399780679549
		-2.3415854723015013 164.34851136239524 7.5655399780679549
		-1.9101856674147637 164.2627006059181 7.5655399780679549
		-1.4787858625280257 164.34851136239524 7.5655399780679549
		-1.1130627672863249 164.59287972202947 7.5655399780679549
		-0.86869440765209438 164.95860281727118 7.5655399780679549
		-0.78288365117495107 165.39000262215791 7.5655399780679549
		-0.86869440765209505 165.82140242704466 7.5655399780679549
		-1.1130627672863249 166.18712552228635 7.5655399780679549
		-1.4787858625280266 166.43149388192057 7.5655399780679549
		;
createNode transform -n "bpctrl_r_BrowOutDrv_001" -p "Brow_Rig_Jnt";
	rename -uid "AF1C86EB-42D1-6C41-5315-40964911FAF7";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -6.4480439154662417 165.45371569588843 5.1548505645314258 ;
	setAttr ".sp" -type "double3" -6.4480439154662417 165.45371569588843 5.1548505645314258 ;
createNode nurbsCurve -n "bpctrl_r_BrowOutDrv_001Shape" -p "bpctrl_r_BrowOutDrv_001";
	rename -uid "60FF7174-43B3-188C-D8C0-F288426834FA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-6.7253423648686272 166.4952069556511 4.8243791412353287
		-6.4480439154662417 166.58101771212824 5.1548505645314249
		-6.1707454660638561 166.4952069556511 5.4853219878275219
		-5.9356631918662801 166.25083859601688 5.7654821326577004
		-5.7785862380939728 165.88511550077516 5.9526791566296016
		-5.723428147052636 165.45371569588843 6.0184140097887537
		-5.7785862380939728 165.02231589100168 5.9526791566296016
		-5.9356631918662801 164.65659279575999 5.7654821326577004
		-6.1707454660638561 164.41222443612577 5.4853219878275219
		-6.4480439154662417 164.32641367964862 5.1548505645314249
		-6.7253423648686272 164.41222443612577 4.8243791412353279
		-6.9604246390662023 164.65659279575999 4.5442189964051511
		-7.1175015928385097 165.02231589100168 4.3570219724332482
		-7.1726596838798464 165.45371569588843 4.2912871192740969
		-7.1175015928385097 165.88511550077516 4.3570219724332491
		-6.9604246390662023 166.25083859601688 4.5442189964051511
		-6.7253423648686272 166.4952069556511 4.8243791412353287
		;
createNode transform -n "bpctrl_r_Brow_001" -p "Brow_Rig_Jnt";
	rename -uid "33BB229F-4CBA-8755-5047-AC9BCD1192D2";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -3.853347315051499 167.6656446063987 6.3676026504934882 ;
	setAttr ".sp" -type "double3" -3.853347315051499 167.6656446063987 6.3676026504934882 ;
createNode nurbsCurve -n "bpctrl_r_Brow_001Shape" -p "bpctrl_r_Brow_001";
	rename -uid "DB502607-454B-CE72-9ABA-0A94663E6192";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-6.4736933539790833 167.89977111150819 5.2922753440076589
		-6.4736933539790833 167.43151810128921 5.2922753440076598
		-1.2330012761239146 167.43151810128921 7.4429299569793166
		-1.2330012761239142 167.89977111150819 7.4429299569793148
		-6.4736933539790833 167.89977111150819 5.2922753440076589
		;
createNode transform -n "Brow_Rig_Crv" -p "Brow_Rig";
	rename -uid "FE79FD7C-4CEF-54F2-7540-A28087A41D87";
createNode transform -n "crv_m_BrowSpans_001" -p "Brow_Rig_Crv";
	rename -uid "2795B725-46D5-7964-C435-18B1EFC15723";
	setAttr ".rp" -type "double3" 1.3322676295501878e-15 165.66429901123047 3.412153571844093 ;
	setAttr ".sp" -type "double3" 1.3322676295501878e-15 165.66429901123047 3.412153571844093 ;
createNode nurbsCurve -n "crv_m_BrowSpans_001Shape" -p "crv_m_BrowSpans_001";
	rename -uid "D22029EE-4B04-99E9-3F02-A2AFF3DFD88C";
	setAttr -k off ".v";
	setAttr ".dcv" yes;
createNode transform -n "crv_m_BrowSpansAim_001" -p "Brow_Rig_Crv";
	rename -uid "1634D635-4F3B-422F-AD14-4CBA178D5272";
	setAttr ".rp" -type "double3" 8.8817841970012523e-16 165.68258310466925 3.789571282292699 ;
	setAttr ".sp" -type "double3" 8.8817841970012523e-16 165.68258310466925 3.789571282292699 ;
createNode nurbsCurve -n "crv_m_BrowSpansAim_001Shape" -p "crv_m_BrowSpansAim_001";
	rename -uid "94FA4E07-4948-FE99-DCA2-6E8DE51B7B34";
	setAttr -k off ".v";
createNode transform -n "Chin_Rig" -p "Face_Rig";
	rename -uid "632C0755-49E0-046B-4827-9380AB385984";
createNode joint -n "bpjnt_m_Chin_001" -p "Chin_Rig";
	rename -uid "9290B412-4DB5-F447-F7D4-27A64C16EA72";
	addAttr -ci true -k true -sn "volumeY" -ln "volumeY" -dv 1 -at "float";
	addAttr -ci true -k true -sn "volumeZ" -ln "volumeZ" -dv 1 -at "float";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.2674710739809541e-08 155.56717364594013 5.6742791969599953 ;
	setAttr ".r" -type "double3" 3.8166656177562201e-14 -3.1805546814635168e-15 -1.0593375115320384e-30 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 6.5139815086680895e-08 -15.830289578119535 -90.00000023879204 ;
	setAttr ".bps" -type "matrix" -4.0096419517965387e-09 -0.96207391734532288 0.27278888827044395 0
		 -1.4141233739550785e-08 0.2727888882704439 0.96207391734532277 0 -1 4.4408920985006262e-16 -1.4698697814452544e-08 0
		 1.2674710684298203e-08 155.56717364594013 5.6742791969599953 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Chin001";
	setAttr ".radi" 3.8000000000000003;
	setAttr ".liw" yes;
createNode joint -n "bpjnt_m_ChinEnd_001" -p "bpjnt_m_Chin_001";
	rename -uid "D31E6EB7-494D-0536-A7DF-E5B755CAE2A0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.1610592643122279 1.9359462842664486e-15 6.2255147297933914e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1.0000000000000002 -4.4408920985006271e-16 1.4698697814452547e-08 0
		 6.7566594802349572e-16 1 -2.775557537084642e-16 0 -1.4698697910298588e-08 2.2204460492503131e-16 1 0
		 -4.5663375506031737e-15 152.52600097656256 6.5365810394287305 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ChinEnd001";
	setAttr ".radi" 0.5;
createNode transform -n "bpctrl_m_Chin_001" -p "bpjnt_m_ChinEnd_001";
	rename -uid "0DFC6778-4C87-FFA9-3CF2-1A97F17A2917";
	setAttr ".rp" -type "double3" -0.086953855690765636 0.49676850039661291 -2.0358956760446745e-06 ;
	setAttr ".sp" -type "double3" -0.086953855690765636 0.49676850039661291 -2.0358956760446745e-06 ;
createNode nurbsCurve -n "bpctrl_m_Chin_00Shape1" -p "bpctrl_m_Chin_001";
	rename -uid "59C05FC8-4494-BF0F-4A2C-C5A96DBCF7A6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 1 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.63622105178469335 0.97839105621720357 0.15573859323162903
		-0.86373498564115747 0.49676850666343347 0.22024846362244468
		-0.63622106856824967 0.01514595343864565 0.15573857851503628
		-0.086953867558563588 -0.18434864372283732 -2.0463018309109961e-06
		0.46231334040311861 0.015145944576024386 -0.15574266502288586
		0.68982727425958257 0.49676849412979429 -0.22025253541370154
		0.46231335718667499 0.97839104735458238 -0.15574265030629317
		-0.086953843823052532 1.177885644516065 -2.025489425965543e-06
		-0.63622105178469335 0.97839105621720357 0.15573859323162903
		-0.86373498564115747 0.49676850666343347 0.22024846362244468
		-0.63622106856824967 0.01514595343864565 0.15573857851503628
		;
createNode transform -n "SecondaryFace_Rig" -p "Face_Rig";
	rename -uid "59F27F13-45F7-02A6-2527-238773D04D9E";
createNode transform -n "l_SecondaryFace_Rig" -p "SecondaryFace_Rig";
	rename -uid "CDC3CD10-4E7E-058B-D381-8AA413027C77";
createNode transform -n "bpctrl_l_SecondaryUpperLidMain_001" -p "l_SecondaryFace_Rig";
	rename -uid "4497D567-4480-1A07-C933-F6BF059DCA6D";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 3.9200431112909739 164.79724444344674 6.0236018359488188 ;
	setAttr ".sp" -type "double3" 3.9200431112909739 164.79724444344674 6.0236018359488188 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryUpperLidMain_001Shape" -p "bpctrl_l_SecondaryUpperLidMain_001";
	rename -uid "8877B6E2-436F-BC7C-6D14-42B324B2E503";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		3.0404426736671013 164.50162587463655 6.2612656650258094
		4.7996435489148466 164.50162587463655 5.7859380068718274
		4.7996435489148466 165.09286301225694 5.7859380068718274
		3.0404426736671031 165.09286301225694 6.2612656650258094
		3.0404426736671013 164.50162587463655 6.2612656650258094
		;
createNode transform -n "bpctrl_l_SecondaryLowerLidMain_001" -p "l_SecondaryFace_Rig";
	rename -uid "DAB6FE8E-4230-B9B4-E164-6FB01D433497";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 4.0793595607726747 161.23250140145473 5.2346349805923342 ;
	setAttr ".sp" -type "double3" 4.0793595607726747 161.23250140145473 5.2346349805923342 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryLowerLidMain_001Shape" -p "bpctrl_l_SecondaryLowerLidMain_001";
	rename -uid "256FE549-4A24-E6E9-1D90-C8A27A489749";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		3.1997591231487981 160.93688283264427 5.4722988096693239
		4.9589599983965496 160.93688283264427 4.9969711515153437
		4.9589599983965513 161.52811997026515 4.9969711515153437
		3.1997591231487981 161.52811997026515 5.4722988096693239
		3.1997591231487981 160.93688283264427 5.4722988096693239
		;
createNode joint -n "bpjnt_l_SecondaryUpperLid_001" -p "l_SecondaryFace_Rig";
	rename -uid "465F9E4C-4F0B-888B-C7D4-BFA2BC6F0A3A";
	setAttr ".t" -type "double3" 1.9997217204634186 163.56332720711879 5.2816046914944081 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryUpperLid_001" -p "bpjnt_l_SecondaryUpperLid_001";
	rename -uid "1DBAF321-4508-8C63-BED7-B0B4655CB2FB";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 2.6645352591003765e-15 -2.8421709430404014e-14 3.5527136788005017e-15 ;
	setAttr ".sp" -type "double3" 2.6645352591003765e-15 -2.8421709430404014e-14 3.5527136788005017e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryUpperLid_001Shape" -p "bpctrl_l_SecondaryUpperLid_001";
	rename -uid "B7A090BB-4649-5045-AA7C-0CAD48AD8B75";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		6.2124390928227887e-19 0.35812273130872541 -8.8817841970012523e-16
		-0.35812273130876626 -5.6843418860808015e-14 -7.2913997892386894e-16
		0.35812273130876893 -5.6843418860808015e-14 -1.0472168604763827e-15
		6.2124390928227887e-19 0.35812273130872541 -8.8817841970012523e-16
		0 -5.6843418860808015e-14 0.35812273130876804
		0 -5.6843418860808015e-14 -0.35812273130876893
		6.2124390928227887e-19 0.35812273130872541 -8.8817841970012523e-16
		0 -5.6843418860808015e-14 0.35812273130876804
		-6.2124390928257469e-19 -0.35812273130900962 -8.8817841970012523e-16
		0 -5.6843418860808015e-14 -0.35812273130876893
		0 -5.6843418860808015e-14 -8.8817841970012523e-16
		-0.35812273130876626 -5.6843418860808015e-14 -7.2913997892386894e-16
		0.35812273130876893 -5.6843418860808015e-14 -1.0472168604763827e-15
		-6.2124390928257469e-19 -0.35812273130900962 -8.8817841970012523e-16
		-0.35812273130876626 -5.6843418860808015e-14 -7.2913997892386894e-16
		0 -5.6843418860808015e-14 -8.8817841970012523e-16
		6.2124390928227887e-19 0.35812273130872541 -8.8817841970012523e-16
		-6.2124390928257469e-19 -0.35812273130900962 -8.8817841970012523e-16
		0 -5.6843418860808015e-14 -8.8817841970012523e-16
		0 -5.6843418860808015e-14 0.35812273130876804
		0.35812273130876893 -5.6843418860808015e-14 -1.0472168604763827e-15
		0 -5.6843418860808015e-14 -0.35812273130876893
		-0.35812273130876626 -5.6843418860808015e-14 -7.2913997892386894e-16
		0 -5.6843418860808015e-14 0.35812273130876804
		;
createNode joint -n "bpjnt_l_SecondaryLowerLid_001" -p "l_SecondaryFace_Rig";
	rename -uid "7B0429AA-4BF4-B973-FE72-2CBF8CEF6DDD";
	setAttr ".t" -type "double3" 2.3563532378736967 161.86851824715791 4.9298290452846949 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryLowerLid_001" -p "bpjnt_l_SecondaryLowerLid_001";
	rename -uid "6175A662-4FB6-D89B-C71E-0B970F69B104";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.3322676295501882e-15 -5.6843418860808027e-14 -2.6645352591003765e-15 ;
	setAttr ".sp" -type "double3" 1.3322676295501882e-15 -5.6843418860808027e-14 -2.6645352591003765e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryLowerLid_001Shape" -p "bpctrl_l_SecondaryLowerLid_001";
	rename -uid "CEB0A48C-436F-0B38-1E44-7A9897A9D3E9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		0 0.35812273130869698 1.2424878185642619e-18
		-0.3581227313087656 0 0
		0.35812273130876759 0 0
		0 0.35812273130869698 1.2424878185642619e-18
		0 0 0.35812273130876271
		0 0 -0.35812273130876804
		0 0.35812273130869698 1.2424878185642619e-18
		0 0 0.35812273130876271
		0 -0.35812273130878225 -1.2424878185645577e-18
		0 0 -0.35812273130876804
		0 0 0
		-0.3581227313087656 0 0
		0.35812273130876759 0 0
		0 -0.35812273130878225 -1.2424878185645577e-18
		-0.3581227313087656 0 0
		0 0 0
		0 0.35812273130869698 1.2424878185642619e-18
		0 -0.35812273130878225 -1.2424878185645577e-18
		0 0 0
		0 0 0.35812273130876271
		0.35812273130876759 0 0
		0 0 -0.35812273130876804
		-0.3581227313087656 0 0
		0 0 0.35812273130876271
		;
createNode joint -n "bpjnt_l_SecondaryLowerLid_002" -p "l_SecondaryFace_Rig";
	rename -uid "4E7EE679-4BA2-695E-6C88-4E9502576D6D";
	setAttr ".t" -type "double3" 3.9748155620161532 161.4562105079001 4.9258684358486562 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryLowerLid_002" -p "bpjnt_l_SecondaryLowerLid_002";
	rename -uid "691D483F-445D-35DE-E28C-67BEF2A95EBB";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 -1.1368683772161605e-13 0 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 -1.1368683772161605e-13 0 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryLowerLid_002Shape" -p "bpctrl_l_SecondaryLowerLid_002";
	rename -uid "90FBA012-4A4A-B786-4A0B-2C8C50F09883";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-1.3322676295501878e-15 0.35812273130861172 2.2824419138097957e-32
		-0.35812273130877192 -5.0423982867603073e-14 3.6812168100330968e-17
		0.35812273130877192 -6.3262854854012994e-14 -3.6812168100331202e-17
		-1.3322676295501878e-15 0.35812273130861172 2.2824419138097957e-32
		-1.3322676295501878e-15 -5.6843418860808015e-14 0.35812273130876626
		-1.3322676295501878e-15 -5.6843418860808015e-14 -0.35812273130876804
		-1.3322676295501878e-15 0.35812273130861172 2.2824419138097957e-32
		-1.3322676295501878e-15 -5.6843418860808015e-14 0.35812273130876626
		-1.3322676295501878e-15 -0.35812273130886751 2.2824419138097957e-32
		-1.3322676295501878e-15 -5.6843418860808015e-14 -0.35812273130876804
		-1.3322676295501878e-15 -5.6843418860808015e-14 2.2824419138097957e-32
		-0.35812273130877192 -5.0423982867603073e-14 3.6812168100330968e-17
		0.35812273130877192 -6.3262854854012994e-14 -3.6812168100331202e-17
		-1.3322676295501878e-15 -0.35812273130886751 2.2824419138097957e-32
		-0.35812273130877192 -5.0423982867603073e-14 3.6812168100330968e-17
		-1.3322676295501878e-15 -5.6843418860808015e-14 2.2824419138097957e-32
		-1.3322676295501878e-15 0.35812273130861172 2.2824419138097957e-32
		-1.3322676295501878e-15 -0.35812273130886751 2.2824419138097957e-32
		-1.3322676295501878e-15 -5.6843418860808015e-14 2.2824419138097957e-32
		-1.3322676295501878e-15 -5.6843418860808015e-14 0.35812273130876626
		0.35812273130877192 -6.3262854854012994e-14 -3.6812168100331202e-17
		-1.3322676295501878e-15 -5.6843418860808015e-14 -0.35812273130876804
		-0.35812273130877192 -5.0423982867603073e-14 3.6812168100330968e-17
		-1.3322676295501878e-15 -5.6843418860808015e-14 0.35812273130876626
		;
createNode joint -n "bpjnt_l_SecondaryLowerLid_003" -p "l_SecondaryFace_Rig";
	rename -uid "9883C1A1-4902-BD13-7733-16948D113DE1";
	setAttr ".t" -type "double3" 5.5603730228010644 162.07875384286098 4.2653416833767359 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryLowerLid_003" -p "bpjnt_l_SecondaryLowerLid_003";
	rename -uid "BD4B2E50-4ABE-8B74-E312-6D9993519B8D";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 8.8817841970012543e-16 -8.5265128291212048e-14 -1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 8.8817841970012543e-16 -8.5265128291212048e-14 -1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryLowerLid_003Shape" -p "bpctrl_l_SecondaryLowerLid_003";
	rename -uid "0330B503-4F8C-71EC-BD3A-3181C463C44A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		0 0.35812273130875383 -2.4849756371289183e-18
		-0.35812273130876537 0 -7.9519220388127948e-17
		0.35812273130876804 0 7.9519220388128539e-17
		0 0.35812273130875383 -2.4849756371289183e-18
		0 0 0.35812273130876893
		0 0 -0.35812273130876848
		0 0.35812273130875383 -2.4849756371289183e-18
		0 0 0.35812273130876893
		0 -0.35812273130892436 2.4849756371301015e-18
		0 0 -0.35812273130876848
		0 0 0
		-0.35812273130876537 0 -7.9519220388127948e-17
		0.35812273130876804 0 7.9519220388128539e-17
		0 -0.35812273130892436 2.4849756371301015e-18
		-0.35812273130876537 0 -7.9519220388127948e-17
		0 0 0
		0 0.35812273130875383 -2.4849756371289183e-18
		0 -0.35812273130892436 2.4849756371301015e-18
		0 0 0
		0 0 0.35812273130876893
		0.35812273130876804 0 7.9519220388128539e-17
		0 0 -0.35812273130876848
		-0.35812273130876537 0 -7.9519220388127948e-17
		0 0 0.35812273130876893
		;
createNode joint -n "bpjnt_l_SecondaryUpperLid_003" -p "l_SecondaryFace_Rig";
	rename -uid "3ACE1722-4136-4806-FB2E-6F826B39B995";
	setAttr ".t" -type "double3" 5.4351465251509179 164.06795062020473 4.733464165676537 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryUpperLid_003" -p "bpjnt_l_SecondaryUpperLid_003";
	rename -uid "5CE98346-4F7F-1DF5-F2CD-AFA5236C8174";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.7763568394002509e-15 0 -3.5527136788005017e-15 ;
	setAttr ".sp" -type "double3" 1.7763568394002509e-15 0 -3.5527136788005017e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryUpperLid_003Shape" -p "bpctrl_l_SecondaryUpperLid_003";
	rename -uid "7DC11DB0-4671-DB8D-B5EF-BBA038B6A416";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-2.4849756371287207e-18 0.35812273130872535 0
		-0.35812273130876537 0 0
		0.35812273130876981 0 0
		-2.4849756371287207e-18 0.35812273130872535 0
		0 0 0.35812273130876093
		0 0 -0.3581227313087707
		-2.4849756371287207e-18 0.35812273130872535 0
		0 0 0.35812273130876093
		2.4849756371287207e-18 -0.35812273130872535 0
		0 0 -0.3581227313087707
		0 0 0
		-0.35812273130876537 0 0
		0.35812273130876981 0 0
		2.4849756371287207e-18 -0.35812273130872535 0
		-0.35812273130876537 0 0
		0 0 0
		-2.4849756371287207e-18 0.35812273130872535 0
		2.4849756371287207e-18 -0.35812273130872535 0
		0 0 0
		0 0 0.35812273130876093
		0.35812273130876981 0 0
		0 0 -0.3581227313087707
		-0.35812273130876537 0 0
		0 0 0.35812273130876093
		;
createNode joint -n "bpjnt_l_SecondaryUpperLid_002" -p "l_SecondaryFace_Rig";
	rename -uid "E92D7105-455A-C636-4937-2C8D479A3D1B";
	setAttr ".t" -type "double3" 3.7903787639204491 164.62024249032191 5.507655068386498 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryUpperLid_002" -p "bpjnt_l_SecondaryUpperLid_002";
	rename -uid "8BA8847D-48C5-F591-FCCA-979A9AA6FEB7";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 3.1086244689504391e-15 -1.1368683772161605e-13 6.2172489379008782e-15 ;
	setAttr ".sp" -type "double3" 3.1086244689504391e-15 -1.1368683772161605e-13 6.2172489379008782e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryUpperLid_002Shape" -p "bpctrl_l_SecondaryUpperLid_002";
	rename -uid "13EECC88-486D-AF1B-11A7-84AF10D5D4B0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		8.8817841970012523e-16 0.35812273130861172 8.8817841970012543e-16
		-0.35812273130876671 2.8421709430404007e-14 7.2913997892386855e-16
		0.35812273130877381 2.8421709430404007e-14 1.0472168604763847e-15
		8.8817841970012523e-16 0.35812273130861172 8.8817841970012543e-16
		8.8817841970012523e-16 2.8421709430404007e-14 0.35812273130877159
		8.8817841970012523e-16 2.8421709430404007e-14 -0.3581227313087636
		8.8817841970012523e-16 0.35812273130861172 8.8817841970012543e-16
		8.8817841970012523e-16 2.8421709430404007e-14 0.35812273130877159
		8.8817841970012523e-16 -0.35812273130878225 8.8817841970012543e-16
		8.8817841970012523e-16 2.8421709430404007e-14 -0.3581227313087636
		8.8817841970012523e-16 2.8421709430404007e-14 8.8817841970012543e-16
		-0.35812273130876671 2.8421709430404007e-14 7.2913997892386855e-16
		0.35812273130877381 2.8421709430404007e-14 1.0472168604763847e-15
		8.8817841970012523e-16 -0.35812273130878225 8.8817841970012543e-16
		-0.35812273130876671 2.8421709430404007e-14 7.2913997892386855e-16
		8.8817841970012523e-16 2.8421709430404007e-14 8.8817841970012543e-16
		8.8817841970012523e-16 0.35812273130861172 8.8817841970012543e-16
		8.8817841970012523e-16 -0.35812273130878225 8.8817841970012543e-16
		8.8817841970012523e-16 2.8421709430404007e-14 8.8817841970012543e-16
		8.8817841970012523e-16 2.8421709430404007e-14 0.35812273130877159
		0.35812273130877381 2.8421709430404007e-14 1.0472168604763847e-15
		8.8817841970012523e-16 2.8421709430404007e-14 -0.3581227313087636
		-0.35812273130876671 2.8421709430404007e-14 7.2913997892386855e-16
		8.8817841970012523e-16 2.8421709430404007e-14 0.35812273130877159
		;
createNode joint -n "bpjnt_l_SecondaryFace_001" -p "l_SecondaryFace_Rig";
	rename -uid "46E8EC90-4BC5-A4D2-8374-229BE0B50B98";
	setAttr ".t" -type "double3" 4.0978590991560466 159.31306780770473 5.2984461030849879 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryFace_001" -p "bpjnt_l_SecondaryFace_001";
	rename -uid "E20E4391-4B06-2612-FF0D-F7B650093B8C";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -5.329070518200753e-15 -4.2632564145606024e-14 3.5527136788005017e-15 ;
	setAttr ".sp" -type "double3" -5.329070518200753e-15 -4.2632564145606024e-14 3.5527136788005017e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryFace_001Shape" -p "bpctrl_l_SecondaryFace_001";
	rename -uid "76E08524-4DBB-066C-1D19-E6976BC10E58";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		0 0.48745526006601375 8.8479601936762566e-16
		-0.26307761886892012 0 0.4103690985154626
		0.26307761886891701 0 -0.41036909851545639
		0 0.48745526006601375 8.8479601936762566e-16
		0.41036909851545467 0 0.26307761886891889
		-0.41036909851546577 0 -0.26307761886892511
		0 0.48745526006601375 8.8479601936762566e-16
		0.41036909851545467 0 0.26307761886891889
		0 -0.48745526006612744 8.915608200326256e-16
		-0.41036909851546577 0 -0.26307761886892511
		0 0 8.8817841970012523e-16
		-0.26307761886892012 0 0.4103690985154626
		0.26307761886891701 0 -0.41036909851545639
		0 -0.48745526006612744 8.915608200326256e-16
		-0.26307761886892012 0 0.4103690985154626
		0 0 8.8817841970012523e-16
		0 0.48745526006601375 8.8479601936762566e-16
		0 -0.48745526006612744 8.915608200326256e-16
		0 0 8.8817841970012523e-16
		0.41036909851545467 0 0.26307761886891889
		0.26307761886891701 0 -0.41036909851545639
		-0.41036909851546577 0 -0.26307761886892511
		-0.26307761886892012 0 0.4103690985154626
		0.41036909851545467 0 0.26307761886891889
		;
createNode joint -n "bpjnt_l_SecondaryFace_002" -p "l_SecondaryFace_Rig";
	rename -uid "10ED4C3C-4B8D-1C1E-1CB1-66A6C7AFA2D1";
	setAttr ".t" -type "double3" 4.4842245128218163 155.76907671883757 4.0838751039394765 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryFace_002" -p "bpjnt_l_SecondaryFace_002";
	rename -uid "5EB0C6E1-41FC-E324-87BE-C2B3A822E578";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 8.5265128291212048e-14 5.329070518200753e-15 ;
	setAttr ".sp" -type "double3" 0 8.5265128291212048e-14 5.329070518200753e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryFace_002Shape" -p "bpctrl_l_SecondaryFace_002";
	rename -uid "1F9E2C0E-4F7B-CFCE-CB5C-09A68FAE9325";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		0 0.48745526006621276 0
		-0.2726807344270874 0 0.4040517883123842
		0.27268073442708918 0 -0.40405178831237754
		0 0.48745526006621276 0
		0.40405178831238242 0 0.27268073442708651
		-0.40405178831238509 0 -0.27268073442708651
		0 0.48745526006621276 0
		0.40405178831238242 0 0.27268073442708651
		0 -0.48745526006595696 0
		-0.40405178831238509 0 -0.27268073442708651
		0 0 0
		-0.2726807344270874 0 0.4040517883123842
		0.27268073442708918 0 -0.40405178831237754
		0 -0.48745526006595696 0
		-0.2726807344270874 0 0.4040517883123842
		0 0 0
		0 0.48745526006621276 0
		0 -0.48745526006595696 0
		0 0 0
		0.40405178831238242 0 0.27268073442708651
		0.27268073442708918 0 -0.40405178831237754
		-0.40405178831238509 0 -0.27268073442708651
		-0.2726807344270874 0 0.4040517883123842
		0.40405178831238242 0 0.27268073442708651
		;
createNode joint -n "bpjnt_l_SecondaryFace_003" -p "l_SecondaryFace_Rig";
	rename -uid "DA50463C-44CF-91BE-B1F8-2986ACD3843A";
	setAttr ".t" -type "double3" 2.7999755885664452 152.70422686532191 4.8250507554897712 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_l_SecondaryFace_003" -p "bpjnt_l_SecondaryFace_003";
	rename -uid "D35C4577-47A2-C18F-7FB2-FA88F984FBC1";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 2.2204460492503135e-15 -5.6843418860808027e-14 1.7763568394002509e-15 ;
	setAttr ".sp" -type "double3" 2.2204460492503135e-15 -5.6843418860808027e-14 1.7763568394002509e-15 ;
createNode nurbsCurve -n "bpctrl_l_SecondaryFace_003Shape" -p "bpctrl_l_SecondaryFace_003";
	rename -uid "B2E85C5C-47BF-08A1-F70F-A89D25AD2558";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		0.15253631198028383 0.44000447067722348 0.14401864420109509
		-0.32197911181558991 -0.0081397836528367407 0.36589045634268486
		0.32197911181559702 0.0081397836526662104 -0.36589045634268308
		0.15253631198028383 0.44000447067722348 0.14401864420109509
		0.33267815625319663 -0.20962452211543336 0.28808928242118087
		-0.33267815625319397 0.20962452211546179 -0.28808928242118353
		0.15253631198028383 0.44000447067722348 0.14401864420109509
		0.33267815625319663 -0.20962452211543336 0.28808928242118087
		-0.15253631198027939 -0.44000447067736559 -0.14401864420109509
		-0.33267815625319397 0.20962452211546179 -0.28808928242118353
		0 0 -8.8817841970012523e-16
		-0.32197911181558991 -0.0081397836528367407 0.36589045634268486
		0.32197911181559702 0.0081397836526662104 -0.36589045634268308
		-0.15253631198027939 -0.44000447067736559 -0.14401864420109509
		-0.32197911181558991 -0.0081397836528367407 0.36589045634268486
		0 0 -8.8817841970012523e-16
		0.15253631198028383 0.44000447067722348 0.14401864420109509
		-0.15253631198027939 -0.44000447067736559 -0.14401864420109509
		0 0 -8.8817841970012523e-16
		0.33267815625319663 -0.20962452211543336 0.28808928242118087
		0.32197911181559702 0.0081397836526662104 -0.36589045634268308
		-0.33267815625319397 0.20962452211546179 -0.28808928242118353
		-0.32197911181558991 -0.0081397836528367407 0.36589045634268486
		0.33267815625319663 -0.20962452211543336 0.28808928242118087
		;
createNode transform -n "r_SecondaryFace_Rig" -p "SecondaryFace_Rig";
	rename -uid "2050661A-4DB9-08E8-7064-ADA8DF51915B";
	setAttr ".s" -type "double3" -1 1 1 ;
createNode transform -n "bpctrl_r_SecondaryUpperLidMain_001" -p "r_SecondaryFace_Rig";
	rename -uid "3BC2D0FF-46B9-E35B-9777-DB9E92097162";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 3.9200431112909739 164.79724444344674 6.0236018359488188 ;
	setAttr ".sp" -type "double3" 3.9200431112909739 164.79724444344674 6.0236018359488188 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryUpperLidMain_001Shape" -p "bpctrl_r_SecondaryUpperLidMain_001";
	rename -uid "33F0904C-4EDD-549B-EA32-5AA9B883E769";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		3.0404426736671013 164.50162587463655 6.2612656650258094
		4.7996435489148466 164.50162587463655 5.7859380068718274
		4.7996435489148466 165.09286301225694 5.7859380068718274
		3.0404426736671031 165.09286301225694 6.2612656650258094
		3.0404426736671013 164.50162587463655 6.2612656650258094
		;
createNode transform -n "bpctrl_r_SecondaryLowerLidMain_001" -p "r_SecondaryFace_Rig";
	rename -uid "954724CD-4326-FB66-590C-FC969EFB2101";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 4.0793595607726747 161.23250140145473 5.2346349805923342 ;
	setAttr ".sp" -type "double3" 4.0793595607726747 161.23250140145473 5.2346349805923342 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryLowerLidMain_001Shape" -p "bpctrl_r_SecondaryLowerLidMain_001";
	rename -uid "E436FBC2-43D4-4B1D-9B82-2E8F9A1C3FC4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		3.1997591231487981 160.93688283264427 5.4722988096693239
		4.9589599983965496 160.93688283264427 4.9969711515153437
		4.9589599983965513 161.52811997026515 4.9969711515153437
		3.1997591231487981 161.52811997026515 5.4722988096693239
		3.1997591231487981 160.93688283264427 5.4722988096693239
		;
createNode transform -n "transform33" -p "r_SecondaryFace_Rig";
	rename -uid "169CAE89-4CE8-D85E-3095-56AEA473231F";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryFace_003" -p "transform33";
	rename -uid "C181AFDF-4D6C-71D1-C96B-8B834EAFC920";
	setAttr ".t" -type "double3" -2.7999755885664461 152.70422686532191 4.8250507554897712 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryFace_003" -p "bpjnt_r_SecondaryFace_003";
	rename -uid "0CEEBD66-4875-E786-5847-33B52799C512";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.9539925233402758e-14 5.6843418860808027e-14 1.5987211554602257e-14 ;
	setAttr ".sp" -type "double3" -1.9539925233402758e-14 5.6843418860808027e-14 1.5987211554602257e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryFace_003Shape" -p "bpctrl_r_SecondaryFace_003";
	rename -uid "DB43D327-4340-5BE2-56A5-B488E7FFD217";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-0.15253631198030204 0.44000447067733717 0.14401864420111105
		0.32197911181557171 -0.0081397836527230087 0.36589045634270079
		-0.32197911181561523 0.0081397836527798521 -0.36589045634266704
		-0.15253631198030204 0.44000447067733717 0.14401864420111105
		-0.33267815625321484 -0.20962452211531965 0.28808928242119691
		0.33267815625317576 0.20962452211557545 -0.2880892824211676
		-0.15253631198030204 0.44000447067733717 0.14401864420111105
		-0.33267815625321484 -0.20962452211531965 0.28808928242119691
		0.15253631198026119 -0.4400044706772519 -0.14401864420107907
		0.33267815625317576 0.20962452211557545 -0.2880892824211676
		-1.8207657603852567e-14 1.1368683772161605e-13 1.5099033134902129e-14
		0.32197911181557171 -0.0081397836527230087 0.36589045634270079
		-0.32197911181561523 0.0081397836527798521 -0.36589045634266704
		0.15253631198026119 -0.4400044706772519 -0.14401864420107907
		0.32197911181557171 -0.0081397836527230087 0.36589045634270079
		-1.8207657603852567e-14 1.1368683772161605e-13 1.5099033134902129e-14
		-0.15253631198030204 0.44000447067733717 0.14401864420111105
		0.15253631198026119 -0.4400044706772519 -0.14401864420107907
		-1.8207657603852567e-14 1.1368683772161605e-13 1.5099033134902129e-14
		-0.33267815625321484 -0.20962452211531965 0.28808928242119691
		-0.32197911181561523 0.0081397836527798521 -0.36589045634266704
		0.33267815625317576 0.20962452211557545 -0.2880892824211676
		0.32197911181557171 -0.0081397836527230087 0.36589045634270079
		-0.33267815625321484 -0.20962452211531965 0.28808928242119691
		;
createNode transform -n "transform34" -p "r_SecondaryFace_Rig";
	rename -uid "F1C5E651-4A36-23BF-FAC7-99ADEC2684F9";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryFace_002" -p "transform34";
	rename -uid "7DBED5DE-4D17-CA5C-88B8-0EB0C7FCDD04";
	setAttr ".t" -type "double3" -4.4842245128218163 155.76907671883757 4.0838751039394765 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryFace_002" -p "bpjnt_r_SecondaryFace_002";
	rename -uid "D92B8BA3-4997-C1BB-9647-20B7FE98316A";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.2434497875801756e-14 -1.4210854715202006e-13 1.5099033134902132e-14 ;
	setAttr ".sp" -type "double3" -1.2434497875801756e-14 -1.4210854715202006e-13 1.5099033134902132e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryFace_002Shape" -p "bpctrl_r_SecondaryFace_002";
	rename -uid "53F24547-440E-F328-537E-54BBC7BD560D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-1.5099033134902129e-14 0.48745526006598539 7.9334056783263871e-15
		0.27268073442707319 -2.2732419337030747e-13 0.40405178831239219
		-0.27268073442710339 -2.2742315751615675e-13 -0.40405178831236954
		-1.5099033134902129e-14 0.48745526006598539 7.9334056783263871e-15
		-0.40405178831239663 -2.2734028168437158e-13 0.27268073442709451
		0.40405178831237087 -2.2740706920209264e-13 -0.27268073442707852
		-1.5099033134902129e-14 0.48745526006598539 7.9334056783263871e-15
		-0.40405178831239663 -2.2734028168437158e-13 0.27268073442709451
		-1.4210854715202004e-14 -0.48745526006618434 8.0538058762758734e-15
		0.40405178831237087 -2.2740706920209264e-13 -0.27268073442707852
		-1.4210854715202004e-14 -2.2737367544323211e-13 7.993605777301146e-15
		0.27268073442707319 -2.2732419337030747e-13 0.40405178831239219
		-0.27268073442710339 -2.2742315751615675e-13 -0.40405178831236954
		-1.4210854715202004e-14 -0.48745526006618434 8.0538058762758734e-15
		0.27268073442707319 -2.2732419337030747e-13 0.40405178831239219
		-1.4210854715202004e-14 -2.2737367544323211e-13 7.993605777301146e-15
		-1.5099033134902129e-14 0.48745526006598539 7.9334056783263871e-15
		-1.4210854715202004e-14 -0.48745526006618434 8.0538058762758734e-15
		-1.4210854715202004e-14 -2.2737367544323211e-13 7.993605777301146e-15
		-0.40405178831239663 -2.2734028168437158e-13 0.27268073442709451
		-0.27268073442710339 -2.2742315751615675e-13 -0.40405178831236954
		0.40405178831237087 -2.2740706920209264e-13 -0.27268073442707852
		0.27268073442707319 -2.2732419337030747e-13 0.40405178831239219
		-0.40405178831239663 -2.2734028168437158e-13 0.27268073442709451
		;
createNode transform -n "transform35" -p "r_SecondaryFace_Rig";
	rename -uid "3A263A65-433E-D41F-265A-64833A7735AE";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryFace_001" -p "transform35";
	rename -uid "485D1BF3-4034-540F-101C-E5A788EFDA13";
	setAttr ".t" -type "double3" -4.0978590991560448 159.31306780770473 5.2984461030849879 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryFace_001" -p "bpjnt_r_SecondaryFace_001";
	rename -uid "1528AE4B-4466-DD0E-D648-F8B27D8314C1";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -1.5987211554602257e-14 4.2632564145606024e-14 1.4210854715202007e-14 ;
	setAttr ".sp" -type "double3" -1.5987211554602257e-14 4.2632564145606024e-14 1.4210854715202007e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryFace_001Shape" -p "bpctrl_r_SecondaryFace_001";
	rename -uid "0436D1BB-408B-237B-0E58-4CBDF3E1C507";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-1.9539925233402755e-14 0.48745526006607054 1.5037141835761155e-14
		0.26307761886890058 5.6893674581104622e-14 0.41036909851547676
		-0.26307761886893655 5.6793163140511433e-14 -0.41036909851544212
		-1.9539925233402755e-14 0.48745526006607054 1.5037141835761155e-14
		-0.41036909851547421 5.6875636577195536e-14 0.26307761886893322
		0.41036909851544623 5.6811201144420513e-14 -0.26307761886891101
		-1.9539925233402755e-14 0.48745526006607054 1.5037141835761155e-14
		-0.41036909851547421 5.6875636577195536e-14 0.26307761886893322
		-1.9539925233402755e-14 -0.48745526006607054 1.5160924434043137e-14
		0.41036909851544623 5.6811201144420513e-14 -0.26307761886891101
		-1.9539925233402755e-14 5.6843418860808027e-14 1.5099033134902135e-14
		0.26307761886890058 5.6893674581104622e-14 0.41036909851547676
		-0.26307761886893655 5.6793163140511433e-14 -0.41036909851544212
		-1.9539925233402755e-14 -0.48745526006607054 1.5160924434043137e-14
		0.26307761886890058 5.6893674581104622e-14 0.41036909851547676
		-1.9539925233402755e-14 5.6843418860808027e-14 1.5099033134902135e-14
		-1.9539925233402755e-14 0.48745526006607054 1.5037141835761155e-14
		-1.9539925233402755e-14 -0.48745526006607054 1.5160924434043137e-14
		-1.9539925233402755e-14 5.6843418860808027e-14 1.5099033134902135e-14
		-0.41036909851547421 5.6875636577195536e-14 0.26307761886893322
		-0.26307761886893655 5.6793163140511433e-14 -0.41036909851544212
		0.41036909851544623 5.6811201144420513e-14 -0.26307761886891101
		0.26307761886890058 5.6893674581104622e-14 0.41036909851547676
		-0.41036909851547421 5.6875636577195536e-14 0.26307761886893322
		;
createNode transform -n "transform36" -p "r_SecondaryFace_Rig";
	rename -uid "5AA1094B-4219-254D-4846-4687DBD43C0D";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryLowerLid_001" -p "transform36";
	rename -uid "F1D06733-4649-AECF-3B12-0287CD4D8ED8";
	setAttr ".t" -type "double3" -2.3563532378736971 161.86851824715791 4.9298290452846949 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryLowerLid_001" -p "bpjnt_r_SecondaryLowerLid_001";
	rename -uid "5CAE64A5-46C4-7EB7-363E-5EB846DA6E84";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.4868995751603513e-14 5.6843418860808027e-14 2.3092638912203262e-14 ;
	setAttr ".sp" -type "double3" -2.4868995751603513e-14 5.6843418860808027e-14 2.3092638912203262e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryLowerLid_001Shape" -p "bpctrl_r_SecondaryLowerLid_001";
	rename -uid "91CD0FA7-418C-E079-7B8E-E5B22C1FCB42";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-2.2204460492503131e-14 0.35812273130878225 2.571418896145213e-14
		0.35812273130874361 8.5265128291212048e-14 2.5757174171303638e-14
		-0.3581227313087898 8.5265128291212048e-14 2.5757174171303638e-14
		-2.2204460492503131e-14 0.35812273130878225 2.571418896145213e-14
		-2.2204460492503131e-14 8.5308985676871969e-14 0.35812273130878847
		-2.2204460492503131e-14 8.5221270905552126e-14 -0.35812273130874228
		-2.2204460492503131e-14 0.35812273130878225 2.571418896145213e-14
		-2.2204460492503131e-14 8.5308985676871969e-14 0.35812273130878847
		-2.2204460492503131e-14 -0.35812273130869698 2.5800159381155155e-14
		-2.2204460492503131e-14 8.5221270905552126e-14 -0.35812273130874228
		-2.2204460492503131e-14 8.5265128291212048e-14 2.5757174171303638e-14
		0.35812273130874361 8.5265128291212048e-14 2.5757174171303638e-14
		-0.3581227313087898 8.5265128291212048e-14 2.5757174171303638e-14
		-2.2204460492503131e-14 -0.35812273130869698 2.5800159381155155e-14
		0.35812273130874361 8.5265128291212048e-14 2.5757174171303638e-14
		-2.2204460492503131e-14 8.5265128291212048e-14 2.5757174171303638e-14
		-2.2204460492503131e-14 0.35812273130878225 2.571418896145213e-14
		-2.2204460492503131e-14 -0.35812273130869698 2.5800159381155155e-14
		-2.2204460492503131e-14 8.5265128291212048e-14 2.5757174171303638e-14
		-2.2204460492503131e-14 8.5308985676871969e-14 0.35812273130878847
		-0.3581227313087898 8.5265128291212048e-14 2.5757174171303638e-14
		-2.2204460492503131e-14 8.5221270905552126e-14 -0.35812273130874228
		0.35812273130874361 8.5265128291212048e-14 2.5757174171303638e-14
		-2.2204460492503131e-14 8.5308985676871969e-14 0.35812273130878847
		;
createNode transform -n "transform37" -p "r_SecondaryFace_Rig";
	rename -uid "EFBBE246-4D23-4989-1982-A9B1588B8C51";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryLowerLid_002" -p "transform37";
	rename -uid "462FFE39-4322-54B7-8A68-C69136DD1E01";
	setAttr ".t" -type "double3" -3.9748155620161523 161.4562105079001 4.9258684358486562 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryLowerLid_002" -p "bpjnt_r_SecondaryLowerLid_002";
	rename -uid "D56BE6BC-4374-F107-A703-5FBC5C118F0A";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.3536728122053325e-14 5.6843418860808027e-14 1.7763568394002508e-14 ;
	setAttr ".sp" -type "double3" -2.3536728122053325e-14 5.6843418860808027e-14 1.7763568394002508e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryLowerLid_002Shape" -p "bpctrl_r_SecondaryLowerLid_002";
	rename -uid "432DA1F8-423B-C607-B235-3592E3D5DB54";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-2.1760371282653062e-14 0.35812273130881067 1.7719340696332442e-14
		0.35812273130874889 1.4531826514862236e-13 1.7781974478052674e-14
		-0.35812273130879463 1.3889882915541741e-13 1.7745162309952342e-14
		-2.1760371282653062e-14 0.35812273130881067 1.7719340696332442e-14
		-2.1760371282653062e-14 1.4215240453767982e-13 0.35812273130878403
		-2.1760371282653062e-14 1.4206468976635998e-13 -0.35812273130875028
		-2.1760371282653062e-14 0.35812273130881067 1.7719340696332442e-14
		-2.1760371282653062e-14 1.4215240453767982e-13 0.35812273130878403
		-2.1316282072802999e-14 -0.35812273130866856 1.7807796091672593e-14
		-2.1760371282653062e-14 1.4206468976635998e-13 -0.35812273130875028
		-2.1760371282653062e-14 1.4210854715201989e-13 1.7763568394002508e-14
		0.35812273130874889 1.4531826514862236e-13 1.7781974478052674e-14
		-0.35812273130879463 1.3889882915541741e-13 1.7745162309952342e-14
		-2.1316282072802999e-14 -0.35812273130866856 1.7807796091672593e-14
		0.35812273130874889 1.4531826514862236e-13 1.7781974478052674e-14
		-2.1760371282653062e-14 1.4210854715201989e-13 1.7763568394002508e-14
		-2.1760371282653062e-14 0.35812273130881067 1.7719340696332442e-14
		-2.1316282072802999e-14 -0.35812273130866856 1.7807796091672593e-14
		-2.1760371282653062e-14 1.4210854715201989e-13 1.7763568394002508e-14
		-2.1760371282653062e-14 1.4215240453767982e-13 0.35812273130878403
		-0.35812273130879463 1.3889882915541741e-13 1.7745162309952342e-14
		-2.1760371282653062e-14 1.4206468976635998e-13 -0.35812273130875028
		0.35812273130874889 1.4531826514862236e-13 1.7781974478052674e-14
		-2.1760371282653062e-14 1.4215240453767982e-13 0.35812273130878403
		;
createNode transform -n "transform38" -p "r_SecondaryFace_Rig";
	rename -uid "31ABC50C-42F0-D7E7-45A7-91AADC62E944";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryUpperLid_001" -p "transform38";
	rename -uid "59AB90F7-4089-110C-7B69-87A2F33F6B1B";
	setAttr ".t" -type "double3" -1.9997217204634186 163.56332720711879 5.2816046914944081 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryUpperLid_001" -p "bpjnt_r_SecondaryUpperLid_001";
	rename -uid "3C52C57A-4C3B-1590-7817-ADAEAA31E11C";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.2426505097428168e-14 5.6843418860808027e-14 1.9539925233402758e-14 ;
	setAttr ".sp" -type "double3" -2.2426505097428168e-14 5.6843418860808027e-14 1.9539925233402758e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryUpperLid_001Shape" -p "bpctrl_r_SecondaryUpperLid_001";
	rename -uid "881CED64-4328-33A2-6C51-57A8BB255A8D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-1.9984635687162099e-14 0.35812273130881067 1.5944226344750728e-14
		0.35812273130874628 2.842170943040402e-14 1.6146249995378502e-14
		-0.35812273130878891 2.842170943040402e-14 1.5828173113825988e-14
		-1.9984635687162099e-14 0.35812273130881067 1.5944226344750728e-14
		-1.9984014443252818e-14 2.8465566816063935e-14 0.35812273130878491
		-1.9984014443252818e-14 2.8377852044744099e-14 -0.35812273130875205
		-1.9984635687162099e-14 0.35812273130881067 1.5944226344750728e-14
		-1.9984014443252818e-14 2.8465566816063935e-14 0.35812273130878491
		-1.9983393199343534e-14 -0.35812273130892436 1.6030196764453781e-14
		-1.9984014443252818e-14 2.8377852044744099e-14 -0.35812273130875205
		-1.9984014443252818e-14 2.842170943040402e-14 1.5987211554602245e-14
		0.35812273130874628 2.842170943040402e-14 1.6146249995378502e-14
		-0.35812273130878891 2.842170943040402e-14 1.5828173113825988e-14
		-1.9983393199343534e-14 -0.35812273130892436 1.6030196764453781e-14
		0.35812273130874628 2.842170943040402e-14 1.6146249995378502e-14
		-1.9984014443252818e-14 2.842170943040402e-14 1.5987211554602245e-14
		-1.9984635687162099e-14 0.35812273130881067 1.5944226344750728e-14
		-1.9983393199343534e-14 -0.35812273130892436 1.6030196764453781e-14
		-1.9984014443252818e-14 2.842170943040402e-14 1.5987211554602245e-14
		-1.9984014443252818e-14 2.8465566816063935e-14 0.35812273130878491
		-0.35812273130878891 2.842170943040402e-14 1.5828173113825988e-14
		-1.9984014443252818e-14 2.8377852044744099e-14 -0.35812273130875205
		0.35812273130874628 2.842170943040402e-14 1.6146249995378502e-14
		-1.9984014443252818e-14 2.8465566816063935e-14 0.35812273130878491
		;
createNode transform -n "transform39" -p "r_SecondaryFace_Rig";
	rename -uid "759FD7ED-45EF-98D1-BEAB-4EBECB83D56E";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryUpperLid_003" -p "transform39";
	rename -uid "32DB4494-4373-C8C0-D6B6-5181DD034EFF";
	setAttr ".t" -type "double3" -5.4351465251509179 164.06795062020473 4.733464165676537 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryUpperLid_003" -p "bpjnt_r_SecondaryUpperLid_003";
	rename -uid "654B665F-4DD5-F570-829E-528862F53A99";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.8421709430404014e-14 0 2.3980817331903388e-14 ;
	setAttr ".sp" -type "double3" -2.8421709430404014e-14 0 2.3980817331903388e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryUpperLid_003Shape" -p "bpctrl_r_SecondaryUpperLid_003";
	rename -uid "47FF223C-4155-83A7-DCB3-B286C889E347";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-2.4866510775966377e-14 0.35812273130872535 2.7488060825215254e-14
		0.35812273130874051 4.3508194350300593e-31 2.7533531010703895e-14
		-0.35812273130879468 4.3508194350300593e-31 2.7533531010703895e-14
		-2.4866510775966377e-14 0.35812273130872535 2.7488060825215254e-14
		-2.4868995751603507e-14 4.3857385659918609e-17 0.35812273130878847
		-2.4868995751603507e-14 -4.3857385659918936e-17 -0.35812273130874317
		-2.4866510775966377e-14 0.35812273130872535 2.7488060825215254e-14
		-2.4868995751603507e-14 4.3857385659918609e-17 0.35812273130878847
		-2.4871480727240636e-14 -0.35812273130872535 2.7579001196192535e-14
		-2.4868995751603507e-14 -4.3857385659918936e-17 -0.35812273130874317
		-2.4868995751603507e-14 4.3508194350300593e-31 2.7533531010703895e-14
		0.35812273130874051 4.3508194350300593e-31 2.7533531010703895e-14
		-0.35812273130879468 4.3508194350300593e-31 2.7533531010703895e-14
		-2.4871480727240636e-14 -0.35812273130872535 2.7579001196192535e-14
		0.35812273130874051 4.3508194350300593e-31 2.7533531010703895e-14
		-2.4868995751603507e-14 4.3508194350300593e-31 2.7533531010703895e-14
		-2.4866510775966377e-14 0.35812273130872535 2.7488060825215254e-14
		-2.4871480727240636e-14 -0.35812273130872535 2.7579001196192535e-14
		-2.4868995751603507e-14 4.3508194350300593e-31 2.7533531010703895e-14
		-2.4868995751603507e-14 4.3857385659918609e-17 0.35812273130878847
		-0.35812273130879468 4.3508194350300593e-31 2.7533531010703895e-14
		-2.4868995751603507e-14 -4.3857385659918936e-17 -0.35812273130874317
		0.35812273130874051 4.3508194350300593e-31 2.7533531010703895e-14
		-2.4868995751603507e-14 4.3857385659918609e-17 0.35812273130878847
		;
createNode transform -n "transform40" -p "r_SecondaryFace_Rig";
	rename -uid "3C93D1D3-45D4-B5CD-2DAE-529825C889DA";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryLowerLid_003" -p "transform40";
	rename -uid "FB5C8B30-47DC-210E-DD4B-1E9D32A2EC38";
	setAttr ".t" -type "double3" -5.5603730228010644 162.07875384286098 4.2653416833767359 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryLowerLid_003" -p "bpjnt_r_SecondaryLowerLid_003";
	rename -uid "D74EE152-4624-1C78-4082-D8B415746552";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.3092638912203262e-14 5.6843418860808027e-14 1.7763568394002508e-14 ;
	setAttr ".sp" -type "double3" -2.3092638912203262e-14 5.6843418860808027e-14 1.7763568394002508e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryLowerLid_003Shape" -p "bpctrl_r_SecondaryLowerLid_003";
	rename -uid "2AD5EBFA-40CE-F134-E689-70A4CA7DCFFE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-1.9539925233402755e-14 0.35812273130889594 1.9495697535732676e-14
		0.35812273130874583 1.4210854715202006e-13 1.9460406013014627e-14
		-0.35812273130878758 1.4210854715202006e-13 1.9619444453790884e-14
		-1.9539925233402755e-14 0.35812273130889594 1.9495697535732676e-14
		-1.9539925233402755e-14 1.4215240453767997e-13 0.35812273130878847
		-1.9539925233402755e-14 1.4206468976636015e-13 -0.35812273130874894
		-1.9539925233402755e-14 0.35812273130889594 1.9495697535732676e-14
		-1.9539925233402755e-14 1.4215240453767997e-13 0.35812273130878847
		-1.9539925233402755e-14 -0.35812273130878225 1.9584152931072856e-14
		-1.9539925233402755e-14 1.4206468976636015e-13 -0.35812273130874894
		-1.9539925233402755e-14 1.4210854715202006e-13 1.9539925233402758e-14
		0.35812273130874583 1.4210854715202006e-13 1.9460406013014627e-14
		-0.35812273130878758 1.4210854715202006e-13 1.9619444453790884e-14
		-1.9539925233402755e-14 -0.35812273130878225 1.9584152931072856e-14
		0.35812273130874583 1.4210854715202006e-13 1.9460406013014627e-14
		-1.9539925233402755e-14 1.4210854715202006e-13 1.9539925233402758e-14
		-1.9539925233402755e-14 0.35812273130889594 1.9495697535732676e-14
		-1.9539925233402755e-14 -0.35812273130878225 1.9584152931072856e-14
		-1.9539925233402755e-14 1.4210854715202006e-13 1.9539925233402758e-14
		-1.9539925233402755e-14 1.4215240453767997e-13 0.35812273130878847
		-0.35812273130878758 1.4210854715202006e-13 1.9619444453790884e-14
		-1.9539925233402755e-14 1.4206468976636015e-13 -0.35812273130874894
		0.35812273130874583 1.4210854715202006e-13 1.9460406013014627e-14
		-1.9539925233402755e-14 1.4215240453767997e-13 0.35812273130878847
		;
createNode transform -n "transform41" -p "r_SecondaryFace_Rig";
	rename -uid "7DF226EC-414B-E237-F6F4-2E8C69CB6862";
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode joint -n "bpjnt_r_SecondaryUpperLid_002" -p "transform41";
	rename -uid "383193CF-4FA0-344A-6AFD-899AABB8FF6D";
	setAttr ".t" -type "double3" -3.7903787639204491 164.62024249032191 5.5076550683865015 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_r_SecondaryUpperLid_002" -p "bpjnt_r_SecondaryUpperLid_002";
	rename -uid "D8292A86-431C-51D3-1FD8-B191C1C252B0";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.3092638912203262e-14 1.1368683772161605e-13 1.6875389974302383e-14 ;
	setAttr ".sp" -type "double3" -2.3092638912203262e-14 1.1368683772161605e-13 1.6875389974302383e-14 ;
createNode nurbsCurve -n "bpctrl_r_SecondaryUpperLid_002Shape" -p "bpctrl_r_SecondaryUpperLid_002";
	rename -uid "0DB74F49-4D99-4247-11A4-2DBB56E51493";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		-1.8207657603852567e-14 0.35812273130883909 1.5944226344750759e-14
		0.35812273130874939 2.5579538487363612e-13 1.5907692334214122e-14
		-0.35812273130879158 2.5579538487363612e-13 1.6066730774990383e-14
		-1.8207657603852567e-14 0.35812273130883909 1.5944226344750759e-14
		-1.8207657603852567e-14 2.5583924225929605e-13 0.35812273130878669
		-1.8207657603852567e-14 2.5575152748797618e-13 -0.3581227313087485
		-1.8207657603852567e-14 0.35812273130883909 1.5944226344750759e-14
		-1.8207657603852567e-14 2.5583924225929605e-13 0.35812273130878669
		-1.8207657603852567e-14 -0.35812273130855488 1.6030196764453771e-14
		-1.8207657603852567e-14 2.5575152748797618e-13 -0.3581227313087485
		-1.8207657603852567e-14 2.5579538487363612e-13 1.5987211554602251e-14
		0.35812273130874939 2.5579538487363612e-13 1.5907692334214122e-14
		-0.35812273130879158 2.5579538487363612e-13 1.6066730774990383e-14
		-1.8207657603852567e-14 -0.35812273130855488 1.6030196764453771e-14
		0.35812273130874939 2.5579538487363612e-13 1.5907692334214122e-14
		-1.8207657603852567e-14 2.5579538487363612e-13 1.5987211554602251e-14
		-1.8207657603852567e-14 0.35812273130883909 1.5944226344750759e-14
		-1.8207657603852567e-14 -0.35812273130855488 1.6030196764453771e-14
		-1.8207657603852567e-14 2.5579538487363612e-13 1.5987211554602251e-14
		-1.8207657603852567e-14 2.5583924225929605e-13 0.35812273130878669
		-0.35812273130879158 2.5579538487363612e-13 1.6066730774990383e-14
		-1.8207657603852567e-14 2.5575152748797618e-13 -0.3581227313087485
		0.35812273130874939 2.5579538487363612e-13 1.5907692334214122e-14
		-1.8207657603852567e-14 2.5583924225929605e-13 0.35812273130878669
		;
createNode joint -n "bpjnt_m_SecondaryFace_001" -p "SecondaryFace_Rig";
	rename -uid "39C58F80-4421-C117-06D5-078A24DEAC54";
	setAttr ".t" -type "double3" 3.8817173624767542e-05 151.21853960946254 6.0545396051296461 ;
	setAttr ".jot" -type "string" "none";
createNode transform -n "bpctrl_m_SecondaryFace_001" -p "bpjnt_m_SecondaryFace_001";
	rename -uid "A1891F94-47A5-659C-7854-FFB9B2B21195";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.3552527156068808e-20 -4.2632564145606024e-14 -5.329070518200753e-15 ;
	setAttr ".sp" -type "double3" 1.3552527156068808e-20 -4.2632564145606024e-14 -5.329070518200753e-15 ;
createNode nurbsCurve -n "bpctrl_m_SecondaryFace_001Shape" -p "bpctrl_m_SecondaryFace_001";
	rename -uid "0BACD58F-4C2D-8F7D-F780-CEA0736E41F6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 19;
	setAttr ".cc" -type "nurbsCurve" 
		1 23 0 no 3
		24 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
		24
		8.3933129811111715e-21 0.53158991089642882 0.38723519478023505
		-0.65767691874013945 0 8.8817841970012523e-16
		0.65767691874013945 0 8.8817841970012523e-16
		8.3933129811111715e-21 0.53158991089642882 0.38723519478023505
		-1.4602521827698505e-16 -0.38723519478034518 0.53158991089658159
		1.4604200490294727e-16 0.3872351947802315 -0.53158991089658691
		8.3933129811111715e-21 0.53158991089642882 0.38723519478023505
		-1.4602521827698505e-16 -0.38723519478034518 0.53158991089658159
		8.3933129811111715e-21 -0.53158991089659935 -0.3872351947802386
		1.4604200490294727e-16 0.3872351947802315 -0.53158991089658691
		8.3933129811111715e-21 0 8.8817841970012523e-16
		-0.65767691874013945 0 8.8817841970012523e-16
		0.65767691874013945 0 8.8817841970012523e-16
		8.3933129811111715e-21 -0.53158991089659935 -0.3872351947802386
		-0.65767691874013945 0 8.8817841970012523e-16
		8.3933129811111715e-21 0 8.8817841970012523e-16
		8.3933129811111715e-21 0.53158991089642882 0.38723519478023505
		8.3933129811111715e-21 -0.53158991089659935 -0.3872351947802386
		8.3933129811111715e-21 0 8.8817841970012523e-16
		-1.4602521827698505e-16 -0.38723519478034518 0.53158991089658159
		0.65767691874013945 0 8.8817841970012523e-16
		1.4604200490294727e-16 0.3872351947802315 -0.53158991089658691
		-0.65767691874013945 0 8.8817841970012523e-16
		-1.4602521827698505e-16 -0.38723519478034518 0.53158991089658159
		;
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
select -ne :ikSystem;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".gsn";
	setAttr -k on ".gsv";
	setAttr -s 4 ".sol";
connectAttr "bpjnt_m_Tougue_001.s" "bpjnt_l_TougueSIdeE_001.is";
connectAttr "bpjnt_l_TougueSIdeE_001.s" "bpjnt_l_TougueSIdeE_002.is";
connectAttr "bpjnt_l_TougueSIdeE_002.s" "bpjnt_l_TougueSIdeE_003.is";
connectAttr "bpjnt_m_Tougue_001.s" "bpjnt_r_TougueSIdeE_001.is";
connectAttr "bpjnt_r_TougueSIdeE_001.s" "bpjnt_r_TougueSIdeE_002.is";
connectAttr "bpjnt_r_TougueSIdeE_002.s" "bpjnt_r_TougueSIdeE_003.is";
connectAttr "bpjnt_m_Tougue_001.s" "bpjnt_m_Tougue_002.is";
connectAttr "bpjnt_m_Tougue_002.s" "bpjnt_l_TougueSIdeD_001.is";
connectAttr "bpjnt_l_TougueSIdeD_001.s" "bpjnt_l_TougueSIdeD_002.is";
connectAttr "bpjnt_l_TougueSIdeD_002.s" "bpjnt_l_TougueSIdeD_003.is";
connectAttr "bpjnt_m_Tougue_002.s" "bpjnt_r_TougueSIdeD_001.is";
connectAttr "bpjnt_r_TougueSIdeD_001.s" "bpjnt_r_TougueSIdeD_002.is";
connectAttr "bpjnt_r_TougueSIdeD_002.s" "bpjnt_r_TougueSIdeD_003.is";
connectAttr "bpjnt_m_Tougue_002.s" "bpjnt_m_Tougue_003.is";
connectAttr "bpjnt_m_Tougue_003.s" "bpjnt_l_TougueSIdeC_001.is";
connectAttr "bpjnt_l_TougueSIdeC_001.s" "bpjnt_l_TougueSIdeC_002.is";
connectAttr "bpjnt_l_TougueSIdeC_002.s" "bpjnt_l_TougueSIdeC_003.is";
connectAttr "bpjnt_m_Tougue_003.s" "bpjnt_r_TougueSIdeC_001.is";
connectAttr "bpjnt_r_TougueSIdeC_001.s" "bpjnt_r_TougueSIdeC_002.is";
connectAttr "bpjnt_r_TougueSIdeC_002.s" "bpjnt_r_TougueSIdeC_003.is";
connectAttr "bpjnt_m_Tougue_003.s" "bpjnt_m_Tougue_004.is";
connectAttr "bpjnt_m_Tougue_004.s" "bpjnt_l_TougueSIdeB_001.is";
connectAttr "bpjnt_l_TougueSIdeB_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_l_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_l_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_l_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002|bpjnt_l_TougueSIdeB_003.is"
		;
connectAttr "bpjnt_m_Tougue_004.s" "bpjnt_r_TougueSIdeB_001.is";
connectAttr "bpjnt_r_TougueSIdeB_001.s" "bpjnt_r_TougueSIdeB_002.is";
connectAttr "bpjnt_r_TougueSIdeB_002.s" "bpjnt_r_TougueSIdeB_003.is";
connectAttr "bpjnt_m_Tougue_004.s" "bpjnt_m_Tougue_005.is";
connectAttr "bpjnt_m_Tougue_005.s" "bpjnt_l_TougueSIdeA_001.is";
connectAttr "bpjnt_l_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_l_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "bpjnt_l_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_l_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_l_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_l_TougueSIdeA_001.s" "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|bpjnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_008|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_m_Tougue_005.s" "bpjnt_r_TougueSIdeA_001.is";
connectAttr "bpjnt_r_TougueSIdeA_001.s" "bpjnt_r_TougueSIdeA_002.is";
connectAttr "bpjnt_r_TougueSIdeA_002.s" "bpjnt_r_TougueSIdeA_003.is";
connectAttr "bpjnt_m_Tougue_005.s" "jntl_TougueSIdeA_001.is";
connectAttr "jntl_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001.s" "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002.is"
		;
connectAttr "jntl_TougueSIdeA_001_jntl_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001.s" "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001.s" "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_003|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001.s" "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001.s" "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_001|jntl_TougueSIdeA_001_jnt_l_TougueSIdeA_005|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_003.is"
		;
connectAttr "bpjnt_m_Tougue_005.s" "jntl_TougueSIdeA_002.is";
connectAttr "jntl_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_002.s" "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_002.s" "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_002.s" "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_004.is"
		;
connectAttr "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jntl_TougueSIdeA_002.s" "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_005.is"
		;
connectAttr "jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_005.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jntl_TougueSIdeA_002|jntl_TougueSIdeA_002_jnt_l_TougueSIdeA_005|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "bpjnt_m_Tougue_005.s" "jnt_l_TougueSIdeA_001.is";
connectAttr "jnt_l_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|bpjnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_001.s" "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_003|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_001.s" "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_005|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_001.s" "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_001|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_007|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_m_Tougue_005.s" "jnt_l_TougueSIdeA_002.is";
connectAttr "jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_002.s" "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_002.s" "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_002|jnt_l_TougueSIdeA_002_jnt_l_TougueSIdeA_003|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_m_Tougue_005.s" "jnt_l_TougueSIdeA_003.is";
connectAttr "jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|bpjnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_003.s" "jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_003|jnt_l_TougueSIdeA_003_jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_m_Tougue_005.s" "jnt_l_TougueSIdeA_004.is";
connectAttr "jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_003|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_002|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_004|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "jnt_l_TougueSIdeA_004.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006|bpjnt_l_TougueSIdeA_003.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|bpjnt_m_Tougue_005|jnt_l_TougueSIdeA_004|jnt_l_TougueSIdeA_001_jnt_l_TougueSIdeA_006|jntl_TougueSIdeA_001_jntl_TougueSIdeA_002_jntl_TougueSIdeA_004.is"
		;
connectAttr "bpjnt_m_Tougue_004.s" "jntl_TougueSIdeB_001.is";
connectAttr "jntl_TougueSIdeB_001.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|jntl_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002.is"
		;
connectAttr "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|jntl_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002.s" "|Face_Rig|Tougue_Rig|Tougue_Rig_Jnt|bpjnt_m_Tougue_001|bpjnt_m_Tougue_002|bpjnt_m_Tougue_003|bpjnt_m_Tougue_004|jntl_TougueSIdeB_001|bpjnt_l_TougueSIdeB_002|bpjnt_l_TougueSIdeB_003.is"
		;
connectAttr "bpjnt_m_Chin_001.s" "bpjnt_m_ChinEnd_001.is";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
// End of face.ma
