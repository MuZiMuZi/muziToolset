//Maya ASCII 2023 scene
//Name: face_guide.ma
//Last modified: Mon, Aug 31, 2026 10:39:36 AM
//Codeset: 936
requires maya "2023";
requires "stereoCamera" "10.0";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "5.2.1.1";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2023";
fileInfo "version" "2023";
fileInfo "cutIdentifier" "202211021031-847a9f9623";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "FC32A97D-4683-76DA-E1A9-A8B66863BE4B";
createNode transform -n "grp_md_face_guide_001";
	rename -uid "A5D2D7C1-42D3-9F38-D74F-379A3A7E4921";
	setAttr ".t" -type "double3" 0 395.41895762905739 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 4.8249478340148908 155.65348362177491 28.47299763228412 ;
	setAttr ".sp" -type "double3" 4.8249478340148908 155.65348362177491 28.47299763228412 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.72000003 0.72000003 0.72000003 ;
createNode transform -n "ctrl_md_face_move_001" -p "grp_md_face_guide_001";
	rename -uid "749E185B-465C-E4CD-DDC1-E6B9FA94F27B";
	setAttr ".t" -type "double3" 0 377.90694843005963 -26.101674136922082 ;
	setAttr ".rp" -type "double3" 4.8249478340148908 155.65348362177491 28.47299763228412 ;
	setAttr ".sp" -type "double3" 4.8249478340148908 155.65348362177491 28.47299763228412 ;
createNode nurbsCurve -n "ctrl_md_face_move_001Shape" -p "ctrl_md_face_move_001";
	rename -uid "BEB52669-4DDC-66EF-7711-D181616F06DF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 86 0 no 3
		91 24 24 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45
		 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72
		 72 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97
		 98 99 100 101 102 103 104 105 106 107 108 108 108
		89
		4.8249478340148926 66.120140630758755 28.472997632284095
		8.6263773074179895 75.527840574084522 28.472997632284084
		16.229236254224176 69.02931295126595 28.472997632284095
		27.438394137697642 71.258953082199966 28.472997632284091
		38.260629685283305 74.932607029250534 28.472997632284088
		48.510771446271384 79.98741755485436 28.472997632284088
		58.013436653255241 86.336895449459917 28.472997632284084
		66.606032069906817 93.872399385882773 28.472997632284084
		74.141536006329716 102.46499480253433 28.472997632284084
		80.491013900935329 111.96766000951817 28.472997632284084
		85.545824426539099 122.21780177050634 28.472997632284084
		89.219478373589652 133.04003731809189 28.472997632284088
		91.449118504523724 144.2491952015655 28.472997632284091
		81.701327070296045 155.65348362177485 28.472997632284066
		91.449118504523753 167.05777204198404 28.472997632284095
		89.219478373589681 178.2669299254575 28.472997632284098
		85.545824426539099 189.08916547304298 28.472997632284098
		80.491013900935357 199.33930723403125 28.472997632284102
		74.141536006329773 208.84197244101523 28.472997632284105
		66.606032069906817 217.43456785766662 28.472997632284113
		58.013436653255255 224.97007179408956 28.47299763228412
		48.510771446271399 231.31954968869519 28.472997632284127
		38.260629685283334 236.37436021429903 28.47299763228413
		27.438394137697671 240.04801416134958 28.472997632284137
		16.229236254224269 242.27765429228319 28.472997632284141
		4.8249478340148908 232.52986285805582 28.472997632284159
		-6.5793405861944469 242.2776542922835 28.472997632284148
		-17.788498469667918 240.0480141613497 28.472997632284152
		-28.610734017253549 236.37436021429906 28.472997632284152
		-38.860875778241684 231.3195496886953 28.472997632284152
		-48.363540985225505 224.97007179408965 28.472997632284155
		-56.956136401877153 217.43456785766676 28.472997632284155
		-64.491640338299916 208.84197244101529 28.472997632284155
		-70.841118232905615 199.33930723403131 28.472997632284155
		-75.895928758509399 189.0891654730431 28.472997632284155
		-79.569582705559881 178.26692992545753 28.472997632284152
		-81.799222836493939 167.05777204198412 28.472997632284152
		-72.05143140226626 155.65348362177485 28.472997632284169
		-81.799222836493939 144.24919520156556 28.472997632284144
		-79.569582705559881 133.04003731809189 28.472997632284141
		-75.895928758509427 122.21780177050634 28.472997632284141
		-70.841118232905558 111.96766000951814 28.472997632284134
		-64.491640338299916 102.46499480253433 28.47299763228413
		-56.956136401877153 93.87239938588273 28.472997632284123
		-48.363540985225505 86.336895449459917 28.47299763228412
		-38.860875778241642 79.987417554854332 28.472997632284109
		-28.610734017253556 74.932607029250562 28.472997632284105
		-17.788498469667918 71.258953082199966 28.472997632284102
		-6.5793405861944718 69.029312951265922 28.472997632284098
		1.0235183606117717 75.527840574084522 28.472997632284088
		4.8249478340148926 66.120140630758783 28.472997632284095
		-0.46145231923033936 64.786488212262029 28.472997632284098
		-11.034252625720748 65.71148838080336 28.472997632284098
		-26.411579304629981 69.831830646166608 28.472997632284102
		-40.839799912876835 76.559820409341924 28.472997632284109
		-53.880520268311692 85.691031105902169 28.47299763228412
		-65.137504681857664 96.948015519448177 28.472997632284127
		-74.268715378418023 109.98873587488303 28.472997632284134
		-80.996705141593324 124.41695648312998 28.472997632284141
		-85.117047406956587 139.79428316203911 28.472997632284144
		-86.504547659768491 155.65348362177485 28.472997632284152
		-85.117047406956587 171.51268408151037 28.472997632284152
		-80.996705141593353 186.89001076041967 28.472997632284155
		-74.268715378418023 201.31823136866637 28.472997632284155
		-65.137504681857664 214.3589517241013 28.472997632284159
		-53.880520268311734 225.61593613764737 28.472997632284155
		-40.839799912876806 234.74714683420785 28.472997632284155
		-26.41157930462996 241.47513659738303 28.472997632284152
		-11.034252625720731 245.59547886274621 28.472997632284152
		4.8249478340148979 246.98297911555824 28.472997632284144
		20.684148293750521 245.59547886274578 28.472997632284141
		36.06147497265971 241.47513659738291 28.472997632284134
		50.489695580906556 234.74714683420771 28.472997632284127
		63.53041593634147 225.6159361376472 28.47299763228412
		74.78740034988742 214.35895172410127 28.472997632284109
		83.918611046447651 201.31823136866635 28.472997632284102
		90.646600809623024 186.89001076041961 28.472997632284098
		94.766943074986244 171.51268408151034 28.472997632284095
		96.154443327798219 155.65348362177485 28.472997632284091
		94.766943074986244 139.79428316203919 28.472997632284088
		90.646600809623052 124.41695648312999 28.472997632284084
		83.91861104644768 109.9887358748831 28.472997632284084
		74.78740034988742 96.948015519448191 28.472997632284081
		63.530415936341498 85.691031105902269 28.472997632284084
		50.489695580906556 76.559820409341938 28.472997632284084
		36.06147497265971 69.831830646166651 28.472997632284088
		20.6841482937505 65.71148838080336 28.472997632284091
		10.111347987260093 64.786488212262029 28.472997632284095
		4.8249478340148926 66.120140630758755 28.472997632284095
		;
createNode transform -n "grp_md_ear_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "ECAC0A9E-44FC-FC55-5717-85B8FC29BBF8";
	setAttr ".t" -type "double3" -1.7763568394002505e-15 -4.5093141948105995 -44.118020044792218 ;
	setAttr ".rp" -type "double3" 4.824947834014889 160.16279781658545 72.591017677076337 ;
	setAttr ".sp" -type "double3" 4.8249478340148908 160.16279781658545 72.591017677076337 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "zero_lf_ear_guide_001" -p "grp_md_ear_guide_001";
	rename -uid "5AD22EE2-44C2-07DC-82D7-07BDFD7E2223";
	setAttr ".rp" -type "double3" 57.396249988682236 145.50662663491426 89.584364431345577 ;
	setAttr ".sp" -type "double3" 57.396249988682236 145.50662663491426 89.584364431345577 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_lf_ear_guide_001" -p "zero_lf_ear_guide_001";
	rename -uid "CE2DC240-4F3D-62A9-7C18-738A8B213D42";
	setAttr ".t" -type "double3" 45.944458946915773 -17.392176016747726 84.515780835539815 ;
	setAttr ".r" -type "double3" 14.402794894414733 -20.517611544491459 8.4899510036892873e-16 ;
	setAttr ".rp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".sp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_lf_ear_guide_001Shape" -p "loc_lf_ear_guide_001";
	rename -uid "2B72E20F-4164-E642-5ACE-FCAF86A274D1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr ".lp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_ear_guide_002" -p "loc_lf_ear_guide_001";
	rename -uid "052DD907-4D85-A785-6A9B-679FB0508C63";
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_lf_ear_guide_002" -p "zero_lf_ear_guide_002";
	rename -uid "9E82B89D-4EC1-6557-ADFB-4393F3A23166";
	setAttr ".t" -type "double3" 0 0 -9.3147123328639339 ;
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_lf_ear_guide_002Shape" -p "loc_lf_ear_guide_002";
	rename -uid "BA8408E7-4F25-D346-B158-F785639BD455";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr ".lp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_ear_guide_003" -p "loc_lf_ear_guide_002";
	rename -uid "3C095879-43B1-9588-200B-D6A5A756F426";
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_lf_ear_guide_003" -p "zero_lf_ear_guide_003";
	rename -uid "654B2BBA-428E-C541-BA43-21B145480A43";
	setAttr ".t" -type "double3" 0 0 -9.3147123328639339 ;
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_lf_ear_guide_003Shape" -p "loc_lf_ear_guide_003";
	rename -uid "C307EE4B-4EAE-D7AD-7308-66ACC1CCDF6E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr ".lp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_ear_guide_001" -p "grp_md_ear_guide_001";
	rename -uid "081BB4A7-4725-D22A-A098-6CA04E8EE154";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".rp" -type "double3" 58.16942443661172 147.82970928458886 -72.099951861450947 ;
	setAttr ".rpt" -type "double3" -116.33884887322344 0 144.19990372290189 ;
	setAttr ".sp" -type "double3" 58.16942443661172 147.82970928458889 72.099951861450947 ;
	setAttr ".spt" -type "double3" 0 -2.8421709430403995e-14 -144.19990372290189 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_rt_ear_guide_001" -p "zero_rt_ear_guide_001";
	rename -uid "5D3DF421-41A0-528F-0623-42AB03581B27";
	setAttr ".rp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".sp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_rt_ear_guide_001Shape" -p "loc_rt_ear_guide_001";
	rename -uid "7F718270-403B-929A-8EAD-4387D81CB4E0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "zero_rt_ear_guide_002" -p "loc_rt_ear_guide_001";
	rename -uid "28DD8639-4A09-FD2D-E695-82A85F15B4FC";
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_rt_ear_guide_002" -p "zero_rt_ear_guide_002";
	rename -uid "62D663DA-4FF0-CC28-CB7C-178989C7EF09";
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_rt_ear_guide_002Shape" -p "loc_rt_ear_guide_002";
	rename -uid "2E65DF77-48EC-86C7-7EF7-61B8494D8D98";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "zero_rt_ear_guide_003" -p "loc_rt_ear_guide_002";
	rename -uid "C15D6A44-472B-7D45-3EBC-E1AF9F31D272";
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_rt_ear_guide_003" -p "zero_rt_ear_guide_003";
	rename -uid "38A22965-433D-382F-1247-3FAEDC858D45";
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_rt_ear_guide_003Shape" -p "loc_rt_ear_guide_003";
	rename -uid "5A184271-4109-9102-FF95-FD881A64DEBB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "grp_md_nose_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "892B1807-4501-0B32-E4D7-9D87F41A8184";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -4.5093141948105995 -44.11802004479226 ;
	setAttr ".rp" -type "double3" 4.8249478340148917 -217.74415061347423 98.692691813998465 ;
	setAttr ".sp" -type "double3" 4.8249478340148917 -217.74415061347423 98.692691813998465 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "zero_md_muzzle_guide_001" -p "grp_md_nose_guide_001";
	rename -uid "6594C598-489F-C52A-78E8-A893CB50AA35";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 161.21337924600084 133.36231185566166 ;
	setAttr ".sp" -type "double3" 0 161.21337924600084 133.36231185566166 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.72000003 0.72000003 0.72000003 ;
createNode transform -n "loc_md_muzzle_guide_001" -p "zero_md_muzzle_guide_001";
	rename -uid "FFD0BC90-41CC-07E3-9245-30B099B43FC2";
	setAttr ".t" -type "double3" 0 -26.271796813103492 70.37691591786735 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" 0 187.48517605910428 62.985395937794308 ;
	setAttr ".sp" -type "double3" 0 187.48517605910428 62.985395937794308 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.72000003 0.72000003 0.72000003 ;
