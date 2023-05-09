//Maya ASCII 2018ff09 scene
//Name: r_hand_rig.ma
//Last modified: Fri, Dec 02, 2022 02:33:01 PM
//Codeset: 936
requires maya "2018ff09";
requires "stereoCamera" "10.0";
requires "mtoa" "3.3.0.1";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201903222215-65bada0e52";
fileInfo "osv" "Microsoft Windows 8 , 64-bit  (Build 9200)\n";
createNode transform -n "r_hand_rig";
	rename -uid "06CC20B6-43EE-19F6-0F76-9BB80FD5E8B6";
	addAttr -ci true -k true -sn "presetProperties" -ln "presetProperties" -nn "Ԥ������ֵ������������" 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "mirror" -ln "mirror" -min 0 -max 1 -at "bool";
	setAttr -l on -k on ".presetProperties";
	setAttr -k on ".mirror" yes;
createNode transform -n "r_indexHand_rig" -p "r_hand_rig";
	rename -uid "3032B364-438F-11B1-05D6-53B25D513B67";
createNode joint -n "bpjnt_r_indexMetacarpal_001" -p "r_indexHand_rig";
	rename -uid "6E14A742-423B-00B3-0736-27B995D08759";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -62.1989 124.185 -2.13394 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -180 0 0 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" 0.35902336789946621 -0.90862187592510235 0.21332723195239828 0
		 0.92492742662076832 0.37697175939078337 0.049005592604314058 0 -0.12494589543801463 0.17971805477515337 0.97575096413020668 0
		 62.198863308166061 124.18541707429988 -2.133940419819528 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_indexBase_001" -p "bpjnt_r_indexMetacarpal_001";
	rename -uid "12F41C73-4DCD-D6E7-F3CD-06A59403ABA2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -13.5032 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" 0.17092896415350972 -0.98528070261028877 -0.0022861052433602036 0
		 0.97340890802255309 0.16850936641775166 0.15517632297431255 0 -0.15250700638248893 -0.028749443355713694 0.98788414427552607 0
		 67.046856366787736 111.91604148137147 0.74667692208505754 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_indexMid_001" -p "bpjnt_r_indexBase_001";
	rename -uid "2694AA98-4A1D-AC82-A399-F5B7A361D2C2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -6.3930000000000007 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.17314648283111564 -0.98333971452121094 -0.055347098646247782 0
		 0.97301691068935969 -0.17948948535242945 0.14498833111824688 0 -0.15250700638248893 -0.028749443355713694 0.98788414427552607 0
		 68.141074108971992 105.61746193750035 0.73229785221395238 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_indexTip_001" -p "bpjnt_r_indexMid_001";
	rename -uid "0AB25836-40C7-0B44-7DA4-71ACCA8EECD8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -5.002200000000002 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.22786320695131101 -0.97162341252666995 -0.063453157115249376 0
		 0.96167560638820149 -0.23477950024813754 0.14162843761448246 0 -0.15250700638248893 -0.028749443355713694 0.98788414427552607 0
		 67.209663428046255 100.7106579948172 0.44571103087159086 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_indexEnd_001" -p "bpjnt_r_indexTip_001";
	rename -uid "845A54B3-4B5B-A4CB-F025-C0957B8110E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -3.5926999999999936 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.22786320695131101 -0.97162341252666995 -0.063453157115249376 0
		 0.96167560638820149 -0.23477950024813754 0.14162843761448246 0 -0.15250700638248893 -0.028749443355713694 0.98788414427552607 0
		 66.391002928683776 97.219836818666039 0.21773831871199834 1;
	setAttr ".radi" 1.4;
createNode transform -n "r_thumbHand_rig" -p "r_hand_rig";
	rename -uid "93561C58-425A-AA61-D0D1-289526ECC9FC";
