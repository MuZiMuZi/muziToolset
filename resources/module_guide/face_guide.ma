//Maya ASCII 2023 scene
//Name: face_guide.ma
//Last modified: Wed, Sep 09, 2026 03:23:53 PM
//Codeset: 936
requires maya "2023";
requires "stereoCamera" "10.0";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "5.2.1.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2023";
fileInfo "version" "2023";
fileInfo "cutIdentifier" "202211021031-847a9f9623";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "ABF1CCD3-4854-90E2-7DAB-5D9A032274B8";
createNode transform -s -n "persp";
	rename -uid "98B40841-481F-949E-E53E-1CA9088A7CA2";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 177.16092533278666 945.32492927282567 130.72980464159102 ;
	setAttr ".r" -type "double3" -8.7383527295913712 82.600000000000406 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "CE6CC8EC-4379-CC42-7849-42B5E94EEDD2";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 164.2256631324924;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 25.726365089416504 928.99777221679699 59.792667388916016 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "CBDB9127-4C25-E47F-F3BF-AAA10B5A0987";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "0E49F92F-4A2C-0FE4-61B3-F9AFEAFC2B4A";
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
	rename -uid "E7D99E30-438A-25CE-D3AD-5C8C7D604FBF";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "B0EE0201-4D2C-8F1A-EE54-9F86FC79EC4E";
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
	rename -uid "3E8171D8-41DA-7B06-28A8-6DB7F789A51A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "3CC3BF1A-465E-7ED5-6DFE-63A212776D9A";
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
createNode transform -n "grp_md_face_guide_001";
	rename -uid "36B7E74C-4AF6-0E16-96A5-8B89CA5B9E91";
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
	rename -uid "E3C5E3AA-45EC-E14C-B9EC-EAAC4B7490EB";
	setAttr ".t" -type "double3" 0 377.90694843005963 -26.101674136922082 ;
	setAttr ".rp" -type "double3" 4.8249478340148908 155.65348362177491 28.47299763228412 ;
	setAttr ".sp" -type "double3" 4.8249478340148908 155.65348362177491 28.47299763228412 ;
createNode nurbsCurve -n "ctrl_md_face_move_001Shape" -p "ctrl_md_face_move_001";
	rename -uid "59CAB24A-49B4-250A-56EF-B9B0DC6997CA";
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
	rename -uid "E4A2102D-4EFF-1805-A820-D38FF2A646D5";
	setAttr ".t" -type "double3" -1.7763568394002505e-15 -4.5093141948105995 -44.118020044792218 ;
	setAttr ".rp" -type "double3" 4.824947834014889 160.16279781658545 72.591017677076337 ;
	setAttr ".sp" -type "double3" 4.8249478340148908 160.16279781658545 72.591017677076337 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "zero_lf_ear_guide_001" -p "grp_md_ear_guide_001";
	rename -uid "BB49D242-4C8C-C73C-6D43-B48A14450B91";
	setAttr ".rp" -type "double3" 57.396249988682236 145.50662663491426 89.584364431345577 ;
	setAttr ".sp" -type "double3" 57.396249988682236 145.50662663491426 89.584364431345577 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_lf_ear_guide_001" -p "zero_lf_ear_guide_001";
	rename -uid "40ED29BB-4B6A-335F-81A6-4BB525D1E635";
	setAttr ".t" -type "double3" 45.944458946915773 -17.392176016747726 84.515780835539815 ;
	setAttr ".r" -type "double3" 14.402794894414733 -20.517611544491459 8.4899510036892873e-16 ;
	setAttr ".rp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".sp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_lf_ear_guide_001Shape" -p "loc_lf_ear_guide_001";
	rename -uid "8A9519BB-46E2-1991-152A-57A7B65D43D2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr ".lp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_ear_guide_002" -p "loc_lf_ear_guide_001";
	rename -uid "65CC830E-45CC-33BE-A1D9-F2BB29D5F329";
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_lf_ear_guide_002" -p "zero_lf_ear_guide_002";
	rename -uid "3269AFEF-4C80-14C1-4F5D-20B116EFCBDD";
	setAttr ".t" -type "double3" 0 0 -9.3147123328639339 ;
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_lf_ear_guide_002Shape" -p "loc_lf_ear_guide_002";
	rename -uid "A845CA58-444C-9ACD-D54B-528D5DF32F28";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr ".lp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_ear_guide_003" -p "loc_lf_ear_guide_002";
	rename -uid "35825FF9-47DC-BE7C-AE3E-86AC8464C51D";
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_lf_ear_guide_003" -p "zero_lf_ear_guide_003";
	rename -uid "44E911AB-412D-5B40-70B1-C38BB066ACD9";
	setAttr ".t" -type "double3" 0 0 -9.3147123328639339 ;
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_lf_ear_guide_003Shape" -p "loc_lf_ear_guide_003";
	rename -uid "8BFC5C43-40FE-49A3-FC03-F3987E2864AE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr ".lp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_ear_guide_001" -p "grp_md_ear_guide_001";
	rename -uid "DA1EB308-4299-2C80-5A3E-7AB3A3EFE849";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".rp" -type "double3" 58.16942443661172 147.82970928458886 -72.099951861450947 ;
	setAttr ".rpt" -type "double3" -116.33884887322344 0 144.19990372290189 ;
	setAttr ".sp" -type "double3" 58.16942443661172 147.82970928458889 72.099951861450947 ;
	setAttr ".spt" -type "double3" 0 -2.8421709430403995e-14 -144.19990372290189 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_rt_ear_guide_001" -p "zero_rt_ear_guide_001";
	rename -uid "891EFB9A-41D3-F9CE-B95D-46A3963473FA";
	setAttr ".rp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".sp" -type "double3" 7.4274153709411621 161.73292541503906 -2.7666976451873788 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_rt_ear_guide_001Shape" -p "loc_rt_ear_guide_001";
	rename -uid "644F8CC8-4DC0-9920-2ABB-B38992114493";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "zero_rt_ear_guide_002" -p "loc_rt_ear_guide_001";
	rename -uid "D21BBDD3-4ABE-4798-65FF-13A329711B4F";
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_rt_ear_guide_002" -p "zero_rt_ear_guide_002";
	rename -uid "3369C588-49A0-3093-6956-29B8428EE243";
	setAttr ".rp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".sp" -type "double3" 8.5352792739868164 162.33744812011719 -5.2081689834594727 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_rt_ear_guide_002Shape" -p "loc_rt_ear_guide_002";
	rename -uid "5A43E96E-4597-6486-2C6C-1B8FD37069CA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "zero_rt_ear_guide_003" -p "loc_rt_ear_guide_002";
	rename -uid "F525A85C-4A54-0F31-3930-7CB2C8AC7EB0";
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "loc_rt_ear_guide_003" -p "zero_rt_ear_guide_003";
	rename -uid "DCEDE493-4EB8-FBFA-ECE1-56A212CE36E6";
	setAttr ".rp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".sp" -type "double3" 9.6498956680297852 163.15933227539062 -6.6362996101379395 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode locator -n "loc_rt_ear_guide_003Shape" -p "loc_rt_ear_guide_003";
	rename -uid "DE756C1F-4A20-E282-649F-A1AAF8042B02";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 6;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
createNode transform -n "crv_lf_ear_guide_001" -p "grp_md_ear_guide_001";
	rename -uid "906AB99E-4813-E0BC-BF5A-289EA1325589";
	setAttr ".it" no;
createNode nurbsCurve -n "curveShape1" -p "crv_lf_ear_guide_001";
	rename -uid "E5B8A82D-4898-81D1-DFF4-54A0948749D6";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 2 0 no 3
		3 0 1 2
		3
		53.371874317856935 913.15734126259781 11.529389008638141
		58.347741515793771 916.66706387958834 1.3941407423945762
		62.966974555366505 920.1352610351928 -7.7688736491648456
		;
createNode transform -n "crv_rt_ear_guide_001" -p "grp_md_ear_guide_001";
	rename -uid "603FE61B-466B-EA70-B24E-9D91B663AD1C";
	setAttr ".it" no;
createNode nurbsCurve -n "curveShape2" -p "crv_rt_ear_guide_001";
	rename -uid "5BC06B78-454A-F451-6864-5D9036EFEFA6";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.15000001 0.40000001 0.94999999 ;
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 2 0 no 3
		3 0 1 2
		3
		-53.371874317856935 913.15734126259781 11.529389008638141
		-58.347741515793771 916.66706387958834 1.3941407423945762
		-62.966974555366505 920.1352610351928 -7.7688736491648456
		;
createNode transform -n "grp_md_nose_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "A8A509AB-4F04-9777-4D67-B1854BA7E5EC";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -4.5093141948105995 -44.11802004479226 ;
	setAttr ".rp" -type "double3" 4.8249478340148917 -217.74415061347423 98.692691813998465 ;
	setAttr ".sp" -type "double3" 4.8249478340148917 -217.74415061347423 98.692691813998465 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "zero_md_muzzle_guide_001" -p "grp_md_nose_guide_001";
	rename -uid "A747ECB3-464A-6B95-DE81-A3AB1E972628";
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
	rename -uid "4D18D812-4537-7197-AD98-47B8B09E9F7B";
	setAttr ".t" -type "double3" 0 -26.271796813103492 70.37691591786735 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" 0 187.48517605910428 62.985395937794308 ;
	setAttr ".sp" -type "double3" 0 187.48517605910428 62.985395937794308 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.72000003 0.72000003 0.72000003 ;