createNode locator -n "loc_md_muzzle_guide_001Shape" -p "loc_md_muzzle_guide_001";
	rename -uid "2C40F566-4D8F-6184-22B9-F48A7DA7707B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 16;
	setAttr ".lp" -type "double3" 0 187.48517605910433 62.985395937794308 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_guide_001" -p "loc_md_muzzle_guide_001";
	rename -uid "5833872B-4F0C-2CB7-DA27-47809A4E88F3";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" -3.9944532589595495e-16 162.54214477539057 6.2591342926025391 ;
	setAttr ".sp" -type "double3" -3.9944532589595495e-16 162.54214477539057 6.2591342926025391 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "loc_md_nose_guide_001" -p "zero_md_nose_guide_001";
	rename -uid "39C8150E-4106-9293-953D-518425DF75B2";
	setAttr ".t" -type "double3" 0 17.785676901527609 61.405784484233024 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" -3.9944532589595495e-16 162.54214477539057 6.2591342926025391 ;
	setAttr ".sp" -type "double3" -3.9944532589595495e-16 162.54214477539057 6.2591342926025391 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_guide_001Shape" -p "loc_md_nose_guide_001";
	rename -uid "A9477F89-4474-CDC8-B2E7-A3AD7528D3F3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".lp" -type "double3" -3.9944532589595495e-16 162.54214477539062 6.2591342926025391 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_center_guide_001" -p "loc_md_nose_guide_001";
	rename -uid "2BDF9790-4668-5A3C-D091-14A125B959CB";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0.0031950360898326115 159.34211938672212 8.1356919210806247 ;
	setAttr ".sp" -type "double3" 0.0031950360898326115 159.34211938672212 8.1356919210806247 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "loc_md_nose_center_guide_001" -p "zero_md_nose_center_guide_001";
	rename -uid "546C26C7-4536-9BB3-EEB9-EE910F564B16";
	setAttr ".t" -type "double3" 0 -12.568160097719669 1.2544033208710204 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" 0.0031950360898326115 159.34211938672212 8.1356919210806247 ;
	setAttr ".sp" -type "double3" 0.0031950360898326115 159.34211938672212 8.1356919210806247 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_center_guide_001Shape" -p "loc_md_nose_center_guide_001";
	rename -uid "2FAFC4BA-4F24-C1D7-41DB-EC96CA89D140";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".lp" -type "double3" 0.0031950360898326115 159.34211938672217 8.1356919210806247 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_front_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "B0BB3E12-47AD-A7DF-F30C-42BC2C0C015F";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0.0019079342662663412 159.5866186092249 9.3060853632271474 ;
	setAttr ".sp" -type "double3" 0.0019079342662663412 159.5866186092249 9.3060853632271474 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "loc_md_nose_front_guide_001" -p "zero_md_nose_front_guide_001";
	rename -uid "3B15B0E3-4F64-F378-A73F-16A5F29FC0EF";
	setAttr ".t" -type "double3" 0 2.3078078170142362 10.126013960805906 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" 0.0019079342662671195 159.58661860922496 9.3060853632271474 ;
	setAttr ".sp" -type "double3" 0.0019079342662671195 159.58661860922496 9.3060853632271474 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_front_guide_001Shape" -p "loc_md_nose_front_guide_001";
	rename -uid "3BC24A6E-4A92-0136-95B2-57A41778B920";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".lp" -type "double3" 0.0019079342662663412 159.58661860922496 9.3060853632271474 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_nose_side_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "436A3950-476E-B2ED-7B36-C3BA785DCFBE";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 1.45680555141727 159.19060817425753 7.6486067491517842 ;
	setAttr ".sp" -type "double3" 1.45680555141727 159.19060817425753 7.6486067491517842 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "loc_lf_nose_side_guide_001" -p "zero_lf_nose_side_guide_001";
	rename -uid "EE62081E-4DD3-F99D-5FA6-39AC258ECF58";
	setAttr ".t" -type "double3" 9.1657981872558594 155.86830337936408 7.6563758591335755 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_lf_nose_side_guide_001Shape" -p "loc_lf_nose_side_guide_001";
	rename -uid "C490F424-4EEE-968E-40AF-03B2AB3798E7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_down_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "C61E917B-4F34-B477-7EC6-7589685A8202";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0.0019079342662663412 159.5866186092249 9.3060853632271474 ;
	setAttr ".sp" -type "double3" 0.0019079342662663412 159.5866186092249 9.3060853632271474 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "loc_md_nose_down_guide_001" -p "zero_md_nose_down_guide_001";
	rename -uid "20666179-448F-2F32-DD3E-66B332D4B008";
	setAttr ".t" -type "double3" 0 151.89918716842658 9.768390629641388 ;
	setAttr -l on ".tx";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_down_guide_001Shape" -p "loc_md_nose_down_guide_001";
	rename -uid "6CDBBE18-4492-1D4C-D3EC-919EB45AA034";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_nose_side_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "5BE4EC84-4EBB-70B3-BD94-278E0C33B379";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "loc_rt_nose_side_guide_001" -p "zero_rt_nose_side_guide_001";
	rename -uid "4EFD5CA3-4CAD-4056-9831-328DE632A061";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_rt_nose_side_guide_001Shape" -p "loc_rt_nose_side_guide_001";
	rename -uid "D702618B-4047-977F-5454-598FC662C9F8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "grp_md_eye_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "1B85A707-461B-8295-9DE1-4EA3C1F1EBFF";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -4.5093141948105995 -44.11802004479226 ;
	setAttr ".rp" -type "double3" 4.8249478340148917 160.1627978165854 72.59101767707638 ;
	setAttr ".sp" -type "double3" 4.8249478340148917 160.1627978165854 72.59101767707638 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "grp_md_eye_ball_guide_001" -p "grp_md_eye_guide_001";
	rename -uid "96911500-477D-03F6-81ED-898739344762";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "zero_lf_eye_ball_guide_001" -p "grp_md_eye_ball_guide_001";
	rename -uid "72903033-4CC0-9EE7-4CFE-0C97061082F6";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 3.6603161618113518 163.24768972396845 2.9115569144487363 ;
	setAttr ".sp" -type "double3" 3.6603161618113518 163.24768972396845 2.9115569144487363 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "loc_lf_eye_ball_guide_001" -p "zero_lf_eye_ball_guide_001";
	rename -uid "D52C8DEA-409E-1ABF-28ED-76B5041BF2A9";
	setAttr ".t" -type "double3" 21.69341666251421 -3.0030938441342983 111.2736953193286 ;
	setAttr ".rp" -type "double3" 3.6603161618113518 163.24768972396845 2.9115569144487363 ;
	setAttr ".sp" -type "double3" 3.6603161618113518 163.24768972396845 2.9115569144487363 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_lf_eye_ball_guide_001Shape" -p "loc_lf_eye_ball_guide_001";
	rename -uid "A3C15B87-4FC1-09DD-0266-458EC3196C04";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
	setAttr ".lp" -type "double3" 3.6603161618113518 163.24768972396851 2.9115569144487363 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_eye_iris_guide_001" -p "loc_lf_eye_ball_guide_001";
	rename -uid "25EB4600-4E67-41FB-24E3-5AA91936CE00";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".sp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "loc_lf_eye_iris_guide_001" -p "zero_lf_eye_iris_guide_001";
	rename -uid "745DF5BF-4769-79C3-64EA-099F10B89E8D";
	setAttr ".t" -type "double3" 0.37263267487287433 -0.06343698501569861 13.780650809407236 ;
	setAttr ".rp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".sp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_lf_eye_iris_guide_001Shape" -p "loc_lf_eye_iris_guide_001";
	rename -uid "980A65F0-49AF-A5A4-F5EC-ABB0F55AF7BD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
	setAttr ".lp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_eye_ball_guide_001" -p "grp_md_eye_ball_guide_001";
	rename -uid "59A0AAC5-4296-C5B6-A581-5DBF0A8A0E61";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "loc_rt_eye_ball_guide_001" -p "zero_rt_eye_ball_guide_001";
	rename -uid "9FF5774B-42F5-F23C-20B8-7D9B9CB68659";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_rt_eye_ball_guide_001Shape" -p "loc_rt_eye_ball_guide_001";
	rename -uid "137FBEF5-4712-F587-ED14-B0A3C7FA085C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
createNode transform -n "zero_rt_eye_iris_guide_001" -p "loc_rt_eye_ball_guide_001";
	rename -uid "76EAF117-460A-B2F3-1F36-C4908A3C6872";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "loc_rt_eye_iris_guide_001" -p "zero_rt_eye_iris_guide_001";
	rename -uid "3A3A6E67-436D-3C43-CCC0-0D9366048655";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_rt_eye_iris_guide_001Shape" -p "loc_rt_eye_iris_guide_001";
	rename -uid "798C0C30-4914-D842-BAB7-A3A19434234F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
