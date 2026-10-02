import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const root=process.argv[2]??'/workspace/scratch/9eb6fec78fce/s2_final';
const data=JSON.parse(await fs.readFile(root+'/workbook_data.json','utf8'));
const w=Workbook.create();
const fields=['state','year','S2_estimate','S2_SE','CI_lower','CI_upper','observation_type','direct_observation','direct_input_available','source_series','measurement_regime','model_estimated','backcast_flag','bridge_flag','uncertainty_flag','provenance','unit','CI_method','latent_logit_coordinate'];
const obs=['year','state','s2_participation','s2_se','source_series','observation_status','observation_type','unit','measurement_regime'];
for(const [name,rows,cols] of [['Latent',data.panel,fields],['Observed',data.observed,obs]]){
 const s=w.worksheets.add(name);s.showGridLines=false;
 const mat=[cols,...rows.map(r=>cols.map(k=>r[k]??null))];
 if(name==='Observed')for(let i=1;i<mat.length;i++){mat[i][0]=Number(mat[i][0]);mat[i][2]=Number(mat[i][2]);mat[i][3]=mat[i][3]===''?null:Number(mat[i][3]);}
 s.getRangeByIndexes(0,0,mat.length,cols.length).values=mat;
 s.getRangeByIndexes(0,0,mat.length,cols.length).format.font={name:'Arial',size:10};
 s.getRangeByIndexes(0,0,1,cols.length).format={fill:'#253B53',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
 s.getRangeByIndexes(0,0,mat.length,cols.length).format.columnWidth=22;
 s.getRangeByIndexes(0,0,mat.length,1).format.columnWidth=10;
 s.getRangeByIndexes(1,1,mat.length-1,1).setNumberFormat(name==='Latent'?'0':'@');
 if(name==='Latent'){s.getRange(`C2:F${mat.length}`).setNumberFormat('0.000');s.getRange('O:O').format.columnWidth=65;s.getRange('P:P').format.columnWidth=65;}
 else{s.getRange(`C2:D${mat.length}`).setNumberFormat('0.00%');s.getRange('E:I').format.columnWidth=38;}
 s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(2);
 const preview=await w.render({sheetName:name,range:name==='Latent'?'A1:I11':'A1:D11',scale:1.5,format:'png'});
 await fs.writeFile(root+'/'+name+'_preview.png',new Uint8Array(await preview.arrayBuffer()));
}
const m=w.worksheets.add('Method');m.showGridLines=false;
const notes=[['Item','Definition'],['Analytical unit','Latent index, 2013 state mean 0 and SD 1'],['Primary model','M2: state and common temporal Gaussian processes plus CEV regime offset'],['Observed values','Separate 400-row direct input table; original proportions preserved'],['Backcast','All 2000–2008 latent values; no 2008 direct observation in current evidence'],['Uncertainty','Model/Hessian and M1/M2 length sensitivity envelope; not calibrated 95% coverage'],['Measurement limitation','Nonoverlapping predicates; bridge is conditional on model assumptions'],['SE limitation','Unknown original design SE for 2009/2010 and archived CEV waves'],['QA checks',data.qa.length],['QA passed',data.qa.filter(x=>x.result==='PASS').length]];
m.getRange('A1:B10').values=notes;m.getRange('A1:B10').format.font={name:'Arial',size:10};m.getRange('A1:B1').format={fill:'#253B53',font:{bold:true,color:'#FFFFFF'}};m.getRange('A:A').format.columnWidth=24;m.getRange('B:B').format.columnWidth=105;m.getRange('A1:B10').format.rowHeight=25;
w.recalculate();
console.log((await w.inspect({kind:'table',range:'Latent!A1:F4',include:'values',tableMaxRows:4,tableMaxCols:6})).ndjson);
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20}})).ndjson);
const preview=await w.render({sheetName:'Method',range:'A1:B10',scale:1,format:'png'});await fs.writeFile(root+'/Method_preview.png',new Uint8Array(await preview.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(w)).save(root+'/final_package/S2_FINAL_2000_2023.xlsx');