createNode joint -n "bpjnt_r_thumbMetacarpal_001" -p "r_thumbHand_rig";
	rename -uid "9D024873-42F8-2DA2-BC32-7FB372DCCF0D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -60.2408 124.534 1.96602 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -180 0 0 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.097307957165230413 -0.86858827321837218 0.48588637879637669 0
		 -0.1575752065674301 0.49549108884038684 0.85420058250682518 0 -0.98270097982426019 0.0065568671859493749 -0.18508320222306612 0
		 60.240817704314196 124.53354598947359 -1.08770432880435 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_thumbBase_001" -p "bpjnt_r_thumbMetacarpal_001";
	rename -uid "44716964-45FA-F1EB-D0EF-009943781B89";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -6.8479000000000028 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.050546679894106668 -0.9709262125099094 0.23398145869458314 0
		 -0.17816794718501219 0.23928915009642202 0.95446156823730233 0 -0.98270097982426019 0.0065568671859493749 -0.18508320222306612 0
		 59.565076760558028 118.61506342272969 2.2904769258558759 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_thumbTip_001" -p "bpjnt_r_thumbBase_001";
	rename -uid "426D5AC6-48DE-8809-E207-8384CF0BF268";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -6.6487999999999943 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" 0.013005979138804642 -0.99446232753789343 -0.10428577858249194 0
		 -0.18474206007046573 -0.10488892506180716 0.97717382519196605 0 -0.98270097982426019 0.0065568671859493749 -0.18508320222306612 0
		 59.255912424427748 112.12343969947428 3.7020118130416746 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_thumbEnd_001" -p "bpjnt_r_thumbTip_001";
	rename -uid "D33BB256-41A7-40F4-DE7F-2182779BB43A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -5.3650999999999982 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" 0.013005979138804642 -0.99446232753789343 -0.10428577858249194 0
		 -0.18474206007046573 -0.10488892506180716 0.97717382519196605 0 -0.98270097982426019 0.0065568671859493749 -0.18508320222306612 0
		 59.325691334496121 106.78800923482872 3.1425039215200181 1;
	setAttr ".radi" 1.4;
createNode transform -n "r_pinkyHand_rig" -p "r_hand_rig";
	rename -uid "3527C114-4848-9216-8754-DBA736B85861";
createNode joint -n "bpjnt_r_pinkyMetacarpal_001" -p "r_pinkyHand_rig";
	rename -uid "9AC53F83-43BB-F763-B15D-EA8D59591CEC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -62.4317 123.663 -8.6368 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -180 0 0 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" 0.10979615186857622 -0.94733909686360562 -0.30082127682147153 0
		 0.96446623908619744 0.17471524934075755 -0.19819045211796288 0 0.24031162830328898 -0.26837141651346696 0.93285963794173088 0
		 62.431723384868064 123.66251002379809 -8.636797925432667 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_pinkyBase_001" -p "bpjnt_r_pinkyMetacarpal_001";
	rename -uid "DD5E612D-45B1-5720-0B24-B6AF67FF9DA9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -11.583300000000001 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.05840763772239442 -0.97733909624124893 -0.20346213115473913 0
		 0.92280722875188514 0.024887488495246413 -0.38445732075181577 0 0.38080883185524328 -0.2102115693170519 0.9004419635414086 0
		 63.613793063000081 112.6631326675831 -12.071831240785659 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_pinkyMid_001" -p "bpjnt_r_pinkyBase_001";
	rename -uid "D83839F1-4146-4AA4-7FBC-A2BD34662D5E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -5.1727000000000061 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.25817830839272332 -0.95925762266694903 -0.1147552806228318 0
		 0.88787870492343524 -0.18877475858974194 -0.41956584210689502 0 0.38080883185524328 -0.2102115693170519 0.9004419635414086 0
		 63.311669381865492 107.60767622568279 -13.124274539752843 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_pinkyTip_001" -p "bpjnt_r_pinkyMid_001";
	rename -uid "D9C68A1F-498E-58B5-3C05-5790F2D2F24C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -2.9823999999999984 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.40318814125592461 -0.91411150404251329 -0.042889170284894015 0
		 0.83212015738812461 -0.34671494675366449 -0.43285654594330236 0 0.38080883185524328 -0.2102115693170519 0.9004419635414086 0
		 62.541672183400806 104.7467632669124 -13.466523473813441 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_pinkyEnd_001" -p "bpjnt_r_pinkyTip_001";
	rename -uid "8C76F541-4F2B-B490-8691-2584D950F853";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -3.40979999999999 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.40318814125592461 -0.91411150404251329 -0.042889170284894015 0
		 0.83212015738812461 -0.34671494675366449 -0.43285654594330236 0 0.38080883185524328 -0.2102115693170519 0.9004419635414086 0
		 61.16687139997773 101.62980350718624 -13.61276801544188 1;
	setAttr ".radi" 1.4;
createNode transform -n "r_ringHand_rig" -p "r_hand_rig";
	rename -uid "02577BAB-434C-17FB-95DB-EAAF249A710C";