createNode transform -n "grp_md_eye_lid_guide_001" -p "grp_md_eye_guide_001";
	rename -uid "58E8DE21-4097-A2B1-C7EC-098CCEB9E895";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "zero_lf_inner_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "1AC18C81-4C74-B4B9-AC66-9EB803A632F3";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_inner_lid_guide_001" -p "zero_lf_inner_lid_guide_001";
	rename -uid "09E84E3B-400E-1E37-EA5F-E7A9FB3B9687";
	setAttr ".t" -type "double3" 14.655315399169977 922.99768066406625 58.630111694336179 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_inner_lid_guide_001Shape" -p "loc_lf_inner_lid_guide_001";
	rename -uid "7A151FBE-4855-9820-3777-FB8DCD68EE13";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "BB3F26AD-47D2-1B43-2FBA-F181C8813AE9";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_upper_lid_guide_001" -p "zero_lf_upper_lid_guide_001";
	rename -uid "8D1DB03C-46F1-9F22-4AE3-BE8D6FA12637";
	setAttr ".t" -type "double3" 21.070215693261247 932.416259765625 63.126163482666016 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_upper_lid_guide_001Shape" -p "loc_lf_upper_lid_guide_001";
	rename -uid "C878F0F4-4176-BA63-D0F3-AE86D16500F9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_lid_guide_002" -p "grp_md_eye_lid_guide_001";
	rename -uid "86F50D8E-4D4A-9E05-7D0D-1096AB222EAB";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_upper_lid_guide_002" -p "zero_lf_upper_lid_guide_002";
	rename -uid "A63C46E7-4F99-3517-4530-7D9410C6AC0C";
	setAttr ".t" -type "double3" 31.373639878217148 935.31620104311492 61.769050598144531 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_upper_lid_guide_002Shape" -p "loc_lf_upper_lid_guide_002";
	rename -uid "8B9CD884-4AAD-17D2-5EC2-43893C15C32D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_lid_guide_003" -p "grp_md_eye_lid_guide_001";
	rename -uid "E1D35193-4FC2-2704-EDA5-9B8C054EBDB6";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_upper_lid_guide_003" -p "zero_lf_upper_lid_guide_003";
	rename -uid "6AF248B8-4505-A109-26A5-9BB22340260E";
	setAttr ".t" -type "double3" 39.100810366552118 932.46839565548237 58.748008728027344 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_upper_lid_guide_003Shape" -p "loc_lf_upper_lid_guide_003";
	rename -uid "C7BB16B4-4FEB-1869-7E75-5B9E4D79B560";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_outer_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "7DD87E3B-4EA1-22C9-F076-9B92BF5C3584";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_outer_lid_guide_001" -p "zero_lf_outer_lid_guide_001";
	rename -uid "7E221072-48C1-9468-2DC0-C3B6A1866869";
	setAttr ".t" -type "double3" 42.03558731079108 927.76257324218875 50.447769165039126 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_outer_lid_guide_001Shape" -p "loc_lf_outer_lid_guide_001";
	rename -uid "2007BC2D-47BB-254B-B832-CB9E8B141438";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "4356745D-436E-A51E-31D4-BEAD438CC48E";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_lower_lid_guide_001" -p "zero_lf_lower_lid_guide_001";
	rename -uid "1BB4C40D-4921-33A1-3B3E-ACA9ACE40362";
	setAttr ".t" -type "double3" 21.904081850007824 919.42087542244542 61.780749368238389 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_lower_lid_guide_001Shape" -p "loc_lf_lower_lid_guide_001";
	rename -uid "3F0A341C-4A6A-2E82-BD6A-B880C3B18537";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_lid_guide_002" -p "grp_md_eye_lid_guide_001";
	rename -uid "FA8E8248-41F8-B4EA-614E-6E9EF1F93810";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_lower_lid_guide_002" -p "zero_lf_lower_lid_guide_002";
	rename -uid "6D5E2522-4C16-DEAD-B0C6-319DB21EBC6C";
	setAttr ".t" -type "double3" 31.673681259155273 919.26068115234375 60.724639892578125 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_lower_lid_guide_002Shape" -p "loc_lf_lower_lid_guide_002";
	rename -uid "304DCF6B-43D1-7684-FE36-01A254B293FC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_lid_guide_003" -p "grp_md_eye_lid_guide_001";
	rename -uid "D05EC112-4DB3-2E66-18B2-BA99F6B6AAEE";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_lower_lid_guide_003" -p "zero_lf_lower_lid_guide_003";
	rename -uid "E2A2AE1A-40AD-F774-E70A-A8A3BCAC2FEA";
	setAttr ".t" -type "double3" 38.504032135009766 921.49102783203125 56.063362121582031 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_lower_lid_guide_003Shape" -p "loc_lf_lower_lid_guide_003";
	rename -uid "BCEEAC45-4178-860E-67CC-019D2812F3EE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_rt_inner_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "165563EA-4C37-711B-7228-99AB8317B1F2";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_inner_lid_guide_001" -p "zero_rt_inner_lid_guide_001";
	rename -uid "C82F2E77-4C72-C3B5-9851-05991D60B329";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_inner_lid_guide_001Shape" -p "loc_rt_inner_lid_guide_001";
	rename -uid "2F9578E2-423B-B366-487D-7E886795DE14";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_lower_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "A9AE505A-4917-FD6E-89AC-4A8A476FE209";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_lower_lid_guide_001" -p "zero_rt_lower_lid_guide_001";
	rename -uid "0C64196B-405A-12FA-14B9-11B757835764";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_lower_lid_guide_001Shape" -p "loc_rt_lower_lid_guide_001";
	rename -uid "EC160600-486C-EDCC-3CA1-7086FECD5422";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_lower_lid_guide_002" -p "grp_md_eye_lid_guide_001";
	rename -uid "8876DB0D-4649-4356-08F1-0FA395CB9F92";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_lower_lid_guide_002" -p "zero_rt_lower_lid_guide_002";
	rename -uid "D759A6EF-4A50-BC63-C1EA-FDA545AA5407";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_lower_lid_guide_002Shape" -p "loc_rt_lower_lid_guide_002";
	rename -uid "96C293C3-4D45-4455-54F6-28B392D821D8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_lower_lid_guide_003" -p "grp_md_eye_lid_guide_001";
	rename -uid "8E088C8E-4340-E8F6-A162-939C1B648901";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_lower_lid_guide_003" -p "zero_rt_lower_lid_guide_003";
	rename -uid "D44F9A49-4BD5-7E93-77E1-0B86E2618C75";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_lower_lid_guide_003Shape" -p "loc_rt_lower_lid_guide_003";
	rename -uid "E507D499-4E0A-61BC-3B23-30842431A8F4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_outer_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "94CDA3AD-40DD-48FF-ABA9-718F92DFFF10";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_outer_lid_guide_001" -p "zero_rt_outer_lid_guide_001";
	rename -uid "45BC6312-416F-D1C0-3DBD-B69A25B525DA";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_outer_lid_guide_001Shape" -p "loc_rt_outer_lid_guide_001";
	rename -uid "92E9718B-48D8-0F96-C59F-ACB0FA7E22B2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_upper_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "295597C2-423D-D606-3C3B-9EA11BCEC671";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_upper_lid_guide_001" -p "zero_rt_upper_lid_guide_001";
	rename -uid "21B8CC28-4C3D-92F9-7539-D9921D2EF8F8";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_upper_lid_guide_001Shape" -p "loc_rt_upper_lid_guide_001";
	rename -uid "D28FB1C7-4D34-E693-0761-0D9439617E79";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_upper_lid_guide_002" -p "grp_md_eye_lid_guide_001";
	rename -uid "E43C6E51-4041-819D-74EB-00A5A9DE1F43";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_upper_lid_guide_002" -p "zero_rt_upper_lid_guide_002";
	rename -uid "9834A177-4DCD-EFA7-A6AD-50AEC11584D6";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_upper_lid_guide_002Shape" -p "loc_rt_upper_lid_guide_002";
	rename -uid "96DF6A54-4637-C6BA-B31D-0493634B5FFB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_upper_lid_guide_003" -p "grp_md_eye_lid_guide_001";
	rename -uid "35BB262E-4BD6-0A82-F2A3-548F7D43AD59";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_upper_lid_guide_003" -p "zero_rt_upper_lid_guide_003";
	rename -uid "8D483943-4D3E-D97E-3834-C0AB4713072D";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_upper_lid_guide_003Shape" -p "loc_rt_upper_lid_guide_003";
	rename -uid "A402B199-479F-4001-DD91-E696B18A57FE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "grp_md_eye_bags_guide_001" -p "grp_md_eye_guide_001";
	rename -uid "7D016F91-460E-281D-7FF5-EAA7C789AF80";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_lf_inner_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "C5A5922D-4A52-D690-A7F5-E892C228A41E";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_inner_eye_bag_guide_001" -p "zero_lf_inner_eye_bag_guide_001";
	rename -uid "84FFA05D-4788-6FA3-C488-A9A81DC2B475";
	setAttr ".t" -type "double3" 11.095543861389174 921.770446777345 61.916465759277429 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_inner_eye_bag_guide_001Shape" -p "loc_lf_inner_eye_bag_guide_001";
	rename -uid "99052911-42EB-52FC-39D9-BA8ACB1E19FC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "57E0EE65-45A5-83AD-7EE7-D48E3ACF96CD";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_upper_eye_bag_guide_001" -p "zero_lf_upper_eye_bag_guide_001";
	rename -uid "95498487-4E93-ED09-4733-619E0E1CB4E1";
	setAttr ".t" -type "double3" 17.322137832641602 935.3453369140625 62.539287567138672 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_upper_eye_bag_guide_001Shape" -p "loc_lf_upper_eye_bag_guide_001";
	rename -uid "A01F2C4C-42DD-4015-3102-769588EFF3D4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_eye_bag_guide_002" -p "grp_md_eye_bags_guide_001";
	rename -uid "994A7B61-46CB-A15D-1CA4-A292941EEC0D";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_upper_eye_bag_guide_002" -p "zero_lf_upper_eye_bag_guide_002";
	rename -uid "4688FA7C-4419-3D72-5ECF-8A8C1D0237AC";
	setAttr ".t" -type "double3" 27.721637725830078 939.0982666015625 62.341476440429688 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_upper_eye_bag_guide_002Shape" -p "loc_lf_upper_eye_bag_guide_002";
	rename -uid "8C6FB650-40E8-0E10-85D3-A4B8D1F6ED71";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_eye_bag_guide_003" -p "grp_md_eye_bags_guide_001";
	rename -uid "7D604EFC-4046-DDB7-D5AF-69B428B66255";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_upper_eye_bag_guide_003" -p "zero_lf_upper_eye_bag_guide_003";
	rename -uid "38760715-40C6-3774-A616-56B8B2601036";
	setAttr ".t" -type "double3" 41.111030578613281 935.79002564748384 57.854137420654297 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_upper_eye_bag_guide_003Shape" -p "loc_lf_upper_eye_bag_guide_003";
	rename -uid "96854016-49E6-9528-88EB-62A08691EA56";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_outer_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "26DEAADA-42F3-B650-1600-FA8A1058BA86";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_outer_eye_bag_guide_001" -p "zero_lf_outer_eye_bag_guide_001";
	rename -uid "4F6C5DDD-4105-726B-4B40-35B84904B812";
	setAttr ".t" -type "double3" 44.514404296875 927.34466552734375 48.438819885253906 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_outer_eye_bag_guide_001Shape" -p "loc_lf_outer_eye_bag_guide_001";
	rename -uid "3ED80679-4561-B968-733C-A9AB50C0C2EB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "96E496B7-40C5-7F55-EFAF-6298456A6ECD";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_lower_eye_bag_guide_001" -p "zero_lf_lower_eye_bag_guide_001";
	rename -uid "930B1F06-4C5A-C9D3-0D1F-C7ABE18680BA";
	setAttr ".t" -type "double3" 20.479196548461914 915.51069325865478 62.755046844482422 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_lower_eye_bag_guide_001Shape" -p "loc_lf_lower_eye_bag_guide_001";
	rename -uid "259F57C0-4FF0-A1F2-6B12-C1BAF9AE635C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_eye_bag_guide_002" -p "grp_md_eye_bags_guide_001";
	rename -uid "FB350846-49FD-3F1C-84FD-F3A03768D01A";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_lower_eye_bag_guide_002" -p "zero_lf_lower_eye_bag_guide_002";
	rename -uid "C1A4DF76-475F-D4B3-BFFE-5EAA071520F1";
	setAttr ".t" -type "double3" 31.809101104736328 913.813335719973 59.792583465576172 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_lower_eye_bag_guide_002Shape" -p "loc_lf_lower_eye_bag_guide_002";
	rename -uid "0B4BF142-45B7-A497-E62A-01AFA6F2F647";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_eye_bag_guide_003" -p "grp_md_eye_bags_guide_001";
	rename -uid "AB72EB9F-44E6-1ABD-96B6-84BC6F23E54E";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_lower_eye_bag_guide_003" -p "zero_lf_lower_eye_bag_guide_003";
	rename -uid "F79E43D5-446F-3503-D132-D6905FD035B0";
	setAttr ".t" -type "double3" 41.439169523881127 918.83096443881573 53.821247100830078 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_lower_eye_bag_guide_003Shape" -p "loc_lf_lower_eye_bag_guide_003";
	rename -uid "A449047F-4728-7CB1-9BF9-56B88FC0DAAB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_rt_inner_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "73C35511-4AA1-278C-12EC-A7846F069764";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_inner_eye_bag_guide_001" -p "zero_rt_inner_eye_bag_guide_001";
	rename -uid "EE4CC5D3-4D2B-1D67-D214-91844016D272";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_inner_eye_bag_guide_001Shape" -p "loc_rt_inner_eye_bag_guide_001";
	rename -uid "3669EAD8-4E85-33DF-7879-D395A896CCD5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_lower_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "3787F740-4B51-D6D5-653C-1586D6ADF7A9";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_lower_eye_bag_guide_001" -p "zero_rt_lower_eye_bag_guide_001";
	rename -uid "C007AF6C-440E-B33B-ADA2-01BFED89CE56";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_lower_eye_bag_guide_001Shape" -p "loc_rt_lower_eye_bag_guide_001";
	rename -uid "250F4FEC-488A-8A39-3653-5FAE34115BF7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_lower_eye_bag_guide_002" -p "grp_md_eye_bags_guide_001";
	rename -uid "E37387F0-47AF-CF57-9C47-EFAA63B3A221";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_lower_eye_bag_guide_002" -p "zero_rt_lower_eye_bag_guide_002";
	rename -uid "6EB98985-43C5-C99A-51D1-39AF7BBB9EAA";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_lower_eye_bag_guide_002Shape" -p "loc_rt_lower_eye_bag_guide_002";
	rename -uid "A873AACA-48E6-9345-E17D-09AFF8EFCC88";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_lower_eye_bag_guide_003" -p "grp_md_eye_bags_guide_001";
	rename -uid "AA2A9213-43A0-F33C-53E0-078EB2E3A459";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_lower_eye_bag_guide_003" -p "zero_rt_lower_eye_bag_guide_003";
	rename -uid "10B4058D-4528-B016-F6A7-0A8D59B874A5";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_lower_eye_bag_guide_003Shape" -p "loc_rt_lower_eye_bag_guide_003";
	rename -uid "74962708-4F31-C86D-E678-F59CA37AC905";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_outer_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "E32E8010-4953-2766-DE74-E09DDF8140EB";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_outer_eye_bag_guide_001" -p "zero_rt_outer_eye_bag_guide_001";
	rename -uid "8DA256D3-456D-151B-6DBB-9B8EFB0B7D6C";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_outer_eye_bag_guide_001Shape" -p "loc_rt_outer_eye_bag_guide_001";
	rename -uid "4324A00D-4552-492D-C069-87AE1C91890E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_upper_eye_bag_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "E0D931C8-4D37-2FB3-FF1D-EA90F972A44F";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_upper_eye_bag_guide_001" -p "zero_rt_upper_eye_bag_guide_001";
	rename -uid "40184F62-4CC3-C67F-B2F1-398B043201F8";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_upper_eye_bag_guide_001Shape" -p "loc_rt_upper_eye_bag_guide_001";
	rename -uid "C12508A2-4AB7-D4F4-88C0-FA809D7B696F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_upper_eye_bag_guide_002" -p "grp_md_eye_bags_guide_001";
	rename -uid "CC21BAF3-4AC7-BFDA-276F-4DB843CB67CD";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_upper_eye_bag_guide_002" -p "zero_rt_upper_eye_bag_guide_002";
	rename -uid "829FB51C-4ED4-A766-5893-D399BEF8F5DC";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_upper_eye_bag_guide_002Shape" -p "loc_rt_upper_eye_bag_guide_002";
	rename -uid "B0B691D7-47B5-937A-E509-869FE5B0B4CC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_upper_eye_bag_guide_003" -p "grp_md_eye_bags_guide_001";
	rename -uid "5F97DDB6-45F5-8048-22AE-338683CF27F8";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_upper_eye_bag_guide_003" -p "zero_rt_upper_eye_bag_guide_003";
	rename -uid "A3F405CF-4B19-6BD6-FF13-95A854670CD0";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_upper_eye_bag_guide_003Shape" -p "loc_rt_upper_eye_bag_guide_003";
	rename -uid "10BEC715-4FDB-F0FB-AC3B-FEA662D5059F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "grp_md_jaw_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "B3C27627-4927-A049-E26E-57B5D02BA6EC";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -4.5093141948119637 -44.11802004479226 ;
	setAttr ".rp" -type "double3" 4.8249478340148917 160.16279781658676 72.59101767707638 ;
	setAttr ".sp" -type "double3" 4.8249478340148917 160.16279781658676 72.59101767707638 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode transform -n "zero_md_jaw_start_guide_001" -p "grp_md_jaw_guide_001";
	rename -uid "DE1A4FAE-451D-B8B1-D0A0-058919860991";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".sp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode transform -n "loc_md_jaw_start_guide_001" -p "zero_md_jaw_start_guide_001";
	rename -uid "ED19DA6F-4B93-7DE2-9708-37B970FF1BC2";
	setAttr ".t" -type "double3" 0 -32.408103494802162 75.620242775090802 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".sp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode locator -n "loc_md_jaw_start_guide_001Shape" -p "loc_md_jaw_start_guide_001";
	rename -uid "9CC072B8-4871-18E1-A18E-0B874EFA9373";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 21;
	setAttr ".ovrgb" -type "float3" 1 0.41999999 0.079999998 ;
	setAttr ".lp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_jaw_end_guide_001" -p "loc_md_jaw_start_guide_001";
	rename -uid "E7507DD1-4021-37CF-0619-09B542BBEE4B";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 2.2154738956068891e-07 123.82179118444549 59.96978168513391 ;
	setAttr ".sp" -type "double3" 2.2154738956068891e-07 123.82179118444549 59.96978168513391 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode transform -n "loc_md_jaw_end_guide_001" -p "zero_md_jaw_end_guide_001";
	rename -uid "543428FE-469F-24EC-04E9-2C9150C9185F";
	setAttr ".t" -type "double3" 0 134.18644025680953 54.256952348413087 ;
	setAttr -l on ".tx";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode locator -n "loc_md_jaw_end_guide_001Shape" -p "loc_md_jaw_end_guide_001";
	rename -uid "15F41D04-41C6-5564-8D9E-F8A9F263B69A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 21;
	setAttr ".ovrgb" -type "float3" 1 0.41999999 0.079999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "grp_md_brow_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "44491867-4A9A-E9B5-B90E-27BB355406D3";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_lf_brow_main_guide_001" -p "grp_md_brow_guide_001";
	rename -uid "F73AD3C7-4DAE-06E7-5888-72A183D3D81D";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_lf_brow_main_guide_001" -p "zero_lf_brow_main_guide_001";
	rename -uid "950D15FD-4EEE-933E-ADFD-9C947140475A";
	setAttr ".t" -type "double3" 27.038382291793823 945.65768257164905 68.284600829618725 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_main_guide_001Shape" -p "loc_lf_brow_main_guide_001";
	rename -uid "1B36B863-418F-6BE0-2FD2-6EB758D22551";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_001" -p "loc_lf_brow_main_guide_001";
	rename -uid "EF5115E8-4005-70AD-011A-AB92128C3AE3";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_lf_brow_guide_001" -p "zero_lf_brow_guide_001";
	rename -uid "8460E4D3-45B7-DAE0-56ED-3FA412BBF003";
	setAttr ".t" -type "double3" -18.947298765182495 -3.4152509310240475 2.9878448490922125 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_001Shape" -p "loc_lf_brow_guide_001";
	rename -uid "C5EBBBBE-4D9A-7CA4-D403-5A8C94C9599F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_002" -p "loc_lf_brow_main_guide_001";
	rename -uid "84868472-4717-735B-734D-70B1AAF58B23";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_lf_brow_guide_002" -p "zero_lf_brow_guide_002";
	rename -uid "F6500564-4635-3D08-AB02-65B81F21832D";
	setAttr ".t" -type "double3" -8.570239782333374 -1.7668744661802975 1.0016807560746344 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_002Shape" -p "loc_lf_brow_guide_002";
	rename -uid "CFD471F4-4C48-1F4F-013C-CEB28583FF0C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_003" -p "loc_lf_brow_main_guide_001";
	rename -uid "EB1C2A61-44B2-FFDD-4094-44AE9711CBA4";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_lf_brow_guide_003" -p "zero_lf_brow_guide_003";
	rename -uid "8D1AEE26-4118-B8DF-C2EB-FC9363385FB2";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_003Shape" -p "loc_lf_brow_guide_003";
	rename -uid "CFC0CE28-4DFB-FF7F-6D03-42A11A720152";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_004" -p "loc_lf_brow_main_guide_001";
	rename -uid "6092BD3A-4B98-6EF6-E9DE-87ADCB9CA133";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_lf_brow_guide_004" -p "zero_lf_brow_guide_004";
	rename -uid "5F391B55-4A44-6FA3-C457-38AE4FF1DB7B";
	setAttr ".t" -type "double3" 9.2975475788116455 0.94894584631970247 -4.629571532743725 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_004Shape" -p "loc_lf_brow_guide_004";
	rename -uid "74620936-4D2B-E778-DFF3-318E8CD1FA51";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_005" -p "loc_lf_brow_main_guide_001";
	rename -uid "DE3D7688-4A31-F8E1-36F6-DD8B2C367EA2";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_lf_brow_guide_005" -p "zero_lf_brow_guide_005";
	rename -uid "8F1A0D30-4413-A3A1-0FC4-C7AC97E6F5BD";
	setAttr ".t" -type "double3" 19.132313966751099 -3.9316693880552975 -18.969853972929272 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_005Shape" -p "loc_lf_brow_guide_005";
	rename -uid "08384441-4B92-90B4-021D-DE846CAF2518";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_brow_main_guide_001" -p "grp_md_brow_guide_001";
	rename -uid "7CB24C73-4DBD-7D78-5B75-998699926EF6";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_main_guide_001" -p "zero_rt_brow_main_guide_001";
	rename -uid "2FE4B4AE-4290-530F-FA96-0F8CE7B78498";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_main_guide_001Shape" -p "loc_rt_brow_main_guide_001";
	rename -uid "04C3ECF3-4C11-2F25-1DCF-188786C1F7DB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_001" -p "loc_rt_brow_main_guide_001";
	rename -uid "961C3AD6-40DF-C417-F68A-458E2271B8BB";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_001" -p "zero_rt_brow_guide_001";
	rename -uid "53C50ED3-4B71-86DB-99CE-A7903993973F";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_001Shape" -p "loc_rt_brow_guide_001";
	rename -uid "176FB8BA-46A5-3906-46E4-DABFEC2AE238";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_002" -p "loc_rt_brow_main_guide_001";
	rename -uid "CE1C192E-4418-4D0E-C3EE-168AFA8FBC9E";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_002" -p "zero_rt_brow_guide_002";
	rename -uid "1EA61A02-4B91-11A5-5788-00904E3C81F5";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_002Shape" -p "loc_rt_brow_guide_002";
	rename -uid "FEC04966-4AB1-047F-52EC-2C94054E4D7E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_003" -p "loc_rt_brow_main_guide_001";
	rename -uid "F348DECF-4C72-8F7E-25A0-A0B2E4834458";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_003" -p "zero_rt_brow_guide_003";
	rename -uid "931A7B60-4CF8-C5DA-36B9-4C805EABF8D1";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_003Shape" -p "loc_rt_brow_guide_003";
	rename -uid "4045E452-41F0-9DDE-4C3C-6A85D7F1FA59";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_004" -p "loc_rt_brow_main_guide_001";
	rename -uid "991AE29B-425F-8B8B-6706-BD82F64E25F0";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_004" -p "zero_rt_brow_guide_004";
	rename -uid "DED21B10-4B70-01E5-33D2-20A405D48A1B";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_004Shape" -p "loc_rt_brow_guide_004";
	rename -uid "8EDCBBA2-4265-7373-E2C6-D8A1ABD365CE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_005" -p "loc_rt_brow_main_guide_001";
	rename -uid "F3FD4D3B-4E70-9A08-653B-84A1427736CE";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_005" -p "zero_rt_brow_guide_005";
	rename -uid "AAD623DF-4F5C-C717-5F66-709048D5B881";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_005Shape" -p "loc_rt_brow_guide_005";
	rename -uid "B7E089AB-469D-C8E5-1778-A9BF30CA1500";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "grp_md_teeth_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "15EB9144-45C1-D105-9BD1-B2B22A25A134";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode transform -n "zero_md_upper_teeth_guide_001" -p "grp_md_teeth_guide_001";
	rename -uid "C7E87B40-4241-D57A-59C4-9DB8BCBC201E";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode transform -n "loc_md_upper_teeth_guide_001" -p "zero_md_upper_teeth_guide_001";
	rename -uid "F6849542-4C20-B12A-82F9-87BE31239AAB";
	setAttr ".t" -type "double3" 0.0009918212890625 893.0157470703125 53.838485717773438 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode locator -n "loc_md_upper_teeth_guide_001Shape" -p "loc_md_upper_teeth_guide_001";
	rename -uid "E9FF8BC7-4F91-3D52-D07C-7C8EAB427B33";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 16;
	setAttr ".ovrgb" -type "float3" 0.92000002 0.92000002 0.77999997 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_md_lower_teeth_guide_001" -p "grp_md_teeth_guide_001";
	rename -uid "D144F077-4584-31EA-5BA6-71B8461DFAE8";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode transform -n "loc_md_lower_teeth_guide_001" -p "zero_md_lower_teeth_guide_001";
	rename -uid "F8872321-4BCB-C1E2-B22B-D58B4236ED8C";
	setAttr ".t" -type "double3" 0.010724067687988281 888.985107421875 53.342178344726562 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode locator -n "loc_md_lower_teeth_guide_001Shape" -p "loc_md_lower_teeth_guide_001";
	rename -uid "22B8D23A-4EC6-D717-2629-7D91E1BF4B9D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 16;
	setAttr ".ovrgb" -type "float3" 0.92000002 0.92000002 0.77999997 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "grp_md_lip_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "DAFF2637-4084-02FC-FE0B-BDB062D26E64";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_md_upper_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "411E10D2-4FFF-1376-8782-658137A5BB03";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_md_upper_lip_guide_001" -p "zero_md_upper_lip_guide_001";
	rename -uid "1B5D00BB-4144-AB9F-F066-7EAB387E9521";
	setAttr ".t" -type "double3" 0 892.22186279296875 74.020088195800781 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_md_upper_lip_guide_001Shape" -p "loc_md_upper_lip_guide_001";
	rename -uid "F9700EDC-4ADE-3FE8-C430-67A83D7AFC68";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_lower_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "70452215-46C6-0499-520C-C4BF589DA050";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_md_lower_lip_guide_001" -p "zero_md_lower_lip_guide_001";
	rename -uid "CABE9592-4C61-9906-35BD-9EB739385B66";
	setAttr ".t" -type "double3" 0 882.94843394032011 74.020088195800781 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_md_lower_lip_guide_001Shape" -p "loc_md_lower_lip_guide_001";
	rename -uid "1310CE19-4750-CBFC-28D4-0AA2F4C0AC61";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_upper_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "21DBBB5B-41C4-0348-35FE-9CACF1532C96";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_lf_upper_lip_guide_001" -p "zero_lf_upper_lip_guide_001";
	rename -uid "B0618E03-4CB3-8F28-1EA8-FB93215E4A75";
	setAttr ".t" -type "double3" 6.5477989414050422 892.76502109125295 72.939836177230916 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_upper_lip_guide_001Shape" -p "loc_lf_upper_lip_guide_001";
	rename -uid "14AA8968-4310-2B93-0C9A-F58251487164";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_upper_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "C2E99EE4-43EA-1958-669E-1F932E358E40";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_lf_upper_lip_guide_002" -p "zero_lf_upper_lip_guide_002";
	rename -uid "E2F373CC-431D-61B5-03BE-6E830B810A74";
	setAttr ".t" -type "double3" 10.205770930650683 890.63682479554507 69.150216379277666 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_upper_lip_guide_002Shape" -p "loc_lf_upper_lip_guide_002";
	rename -uid "C4B9EFFD-46FF-18CE-1768-188B945F951E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_lower_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "C027DCE2-480B-C4F1-DA21-378EE5E65819";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_lf_lower_lip_guide_001" -p "zero_lf_lower_lip_guide_001";
	rename -uid "19AC1D2B-41DC-C5A6-DC1D-FCAAD6EBB142";
	setAttr ".t" -type "double3" 6.6253784360383987 883.47470036636889 69.648095703382168 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_lower_lip_guide_001Shape" -p "loc_lf_lower_lip_guide_001";
	rename -uid "5A31A5D3-4EF7-4011-0AE8-F790E3A1C513";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_lower_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "EEC88CBB-405A-664B-CBFB-04B4C430E0D8";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_lf_lower_lip_guide_002" -p "zero_lf_lower_lip_guide_002";
	rename -uid "11AB951D-44F5-A322-89D3-82ACF7C73B58";
	setAttr ".t" -type "double3" 10.211730939521074 886.85846770270939 68.357601887976926 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_lower_lip_guide_002Shape" -p "loc_lf_lower_lip_guide_002";
	rename -uid "54C2D636-454F-2791-07A1-CBAE672275EB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_mouth_corner_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "8BFED679-484F-78BF-92B2-03A45D7E1279";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_lf_mouth_corner_guide_001" -p "zero_lf_mouth_corner_guide_001";
	rename -uid "808A1D41-43D2-1A6B-DB3B-9295CBE717ED";
	setAttr ".t" -type "double3" 14.916315078735352 888.8077392578125 63.507129669189453 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_mouth_corner_guide_001Shape" -p "loc_lf_mouth_corner_guide_001";
	rename -uid "ECEE7556-4A56-676F-0DF6-E38EB228EDEF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_lower_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "527ED4C3-4467-9AEC-1676-1C80D965AEAE";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_lower_lip_guide_001" -p "zero_rt_lower_lip_guide_001";
	rename -uid "E9CFF3F4-4162-7A3B-EACB-ECA0B8F6C6D3";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_lower_lip_guide_001Shape" -p "loc_rt_lower_lip_guide_001";
	rename -uid "6DA2F28E-4464-C08F-DCAF-2F89E9A4B1B8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_rt_lower_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "B7020BD5-479A-B400-6E54-8CAA353E3F7B";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_lower_lip_guide_002" -p "zero_rt_lower_lip_guide_002";
	rename -uid "E065A93F-40CC-B66C-6D56-87AAA5812616";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_lower_lip_guide_002Shape" -p "loc_rt_lower_lip_guide_002";
	rename -uid "66E831CA-4B52-7BF5-2CD9-A194223BACB7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_rt_mouth_corner_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "C7D15F87-4FCF-D2C2-CB6D-B1BD4582F7B7";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_mouth_corner_guide_001" -p "zero_rt_mouth_corner_guide_001";
	rename -uid "8EBD5F8D-4B48-B034-D184-70BC709648CF";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_mouth_corner_guide_001Shape" -p "loc_rt_mouth_corner_guide_001";
	rename -uid "890A3452-4B56-BF92-D10E-C1B4459D4679";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_rt_upper_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "1A5F360E-4314-016D-6F55-DA98F83AF2CF";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_upper_lip_guide_001" -p "zero_rt_upper_lip_guide_001";
	rename -uid "8BF76F77-46D9-39F5-0EC6-47B4A51B1DC9";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_upper_lip_guide_001Shape" -p "loc_rt_upper_lip_guide_001";
	rename -uid "0B5617D5-4934-9252-5B34-F9935BC97E26";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_rt_upper_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "4F36BA2A-4001-BC7B-8C3D-2DB532FD0FF3";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_upper_lip_guide_002" -p "zero_rt_upper_lip_guide_002";
	rename -uid "94F659BE-4855-D8EC-4B8F-9185AAEF6422";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_upper_lip_guide_002Shape" -p "loc_rt_upper_lip_guide_002";
	rename -uid "4F40BBBF-4858-4590-1300-B1B8F69E6C6C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "grp_md_tongue_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "FC8BBDE0-4284-2762-7A81-4488EE54B0C6";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode transform -n "zero_md_tongue_guide_001" -p "grp_md_tongue_guide_001";
	rename -uid "A5B1225B-4090-2155-16E9-24B3392DDBA1";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode transform -n "loc_md_tongue_guide_001" -p "zero_md_tongue_guide_001";
	rename -uid "9FEDCD23-4870-7669-AA9E-8BB1EBD30363";
	setAttr ".t" -type "double3" 0 884.68551007538588 21.481754293539911 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_001Shape" -p "loc_md_tongue_guide_001";
	rename -uid "EF99F9DB-481A-4B7B-8314-77B621E75A80";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_002" -p "loc_md_tongue_guide_001";
	rename -uid "56794A90-46B2-DA10-DF9B-67AEB4087CD5";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode transform -n "loc_md_tongue_guide_002" -p "zero_md_tongue_guide_002";
	rename -uid "028C3F5C-4FE0-4841-6876-8C84626162F3";
	setAttr ".t" -type "double3" 0 4.0712308883461219 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_002Shape" -p "loc_md_tongue_guide_002";
	rename -uid "8299DF29-4D98-33FF-BD76-CAA51FADE72A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_003" -p "loc_md_tongue_guide_002";
	rename -uid "36F2AF03-4038-C668-AB5B-1BB63967F478";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode transform -n "loc_md_tongue_guide_003" -p "zero_md_tongue_guide_003";
	rename -uid "C8001D8A-48B2-E6DC-8CFD-F39BA42D88D8";
	setAttr ".t" -type "double3" 0 4.0712308883461219 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_003Shape" -p "loc_md_tongue_guide_003";
	rename -uid "4BDCA2B5-46D8-A276-8C17-888240B98D7A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_004" -p "loc_md_tongue_guide_003";
	rename -uid "A83584A1-4E07-F963-9D0C-F49E02E7D280";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode transform -n "loc_md_tongue_guide_004" -p "zero_md_tongue_guide_004";
	rename -uid "B661B22E-47C2-014F-53F6-ADAD2D66A98C";
	setAttr ".t" -type "double3" 0 -2.65083241927789 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_004Shape" -p "loc_md_tongue_guide_004";
	rename -uid "72AFC297-4986-A487-701C-EB9E0DFBEB08";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_005" -p "loc_md_tongue_guide_004";
	rename -uid "4108748B-4443-70AF-4684-3E9BF473D9E4";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode transform -n "loc_md_tongue_guide_005" -p "zero_md_tongue_guide_005";
	rename -uid "A724A2E3-4307-C519-A30A-49AF507CB522";
	setAttr ".t" -type "double3" 0 -4.5214447098502433 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_005Shape" -p "loc_md_tongue_guide_005";
	rename -uid "084D410D-4D35-F2EE-E6DD-F2A331181112";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "grp_md_zygoma_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "77ED8793-433B-C382-BFB9-88959ED64D04";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode transform -n "zero_lf_zygoma_guide_001" -p "grp_md_zygoma_guide_001";
	rename -uid "60BBE4CA-4A49-EE1D-4789-E897E7BE43F6";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode transform -n "loc_lf_zygoma_guide_001" -p "zero_lf_zygoma_guide_001";
	rename -uid "5926EE39-477B-322C-00AB-518665478585";
	setAttr ".t" -type "double3" 10.599196434020996 916.290283203125 65.919540405273438 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode locator -n "loc_lf_zygoma_guide_001Shape" -p "loc_lf_zygoma_guide_001";
	rename -uid "94DD1B2D-4AEA-4116-D338-BFBA2C1D5286";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0.94999999 0.68000001 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_zygoma_guide_002" -p "grp_md_zygoma_guide_001";
	rename -uid "72F85D16-4F6E-A1BF-D8A5-BAB8E2316242";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode transform -n "loc_lf_zygoma_guide_002" -p "zero_lf_zygoma_guide_002";
	rename -uid "7ECBD80E-4E2B-D1E6-C4C1-4B9B27A2AE71";
	setAttr ".t" -type "double3" 26.95750617980957 907.423095703125 63.240692138671875 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode locator -n "loc_lf_zygoma_guide_002Shape" -p "loc_lf_zygoma_guide_002";
	rename -uid "076B05AA-4984-F185-1BE1-4FA52602A0BE";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_rt_zygoma_guide_001" -p "grp_md_zygoma_guide_001";
	rename -uid "287FF076-4830-3F2D-D41D-27ABCB47C7F8";
	setAttr ".s" -type "double3" -1 1 1 ;
