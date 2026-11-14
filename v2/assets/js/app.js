/* IVO Platform prototype V02 — sample data only; nothing is sent anywhere. */
(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
window.IVO={$,$$};

/* theme */
const root=document.documentElement;
const saved=localStorage.getItem('ivo-v2-theme');
root.setAttribute('data-theme',saved||'dark');
function setTheme(t){root.setAttribute('data-theme',t);localStorage.setItem('ivo-v2-theme',t);$$('[data-theme-toggle]').forEach(b=>b.setAttribute('aria-label',t==='dark'?'Switch to light mode':'Switch to dark mode'))}
$$('[data-theme-toggle]').forEach(b=>b.addEventListener('click',()=>setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark')));
setTheme(root.getAttribute('data-theme'));

/* toast */
const toast=document.createElement('div');toast.className='toast';toast.setAttribute('role','status');document.body.appendChild(toast);
let tt;function say(m){toast.textContent=m;toast.classList.add('show');clearTimeout(tt);tt=setTimeout(()=>toast.classList.remove('show'),2600)}
IVO.say=say;

/* screen router */
const router=$('[data-router]');
function show(id){
  if(!router)return;
  const screens=$$('[data-screen]',router);
  let target=screens.find(s=>s.dataset.screen===id)||screens[0];
  screens.forEach(s=>s.classList.toggle('on',s===target));
  const cur=target.dataset.screen;
  $$('a.nav,.tabbar a').forEach(a=>{
    const h=(a.getAttribute('href')||'').replace(/^#/,'');
    const grp=(a.dataset.match||'').split(' ');
    a.classList.toggle('active',h===cur||grp.includes(cur));
  });
  const sel=$('.mobile-jump select');if(sel)sel.value=cur;
  const sc=target.closest('.app-b')||target.querySelector('.app-b');if(sc)sc.scrollTop=0;
  $$('.app-b',target).forEach(b=>b.scrollTop=0);
  if(!target.closest('.phone'))window.scrollTo({top:0});
  $('.side')&&$('.side').classList.remove('open');
  $$('[data-note]').forEach(n=>n.hidden=!n.dataset.note.split(' ').includes(cur));
  document.dispatchEvent(new CustomEvent('screen',{detail:cur}));
}
IVO.show=show;
if(router){
  window.addEventListener('hashchange',()=>show(location.hash.slice(1)));
  show(location.hash.slice(1));
  const idx=$('.phone-index');const ban=$('.proto-banner');
  if(idx&&ban){
    const w=document.createElement('label');w.className='mobile-jump';w.innerHTML='<span>Screen:</span>';
    const sel=document.createElement('select');sel.setAttribute('aria-label','Jump to screen');
    $$('a.nav',idx).forEach(a=>{const o=document.createElement('option');o.value=a.getAttribute('href').slice(1);o.textContent=a.textContent.trim();sel.appendChild(o)});
    sel.addEventListener('change',()=>location.hash=sel.value);w.appendChild(sel);ban.appendChild(w);
    sel.value=location.hash.slice(1)||sel.options[0].value;
  }
}
const mb=$('.menu-btn');if(mb)mb.addEventListener('click',()=>$('.side').classList.toggle('open'));

/* wizards */
$$('[data-wizard]').forEach(w=>{
  const steps=$$('.wstep',w);let i=0;
  const bar=$('.steps',w),cnt=$$('[data-count]',w),lbl=$$('[data-step-label]',w);
  if(bar&&!bar.children.length)steps.forEach(()=>bar.appendChild(document.createElement('i')));
  function go(n){i=Math.max(0,Math.min(steps.length-1,n));steps.forEach((s,k)=>s.classList.toggle('on',k===i));
    if(bar)[...bar.children].forEach((b,k)=>b.classList.toggle('on',k<=i));
    cnt.forEach(c=>c.textContent=`Step ${i+1} of ${steps.length}`);
    lbl.forEach(c=>c.textContent=steps[i].dataset.label||'');
    $$('[data-prev]',w).forEach(b=>b.disabled=i===0&&!b.hasAttribute('data-exit'));
    $$('[data-next]',w).forEach(b=>{if(!b.dataset.label0)b.dataset.label0=b.textContent;b.textContent=(i===steps.length-1&&b.dataset.lastLabel)?b.dataset.lastLabel:b.dataset.label0;b.disabled=(i===steps.length-1&&!w.dataset.finish&&!b.dataset.lastLabel)});
    const sc=w.closest('.app-b');if(sc)sc.scrollTop=0;}
  w.addEventListener('click',e=>{
    const n=e.target.closest('[data-next]'),p=e.target.closest('[data-prev]'),g=e.target.closest('[data-goto]');
    if(n&&w.contains(n)){e.preventDefault();if(i===steps.length-1&&w.dataset.finish){if(n.dataset.toastLast)say(n.dataset.toastLast);location.hash=w.dataset.finish;setTimeout(()=>go(0),300)}else go(i+1)}
    else if(p&&w.contains(p)){e.preventDefault();go(i-1)}
    else if(g&&w.contains(g)){e.preventDefault();go(+g.dataset.goto)}
  });
  w._go=go;go(0);
  document.addEventListener('screen',ev=>{if(w.closest('[data-screen]')&&w.closest('[data-screen]').dataset.screen===ev.detail&&w.hasAttribute('data-reset'))go(0)});
});

/* option pills / tabs / toggles */
$$('.opts,.tiles').forEach(g=>g.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b||!g.contains(b))return;e.preventDefault();
  if(g.hasAttribute('data-multi'))b.classList.toggle('on');else{$$('button',g).forEach(x=>x.classList.toggle('on',x===b))}
  if(b.dataset.show){$$(b.dataset.group||'[data-optpane]').forEach(p=>p.hidden=p.dataset.optpane!==b.dataset.show)}
}));
$$('[data-tabset]').forEach(ts=>{
  const btns=$$('[data-tab]',ts),panes=$$('[data-pane]',ts);
  function sel(k){btns.forEach(b=>{b.classList.toggle('on',b.dataset.tab===k);b.setAttribute('aria-selected',b.dataset.tab===k)});panes.forEach(p=>p.hidden=p.dataset.pane!==k)}
  btns.forEach(b=>b.addEventListener('click',e=>{e.preventDefault();sel(b.dataset.tab)}));
  if(btns[0])sel((btns.find(b=>b.classList.contains('on'))||btns[0]).dataset.tab);
});
$$('.toggle').forEach(t=>t.addEventListener('click',()=>{t.classList.toggle('on');t.setAttribute('aria-pressed',t.classList.contains('on'))}));

/* generic actions */
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-toast],[data-set],[data-hide-item],[data-go],[data-modal],[data-close],[data-add-thumb],[data-add-file],[data-cmd-open]');
  if(!b)return;
  if(b.dataset.modal){e.preventDefault();$(b.dataset.modal).classList.add('on')}
  if(b.hasAttribute('data-close')){e.preventDefault();b.closest('.modal').classList.remove('on')}
  if(b.dataset.set){const it=b.closest('[data-item]');if(it){const [txt,cls]=b.dataset.set.split('|');const st=$('[data-status]',it);if(st){st.textContent=txt;st.className='chip '+(cls||'');st.hidden=false}
      $$('[data-set],[data-hide-on-set]',it).forEach(x=>{if(x.closest('[data-item]')===it&&!x.hasAttribute('data-keep'))x.style.display='none'});
      const done=$('[data-done]',it);if(done)done.hidden=false;}}
  if(b.hasAttribute('data-hide-item')){const it=b.closest('[data-item]');if(it){it.style.transition='.3s';it.style.opacity='.35'}}
  if(b.hasAttribute('data-add-thumb')){const t=$(b.dataset.addThumb);if(t){const imgs=['ivo-05','ivo-36','ivo-51','ivo-76','ivo-99','ivo-113'];const d=document.createElement('div');d.className='thumb';d.style.backgroundImage=`url(${b.dataset.base||'../'}assets/img/${imgs[t.children.length%imgs.length]}.webp)`;d.innerHTML='<span>sample</span>';t.appendChild(d)}}
  if(b.hasAttribute('data-add-file')){const t=$(b.dataset.addFile);if(t){const names=['Floor-plan_sample.pdf','Scope-notes_sample.docx','Moisture-readings_sample.xlsx','Site-video_sample.mp4'];const n=names[t.children.length%names.length];const ext=n.split('.').pop().toUpperCase();const d=document.createElement('div');d.className='file';d.innerHTML=`<span class="ic">${ext}</span><span class="grow">${n}</span><span class="chip ok">Uploaded</span>`;t.appendChild(d)}}
  if(b.hasAttribute('data-cmd-open')){e.preventDefault();openCmd()}
  if(b.dataset.toast)say(b.dataset.toast);
  if(b.dataset.go){e.preventDefault();const g=b.dataset.go;setTimeout(()=>{location.hash=g},b.dataset.toast?350:0)}
});