createNode joint -n "bpjnt_r_ringMetacarpal_001" -p "r_ringHand_rig";
	rename -uid "4A8C90B0-4B6F-315C-6866-1E8952A30EBD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -62.329 123.719 -6.63733 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -180 0 0 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" 0.25460818500862026 -0.95316307759851837 -0.16326303816092771 0
		 0.94088514523250899 0.2831671328997421 -0.18588038714759433 0 0.2234050483033361 -0.10628509937079655 0.96891365045824585 0
		 62.328982160994137 123.71946030913374 -6.6373264676285793 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_ringBase_001" -p "bpjnt_r_ringMetacarpal_001";
	rename -uid "3C19E94D-433A-8188-82D2-0A8D2C65FCD3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -13.109000000000002 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.013588243246553226 -0.99534733749414228 -0.095388874554604652 0
		 0.94737791084369027 0.017698069086777887 -0.31962770905546312 0 0.31982878808968485 -0.094712491752256461 0.9427295954912851 0
		 65.66665232414114 111.22440260073273 -8.7775489871677923 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_ringMid_001" -p "bpjnt_r_ringBase_001";
	rename -uid "5F648CE0-429A-C903-9B6A-218C11B70E67";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -6.560299999999998 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.18107905940833 -0.98276088438586706 -0.037301720669461545 0
		 0.93001070991299728 -0.15877842431258352 -0.33146567155579676 0 0.31982878808968485 -0.094712491752256461 0.9427295954912851 0
		 65.577510385764981 104.69470096448245 -9.4033214354102839 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_ringTip_001" -p "bpjnt_r_ringMid_001";
	rename -uid "B67F169A-4C1D-8A88-D012-7897E7E6AC78";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -4.6980999999999966 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.25000331133310183 -0.96816490698185398 -0.012452197047183176 0
		 0.91389708973798955 -0.2317029494738824 -0.33332544543364223 0 0.31982878808968485 -0.094712491752256461 0.9427295954912851 0
		 64.72676897890436 100.07751679873647 -9.5785715386141526 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_ringEnd_001" -p "bpjnt_r_ringTip_001";
	rename -uid "78A3BFCF-441F-3651-FD57-CF88C1D57C2A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -3.6668999999999983 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.25000331133310183 -0.96816490698185398 -0.012452197047183176 0
		 0.91389708973798955 -0.2317029494738824 -0.33332544543364223 0 0.31982878808968485 -0.094712491752256461 0.9427295954912851 0
		 63.810045854794943 96.52740718839226 -9.6242318017453066 1;
	setAttr ".radi" 1.4;
createNode transform -n "r_middleHand_rig" -p "r_hand_rig";
	rename -uid "D5070277-4F81-C29E-1C8A-81ADD9D943CC";
createNode joint -n "bpjnt_r_middleMetacarpal_001" -p "r_middleHand_rig";
	rename -uid "B45E3C82-48FC-0D9D-A494-C19277AC43B2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -62.6308 123.78 -4.41453 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -180 0 0 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" 0.36406151137656245 -0.93136097595707612 0.0050939570567025416 0
		 0.93134886074962742 0.36408678775843817 0.0054873090047255907 0 -0.0069653079317736483 0.0027465330918168239 0.99997197012785899 0
		 62.6307976603211 123.7797196529321 -4.414525621648913 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_middleBase_001" -p "bpjnt_r_middleMetacarpal_001";
	rename -uid "1E1FF7CD-438E-66F5-F5FD-18888AD0EE58";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -13.776599999999995 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.040799413543310924 -0.99865337688975964 -0.032044354903811884 0
		 0.99170107865621293 -0.036560361468348387 -0.12325709132300545 0 0.12191955727702536 -0.036807238363985646 0.99185727237208454 0
		 67.646344239510626 110.94868915127491 -4.3443479783334205 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_middleMid_001" -p "bpjnt_r_middleBase_001";
	rename -uid "1B0A5994-4C5A-9793-30D8-AC85D4C1A1C2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -7.3187000000000069 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.15737908363727782 -0.98738678562363147 -0.017296231072793013 0
		 0.97998339046478999 -0.15398883978993239 -0.12617444920936136 0 0.12191955727702536 -0.036807238363985646 0.99185727237208454 0
		 67.323792274706506 103.64078871806117 -4.5758916854111682 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_middleTip_001" -p "bpjnt_r_middleMid_001";
	rename -uid "89FF0FDF-4DDC-D2E3-8510-C49CB77CDB07";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -4.9605999999999995 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.21251474638467396 -0.97710527371157041 -0.010137388918975926 0
		 0.96952210089426638 -0.20954835071900135 -0.12695032331000414 0 0.12191955727702536 -0.036807238363985646 0.99185727237208454 0
		 66.49573860863822 98.750208251104198 -4.6555935440076759 1;
	setAttr ".radi" 1.4;
