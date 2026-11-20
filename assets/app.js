// ShopNow Kitchen — privacy-preserving measurement layer.
// Five defined events: page_view, outbound_click, guide_read, search, suggestion_rank.
// Privacy rules: no cookies, no cross-site identifiers, no IP logging client-side.
// Events are kept in localStorage (user-owned) AND beacons are sent to the
// self-hosted endpoint at <origin>/api/analytics (see analytics-endpoint/README.md).
// The beacon is fire-and-forget: if no endpoint is deployed, nothing breaks and
// nothing leaves the browser (FLG-010 / Q-08).
(function(){try{
 var ENDPOINT='api/analytics';
 // Session token: random, memory-only, regenerated per tab session. Not a cookie,
 // not persisted, not shared across sites — lets the server count sessions, not people.
 var SESSION=Math.random().toString(36).slice(2,12)+Date.now().toString(36).slice(-4);
 var ev=JSON.parse(localStorage.getItem('sn_events')||'[]');
 function beacon(payload){
   try{
     var body=JSON.stringify(Object.assign({s:SESSION,d:new Date().toISOString().slice(0,10)},payload));
     if(navigator.sendBeacon){navigator.sendBeacon(ENDPOINT,new Blob([body],{type:'application/json'}));}
     else{fetch(ENDPOINT,{method:'POST',body:body,keepalive:true,headers:{'Content-Type':'application/json'}}).catch(function(){});}
   }catch(e){}
 }
 function log(e,d){
   var row=Object.assign({e:e,t:Date.now(),page:location.pathname},d||{});
   ev.push(row);localStorage.setItem('sn_events',JSON.stringify(ev.slice(-500)));
   beacon(Object.assign({e:e,p:location.pathname},d||{}));
 }
 log('page_view');
 if(/guides\//.test(location.pathname)) log('guide_read',{guide:location.pathname.split('/').pop()});
 // Outbound click counter (privacy-preserving: product id only, no query strings)
 document.querySelectorAll('[data-outbound]').forEach(function(a){a.addEventListener('click',function(){
   var pid=a.getAttribute('data-outbound');
   log('outbound_click',{product:pid});
   var c=JSON.parse(localStorage.getItem('sn_clicks')||'{}');
   c[pid]=(c[pid]||0)+1;localStorage.setItem('sn_clicks',JSON.stringify(c));
   var el=document.getElementById('localClicks');if(el)el.textContent=Object.values(c).reduce(function(x,y){return x+y},0);
 });});
 // Search event: load-time on search.html?q=… and on submit
 if(/search\.html$/.test(location.pathname)){
   var q0=new URLSearchParams(location.search).get('q');
   if(q0) log('search',{q:q0.slice(0,80)});
   var sf=document.querySelector('form.search');
   if(sf)sf.addEventListener('submit',function(){var i=sf.querySelector('input[name=q]');if(i&&i.value)log('search',{q:i.value.slice(0,80)});});
 }
 var ex=document.getElementById('exportClicks');
 if(ex)ex.addEventListener('click',function(){
   var c=localStorage.getItem('sn_clicks')||'{}';
   download('clicks.csv','product,clicks\n'+Object.entries(JSON.parse(c)).map(function(x){return x[0]+','+x[1]}).join('\n'));
 });
 // Suggestions ranking (event: suggestion_rank)
 var rank=JSON.parse(localStorage.getItem('sn_rank')||'[]');
 function renderRank(){document.querySelectorAll('#sugTable tbody tr').forEach(function(tr){var s=tr.querySelector('.rank');if(s)s.textContent=rank.indexOf(tr.getAttribute('data-sug'))>=0?('#'+(rank.indexOf(tr.getAttribute('data-sug'))+1)):'';});}
 if(document.getElementById('sugTable')){
   if(!rank.length){rank=[].slice.call(document.querySelectorAll('#sugTable tbody tr')).map(function(tr){return tr.getAttribute('data-sug')});}
   document.querySelectorAll('[data-up],[data-down]').forEach(function(b){b.addEventListener('click',function(){
     var id=b.getAttribute('data-up')||b.getAttribute('data-down');var i=rank.indexOf(id);var j=b.hasAttribute('data-up')?i-1:i+1;
     if(j<0||j>=rank.length)return;var t=rank[i];rank[i]=rank[j];rank[j]=t;
     localStorage.setItem('sn_rank',JSON.stringify(rank));log('suggestion_rank',{top:rank.slice(0,5).join(',')});renderRank();
   });});
   renderRank();
   var er=document.getElementById('exportRank');
   if(er)er.addEventListener('click',function(){download('ranking.csv','rank,suggestion\n'+rank.map(function(s,i){return (i+1)+','+s}).join('\n'));});
   var rr=document.getElementById('resetRank');
   if(rr)rr.addEventListener('click',function(){localStorage.removeItem('sn_rank');location.reload();});
   var f=document.getElementById('decisionForm');
   if(f)f.addEventListener('submit',function(e){e.preventDefault();
     localStorage.setItem('sn_decision',JSON.stringify({chosen:f.chosen.value,why:f.why.value,measure:f.measure.value,t:Date.now()}));
     document.getElementById('decisionSaved').textContent='Saved locally at '+new Date().toISOString()+'. Export it with your ranking.';
   });
 }
 function download(n,c){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([c],{type:'text/csv'}));a.download=n;a.click();}
}catch(e){}})();