createNode transform -n "loc_rt_zygoma_guide_001" -p "zero_rt_zygoma_guide_001";
	rename -uid "30089FEC-401E-A6B2-45EF-E9A6245D9B7B";
createNode locator -n "loc_rt_zygoma_guide_001Shape" -p "loc_rt_zygoma_guide_001";
	rename -uid "DA6AAEF8-47ED-4A36-44BA-609145D68D4B";
	setAttr -k off ".v";
createNode transform -n "zero_rt_zygoma_guide_002" -p "grp_md_zygoma_guide_001";
	rename -uid "09FF952B-4142-580F-8782-2FA2D6AAD33E";
	setAttr ".s" -type "double3" -1 1 1 ;
createNode transform -n "loc_rt_zygoma_guide_002" -p "zero_rt_zygoma_guide_002";
	rename -uid "BCF339FD-4817-59D2-CFFF-59A10623AD60";
createNode locator -n "loc_rt_zygoma_guide_002Shape" -p "loc_rt_zygoma_guide_002";
	rename -uid "1EDE3721-420E-6701-0D6F-E980B8AC5BF4";
	setAttr -k off ".v";
createNode transform -s -n "persp";
	rename -uid "EF5B9113-4915-066E-159D-66A0EA1EA6AC";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -8.2261182750269413 890.62649934375906 211.39801275237136 ;
	setAttr ".r" -type "double3" -0.93835272960256522 -2.2000000000005659 6.2166030182999065e-18 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "02439AC3-41B7-BDBF-7DFF-2F879356FCCF";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 138.22028649686436;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 892.22186279296875 74.020088195800781 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "5041CD41-400F-B3DF-24D6-37B625673249";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1020.4088851746753 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "865048E8-4B91-51DA-9957-57BA65DD6206";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1020.4088851746753;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "B331CC3B-4A79-4079-725C-AE8B439309CA";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1020.4088851746753 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "4C32779B-42CB-105D-6D84-628803B0AF27";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1020.4088851746753;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "58B9D5C3-43D4-405A-AED9-6F894E5267D4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1020.4088851746753 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "3937358F-4892-5FEE-90CB-6ABDFCDC1581";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1020.4088851746753;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "3C007B44-451D-CAA2-57B5-0C855424E79B";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "639B840B-47BC-7D02-0BA7-E0B12BE176A0";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "2973AAE0-4470-82DD-3264-CC8394DB01D7";
createNode displayLayerManager -n "layerManager";
	rename -uid "56F46A82-45C6-3642-1099-2483BC02363B";
