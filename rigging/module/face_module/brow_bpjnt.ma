//Maya ASCII 2023 scene
//Name: brow_bpjnt.ma
//Last modified: Wed, May 17, 2023 01:59:29 PM
//Codeset: 936
requires maya "2023";
requires "stereoCamera" "10.0";
requires "mtoa" "5.2.2.3";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2023";
fileInfo "version" "2023";
fileInfo "cutIdentifier" "202211021031-847a9f9623";
fileInfo "osv" "Windows 10 Pro for Workstations v2009 (Build: 19044)";
fileInfo "UUID" "0293D2BD-4BDF-FE68-BFF5-7B8C5AC6E1D3";
createNode transform -n "bpjnt_r_BrowJnt_001";
	rename -uid "52186E92-4A71-7972-EE56-B2BF33680852";
createNode joint -n "bpjnt_r_Brow_001" -p "bpjnt_r_BrowJnt_001";
	rename -uid "C820C2FF-4177-212F-BB19-BFB59766F051";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.54816741153675108;
createNode transform -n "bpctrl_r_Brow_001" -p "bpjnt_r_Brow_001";
	rename -uid "7AD2BB81-420E-E764-E5BD-26B6D8307198";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.1102230246251565e-16 0 -2.2204460492503131e-15 ;
	setAttr ".sp" -type "double3" 0 0 -1.7763568394002505e-15 ;
createNode nurbsCurve -n "bpctrl_r_Brow_001Shape" -p "bpctrl_r_Brow_001";
	rename -uid "38315E4D-4A72-542C-8730-D6869DA079DF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.086279960977347525 0.20829825195253449 -1.7763568394002505e-15
		1.6653345369377348e-16 0.22546040324796479 -1.7763568394002505e-15
		-0.086279960977347414 0.20829825195253449 -1.7763568394002505e-15
		-0.15942458002568771 0.15942458002569282 -1.7763568394002505e-15
		-0.20829825195253371 0.086279960977350356 -1.7763568394002505e-15
		-0.22546040324796257 0 -1.7763568394002505e-15
		-0.20829825195253371 -0.086279960977350356 -1.7763568394002505e-15
		-0.15942458002568771 -0.15942458002568571 -1.7763568394002505e-15
		-0.086279960977347414 -0.20829825195252738 -1.7763568394002505e-15
		1.1102230246251565e-16 -0.22546040324795769 -1.7763568394002505e-15
		0.086279960977347747 -0.20829825195252738 -1.7763568394002505e-15
		0.15942458002568788 -0.15942458002568571 -1.7763568394002505e-15
		0.20829825195253399 -0.086279960977343251 -1.7763568394002505e-15
		0.22546040324796265 0 -1.7763568394002505e-15
		0.20829825195253385 0.086279960977350356 -1.7763568394002505e-15
		0.15942458002568788 0.15942458002569282 -1.7763568394002505e-15
		0.086279960977347525 0.20829825195253449 -1.7763568394002505e-15
		;
createNode joint -n "bpjnt_r_Brow_002" -p "bpjnt_r_BrowJnt_001";
	rename -uid "CAF4CE91-4946-372C-FD0F-EC9F3C643584";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.54131012972560655;
createNode transform -n "bpctrl_r_Brow_002" -p "bpjnt_r_Brow_002";
	rename -uid "8E2A13A1-4D92-0133-EC3D-4AB6ED5EE677";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 5.5511151231257827e-17 7.1054273576010019e-15 8.8817841970012523e-16 ;
	setAttr ".sp" -type "double3" 5.5511151231257827e-17 7.1054273576010019e-15 8.8817841970012523e-16 ;
createNode nurbsCurve -n "bpctrl_r_Brow_002Shape" -p "bpctrl_r_Brow_002";
	rename -uid "A63682CB-4A14-6763-1B4E-8AA0BEBF9334";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.12145183876619911 0.12147764490230345 0.0025038113584364696
		-0.12145183876619911 -0.12147764490229492 0.0025038113584364696
		0.12145183876619935 -0.12147764490229492 -0.0025038113584365806
		0.12145183876619935 0.12147764490230345 -0.0025038113584365806
		-0.12145183876619911 0.12147764490230345 0.0025038113584364696
		;