/* OTP */
$$('.otp').forEach(o=>{const ins=$$('input',o);ins.forEach((inp,k)=>{inp.addEventListener('input',()=>{inp.value=inp.value.replace(/\D/g,'').slice(-1);if(inp.value&&ins[k+1])ins[k+1].focus();
  if(ins.every(x=>x.value)&&o.dataset.then){say('Code accepted (prototype)');setTimeout(()=>location.hash=o.dataset.then,400)}})})});
$$('[data-fill-otp]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();const o=$(b.dataset.fillOtp);$$('input',o).forEach((x,k)=>x.value='204816'[k]);say('Sample code filled in');if(o.dataset.then)setTimeout(()=>location.hash=o.dataset.then,500)}));

/* SLA countdowns */
const slas=$$('[data-sla]');const t0=Date.now();
function fmt(m){const neg=m<0;m=Math.abs(m);const h=Math.floor(m/60),mm=Math.floor(m%60),ss=Math.floor((m*60)%60);return (neg?'-':'')+(h?h+'h ':'')+String(mm).padStart(h?2:1,'0')+'m '+String(ss).padStart(2,'0')+'s'}
function tick(){const el=(Date.now()-t0)/60000;slas.forEach(s=>{const m=parseFloat(s.dataset.sla)-el;s.querySelector('.v')?s.querySelector('.v').textContent=fmt(m):s.textContent=fmt(m);s.classList.toggle('bad',m<0);s.classList.toggle('warn',m>=0&&m<(parseFloat(s.dataset.warn)||30))})}
if(slas.length){tick();setInterval(tick,1000)}

/* NTE calculator */
$$('[data-nte]').forEach(box=>{const nte=+box.dataset.nte,spent=+box.dataset.spent;const inp=$('input',box),out=$('[data-nte-out]',box),bar=$('.prog i',box);
  function upd(){const v=+(inp.value||0),tot=spent+v,pct=Math.min(100,tot/nte*100);if(bar){bar.style.width=pct+'%';bar.parentElement.className='prog '+(tot>nte?'bad':pct>85?'warn':'ok')}
    if(out)out.innerHTML=tot>nte?`<b>$${tot.toLocaleString()}</b> would exceed the $${nte.toLocaleString()} not-to-exceed by $${(tot-nte).toLocaleString()}. A change order must be approved by the customer first.`:`<b>$${tot.toLocaleString()}</b> of $${nte.toLocaleString()} not-to-exceed. Within the approved limit.`}
  if(inp){inp.addEventListener('input',upd);upd()}});

/* hold-to-confirm emergency */
$$('[data-hold]').forEach(b=>{let tm,st;const lab=$('.hl',b),orig=lab?lab.textContent:'';
  const start=e=>{e.preventDefault();st=Date.now();b.style.setProperty('--p','0');tm=setInterval(()=>{const p=Math.min(1,(Date.now()-st)/1200);b.style.setProperty('--p',p);if(lab)lab.textContent=p<1?'Keep holding…':'Sending…';if(p>=1){clearInterval(tm);location.hash=b.dataset.hold}},50)};
  const stop=()=>{clearInterval(tm);b.style.setProperty('--p','0');if(lab&&location.hash.slice(1)!==b.dataset.hold)lab.textContent=orig};
  b.addEventListener('pointerdown',start);['pointerup','pointerleave','pointercancel'].forEach(ev=>b.addEventListener(ev,stop));
  b.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();location.hash=b.dataset.hold}});
});