createNode displayLayer -n "defaultLayer";
	rename -uid "9E0D7A24-41C7-9376-D977-CF80E55971E4";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "08BF7B62-4540-3CAD-40FF-BF91A408C113";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "34F4F415-4609-A8F5-64B8-24B9847360F3";
	setAttr ".g" yes;
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "A9D1AD88-4F4A-355B-9A2F-15A19783882D";
	setAttr ".version" -type "string" "5.2.1.1";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "31EA36FE-454E-FE3B-501C-E180A842640A";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "AAECEDD5-4121-EA8D-E927-399458D07303";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "315C101A-4213-BD7D-60BA-00BD0F076856";
	setAttr ".output_mode" 0;
	setAttr ".ai_translator" -type "string" "maya";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "1BAB8BAF-41E1-E348-929E-929BEF206F84";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"CgAbBlastPanelOptChangeCallback\" \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n"
		+ "            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n"
		+ "            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"CgAbBlastPanelOptChangeCallback\" \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n"
		+ "            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"CgAbBlastPanelOptChangeCallback\" \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n"
		+ "            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n"
		+ "            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n"
		+ "            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"CgAbBlastPanelOptChangeCallback\" \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 1\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n"
		+ "            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1156\n            -height 689\n            -sceneRenderFilter 0\n            $editorName;\n"
		+ "        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n"
		+ "            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n"
		+ "            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n"
		+ "            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n"
		+ "            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n"
		+ "                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n"
		+ "                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -valueLinesToggle 0\n                -outliner \"graphEditor1OutlineEd\" \n                -highlightAffectedCurves 0\n                $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n"
		+ "                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n"
		+ "                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n"
		+ "                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n"
		+ "                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 1\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n"
		+ "                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 1\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -editorChanged \"updateModelPanelBar\" \n                -camera \"|persp\" \n                -useInteractiveMode 0\n"
		+ "                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n"
		+ "                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n"
		+ "                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n"
		+ "                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n"
		+ "            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n"
		+ "            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n"
		+ "\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -editorChanged \\\"CgAbBlastPanelOptChangeCallback\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 1\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1156\\n    -height 689\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -editorChanged \\\"CgAbBlastPanelOptChangeCallback\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 1\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1156\\n    -height 689\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 100 -size 300 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "F65A7765-4DE0-202E-F2A8-6B8E00761C08";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 10 -ast 0 -aet 30 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
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
	setAttr -av -k on ".fzn";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rm";
	setAttr -av -k on ".lm";
	setAttr -av -k on ".hom";
	setAttr -av -k on ".hodm";
	setAttr -av -k on ".xry";
	setAttr -av -k on ".jxr";
	setAttr -av -k on ".sslt";
	setAttr -av -k on ".cbr";
	setAttr -av -k on ".bbr";
	setAttr -av -k on ".mhl";
	setAttr -k on ".cons";
	setAttr -k on ".vac";
	setAttr -av -k on ".hwi";
	setAttr -k on ".csvd";
	setAttr -av -k on ".ta";
	setAttr -av -k on ".tq";
	setAttr -k on ".ts";
	setAttr -av -k on ".etmr";
	setAttr -av -k on ".tmr";
	setAttr -av -k on ".aoon";
	setAttr -av -k on ".aoam";
	setAttr -av -k on ".aora";
	setAttr -av -k on ".aofr";
	setAttr -av -k on ".aosm";
	setAttr -av -k on ".hff";
	setAttr -av -k on ".hfd";
	setAttr -av -k on ".hfs";
	setAttr -av -k on ".hfe";
	setAttr -av ".hfc";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av -k on ".hfa";
	setAttr -av -k on ".mbe";
	setAttr -av -k on ".mbt";
	setAttr -av -k on ".mbsof";
	setAttr -k on ".mbsc";
	setAttr -k on ".mbc";
	setAttr -k on ".mbfa";
	setAttr -k on ".mbftb";
	setAttr -k on ".mbftg";
	setAttr -k on ".mbftr";
	setAttr -av -k on ".mbfta";
	setAttr -k on ".mbfe";
	setAttr -k on ".mbme";
	setAttr -av -k on ".mbcsx";
	setAttr -av -k on ".mbcsy";
	setAttr -av -k on ".mbasx";
	setAttr -av -k on ".mbasy";
	setAttr -av -k on ".blen";
	setAttr -av -k on ".blth";
	setAttr -av -k on ".blfr";
	setAttr -av -k on ".blfa";
	setAttr -av -k on ".blat";
	setAttr -av -k on ".msaa";
	setAttr -av -k on ".aasc";
	setAttr -av -k on ".aasq";
	setAttr -k on ".laa";
	setAttr -k on ".fprt" yes;
	setAttr -k on ".rtfm";
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
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -k on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -av -cb on ".ren";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -k on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -k on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".exrc";
	setAttr -av -k on ".expt";
	setAttr -av -k on ".an";
	setAttr -k on ".ar";
	setAttr -av -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -av -k on ".me";
	setAttr -k on ".se";
	setAttr -av -k on ".be";
	setAttr -av -cb on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -k on ".ofe";
	setAttr -k on ".efe";
	setAttr -k on ".oft";
	setAttr -k on ".umfn";
	setAttr -k on ".ufe";
	setAttr -av -k on ".pff";
	setAttr -av -k on ".peie";
	setAttr -av -k on ".ifp";
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
	setAttr -k on ".gv";
	setAttr -k on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -k on ".isp";
	setAttr -av -k on ".uf";
	setAttr -av -k on ".oi";
	setAttr -av -k on ".rut";
	setAttr -av -k on ".mot";
	setAttr -av -k on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -av -k on ".pram";
	setAttr -av -k on ".poam";
	setAttr -av -k on ".prlm";
	setAttr -av -k on ".polm";
	setAttr -av -k on ".prm";
	setAttr -av -k on ".pom";
	setAttr -k on ".pfrm";
	setAttr -k on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -k on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -k on ".isl";
	setAttr -k on ".ism";
	setAttr -k on ".imb";
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
select -ne :defaultColorMgtGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
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
connectAttr "loc_lf_ear_guide_001.tx" "loc_rt_ear_guide_001.tx";
connectAttr "loc_lf_ear_guide_001.ty" "loc_rt_ear_guide_001.ty";
connectAttr "loc_lf_ear_guide_001.tz" "loc_rt_ear_guide_001.tz";
connectAttr "loc_lf_ear_guide_001.rx" "loc_rt_ear_guide_001.rx";
connectAttr "loc_lf_ear_guide_001.ry" "loc_rt_ear_guide_001.ry";
connectAttr "loc_lf_ear_guide_001.rz" "loc_rt_ear_guide_001.rz";
connectAttr "loc_lf_ear_guide_001.sx" "loc_rt_ear_guide_001.sx";
connectAttr "loc_lf_ear_guide_001.sy" "loc_rt_ear_guide_001.sy";
connectAttr "loc_lf_ear_guide_001.sz" "loc_rt_ear_guide_001.sz";
connectAttr "loc_lf_ear_guide_001.ro" "loc_rt_ear_guide_001.ro";
connectAttr "loc_lf_ear_guide_001.v" "loc_rt_ear_guide_001.v";
connectAttr "loc_lf_ear_guide_001Shape.lpx" "loc_rt_ear_guide_001Shape.lpx";
connectAttr "loc_lf_ear_guide_001Shape.lpy" "loc_rt_ear_guide_001Shape.lpy";
connectAttr "loc_lf_ear_guide_001Shape.lpz" "loc_rt_ear_guide_001Shape.lpz";
connectAttr "loc_lf_ear_guide_001Shape.lsx" "loc_rt_ear_guide_001Shape.lsx";
connectAttr "loc_lf_ear_guide_001Shape.lsy" "loc_rt_ear_guide_001Shape.lsy";
connectAttr "loc_lf_ear_guide_001Shape.lsz" "loc_rt_ear_guide_001Shape.lsz";
connectAttr "loc_lf_ear_guide_002.tx" "loc_rt_ear_guide_002.tx";
connectAttr "loc_lf_ear_guide_002.ty" "loc_rt_ear_guide_002.ty";
connectAttr "loc_lf_ear_guide_002.tz" "loc_rt_ear_guide_002.tz";
connectAttr "loc_lf_ear_guide_002.rx" "loc_rt_ear_guide_002.rx";
connectAttr "loc_lf_ear_guide_002.ry" "loc_rt_ear_guide_002.ry";
connectAttr "loc_lf_ear_guide_002.rz" "loc_rt_ear_guide_002.rz";
connectAttr "loc_lf_ear_guide_002.sx" "loc_rt_ear_guide_002.sx";
connectAttr "loc_lf_ear_guide_002.sy" "loc_rt_ear_guide_002.sy";
connectAttr "loc_lf_ear_guide_002.sz" "loc_rt_ear_guide_002.sz";
connectAttr "loc_lf_ear_guide_002.ro" "loc_rt_ear_guide_002.ro";
connectAttr "loc_lf_ear_guide_002.v" "loc_rt_ear_guide_002.v";
connectAttr "loc_lf_ear_guide_002Shape.lpx" "loc_rt_ear_guide_002Shape.lpx";
connectAttr "loc_lf_ear_guide_002Shape.lpy" "loc_rt_ear_guide_002Shape.lpy";
connectAttr "loc_lf_ear_guide_002Shape.lpz" "loc_rt_ear_guide_002Shape.lpz";
connectAttr "loc_lf_ear_guide_002Shape.lsx" "loc_rt_ear_guide_002Shape.lsx";
connectAttr "loc_lf_ear_guide_002Shape.lsy" "loc_rt_ear_guide_002Shape.lsy";
connectAttr "loc_lf_ear_guide_002Shape.lsz" "loc_rt_ear_guide_002Shape.lsz";
connectAttr "loc_lf_ear_guide_003.tx" "loc_rt_ear_guide_003.tx";
connectAttr "loc_lf_ear_guide_003.ty" "loc_rt_ear_guide_003.ty";
connectAttr "loc_lf_ear_guide_003.tz" "loc_rt_ear_guide_003.tz";
connectAttr "loc_lf_ear_guide_003.rx" "loc_rt_ear_guide_003.rx";
connectAttr "loc_lf_ear_guide_003.ry" "loc_rt_ear_guide_003.ry";
connectAttr "loc_lf_ear_guide_003.rz" "loc_rt_ear_guide_003.rz";
connectAttr "loc_lf_ear_guide_003.sx" "loc_rt_ear_guide_003.sx";
connectAttr "loc_lf_ear_guide_003.sy" "loc_rt_ear_guide_003.sy";
connectAttr "loc_lf_ear_guide_003.sz" "loc_rt_ear_guide_003.sz";
connectAttr "loc_lf_ear_guide_003.ro" "loc_rt_ear_guide_003.ro";
connectAttr "loc_lf_ear_guide_003.v" "loc_rt_ear_guide_003.v";
connectAttr "loc_lf_ear_guide_003Shape.lpx" "loc_rt_ear_guide_003Shape.lpx";
connectAttr "loc_lf_ear_guide_003Shape.lpy" "loc_rt_ear_guide_003Shape.lpy";
connectAttr "loc_lf_ear_guide_003Shape.lpz" "loc_rt_ear_guide_003Shape.lpz";
connectAttr "loc_lf_ear_guide_003Shape.lsx" "loc_rt_ear_guide_003Shape.lsx";
connectAttr "loc_lf_ear_guide_003Shape.lsy" "loc_rt_ear_guide_003Shape.lsy";
connectAttr "loc_lf_ear_guide_003Shape.lsz" "loc_rt_ear_guide_003Shape.lsz";
connectAttr "loc_lf_nose_side_guide_001.tx" "loc_rt_nose_side_guide_001.tx";
connectAttr "loc_lf_nose_side_guide_001.ty" "loc_rt_nose_side_guide_001.ty";
connectAttr "loc_lf_nose_side_guide_001.tz" "loc_rt_nose_side_guide_001.tz";
connectAttr "loc_lf_nose_side_guide_001.rx" "loc_rt_nose_side_guide_001.rx";
connectAttr "loc_lf_nose_side_guide_001.ry" "loc_rt_nose_side_guide_001.ry";
connectAttr "loc_lf_nose_side_guide_001.rz" "loc_rt_nose_side_guide_001.rz";
connectAttr "loc_lf_nose_side_guide_001.sx" "loc_rt_nose_side_guide_001.sx";
connectAttr "loc_lf_nose_side_guide_001.sy" "loc_rt_nose_side_guide_001.sy";
connectAttr "loc_lf_nose_side_guide_001.sz" "loc_rt_nose_side_guide_001.sz";
connectAttr "loc_lf_nose_side_guide_001.ro" "loc_rt_nose_side_guide_001.ro";
connectAttr "loc_lf_nose_side_guide_001.v" "loc_rt_nose_side_guide_001.v";
connectAttr "loc_lf_nose_side_guide_001Shape.lpx" "loc_rt_nose_side_guide_001Shape.lpx"
		;
connectAttr "loc_lf_nose_side_guide_001Shape.lpy" "loc_rt_nose_side_guide_001Shape.lpy"
		;
connectAttr "loc_lf_nose_side_guide_001Shape.lpz" "loc_rt_nose_side_guide_001Shape.lpz"
		;
connectAttr "loc_lf_nose_side_guide_001Shape.lsx" "loc_rt_nose_side_guide_001Shape.lsx"
		;
connectAttr "loc_lf_nose_side_guide_001Shape.lsy" "loc_rt_nose_side_guide_001Shape.lsy"
		;
connectAttr "loc_lf_nose_side_guide_001Shape.lsz" "loc_rt_nose_side_guide_001Shape.lsz"
		;
connectAttr "loc_lf_eye_ball_guide_001.tx" "loc_rt_eye_ball_guide_001.tx";
connectAttr "loc_lf_eye_ball_guide_001.ty" "loc_rt_eye_ball_guide_001.ty";
connectAttr "loc_lf_eye_ball_guide_001.tz" "loc_rt_eye_ball_guide_001.tz";
connectAttr "loc_lf_eye_ball_guide_001.rx" "loc_rt_eye_ball_guide_001.rx";
connectAttr "loc_lf_eye_ball_guide_001.ry" "loc_rt_eye_ball_guide_001.ry";
connectAttr "loc_lf_eye_ball_guide_001.rz" "loc_rt_eye_ball_guide_001.rz";
connectAttr "loc_lf_eye_ball_guide_001.sx" "loc_rt_eye_ball_guide_001.sx";
connectAttr "loc_lf_eye_ball_guide_001.sy" "loc_rt_eye_ball_guide_001.sy";
connectAttr "loc_lf_eye_ball_guide_001.sz" "loc_rt_eye_ball_guide_001.sz";
connectAttr "loc_lf_eye_ball_guide_001.ro" "loc_rt_eye_ball_guide_001.ro";
connectAttr "loc_lf_eye_ball_guide_001.v" "loc_rt_eye_ball_guide_001.v";
connectAttr "loc_lf_eye_ball_guide_001Shape.lpx" "loc_rt_eye_ball_guide_001Shape.lpx"
		;
connectAttr "loc_lf_eye_ball_guide_001Shape.lpy" "loc_rt_eye_ball_guide_001Shape.lpy"
		;
connectAttr "loc_lf_eye_ball_guide_001Shape.lpz" "loc_rt_eye_ball_guide_001Shape.lpz"
		;
connectAttr "loc_lf_eye_ball_guide_001Shape.lsx" "loc_rt_eye_ball_guide_001Shape.lsx"
		;
connectAttr "loc_lf_eye_ball_guide_001Shape.lsy" "loc_rt_eye_ball_guide_001Shape.lsy"
		;
connectAttr "loc_lf_eye_ball_guide_001Shape.lsz" "loc_rt_eye_ball_guide_001Shape.lsz"
		;
connectAttr "loc_lf_eye_iris_guide_001.tx" "loc_rt_eye_iris_guide_001.tx";
connectAttr "loc_lf_eye_iris_guide_001.ty" "loc_rt_eye_iris_guide_001.ty";
connectAttr "loc_lf_eye_iris_guide_001.tz" "loc_rt_eye_iris_guide_001.tz";
connectAttr "loc_lf_eye_iris_guide_001.rx" "loc_rt_eye_iris_guide_001.rx";
connectAttr "loc_lf_eye_iris_guide_001.ry" "loc_rt_eye_iris_guide_001.ry";
connectAttr "loc_lf_eye_iris_guide_001.rz" "loc_rt_eye_iris_guide_001.rz";
connectAttr "loc_lf_eye_iris_guide_001.sx" "loc_rt_eye_iris_guide_001.sx";
connectAttr "loc_lf_eye_iris_guide_001.sy" "loc_rt_eye_iris_guide_001.sy";
connectAttr "loc_lf_eye_iris_guide_001.sz" "loc_rt_eye_iris_guide_001.sz";
connectAttr "loc_lf_eye_iris_guide_001.ro" "loc_rt_eye_iris_guide_001.ro";
connectAttr "loc_lf_eye_iris_guide_001.v" "loc_rt_eye_iris_guide_001.v";
connectAttr "loc_lf_eye_iris_guide_001Shape.lpx" "loc_rt_eye_iris_guide_001Shape.lpx"
		;
connectAttr "loc_lf_eye_iris_guide_001Shape.lpy" "loc_rt_eye_iris_guide_001Shape.lpy"
		;
connectAttr "loc_lf_eye_iris_guide_001Shape.lpz" "loc_rt_eye_iris_guide_001Shape.lpz"
		;
connectAttr "loc_lf_eye_iris_guide_001Shape.lsx" "loc_rt_eye_iris_guide_001Shape.lsx"
		;
connectAttr "loc_lf_eye_iris_guide_001Shape.lsy" "loc_rt_eye_iris_guide_001Shape.lsy"
		;
connectAttr "loc_lf_eye_iris_guide_001Shape.lsz" "loc_rt_eye_iris_guide_001Shape.lsz"
		;
connectAttr "loc_lf_inner_lid_guide_001.tx" "loc_rt_inner_lid_guide_001.tx";
connectAttr "loc_lf_inner_lid_guide_001.ty" "loc_rt_inner_lid_guide_001.ty";
connectAttr "loc_lf_inner_lid_guide_001.tz" "loc_rt_inner_lid_guide_001.tz";
connectAttr "loc_lf_inner_lid_guide_001.rx" "loc_rt_inner_lid_guide_001.rx";
connectAttr "loc_lf_inner_lid_guide_001.ry" "loc_rt_inner_lid_guide_001.ry";
connectAttr "loc_lf_inner_lid_guide_001.rz" "loc_rt_inner_lid_guide_001.rz";
connectAttr "loc_lf_inner_lid_guide_001.sx" "loc_rt_inner_lid_guide_001.sx";
connectAttr "loc_lf_inner_lid_guide_001.sy" "loc_rt_inner_lid_guide_001.sy";
connectAttr "loc_lf_inner_lid_guide_001.sz" "loc_rt_inner_lid_guide_001.sz";
connectAttr "loc_lf_inner_lid_guide_001.ro" "loc_rt_inner_lid_guide_001.ro";
connectAttr "loc_lf_inner_lid_guide_001.v" "loc_rt_inner_lid_guide_001.v";
connectAttr "loc_lf_inner_lid_guide_001Shape.lpx" "loc_rt_inner_lid_guide_001Shape.lpx"
		;
connectAttr "loc_lf_inner_lid_guide_001Shape.lpy" "loc_rt_inner_lid_guide_001Shape.lpy"
		;
connectAttr "loc_lf_inner_lid_guide_001Shape.lpz" "loc_rt_inner_lid_guide_001Shape.lpz"
		;
connectAttr "loc_lf_inner_lid_guide_001Shape.lsx" "loc_rt_inner_lid_guide_001Shape.lsx"
		;
connectAttr "loc_lf_inner_lid_guide_001Shape.lsy" "loc_rt_inner_lid_guide_001Shape.lsy"
		;
connectAttr "loc_lf_inner_lid_guide_001Shape.lsz" "loc_rt_inner_lid_guide_001Shape.lsz"
		;
connectAttr "loc_lf_lower_lid_guide_001.tx" "loc_rt_lower_lid_guide_001.tx";
connectAttr "loc_lf_lower_lid_guide_001.ty" "loc_rt_lower_lid_guide_001.ty";
connectAttr "loc_lf_lower_lid_guide_001.tz" "loc_rt_lower_lid_guide_001.tz";
connectAttr "loc_lf_lower_lid_guide_001.rx" "loc_rt_lower_lid_guide_001.rx";
connectAttr "loc_lf_lower_lid_guide_001.ry" "loc_rt_lower_lid_guide_001.ry";
connectAttr "loc_lf_lower_lid_guide_001.rz" "loc_rt_lower_lid_guide_001.rz";
connectAttr "loc_lf_lower_lid_guide_001.sx" "loc_rt_lower_lid_guide_001.sx";
connectAttr "loc_lf_lower_lid_guide_001.sy" "loc_rt_lower_lid_guide_001.sy";
connectAttr "loc_lf_lower_lid_guide_001.sz" "loc_rt_lower_lid_guide_001.sz";
connectAttr "loc_lf_lower_lid_guide_001.ro" "loc_rt_lower_lid_guide_001.ro";
connectAttr "loc_lf_lower_lid_guide_001.v" "loc_rt_lower_lid_guide_001.v";
connectAttr "loc_lf_lower_lid_guide_001Shape.lpx" "loc_rt_lower_lid_guide_001Shape.lpx"
		;
connectAttr "loc_lf_lower_lid_guide_001Shape.lpy" "loc_rt_lower_lid_guide_001Shape.lpy"
		;
connectAttr "loc_lf_lower_lid_guide_001Shape.lpz" "loc_rt_lower_lid_guide_001Shape.lpz"
		;
connectAttr "loc_lf_lower_lid_guide_001Shape.lsx" "loc_rt_lower_lid_guide_001Shape.lsx"
		;
connectAttr "loc_lf_lower_lid_guide_001Shape.lsy" "loc_rt_lower_lid_guide_001Shape.lsy"
		;