createNode locator -n "loc_md_muzzle_guide_001Shape" -p "loc_md_muzzle_guide_001";
	rename -uid "CE05E7BA-4D15-E59D-0171-218550331353";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 16;
	setAttr ".lp" -type "double3" 0 187.48517605910433 62.985395937794308 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_guide_001" -p "loc_md_muzzle_guide_001";
	rename -uid "CF59807D-49C5-4860-48CC-97B6D7BDBD89";
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
	rename -uid "E52885D0-4EE5-CC30-BF4C-F686FEEA9DD8";
	setAttr ".t" -type "double3" 0 17.785676901527609 61.405784484233024 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" -3.9944532589595495e-16 162.54214477539057 6.2591342926025391 ;
	setAttr ".sp" -type "double3" -3.9944532589595495e-16 162.54214477539057 6.2591342926025391 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_guide_001Shape" -p "loc_md_nose_guide_001";
	rename -uid "1F5A2723-4C19-5818-5249-40B39D7ED531";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".lp" -type "double3" -3.9944532589595495e-16 162.54214477539062 6.2591342926025391 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_center_guide_001" -p "loc_md_nose_guide_001";
	rename -uid "11CBA3F4-4F2A-E355-8D34-388B6D885361";
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
	rename -uid "6D883B1E-495A-D067-7EB6-B7BEFB74C1D5";
	setAttr ".t" -type "double3" 0 -12.568160097719669 1.2544033208710204 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" 0.0031950360898326115 159.34211938672212 8.1356919210806247 ;
	setAttr ".sp" -type "double3" 0.0031950360898326115 159.34211938672212 8.1356919210806247 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_center_guide_001Shape" -p "loc_md_nose_center_guide_001";
	rename -uid "4B0368C9-4B1C-F6FB-3B1C-A3833FC5E0D3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".lp" -type "double3" 0.0031950360898326115 159.34211938672217 8.1356919210806247 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_front_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "2A8FC1FD-451A-54FD-6874-DEBCD92057F3";
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
	rename -uid "C01EAB6F-4473-C167-6895-2FBBC30FEC1D";
	setAttr ".t" -type "double3" 0 2.3078078170142362 10.126013960805906 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" 0.0019079342662671195 159.58661860922496 9.3060853632271474 ;
	setAttr ".sp" -type "double3" 0.0019079342662671195 159.58661860922496 9.3060853632271474 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_front_guide_001Shape" -p "loc_md_nose_front_guide_001";
	rename -uid "1EAE70B7-4251-54A9-AB32-C8B54B1D4475";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".lp" -type "double3" 0.0019079342662663412 159.58661860922496 9.3060853632271474 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_nose_side_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "8B695B07-4C8C-8780-85AC-09A573A2B4C7";
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
	rename -uid "6CBB9BDB-449A-FB15-EB96-B6A530A86DC8";
	setAttr ".t" -type "double3" 9.1657981872558594 155.86830337936408 7.6563758591335755 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_lf_nose_side_guide_001Shape" -p "loc_lf_nose_side_guide_001";
	rename -uid "FA5914B1-485A-C5F0-4C5D-4EB985E58BE2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_nose_down_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "CC922EAF-4227-3354-456E-FC86A2FFDC99";
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
	rename -uid "4C26B402-447C-04EE-019B-C99BA7F7C0A6";
	setAttr ".t" -type "double3" 0 151.89918716842658 9.768390629641388 ;
	setAttr -l on ".tx";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_md_nose_down_guide_001Shape" -p "loc_md_nose_down_guide_001";
	rename -uid "6DE87144-4265-C43F-6F5B-17ABB95CF9DC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_nose_side_guide_001" -p "loc_md_nose_center_guide_001";
	rename -uid "14B798A8-4F12-299A-A6CE-2D9E66A0401F";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "loc_rt_nose_side_guide_001" -p "zero_rt_nose_side_guide_001";
	rename -uid "CDF58CBC-4E14-72ED-E81A-C4802426B7BD";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode locator -n "loc_rt_nose_side_guide_001Shape" -p "loc_rt_nose_side_guide_001";
	rename -uid "EF85F99D-4F94-3FB8-9F7D-C4896B29F1CD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 14;
	setAttr ".ovrgb" -type "float3" 0.18000001 0.88 0.31999999 ;
createNode transform -n "crv_md_nose_guide_001" -p "grp_md_nose_guide_001";
	rename -uid "F143D057-4FE0-29E1-85C2-D5A138BAFA22";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape21" -p "crv_md_nose_guide_001";
	rename -uid "6101B463-4EE2-3BE5-A566-25B4D1207309";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 7 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 1 2 3 4 5 6
		7
		-8.8817841970012523e-16 930.02997111030732 63.142617673947314
		-1.2876237455960802e-15 922.87261672812122 67.822140512988568
		0.0031950360898317233 907.1044312417331 70.953101462337671
		0.0019079342662654531 909.65673828125011 82.249508865290096
		9.1657981872558594 903.630615234375 70.473785400390625
		-8.8817841970012523e-16 899.6614990234375 72.585800170898438
		-9.1657981872558594 903.630615234375 70.473785400390625
		;
createNode transform -n "grp_md_eye_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "65C72698-4068-1683-1BF4-7BB62E117D61";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -4.5093141948105995 -44.11802004479226 ;
	setAttr ".rp" -type "double3" 4.8249478340148917 160.1627978165854 72.59101767707638 ;
	setAttr ".sp" -type "double3" 4.8249478340148917 160.1627978165854 72.59101767707638 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "grp_md_eye_ball_guide_001" -p "grp_md_eye_guide_001";
	rename -uid "DD77A46C-43F8-ACC3-A17A-279DDB892D78";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "zero_lf_eye_ball_guide_001" -p "grp_md_eye_ball_guide_001";
	rename -uid "157AE381-4A38-A152-3565-6BAFEFA7DDCD";
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
	rename -uid "3BE697E1-4248-733D-861C-B0BB3D044C7D";
	setAttr ".t" -type "double3" 21.69341666251421 -3.0030938441342983 111.2736953193286 ;
	setAttr ".rp" -type "double3" 3.6603161618113518 163.24768972396845 2.9115569144487363 ;
	setAttr ".sp" -type "double3" 3.6603161618113518 163.24768972396845 2.9115569144487363 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_lf_eye_ball_guide_001Shape" -p "loc_lf_eye_ball_guide_001";
	rename -uid "3F79A2CB-417C-E79F-3448-C4A2C1842DCF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
	setAttr ".lp" -type "double3" 3.6603161618113518 163.24768972396851 2.9115569144487363 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_eye_iris_guide_001" -p "loc_lf_eye_ball_guide_001";
	rename -uid "EF4692CA-4A75-6567-ADDA-93A77E0BC142";
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
	rename -uid "FA3B4D53-446C-527F-7DEC-07A491CDF878";
	setAttr ".t" -type "double3" 0.37263267487287433 -0.06343698501569861 13.780650809407236 ;
	setAttr ".rp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".sp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_lf_eye_iris_guide_001Shape" -p "loc_lf_eye_iris_guide_001";
	rename -uid "E643B8DB-4F21-6A29-DF86-38A38D44C455";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
	setAttr ".lp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "loc_lf_eye_aim_guide_001" -p "zero_lf_eye_iris_guide_001";
	rename -uid "759616F9-4F3B-28BE-43C8-7BA58DA11893";
	setAttr ".t" -type "double3" 0.37263267487287433 -0.06343698501569861 100 ;
	setAttr ".rp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".sp" -type "double3" 3.6603157520294198 163.24771118164045 4.9580154418945295 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_lf_eye_aim_guide_001Shape" -p "loc_lf_eye_aim_guide_001";
	rename -uid "6B76100A-460A-EED6-7233-1D9D30899284";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
	setAttr ".lp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_eye_ball_guide_001" -p "grp_md_eye_ball_guide_001";
	rename -uid "C4593F0C-47CD-077E-FD30-218E5FAE531C";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "loc_rt_eye_ball_guide_001" -p "zero_rt_eye_ball_guide_001";
	rename -uid "77307F82-4E05-65D9-3796-308C4DE22FC1";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_rt_eye_ball_guide_001Shape" -p "loc_rt_eye_ball_guide_001";
	rename -uid "31BDAAAF-442F-7AB6-84E4-D789A0D4EF50";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
createNode transform -n "zero_rt_eye_iris_guide_001" -p "loc_rt_eye_ball_guide_001";
	rename -uid "AD3AE5BB-4ADC-08A5-CC42-779271EF9D35";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "loc_rt_eye_iris_guide_001" -p "zero_rt_eye_iris_guide_001";
	rename -uid "2A568DC4-4669-44D3-8DA3-51B19E771E8E";
	setAttr ".rp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".sp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_rt_eye_iris_guide_001Shape" -p "loc_rt_eye_iris_guide_001";
	rename -uid "AEB24B46-47DC-F03B-4389-B1B1DE934230";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
createNode transform -n "loc_rt_eye_aim_guide_001" -p "zero_rt_eye_iris_guide_001";
	rename -uid "7DBEBB2E-4913-FE44-7290-268F8ACACCE0";
	setAttr ".t" -type "double3" 0.37263267487287433 -0.063436985015812297 100 ;
	setAttr ".rp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".sp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode locator -n "loc_rt_eye_aim_guide_001Shape" -p "loc_rt_eye_aim_guide_001";
	rename -uid "3E191FF3-4217-9309-2BDE-4D93B6816744";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 18;
	setAttr ".ovrgb" -type "float3" 0 0.81999999 1 ;
	setAttr ".lp" -type "double3" 3.6603157520294198 163.24771118164051 4.9580154418945295 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "grp_md_eye_lid_guide_001" -p "grp_md_eye_guide_001";
	rename -uid "35FD0AA4-4A69-2B8A-B025-AD9B50569F37";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.81999999 1 ;
