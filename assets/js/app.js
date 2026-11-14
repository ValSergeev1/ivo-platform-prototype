/* IVO Platform prototype V01 — tiny UI kit. Sample data only; nothing is sent anywhere. */
(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
window.IVO={$,$$};

/* toast */
const toast=document.createElement('div');toast.className='toast';toast.setAttribute('role','status');document.body.appendChild(toast);
let tt;function say(m){toast.textContent=m;toast.classList.add('show');clearTimeout(tt);tt=setTimeout(()=>toast.classList.remove('show'),2600)}
IVO.say=say;

/* screen router: one [data-router] per page; links href="#id" */
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
  // mobile screen jumper built from the phone index (phone pages only)
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

/* wizards: [data-wizard] > .wstep ; [data-next] [data-prev] [data-goto=n]; .steps i auto */
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

/* option pills / tiles: single select unless data-multi */
$$('.opts,.tiles').forEach(g=>g.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b||!g.contains(b))return;e.preventDefault();
  if(g.hasAttribute('data-multi'))b.classList.toggle('on');else{$$('button',g).forEach(x=>x.classList.toggle('on',x===b))}
  if(b.dataset.show){$$(b.dataset.group||'[data-optpane]').forEach(p=>p.hidden=p.dataset.optpane!==b.dataset.show)}
}));

/* tabs: [data-tabs] buttons[data-tab] -> [data-pane] siblings within closest [data-tabset] */
$$('[data-tabset]').forEach(ts=>{
  const btns=$$('[data-tab]',ts),panes=$$('[data-pane]',ts);
  function sel(k){btns.forEach(b=>{b.classList.toggle('on',b.dataset.tab===k);b.setAttribute('aria-selected',b.dataset.tab===k)});panes.forEach(p=>p.hidden=p.dataset.pane!==k)}
  btns.forEach(b=>b.addEventListener('click',e=>{e.preventDefault();sel(b.dataset.tab)}));
  sel((btns.find(b=>b.classList.contains('on'))||btns[0]).dataset.tab);
});

/* toggles */
$$('.toggle').forEach(t=>t.addEventListener('click',()=>{t.classList.toggle('on');t.setAttribute('aria-pressed',t.classList.contains('on'))}));

/* generic actions
   data-toast="msg"                     -> toast
   data-set="text|chipclass" + data-target(closest selector) -> sets [data-status] chip inside item
   data-hide-item                        -> fades the closest [data-item]
   data-go="#screen"                     -> navigate after action
   data-modal="#id" / data-close         -> modals */
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-toast],[data-set],[data-hide-item],[data-go],[data-modal],[data-close],[data-add-thumb],[data-add-file]');
  if(!b)return;
  if(b.matches('a[href^="#"]')&&!b.dataset.go){}else if(b.tagName==='A'&&!b.getAttribute('href'))e.preventDefault();
  if(b.dataset.modal){e.preventDefault();$(b.dataset.modal).classList.add('on')}
  if(b.hasAttribute('data-close')){e.preventDefault();b.closest('.modal').classList.remove('on')}
  if(b.dataset.set){const it=b.closest('[data-item]');if(it){const [txt,cls]=b.dataset.set.split('|');const st=$('[data-status]',it);if(st){st.textContent=txt;st.className='chip '+(cls||'');st.hidden=false}
      $$('[data-set],[data-hide-on-set]',it).forEach(x=>{if(x.closest('[data-item]')===it&&!x.hasAttribute('data-keep'))x.style.display='none'});
      const done=$('[data-done]',it);if(done)done.hidden=false;}}
  if(b.hasAttribute('data-hide-item')){const it=b.closest('[data-item]');if(it){it.style.transition='.3s';it.style.opacity='.35'}}
  if(b.hasAttribute('data-add-thumb')){const t=$(b.dataset.addThumb);if(t){const imgs=['ivo-05','ivo-36','ivo-51','ivo-76','ivo-99','ivo-113'];const d=document.createElement('div');d.className='thumb';d.style.backgroundImage=`url(${b.dataset.base||'../'}assets/img/${imgs[t.children.length%imgs.length]}.webp)`;d.innerHTML='<span>sample</span>';t.appendChild(d)}}
  if(b.hasAttribute('data-add-file')){const t=$(b.dataset.addFile);if(t){const names=['Floor-plan_sample.pdf','Scope-notes_sample.docx','Moisture-readings_sample.xlsx','Site-video_sample.mp4'];const n=names[t.children.length%names.length];const ext=n.split('.').pop().toUpperCase();const d=document.createElement('div');d.className='file';d.innerHTML=`<span class="ic">${ext}</span><span class="grow">${n}</span><span class="chip ok">Uploaded</span>`;t.appendChild(d)}}
  if(b.dataset.toast)say(b.dataset.toast);
  if(b.dataset.go){e.preventDefault();const g=b.dataset.go;setTimeout(()=>{location.hash=g},b.dataset.toast?350:0)}
});