createNode joint -n "bpjnt_r_Brow_003" -p "bpjnt_r_BrowJnt_001";
	rename -uid "6738DDE4-4498-8ED2-D957-10A86387C96A";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.52839033437406968;
createNode transform -n "bpctrl_r_Brow_003" -p "bpjnt_r_Brow_003";
	rename -uid "E3A91F5C-4241-87E9-E83E-5E81CDC2517D";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 2.2204460492503131e-16 -1.4210854715202004e-14 -4.4408920985006262e-16 ;
	setAttr ".sp" -type "double3" 2.2204460492503131e-16 -1.4210854715202004e-14 -4.4408920985006262e-16 ;
createNode nurbsCurve -n "bpctrl_r_Brow_003Shape" -p "bpctrl_r_Brow_003";
	rename -uid "14A86D40-4A14-6005-556E-34B5508811CA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.094244076100422194 0.094482612701770566 0.0067095620523231203
		-0.094244076100422416 -0.094482612701804677 0.0067095620523235644
		0.094244076100422916 -0.094482612701804677 -0.0067095620523263677
		0.094244076100422916 0.094482612701770566 -0.0067095620523263677
		-0.094244076100422194 0.094482612701770566 0.0067095620523231203
		;
createNode joint -n "bpjnt_r_Brow_004" -p "bpjnt_r_BrowJnt_001";
	rename -uid "2D91CB89-4A7F-7A46-7CBC-EFAFF84789A9";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.52326743915106277;
createNode transform -n "bpctrl_r_Brow_004" -p "bpjnt_r_Brow_004";
	rename -uid "AF1C86EB-42D1-6C41-5315-40964911FAF7";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.2204460492503131e-16 3.5527136788005009e-14 8.8817841970012523e-16 ;
	setAttr ".sp" -type "double3" 0 2.8421709430404007e-14 8.8817841970012523e-16 ;
createNode nurbsCurve -n "bpctrl_r_Brow_004Shape" -p "bpctrl_r_Brow_004";
	rename -uid "60FF7174-43B3-188C-D8C0-F288426834FA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.086028866763561807 0.20829825195256291 -0.0065776705321833884
		-1.1102230246251565e-16 0.22546040324798611 6.6613381477509392e-16
		0.086028866763561584 0.20829825195256291 0.0065776705321849427
		0.15896061841599018 0.15942458002571414 0.012153950352575826
		0.20769205689617842 0.086279960977371672 0.015879901407621633
		0.22480426244710783 2.8421709430404007e-14 0.017188281425021934
		0.20769205689617842 -0.086279960977321934 0.015879901407621633
		0.15896061841599018 -0.1594245800256644 0.012153950352575826
		0.086028866763561584 -0.20829825195250606 0.0065776705321849427
		-1.1102230246251565e-16 -0.22546040324793637 6.6613381477509392e-16
		-0.086028866763561918 -0.20829825195250606 -0.0065776705321836104
		-0.15896061841599018 -0.1594245800256644 -0.012153950352574494
		-0.20769205689617865 -0.086279960977321934 -0.015879901407620522
		-0.22480426244710783 2.8421709430404007e-14 -0.017188281425020602
		-0.20769205689617853 0.086279960977371672 -0.015879901407620078
		-0.15896061841599018 0.15942458002571414 -0.012153950352574494
		-0.086028866763561807 0.20829825195256291 -0.0065776705321833884
		;
createNode transform -n "bpjnt_l_BrowJnt_001";
	rename -uid "C062B142-4689-B3CE-55C8-F8872EE3AC41";
createNode joint -n "bpjnt_l_Brow_001" -p "bpjnt_l_BrowJnt_001";
	rename -uid "F6569858-471E-E711-F697-3B8CDA4E92E8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.19919462502002716 32.955272674560547 2.1782350540161133 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.19919462502002716 32.955272674560547 2.1782350540161133 1;
	setAttr ".radi" 0.54816741153675108;