createNode transform -n "grp_lf_eye_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "BCF81E73-4719-996E-0A35-B19E04B3E331";
createNode transform -n "zero_lf_upper_lid_guide_001" -p "grp_lf_eye_lid_guide_001";
	rename -uid "EC4EA371-492F-A482-32F4-C49785A569DD";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_upper_lid_guide_001" -p "zero_lf_upper_lid_guide_001";
	rename -uid "2E60769B-4BAA-0741-3473-6C8CC2E1DC44";
	setAttr ".t" -type "double3" 21.070215693261247 932.416259765625 63.126163482666016 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_upper_lid_guide_001Shape" -p "loc_lf_upper_lid_guide_001";
	rename -uid "CF22127C-46DE-F850-26FC-97811737BA6D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_lid_guide_002" -p "grp_lf_eye_lid_guide_001";
	rename -uid "637E1DEC-479B-CBC8-E19A-A2976056448A";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_upper_lid_guide_002" -p "zero_lf_upper_lid_guide_002";
	rename -uid "0B9E4F24-4FDC-132D-BD83-C79CFEB284E8";
	setAttr ".t" -type "double3" 31.373639878217148 935.31620104311492 61.769050598144531 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_upper_lid_guide_002Shape" -p "loc_lf_upper_lid_guide_002";
	rename -uid "E9161DFD-4A01-F6FB-1719-088C668A297B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_lid_guide_003" -p "grp_lf_eye_lid_guide_001";
	rename -uid "2ACF5E91-49B0-9F61-3326-BE94D8745C38";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_upper_lid_guide_003" -p "zero_lf_upper_lid_guide_003";
	rename -uid "F96113D1-419A-AE32-0E7B-6B85531EE5B1";
	setAttr ".t" -type "double3" 39.100810366552118 932.46839565548237 58.748008728027344 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_upper_lid_guide_003Shape" -p "loc_lf_upper_lid_guide_003";
	rename -uid "9C25CDC3-4FD2-7245-9093-20BF4E21ABE3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_inner_lid_guide_001" -p "grp_lf_eye_lid_guide_001";
	rename -uid "8210FCFC-403A-60E2-A78E-9F875A50EEEE";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_inner_lid_guide_001" -p "zero_lf_inner_lid_guide_001";
	rename -uid "6B4F806F-416D-06D8-9CEC-D99B275B618D";
	setAttr ".t" -type "double3" 14.655315399169977 922.99768066406625 58.630111694336179 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_inner_lid_guide_001Shape" -p "loc_lf_inner_lid_guide_001";
	rename -uid "B2BAC533-4939-ED1A-465E-A49123C7BC56";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_outer_lid_guide_001" -p "grp_lf_eye_lid_guide_001";
	rename -uid "05E66C90-4C53-BB35-BCC1-B09A584FA37F";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_outer_lid_guide_001" -p "zero_lf_outer_lid_guide_001";
	rename -uid "F135FE90-4933-8350-839F-39A4E3D7B830";
	setAttr ".t" -type "double3" 42.03558731079108 927.76257324218875 50.447769165039126 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_outer_lid_guide_001Shape" -p "loc_lf_outer_lid_guide_001";
	rename -uid "DD85E025-4555-FD38-513C-C79E18B578F3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_lid_guide_001" -p "grp_lf_eye_lid_guide_001";
	rename -uid "20A6FADC-49F3-6DE8-4C4B-2C8A0EA42B84";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_lower_lid_guide_001" -p "zero_lf_lower_lid_guide_001";
	rename -uid "438D4A6B-4558-A6FD-1F39-A7A143444236";
	setAttr ".t" -type "double3" 21.904081850007824 919.42087542244542 61.780749368238389 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_lower_lid_guide_001Shape" -p "loc_lf_lower_lid_guide_001";
	rename -uid "10E35562-4DD2-1F17-2965-5D8FE37E4CA0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_lid_guide_002" -p "grp_lf_eye_lid_guide_001";
	rename -uid "B102D5EE-484A-A4AE-08E5-B288F42B165E";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_lower_lid_guide_002" -p "zero_lf_lower_lid_guide_002";
	rename -uid "13A5F0F1-48CB-03F3-4895-18ABEE1B9367";
	setAttr ".t" -type "double3" 31.673681259155273 919.26068115234375 60.724639892578125 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_lower_lid_guide_002Shape" -p "loc_lf_lower_lid_guide_002";
	rename -uid "DBF0F2B1-44EC-9F49-3D69-E490D58FE601";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_lid_guide_003" -p "grp_lf_eye_lid_guide_001";
	rename -uid "7C6A2C6B-4D8E-94EB-77CD-A19179433C67";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_lf_lower_lid_guide_003" -p "zero_lf_lower_lid_guide_003";
	rename -uid "264A24FA-41B1-D9F7-1A4A-88A76F4B6439";
	setAttr ".t" -type "double3" 38.504032135009766 921.49102783203125 56.063362121582031 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_lf_lower_lid_guide_003Shape" -p "loc_lf_lower_lid_guide_003";
	rename -uid "39F12909-4E0C-2B99-0840-AA96706BAC16";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "crv_lf_upper_lid_guide_001" -p "grp_lf_eye_lid_guide_001";
	rename -uid "122A924C-499E-0170-255A-47931F11E057";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape12" -p "crv_lf_upper_lid_guide_001";
	rename -uid "576DF349-44AE-69CD-C6D5-27AA1A826B11";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		14.655315399169977 922.99768066406625 58.630111694336179
		21.070215693261247 932.416259765625 63.126163482666016
		31.373639878217148 935.31620104311492 61.769050598144531
		39.100810366552118 932.46839565548237 58.748008728027344
		42.03558731079108 927.76257324218875 50.447769165039126
		;
createNode transform -n "crv_lf_lower_lid_guide_001" -p "grp_lf_eye_lid_guide_001";
	rename -uid "12EA3892-44DC-1DAF-AB5E-9AB5BBAB4582";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape13" -p "crv_lf_lower_lid_guide_001";
	rename -uid "AF25D3F9-4CB0-65C3-B292-4AAFE83A158A";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		14.655315399169977 922.99768066406625 58.630111694336179
		21.904081850007824 919.42087542244542 61.780749368238389
		31.673681259155273 919.26068115234375 60.724639892578125
		38.504032135009766 921.49102783203125 56.063362121582031
		42.03558731079108 927.76257324218875 50.447769165039126
		;
createNode transform -n "grp_rt_eye_lid_guide_001" -p "grp_md_eye_lid_guide_001";
	rename -uid "86DC16F7-4D5C-9B6F-F0E1-47BA6231A663";
createNode transform -n "zero_rt_lower_lid_guide_001" -p "grp_rt_eye_lid_guide_001";
	rename -uid "4914DCB6-4077-2003-450F-1BB84B9CB4ED";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_lower_lid_guide_001" -p "zero_rt_lower_lid_guide_001";
	rename -uid "353DABC3-4A5A-5847-8B38-EAB435E87970";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_lower_lid_guide_001Shape" -p "loc_rt_lower_lid_guide_001";
	rename -uid "324160AC-41F5-D66E-C71E-6D9F87ABE093";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_lower_lid_guide_002" -p "grp_rt_eye_lid_guide_001";
	rename -uid "26CBD590-4E09-A59F-C2C3-65BE5DC32233";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_lower_lid_guide_002" -p "zero_rt_lower_lid_guide_002";
	rename -uid "3AF328BA-4FF3-B838-EAA0-91930BBF2940";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_lower_lid_guide_002Shape" -p "loc_rt_lower_lid_guide_002";
	rename -uid "80499974-4D2B-A079-3828-42A173B950A9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_lower_lid_guide_003" -p "grp_rt_eye_lid_guide_001";
	rename -uid "ECF4A9C3-4CE3-8AC5-07E1-E29A98C57F95";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_lower_lid_guide_003" -p "zero_rt_lower_lid_guide_003";
	rename -uid "AF7CB703-4C07-8983-BB4D-90802B30E0A0";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_lower_lid_guide_003Shape" -p "loc_rt_lower_lid_guide_003";
	rename -uid "04795FF4-49EB-AB42-F6A7-18A8566D80C3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_inner_lid_guide_001" -p "grp_rt_eye_lid_guide_001";
	rename -uid "E23AF993-40D1-CC25-659F-5B8397DA804E";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_inner_lid_guide_001" -p "zero_rt_inner_lid_guide_001";
	rename -uid "4F9A5F90-4B9B-FC9F-2814-66ABDA380A97";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_inner_lid_guide_001Shape" -p "loc_rt_inner_lid_guide_001";
	rename -uid "33AC33E3-4459-1C2A-8B99-BF809F1AF984";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_outer_lid_guide_001" -p "grp_rt_eye_lid_guide_001";
	rename -uid "889F2658-48A7-8DAD-DEA1-6380482B6D67";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_outer_lid_guide_001" -p "zero_rt_outer_lid_guide_001";
	rename -uid "03623BFE-42F4-2E80-698F-08AC62C3B15C";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_outer_lid_guide_001Shape" -p "loc_rt_outer_lid_guide_001";
	rename -uid "85EB2A6F-4313-E23B-5982-F48C9F1629D5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_upper_lid_guide_001" -p "grp_rt_eye_lid_guide_001";
	rename -uid "2CFD5526-467A-0765-F43F-BD86AF3CB741";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_upper_lid_guide_001" -p "zero_rt_upper_lid_guide_001";
	rename -uid "0CE466D9-403D-1985-A7A5-C9804D8F0149";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_upper_lid_guide_001Shape" -p "loc_rt_upper_lid_guide_001";
	rename -uid "ADE8A74D-469E-A7C0-EEAB-9B812992448F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_upper_lid_guide_002" -p "grp_rt_eye_lid_guide_001";
	rename -uid "F483DE00-4B71-A2DC-2BA2-54BBBFE58A78";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_upper_lid_guide_002" -p "zero_rt_upper_lid_guide_002";
	rename -uid "E83B5BDC-4A06-63BC-4B18-B2A00C65A986";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_upper_lid_guide_002Shape" -p "loc_rt_upper_lid_guide_002";
	rename -uid "2029EF6E-4A75-EB41-7797-308DC2D47BD8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "zero_rt_upper_lid_guide_003" -p "grp_rt_eye_lid_guide_001";
	rename -uid "15B71549-484C-B15C-5A5F-95BABA03EB80";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode transform -n "loc_rt_upper_lid_guide_003" -p "zero_rt_upper_lid_guide_003";
	rename -uid "F0A30D04-4347-79B1-6C7F-30A8CE960FAE";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.38 0.28 1 ;
createNode locator -n "loc_rt_upper_lid_guide_003Shape" -p "loc_rt_upper_lid_guide_003";
	rename -uid "35CF61C8-46DF-A043-553B-0CB856B9E6C9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 0.38 0.28 1 ;
createNode transform -n "crv_rt_upper_lid_guide_001" -p "grp_rt_eye_lid_guide_001";
	rename -uid "7A2AA33E-49A8-0F88-1747-F1B7F4F8134B";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape14" -p "crv_rt_upper_lid_guide_001";
	rename -uid "E962C0D5-4E90-16FE-CE7A-7FA12B51C2FD";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-14.655315399169986 922.99768066406625 58.630111694336179
		-21.070215693261254 932.416259765625 63.126163482666016
		-31.373639878217155 935.31620104311492 61.769050598144524
		-39.100810366552125 932.46839565548237 58.748008728027337
		-42.035587310791087 927.76257324218875 50.447769165039119
		;
createNode transform -n "crv_rt_lower_lid_guide_001" -p "grp_rt_eye_lid_guide_001";
	rename -uid "82AABEF6-4B17-4934-A061-A3BC0A7EEB38";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape15" -p "crv_rt_lower_lid_guide_001";
	rename -uid "4E83735B-481C-B01F-00BA-7D941689F3F4";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-14.655315399169986 922.99768066406625 58.630111694336179
		-21.904081850007834 919.42087542244542 61.780749368238389
		-31.673681259155281 919.26068115234375 60.724639892578118
		-38.504032135009773 921.49102783203125 56.063362121582024
		-42.035587310791087 927.76257324218875 50.447769165039119
		;
createNode transform -n "grp_md_eye_bags_guide_001" -p "grp_md_eye_guide_001";
	rename -uid "A5C24A79-483B-13D7-8B54-AA8642B53B65";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "grp_rt_eye_bags_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "91DCD24E-4F32-F020-2DDD-F3A8A6FE1476";