connectAttr "loc_lf_lower_lid_guide_001Shape.lsz" "loc_rt_lower_lid_guide_001Shape.lsz"
		;
connectAttr "loc_lf_lower_lid_guide_002.tx" "loc_rt_lower_lid_guide_002.tx";
connectAttr "loc_lf_lower_lid_guide_002.ty" "loc_rt_lower_lid_guide_002.ty";
connectAttr "loc_lf_lower_lid_guide_002.tz" "loc_rt_lower_lid_guide_002.tz";
connectAttr "loc_lf_lower_lid_guide_002.rx" "loc_rt_lower_lid_guide_002.rx";
connectAttr "loc_lf_lower_lid_guide_002.ry" "loc_rt_lower_lid_guide_002.ry";
connectAttr "loc_lf_lower_lid_guide_002.rz" "loc_rt_lower_lid_guide_002.rz";
connectAttr "loc_lf_lower_lid_guide_002.sx" "loc_rt_lower_lid_guide_002.sx";
connectAttr "loc_lf_lower_lid_guide_002.sy" "loc_rt_lower_lid_guide_002.sy";
connectAttr "loc_lf_lower_lid_guide_002.sz" "loc_rt_lower_lid_guide_002.sz";
connectAttr "loc_lf_lower_lid_guide_002.ro" "loc_rt_lower_lid_guide_002.ro";
connectAttr "loc_lf_lower_lid_guide_002.v" "loc_rt_lower_lid_guide_002.v";
connectAttr "loc_lf_lower_lid_guide_002Shape.lpx" "loc_rt_lower_lid_guide_002Shape.lpx"
		;
connectAttr "loc_lf_lower_lid_guide_002Shape.lpy" "loc_rt_lower_lid_guide_002Shape.lpy"
		;
connectAttr "loc_lf_lower_lid_guide_002Shape.lpz" "loc_rt_lower_lid_guide_002Shape.lpz"
		;
connectAttr "loc_lf_lower_lid_guide_002Shape.lsx" "loc_rt_lower_lid_guide_002Shape.lsx"
		;
connectAttr "loc_lf_lower_lid_guide_002Shape.lsy" "loc_rt_lower_lid_guide_002Shape.lsy"
		;
connectAttr "loc_lf_lower_lid_guide_002Shape.lsz" "loc_rt_lower_lid_guide_002Shape.lsz"
		;
connectAttr "loc_lf_lower_lid_guide_003.tx" "loc_rt_lower_lid_guide_003.tx";
connectAttr "loc_lf_lower_lid_guide_003.ty" "loc_rt_lower_lid_guide_003.ty";
connectAttr "loc_lf_lower_lid_guide_003.tz" "loc_rt_lower_lid_guide_003.tz";
connectAttr "loc_lf_lower_lid_guide_003.rx" "loc_rt_lower_lid_guide_003.rx";
connectAttr "loc_lf_lower_lid_guide_003.ry" "loc_rt_lower_lid_guide_003.ry";
connectAttr "loc_lf_lower_lid_guide_003.rz" "loc_rt_lower_lid_guide_003.rz";
connectAttr "loc_lf_lower_lid_guide_003.sx" "loc_rt_lower_lid_guide_003.sx";
connectAttr "loc_lf_lower_lid_guide_003.sy" "loc_rt_lower_lid_guide_003.sy";
connectAttr "loc_lf_lower_lid_guide_003.sz" "loc_rt_lower_lid_guide_003.sz";
connectAttr "loc_lf_lower_lid_guide_003.ro" "loc_rt_lower_lid_guide_003.ro";
connectAttr "loc_lf_lower_lid_guide_003.v" "loc_rt_lower_lid_guide_003.v";
connectAttr "loc_lf_lower_lid_guide_003Shape.lpx" "loc_rt_lower_lid_guide_003Shape.lpx"
		;
connectAttr "loc_lf_lower_lid_guide_003Shape.lpy" "loc_rt_lower_lid_guide_003Shape.lpy"
		;
connectAttr "loc_lf_lower_lid_guide_003Shape.lpz" "loc_rt_lower_lid_guide_003Shape.lpz"
		;
connectAttr "loc_lf_lower_lid_guide_003Shape.lsx" "loc_rt_lower_lid_guide_003Shape.lsx"
		;
connectAttr "loc_lf_lower_lid_guide_003Shape.lsy" "loc_rt_lower_lid_guide_003Shape.lsy"
		;
connectAttr "loc_lf_lower_lid_guide_003Shape.lsz" "loc_rt_lower_lid_guide_003Shape.lsz"
		;
connectAttr "loc_lf_outer_lid_guide_001.tx" "loc_rt_outer_lid_guide_001.tx";
connectAttr "loc_lf_outer_lid_guide_001.ty" "loc_rt_outer_lid_guide_001.ty";
connectAttr "loc_lf_outer_lid_guide_001.tz" "loc_rt_outer_lid_guide_001.tz";
connectAttr "loc_lf_outer_lid_guide_001.rx" "loc_rt_outer_lid_guide_001.rx";
connectAttr "loc_lf_outer_lid_guide_001.ry" "loc_rt_outer_lid_guide_001.ry";
connectAttr "loc_lf_outer_lid_guide_001.rz" "loc_rt_outer_lid_guide_001.rz";
connectAttr "loc_lf_outer_lid_guide_001.sx" "loc_rt_outer_lid_guide_001.sx";
connectAttr "loc_lf_outer_lid_guide_001.sy" "loc_rt_outer_lid_guide_001.sy";
connectAttr "loc_lf_outer_lid_guide_001.sz" "loc_rt_outer_lid_guide_001.sz";
connectAttr "loc_lf_outer_lid_guide_001.ro" "loc_rt_outer_lid_guide_001.ro";
connectAttr "loc_lf_outer_lid_guide_001.v" "loc_rt_outer_lid_guide_001.v";
connectAttr "loc_lf_outer_lid_guide_001Shape.lpx" "loc_rt_outer_lid_guide_001Shape.lpx"
		;
connectAttr "loc_lf_outer_lid_guide_001Shape.lpy" "loc_rt_outer_lid_guide_001Shape.lpy"
		;
connectAttr "loc_lf_outer_lid_guide_001Shape.lpz" "loc_rt_outer_lid_guide_001Shape.lpz"
		;
connectAttr "loc_lf_outer_lid_guide_001Shape.lsx" "loc_rt_outer_lid_guide_001Shape.lsx"
		;
connectAttr "loc_lf_outer_lid_guide_001Shape.lsy" "loc_rt_outer_lid_guide_001Shape.lsy"
		;
connectAttr "loc_lf_outer_lid_guide_001Shape.lsz" "loc_rt_outer_lid_guide_001Shape.lsz"
		;
connectAttr "loc_lf_upper_lid_guide_001.tx" "loc_rt_upper_lid_guide_001.tx";
connectAttr "loc_lf_upper_lid_guide_001.ty" "loc_rt_upper_lid_guide_001.ty";
connectAttr "loc_lf_upper_lid_guide_001.tz" "loc_rt_upper_lid_guide_001.tz";
connectAttr "loc_lf_upper_lid_guide_001.rx" "loc_rt_upper_lid_guide_001.rx";
connectAttr "loc_lf_upper_lid_guide_001.ry" "loc_rt_upper_lid_guide_001.ry";
connectAttr "loc_lf_upper_lid_guide_001.rz" "loc_rt_upper_lid_guide_001.rz";
connectAttr "loc_lf_upper_lid_guide_001.sx" "loc_rt_upper_lid_guide_001.sx";
connectAttr "loc_lf_upper_lid_guide_001.sy" "loc_rt_upper_lid_guide_001.sy";
connectAttr "loc_lf_upper_lid_guide_001.sz" "loc_rt_upper_lid_guide_001.sz";
connectAttr "loc_lf_upper_lid_guide_001.ro" "loc_rt_upper_lid_guide_001.ro";
connectAttr "loc_lf_upper_lid_guide_001.v" "loc_rt_upper_lid_guide_001.v";
connectAttr "loc_lf_upper_lid_guide_001Shape.lpx" "loc_rt_upper_lid_guide_001Shape.lpx"
		;
connectAttr "loc_lf_upper_lid_guide_001Shape.lpy" "loc_rt_upper_lid_guide_001Shape.lpy"
		;
connectAttr "loc_lf_upper_lid_guide_001Shape.lpz" "loc_rt_upper_lid_guide_001Shape.lpz"
		;
connectAttr "loc_lf_upper_lid_guide_001Shape.lsx" "loc_rt_upper_lid_guide_001Shape.lsx"
		;
connectAttr "loc_lf_upper_lid_guide_001Shape.lsy" "loc_rt_upper_lid_guide_001Shape.lsy"
		;
connectAttr "loc_lf_upper_lid_guide_001Shape.lsz" "loc_rt_upper_lid_guide_001Shape.lsz"
		;
connectAttr "loc_lf_upper_lid_guide_002.tx" "loc_rt_upper_lid_guide_002.tx";
connectAttr "loc_lf_upper_lid_guide_002.ty" "loc_rt_upper_lid_guide_002.ty";
connectAttr "loc_lf_upper_lid_guide_002.tz" "loc_rt_upper_lid_guide_002.tz";
connectAttr "loc_lf_upper_lid_guide_002.rx" "loc_rt_upper_lid_guide_002.rx";
connectAttr "loc_lf_upper_lid_guide_002.ry" "loc_rt_upper_lid_guide_002.ry";
connectAttr "loc_lf_upper_lid_guide_002.rz" "loc_rt_upper_lid_guide_002.rz";
connectAttr "loc_lf_upper_lid_guide_002.sx" "loc_rt_upper_lid_guide_002.sx";
connectAttr "loc_lf_upper_lid_guide_002.sy" "loc_rt_upper_lid_guide_002.sy";
connectAttr "loc_lf_upper_lid_guide_002.sz" "loc_rt_upper_lid_guide_002.sz";
connectAttr "loc_lf_upper_lid_guide_002.ro" "loc_rt_upper_lid_guide_002.ro";
connectAttr "loc_lf_upper_lid_guide_002.v" "loc_rt_upper_lid_guide_002.v";
connectAttr "loc_lf_upper_lid_guide_002Shape.lpx" "loc_rt_upper_lid_guide_002Shape.lpx"
		;
connectAttr "loc_lf_upper_lid_guide_002Shape.lpy" "loc_rt_upper_lid_guide_002Shape.lpy"
		;
connectAttr "loc_lf_upper_lid_guide_002Shape.lpz" "loc_rt_upper_lid_guide_002Shape.lpz"
		;
connectAttr "loc_lf_upper_lid_guide_002Shape.lsx" "loc_rt_upper_lid_guide_002Shape.lsx"
		;
connectAttr "loc_lf_upper_lid_guide_002Shape.lsy" "loc_rt_upper_lid_guide_002Shape.lsy"
		;
connectAttr "loc_lf_upper_lid_guide_002Shape.lsz" "loc_rt_upper_lid_guide_002Shape.lsz"
		;
connectAttr "loc_lf_upper_lid_guide_003.tx" "loc_rt_upper_lid_guide_003.tx";
connectAttr "loc_lf_upper_lid_guide_003.ty" "loc_rt_upper_lid_guide_003.ty";
connectAttr "loc_lf_upper_lid_guide_003.tz" "loc_rt_upper_lid_guide_003.tz";
connectAttr "loc_lf_upper_lid_guide_003.rx" "loc_rt_upper_lid_guide_003.rx";
connectAttr "loc_lf_upper_lid_guide_003.ry" "loc_rt_upper_lid_guide_003.ry";
connectAttr "loc_lf_upper_lid_guide_003.rz" "loc_rt_upper_lid_guide_003.rz";
connectAttr "loc_lf_upper_lid_guide_003.sx" "loc_rt_upper_lid_guide_003.sx";
connectAttr "loc_lf_upper_lid_guide_003.sy" "loc_rt_upper_lid_guide_003.sy";
connectAttr "loc_lf_upper_lid_guide_003.sz" "loc_rt_upper_lid_guide_003.sz";
connectAttr "loc_lf_upper_lid_guide_003.ro" "loc_rt_upper_lid_guide_003.ro";
connectAttr "loc_lf_upper_lid_guide_003.v" "loc_rt_upper_lid_guide_003.v";
connectAttr "loc_lf_upper_lid_guide_003Shape.lpx" "loc_rt_upper_lid_guide_003Shape.lpx"
		;
connectAttr "loc_lf_upper_lid_guide_003Shape.lpy" "loc_rt_upper_lid_guide_003Shape.lpy"
		;
connectAttr "loc_lf_upper_lid_guide_003Shape.lpz" "loc_rt_upper_lid_guide_003Shape.lpz"
		;
connectAttr "loc_lf_upper_lid_guide_003Shape.lsx" "loc_rt_upper_lid_guide_003Shape.lsx"
		;
connectAttr "loc_lf_upper_lid_guide_003Shape.lsy" "loc_rt_upper_lid_guide_003Shape.lsy"
		;
connectAttr "loc_lf_upper_lid_guide_003Shape.lsz" "loc_rt_upper_lid_guide_003Shape.lsz"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.tx" "loc_rt_inner_eye_bag_guide_001.tx"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.ty" "loc_rt_inner_eye_bag_guide_001.ty"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.tz" "loc_rt_inner_eye_bag_guide_001.tz"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.rx" "loc_rt_inner_eye_bag_guide_001.rx"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.ry" "loc_rt_inner_eye_bag_guide_001.ry"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.rz" "loc_rt_inner_eye_bag_guide_001.rz"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.sx" "loc_rt_inner_eye_bag_guide_001.sx"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.sy" "loc_rt_inner_eye_bag_guide_001.sy"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.sz" "loc_rt_inner_eye_bag_guide_001.sz"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.ro" "loc_rt_inner_eye_bag_guide_001.ro"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001.v" "loc_rt_inner_eye_bag_guide_001.v"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.lpx" "loc_rt_inner_eye_bag_guide_001Shape.lpx"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.lpy" "loc_rt_inner_eye_bag_guide_001Shape.lpy"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.lpz" "loc_rt_inner_eye_bag_guide_001Shape.lpz"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.lsx" "loc_rt_inner_eye_bag_guide_001Shape.lsx"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.lsy" "loc_rt_inner_eye_bag_guide_001Shape.lsy"
		;
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.lsz" "loc_rt_inner_eye_bag_guide_001Shape.lsz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.tx" "loc_rt_lower_eye_bag_guide_001.tx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.ty" "loc_rt_lower_eye_bag_guide_001.ty"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.tz" "loc_rt_lower_eye_bag_guide_001.tz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.rx" "loc_rt_lower_eye_bag_guide_001.rx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.ry" "loc_rt_lower_eye_bag_guide_001.ry"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.rz" "loc_rt_lower_eye_bag_guide_001.rz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.sx" "loc_rt_lower_eye_bag_guide_001.sx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.sy" "loc_rt_lower_eye_bag_guide_001.sy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.sz" "loc_rt_lower_eye_bag_guide_001.sz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.ro" "loc_rt_lower_eye_bag_guide_001.ro"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001.v" "loc_rt_lower_eye_bag_guide_001.v"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001Shape.lpx" "loc_rt_lower_eye_bag_guide_001Shape.lpx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001Shape.lpy" "loc_rt_lower_eye_bag_guide_001Shape.lpy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001Shape.lpz" "loc_rt_lower_eye_bag_guide_001Shape.lpz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001Shape.lsx" "loc_rt_lower_eye_bag_guide_001Shape.lsx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001Shape.lsy" "loc_rt_lower_eye_bag_guide_001Shape.lsy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_001Shape.lsz" "loc_rt_lower_eye_bag_guide_001Shape.lsz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.tx" "loc_rt_lower_eye_bag_guide_002.tx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.ty" "loc_rt_lower_eye_bag_guide_002.ty"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.tz" "loc_rt_lower_eye_bag_guide_002.tz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.rx" "loc_rt_lower_eye_bag_guide_002.rx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.ry" "loc_rt_lower_eye_bag_guide_002.ry"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.rz" "loc_rt_lower_eye_bag_guide_002.rz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.sx" "loc_rt_lower_eye_bag_guide_002.sx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.sy" "loc_rt_lower_eye_bag_guide_002.sy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.sz" "loc_rt_lower_eye_bag_guide_002.sz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.ro" "loc_rt_lower_eye_bag_guide_002.ro"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002.v" "loc_rt_lower_eye_bag_guide_002.v"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002Shape.lpx" "loc_rt_lower_eye_bag_guide_002Shape.lpx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002Shape.lpy" "loc_rt_lower_eye_bag_guide_002Shape.lpy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002Shape.lpz" "loc_rt_lower_eye_bag_guide_002Shape.lpz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002Shape.lsx" "loc_rt_lower_eye_bag_guide_002Shape.lsx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002Shape.lsy" "loc_rt_lower_eye_bag_guide_002Shape.lsy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_002Shape.lsz" "loc_rt_lower_eye_bag_guide_002Shape.lsz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.tx" "loc_rt_lower_eye_bag_guide_003.tx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.ty" "loc_rt_lower_eye_bag_guide_003.ty"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.tz" "loc_rt_lower_eye_bag_guide_003.tz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.rx" "loc_rt_lower_eye_bag_guide_003.rx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.ry" "loc_rt_lower_eye_bag_guide_003.ry"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.rz" "loc_rt_lower_eye_bag_guide_003.rz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.sx" "loc_rt_lower_eye_bag_guide_003.sx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.sy" "loc_rt_lower_eye_bag_guide_003.sy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.sz" "loc_rt_lower_eye_bag_guide_003.sz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.ro" "loc_rt_lower_eye_bag_guide_003.ro"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003.v" "loc_rt_lower_eye_bag_guide_003.v"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003Shape.lpx" "loc_rt_lower_eye_bag_guide_003Shape.lpx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003Shape.lpy" "loc_rt_lower_eye_bag_guide_003Shape.lpy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003Shape.lpz" "loc_rt_lower_eye_bag_guide_003Shape.lpz"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003Shape.lsx" "loc_rt_lower_eye_bag_guide_003Shape.lsx"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003Shape.lsy" "loc_rt_lower_eye_bag_guide_003Shape.lsy"
		;