createNode transform -n "bpctrl_l_Brow_001" -p "bpjnt_l_Brow_001";
	rename -uid "73773AFB-4F62-6F16-DCC5-D7B716230603";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 -7.1054273576010019e-15 -8.8817841970012523e-16 ;
	setAttr ".sp" -type "double3" 0 0 -8.8817841970012523e-16 ;
createNode nurbsCurve -n "bpctrl_l_Brow_001Shape" -p "bpctrl_l_Brow_001";
	rename -uid "24CF4563-45CF-FA57-3575-13A5E4020BCE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.086279960977347581 0.20829825195254159 -2.2204460492503131e-16
		1.6653345369377348e-16 0.2254604032479719 -4.4408920985006262e-16
		-0.08627996097734747 0.20829825195254159 -6.6613381477509392e-16
		-0.15942458002568777 0.15942458002569282 -6.6613381477509392e-16
		-0.20829825195253365 0.086279960977350356 -6.6613381477509392e-16
		-0.22546040324796249 0 -6.6613381477509392e-16
		-0.2082982519525336 -0.086279960977350356 -6.6613381477509392e-16
		-0.15942458002568777 -0.15942458002567861 -6.6613381477509392e-16
		-0.086279960977347414 -0.20829825195252738 -6.6613381477509392e-16
		1.1102230246251565e-16 -0.22546040324795058 -4.4408920985006262e-16
		0.086279960977347692 -0.20829825195252738 -2.2204460492503131e-16
		0.15942458002568782 -0.15942458002567861 -2.2204460492503131e-16
		0.20829825195253393 -0.08627996097732904 -2.2204460492503131e-16
		0.22546040324796246 1.4210854715202004e-14 -2.2204460492503131e-16
		0.20829825195253382 0.086279960977364567 -2.2204460492503131e-16
		0.15942458002568782 0.15942458002569992 -2.2204460492503131e-16
		0.086279960977347581 0.20829825195254159 -2.2204460492503131e-16
		;
createNode joint -n "bpjnt_l_Brow_002" -p "bpjnt_l_BrowJnt_001";
	rename -uid "25A03B60-4BE9-C711-D712-56A4B46C91DD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.48069290145496241 33.022665506379518 2.1441271252247365 ;
	setAttr ".r" -type "double3" 0 19.129160836124342 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.94478225137692962 0 -0.32769879078681408 0 0 1 0 0
		 0.32769879078681408 0 0.94478225137692962 0 0.48069290145496241 33.022665506379518 2.1441271252247365 1;
	setAttr ".radi" 0.54131012972560655;
createNode transform -n "bpctrl_l_Brow_002" -p "bpjnt_l_Brow_002";
	rename -uid "2570587D-4F9A-9FE5-DBDC-3DA6278DB276";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 1.6653345369377348e-16 0 0 ;
	setAttr ".sp" -type "double3" 1.6653345369377348e-16 0 0 ;
createNode nurbsCurve -n "bpctrl_l_Brow_002Shape" -p "bpctrl_l_Brow_002";
	rename -uid "A51E1498-49F0-F81C-5B81-84A795BBC158";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.12200261122293701 0.12087118407460486 0.0043767724647749695
		-0.12090517849354002 -0.12204710246257593 0.0002810977607763665
		0.12200261122293762 -0.12087118407458776 -0.0043767724647764128
		0.12090517849354065 0.12204710246259302 -0.00028109776077783755
		-0.12200261122293701 0.12087118407460486 0.0043767724647749695
		;
createNode joint -n "bpjnt_l_Brow_003" -p "bpjnt_l_BrowJnt_001";
	rename -uid "A4FC6E5A-48E1-C670-9492-C8A39EA882FA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.76909813658598547 33.017352660330893 2.0081801459216706 ;
	setAttr ".r" -type "double3" 0 29.319538085954999 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.87190234039259185 0 -0.48967980233814096 0 0 1 0 0
		 0.48967980233814096 0 0.87190234039259185 0 0.76909813658598547 33.017352660330893 2.0081801459216706 1;
	setAttr ".radi" 0.52839033437406968;
