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
 var er=document.getElementById('exportRank');if(er)er.addEventListener('click',function(){download('ranking.csv','rank,suggestion\n'+rank.map(function(s,i){return (i+1)+','+s}).join('\n'));});
 var rr=document.getElementById('resetRank');if(rr)rr.addEventListener('click',function(){localStorage.removeItem('sn_rank');location.reload();});
 var f=document.getElementById('decisionForm');if(f)f.addEventListener('submit',function(e){e.preventDefault();localStorage.setItem('sn_decision',JSON.stringify({chosen:f.chosen.value,why:f.why.value,measure:f.measure.value,t:Date.now()}));document.getElementById('decisionSaved').textContent='Saved locally at '+new Date().toISOString()+'. Export it with your ranking.';});}
 var eventExport=document.getElementById('exportEvents');
 if(eventExport)eventExport.addEventListener('click',()=>{
   const rows=JSON.parse(localStorage.getItem('sn_events')||'[]');
   download('events.csv','event,utc,product,result_count\n'+rows.map(r=>[r.e,new Date(r.t).toISOString(),r.product||'',r.results??''].join(',')).join('\n'));
 });
 function download(n,c){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([c],{type:'text/csv'}));a.download=n;a.click();}
}catch(e){}})();
// Keep navigation and search operational without sending query text in a request URL.
(() => {
 const toggle=document.querySelector('.navtoggle'), nav=document.querySelector('#primary-nav');
 toggle?.addEventListener('click',()=>toggle.setAttribute('aria-expanded',nav.classList.toggle('open')));
 document.querySelectorAll('form[role="search"]').forEach(form=>{
   const field=form.querySelector('input[type="search"]');
   if(!field)return;
   form.addEventListener('submit',event=>{
     event.preventDefault();
     const query=field.value.trim().replace(/\s+/g,' ').slice(0,120);
     if(!query)return;
     try{sessionStorage.setItem('sn_search_query',query)}catch(error){
       const status=document.querySelector('#searchMeta');
       if(status)status.textContent='This browser could not start a local search session. No query was sent.';
       return;
     }
     // Search inputs have no name attribute, so a no-JavaScript form submit cannot serialize q.
     location.assign(form.getAttribute('action')||'search.html');
   });
 });
 const index=document.querySelector('#searchIndex'); if(!index)return;
 const searchField=document.querySelector('#sq');
 let q='';
 try{q=sessionStorage.getItem('sn_search_query')||'';sessionStorage.removeItem('sn_search_query')}catch(error){}
 if(searchField)searchField.value=q;
 if(!q)return;
 const tokens=q.toLowerCase().split(/\s+/), hits=JSON.parse(index.textContent).filter(x=>tokens.every(t=>(x.t+' '+x.d+' '+x.k).toLowerCase().includes(t)));
 document.querySelector('#searchMeta').textContent=hits.length?`${hits.length} matching pages`:'No matches. Try “basket”, “wireless” or “capacity”.';
 for(const hit of hits){const p=document.createElement('p'),a=document.createElement('a');a.href=hit.u;a.textContent=hit.t;p.append(a);document.querySelector('#results').append(p)}
 if(hits.length)try{const events=JSON.parse(localStorage.getItem('sn_events')||'[]');events.push({e:'search',t:Date.now(),results:hits.length});localStorage.setItem('sn_events',JSON.stringify(events.slice(-500)))}catch{}
})();

// compare page: two-at-a-time head-to-head, rendered from the embedded register view
(function(){
 var el=document.getElementById('pairData');if(!el)return;
 var data={};try{data=JSON.parse(el.textContent||'{}');}catch(e){return;}
 var a=document.getElementById('pairA'),b=document.getElementById('pairB');
 var out=document.getElementById('pairView');if(!a||!b||!out)return;
 function esc(t){return String(t==null?'':t);}
 function render(){
  var A=data[a.value],B=data[b.value];
  if(!A||!B)return;
  if(a.value===b.value){out.innerHTML='<p class="small">Pick two different products.</p>';return;}
  var rows=A.rows.map(function(r,i){
    var other=B.rows[i]?B.rows[i][1]:'';
    return '<tr><th scope="row">'+r[0]+'</th><td>'+r[1]+'</td><td>'+other+'</td></tr>';
  }).join('');
  out.innerHTML='<table class="compare pair"><caption>Same rows, same sources, two columns. '+
   'Blank-looking cells say why they are blank.</caption><thead><tr><th scope="col">Field</th>'+
   '<th scope="col"><a href="'+A.url+'">'+A.name+'</a></th>'+
   '<th scope="col"><a href="'+B.url+'">'+B.name+'</a></th></tr></thead><tbody>'+rows+'</tbody></table>'+
   '<p class="cta"><a class="btn" rel="sponsored nofollow" href="'+A.buy+'" data-outbound="pair">'+
   'Check the first on Amazon<span class="btn-sub">paid link</span></a>'+
   '<a class="btn ghost" rel="sponsored nofollow" href="'+B.buy+'" data-outbound="pair">'+
   'Check the second<span class="btn-sub">paid link</span></a></p>';
 }
 a.addEventListener('change',render);b.addEventListener('change',render);render();

})();