createNode transform -n "zero_rt_upper_eye_bag_guide_001" -p "grp_rt_eye_bags_guide_001";
	rename -uid "64C2B222-49D7-6D8C-2103-708E39263ABC";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_upper_eye_bag_guide_001" -p "zero_rt_upper_eye_bag_guide_001";
	rename -uid "875003A1-4753-8FF2-6CC2-4ABB4C6DF5B2";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_upper_eye_bag_guide_001Shape" -p "loc_rt_upper_eye_bag_guide_001";
	rename -uid "7D58B8B2-4374-C604-78D8-58AAF255651A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_upper_eye_bag_guide_002" -p "grp_rt_eye_bags_guide_001";
	rename -uid "26798234-4483-4C0F-8199-E9ADD8AF1414";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_upper_eye_bag_guide_002" -p "zero_rt_upper_eye_bag_guide_002";
	rename -uid "CE9C9291-4ACF-D192-E294-DDB3BC6248D4";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_upper_eye_bag_guide_002Shape" -p "loc_rt_upper_eye_bag_guide_002";
	rename -uid "CAB75F7C-4D62-1FD7-1230-A295DB5F6B94";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_upper_eye_bag_guide_003" -p "grp_rt_eye_bags_guide_001";
	rename -uid "28355198-4A94-A2DF-2759-908D03B19217";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_upper_eye_bag_guide_003" -p "zero_rt_upper_eye_bag_guide_003";
	rename -uid "238ABE88-4FC7-D8E1-926F-9CA1D97F8D50";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_upper_eye_bag_guide_003Shape" -p "loc_rt_upper_eye_bag_guide_003";
	rename -uid "354F4F70-4485-3B73-5FC6-E8A29FB12885";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_inner_eye_bag_guide_001" -p "grp_rt_eye_bags_guide_001";
	rename -uid "D659F3D3-48E5-B510-08E6-078FA3772A2D";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_inner_eye_bag_guide_001" -p "zero_rt_inner_eye_bag_guide_001";
	rename -uid "B1D1D8FD-4D85-6735-215C-F6917443BEEB";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_inner_eye_bag_guide_001Shape" -p "loc_rt_inner_eye_bag_guide_001";
	rename -uid "76A06070-4468-B81B-249B-6E8764B48CB5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_outer_eye_bag_guide_001" -p "grp_rt_eye_bags_guide_001";
	rename -uid "D6418B48-450C-E44D-3BA1-BFBD764E7E97";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_outer_eye_bag_guide_001" -p "zero_rt_outer_eye_bag_guide_001";
	rename -uid "11F35D61-428C-2B11-B464-08BDFF2E0D4A";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_outer_eye_bag_guide_001Shape" -p "loc_rt_outer_eye_bag_guide_001";
	rename -uid "9D31FB4C-460A-A7D4-9456-D08ABFFD58CF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_lower_eye_bag_guide_003" -p "grp_rt_eye_bags_guide_001";
	rename -uid "F8014027-46AF-70C7-2E8E-069B4FAC0161";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_lower_eye_bag_guide_003" -p "zero_rt_lower_eye_bag_guide_003";
	rename -uid "277D736F-424B-DB8E-8AEA-A083417D7E00";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_lower_eye_bag_guide_003Shape" -p "loc_rt_lower_eye_bag_guide_003";
	rename -uid "D5AD9A82-4F58-FD19-6335-CE8398B844F0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_lower_eye_bag_guide_002" -p "grp_rt_eye_bags_guide_001";
	rename -uid "B4831D33-407E-2BF2-751D-B397E8EFE0E1";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_lower_eye_bag_guide_002" -p "zero_rt_lower_eye_bag_guide_002";
	rename -uid "02C179AD-4C79-5BA9-88DA-B397B20A9E95";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_lower_eye_bag_guide_002Shape" -p "loc_rt_lower_eye_bag_guide_002";
	rename -uid "4EC8483F-44F1-DB9B-7DD5-E99E5BD56DFA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "zero_rt_lower_eye_bag_guide_001" -p "grp_rt_eye_bags_guide_001";
	rename -uid "81B497C6-44AA-3613-5BDC-6584A18EE959";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_rt_lower_eye_bag_guide_001" -p "zero_rt_lower_eye_bag_guide_001";
	rename -uid "6536338D-46FD-7301-016B-8B8DF36A94DB";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_rt_lower_eye_bag_guide_001Shape" -p "loc_rt_lower_eye_bag_guide_001";
	rename -uid "BCB6F0F1-4594-4446-EEA4-20A5F2897EDD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "crv_rt_upper_eye_bag_guide_001" -p "grp_rt_eye_bags_guide_001";
	rename -uid "70E1F5A6-4C69-FB34-8410-F4A87C9B6A7D";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape18" -p "crv_rt_upper_eye_bag_guide_001";
	rename -uid "AB6D4C02-40D5-8133-501B-35ABE7BD2A9E";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-11.095543861389183 921.770446777345 61.916465759277429
		-17.322137832641609 935.3453369140625 62.539287567138672
		-27.721637725830085 939.0982666015625 62.341476440429688
		-41.111030578613288 935.79002564748384 57.85413742065429
		-44.514404296875007 927.34466552734375 48.438819885253899
		;
createNode transform -n "crv_rt_lower_eye_bag_guide_001" -p "grp_rt_eye_bags_guide_001";
	rename -uid "3F3DE6FC-4A47-0F4F-E2CC-B0980FFC6CEE";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape19" -p "crv_rt_lower_eye_bag_guide_001";
	rename -uid "814B1287-404F-AC00-CF9C-D6B1CE7EB932";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-11.095543861389183 921.770446777345 61.916465759277429
		-20.479196548461921 915.51069325865478 62.755046844482422
		-31.809101104736335 913.813335719973 59.792583465576165
		-41.439169523881134 918.83096443881573 53.821247100830071
		-44.514404296875007 927.34466552734375 48.438819885253899
		;
createNode transform -n "grp_lf_eye_bags_guide_001" -p "grp_md_eye_bags_guide_001";
	rename -uid "6D7BFBED-44FA-A1B0-4326-40ACBC197033";
createNode transform -n "zero_lf_upper_eye_bag_guide_001" -p "grp_lf_eye_bags_guide_001";
	rename -uid "4B00DAD0-4C80-C975-F6A2-ECAD5B976955";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_upper_eye_bag_guide_001" -p "zero_lf_upper_eye_bag_guide_001";
	rename -uid "154AB478-4CE5-D737-F51A-34AC5292D050";
	setAttr ".t" -type "double3" 17.322137832641602 935.3453369140625 62.539287567138672 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_upper_eye_bag_guide_001Shape" -p "loc_lf_upper_eye_bag_guide_001";
	rename -uid "213CBAC2-4964-7247-B043-5AB210092DEF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_eye_bag_guide_002" -p "grp_lf_eye_bags_guide_001";
	rename -uid "22F7F96D-4F0A-0386-586C-FD8E8C62923C";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_upper_eye_bag_guide_002" -p "zero_lf_upper_eye_bag_guide_002";
	rename -uid "759EAAFE-4208-23E1-3D60-7BB2A08EA75B";
	setAttr ".t" -type "double3" 27.721637725830078 939.0982666015625 62.341476440429688 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_upper_eye_bag_guide_002Shape" -p "loc_lf_upper_eye_bag_guide_002";
	rename -uid "B0953088-41E1-374B-E303-D3946D7F9AD3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_upper_eye_bag_guide_003" -p "grp_lf_eye_bags_guide_001";
	rename -uid "688B24AA-43A2-6BB7-DABC-8FA07618B79C";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_upper_eye_bag_guide_003" -p "zero_lf_upper_eye_bag_guide_003";
	rename -uid "DA803AC0-4628-D3CF-26B3-0DA02A57C674";
	setAttr ".t" -type "double3" 41.111030578613281 935.79002564748384 57.854137420654297 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_upper_eye_bag_guide_003Shape" -p "loc_lf_upper_eye_bag_guide_003";
	rename -uid "B54E0CF4-4A09-21C3-3786-9581FB4B5E47";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_inner_eye_bag_guide_001" -p "grp_lf_eye_bags_guide_001";
	rename -uid "A4EFABFE-4844-EC38-5AE2-AC9BDA8D31CB";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_inner_eye_bag_guide_001" -p "zero_lf_inner_eye_bag_guide_001";
	rename -uid "78063FF3-4ECD-B710-15DD-7C938C4CF397";
	setAttr ".t" -type "double3" 11.095543861389174 921.770446777345 61.916465759277429 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_inner_eye_bag_guide_001Shape" -p "loc_lf_inner_eye_bag_guide_001";
	rename -uid "2AD23780-4C11-DEA9-6BDB-35B1A140846D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_outer_eye_bag_guide_001" -p "grp_lf_eye_bags_guide_001";
	rename -uid "FFDA21DC-42DB-AAE6-EDDE-F39EDD2C4D32";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_outer_eye_bag_guide_001" -p "zero_lf_outer_eye_bag_guide_001";
	rename -uid "CC2CFE12-4835-4B39-86CE-768669AD6F1E";
	setAttr ".t" -type "double3" 44.514404296875 927.34466552734375 48.438819885253906 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_outer_eye_bag_guide_001Shape" -p "loc_lf_outer_eye_bag_guide_001";
	rename -uid "160CF3CF-4928-B140-89DD-24B9795E8E73";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 9;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_eye_bag_guide_001" -p "grp_lf_eye_bags_guide_001";
	rename -uid "6103E21C-4D7E-FEB5-60A9-8E8F3B58B8A2";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_lower_eye_bag_guide_001" -p "zero_lf_lower_eye_bag_guide_001";
	rename -uid "763C98DE-4F7C-913E-98C4-17864F879C3B";
	setAttr ".t" -type "double3" 20.479196548461914 915.51069325865478 62.755046844482422 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_lower_eye_bag_guide_001Shape" -p "loc_lf_lower_eye_bag_guide_001";
	rename -uid "23CB2F95-4620-8317-C127-C9B167FE0D9C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_eye_bag_guide_002" -p "grp_lf_eye_bags_guide_001";
	rename -uid "3E0AD3C3-4B69-6B33-4E92-C99DDA9FDA43";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_lower_eye_bag_guide_002" -p "zero_lf_lower_eye_bag_guide_002";
	rename -uid "B9D3D633-4086-7130-3F9D-0E817C5FB535";
	setAttr ".t" -type "double3" 31.809101104736328 913.813335719973 59.792583465576172 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_lower_eye_bag_guide_002Shape" -p "loc_lf_lower_eye_bag_guide_002";
	rename -uid "940096C4-4D49-1655-62B5-2D9D2C49CF5B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_lower_eye_bag_guide_003" -p "grp_lf_eye_bags_guide_001";
	rename -uid "1AB47BB4-40DE-98F0-8034-7FA2BA36A313";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode transform -n "loc_lf_lower_eye_bag_guide_003" -p "zero_lf_lower_eye_bag_guide_003";
	rename -uid "7B8C0B48-4CD6-F744-1CDA-9E8EC8652B9F";
	setAttr ".t" -type "double3" 41.439169523881127 918.83096443881573 53.821247100830078 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.94999999 0.2 0.72000003 ;
createNode locator -n "loc_lf_lower_eye_bag_guide_003Shape" -p "loc_lf_lower_eye_bag_guide_003";
	rename -uid "307A6E0A-4993-9183-D294-ACB6FD3916E9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 0.94999999 0.2 0.72000003 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "crv_lf_upper_eye_bag_guide_001" -p "grp_lf_eye_bags_guide_001";
	rename -uid "702D231D-45D5-CBAA-3CBD-CFB7346B27A2";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape16" -p "crv_lf_upper_eye_bag_guide_001";
	rename -uid "3647C8CC-4527-43DE-BE43-1D856A7F6C1D";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		11.095543861389174 921.770446777345 61.916465759277429
		17.322137832641602 935.3453369140625 62.539287567138672
		27.721637725830078 939.0982666015625 62.341476440429688
		41.111030578613281 935.79002564748384 57.854137420654297
		44.514404296875 927.34466552734375 48.438819885253906
		;