connectAttr "loc_lf_lower_eye_bag_guide_003Shape.lsz" "loc_rt_lower_eye_bag_guide_003Shape.lsz"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.tx" "loc_rt_outer_eye_bag_guide_001.tx"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.ty" "loc_rt_outer_eye_bag_guide_001.ty"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.tz" "loc_rt_outer_eye_bag_guide_001.tz"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.rx" "loc_rt_outer_eye_bag_guide_001.rx"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.ry" "loc_rt_outer_eye_bag_guide_001.ry"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.rz" "loc_rt_outer_eye_bag_guide_001.rz"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.sx" "loc_rt_outer_eye_bag_guide_001.sx"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.sy" "loc_rt_outer_eye_bag_guide_001.sy"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.sz" "loc_rt_outer_eye_bag_guide_001.sz"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.ro" "loc_rt_outer_eye_bag_guide_001.ro"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001.v" "loc_rt_outer_eye_bag_guide_001.v"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.lpx" "loc_rt_outer_eye_bag_guide_001Shape.lpx"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.lpy" "loc_rt_outer_eye_bag_guide_001Shape.lpy"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.lpz" "loc_rt_outer_eye_bag_guide_001Shape.lpz"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.lsx" "loc_rt_outer_eye_bag_guide_001Shape.lsx"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.lsy" "loc_rt_outer_eye_bag_guide_001Shape.lsy"
		;
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.lsz" "loc_rt_outer_eye_bag_guide_001Shape.lsz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.tx" "loc_rt_upper_eye_bag_guide_001.tx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.ty" "loc_rt_upper_eye_bag_guide_001.ty"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.tz" "loc_rt_upper_eye_bag_guide_001.tz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.rx" "loc_rt_upper_eye_bag_guide_001.rx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.ry" "loc_rt_upper_eye_bag_guide_001.ry"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.rz" "loc_rt_upper_eye_bag_guide_001.rz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.sx" "loc_rt_upper_eye_bag_guide_001.sx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.sy" "loc_rt_upper_eye_bag_guide_001.sy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.sz" "loc_rt_upper_eye_bag_guide_001.sz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.ro" "loc_rt_upper_eye_bag_guide_001.ro"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001.v" "loc_rt_upper_eye_bag_guide_001.v"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001Shape.lpx" "loc_rt_upper_eye_bag_guide_001Shape.lpx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001Shape.lpy" "loc_rt_upper_eye_bag_guide_001Shape.lpy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001Shape.lpz" "loc_rt_upper_eye_bag_guide_001Shape.lpz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001Shape.lsx" "loc_rt_upper_eye_bag_guide_001Shape.lsx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001Shape.lsy" "loc_rt_upper_eye_bag_guide_001Shape.lsy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_001Shape.lsz" "loc_rt_upper_eye_bag_guide_001Shape.lsz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.tx" "loc_rt_upper_eye_bag_guide_002.tx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.ty" "loc_rt_upper_eye_bag_guide_002.ty"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.tz" "loc_rt_upper_eye_bag_guide_002.tz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.rx" "loc_rt_upper_eye_bag_guide_002.rx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.ry" "loc_rt_upper_eye_bag_guide_002.ry"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.rz" "loc_rt_upper_eye_bag_guide_002.rz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.sx" "loc_rt_upper_eye_bag_guide_002.sx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.sy" "loc_rt_upper_eye_bag_guide_002.sy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.sz" "loc_rt_upper_eye_bag_guide_002.sz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.ro" "loc_rt_upper_eye_bag_guide_002.ro"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002.v" "loc_rt_upper_eye_bag_guide_002.v"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002Shape.lpx" "loc_rt_upper_eye_bag_guide_002Shape.lpx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002Shape.lpy" "loc_rt_upper_eye_bag_guide_002Shape.lpy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002Shape.lpz" "loc_rt_upper_eye_bag_guide_002Shape.lpz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002Shape.lsx" "loc_rt_upper_eye_bag_guide_002Shape.lsx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002Shape.lsy" "loc_rt_upper_eye_bag_guide_002Shape.lsy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_002Shape.lsz" "loc_rt_upper_eye_bag_guide_002Shape.lsz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.tx" "loc_rt_upper_eye_bag_guide_003.tx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.ty" "loc_rt_upper_eye_bag_guide_003.ty"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.tz" "loc_rt_upper_eye_bag_guide_003.tz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.rx" "loc_rt_upper_eye_bag_guide_003.rx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.ry" "loc_rt_upper_eye_bag_guide_003.ry"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.rz" "loc_rt_upper_eye_bag_guide_003.rz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.sx" "loc_rt_upper_eye_bag_guide_003.sx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.sy" "loc_rt_upper_eye_bag_guide_003.sy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.sz" "loc_rt_upper_eye_bag_guide_003.sz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.ro" "loc_rt_upper_eye_bag_guide_003.ro"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003.v" "loc_rt_upper_eye_bag_guide_003.v"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003Shape.lpx" "loc_rt_upper_eye_bag_guide_003Shape.lpx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003Shape.lpy" "loc_rt_upper_eye_bag_guide_003Shape.lpy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003Shape.lpz" "loc_rt_upper_eye_bag_guide_003Shape.lpz"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003Shape.lsx" "loc_rt_upper_eye_bag_guide_003Shape.lsx"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003Shape.lsy" "loc_rt_upper_eye_bag_guide_003Shape.lsy"
		;
connectAttr "loc_lf_upper_eye_bag_guide_003Shape.lsz" "loc_rt_upper_eye_bag_guide_003Shape.lsz"
		;
connectAttr "loc_lf_brow_main_guide_001.tx" "loc_rt_brow_main_guide_001.tx";
connectAttr "loc_lf_brow_main_guide_001.ty" "loc_rt_brow_main_guide_001.ty";
connectAttr "loc_lf_brow_main_guide_001.tz" "loc_rt_brow_main_guide_001.tz";
connectAttr "loc_lf_brow_main_guide_001.rx" "loc_rt_brow_main_guide_001.rx";
connectAttr "loc_lf_brow_main_guide_001.ry" "loc_rt_brow_main_guide_001.ry";
connectAttr "loc_lf_brow_main_guide_001.rz" "loc_rt_brow_main_guide_001.rz";
connectAttr "loc_lf_brow_main_guide_001.sx" "loc_rt_brow_main_guide_001.sx";
connectAttr "loc_lf_brow_main_guide_001.sy" "loc_rt_brow_main_guide_001.sy";
connectAttr "loc_lf_brow_main_guide_001.sz" "loc_rt_brow_main_guide_001.sz";
connectAttr "loc_lf_brow_main_guide_001.ro" "loc_rt_brow_main_guide_001.ro";
connectAttr "loc_lf_brow_main_guide_001.v" "loc_rt_brow_main_guide_001.v";
connectAttr "loc_lf_brow_main_guide_001Shape.lpx" "loc_rt_brow_main_guide_001Shape.lpx"
		;
connectAttr "loc_lf_brow_main_guide_001Shape.lpy" "loc_rt_brow_main_guide_001Shape.lpy"
		;
connectAttr "loc_lf_brow_main_guide_001Shape.lpz" "loc_rt_brow_main_guide_001Shape.lpz"
		;
connectAttr "loc_lf_brow_main_guide_001Shape.lsx" "loc_rt_brow_main_guide_001Shape.lsx"
		;
connectAttr "loc_lf_brow_main_guide_001Shape.lsy" "loc_rt_brow_main_guide_001Shape.lsy"
		;
connectAttr "loc_lf_brow_main_guide_001Shape.lsz" "loc_rt_brow_main_guide_001Shape.lsz"
		;
connectAttr "loc_lf_brow_guide_001.tx" "loc_rt_brow_guide_001.tx";
connectAttr "loc_lf_brow_guide_001.ty" "loc_rt_brow_guide_001.ty";
connectAttr "loc_lf_brow_guide_001.tz" "loc_rt_brow_guide_001.tz";
connectAttr "loc_lf_brow_guide_001.rx" "loc_rt_brow_guide_001.rx";
connectAttr "loc_lf_brow_guide_001.ry" "loc_rt_brow_guide_001.ry";
connectAttr "loc_lf_brow_guide_001.rz" "loc_rt_brow_guide_001.rz";
connectAttr "loc_lf_brow_guide_001.sx" "loc_rt_brow_guide_001.sx";
connectAttr "loc_lf_brow_guide_001.sy" "loc_rt_brow_guide_001.sy";
connectAttr "loc_lf_brow_guide_001.sz" "loc_rt_brow_guide_001.sz";
connectAttr "loc_lf_brow_guide_001.ro" "loc_rt_brow_guide_001.ro";
connectAttr "loc_lf_brow_guide_001.v" "loc_rt_brow_guide_001.v";
connectAttr "loc_lf_brow_guide_001Shape.lpx" "loc_rt_brow_guide_001Shape.lpx";
connectAttr "loc_lf_brow_guide_001Shape.lpy" "loc_rt_brow_guide_001Shape.lpy";
connectAttr "loc_lf_brow_guide_001Shape.lpz" "loc_rt_brow_guide_001Shape.lpz";
connectAttr "loc_lf_brow_guide_001Shape.lsx" "loc_rt_brow_guide_001Shape.lsx";
connectAttr "loc_lf_brow_guide_001Shape.lsy" "loc_rt_brow_guide_001Shape.lsy";
connectAttr "loc_lf_brow_guide_001Shape.lsz" "loc_rt_brow_guide_001Shape.lsz";
connectAttr "loc_lf_brow_guide_002.tx" "loc_rt_brow_guide_002.tx";
connectAttr "loc_lf_brow_guide_002.ty" "loc_rt_brow_guide_002.ty";
connectAttr "loc_lf_brow_guide_002.tz" "loc_rt_brow_guide_002.tz";
connectAttr "loc_lf_brow_guide_002.rx" "loc_rt_brow_guide_002.rx";
connectAttr "loc_lf_brow_guide_002.ry" "loc_rt_brow_guide_002.ry";
connectAttr "loc_lf_brow_guide_002.rz" "loc_rt_brow_guide_002.rz";
connectAttr "loc_lf_brow_guide_002.sx" "loc_rt_brow_guide_002.sx";
connectAttr "loc_lf_brow_guide_002.sy" "loc_rt_brow_guide_002.sy";
connectAttr "loc_lf_brow_guide_002.sz" "loc_rt_brow_guide_002.sz";
connectAttr "loc_lf_brow_guide_002.ro" "loc_rt_brow_guide_002.ro";
connectAttr "loc_lf_brow_guide_002.v" "loc_rt_brow_guide_002.v";
connectAttr "loc_lf_brow_guide_002Shape.lpx" "loc_rt_brow_guide_002Shape.lpx";
connectAttr "loc_lf_brow_guide_002Shape.lpy" "loc_rt_brow_guide_002Shape.lpy";
connectAttr "loc_lf_brow_guide_002Shape.lpz" "loc_rt_brow_guide_002Shape.lpz";
connectAttr "loc_lf_brow_guide_002Shape.lsx" "loc_rt_brow_guide_002Shape.lsx";
connectAttr "loc_lf_brow_guide_002Shape.lsy" "loc_rt_brow_guide_002Shape.lsy";
connectAttr "loc_lf_brow_guide_002Shape.lsz" "loc_rt_brow_guide_002Shape.lsz";
connectAttr "loc_lf_brow_guide_003.tx" "loc_rt_brow_guide_003.tx";
connectAttr "loc_lf_brow_guide_003.ty" "loc_rt_brow_guide_003.ty";
connectAttr "loc_lf_brow_guide_003.tz" "loc_rt_brow_guide_003.tz";
connectAttr "loc_lf_brow_guide_003.rx" "loc_rt_brow_guide_003.rx";
connectAttr "loc_lf_brow_guide_003.ry" "loc_rt_brow_guide_003.ry";
connectAttr "loc_lf_brow_guide_003.rz" "loc_rt_brow_guide_003.rz";
connectAttr "loc_lf_brow_guide_003.sx" "loc_rt_brow_guide_003.sx";
connectAttr "loc_lf_brow_guide_003.sy" "loc_rt_brow_guide_003.sy";
connectAttr "loc_lf_brow_guide_003.sz" "loc_rt_brow_guide_003.sz";
connectAttr "loc_lf_brow_guide_003.ro" "loc_rt_brow_guide_003.ro";
connectAttr "loc_lf_brow_guide_003.v" "loc_rt_brow_guide_003.v";
connectAttr "loc_lf_brow_guide_003Shape.lpx" "loc_rt_brow_guide_003Shape.lpx";
connectAttr "loc_lf_brow_guide_003Shape.lpy" "loc_rt_brow_guide_003Shape.lpy";
connectAttr "loc_lf_brow_guide_003Shape.lpz" "loc_rt_brow_guide_003Shape.lpz";
connectAttr "loc_lf_brow_guide_003Shape.lsx" "loc_rt_brow_guide_003Shape.lsx";
connectAttr "loc_lf_brow_guide_003Shape.lsy" "loc_rt_brow_guide_003Shape.lsy";
connectAttr "loc_lf_brow_guide_003Shape.lsz" "loc_rt_brow_guide_003Shape.lsz";
connectAttr "loc_lf_brow_guide_004.tx" "loc_rt_brow_guide_004.tx";
connectAttr "loc_lf_brow_guide_004.ty" "loc_rt_brow_guide_004.ty";
connectAttr "loc_lf_brow_guide_004.tz" "loc_rt_brow_guide_004.tz";
connectAttr "loc_lf_brow_guide_004.rx" "loc_rt_brow_guide_004.rx";
connectAttr "loc_lf_brow_guide_004.ry" "loc_rt_brow_guide_004.ry";
connectAttr "loc_lf_brow_guide_004.rz" "loc_rt_brow_guide_004.rz";
connectAttr "loc_lf_brow_guide_004.sx" "loc_rt_brow_guide_004.sx";
connectAttr "loc_lf_brow_guide_004.sy" "loc_rt_brow_guide_004.sy";
connectAttr "loc_lf_brow_guide_004.sz" "loc_rt_brow_guide_004.sz";
connectAttr "loc_lf_brow_guide_004.ro" "loc_rt_brow_guide_004.ro";
connectAttr "loc_lf_brow_guide_004.v" "loc_rt_brow_guide_004.v";
connectAttr "loc_lf_brow_guide_004Shape.lpx" "loc_rt_brow_guide_004Shape.lpx";
connectAttr "loc_lf_brow_guide_004Shape.lpy" "loc_rt_brow_guide_004Shape.lpy";
connectAttr "loc_lf_brow_guide_004Shape.lpz" "loc_rt_brow_guide_004Shape.lpz";
connectAttr "loc_lf_brow_guide_004Shape.lsx" "loc_rt_brow_guide_004Shape.lsx";
connectAttr "loc_lf_brow_guide_004Shape.lsy" "loc_rt_brow_guide_004Shape.lsy";
connectAttr "loc_lf_brow_guide_004Shape.lsz" "loc_rt_brow_guide_004Shape.lsz";
connectAttr "loc_lf_brow_guide_005.tx" "loc_rt_brow_guide_005.tx";
connectAttr "loc_lf_brow_guide_005.ty" "loc_rt_brow_guide_005.ty";
connectAttr "loc_lf_brow_guide_005.tz" "loc_rt_brow_guide_005.tz";
connectAttr "loc_lf_brow_guide_005.rx" "loc_rt_brow_guide_005.rx";
connectAttr "loc_lf_brow_guide_005.ry" "loc_rt_brow_guide_005.ry";
connectAttr "loc_lf_brow_guide_005.rz" "loc_rt_brow_guide_005.rz";
connectAttr "loc_lf_brow_guide_005.sx" "loc_rt_brow_guide_005.sx";
connectAttr "loc_lf_brow_guide_005.sy" "loc_rt_brow_guide_005.sy";
connectAttr "loc_lf_brow_guide_005.sz" "loc_rt_brow_guide_005.sz";
connectAttr "loc_lf_brow_guide_005.ro" "loc_rt_brow_guide_005.ro";
connectAttr "loc_lf_brow_guide_005.v" "loc_rt_brow_guide_005.v";
connectAttr "loc_lf_brow_guide_005Shape.lpx" "loc_rt_brow_guide_005Shape.lpx";
connectAttr "loc_lf_brow_guide_005Shape.lpy" "loc_rt_brow_guide_005Shape.lpy";
connectAttr "loc_lf_brow_guide_005Shape.lpz" "loc_rt_brow_guide_005Shape.lpz";
connectAttr "loc_lf_brow_guide_005Shape.lsx" "loc_rt_brow_guide_005Shape.lsx";
connectAttr "loc_lf_brow_guide_005Shape.lsy" "loc_rt_brow_guide_005Shape.lsy";
connectAttr "loc_lf_brow_guide_005Shape.lsz" "loc_rt_brow_guide_005Shape.lsz";
connectAttr "loc_lf_lower_lip_guide_001.tx" "loc_rt_lower_lip_guide_001.tx";
connectAttr "loc_lf_lower_lip_guide_001.ty" "loc_rt_lower_lip_guide_001.ty";
connectAttr "loc_lf_lower_lip_guide_001.tz" "loc_rt_lower_lip_guide_001.tz";
connectAttr "loc_lf_lower_lip_guide_001.rx" "loc_rt_lower_lip_guide_001.rx";
connectAttr "loc_lf_lower_lip_guide_001.ry" "loc_rt_lower_lip_guide_001.ry";
connectAttr "loc_lf_lower_lip_guide_001.rz" "loc_rt_lower_lip_guide_001.rz";
connectAttr "loc_lf_lower_lip_guide_001.sx" "loc_rt_lower_lip_guide_001.sx";
connectAttr "loc_lf_lower_lip_guide_001.sy" "loc_rt_lower_lip_guide_001.sy";
connectAttr "loc_lf_lower_lip_guide_001.sz" "loc_rt_lower_lip_guide_001.sz";
connectAttr "loc_lf_lower_lip_guide_001.ro" "loc_rt_lower_lip_guide_001.ro";
connectAttr "loc_lf_lower_lip_guide_001.v" "loc_rt_lower_lip_guide_001.v";
connectAttr "loc_lf_lower_lip_guide_001Shape.lpx" "loc_rt_lower_lip_guide_001Shape.lpx"
		;