/* OTP: auto-advance */
$$('.otp').forEach(o=>{const ins=$$('input',o);ins.forEach((inp,k)=>{inp.addEventListener('input',()=>{inp.value=inp.value.replace(/\D/g,'').slice(-1);if(inp.value&&ins[k+1])ins[k+1].focus();
  if(ins.every(x=>x.value)&&o.dataset.then){say('Code accepted (prototype)');setTimeout(()=>location.hash=o.dataset.then,400)}})})});
$$('[data-fill-otp]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();const o=$(b.dataset.fillOtp);$$('input',o).forEach((x,k)=>x.value='204816'[k]);say('Sample code filled in');if(o.dataset.then)setTimeout(()=>location.hash=o.dataset.then,500)}));

/* live SLA countdowns: data-sla="minutes remaining" (negative = overdue) */
const slas=$$('[data-sla]');const t0=Date.now();
function fmt(m){const neg=m<0;m=Math.abs(m);const h=Math.floor(m/60),mm=Math.floor(m%60),ss=Math.floor((m*60)%60);return (neg?'-':'')+(h?h+'h ':'')+String(mm).padStart(h?2:1,'0')+'m '+String(ss).padStart(2,'0')+'s'}
function tick(){const el=(Date.now()-t0)/60000;slas.forEach(s=>{const m=parseFloat(s.dataset.sla)-el;s.querySelector('.v')?s.querySelector('.v').textContent=fmt(m):s.textContent=fmt(m);s.classList.toggle('bad',m<0);s.classList.toggle('warn',m>=0&&m<(parseFloat(s.dataset.warn)||30))})}
if(slas.length){tick();setInterval(tick,1000)}

/* NTE calculator (change orders) */
$$('[data-nte]').forEach(box=>{const nte=+box.dataset.nte,spent=+box.dataset.spent;const inp=$('input',box),out=$('[data-nte-out]',box),bar=$('.prog i',box);
  function upd(){const v=+(inp.value||0),tot=spent+v,pct=Math.min(100,tot/nte*100);bar.style.width=pct+'%';bar.parentElement.className='prog '+(tot>nte?'bad':pct>85?'warn':'ok');
    out.innerHTML=tot>nte?`<b>$${tot.toLocaleString()}</b> would exceed the $${nte.toLocaleString()} not-to-exceed by $${(tot-nte).toLocaleString()}. A change order must be approved by the customer first.`:`<b>$${tot.toLocaleString()}</b> of $${nte.toLocaleString()} not-to-exceed. Within the approved limit.`}
  inp.addEventListener('input',upd);upd()});

/* hold-to-confirm emergency */
$$('[data-hold]').forEach(b=>{let tm,st;const lab=$('.hl',b),orig=lab?lab.textContent:'';
  const start=e=>{e.preventDefault();st=Date.now();b.style.setProperty('--p','0');tm=setInterval(()=>{const p=Math.min(1,(Date.now()-st)/1200);if(lab)lab.textContent=p<1?'Keep holding…':'Sending…';if(p>=1){clearInterval(tm);location.hash=b.dataset.hold}},50)};
  const stop=()=>{clearInterval(tm);if(lab&&location.hash.slice(1)!==b.dataset.hold)lab.textContent=orig};
  b.addEventListener('pointerdown',start);['pointerup','pointerleave','pointercancel'].forEach(ev=>b.addEventListener(ev,stop));
  b.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();location.hash=b.dataset.hold}});
});

/* filter chips for tables: [data-filter-group] buttons data-f -> rows [data-f] */
$$('[data-filter-group]').forEach(g=>{const tgt=$(g.dataset.filterGroup);g.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;$$('button',g).forEach(x=>x.classList.toggle('on',x===b));
  $$('[data-f]',tgt).forEach(r=>r.hidden=!(b.dataset.f==='all'||r.dataset.f.split(' ').includes(b.dataset.f)))})});

/* PWA: register service worker if present at scope */
if('serviceWorker' in navigator&&document.querySelector('link[rel=manifest]')){navigator.serviceWorker.register('sw.js').catch(()=>{})}
})();
