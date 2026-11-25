// usage: node render.js <width> <outdir> <fps> <worker> <nworkers> [t list for stills]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const [w,out,fps,k,n,...ts]=process.argv.slice(2);const W=+w,H=W*9/16;fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--disable-gpu-vsync']});
 const p=await b.newPage({viewport:{width:W,height:H}});
 p.on('console',m=>{if(m.type()=='error')console.log('ERR',m.text())});p.on('pageerror',e=>console.log('PAGEERR',e.message));
 await p.goto(`http://localhost:8765/index.html?w=${W}`);await p.waitForFunction('window.ready===true',null,{timeout:120000});
 const shot=async(t,f)=>{await p.evaluate(t=>window.setTime(t),t);await p.screenshot({path:f,type:'jpeg',quality:93})};
 if(ts.length){for(const t of ts){const t0=Date.now();await shot(+t,`${out}/s${String(t).padStart(5,'0')}.jpg`);console.log(t,Date.now()-t0,'ms')}}
 else{const N=Math.round(120*fps);for(let i=+k;i<N;i+=+n){const f=`${out}/f${String(i).padStart(5,'0')}.jpg`;if(fs.existsSync(f))continue;await shot(i/fps,f);if(i%200<+n)console.log('frame',i)}}
 await b.close();
})();
