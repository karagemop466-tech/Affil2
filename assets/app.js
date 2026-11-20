// Privacy-preserving measurement: localStorage only, no cookies/trackers. Five events: page_view, outbound_click, guide_read, search, suggestion_rank
(function(){try{
 var ev=JSON.parse(localStorage.getItem('sn_events')||'[]');
 function log(e,d){ev.push(Object.assign({e:e,t:Date.now(),page:location.pathname},d||{}));localStorage.setItem('sn_events',JSON.stringify(ev.slice(-500)));}
 log('page_view');
 if(/guides\//.test(location.pathname)) log('guide_read');
 document.querySelectorAll('[data-outbound]').forEach(function(a){a.addEventListener('click',function(){log('outbound_click',{product:a.getAttribute('data-outbound')});var c=JSON.parse(localStorage.getItem('sn_clicks')||'{}');c[a.getAttribute('data-outbound')]=(c[a.getAttribute('data-outbound')]||0)+1;localStorage.setItem('sn_clicks',JSON.stringify(c));var el=document.getElementById('localClicks');if(el)el.textContent=Object.values(c).reduce(function(x,y){return x+y},0);});});
 var ex=document.getElementById('exportClicks');if(ex)ex.addEventListener('click',function(){var c=localStorage.getItem('sn_clicks')||'{}';download('clicks.csv','product,clicks\n'+Object.entries(JSON.parse(c)).map(function(x){return x[0]+','+x[1]}).join('\n'));});
 // Suggestions ranking
 var rank=JSON.parse(localStorage.getItem('sn_rank')||'[]');
 function renderRank(){document.querySelectorAll('#sugTable tbody tr').forEach(function(tr,i){var s=tr.querySelector('.rank');if(s)s.textContent=rank.indexOf(tr.getAttribute('data-sug'))>=0?('#'+(rank.indexOf(tr.getAttribute('data-sug'))+1)):'';});}
 if(document.getElementById('sugTable')){if(!rank.length){rank=[].slice.call(document.querySelectorAll('#sugTable tbody tr')).map(function(tr){return tr.getAttribute('data-sug')});}
 document.querySelectorAll('[data-up],[data-down]').forEach(function(b){b.addEventListener('click',function(){var id=b.getAttribute('data-up')||b.getAttribute('data-down');var i=rank.indexOf(id);var j=b.hasAttribute('data-up')?i-1:i+1;if(j<0||j>=rank.length)return;var t=rank[i];rank[i]=rank[j];rank[j]=t;localStorage.setItem('sn_rank',JSON.stringify(rank));log('suggestion_rank',{rank:rank.slice()});renderRank();});});
 renderRank();
 
 var review=JSON.parse(localStorage.getItem('sn_review')||'{}');
 function renderReview(){var n={approve:0,defer:0,reject:0};document.querySelectorAll('#sugTable tbody tr').forEach(function(tr){var id=tr.getAttribute('data-sug'),out=tr.querySelector('.verdict[data-for="'+id+'"]'),v=review[id];if(out){out.textContent=v?(v.charAt(0).toUpperCase()+v.slice(1)+'d'):'';out.className='verdict'+(v?' v-'+v:'');}tr.classList.remove('rv-approve','rv-defer','rv-reject');tr.querySelectorAll('.rvbt').forEach(function(b){b.setAttribute('aria-pressed',String(v===b.getAttribute('data-verdict')));});if(v){n[v]=(n[v]||0)+1;tr.classList.add('rv-'+v);}});var a=document.getElementById('tApprove'),d=document.getElementById('tDefer'),r=document.getElementById('tReject'),left=document.getElementById('tLeft');if(a)a.textContent=n.approve;if(d)d.textContent=n.defer;if(r)r.textContent=n.reject;var total=document.querySelectorAll('#sugTable tbody tr').length,done=n.approve+n.defer+n.reject;if(left)left.textContent=(total-done)+' of '+total+' not reviewed yet';}
 document.querySelectorAll('.rvbt').forEach(function(b){b.addEventListener('click',function(){var id=b.getAttribute('data-review'),v=b.getAttribute('data-verdict');if(review[id]===v){delete review[id];}else{review[id]=v;}localStorage.setItem('sn_review',JSON.stringify(review));log('suggestion_review',{suggestion:id,verdict:review[id]||'cleared'});renderReview();});});
 renderReview();
 var exr=document.getElementById('exportReview');if(exr)exr.addEventListener('click',function(){var out=['suggestion,verdict,exported_utc'],now=new Date().toISOString();Object.keys(review).sort().forEach(function(id){out.push(id+','+review[id]+','+now);});download('review.csv',out.join('\n'));});
 var rvr=document.getElementById('resetReview');if(rvr)rvr.addEventListener('click',function(){localStorage.removeItem('sn_review');location.reload();});
 var er=document.getElementById('exportRank');if(er)er.addEventListener('click',function(){download('ranking.csv','rank,suggestion,review\n'+rank.map(function(s,i){return (i+1)+','+s+','+(review[s]||'unreviewed')}).join('\n'));});
 var rr=document.getElementById('resetRank');if(rr)rr.addEventListener('click',function(){localStorage.removeItem('sn_rank');location.reload();});
 var f=document.getElementById('decisionForm');if(f)f.addEventListener('submit',function(e){e.preventDefault();localStorage.setItem('sn_decision',JSON.stringify({chosen:f.chosen.value,why:f.why.value,measure:f.measure.value,t:Date.now()}));document.getElementById('decisionSaved').textContent='Saved locally at '+new Date().toISOString()+'. Export it with your ranking.';});}
 var eventExport=document.getElementById('exportEvents');
 if(eventExport)eventExport.addEventListener('click',()=>{
   const rows=JSON.parse(localStorage.getItem('sn_events')||'[]');
   download('events.csv','event,utc,product,result_count\n'+rows.map(r=>[r.e,new Date(r.t).toISOString(),r.product||'',r.results??''].join(',')).join('\n'));
 });
 function download(n,c){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([c],{type:'text/csv'}));a.download=n;a.click();}
}catch(e){}})();
// Keep navigation and search operational even when browser storage is disabled.
(() => {
 const toggle=document.querySelector('.navtoggle'), nav=document.querySelector('#primary-nav');
 toggle?.addEventListener('click',()=>toggle.setAttribute('aria-expanded',nav.classList.toggle('open')));
 const index=document.querySelector('#searchIndex'); if(!index)return;
 const q=(new URLSearchParams(location.search).get('q')||'').trim(); document.querySelector('#sq').value=q;
 if(!q)return;
 const tokens=q.toLowerCase().split(/\s+/), hits=JSON.parse(index.textContent).filter(x=>tokens.every(t=>(x.t+' '+x.d+' '+x.k).toLowerCase().includes(t)));
 document.querySelector('#searchMeta').textContent=hits.length?`${hits.length} matching pages`:'No matches. Try “basket”, “wireless” or “capacity”.';
 for(const hit of hits){const p=document.createElement('p'),a=document.createElement('a');a.href=hit.u;a.textContent=hit.t;p.append(a);document.querySelector('#results').append(p)}
 if(hits.length)try{const events=JSON.parse(localStorage.getItem('sn_events')||'[]');events.push({e:'search',t:Date.now(),results:hits.length});localStorage.setItem('sn_events',JSON.stringify(events.slice(-500)))}catch{}
})();