createNode transform -n "crv_lf_lower_eye_bag_guide_001" -p "grp_lf_eye_bags_guide_001";
	rename -uid "DD7C0DBF-4B91-CE59-639B-F48F69CDF4B8";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430647 70.219694181714345 ;
createNode nurbsCurve -n "curveShape17" -p "crv_lf_lower_eye_bag_guide_001";
	rename -uid "AD55D8A9-4200-B451-17D6-62B974635401";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		11.095543861389174 921.770446777345 61.916465759277429
		20.479196548461914 915.51069325865478 62.755046844482422
		31.809101104736328 913.813335719973 59.792583465576172
		41.439169523881127 918.83096443881573 53.821247100830078
		44.514404296875 927.34466552734375 48.438819885253906
		;
createNode transform -n "grp_md_jaw_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "74E15B54-4B30-A3FC-9497-F79355734C93";
	setAttr ".t" -type "double3" -8.8817841970012523e-16 -4.5093141948119637 -44.11802004479226 ;
	setAttr ".rp" -type "double3" 4.8249478340148917 160.16279781658676 72.59101767707638 ;
	setAttr ".sp" -type "double3" 4.8249478340148917 160.16279781658676 72.59101767707638 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode transform -n "zero_md_jaw_start_guide_001" -p "grp_md_jaw_guide_001";
	rename -uid "16C5DD31-41D0-CB46-5DF9-3680B87FDC7B";
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
	rename -uid "4158F754-4EF4-E5ED-DB3B-CFB96BDC7F05";
	setAttr ".t" -type "double3" 0 -32.408103494802162 75.620242775090802 ;
	setAttr -l on ".tx";
	setAttr ".rp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".sp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode locator -n "loc_md_jaw_start_guide_001Shape" -p "loc_md_jaw_start_guide_001";
	rename -uid "FEDDAB4F-451E-613B-58C5-E7B85268D716";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 21;
	setAttr ".ovrgb" -type "float3" 1 0.41999999 0.079999998 ;
	setAttr ".lp" -type "double3" -2.7179870714047889e-15 161.34430700893438 6.8931037607512913 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_jaw_end_guide_001" -p "loc_md_jaw_start_guide_001";
	rename -uid "3C0079E0-44C7-5F2A-89B8-5DBBD0086E53";
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
	rename -uid "FBE49331-48AC-D0E1-6081-A1B57448E699";
	setAttr ".t" -type "double3" 0 134.18644025680953 54.256952348413087 ;
	setAttr -l on ".tx";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.41999999 0.079999998 ;
createNode locator -n "loc_md_jaw_end_guide_001Shape" -p "loc_md_jaw_end_guide_001";
	rename -uid "8DABB9AC-4CD5-A8C8-8643-D894F3DBE0CF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 21;
	setAttr ".ovrgb" -type "float3" 1 0.41999999 0.079999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "crv_md_jaw_guide_001" -p "grp_md_jaw_guide_001";
	rename -uid "CD644C93-4A8F-8338-B924-CE86B80EC37D";
	setAttr ".t" -type "double3" 8.8817841970012523e-16 -768.81659186430511 70.219694181714345 ;
createNode nurbsCurve -n "curveShape20" -p "crv_md_jaw_guide_001";
	rename -uid "597D6214-4BA0-BCFF-2B4B-ABAD3CF8962C";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 2 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		-3.6061654911049141e-15 897.75279537843733 12.293652354127747
		-8.8817841970012523e-16 870.59492862631248 59.657500941789543
		;
createNode transform -n "grp_md_brow_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "8D268A5E-40D6-75F1-294C-E09AC61EA35A";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_lf_brow_main_guide_001" -p "grp_md_brow_guide_001";
	rename -uid "4817944E-4A6F-292B-17FD-CD886AD24439";
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
	rename -uid "EB2EAF2B-4EA8-A059-6BE9-8B988BC293E2";
	setAttr ".t" -type "double3" 27.038382291793823 945.65768257164905 68.284600829618725 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_main_guide_001Shape" -p "loc_lf_brow_main_guide_001";
	rename -uid "0F9A7D21-4532-8D88-636B-E6B9AD039029";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_001" -p "loc_lf_brow_main_guide_001";
	rename -uid "CC5D8010-44FB-6781-579A-B68BCA2BAFCA";
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
	rename -uid "00E90087-463B-CA42-641B-9FBF6DF5A0D0";
	setAttr ".t" -type "double3" -18.947298765182495 -3.4152509310240475 2.9878448490922125 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_001Shape" -p "loc_lf_brow_guide_001";
	rename -uid "A8050FDA-4E1C-FA07-1109-8E9264422B1E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_002" -p "loc_lf_brow_main_guide_001";
	rename -uid "0E790CA1-41C1-3C12-8886-D8A9A53FE3A1";
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
	rename -uid "48046DA1-4A81-2C88-0E09-BB98B6BA68CB";
	setAttr ".t" -type "double3" -8.570239782333374 -1.7668744661802975 1.0016807560746344 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_002Shape" -p "loc_lf_brow_guide_002";
	rename -uid "7FC0B416-4767-6900-B64E-A5B9AAD54758";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_003" -p "loc_lf_brow_main_guide_001";
	rename -uid "A1900F9B-4692-49A9-4B0F-99BE3284D254";
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
	rename -uid "3B04FA6A-4BF3-4601-522D-D8916505A216";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_003Shape" -p "loc_lf_brow_guide_003";
	rename -uid "D20CF294-4AED-8BBA-13FD-6FAD9090A9E4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_004" -p "loc_lf_brow_main_guide_001";
	rename -uid "EBFD3E14-4C57-D49A-08B1-B1B862265CB5";
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
	rename -uid "5577568B-4D3E-AC5C-C31E-9E823E6BE5FC";
	setAttr ".t" -type "double3" 9.2975475788116455 0.94894584631970247 -4.629571532743725 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_004Shape" -p "loc_lf_brow_guide_004";
	rename -uid "2D0B1999-4C1A-D9A5-B780-82972301672C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_brow_guide_005" -p "loc_lf_brow_main_guide_001";
	rename -uid "E00E5864-49DC-96EC-8C22-54B8279F2756";
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
	rename -uid "BA663CC3-4D4A-9CA0-0EE8-DBB20DA87B3C";
	setAttr ".t" -type "double3" 19.132313966751099 -3.9316693880552975 -18.969853972929272 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_lf_brow_guide_005Shape" -p "loc_lf_brow_guide_005";
	rename -uid "4184AAF3-4695-7671-84D3-8D869B633C03";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "crv_lf_brow_guide_001" -p "loc_lf_brow_main_guide_001";
	rename -uid "3906D48C-4D79-0C20-F90F-949B9EECD510";
	setAttr ".t" -type "double3" -27.038382291793823 -945.65768257164905 -68.284600829618725 ;
createNode nurbsCurve -n "curveShape8" -p "crv_lf_brow_guide_001";
	rename -uid "B719BE55-47BF-B837-D41E-7B87A13D252B";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		8.0910835266113281 942.242431640625 71.272445678710938
		18.468142509460449 943.89080810546875 69.286281585693359
		27.038382291793823 945.65768257164905 68.284600829618725
		36.335929870605469 946.60662841796875 63.655029296875
		46.170696258544922 941.72601318359375 49.314746856689453
		;
createNode transform -n "zero_rt_brow_main_guide_001" -p "grp_md_brow_guide_001";
	rename -uid "2E0BEBE6-489E-EFC0-1EFC-6ABB87EE8D26";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_main_guide_001" -p "zero_rt_brow_main_guide_001";
	rename -uid "4AFEBA91-415B-0CEF-CCCE-64A744CE53B7";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_main_guide_001Shape" -p "loc_rt_brow_main_guide_001";
	rename -uid "18F2F54E-45DB-7A25-A037-42915C0E5883";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_001" -p "loc_rt_brow_main_guide_001";
	rename -uid "FE4BDE97-45A9-6A98-FE5D-8EB852EC846C";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_001" -p "zero_rt_brow_guide_001";
	rename -uid "8B4A654B-4506-17FE-6120-4399C765C1CC";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_001Shape" -p "loc_rt_brow_guide_001";
	rename -uid "61756549-433E-9521-3FFD-1D9C4E0565A5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_002" -p "loc_rt_brow_main_guide_001";
	rename -uid "C73EBC74-4216-3A9B-AA3B-A7A16E093176";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_002" -p "zero_rt_brow_guide_002";
	rename -uid "C7544022-453A-82DC-DB4C-DD9EE060DFA5";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_002Shape" -p "loc_rt_brow_guide_002";
	rename -uid "E97654BB-4260-AF24-F61D-6DB7C08FBAB5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_003" -p "loc_rt_brow_main_guide_001";
	rename -uid "E770E0FF-4FFF-566A-8808-C48802097A46";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_003" -p "zero_rt_brow_guide_003";
	rename -uid "3F9E28C3-40FF-8CCB-A0AA-F7ACEC92158D";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_003Shape" -p "loc_rt_brow_guide_003";
	rename -uid "C703478B-45C0-F5A5-6904-01A950911C57";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_004" -p "loc_rt_brow_main_guide_001";
	rename -uid "971DFA0F-4BCB-86F7-E06A-66ACC21591ED";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_004" -p "zero_rt_brow_guide_004";
	rename -uid "7F219766-4FCA-2BAB-849F-4384B107B3E0";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_004Shape" -p "loc_rt_brow_guide_004";
	rename -uid "72045A55-459F-69E6-7B50-7A97615FE430";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "zero_rt_brow_guide_005" -p "loc_rt_brow_main_guide_001";
	rename -uid "EC5D6DC8-4F4F-8245-63F7-0183D5F94D66";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "loc_rt_brow_guide_005" -p "zero_rt_brow_guide_005";
	rename -uid "E52D114A-4CE9-343B-3EE3-F6AE5B0C3686";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.72000003 0.050000001 ;
createNode locator -n "loc_rt_brow_guide_005Shape" -p "loc_rt_brow_guide_005";
	rename -uid "558E860E-435B-5DB4-B2FB-D39C71BECEE5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 17;
	setAttr ".ovrgb" -type "float3" 1 0.72000003 0.050000001 ;
createNode transform -n "crv_rt_brow_guide_001" -p "loc_rt_brow_main_guide_001";
	rename -uid "F174A781-434A-FB70-A881-12942E15EE28";
	setAttr ".t" -type "double3" -27.03838229179382 -945.65768257164893 -68.284600829618711 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".s" -type "double3" 1 1 -1 ;