connectAttr "loc_lf_lower_lip_guide_001Shape.lpy" "loc_rt_lower_lip_guide_001Shape.lpy"
		;
connectAttr "loc_lf_lower_lip_guide_001Shape.lpz" "loc_rt_lower_lip_guide_001Shape.lpz"
		;
connectAttr "loc_lf_lower_lip_guide_001Shape.lsx" "loc_rt_lower_lip_guide_001Shape.lsx"
		;
connectAttr "loc_lf_lower_lip_guide_001Shape.lsy" "loc_rt_lower_lip_guide_001Shape.lsy"
		;
connectAttr "loc_lf_lower_lip_guide_001Shape.lsz" "loc_rt_lower_lip_guide_001Shape.lsz"
		;
connectAttr "loc_lf_lower_lip_guide_002.tx" "loc_rt_lower_lip_guide_002.tx";
connectAttr "loc_lf_lower_lip_guide_002.ty" "loc_rt_lower_lip_guide_002.ty";
connectAttr "loc_lf_lower_lip_guide_002.tz" "loc_rt_lower_lip_guide_002.tz";
connectAttr "loc_lf_lower_lip_guide_002.rx" "loc_rt_lower_lip_guide_002.rx";
connectAttr "loc_lf_lower_lip_guide_002.ry" "loc_rt_lower_lip_guide_002.ry";
connectAttr "loc_lf_lower_lip_guide_002.rz" "loc_rt_lower_lip_guide_002.rz";
connectAttr "loc_lf_lower_lip_guide_002.sx" "loc_rt_lower_lip_guide_002.sx";
connectAttr "loc_lf_lower_lip_guide_002.sy" "loc_rt_lower_lip_guide_002.sy";
connectAttr "loc_lf_lower_lip_guide_002.sz" "loc_rt_lower_lip_guide_002.sz";
connectAttr "loc_lf_lower_lip_guide_002.ro" "loc_rt_lower_lip_guide_002.ro";
connectAttr "loc_lf_lower_lip_guide_002.v" "loc_rt_lower_lip_guide_002.v";
connectAttr "loc_lf_lower_lip_guide_002Shape.lpx" "loc_rt_lower_lip_guide_002Shape.lpx"
		;
connectAttr "loc_lf_lower_lip_guide_002Shape.lpy" "loc_rt_lower_lip_guide_002Shape.lpy"
		;
connectAttr "loc_lf_lower_lip_guide_002Shape.lpz" "loc_rt_lower_lip_guide_002Shape.lpz"
		;
connectAttr "loc_lf_lower_lip_guide_002Shape.lsx" "loc_rt_lower_lip_guide_002Shape.lsx"
		;
connectAttr "loc_lf_lower_lip_guide_002Shape.lsy" "loc_rt_lower_lip_guide_002Shape.lsy"
		;
connectAttr "loc_lf_lower_lip_guide_002Shape.lsz" "loc_rt_lower_lip_guide_002Shape.lsz"
		;
connectAttr "loc_lf_mouth_corner_guide_001.tx" "loc_rt_mouth_corner_guide_001.tx"
		;
connectAttr "loc_lf_mouth_corner_guide_001.ty" "loc_rt_mouth_corner_guide_001.ty"
		;
connectAttr "loc_lf_mouth_corner_guide_001.tz" "loc_rt_mouth_corner_guide_001.tz"
		;
connectAttr "loc_lf_mouth_corner_guide_001.rx" "loc_rt_mouth_corner_guide_001.rx"
		;
connectAttr "loc_lf_mouth_corner_guide_001.ry" "loc_rt_mouth_corner_guide_001.ry"
		;
connectAttr "loc_lf_mouth_corner_guide_001.rz" "loc_rt_mouth_corner_guide_001.rz"
		;
connectAttr "loc_lf_mouth_corner_guide_001.sx" "loc_rt_mouth_corner_guide_001.sx"
		;
connectAttr "loc_lf_mouth_corner_guide_001.sy" "loc_rt_mouth_corner_guide_001.sy"
		;
connectAttr "loc_lf_mouth_corner_guide_001.sz" "loc_rt_mouth_corner_guide_001.sz"
		;
connectAttr "loc_lf_mouth_corner_guide_001.ro" "loc_rt_mouth_corner_guide_001.ro"
		;
connectAttr "loc_lf_mouth_corner_guide_001.v" "loc_rt_mouth_corner_guide_001.v";
connectAttr "loc_lf_mouth_corner_guide_001Shape.lpx" "loc_rt_mouth_corner_guide_001Shape.lpx"
		;
connectAttr "loc_lf_mouth_corner_guide_001Shape.lpy" "loc_rt_mouth_corner_guide_001Shape.lpy"
		;
connectAttr "loc_lf_mouth_corner_guide_001Shape.lpz" "loc_rt_mouth_corner_guide_001Shape.lpz"
		;
connectAttr "loc_lf_mouth_corner_guide_001Shape.lsx" "loc_rt_mouth_corner_guide_001Shape.lsx"
		;
connectAttr "loc_lf_mouth_corner_guide_001Shape.lsy" "loc_rt_mouth_corner_guide_001Shape.lsy"
		;
connectAttr "loc_lf_mouth_corner_guide_001Shape.lsz" "loc_rt_mouth_corner_guide_001Shape.lsz"
		;
connectAttr "loc_lf_upper_lip_guide_001.tx" "loc_rt_upper_lip_guide_001.tx";
connectAttr "loc_lf_upper_lip_guide_001.ty" "loc_rt_upper_lip_guide_001.ty";
connectAttr "loc_lf_upper_lip_guide_001.tz" "loc_rt_upper_lip_guide_001.tz";
connectAttr "loc_lf_upper_lip_guide_001.rx" "loc_rt_upper_lip_guide_001.rx";
connectAttr "loc_lf_upper_lip_guide_001.ry" "loc_rt_upper_lip_guide_001.ry";
connectAttr "loc_lf_upper_lip_guide_001.rz" "loc_rt_upper_lip_guide_001.rz";
connectAttr "loc_lf_upper_lip_guide_001.sx" "loc_rt_upper_lip_guide_001.sx";
connectAttr "loc_lf_upper_lip_guide_001.sy" "loc_rt_upper_lip_guide_001.sy";
connectAttr "loc_lf_upper_lip_guide_001.sz" "loc_rt_upper_lip_guide_001.sz";
connectAttr "loc_lf_upper_lip_guide_001.ro" "loc_rt_upper_lip_guide_001.ro";
connectAttr "loc_lf_upper_lip_guide_001.v" "loc_rt_upper_lip_guide_001.v";
connectAttr "loc_lf_upper_lip_guide_001Shape.lpx" "loc_rt_upper_lip_guide_001Shape.lpx"
		;
connectAttr "loc_lf_upper_lip_guide_001Shape.lpy" "loc_rt_upper_lip_guide_001Shape.lpy"
		;
connectAttr "loc_lf_upper_lip_guide_001Shape.lpz" "loc_rt_upper_lip_guide_001Shape.lpz"
		;
connectAttr "loc_lf_upper_lip_guide_001Shape.lsx" "loc_rt_upper_lip_guide_001Shape.lsx"
		;
connectAttr "loc_lf_upper_lip_guide_001Shape.lsy" "loc_rt_upper_lip_guide_001Shape.lsy"
		;
connectAttr "loc_lf_upper_lip_guide_001Shape.lsz" "loc_rt_upper_lip_guide_001Shape.lsz"
		;
connectAttr "loc_lf_upper_lip_guide_002.tx" "loc_rt_upper_lip_guide_002.tx";
connectAttr "loc_lf_upper_lip_guide_002.ty" "loc_rt_upper_lip_guide_002.ty";
connectAttr "loc_lf_upper_lip_guide_002.tz" "loc_rt_upper_lip_guide_002.tz";
connectAttr "loc_lf_upper_lip_guide_002.rx" "loc_rt_upper_lip_guide_002.rx";
connectAttr "loc_lf_upper_lip_guide_002.ry" "loc_rt_upper_lip_guide_002.ry";
connectAttr "loc_lf_upper_lip_guide_002.rz" "loc_rt_upper_lip_guide_002.rz";
connectAttr "loc_lf_upper_lip_guide_002.sx" "loc_rt_upper_lip_guide_002.sx";
connectAttr "loc_lf_upper_lip_guide_002.sy" "loc_rt_upper_lip_guide_002.sy";
connectAttr "loc_lf_upper_lip_guide_002.sz" "loc_rt_upper_lip_guide_002.sz";
connectAttr "loc_lf_upper_lip_guide_002.ro" "loc_rt_upper_lip_guide_002.ro";
connectAttr "loc_lf_upper_lip_guide_002.v" "loc_rt_upper_lip_guide_002.v";
connectAttr "loc_lf_upper_lip_guide_002Shape.lpx" "loc_rt_upper_lip_guide_002Shape.lpx"
		;
connectAttr "loc_lf_upper_lip_guide_002Shape.lpy" "loc_rt_upper_lip_guide_002Shape.lpy"
		;
connectAttr "loc_lf_upper_lip_guide_002Shape.lpz" "loc_rt_upper_lip_guide_002Shape.lpz"
		;
connectAttr "loc_lf_upper_lip_guide_002Shape.lsx" "loc_rt_upper_lip_guide_002Shape.lsx"
		;
connectAttr "loc_lf_upper_lip_guide_002Shape.lsy" "loc_rt_upper_lip_guide_002Shape.lsy"
		;
connectAttr "loc_lf_upper_lip_guide_002Shape.lsz" "loc_rt_upper_lip_guide_002Shape.lsz"
		;
connectAttr "loc_lf_zygoma_guide_001.tx" "loc_rt_zygoma_guide_001.tx";
connectAttr "loc_lf_zygoma_guide_001.ty" "loc_rt_zygoma_guide_001.ty";
connectAttr "loc_lf_zygoma_guide_001.tz" "loc_rt_zygoma_guide_001.tz";
connectAttr "loc_lf_zygoma_guide_001.rx" "loc_rt_zygoma_guide_001.rx";
connectAttr "loc_lf_zygoma_guide_001.ry" "loc_rt_zygoma_guide_001.ry";
connectAttr "loc_lf_zygoma_guide_001.rz" "loc_rt_zygoma_guide_001.rz";
connectAttr "loc_lf_zygoma_guide_001.sx" "loc_rt_zygoma_guide_001.sx";
connectAttr "loc_lf_zygoma_guide_001.sy" "loc_rt_zygoma_guide_001.sy";
connectAttr "loc_lf_zygoma_guide_001.sz" "loc_rt_zygoma_guide_001.sz";
connectAttr "loc_lf_zygoma_guide_001.ro" "loc_rt_zygoma_guide_001.ro";
connectAttr "loc_lf_zygoma_guide_001.v" "loc_rt_zygoma_guide_001.v";
connectAttr "loc_lf_zygoma_guide_001Shape.lpx" "loc_rt_zygoma_guide_001Shape.lpx"
		;
connectAttr "loc_lf_zygoma_guide_001Shape.lpy" "loc_rt_zygoma_guide_001Shape.lpy"
		;
connectAttr "loc_lf_zygoma_guide_001Shape.lpz" "loc_rt_zygoma_guide_001Shape.lpz"
		;
connectAttr "loc_lf_zygoma_guide_001Shape.lsx" "loc_rt_zygoma_guide_001Shape.lsx"
		;
connectAttr "loc_lf_zygoma_guide_001Shape.lsy" "loc_rt_zygoma_guide_001Shape.lsy"
		;
connectAttr "loc_lf_zygoma_guide_001Shape.lsz" "loc_rt_zygoma_guide_001Shape.lsz"
		;
connectAttr "loc_lf_zygoma_guide_002.tx" "loc_rt_zygoma_guide_002.tx";
connectAttr "loc_lf_zygoma_guide_002.ty" "loc_rt_zygoma_guide_002.ty";
connectAttr "loc_lf_zygoma_guide_002.tz" "loc_rt_zygoma_guide_002.tz";
connectAttr "loc_lf_zygoma_guide_002.rx" "loc_rt_zygoma_guide_002.rx";
connectAttr "loc_lf_zygoma_guide_002.ry" "loc_rt_zygoma_guide_002.ry";
connectAttr "loc_lf_zygoma_guide_002.rz" "loc_rt_zygoma_guide_002.rz";
connectAttr "loc_lf_zygoma_guide_002.sx" "loc_rt_zygoma_guide_002.sx";
connectAttr "loc_lf_zygoma_guide_002.sy" "loc_rt_zygoma_guide_002.sy";
connectAttr "loc_lf_zygoma_guide_002.sz" "loc_rt_zygoma_guide_002.sz";
connectAttr "loc_lf_zygoma_guide_002.ro" "loc_rt_zygoma_guide_002.ro";
connectAttr "loc_lf_zygoma_guide_002.v" "loc_rt_zygoma_guide_002.v";
connectAttr "loc_lf_zygoma_guide_002Shape.lpx" "loc_rt_zygoma_guide_002Shape.lpx"
		;
connectAttr "loc_lf_zygoma_guide_002Shape.lpy" "loc_rt_zygoma_guide_002Shape.lpy"
		;
connectAttr "loc_lf_zygoma_guide_002Shape.lpz" "loc_rt_zygoma_guide_002Shape.lpz"
		;
connectAttr "loc_lf_zygoma_guide_002Shape.lsx" "loc_rt_zygoma_guide_002Shape.lsx"
		;
connectAttr "loc_lf_zygoma_guide_002Shape.lsy" "loc_rt_zygoma_guide_002Shape.lsy"
		;
connectAttr "loc_lf_zygoma_guide_002Shape.lsz" "loc_rt_zygoma_guide_002Shape.lsz"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":defaultArnoldDisplayDriver.msg" ":defaultArnoldRenderOptions.drivers"
		 -na;
connectAttr ":defaultArnoldFilter.msg" ":defaultArnoldRenderOptions.filt";
connectAttr ":defaultArnoldDriver.msg" ":defaultArnoldRenderOptions.drvr";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of face_guide.ma