/* table filters */
$$('[data-filter-group]').forEach(g=>{const tgt=$(g.dataset.filterGroup);g.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;$$('button',g).forEach(x=>x.classList.toggle('on',x===b));
  $$('[data-f]',tgt).forEach(r=>r.hidden=!(b.dataset.f==='all'||r.dataset.f.split(' ').includes(b.dataset.f)))})});

/* command bar */
const cmd=$('#cmdk');
function openCmd(){if(!cmd)return;cmd.classList.add('on');const inp=$('input',cmd);filterCmd('');if(inp){inp.value='';inp.focus()}setSel(0)}
function closeCmd(){if(cmd)cmd.classList.remove('on')}
function items(){return $$('#cmdk-results [data-cmd]').filter(x=>x.style.display!=='none')}
function setSel(i){const list=items();list.forEach((el,k)=>el.setAttribute('aria-selected',k===i?'true':'false'))}
function filterCmd(q){q=q.toLowerCase().trim();$$('#cmdk-results [data-cmd]').forEach(el=>{
  const hay=(el.dataset.cmd+' '+(el.textContent||'')).toLowerCase();el.style.display=!q||hay.includes(q)?'':'none'});setSel(0)}
if(cmd){
  const inp=$('input',cmd);
  inp&&inp.addEventListener('input',()=>filterCmd(inp.value));
  cmd.addEventListener('click',e=>{if(e.target===cmd)closeCmd();const b=e.target.closest('[data-cmd]');if(!b)return;
    const href=b.getAttribute('data-href');closeCmd();if(href){if(href.startsWith('#'))location.hash=href;else location.href=href}});
}
window.addEventListener('keydown',e=>{
  const k=e.key,meta=e.metaKey||e.ctrlKey;
  if(meta&&(k==='k'||k==='K')){e.preventDefault();cmd&&cmd.classList.contains('on')?closeCmd():openCmd();return}
  if(k==='Escape'&&cmd&&cmd.classList.contains('on')){e.preventDefault();closeCmd();return}
  if(cmd&&cmd.classList.contains('on')){
    const list=items();const cur=list.findIndex(x=>x.getAttribute('aria-selected')==='true');
    if(k==='ArrowDown'||k==='ArrowUp'){e.preventDefault();const n=k==='ArrowDown'?Math.min(list.length-1,cur+1):Math.max(0,cur-1);setSel(n);list[n]&&list[n].scrollIntoView({block:'nearest'});}
    if(k==='Enter'&&list[Math.max(0,cur)]){e.preventDefault();list[Math.max(0,cur)].click()}
    return;
  }
  /* triage board shortcuts when on #triage and not typing */
  if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName))return;
  const onTriage=location.hash.replace('#','')==='triage'||($('[data-screen].on')&&$('[data-screen].on').dataset.screen==='triage');
  if(onTriage){
    const cards=$$('[data-board-item]');
    let i=cards.findIndex(c=>c.classList.contains('sel'));if(i<0)i=0;
    if(k==='j'||k==='J'||k==='ArrowDown'){e.preventDefault();cards.forEach(c=>c.classList.remove('sel'));cards[Math.min(cards.length-1,i+1)]?.classList.add('sel');cards[Math.min(cards.length-1,i+1)]?.scrollIntoView({block:'nearest'})}
    if(k==='k'||k==='K'||k==='ArrowUp'){e.preventDefault();cards.forEach(c=>c.classList.remove('sel'));cards[Math.max(0,i-1)]?.classList.add('sel');cards[Math.max(0,i-1)]?.scrollIntoView({block:'nearest'})}
    if(k==='Enter'){const s=$('[data-board-item].sel [data-open]');if(s){e.preventDefault();s.click()}}
    if(k==='?'||(e.shiftKey&&k==='/')){e.preventDefault();say('Triage keys: J/K move · Enter open · 1 confirm type · 2 pick path')}
    if(k==='1'){const b=$('[data-board-item].sel [data-toast]');if(b){e.preventDefault();b.click()}}
  }
});

