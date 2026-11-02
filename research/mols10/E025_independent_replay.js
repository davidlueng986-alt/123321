// E025 independent JavaScript replay, no Python dependencies.
// Six source TRPs from Bright-Keita-Stevens 2026 Appendix, as in E024.
// This enumerates all proper 2-symbol row/column cycle flips in BOTH squares.
// node E025_independent_replay.js
const RAW={
  "UW": [
    "0234561789 1460923857 2359087461 5671308294 6012854973 7503419628 8725196340 9148270536 3897642015 4986735102",
    "0372495816 1537286904 3716520498 5049132687 9263807145 2481659730 6150748329 7928364051 8694013572 4805971263"
  ],
  "UX": [
    "0124563789 1382647590 2895314076 5901278634 7043192865 9537026148 3476805921 6710489352 4658930217 8269751403",
    "0591837462 3215670849 5364109278 6408321795 1936452087 2783965104 4820796531 7159048326 8647213950 9072584613"
  ],
  "VX": [
    "0234561789 1375094826 3029685147 4618207953 5103972468 7540138692 2786349015 6892713504 9451826370 8967450231",
    "0349817265 1508629734 2630984571 4152390687 3876251490 5924708316 6487032159 7061543928 8295176043 9713465802"
  ],
  "WW": [
    "0234561789 1376294058 2715048936 3540817692 8023975164 4168359207 5897126340 6901783425 9452630871 7689402513",
    "0358172496 2061597843 5932418067 6125804379 9704325618 1583649720 3819760254 4270986531 8647231905 7496053182"
  ],
  "WX": [
    "0134562789 1502798643 2690813475 3257041896 7918235064 4075629318 5423986107 6789104532 8361457920 9846370251",
    "6172083954 7305914286 8720345619 9051836742 0248697135 1684250397 2817469503 3469528071 4593172860 5936701428"
  ],
  "XX": [
    "0134562789 1763285940 2915637804 6298314075 3607849251 4529703168 5840176392 7052498613 8471920536 9386051427",
    "0728159634 3254087196 6802731549 8930415267 1047963825 2693570418 4375296081 5416802973 7189624350 9561348702"
  ]
};
const parse=s=>s.split(/\s+/).map(x=>[...x].map(Number));
const derive=(p,q)=>{
 const inv=Array.from({length:10},()=>[]);
 for(let r=0;r<10;r++)for(let c=0;c<10;c++)inv[c][p[r][c]]=r;
 return q.map(row=>row.map((v,c)=>inv[c][v]));
};
function variants(a){
 const variants=[];
 for(let u=0;u<10;u++)for(let v=u+1;v<10;v++){
  const cells=[];
  for(let r=0;r<10;r++)for(let c=0;c<10;c++)
   if(a[r][c]===u||a[r][c]===v)cells.push(r*10+c);
  if(cells.length!==20)throw Error('wrong symbol counts');
  const group=Array(20).fill(-1);let k=0;
  for(let i=0;i<20;i++)if(group[i]===-1){
   const stack=[i];group[i]=k;
   while(stack.length){
    const j=stack.pop(),r=Math.floor(cells[j]/10),c=cells[j]%10;
    for(let h=0;h<20;h++)if(group[h]<0&&
      (Math.floor(cells[h]/10)===r||cells[h]%10===c)){
      group[h]=k;stack.push(h);
    }
   }
   k++;
  }
  for(let mask=1;mask<(1<<k)-1;mask++){
   const arr=a.flat().slice();
   for(let i=0;i<20;i++)if(mask&(1<<group[i]))
    arr[cells[i]]=arr[cells[i]]===u?v:u;
   variants.push(arr);
  }
 }
 return variants;
}
function overlay(a,b){
 const seen=new Uint8Array(100);let count=0;
 for(let i=0;i<100;i++){const k=a[i]*10+b[i];if(!seen[k]){seen[k]=1;count++}}
 return count;
}
const expected={UW:[118,138,16284,96],UX:[108,118,12744,96],
 VX:[126,108,13608,96],WW:[154,130,20020,98],
 WX:[100,100,10000,96],XX:[132,114,15048,96]};
const result={};
for(const [label,ss] of Object.entries(RAW)){
 const [p,q]=ss.map(parse),z=derive(p,q),av=variants(z),bv=variants(q);
 if(overlay(z.flat(),q.flat())!==100)throw Error('source not orthogonal');
 let max=0,orthogonal=0,best=0;
 for(const a of av)for(const b of bv){
  const n=overlay(a,b);
  if(n>max){max=n;best=0}
  if(n===max)best++;
  if(n===100)orthogonal++;
 }
 const values=[av.length,bv.length,av.length*bv.length,max];
 if(JSON.stringify(values)!==JSON.stringify(expected[label])||orthogonal!==0)
  throw Error(label+': unexpected '+JSON.stringify({values,orthogonal}));
 result[label]={A_trades:av.length,B_trades:bv.length,
  coupled:av.length*bv.length,max_overlay:max,best_count:best,orthogonal};
}
console.log(JSON.stringify(result,null,2));