createNode transform -n "bpctrl_l_Brow_003" -p "bpjnt_l_Brow_003";
	rename -uid "D36E55E6-42C2-8014-AB0C-628BCA472A32";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -2.2204460492503131e-16 -7.1054273576010019e-15 0 ;
	setAttr ".sp" -type "double3" -2.2204460492503131e-16 -7.1054273576010019e-15 0 ;
createNode nurbsCurve -n "bpctrl_l_Brow_003Shape" -p "bpctrl_l_Brow_003";
	rename -uid "F6249C85-48FD-5B26-539C-6A85581324D9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-0.094369382149874503 0.094482612701800431 0.0046242637908458506
		-0.094369382149874503 -0.094482612701774826 0.0046242637908458506
		0.094369382149873948 -0.094482612701774826 -0.004624263790845462
		0.094369382149873948 0.094482612701800431 -0.004624263790845462
		-0.094369382149874503 0.094482612701800431 0.0046242637908458506
		;
createNode joint -n "bpjnt_l_Brow_004" -p "bpjnt_l_BrowJnt_001";
	rename -uid "188E31C8-414F-A910-43BA-47A42A376A30";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0180069049165605 32.932854891936728 1.7790202827492114 ;
	setAttr ".r" -type "double3" 0 52.06043014383431 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 0.61483001418402605 0 -0.78865965641616931 0 0 1 0 0
		 0.78865965641616931 0 0.61483001418402605 0 1.0180069049165605 32.932854891936728 1.7790202827492114 1;
	setAttr ".radi" 0.52326743915106277;
createNode transform -n "bpctrl_l_Brow_004" -p "bpjnt_l_Brow_004";
	rename -uid "6C92D4D9-4744-D96D-6632-20B362C15540";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" -6.6613381477509392e-16 0 -2.6645352591003757e-15 ;
	setAttr ".sp" -type "double3" -2.2204460492503131e-16 0 -2.6645352591003757e-15 ;
createNode nurbsCurve -n "bpctrl_l_Brow_004Shape" -p "bpctrl_l_Brow_004";
	rename -uid "351E7576-4594-5264-4B6A-819E6464B201";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.08624608582315163 0.20829825195252738 0.0024175083119084562
		2.2204460492503131e-16 0.22546040324795058 -2.4424906541753444e-15
		-0.086246085823151741 0.20829825195252738 -0.0024175083119140073
		-0.15936198690244352 0.15942458002567861 -0.0044669728981046042
		-0.20821647009584676 0.086279960977343251 -0.0058363813537687381
		-0.22537188320415924 0 -0.0063172536552507097
		-0.20821647009584676 -0.086279960977350356 -0.0058363813537687381
		-0.15936198690244374 -0.15942458002569992 -0.0044669728981046042
		-0.086246085823151741 -0.20829825195253449 -0.0024175083119140073
		2.2204460492503131e-16 -0.22546040324796479 -2.4424906541753444e-15
		0.086246085823151852 -0.20829825195253449 0.0024175083119084562
		0.15936198690244374 -0.15942458002569992 0.004466972898098831
		0.20821647009584687 -0.086279960977350356 0.0058363813537636311
		0.22537188320415924 0 0.0063172536552458247
		0.20821647009584676 0.086279960977343251 0.005836381353763187
		0.15936198690244363 0.15942458002567861 0.004466972898098831
		0.08624608582315163 0.20829825195252738 0.0024175083119084562
		;
createNode joint -n "bpjnt_m_Brow_001";
	rename -uid "13810C1E-4FC4-BA28-0B4F-8192B940817B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.5361250049750197e-09 32.949718475341797 2.1906836032867432 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.19919462502002716 32.955272674560547 2.1782350540161133 1;
	setAttr ".radi" 0.54816741153675108;
createNode transform -n "bpctrl_m_Brow_001" -p "bpjnt_m_Brow_001";
	rename -uid "AE6E4B83-4E60-6751-A8C7-2192DC6398B2";
	setAttr -l on ".ro";
	setAttr ".rp" -type "double3" 0 -7.1054273576010019e-15 -8.8817841970012523e-16 ;
	setAttr ".sp" -type "double3" 0 0 -8.8817841970012523e-16 ;
