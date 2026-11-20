// Privacy-preserving measurement: localStorage only, no cookies/trackers. Five events are defined:
// page_view, outbound_click, guide_read, search, suggestion_rank. None is sent anywhere; there is
// no analytics endpoint configured on this site.
(function(){try{
 function download(n,c){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([c],{type:'text/csv'}));a.download=n;a.click();}
 function csvCell(v){v=String(v==null?'':v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;}
 var ev=JSON.parse(localStorage.getItem('sn_events')||'[]');
 function log(e,d){ev.push(Object.assign({e:e,t:Date.now(),page:location.pathname},d||{}));localStorage.setItem('sn_events',JSON.stringify(ev.slice(-500)));}
 log('page_view');
 if(/guides\//.test(location.pathname)) log('guide_read');
 document.querySelectorAll('[data-outbound]').forEach(function(a){a.addEventListener('click',function(){log('outbound_click',{product:a.getAttribute('data-outbound')});var c=JSON.parse(localStorage.getItem('sn_clicks')||'{}');c[a.getAttribute('data-outbound')]=(c[a.getAttribute('data-outbound')]||0)+1;localStorage.setItem('sn_clicks',JSON.stringify(c));var el=document.getElementById('localClicks');if(el)el.textContent=Object.values(c).reduce(function(x,y){return x+y},0);});});
 var ex=document.getElementById('exportClicks');if(ex)ex.addEventListener('click',function(){var c=localStorage.getItem('sn_clicks')||'{}';download('clicks.csv','product,clicks\n'+Object.entries(JSON.parse(c)).map(function(x){return x[0]+','+x[1]}).join('\n'));});
 // Search: runs entirely in the browser over the embedded index. Logs that a search ran and how
 // many results it returned — never the query words.
 var idxEl=document.getElementById('searchIndex');
 if(idxEl){
   try{
     var index=JSON.parse(idxEl.textContent);
     var params=new URLSearchParams(location.search);
     var q=(params.get('q')||'').trim().toLowerCase();
     var box=document.getElementById('results');
     var meta=document.getElementById('searchMeta');
     if(q){
       var terms=q.split(/\s+/).filter(Boolean);
       var hits=index.filter(function(it){
         var hay=(it.t+' '+it.d+' '+(it.k||'')).toLowerCase();
         return terms.every(function(t){return hay.indexOf(t)!==-1;});
       });
       if(box){
         box.innerHTML = hits.length
           ? hits.map(function(it){return '<article class="hit"><p class="where">'+(it.k||'page').replace(/</g,'&lt;')+'</p><h3><a href="'+it.u+'">'+it.t.replace(/</g,'&lt;')+'</a></h3><p>'+it.d.replace(/</g,'&lt;').slice(0,220)+'</p></article>';}).join('')
           : '<p class="small">No pages matched. Try a broader word — the index only covers this site.</p>';
       }
       if(meta) meta.textContent = hits.length+' result'+(hits.length===1?'':'s')+' for your search. Matching happened in your browser; nothing was sent anywhere.';
       log('search',{hits:hits.length});
     }
   }catch(e){/* search stays silent on malformed index */}
 }
 // Suggestions ranking
 var rank=JSON.parse(localStorage.getItem('sn_rank')||'[]');
 function renderRank(){document.querySelectorAll('#sugTable tbody tr').forEach(function(tr,i){var s=tr.querySelector('.rank');if(s)s.textContent=rank.indexOf(tr.getAttribute('data-sug'))>=0?('#'+(rank.indexOf(tr.getAttribute('data-sug'))+1)):'';});}
 if(document.getElementById('sugTable')){if(!rank.length){rank=[].slice.call(document.querySelectorAll('#sugTable tbody tr')).map(function(tr){return tr.getAttribute('data-sug')});}
 document.querySelectorAll('[data-up],[data-down]').forEach(function(b){b.addEventListener('click',function(){var id=b.getAttribute('data-up')||b.getAttribute('data-down');var i=rank.indexOf(id);var j=b.hasAttribute('data-up')?i-1:i+1;if(j<0||j>=rank.length)return;var t=rank[i];rank[i]=rank[j];rank[j]=t;localStorage.setItem('sn_rank',JSON.stringify(rank));log('suggestion_rank',{rank:rank.slice()});renderRank();});});
 renderRank();
 var er=document.getElementById('exportRank');if(er)er.addEventListener('click',function(){download('ranking.csv','rank,suggestion\n'+rank.map(function(s,i){return (i+1)+','+s}).join('\n'));});
 var rr=document.getElementById('resetRank');if(rr)rr.addEventListener('click',function(){localStorage.removeItem('sn_rank');location.reload();});
 var f=document.getElementById('decisionForm');if(f)f.addEventListener('submit',function(e){e.preventDefault();localStorage.setItem('sn_decision',JSON.stringify({chosen:f.chosen.value,why:f.why.value,measure:f.measure.value,t:Date.now()}));document.getElementById('decisionSaved').textContent='Saved locally at '+new Date().toISOString()+'. Export it with your ranking.';});}
 // Export the local event log (Disclosure & Privacy page, button #exportEvents)
 var ee=document.getElementById('exportEvents');if(ee)ee.addEventListener('click',function(){var rows=['t,event,page,detail'];ev.forEach(function(r){var d=Object.assign({},r);delete d.e;delete d.t;delete d.page;rows.push(csvCell(new Date(r.t).toISOString())+','+csvCell(r.e)+','+csvCell(r.page)+','+csvCell(JSON.stringify(d)));});download('events.csv',rows.join('\n'));});
}catch(e){}})();
