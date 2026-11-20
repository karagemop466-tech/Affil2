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
 function download(n,c){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([c],{type:'text/csv'}));a.download=n;a.click();}
}catch(e){}})();
// nav toggle for small screens (was styled but never wired)
(function(){var b=document.querySelector('.navtoggle'),n=document.getElementById('primary-nav');
 if(!b||!n)return;
 b.addEventListener('click',function(){var open=n.classList.toggle('open');
 b.setAttribute('aria-expanded',open?'true':'false');});})();

// search page: run the query, render results, record the 'search' event
(function(){
 var idxEl=document.getElementById('searchIndex');if(!idxEl)return;
 var data=[];try{data=JSON.parse(idxEl.textContent||'[]');}catch(e){return;}
 var box=document.getElementById('results'),meta=document.getElementById('searchMeta');
 var input=document.getElementById('sq');
 function norm(t){return (t||'').toLowerCase();}
 function run(){
  var q=norm(new URLSearchParams(location.search).get('q')||'').trim();
  if(input&&q)input.value=q;
  if(!q){box.innerHTML='';return;}
  var terms=q.split(/\s+/).filter(Boolean);
  var hits=data.map(function(d){
    var hay=norm(d.t)+' '+norm(d.d)+' '+norm(d.k),score=0;
    terms.forEach(function(t){
      if(norm(d.t).indexOf(t)>=0)score+=6;
      if(norm(d.k).indexOf(t)>=0)score+=2;
      if(hay.indexOf(t)>=0)score+=1;
    });
    return {d:d,score:score};
  }).filter(function(r){return r.score>0}).sort(function(a,b){return b.score-a.score}).slice(0,12);
  if(!hits.length){box.innerHTML='<p class="small">No match for &ldquo;'+q.replace(/[<>&]/g,'')+'&rdquo;. Try a shorter word: capacity, wireless, baskets, 450.</p>';return;}
  box.innerHTML=hits.map(function(r){
    return '<div class="hit"><p class="where">'+r.d.k+'</p><h3><a href="'+r.d.u+'">'+r.d.t+'</a></h3><p>'+(r.d.d||'').slice(0,180)+'&hellip;</p></div>';
  }).join('');
  try{var ev=JSON.parse(localStorage.getItem('sn_events')||'[]');
   ev.push({e:'search',t:Date.now(),page:location.pathname,q:q,hits:hits.length});
   localStorage.setItem('sn_events',JSON.stringify(ev.slice(-500)));}catch(e){}
 }
 if(meta)meta.textContent=meta.textContent.replace('{n}',data.length);
 run();
})();
