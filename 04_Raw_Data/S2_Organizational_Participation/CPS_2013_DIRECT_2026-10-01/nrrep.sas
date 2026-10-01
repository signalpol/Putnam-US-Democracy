/* 
This code is for documentation of the record layout for the 
ASCII NR replicate weight code for the 2013 Civic Engagement. 
*/

filename ipfile "/cpspb/supp/data/nov13/nov13nrrep.dat";

%let replist=CPS_CIVENG_NRREPWGT_NOV13.LST ;

filename replist  "&replist";

*Add SAS library;
libname sas '.';


data rep_nov13;

infile ipfile lrecl = 1617      recfm = v ;
input 

qstnum 1-5
occurnum 6-7

repwgt0  8 -17
repwgt1  18 -27
repwgt2  28 -37
repwgt3  38 -47
repwgt4  48 -57
repwgt5  58 -67
repwgt6  68 -77
repwgt7  78 -87
repwgt8  88 -97
repwgt9  98 -107
repwgt10  108 -117
repwgt11  118 -127
repwgt12  128 -137
repwgt13  138 -147
repwgt14  148 -157
repwgt15  158 -167
repwgt16  168 -177
repwgt17  178 -187
repwgt18  188 -197
repwgt19  198 -207
repwgt20  208 -217
repwgt21  218 -227
repwgt22  228 -237
repwgt23  238 -247
repwgt24  248 -257
repwgt25  258 -267
repwgt26  268 -277
repwgt27  278 -287
repwgt28  288 -297
repwgt29  298 -307
repwgt30  308 -317
repwgt31  318 -327
repwgt32  328 -337
repwgt33  338 -347
repwgt34  348 -357
repwgt35  358 -367
repwgt36  368 -377
repwgt37  378 -387
repwgt38  388 -397
repwgt39  399 -407
repwgt40  408 -417
repwgt41  418 -427
repwgt42  428 -437
repwgt43  438 -447
repwgt44  448 -457
repwgt45  458 -467
repwgt46  468 -477
repwgt47  478 -487
repwgt48  488 -497
repwgt49  498 -507
repwgt50  508 -517
repwgt51  518 -527
repwgt52  528 -537
repwgt53  538 -547
repwgt54  548 -557
repwgt55  558 -567
repwgt56  568 -577
repwgt57  578 -587
repwgt58  588 -597
repwgt59  598 -607
repwgt60  608 -617
repwgt61  618 -627
repwgt62  628 -637
repwgt63  638 -647
repwgt64  648 -657
repwgt65  658 -667
repwgt66  668 -677
repwgt67  678 -687
repwgt68  688 -697
repwgt69  699 -707
repwgt70  708 -717
repwgt71  718 -727
repwgt72  728 -737
repwgt73  738 -747
repwgt74  748 -757
repwgt75  758 -767
repwgt76  768 -777
repwgt77  778 -787
repwgt78  788 -797
repwgt79  798 -807
repwgt80  808 -817
repwgt81  818 -827
repwgt82  828 -837
repwgt83  838 -847
repwgt84  848 -857
repwgt85  858 -867
repwgt86  868 -877
repwgt87  878 -887
repwgt88  888 -897
repwgt89  898 -907
repwgt90  908 -917
repwgt91  918 -927
repwgt92  928 -937
repwgt93  938 -947
repwgt94  948 -957
repwgt95  958 -967
repwgt96  968 -977
repwgt97  978 -987
repwgt98  988 -997
repwgt99  998 -1007
repwgt100  1008 -1017
repwgt101  1018 -1027
repwgt102  1028 -1037
repwgt103  1038 -1047
repwgt104  1048 -1057
repwgt105  1058 -1067
repwgt106  1068 -1077
repwgt107  1078 -1087
repwgt108  1088 -1097
repwgt109  1098 -1107
repwgt110  1108 -1117
repwgt111  1118 -1127
repwgt112  1128 -1137
repwgt113  1138 -1147
repwgt114  1148 -1157
repwgt115  1158 -1167
repwgt116  1168 -1177
repwgt117  1178 -1187
repwgt118  1188 -1197
repwgt119  1198 -1207
repwgt120  1208 -1217
repwgt121  1218 -1227
repwgt122  1228 -1237
repwgt123  1238 -1247
repwgt124  1248 -1257
repwgt125  1258 -1267
repwgt126  1268 -1277
repwgt127  1278 -1287
repwgt128  1288 -1297
repwgt129  1298 -1307
repwgt130  1308 -1317
repwgt131  1318 -1327
repwgt132  1328 -1337
repwgt133  1338 -1347
repwgt134  1348 -1357
repwgt135  1358 -1367
repwgt136  1368 -1377
repwgt137  1378 -1387
repwgt138  1388 -1397
repwgt139  1398 -1407
repwgt140  1408 -1417
repwgt141  1418 -1427
repwgt142  1428 -1437
repwgt143  1438 -1447
repwgt144  1448 -1457
repwgt145  1458 -1467
repwgt146  1468 -1477
repwgt147  1478 -1487
repwgt148  1488 -1497
repwgt149  1498 -1507
repwgt150  1508 -1517
repwgt151  1518 -1527
repwgt152  1528 -1537
repwgt153  1538 -1547
repwgt154  1548 -1557
repwgt155  1558 -1567
repwgt156  1568 -1577
repwgt157  1578 -1587
repwgt158  1588 -1597
repwgt159  1598 -1607
repwgt160  1608 -1617
;

