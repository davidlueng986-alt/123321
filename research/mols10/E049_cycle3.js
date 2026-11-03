// E049: exhaustive three-column cyclic rewrites of fourth row; no external dependencies.
// Input: E047_SOURCES.json. Run: node research/mols10/E049_cycle3.js
const fs=require('fs'),assert=require('assert');
const path=require('path');
const src=require('./E047_SOURCES.json').sources;
function valid(s){
 for(let q=0;q<3;q++){for(let r=0;r<4;r++)if(new Set(s[q][r]).size!==10)return false;
 for(let c=0;c<10;c++)if(new Set([0,1,2,3].map(r=>s[q][r][c])).size!==4)return false;}
 for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let z=new Set();
 for(let r=0;r<4;r++)for(let c=0;c<10;c++)z.add(s[a][r][c]*10+s[b][r][c]);
 if(z.size!==40)return false;}return true;
}
function residual(s){
 const used=[0,1,2].map(q=>Array.from({length:10},(_,c)=>new Set(s[q].map(row=>row[c]))));
 const pairs=[[0,1],[0,2],[1,2]], pu=pairs.map(([a,b])=>new Set(s[a].flatMap((row,r)=>row.map((v,c)=>v*10+s[b][r][c]))));
 const need=new Set(),covered=new Set();let candidates=0;
 for(let q=0;q<3;q++)for(let c=0;c<10;c++)for(let v=0;v<10;v++)if(!used[q][c].has(v))need.add('c'+q+','+c+','+v);
 for(let t=0;t<3;t++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)if(!pu[t].has(a*10+b))need.add('p'+t+','+a+','+b);
 for(let c=0;c<10;c++)for(let a=0;a<10;a++)if(!used[0][c].has(a))for(let b=0;b<10;b++)if(!used[1][c].has(b)&&!pu[0].has(a*10+b))for(let d=0;d<10;d++)
 if(!used[2][c].has(d)&&!pu[1].has(a*10+d)&&!pu[2].has(b*10+d)){
 candidates++;for(let q=0;q<3;q++)covered.add('c'+q+','+c+','+[a,b,d][q]);
 covered.add('p0,'+a+','+b);covered.add('p1,'+a+','+d);covered.add('p2,'+b+','+d);
 }
 return {candidates,missing:[...need].filter(x=>!covered.has(x))};
}
const counts={},masks={},cases=[];let proposals=0;
for(const [key,source] of Object.entries(src)){let n=0;
for(let i=0;i<10;i++)for(let j=i+1;j<10;j++)for(let k=j+1;k<10;k++)for(let dir=0;dir<2;dir++)for(let mask=1;mask<8;mask++){
 proposals++;const s=source.map(x=>x.map(y=>y.slice()));
 for(let q=0;q<3;q++)if(mask&(1<<q)){let x=[i,j,k],v=x.map(c=>s[q][3][c]);for(let t=0;t<3;t++)s[q][3][x[t]]=v[(t+(dir?2:1))%3];}
 if(!valid(s))continue;n++;masks[mask]=(masks[mask]||0)+1;
 const z=residual(s);cases.push({source:key,columns:[i,j,k],dir,mask,candidates:z.candidates,missing:z.missing});
}counts[key]=n;}
const unique=new Set(cases.map(x=>JSON.stringify(x))); // unique moves, not proof of isotopy distinctness
const zero=cases.filter(x=>x.missing.length).length;
assert.equal(proposals,13440);assert.equal(cases.length,133);assert.equal(zero,24);
assert.deepEqual(counts,{'0':15,'70':15,'140':11,'210':16,'280':22,'350':20,'420':12,'490':22});
const result={experiment:'E049',proposals,valid:cases.length,zero_support:zero,full_support:cases.length-zero,counts,masks,cases};
if(process.argv.includes('--write'))fs.writeFileSync(path.join(__dirname,'E049_RESULTS.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({proposals,valid:cases.length,zero_support:zero,full_support:cases.length-zero,counts,masks}));