/* swipe to accept / decline */
$$('[data-swipe]').forEach(card=>{
  let x0=0,dx=0,drag=false;
  const yes=$('.swipe-hint.yes',card),no=$('.swipe-hint.no',card);
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function end(){card.classList.remove('dragging');
    if(Math.abs(dx)>90){const ok=dx>0;card.style.transform=`translateX(${ok?420:-420}px)`;card.style.opacity='0';
      say(ok?(card.dataset.swipeYes||'Accepted (prototype)'):(card.dataset.swipeNo||'Declined (prototype)'));
      const go=ok?card.dataset.goYes:card.dataset.goNo;setTimeout(()=>{if(go)location.hash=go;else{card.style.transform='';card.style.opacity='';}},280)}
    else{card.style.transform='';if(yes)yes.style.opacity=0;if(no)no.style.opacity=0}
    drag=false;dx=0}
  card.addEventListener('pointerdown',e=>{if(e.target.closest('a,button'))return;drag=true;x0=e.clientX;dx=0;card.classList.add('dragging');card.setPointerCapture(e.pointerId)});
  card.addEventListener('pointermove',e=>{if(!drag)return;dx=e.clientX-x0;if(reduced)return;card.style.transform=`translateX(${dx}px) rotate(${dx/40}deg)`;
    if(yes)yes.style.opacity=Math.max(0,Math.min(1,dx/90));if(no)no.style.opacity=Math.max(0,Math.min(1,-dx/90))});
  card.addEventListener('pointerup',end);card.addEventListener('pointercancel',end);
});

/* map pin clicks */
$$('[data-map-go]').forEach(p=>p.addEventListener('click',()=>{const h=p.dataset.mapGo;if(h)location.hash=h}));

if('serviceWorker' in navigator&&document.querySelector('link[rel=manifest]')){navigator.serviceWorker.register('sw.js').catch(()=>{})}
})();