run;

data sas.rep_nov13;
  array wt(0:160)  repwgt0-repwgt160;
  set rep_nov13;
   
  drop i;
/* ASCII weights has 4 implied decimal places.
   undo by dividing by 10000.
*/
  do i= 0 to 160;
     wt(i)= wt(i)/10000;
  end;
run;

/* SUM of Weights for Verification:

The sum of the replicate weights, repwgt0 - repwgt160,
is outputted in CPS_CIVENG_NRREPWGT_NOV13.LST 

NOV13 Sum of Replicate Weigthts - nov13rep.dat
   
nrrepwgt0 =    238309392.9755
nrrepwgt1 =    238309393.0104
nrrepwgt2 =    238309392.9879
nrrepwgt3 =    238309392.9985
nrrepwgt4 =    238309393.0161
nrrepwgt5 =    238309393.0016
nrrepwgt6 =    238309392.9824
nrrepwgt7 =    238309392.9991
nrrepwgt8 =    238309393.0042
nrrepwgt9 =    238309393.0041
nrrepwgt10 =   238309392.9931
nrrepwgt11 =   238309392.9968
nrrepwgt12 =   238309393.0090
nrrepwgt13 =   238309392.9893
nrrepwgt14 =   238309392.9952
nrrepwgt15 =   238309393.0046
nrrepwgt16 =   238309393.0054
nrrepwgt17 =   238309393.0125
nrrepwgt18 =   238309392.9941
nrrepwgt19 =   238309393.0046
nrrepwgt20 =   238309393.0149
nrrepwgt21 =   238309392.9968
nrrepwgt22 =   238309392.9951
nrrepwgt23 =   238309392.9951
nrrepwgt24 =   238309393.0047
nrrepwgt25 =   238309393.0099
nrrepwgt26 =   238309392.9901
nrrepwgt27 =   238309393.0037
nrrepwgt28 =   238309392.9952
nrrepwgt29 =   238309392.9983
nrrepwgt30 =   238309392.9985
nrrepwgt31 =   238309393.0073
nrrepwgt32 =   238309393.0057
nrrepwgt33 =   238309392.9979
nrrepwgt34 =   238309393.0088
nrrepwgt35 =   238309392.9883
nrrepwgt36 =   238309393.0001
nrrepwgt37 =   238309393.0095
nrrepwgt38 =   238309392.9928
nrrepwgt39 =   238309393.0055
nrrepwgt40 =   238309393.0125
nrrepwgt41 =   238309392.9965
nrrepwgt42 =   238309392.9886
nrrepwgt43 =   238309393.0125
nrrepwgt44 =   238309392.9944
nrrepwgt45 =   238309392.9998
nrrepwgt46 =   238309393.0079
nrrepwgt47 =   238309392.9983
nrrepwgt48 =   238309392.9913
nrrepwgt49 =   238309393.0049
nrrepwgt50 =   238309392.9981
nrrepwgt51 =   238309392.9962
nrrepwgt52 =   238309392.9959
nrrepwgt53 =   238309392.9973
nrrepwgt54 =   238309393.0139
nrrepwgt55 =   238309393.0094
nrrepwgt56 =   238309393.0037
nrrepwgt57 =   238309392.9977
nrrepwgt58 =   238309393.0019
nrrepwgt59 =   238309392.9886
nrrepwgt60 =   238309393.0094
nrrepwgt61 =   238309393.0037
nrrepwgt62 =   238309393.0124
nrrepwgt63 =   238309392.9939
nrrepwgt64 =   238309392.9954
nrrepwgt65 =   238309392.9878
nrrepwgt66 =   238309393.0046
nrrepwgt67 =   238309392.9979
nrrepwgt68 =   238309393.0041
nrrepwgt69 =   238309393.0127
nrrepwgt70 =   238309393.0047
nrrepwgt71 =   238309393.0134
nrrepwgt72 =   238309392.9991
nrrepwgt73 =   238309392.9891
nrrepwgt74 =   238309393.0014
nrrepwgt75 =   238309393.0101
nrrepwgt76 =   238309392.9957
nrrepwgt77 =   238309392.9900
nrrepwgt78 =   238309393.0022
nrrepwgt79 =   238309393.0079
nrrepwgt80 =   238309392.9925
nrrepwgt81 =   238309393.0094
nrrepwgt82 =   238309393.0024
nrrepwgt83 =   238309392.9909
nrrepwgt84 =   238309392.9938
nrrepwgt85 =   238309393.0025
nrrepwgt86 =   238309392.9978
nrrepwgt87 =   238309393.0008
nrrepwgt88 =   238309393.0033
nrrepwgt89 =   238309392.9959
nrrepwgt90 =   238309392.9898
nrrepwgt91 =   238309393.0094
nrrepwgt92 =   238309393.0052
nrrepwgt93 =   238309393.0065
nrrepwgt94 =   238309393.0032
nrrepwgt95 =   238309393.0024
nrrepwgt95 =   238309393.0024
nrrepwgt96 =   238309392.9990
nrrepwgt97 =   238309392.9932
nrrepwgt98 =   238309392.9893
nrrepwgt99 =   238309392.9933
nrrepwgt100 =  238309393.0041
nrrepwgt101 =  238309393.0183
nrrepwgt102 =  238309392.9879
nrrepwgt103 =  238309392.9896
nrrepwgt104 =  238309393.0016
nrrepwgt105 =  238309392.9792
nrrepwgt106 =  238309392.9954
nrrepwgt107 =  238309392.9898
nrrepwgt108 =  238309392.9918
nrrepwgt109 =  238309392.9954
nrrepwgt110 =  238309393.0171
nrrepwgt111 =  238309393.0011
nrrepwgt112 =  238309392.9998
nrrepwgt113 =  238309393.0025
nrrepwgt114 =  238309393.0010
nrrepwgt115 =  238309393.0198
nrrepwgt116 =  238309393.0051
nrrepwgt117 =  238309392.9888
nrrepwgt118 =  238309392.9980
nrrepwgt119 =  238309393.0003
nrrepwgt120 =  238309393.0135
nrrepwgt121 =  238309393.0067
nrrepwgt122 =  238309392.9861
nrrepwgt123 =  238309393.0110
nrrepwgt124 =  238309392.9952
nrrepwgt125 =  238309392.9963
nrrepwgt126 =  238309393.0016
nrrepwgt127 =  238309392.9930
nrrepwgt128 =  238309392.9780
nrrepwgt129 =  238309392.9978
nrrepwgt130 =  238309392.9986
nrrepwgt131 =  238309393.0053
nrrepwgt132 =  238309393.0015
nrrepwgt133 =  238309392.9992
nrrepwgt134 =  238309393.0096
nrrepwgt135 =  238309393.0048
nrrepwgt136 =  238309392.9991
nrrepwgt137 =  238309393.0055
nrrepwgt138 =  238309392.9901
nrrepwgt139 =  238309392.9972
nrrepwgt140 =  238309393.0140
nrrepwgt141 =  238309393.0040
nrrepwgt142 =  238309392.9950
nrrepwgt143 =  238309392.9862
nrrepwgt144 =  238309392.9925
nrrepwgt145 =  238309392.9883
nrrepwgt146 =  238309393.0082
nrrepwgt147 =  238309393.0010
nrrepwgt148 =  238309393.0086
nrrepwgt149 =  238309393.0012
nrrepwgt150 =  238309393.0151
nrrepwgt151 =  238309393.0128
nrrepwgt152 =  238309393.0020
nrrepwgt153 =  238309393.0120
nrrepwgt154 =  238309392.9911
nrrepwgt155 =  238309393.0063
nrrepwgt156 =  238309392.9950
nrrepwgt157 =  238309392.9988
nrrepwgt158 =  238309392.9846
nrrepwgt159 =  238309392.9877
nrrepwgt160 =  238309392.9914

*/

%macro total;
data _null_;
   retain tot_repwgt0-tot_repwgt160 0;
   set sas.rep_nov13   end = last;
   %do i = 0 %to 160;
      tot_repwgt&i + repwgt&i;
   %end;
   if last then do;
      file replist;
           put "&replist";
       put 'Sum of replicate weights';
      put;
      %do i = 0 %to 160;
          put "   repwgt&i = " @16 tot_repwgt&i f15.4;
      %end;
   end;
run;
%mend total;

%total;

