import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.argv[2];
const d=JSON.parse(await fs.readFile(root+'/workbook_data.json','utf8'));
const w=Workbook.create();
for(const [name,records] of [['Canonical',d.panel],['Observed items',d.observed],['Sensitivity',d.sensitivity],['QA',d.qa]]){
  const fields=Object.keys(records[0]);
  const rows=[fields,...records.map(r=>fields.map(k=>r[k]??null))];
  if(name==='Observed items') for(let i=1;i<rows.length;i++) for(const k of ['year','value','SE','eligible_n','valid_n','weighted_denominator']){
    const j=fields.indexOf(k);if(j>=0)rows[i][j]=rows[i][j]===''?null:Number(rows[i][j]);
  }
  const s=w.worksheets.add(name);s.showGridLines=false;
  s.getRangeByIndexes(0,0,rows.length,fields.length).values=rows;
  s.getRangeByIndexes(0,0,rows.length,fields.length).format.font={name:'Arial',size:10};
  s.getRangeByIndexes(0,0,rows.length,fields.length).format.columnWidth=22;
  s.getRangeByIndexes(0,0,1,fields.length).format={fill:'#253B53',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:42,wrapText:true};
  s.freezePanes.freezeRows(1);
  if(name!=='QA')s.freezePanes.freezeColumns(2);
  if(name==='Canonical')s.getRange(`C2:F${rows.length}`).setNumberFormat('0.000');
  if(name==='Observed items'){
    s.getRange(`D2:E${rows.length}`).setNumberFormat('0.00%');s.getRange('C:C').format.columnWidth=40;
  }
  if(name==='Sensitivity')s.getRange(`D2:E${rows.length}`).setNumberFormat('0.000');
  if(name==='QA'){s.getRange('A:A').format.columnWidth=42;s.getRange('C:C').format.columnWidth=70;}
  const preview=await w.render({sheetName:name,range:name==='QA'?'A1:C11':'A1:F11',scale:1.2,format:'png'});
  await fs.writeFile(root+'/'+name.replaceAll(' ','_')+'_preview.png',new Uint8Array(await preview.arrayBuffer()));
}
const m=w.worksheets.add('Method');m.showGridLines=false;
const notes=[['Item','Definition'],['Primary construct','Active6: local voting, contact, political donation, public meetings, neighborhood action, political consumption'],['Analytical unit','Latent signal in fixed 2017 Active6 input-index SD. Not a percentage.'],['Primary model','M2: state/common temporal GP, partial-item calibration covariance, marginalized CPS regime shift'],['Direct observations','2,300 separate item rates; 200 complete-basket CEV state-years and 150 partial historical state-years'],['Backcast','2000–2016 full-basket backcast; 2000–2009 has no direct item inputs'],['SE and CI','Conditional model SE; nominal 95% model/sensitivity envelope is not calibrated latent-truth coverage'],['Sensitivity','Broad10, Active5 excluding vote, no-regime, CEV-only, lengths 3/12, regime prior SD 1'],['Measurement limitation','Historical transfer assumed; original CEV denominator implementation and survey SE not independently reproduced'],['S7 overlap','Self-reported local election participation differs from administrative general-election VEP turnout'],['Validation','Training-only complete-wave holdout; early partial-item tests do not validate historical latent truth']];
m.getRange('A1:B11').values=notes;m.getRange('A1:B11').format.font={name:'Arial',size:10};
m.getRange('A:A').format.columnWidth=25;m.getRange('B:B').format.columnWidth=135;
m.getRange('A1:B11').format.rowHeight=28;m.getRange('A1:B1').format={fill:'#253B53',font:{bold:true,color:'#FFFFFF'}};
w.recalculate();
console.log((await w.inspect({kind:'table',range:'Canonical!A1:F4',include:'values',tableMaxRows:4,tableMaxCols:6})).ndjson);
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20}})).ndjson);
const preview=await w.render({sheetName:'Method',range:'A1:B11',scale:1,format:'png'});
await fs.writeFile(root+'/Method_preview.png',new Uint8Array(await preview.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(w)).save(root+'/final_package/S5_FINAL_2000_2023.xlsx');
