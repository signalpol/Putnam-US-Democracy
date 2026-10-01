/* cps_civiceng_nrrepwgt_nov11.sas
This code is for documentation of the record layout for
the ASCII replicate weight code for the 
NOV 2011 Civic Engagement  Non-Response 
*/

/* Enter filepath and name of ASCII replicate file */
filename ipfile "N:\CPS\Supplements\Civic Engagement\2011\nov11nrrep.dat";

/* Add SAS library. Enter file path to store ASCII file converted to SAS dataset */
libname sas '.';

/* Name of output */
%let replist= CPS_CIVENG_NRREPWGT_NOV11.LST;
filename replist "&replist";


data repwgtds_nov11;
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

data sas.repwgts_nov11;
set repwgtds_nov11;

   array wt(0:160)  repwgt0-repwgt160;

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
is outputted in CPS_CIVENG_NRREPWGT_NOV11.LST
and should appear the same as the following:
                                                                        

CPS_CIVENG_NRREPWGT_NOV11.LST                                                 
                                                                              
NOV 2011 Civic Engagement: Sum of replicate weights in nov11nrrep.dat         
                                                                              
   repwgt0 =    232216826.9937                                                
   repwgt1 =    232216827.0224                                                
   repwgt2 =    232216826.9959                                                
   repwgt3 =    232216826.9896                                                
   repwgt4 =    232216826.9957                                                
   repwgt5 =    232216827.0069                                                
   repwgt6 =    232216826.9865                                                
   repwgt7 =    232216826.9996                                                
   repwgt8 =    232216826.9981                                                
   repwgt9 =    232216826.9970                                                
   repwgt10 =   232216827.0018                                                
   repwgt11 =   232216826.9972                                                
   repwgt12 =   232216826.9940                                                
   repwgt13 =   232216826.9969                                                
   repwgt14 =   232216826.9935                                                
   repwgt15 =   232216826.9923                                                
   repwgt16 =   232216826.9964                                                
   repwgt17 =   232216826.9990                                                
   repwgt18 =   232216827.0151                                                
   repwgt19 =   232216827.0144                                                
   repwgt20 =   232216827.0023                                                
   repwgt21 =   232216827.0078                                                
   repwgt22 =   232216827.0031                                                
   repwgt23 =   232216827.0027                                                
   repwgt24 =   232216827.0064                                                
   repwgt25 =   232216827.0046                                                
   repwgt26 =   232216827.0040                                                
   repwgt27 =   232216826.9898                                                
   repwgt28 =   232216827.0165                                                
   repwgt29 =   232216827.0116                                                
   repwgt30 =   232216827.0122                                                
   repwgt31 =   232216826.9889                                                
   repwgt32 =   232216827.0117                                                
   repwgt33 =   232216827.0028                                                
   repwgt34 =   232216826.9945                                                
   repwgt35 =   232216826.9919                                                
   repwgt36 =   232216826.9995                                                
   repwgt37 =   232216826.9936                                                
   repwgt38 =   232216827.0046                                                
   repwgt39 =   232216827.0012                                                
   repwgt40 =   232216827.0154                                                
   repwgt41 =   232216826.9869                                                
   repwgt42 =   232216826.9905                                                
   repwgt43 =   232216827.0006                                                
   repwgt44 =   232216826.9976                                                
   repwgt45 =   232216827.0032                                                
   repwgt46 =   232216827.0044                                                
   repwgt47 =   232216827.0094                                                
   repwgt48 =   232216826.9945                                                
   repwgt49 =   232216826.9991                                                
   repwgt50 =   232216826.9768                                                
   repwgt51 =   232216826.9882                                                
   repwgt52 =   232216827.0024                                                
   repwgt53 =   232216827.0009                                                
   repwgt54 =   232216826.9977                                                
   repwgt55 =   232216827.0016                                                
   repwgt56 =   232216826.9983                                                
   repwgt57 =   232216827.0025                                                
   repwgt58 =   232216826.9915                                                
   repwgt59 =   232216827.0120                                                
   repwgt60 =   232216826.9942                                                
   repwgt61 =   232216827.0175                                                
   repwgt62 =   232216827.0116                                                
   repwgt63 =   232216827.0106                                                
   repwgt64 =   232216827.0067                                                
   repwgt65 =   232216827.0133                                                
   repwgt66 =   232216826.9950                                                
   repwgt67 =   232216827.0061                                                
   repwgt68 =   232216827.0107                                                
   repwgt69 =   232216827.0068                                                
   repwgt70 =   232216826.9927                                                
   repwgt71 =   232216826.9876                                                
   repwgt72 =   232216826.9974                                                
   repwgt73 =   232216826.9901                                                
   repwgt74 =   232216826.9919                                                
   repwgt75 =   232216826.9844                                                
   repwgt76 =   232216826.9923                                                
   repwgt77 =   232216827.0077                                                
   repwgt78 =   232216827.0007                                                
   repwgt79 =   232216827.0161                                                
   repwgt80 =   232216827.0021                                                
   repwgt81 =   232216827.0218                                                
   repwgt82 =   232216826.9887                                                
   repwgt83 =   232216826.9950                                                
   repwgt84 =   232216826.9971                                                
   repwgt85 =   232216827.0065                                                
   repwgt86 =   232216826.9885                                                
   repwgt87 =   232216826.9871                                                
   repwgt88 =   232216826.9977                                                
   repwgt89 =   232216827.0052                                                
   repwgt90 =   232216827.0113                                                
   repwgt91 =   232216827.0035                                                
   repwgt92 =   232216826.9866                                                
   repwgt93 =   232216826.9936                                                
   repwgt94 =   232216826.9962                                                
   repwgt95 =   232216827.0008                                                
   repwgt96 =   232216826.9913                                                
   repwgt97 =   232216826.9980                                                
   repwgt98 =   232216826.9749                                                
   repwgt99 =   232216826.9915                                                
   repwgt100 =  232216827.0073                                                
   repwgt101 =  232216827.0130                                                
   repwgt102 =  232216826.9887                                                
   repwgt103 =  232216826.9873                                                
   repwgt104 =  232216827.0279                                                
   repwgt105 =  232216826.9984                                                
   repwgt106 =  232216827.0201                                                
   repwgt107 =  232216826.9974                                                
   repwgt108 =  232216827.0039                                                
   repwgt109 =  232216826.9945                                                
   repwgt110 =  232216826.9941                                                
   repwgt111 =  232216826.9962                                                
   repwgt112 =  232216827.0203                                                
   repwgt113 =  232216827.0185                                                
   repwgt114 =  232216827.0006                                                
   repwgt115 =  232216827.0005                                                
   repwgt116 =  232216827.0106                                                
   repwgt117 =  232216826.9980                                                
   repwgt118 =  232216826.9852                                                
   repwgt119 =  232216827.0120                                                
   repwgt120 =  232216826.9848                                                
   repwgt121 =  232216826.9951                                                
   repwgt122 =  232216826.9804                                                
   repwgt123 =  232216826.9889                                                
   repwgt124 =  232216827.0117                                                
   repwgt125 =  232216826.9915                                                
   repwgt126 =  232216826.9953                                                
   repwgt127 =  232216826.9992                                                
   repwgt128 =  232216827.0274                                                
   repwgt129 =  232216827.0103                                                
   repwgt130 =  232216826.9930                                                
   repwgt131 =  232216826.9928                                                
   repwgt132 =  232216827.0115                                                
   repwgt133 =  232216826.9894                                                
   repwgt134 =  232216826.9879                                                
   repwgt135 =  232216827.0065                                                
   repwgt136 =  232216826.9829                                                
   repwgt137 =  232216826.9915                                                
   repwgt138 =  232216827.0063                                                
   repwgt139 =  232216827.0028                                                
   repwgt140 =  232216826.9956                                                
   repwgt141 =  232216826.9856                                                
   repwgt142 =  232216826.9918                                                
   repwgt143 =  232216826.9825                                                
   repwgt144 =  232216827.0002                                                
   repwgt145 =  232216826.9978                                                
   repwgt146 =  232216827.0045                                                
   repwgt147 =  232216827.0072                                                
   repwgt148 =  232216827.0192                                                
   repwgt149 =  232216827.0154                                                
   repwgt150 =  232216826.9860                                                
   repwgt151 =  232216827.0054                                                
   repwgt152 =  232216826.9936                                                
   repwgt153 =  232216826.9838                                                
   repwgt154 =  232216826.9906                                                
   repwgt155 =  232216826.9984                                                
   repwgt156 =  232216827.0093                                                
   repwgt157 =  232216827.0068                                                
   repwgt158 =  232216827.0135                                                
   repwgt159 =  232216827.0068                                                
   repwgt160 =  232216827.0117

Use these totals to verify that your file is created correctly.

*/


%macro total;
data _null_;
   set sas.repwgts_nov11   end = last;

   retain tot_repwgt0-tot_repwgt160 0;

   %do i = 0 %to 160;
      tot_repwgt&i + repwgt&i;
   %end;

   if last then do;
      file replist;
      put "&replist";
      put;
      put 'NOV 2011 Civic Engagement: Sum of replicate weights in nov11nrrep.dat';
      put;
      %do i = 0 %to 160;
          put "   repwgt&i = " @16 tot_repwgt&i f15.4;
      %end;
   end;
run;
%mend total;

%total;