createNode nurbsCurve -n "curveShape9" -p "crv_rt_brow_guide_001";
	rename -uid "0E98B305-469E-FCB2-754C-A8AE858BD820";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-8.0910835266113281 942.242431640625 71.272445678710938
		-18.468142509460449 943.89080810546875 69.286281585693359
		-27.038382291793823 945.65768257164905 68.284600829618725
		-36.335929870605469 946.60662841796875 63.655029296875
		-46.170696258544922 941.72601318359375 49.314746856689453
		;
createNode transform -n "grp_md_teeth_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "5B2C74AD-4740-8F82-0304-C99C588361B0";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode transform -n "zero_md_upper_teeth_guide_001" -p "grp_md_teeth_guide_001";
	rename -uid "01E428A1-44B6-C74F-0C07-74B34838C68A";
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
	rename -uid "6FF44F26-471A-69D1-BF1C-C38772EA2A08";
	setAttr ".t" -type "double3" 0.0009918212890625 893.0157470703125 53.838485717773438 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode locator -n "loc_md_upper_teeth_guide_001Shape" -p "loc_md_upper_teeth_guide_001";
	rename -uid "19DE0CA5-4B35-C6FD-99CB-3BA3BDA9B755";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 16;
	setAttr ".ovrgb" -type "float3" 0.92000002 0.92000002 0.77999997 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_md_lower_teeth_guide_001" -p "grp_md_teeth_guide_001";
	rename -uid "39928BA8-4879-53DB-5918-309D77EB2533";
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
	rename -uid "AB19906C-4B98-9C43-54A0-69945581D4A9";
	setAttr ".t" -type "double3" 0.010724067687988281 888.985107421875 53.342178344726562 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.92000002 0.92000002 0.77999997 ;
createNode locator -n "loc_md_lower_teeth_guide_001Shape" -p "loc_md_lower_teeth_guide_001";
	rename -uid "71148806-4CE0-8C8B-2170-E49B490E1487";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 16;
	setAttr ".ovrgb" -type "float3" 0.92000002 0.92000002 0.77999997 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "grp_md_lip_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "2C19D535-4EE2-2F44-B516-6F915E0B3450";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_md_upper_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "4E2E58D7-425B-693E-BDD8-BB810DE584E1";
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
	rename -uid "6BC76C5B-4702-D85A-D2E3-2AB213488F96";
	setAttr ".t" -type "double3" 0 892.22186279296875 74.020088195800781 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_md_upper_lip_guide_001Shape" -p "loc_md_upper_lip_guide_001";
	rename -uid "0A772CD2-49E8-9CF3-2606-8F873938459C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_upper_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "0EA58499-43DE-DBA8-45AB-378993EADCCF";
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
	rename -uid "079B4D9E-421A-B13A-B671-F68EC2FC3012";
	setAttr ".t" -type "double3" 6.5477989414050422 892.76502109125295 72.939836177230916 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_upper_lip_guide_001Shape" -p "loc_lf_upper_lip_guide_001";
	rename -uid "E3428600-47F2-E2BF-8042-93A3F9904544";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_upper_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "DFBAD3F9-4D68-C463-6C6A-6985402FFC23";
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
	rename -uid "9FF0A7E6-466A-DE8A-8ABA-9A80649A4C6A";
	setAttr ".t" -type "double3" 10.205770930650683 890.63682479554507 69.150216379277666 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_upper_lip_guide_002Shape" -p "loc_lf_upper_lip_guide_002";
	rename -uid "5F0271CD-4A26-C426-AA5A-DE867C2410BF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_upper_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "4D2D8554-461F-3E21-DBE0-CD8DED0DA7E1";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_upper_lip_guide_001" -p "zero_rt_upper_lip_guide_001";
	rename -uid "010761B5-4CE1-2784-CE25-FE9D98F7BBB0";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_upper_lip_guide_001Shape" -p "loc_rt_upper_lip_guide_001";
	rename -uid "6420AAA9-44D0-08FF-9495-6DBD92B94725";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_rt_upper_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "58814675-4709-CD22-3713-1D86BD9B878D";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_upper_lip_guide_002" -p "zero_rt_upper_lip_guide_002";
	rename -uid "ADD5B1D4-4AF4-26B7-0FE9-38AC8972FDE6";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_upper_lip_guide_002Shape" -p "loc_rt_upper_lip_guide_002";
	rename -uid "0BE5553C-46CA-068D-2F7E-EA8B3EAED3F7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_lf_mouth_corner_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "D8036261-4330-7795-7F41-1B8D99C5DF98";
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
	rename -uid "E7317BA8-4856-7ED2-B5B2-5493089E32F7";
	setAttr ".t" -type "double3" 14.916315078735352 888.8077392578125 63.507129669189453 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_mouth_corner_guide_001Shape" -p "loc_lf_mouth_corner_guide_001";
	rename -uid "357AD8C9-465D-5BFF-14CC-8AA001DEC9A9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_mouth_corner_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "732CA18C-4582-547A-F661-35B66C4A16B4";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_mouth_corner_guide_001" -p "zero_rt_mouth_corner_guide_001";
	rename -uid "40948CC8-4977-25E1-5933-55838C09E209";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_mouth_corner_guide_001Shape" -p "loc_rt_mouth_corner_guide_001";
	rename -uid "DE3D35AF-4278-4DAF-08E8-CAACAF21B8E0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_md_lower_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "39CD81AE-4EB4-DE63-25C8-588545B16802";
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
	rename -uid "BBD1DDB3-4D62-2B9E-C6BC-D68975CE0E64";
	setAttr ".t" -type "double3" 0 882.94843394032011 74.020088195800781 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_md_lower_lip_guide_001Shape" -p "loc_md_lower_lip_guide_001";
	rename -uid "C14B9B04-46E8-79FE-457B-8DAB8451CDA5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_lower_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "6B3CD46E-49C8-832B-20E3-77B79E5DA57F";
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
	rename -uid "B4CFB052-4A9D-B2E2-86A0-B4B7CBFAB7C6";
	setAttr ".t" -type "double3" 6.6253784360383987 883.47470036636889 69.648095703382168 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_lower_lip_guide_001Shape" -p "loc_lf_lower_lip_guide_001";
	rename -uid "D5817944-4F5D-D9DE-5445-41992B716A04";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_lf_lower_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "F715BBC4-45F5-083A-04D4-F5BA809A033F";
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
	rename -uid "42F4F760-4185-B117-E495-A9AA69F3D18B";
	setAttr ".t" -type "double3" 10.211730939521074 886.85846770270939 68.357601887976926 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_lf_lower_lip_guide_002Shape" -p "loc_lf_lower_lip_guide_002";
	rename -uid "CB87091F-4185-8285-B5D8-428458C12796";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_rt_lower_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "D3980A6A-40F1-ECCA-69BB-5FADF4FE33E4";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_lower_lip_guide_001" -p "zero_rt_lower_lip_guide_001";
	rename -uid "2A74388E-433C-67C7-99F4-62B3671D5CB7";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_lower_lip_guide_001Shape" -p "loc_rt_lower_lip_guide_001";
	rename -uid "E44D6016-47C5-E4FA-5CE5-2A9EAFBB8DF3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "zero_rt_lower_lip_guide_002" -p "grp_md_lip_guide_001";
	rename -uid "6552D544-4FCF-BE24-0D0D-9EA5BB9A60CD";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "loc_rt_lower_lip_guide_002" -p "zero_rt_lower_lip_guide_002";
	rename -uid "354B8BBF-4A50-623D-1B92-9182701A1581";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.12 0.18000001 ;
createNode locator -n "loc_rt_lower_lip_guide_002Shape" -p "loc_rt_lower_lip_guide_002";
	rename -uid "72CDB2EB-4F4F-C2FB-EE2B-45A67498DF5C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 13;
	setAttr ".ovrgb" -type "float3" 1 0.12 0.18000001 ;
createNode transform -n "crv_md_upper_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "7835682F-4992-7E6B-A05F-DEAA659B4876";
createNode nurbsCurve -n "curveShape10" -p "crv_md_upper_lip_guide_001";
	rename -uid "B55D1B5F-4803-7ACD-D9B8-FCAAC75FEAEF";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 7 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 1 2 3 4 5 6
		7
		14.916315078735352 888.8077392578125 63.507129669189453
		10.205770930650683 890.63682479554507 69.150216379277666
		6.5477989414050422 892.76502109125295 72.939836177230916
		0 892.22186279296875 74.020088195800781
		-6.5477989414050422 892.76502109125295 72.939836177230916
		-10.205770930650683 890.63682479554507 69.150216379277666
		-14.916315078735352 888.8077392578125 63.507129669189453
		;
createNode transform -n "crv_md_lower_lip_guide_001" -p "grp_md_lip_guide_001";
	rename -uid "F5C42F1B-4FC9-F3E2-0BF5-B9A41A4FB62C";
createNode nurbsCurve -n "curveShape11" -p "crv_md_lower_lip_guide_001";
	rename -uid "126A5104-4D37-315B-11FC-59941E537BC8";
	addAttr -ci true -k true -sn "ll" -ln "lockLength" -min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 7 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 6 0 no 3
		7 0 1 2 3 4 5 6
		7
		14.916315078735352 888.8077392578125 63.507129669189453
		10.211730939521074 886.85846770270939 68.357601887976926
		6.6253784360383987 883.47470036636889 69.648095703382168
		0 882.94843394032011 74.020088195800781
		-6.6253784360383987 883.47470036636889 69.648095703382168
		-10.211730939521074 886.85846770270939 68.357601887976926
		-14.916315078735352 888.8077392578125 63.507129669189453
		;
createNode transform -n "grp_md_tongue_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "1A9EA3A0-4DCC-E8BA-F0EB-57A3E2108BB5";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode transform -n "zero_md_tongue_guide_001" -p "grp_md_tongue_guide_001";
	rename -uid "1AB05258-4C0A-8900-16FA-41AB1D88AF51";
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
	rename -uid "7BE4D178-4256-E75C-8BD7-1EADE527518F";
	setAttr ".t" -type "double3" 0 884.68551007538588 21.481754293539911 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_001Shape" -p "loc_md_tongue_guide_001";
	rename -uid "F2E37633-468B-6446-3682-8B948B27B192";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_002" -p "loc_md_tongue_guide_001";
	rename -uid "87ADBBF5-4A80-6D21-1EBE-26B07D9ECFEB";
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
	rename -uid "461C42F7-462A-37A4-8AE3-A4AD852BB271";
	setAttr ".t" -type "double3" 0 4.0712308883461219 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_002Shape" -p "loc_md_tongue_guide_002";
	rename -uid "24D04BAE-4495-3C30-9179-EA97A64BB01A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_003" -p "loc_md_tongue_guide_002";
	rename -uid "C5906A05-457C-7BEC-406B-05B7E535773E";
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
	rename -uid "202EA624-4723-37CA-66FA-C7A45A862C5B";
	setAttr ".t" -type "double3" 0 4.0712308883461219 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_003Shape" -p "loc_md_tongue_guide_003";
	rename -uid "B89B7C16-4632-B9AF-FF8E-79BCBC60BEA2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_004" -p "loc_md_tongue_guide_003";
	rename -uid "27A22EC3-4087-9455-3892-6CA3ABED967A";
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
	rename -uid "0D1DB3BF-46FC-6B08-CD2D-A7AAE2C4A949";
	setAttr ".t" -type "double3" 0 -2.65083241927789 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_004Shape" -p "loc_md_tongue_guide_004";
	rename -uid "853A91E1-40C1-ED25-CB68-1084F3B00F61";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "zero_md_tongue_guide_005" -p "loc_md_tongue_guide_004";
	rename -uid "FCFE12C8-40B0-A625-67FB-9C9D0D2B7E1F";
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
	rename -uid "768ECCF7-49F2-4297-11DE-34948F96FD78";
	setAttr ".t" -type "double3" 0 -4.5214447098502433 10.253410919902333 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 0.31999999 0.51999998 ;