createNode nurbsCurve -n "bpctrl_m_Brow_001Shape" -p "bpctrl_m_Brow_001";
	rename -uid "CC00177F-4D13-1511-277B-3DA3869070A0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		0.086279960977347581 0.20829825195254159 -2.2204460492503131e-16
		1.6653345369377348e-16 0.2254604032479719 -4.4408920985006262e-16
		-0.08627996097734747 0.20829825195254159 -6.6613381477509392e-16
		-0.15942458002568777 0.15942458002569282 -6.6613381477509392e-16
		-0.20829825195253365 0.086279960977350356 -6.6613381477509392e-16
		-0.22546040324796249 0 -6.6613381477509392e-16
		-0.2082982519525336 -0.086279960977350356 -6.6613381477509392e-16
		-0.15942458002568777 -0.15942458002567861 -6.6613381477509392e-16
		-0.086279960977347414 -0.20829825195252738 -6.6613381477509392e-16
		1.1102230246251565e-16 -0.22546040324795058 -4.4408920985006262e-16
		0.086279960977347692 -0.20829825195252738 -2.2204460492503131e-16
		0.15942458002568782 -0.15942458002567861 -2.2204460492503131e-16
		0.20829825195253393 -0.08627996097732904 -2.2204460492503131e-16
		0.22546040324796246 1.4210854715202004e-14 -2.2204460492503131e-16
		0.20829825195253382 0.086279960977364567 -2.2204460492503131e-16
		0.15942458002568782 0.15942458002569992 -2.2204460492503131e-16
		0.086279960977347581 0.20829825195254159 -2.2204460492503131e-16
		;
createNode multiplyDivide -n "transjnt_l_Brow_001";
	rename -uid "D4464A72-451B-D322-E39A-798300125A9F";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion2";
	rename -uid "61B71CF2-464E-AB53-0D66-2ABB56387CC8";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatejnt_l_Brow_001";
	rename -uid "F4B96734-4E38-2D02-62C9-0B87CA6AD512";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion1";
	rename -uid "2EEB2B08-4EBF-3FED-CCC8-3CAC92A1C4B7";
	setAttr ".cf" 57.295779513082323;
createNode displayLayer -n "bp_r_Brow";
	rename -uid "75377EAA-4F06-42CE-2E1A-7F946560B3A3";
	setAttr ".c" 13;
	setAttr ".ufem" -type "stringArray" 0  ;
	setAttr ".do" 2;
createNode displayLayerManager -n "layerManager";
	rename -uid "F0123D22-4D6E-76C6-4651-56A7249A09A7";
	setAttr ".cdl" 4;
	setAttr -s 5 ".dli[1:5]"  1 2 0 3 4;
	setAttr -s 4 ".dli";
createNode multiplyDivide -n "transctrl_l_Brow_001";
	rename -uid "7592FE90-45AB-CB0A-1469-91A0C2600CDD";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion4";
	rename -uid "33F992F0-4387-9F70-D173-31B4CBFB5A02";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatectrl_l_Brow_001";
	rename -uid "65B8781C-48C7-B085-09AC-16AB5B3CFAB8";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion3";
	rename -uid "596A1E15-42C7-FE9D-AC53-89BF3120C199";
	setAttr ".cf" 57.295779513082323;
createNode multiplyDivide -n "transjnt_l_Brow_002";
	rename -uid "06F062AF-4D3D-F9FD-DD9A-CF87A286E1B1";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion6";
	rename -uid "7B178F54-4097-8DE7-DCCD-FCB761A01022";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatejnt_l_Brow_002";
	rename -uid "1372E79A-4A82-541C-2AD8-06AF5600DFF9";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion5";
	rename -uid "0405FE95-4DC7-AF8D-F184-34A28C60A6CA";
	setAttr ".cf" 57.295779513082323;