createNode joint -n "bpjnt_r_middleEnd_001" -p "bpjnt_r_middleTip_001";
	rename -uid "38FBD1AB-4A22-55C7-A50B-15B27E90EAC4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -3.9928999999999917 0 0 ;
	setAttr -cb on ".ro";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr ".bps" -type "matrix" -0.21251474638467396 -0.97710527371157041 -0.010137388918975926 0
		 0.96952210089426638 -0.20954835071900135 -0.12695032331000414 0 0.12191955727702536 -0.036807238363985646 0.99185727237208454 0
		 65.647187274100105 94.848719069306838 -4.6960711816411536 1;
	setAttr ".radi" 1.4;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av -k on ".unw" 1;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".rm";
	setAttr -k on ".lm";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -k on ".hom";
	setAttr -k on ".hodm";
	setAttr -k on ".xry";
	setAttr -k on ".jxr";
	setAttr -k on ".sslt";
	setAttr -k on ".cbr";
	setAttr -k on ".bbr";
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
	setAttr -k on ".aofr";
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
	setAttr -k on ".mbt";
	setAttr -av -k on ".mbsof";
	setAttr -k on ".mbsc";
	setAttr -k on ".mbc";
	setAttr -k on ".mbfa";
	setAttr -k on ".mbftb";
	setAttr -k on ".mbftg";
	setAttr -k on ".mbftr";
	setAttr -k on ".mbfta";
	setAttr -k on ".mbfe";
	setAttr -k on ".mbme";
	setAttr -k on ".mbcsx";
	setAttr -k on ".mbcsy";
	setAttr -k on ".mbasx";
	setAttr -k on ".mbasy";
	setAttr -av -k on ".blen";
	setAttr -k on ".blth";
	setAttr -k on ".blfr";
	setAttr -k on ".blfa";
	setAttr -av -k on ".blat";
	setAttr -av -k on ".msaa";
	setAttr -av -k on ".aasc";
	setAttr -k on ".aasq";
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
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
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
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".ai_override";
	setAttr -cb on ".rsMaterialId";
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
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".ai_override";
	setAttr -cb on ".rsMaterialId";
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
	setAttr -av -k on ".an";
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
	setAttr -av -k on ".peie";
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
	setAttr -av -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -cb on ".isu";
	setAttr -av -cb on ".pdu";
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
select -ne :ikSystem;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".gsn";
	setAttr -k on ".gsv";
	setAttr -s 4 ".sol";
connectAttr "bpjnt_r_indexMetacarpal_001.s" "bpjnt_r_indexBase_001.is";
connectAttr "bpjnt_r_indexBase_001.s" "bpjnt_r_indexMid_001.is";
connectAttr "bpjnt_r_indexMid_001.s" "bpjnt_r_indexTip_001.is";
connectAttr "bpjnt_r_indexTip_001.s" "bpjnt_r_indexEnd_001.is";
connectAttr "bpjnt_r_thumbMetacarpal_001.s" "bpjnt_r_thumbBase_001.is";
connectAttr "bpjnt_r_thumbBase_001.s" "bpjnt_r_thumbTip_001.is";
connectAttr "bpjnt_r_thumbTip_001.s" "bpjnt_r_thumbEnd_001.is";
connectAttr "bpjnt_r_pinkyMetacarpal_001.s" "bpjnt_r_pinkyBase_001.is";
connectAttr "bpjnt_r_pinkyBase_001.s" "bpjnt_r_pinkyMid_001.is";
connectAttr "bpjnt_r_pinkyMid_001.s" "bpjnt_r_pinkyTip_001.is";
connectAttr "bpjnt_r_pinkyTip_001.s" "bpjnt_r_pinkyEnd_001.is";
connectAttr "bpjnt_r_ringMetacarpal_001.s" "bpjnt_r_ringBase_001.is";
connectAttr "bpjnt_r_ringBase_001.s" "bpjnt_r_ringMid_001.is";
connectAttr "bpjnt_r_ringMid_001.s" "bpjnt_r_ringTip_001.is";
connectAttr "bpjnt_r_ringTip_001.s" "bpjnt_r_ringEnd_001.is";
connectAttr "bpjnt_r_middleMetacarpal_001.s" "bpjnt_r_middleBase_001.is";
connectAttr "bpjnt_r_middleBase_001.s" "bpjnt_r_middleMid_001.is";
connectAttr "bpjnt_r_middleMid_001.s" "bpjnt_r_middleTip_001.is";
connectAttr "bpjnt_r_middleTip_001.s" "bpjnt_r_middleEnd_001.is";
// End of r_hand_rig.ma