createNode locator -n "loc_md_tongue_guide_005Shape" -p "loc_md_tongue_guide_005";
	rename -uid "A5604748-4F5C-9542-AB25-46B21BB4ED4C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 20;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr ".los" -type "double3" 4.8999999999999995 4.8999999999999995 4.8999999999999995 ;
createNode transform -n "crv_md_tongue_guide_001" -p "grp_md_tongue_guide_001";
	rename -uid "AE378961-4A0F-767D-FFBF-B3A8CB08CB31";
	setAttr ".it" no;
createNode nurbsCurve -n "curveShape7" -p "crv_md_tongue_guide_001";
	rename -uid "5D9C4125-48C8-0CAA-0C37-ACB3557E87C4";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0.31999999 0.51999998 ;
	setAttr -s 5 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		0 884.68551007538588 21.481754293539911
		0 888.756740963732 31.735165213442244
		0 892.82797185207812 41.98857613334458
		0 890.17713943280023 52.241987053246916
		0 885.65569472294999 62.495397973149252
		;
createNode transform -n "grp_md_zygoma_guide_001" -p "ctrl_md_face_move_001";
	rename -uid "E407EDA2-4E66-637A-5615-0AB4A0B3F20B";
	setAttr ".t" -type "double3" 0 -773.32590605911707 26.101674136922082 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode transform -n "grp_lf_zygoma_guide_001" -p "grp_md_zygoma_guide_001";
	rename -uid "91123C74-4F2E-C7B2-6E80-86A1B7347ED9";
createNode transform -n "zero_lf_zygoma_guide_001" -p "grp_lf_zygoma_guide_001";
	rename -uid "8222C5CD-40FC-1949-F66E-FAB511CB1C72";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode transform -n "loc_lf_zygoma_guide_001" -p "zero_lf_zygoma_guide_001";
	rename -uid "EA1BEB6C-4A6F-A598-700C-C29A8469F24B";
	setAttr ".t" -type "double3" 10.599196434020996 916.290283203125 65.919540405273438 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode locator -n "loc_lf_zygoma_guide_001Shape" -p "loc_lf_zygoma_guide_001";
	rename -uid "73FF8B24-4424-A4A3-69AB-CDB694401760";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0.94999999 0.68000001 ;
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_zygoma_guide_002" -p "grp_lf_zygoma_guide_001";
	rename -uid "7CE7182B-4BF5-0AFE-8E2A-9CB8D1067B66";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode transform -n "loc_lf_zygoma_guide_002" -p "zero_lf_zygoma_guide_002";
	rename -uid "5357DCF3-4ED2-EEF9-2473-F29114726EC7";
	setAttr ".t" -type "double3" 26.95750617980957 907.423095703125 63.240692138671875 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode locator -n "loc_lf_zygoma_guide_002Shape" -p "loc_lf_zygoma_guide_002";
	rename -uid "C013E3E4-49D1-89B1-FBEA-A5B43746A3CD";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "zero_lf_zygoma_guide_003" -p "grp_lf_zygoma_guide_001";
	rename -uid "FC598ED0-4711-B27F-FF40-A88ACE011A90";
createNode transform -n "loc_lf_zygoma_guide_003" -p "zero_lf_zygoma_guide_003";
	rename -uid "AF274ACE-4702-ED39-59D4-438A6FF642ED";
	setAttr ".t" -type "double3" 49.228466652018575 911.93424312423656 58.506034603746429 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0 0.94999999 0.68000001 ;
createNode locator -n "loc_lf_zygoma_guide_003Shape" -p "loc_lf_zygoma_guide_003";
	rename -uid "6D2F5D22-48CF-DBAB-A331-5DA6D5BF16AD";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "crv_lf_zygoma_guide_001" -p "grp_lf_zygoma_guide_001";
	rename -uid "6C0B5523-4D7D-B1FA-8B39-9D8E66DE2EE1";
createNode nurbsCurve -n "curveShape22" -p "crv_lf_zygoma_guide_001";
	rename -uid "7B8A25DA-4ECA-0A88-F1C7-AD959E8AB15D";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 2 0 no 3
		3 0 1 2
		3
		10.599196434020996 916.290283203125 65.919540405273438
		26.95750617980957 907.423095703125 63.240692138671875
		49.228466652018575 911.93424312423656 58.506034603746429
		;
createNode transform -n "grp_rt_zygoma_guide_001" -p "grp_md_zygoma_guide_001";
	rename -uid "B70965FD-418A-618A-505E-6D87032626E9";
createNode transform -n "zero_rt_zygoma_guide_001" -p "grp_rt_zygoma_guide_001";
	rename -uid "4792C670-4C3D-2FC4-A3B7-459093BBAC71";
	setAttr ".s" -type "double3" -1 1 1 ;
createNode transform -n "loc_rt_zygoma_guide_001" -p "zero_rt_zygoma_guide_001";
	rename -uid "EAD44D2D-4693-45C3-1484-9E95C0ED9AC8";
createNode locator -n "loc_rt_zygoma_guide_001Shape" -p "loc_rt_zygoma_guide_001";
	rename -uid "DD56998F-4551-B2D5-3238-EAA8A7BDCBC3";
	setAttr -k off ".v";
createNode transform -n "zero_rt_zygoma_guide_002" -p "grp_rt_zygoma_guide_001";
	rename -uid "A5CC2C1C-4565-8327-2F88-EDBDD8DBCBC1";
	setAttr ".s" -type "double3" -1 1 1 ;
createNode transform -n "loc_rt_zygoma_guide_002" -p "zero_rt_zygoma_guide_002";
	rename -uid "B0A395B7-4D8E-6683-4F1F-468AD8789FA9";
createNode locator -n "loc_rt_zygoma_guide_002Shape" -p "loc_rt_zygoma_guide_002";
	rename -uid "3C7C55BF-4C6F-4E28-216D-C1A79C1581C8";
	setAttr -k off ".v";
createNode transform -n "zero_rt_zygoma_guide_003" -p "grp_rt_zygoma_guide_001";
	rename -uid "7D454BF9-455C-B4FE-C9AB-91987074A720";
	setAttr ".s" -type "double3" -1 1 1 ;
createNode transform -n "loc_rt_zygoma_guide_003" -p "zero_rt_zygoma_guide_003";
	rename -uid "728BD2AA-4464-8B06-C92C-A39BA3DD22B7";
	setAttr ".t" -type "double3" 49.228466652018575 911.93424312423656 58.506034603746429 ;
createNode locator -n "loc_rt_zygoma_guide_003Shape" -p "loc_rt_zygoma_guide_003";
	rename -uid "6D54D1FC-454A-AD24-F62A-CF86D6439BD3";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 4 4 4 ;
createNode transform -n "crv_rt_zygoma_guide_001" -p "grp_rt_zygoma_guide_001";
	rename -uid "87569D44-4479-2BFF-3B37-EB8669747EB3";
createNode nurbsCurve -n "curveShape23" -p "crv_rt_zygoma_guide_001";
	rename -uid "4A6AB09C-4602-3CE8-1A1E-3597D7A241EF";
	setAttr -k off ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -s 3 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 2 0 no 3
		3 0 1 2
		3
		-10.599196434020996 916.290283203125 65.919540405273438
		-26.95750617980957 907.423095703125 63.240692138671875
		-49.228466652018575 911.93424312423656 58.506034603746429
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "CE33E1E8-47E8-A33D-0BEB-E88B93216E8A";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "21BF0F81-4A66-F69B-CA65-219BE187F1D1";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "AA473E14-45F6-EA84-36A6-DBAA17027158";
createNode displayLayerManager -n "layerManager";
	rename -uid "7FAE2AFC-484C-BAD1-50FC-4998C66200BF";