createNode multiplyDivide -n "transctrl_l_Brow_002";
	rename -uid "84969906-4219-35A5-3D2B-4FAC562C3602";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion8";
	rename -uid "A6A02FF7-422C-76FA-EE36-66A7203C3158";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatectrl_l_Brow_002";
	rename -uid "60168511-478A-9AE9-C3DB-1089ADE2A6EA";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion7";
	rename -uid "B35ABC82-4DF0-2E1F-4625-20B803097B6C";
	setAttr ".cf" 57.295779513082323;
createNode multiplyDivide -n "transjnt_l_Brow_003";
	rename -uid "64C2F203-4227-FFA2-56D8-2DBC79A08A2F";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion10";
	rename -uid "59BB6A01-49E1-8CAD-0B69-8EB34C1E56A1";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatejnt_l_Brow_003";
	rename -uid "333B3A80-4778-E17C-81C1-0391D55B5CF9";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion9";
	rename -uid "A9F219B0-4FFF-128C-5B75-32A691868B1B";
	setAttr ".cf" 57.295779513082323;
createNode multiplyDivide -n "transctrl_l_Brow_003";
	rename -uid "E929C970-49DD-C9F4-DA90-7791FBC5B094";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion12";
	rename -uid "0784CAD5-4CC5-D283-5033-1F9DE9DA8E90";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatectrl_l_Brow_003";
	rename -uid "64C51F8E-4652-271E-A2F0-57AFD0494C8C";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion11";
	rename -uid "7AA137CB-4926-A683-E85D-62B3727E0E4E";
	setAttr ".cf" 57.295779513082323;
createNode multiplyDivide -n "transjnt_l_Brow_004";
	rename -uid "379BEF4E-4C7B-CCCF-60C1-5E89BABD44CA";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion14";
	rename -uid "E85A3579-46CA-0621-9BAD-6383BC91B960";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatejnt_l_Brow_004";
	rename -uid "3E14868F-4F44-38C7-A2E6-F6BDB4946464";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion13";
	rename -uid "3A778EC1-4332-2A24-FF1A-DA97DC276067";
	setAttr ".cf" 57.295779513082323;
createNode multiplyDivide -n "transctrl_l_Brow_004";
	rename -uid "8E162AF5-4DFC-59F4-526D-1C96EC9D7600";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode unitConversion -n "unitConversion16";
	rename -uid "165660DB-4B57-3D42-A483-57BFCC6B8571";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "rotatectrl_l_Brow_004";
	rename -uid "D6046C4E-4806-9DA0-663E-9BA42DD3C4A7";
	setAttr ".i2" -type "float3" 1 -1 -1 ;
createNode unitConversion -n "unitConversion15";
	rename -uid "7AAF5CA6-4693-9ABC-C514-D99A7A358153";
	setAttr ".cf" 57.295779513082323;
createNode displayLayer -n "bp_l_Brow";
	rename -uid "12A9D453-4F6C-EBA7-B565-C4BCE41FB14F";
	setAttr ".c" 6;
	setAttr ".ufem" -type "stringArray" 0  ;
	setAttr ".do" 1;
createNode displayLayer -n "bp_m_Brow";
	rename -uid "283426EA-4044-37DD-C2D8-A7A8FF86565F";
	setAttr ".c" 17;
	setAttr ".ufem" -type "stringArray" 0  ;
	setAttr ".do" 3;
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
	setAttr -av ".ta" 5;
	setAttr -av -k on ".tq" 1;
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
	setAttr -s 11 ".st";
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
	setAttr -s 14 ".s";
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
	setAttr -s 4 ".sol";