createNode displayLayer -n "defaultLayer";
	rename -uid "237A14AC-4611-603B-E460-35A799EB2443";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "5081B234-4062-B0BA-7DE8-71974D11B3B0";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "A7515B81-4B70-4F69-4840-68BAEAE50BBF";
	setAttr ".g" yes;
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "B1990A54-411B-6295-83B4-BD9D330DC62D";
	setAttr ".version" -type "string" "5.2.1.1";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "418CCC98-4FF4-4329-DFC1-61AC1E968DB0";
	setAttr ".ai_translator" -type "string" "gaussian";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "6E3CCB93-4F0F-CEE9-ABF0-528DFB3D3540";
	setAttr ".ai_translator" -type "string" "exr";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "FC3A552B-4D33-EA10-D1D6-8DA693AD5E08";
	setAttr ".output_mode" 0;
	setAttr ".ai_translator" -type "string" "maya";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "CC502687-4F3D-7DFE-D094-34ABAF267640";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n"
		+ "            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n"
		+ "            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n"
		+ "            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n"
		+ "            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n"
		+ "            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n"
		+ "            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n"
		+ "            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n"
		+ "            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1156\n            -height 689\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n"
		+ "            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n"
		+ "            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n"
		+ "            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n"
		+ "            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n"
		+ "                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n"
		+ "                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n"
		+ "                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -valueLinesToggle 1\n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n"
		+ "                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n"
		+ "                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n"
		+ "                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n"
		+ "                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n"
		+ "                -additiveGraphingMode 1\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n"
		+ "                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 1\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n"
		+ "                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n"
		+ "                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n"
		+ "        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1156\\n    -height 689\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1156\\n    -height 689\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 100 -size 300 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "3523E45B-4202-34B0-3003-42AD0101C514";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 10 -ast 0 -aet 30 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "2A21B5E0-4F2F-2F62-2CCA-DFB043FD7E6E";
	setAttr ".tgi[0].tn" -type "string" "Œﬁ±ÍÃ‚_1";
	setAttr ".tgi[0].vl" -type "double2" 388.75341843730155 -1207.8268262030299 ;
	setAttr ".tgi[0].vh" -type "double2" 1808.9469698867474 -623.23300012820062 ;
	setAttr -s 8 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 631.4285888671875;
	setAttr ".tgi[0].ni[0].y" -761.4285888671875;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 1002.8571166992188;
	setAttr ".tgi[0].ni[1].y" -761.4285888671875;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 674.11761474609375;
	setAttr ".tgi[0].ni[2].y" -847.7310791015625;
	setAttr ".tgi[0].ni[2].nvs" 18305;
	setAttr ".tgi[0].ni[3].x" 1418.5130615234375;
	setAttr ".tgi[0].ni[3].y" -959.81787109375;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 144.03361511230469;
	setAttr ".tgi[0].ni[4].y" -830.08404541015625;
	setAttr ".tgi[0].ni[4].nvs" 18305;
	setAttr ".tgi[0].ni[5].x" 1002.8571166992188;
	setAttr ".tgi[0].ni[5].y" -865.71429443359375;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 1377.142822265625;
	setAttr ".tgi[0].ni[6].y" -812.85711669921875;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" 1377.142822265625;
	setAttr ".tgi[0].ni[7].y" -998.5714111328125;
	setAttr ".tgi[0].ni[7].nvs" 18304;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
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
connectAttr "loc_lf_ear_guide_001Shape.wp" "curveShape1.cp[0]";
connectAttr "loc_lf_ear_guide_002Shape.wp" "curveShape1.cp[1]";
connectAttr "loc_lf_ear_guide_003Shape.wp" "curveShape1.cp[2]";
connectAttr "loc_rt_ear_guide_001Shape.wp" "curveShape2.cp[0]";
connectAttr "loc_rt_ear_guide_002Shape.wp" "curveShape2.cp[1]";
connectAttr "loc_rt_ear_guide_003Shape.wp" "curveShape2.cp[2]";
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
connectAttr "loc_md_muzzle_guide_001Shape.wp" "curveShape21.cp[0]";
connectAttr "loc_md_nose_guide_001Shape.wp" "curveShape21.cp[1]";
connectAttr "loc_md_nose_center_guide_001Shape.wp" "curveShape21.cp[2]";
connectAttr "loc_md_nose_front_guide_001Shape.wp" "curveShape21.cp[3]";
connectAttr "loc_lf_nose_side_guide_001Shape.wp" "curveShape21.cp[4]";
connectAttr "loc_md_nose_down_guide_001Shape.wp" "curveShape21.cp[5]";
connectAttr "loc_rt_nose_side_guide_001Shape.wp" "curveShape21.cp[6]";
connectAttr "loc_lf_eye_iris_guide_001.tx" "loc_lf_eye_aim_guide_001.tx";
connectAttr "loc_lf_eye_iris_guide_001.ty" "loc_lf_eye_aim_guide_001.ty";
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
connectAttr "loc_lf_inner_lid_guide_001Shape.wp" "curveShape12.cp[0]";
connectAttr "loc_lf_upper_lid_guide_001Shape.wp" "curveShape12.cp[1]";
connectAttr "loc_lf_upper_lid_guide_002Shape.wp" "curveShape12.cp[2]";
connectAttr "loc_lf_upper_lid_guide_003Shape.wp" "curveShape12.cp[3]";
connectAttr "loc_lf_outer_lid_guide_001Shape.wp" "curveShape12.cp[4]";
connectAttr "loc_lf_inner_lid_guide_001Shape.wp" "curveShape13.cp[0]";
connectAttr "loc_lf_lower_lid_guide_001Shape.wp" "curveShape13.cp[1]";
connectAttr "loc_lf_lower_lid_guide_002Shape.wp" "curveShape13.cp[2]";
connectAttr "loc_lf_lower_lid_guide_003Shape.wp" "curveShape13.cp[3]";
connectAttr "loc_lf_outer_lid_guide_001Shape.wp" "curveShape13.cp[4]";
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
connectAttr "loc_rt_inner_lid_guide_001Shape.wp" "curveShape14.cp[0]";
connectAttr "loc_rt_upper_lid_guide_001Shape.wp" "curveShape14.cp[1]";
connectAttr "loc_rt_upper_lid_guide_002Shape.wp" "curveShape14.cp[2]";
connectAttr "loc_rt_upper_lid_guide_003Shape.wp" "curveShape14.cp[3]";
connectAttr "loc_rt_outer_lid_guide_001Shape.wp" "curveShape14.cp[4]";
connectAttr "loc_rt_inner_lid_guide_001Shape.wp" "curveShape15.cp[0]";
connectAttr "loc_rt_lower_lid_guide_001Shape.wp" "curveShape15.cp[1]";
connectAttr "loc_rt_lower_lid_guide_002Shape.wp" "curveShape15.cp[2]";
connectAttr "loc_rt_lower_lid_guide_003Shape.wp" "curveShape15.cp[3]";
connectAttr "loc_rt_outer_lid_guide_001Shape.wp" "curveShape15.cp[4]";
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
connectAttr "loc_rt_inner_eye_bag_guide_001Shape.wp" "curveShape18.cp[0]";
connectAttr "loc_rt_upper_eye_bag_guide_001Shape.wp" "curveShape18.cp[1]";
connectAttr "loc_rt_upper_eye_bag_guide_002Shape.wp" "curveShape18.cp[2]";
connectAttr "loc_rt_upper_eye_bag_guide_003Shape.wp" "curveShape18.cp[3]";
connectAttr "loc_rt_outer_eye_bag_guide_001Shape.wp" "curveShape18.cp[4]";
connectAttr "loc_rt_inner_eye_bag_guide_001Shape.wp" "curveShape19.cp[0]";
connectAttr "loc_rt_lower_eye_bag_guide_001Shape.wp" "curveShape19.cp[1]";
connectAttr "loc_rt_lower_eye_bag_guide_002Shape.wp" "curveShape19.cp[2]";
connectAttr "loc_rt_lower_eye_bag_guide_003Shape.wp" "curveShape19.cp[3]";
connectAttr "loc_rt_outer_eye_bag_guide_001Shape.wp" "curveShape19.cp[4]";
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.wp" "curveShape16.cp[0]";
connectAttr "loc_lf_upper_eye_bag_guide_001Shape.wp" "curveShape16.cp[1]";
connectAttr "loc_lf_upper_eye_bag_guide_002Shape.wp" "curveShape16.cp[2]";
connectAttr "loc_lf_upper_eye_bag_guide_003Shape.wp" "curveShape16.cp[3]";
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.wp" "curveShape16.cp[4]";
connectAttr "loc_lf_inner_eye_bag_guide_001Shape.wp" "curveShape17.cp[0]";
connectAttr "loc_lf_lower_eye_bag_guide_001Shape.wp" "curveShape17.cp[1]";
connectAttr "loc_lf_lower_eye_bag_guide_002Shape.wp" "curveShape17.cp[2]";
connectAttr "loc_lf_lower_eye_bag_guide_003Shape.wp" "curveShape17.cp[3]";
connectAttr "loc_lf_outer_eye_bag_guide_001Shape.wp" "curveShape17.cp[4]";
connectAttr "loc_md_jaw_start_guide_001Shape.wp" "curveShape20.cp[0]";
connectAttr "loc_md_jaw_end_guide_001Shape.wp" "curveShape20.cp[1]";
connectAttr "loc_lf_brow_guide_001Shape.wp" "curveShape8.cp[0]";
connectAttr "loc_lf_brow_guide_002Shape.wp" "curveShape8.cp[1]";
connectAttr "loc_lf_brow_guide_003Shape.wp" "curveShape8.cp[2]";
connectAttr "loc_lf_brow_guide_004Shape.wp" "curveShape8.cp[3]";
connectAttr "loc_lf_brow_guide_005Shape.wp" "curveShape8.cp[4]";
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
connectAttr "loc_rt_brow_guide_001Shape.wp" "curveShape9.cp[0]";
connectAttr "loc_rt_brow_guide_002Shape.wp" "curveShape9.cp[1]";
connectAttr "loc_rt_brow_guide_003Shape.wp" "curveShape9.cp[2]";
connectAttr "loc_rt_brow_guide_004Shape.wp" "curveShape9.cp[3]";
connectAttr "loc_rt_brow_guide_005Shape.wp" "curveShape9.cp[4]";
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
connectAttr "loc_lf_mouth_corner_guide_001Shape.wp" "curveShape10.cp[0]";
connectAttr "loc_lf_upper_lip_guide_002Shape.wp" "curveShape10.cp[1]";
connectAttr "loc_lf_upper_lip_guide_001Shape.wp" "curveShape10.cp[2]";
connectAttr "loc_md_upper_lip_guide_001Shape.wp" "curveShape10.cp[3]";
connectAttr "loc_rt_upper_lip_guide_001Shape.wp" "curveShape10.cp[4]";
connectAttr "loc_rt_upper_lip_guide_002Shape.wp" "curveShape10.cp[5]";
connectAttr "loc_rt_mouth_corner_guide_001Shape.wp" "curveShape10.cp[6]";
connectAttr "loc_lf_mouth_corner_guide_001Shape.wp" "curveShape11.cp[0]";
connectAttr "loc_lf_lower_lip_guide_002Shape.wp" "curveShape11.cp[1]";
connectAttr "loc_lf_lower_lip_guide_001Shape.wp" "curveShape11.cp[2]";
connectAttr "loc_md_lower_lip_guide_001Shape.wp" "curveShape11.cp[3]";
connectAttr "loc_rt_lower_lip_guide_001Shape.wp" "curveShape11.cp[4]";
connectAttr "loc_rt_lower_lip_guide_002Shape.wp" "curveShape11.cp[5]";
connectAttr "loc_rt_mouth_corner_guide_001Shape.wp" "curveShape11.cp[6]";
connectAttr "loc_md_tongue_guide_001Shape.wp" "curveShape7.cp[0]";
connectAttr "loc_md_tongue_guide_002Shape.wp" "curveShape7.cp[1]";
connectAttr "loc_md_tongue_guide_003Shape.wp" "curveShape7.cp[2]";
connectAttr "loc_md_tongue_guide_004Shape.wp" "curveShape7.cp[3]";
connectAttr "loc_md_tongue_guide_005Shape.wp" "curveShape7.cp[4]";
connectAttr "loc_lf_zygoma_guide_001Shape.wp" "curveShape22.cp[0]";
connectAttr "loc_lf_zygoma_guide_002Shape.wp" "curveShape22.cp[1]";
connectAttr "loc_lf_zygoma_guide_003Shape.wp" "curveShape22.cp[2]";
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
connectAttr "loc_rt_zygoma_guide_001Shape.wp" "curveShape23.cp[0]";
connectAttr "loc_rt_zygoma_guide_002Shape.wp" "curveShape23.cp[1]";
connectAttr "loc_rt_zygoma_guide_003Shape.wp" "curveShape23.cp[2]";
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
connectAttr "loc_lf_zygoma_guide_002Shape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "loc_rt_zygoma_guide_002Shape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "loc_rt_zygoma_guide_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "loc_rt_zygoma_guide_003.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "loc_lf_zygoma_guide_002.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "loc_rt_zygoma_guide_003Shape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "curveShape23.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr "crv_rt_zygoma_guide_001.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of face_guide.ma