connectAttr "transjnt_l_Brow_001.o" "bpjnt_r_Brow_001.t";
connectAttr "unitConversion2.o" "bpjnt_r_Brow_001.r";
connectAttr "bp_r_Brow.di" "bpjnt_r_Brow_001.do";
connectAttr "transctrl_l_Brow_001.o" "bpctrl_r_Brow_001.t";
connectAttr "unitConversion4.o" "bpctrl_r_Brow_001.r";
connectAttr "bp_r_Brow.di" "bpctrl_r_Brow_001.do";
connectAttr "transjnt_l_Brow_002.o" "bpjnt_r_Brow_002.t";
connectAttr "unitConversion6.o" "bpjnt_r_Brow_002.r";
connectAttr "bp_r_Brow.di" "bpjnt_r_Brow_002.do";
connectAttr "transctrl_l_Brow_002.o" "bpctrl_r_Brow_002.t";
connectAttr "unitConversion8.o" "bpctrl_r_Brow_002.r";
connectAttr "bp_r_Brow.di" "bpctrl_r_Brow_002.do";
connectAttr "transjnt_l_Brow_003.o" "bpjnt_r_Brow_003.t";
connectAttr "unitConversion10.o" "bpjnt_r_Brow_003.r";
connectAttr "bp_r_Brow.di" "bpjnt_r_Brow_003.do";
connectAttr "transctrl_l_Brow_003.o" "bpctrl_r_Brow_003.t";
connectAttr "unitConversion12.o" "bpctrl_r_Brow_003.r";
connectAttr "bp_r_Brow.di" "bpctrl_r_Brow_003.do";
connectAttr "transjnt_l_Brow_004.o" "bpjnt_r_Brow_004.t";
connectAttr "unitConversion14.o" "bpjnt_r_Brow_004.r";
connectAttr "bp_r_Brow.di" "bpjnt_r_Brow_004.do";
connectAttr "transctrl_l_Brow_004.o" "bpctrl_r_Brow_004.t";
connectAttr "unitConversion16.o" "bpctrl_r_Brow_004.r";
connectAttr "bp_r_Brow.di" "bpctrl_r_Brow_004.do";
connectAttr "bp_l_Brow.di" "bpjnt_l_Brow_001.do";
connectAttr "bp_l_Brow.di" "bpctrl_l_Brow_001.do";
connectAttr "bp_l_Brow.di" "bpjnt_l_Brow_002.do";
connectAttr "bp_l_Brow.di" "bpctrl_l_Brow_002.do";
connectAttr "bp_l_Brow.di" "bpjnt_l_Brow_003.do";
connectAttr "bp_l_Brow.di" "bpctrl_l_Brow_003.do";
connectAttr "bp_l_Brow.di" "bpjnt_l_Brow_004.do";
connectAttr "bp_l_Brow.di" "bpctrl_l_Brow_004.do";
connectAttr "bp_m_Brow.di" "bpjnt_m_Brow_001.do";
connectAttr "bp_m_Brow.di" "bpctrl_m_Brow_001.do";
connectAttr "bpjnt_l_Brow_001.t" "transjnt_l_Brow_001.i1";
connectAttr "rotatejnt_l_Brow_001.o" "unitConversion2.i";
connectAttr "unitConversion1.o" "rotatejnt_l_Brow_001.i1";
connectAttr "bpjnt_l_Brow_001.r" "unitConversion1.i";
connectAttr "layerManager.dli[4]" "bp_r_Brow.id";
connectAttr "bpctrl_l_Brow_001.t" "transctrl_l_Brow_001.i1";
connectAttr "rotatectrl_l_Brow_001.o" "unitConversion4.i";
connectAttr "unitConversion3.o" "rotatectrl_l_Brow_001.i1";
connectAttr "bpctrl_l_Brow_001.r" "unitConversion3.i";
connectAttr "bpjnt_l_Brow_002.t" "transjnt_l_Brow_002.i1";
connectAttr "rotatejnt_l_Brow_002.o" "unitConversion6.i";
connectAttr "unitConversion5.o" "rotatejnt_l_Brow_002.i1";
connectAttr "bpjnt_l_Brow_002.r" "unitConversion5.i";
connectAttr "bpctrl_l_Brow_002.t" "transctrl_l_Brow_002.i1";
connectAttr "rotatectrl_l_Brow_002.o" "unitConversion8.i";
connectAttr "unitConversion7.o" "rotatectrl_l_Brow_002.i1";
connectAttr "bpctrl_l_Brow_002.r" "unitConversion7.i";
connectAttr "bpjnt_l_Brow_003.t" "transjnt_l_Brow_003.i1";
connectAttr "rotatejnt_l_Brow_003.o" "unitConversion10.i";
connectAttr "unitConversion9.o" "rotatejnt_l_Brow_003.i1";
connectAttr "bpjnt_l_Brow_003.r" "unitConversion9.i";
connectAttr "bpctrl_l_Brow_003.t" "transctrl_l_Brow_003.i1";
connectAttr "rotatectrl_l_Brow_003.o" "unitConversion12.i";
connectAttr "unitConversion11.o" "rotatectrl_l_Brow_003.i1";
connectAttr "bpctrl_l_Brow_003.r" "unitConversion11.i";
connectAttr "bpjnt_l_Brow_004.t" "transjnt_l_Brow_004.i1";
connectAttr "rotatejnt_l_Brow_004.o" "unitConversion14.i";
connectAttr "unitConversion13.o" "rotatejnt_l_Brow_004.i1";
connectAttr "bpjnt_l_Brow_004.r" "unitConversion13.i";
connectAttr "bpctrl_l_Brow_004.t" "transctrl_l_Brow_004.i1";
connectAttr "rotatectrl_l_Brow_004.o" "unitConversion16.i";
connectAttr "unitConversion15.o" "rotatectrl_l_Brow_004.i1";
connectAttr "bpctrl_l_Brow_004.r" "unitConversion15.i";
connectAttr "layerManager.dli[2]" "bp_l_Brow.id";
connectAttr "layerManager.dli[5]" "bp_m_Brow.id";
dataStructure -fmt "raw" -as "name=notes_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=faceConnectMarkerStructure:bool=faceConnectMarker:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=notes_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_ground:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane2:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane5:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchF_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left1:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=mapManager_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchDegraded_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesMountainsGrass_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_mountains_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseLeaves:string=value";
dataStructure -fmt "raw" -as "name=notes_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_slopes_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_left:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatt:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchC_parShape:string=value";
dataStructure -fmt "raw" -as "name=faceConnectOutputStructure:bool=faceConnectOutput:string[200]=faceConnectOutputAttributes:string[200]=faceConnectOutputGroups";
dataStructure -fmt "raw" -as "name=mapManager_polySurface56:string=value";
dataStructure -fmt "raw" -as "name=notes_left_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchH_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_baseScatter:string=value";
dataStructure -fmt "raw" -as "name=notes_base_left:string=value";
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
dataStructure -fmt "raw" -as "name=mapManager_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_floor:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane3:string=value";
dataStructure -fmt "raw" -as "name=notes_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane1:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassesCenter_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_juneBackYard:string=value";
dataStructure -fmt "raw" -as "name=notes_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_pPlane4:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchE_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grassBase:string=value";
dataStructure -fmt "raw" -as "name=notes_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_groundD_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_trees_left:string=value";
dataStructure -fmt "raw" -as "name=notes_grassJuneBackYard_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassA_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_right_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_groundC_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_base_hojas:string=value";
dataStructure -fmt "raw" -as "name=notes_decayGrassPatchA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_base_right:string=value";
dataStructure -fmt "raw" -as "name=notes_groundA_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeaves_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_groundWoods_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=mapManager_degraded:string=value";
dataStructure -fmt "raw" -as "name=notes_ferns_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=notes_floorOrangeConcrete_c_geo:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_pPlane6:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassD_Combined:string=value";
dataStructure -fmt "raw" -as "name=mapManager_suelo:string=value";
dataStructure -fmt "raw" -as "name=notes_bushes_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_snapshot_CombinedGrass:string=value";
dataStructure -fmt "raw" -as "name=mapManager_slopesGroundGrassB_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_groundB_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_slopesGroundGrassC_Combined:string=value";
dataStructure -fmt "raw" -as "name=notes_wildPatchG_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_ground_c_geo:string=value";
dataStructure -fmt "raw" -as "name=mapManager_grass_c_geo1:string=value";
dataStructure -fmt "raw" -as "name=notes_decayLeavesCarousel_parShape:string=value";
dataStructure -fmt "raw" -as "name=notes_widlPatchB_parShape:string=value";
dataStructure -fmt "raw" -as "name=mapManager_baseScatter:string=value";
// End of brow_bpjnt.ma
