/* IVO OS · V03 prototype runtime. Sample data only: nothing is sent, saved or connected. */
(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const root=document.documentElement;
/* theme */
const TK='ivo-v3-theme';
function applyTheme(t){root.setAttribute('data-theme',t);$$('[data-theme-toggle]').forEach(b=>{b.setAttribute('aria-label',t==='dark'?'Switch to light theme':'Switch to dark theme');b.setAttribute('aria-pressed',t==='light')});const m=$('meta[name=theme-color]');if(m)m.content=t==='dark'?'#0a1c26':'#f3f5f7'}
let saved=null;try{saved=localStorage.getItem(TK)}catch(e){}
applyTheme(saved||root.getAttribute('data-theme')||'dark');
document.addEventListener('click',e=>{const b=e.target.closest('[data-theme-toggle]');if(!b)return;const t=root.getAttribute('data-theme')==='dark'?'light':'dark';applyTheme(t);try{localStorage.setItem(TK,t)}catch(e){};toast(t==='dark'?'Dark theme':'Light theme','sun-moon')});

/* toasts */
const tz=$('#toasts');
function toast(msg,ic='check'){if(!tz)return;const d=document.createElement('div');d.className='toast';d.innerHTML=`<svg class="i sm" aria-hidden="true"><use href="#i-${ic}"/></svg><span></span>`;d.querySelector('span').textContent=msg;tz.appendChild(d);setTimeout(()=>{d.style.transition='opacity .3s';d.style.opacity='0';setTimeout(()=>d.remove(),320)},2600)}
window.IVO={toast};

const scrim=$('.scrim');
/* router */
const router=$('[data-router]');const seen=new Set();let first=true;
function show(id){
  if(!router)return;
  const screens=$$('[data-screen]',router);if(!screens.length)return;
  let s=screens.find(x=>x.dataset.screen===id)||screens.find(x=>x.hasAttribute('data-default'))||screens[0];
  screens.forEach(x=>x.classList.toggle('on',x===s));
  const sid=s.dataset.screen;
  $$('a[href^="#"]').forEach(a=>{if(!a.closest('.navset'))return;const h=a.getAttribute('href').slice(1);const m=(a.dataset.match||'').split(' ');const on=h===sid||m.includes(sid);a.classList.toggle('active',on);if(on)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  const dev=$('.device');if(dev)dev.classList.toggle('notab',s.hasAttribute('data-notab'));
  $$('[data-crumb]').forEach(c=>c.textContent=s.dataset.title||'');
  if(s.dataset.title)document.title=s.dataset.title+' · '+(document.body.dataset.app||'IVO OS');
  if(!first){window.scrollTo({top:0});const sc=$('.device .scr');if(sc)sc.scrollTop=0;const h=$('h1',s);if(h){h.setAttribute('tabindex','-1');h.focus({preventScroll:true})}}
  if(!seen.has(sid)&&$('[data-skel]',s)){s.classList.add('skel-on');setTimeout(()=>s.classList.remove('skel-on'),380)}
  seen.add(sid);first=false;
  s.dispatchEvent(new CustomEvent('screen:show',{bubbles:true}));
  closeSheets();
}
window.addEventListener('hashchange',()=>show(location.hash.slice(1)));
show(location.hash.slice(1));

/* sheets & scrim */
function closeSheets(){$$('.sheet.on').forEach(s=>s.classList.remove('on'));if(scrim)scrim.classList.remove('on')}
document.addEventListener('click',e=>{const o=e.target.closest('[data-sheet-open]');if(o){const sh=document.getElementById(o.dataset.sheetOpen);if(sh){sh.classList.add('on');scrim&&scrim.classList.add('on');const f=$('a,button',sh);f&&f.focus()}return}if(e.target===scrim)closeSheets()});

/* command palette */
let cmds=[];try{cmds=JSON.parse(($('#cmd-data')||{}).textContent||'[]')}catch(e){}
const dlg=$('#cmdk');let sel=0,vis=[];
function renderCmd(q){
  if(!dlg)return;const res=$('.res',dlg);q=(q||'').toLowerCase().trim();const words=q.split(/\s+/).filter(Boolean);
  vis=cmds.filter(c=>{const hay=(c.t+' '+(c.s||'')+' '+(c.g||'')).toLowerCase();return words.every(w=>hay.includes(w))});
  sel=0;let html='',g=null;
  vis.forEach((c,i)=>{if(c.g!==g){g=c.g;html+=`<div class="gh" role="presentation">${g}</div>`}html+=`<a class="it" role="option" id="cmd-${i}" href="${c.h}" aria-selected="${i===0}"><svg class="i" aria-hidden="true"><use href="#i-${c.ic||'arrow-right'}"/></svg><span>${c.t}</span><span class="sub">${c.s||''}</span></a>`});
  res.innerHTML=html||`<div class="empty"><svg class="i" aria-hidden="true"><use href="#i-search-x"/></svg><b>No match</b><span class="small">Try “bid”, “approve”, “REQ-1042” or a contractor name.</span></div>`;
  $('input',dlg).setAttribute('aria-activedescendant',vis.length?'cmd-0':'');
}
function openCmd(){if(!dlg)return;if(!dlg.open)dlg.showModal();const i=$('input',dlg);i.value='';renderCmd('');i.focus()}
function moveSel(d){const items=$$('.it',dlg);if(!items.length)return;sel=(sel+d+items.length)%items.length;items.forEach((x,i)=>x.setAttribute('aria-selected',i===sel));items[sel].scrollIntoView({block:'nearest'});$('input',dlg).setAttribute('aria-activedescendant','cmd-'+sel)}
if(dlg){const inp=$('input',dlg);inp.addEventListener('input',()=>renderCmd(inp.value));
  inp.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();moveSel(1)}else if(e.key==='ArrowUp'){e.preventDefault();moveSel(-1)}else if(e.key==='Enter'){e.preventDefault();const it=$$('.it',dlg)[sel];if(it){dlg.close();location.href=it.getAttribute('href')}}});
  dlg.addEventListener('click',e=>{if(e.target===dlg)dlg.close();if(e.target.closest('.it'))dlg.close()});}
document.addEventListener('click',e=>{if(e.target.closest('[data-cmd-open]')){e.preventDefault();openCmd()}if(e.target.closest('[data-keys-open]')){const k=$('#keys');k&&k.showModal()}});

/* keyboard */
let gWait=false,gT;
document.addEventListener('keydown',e=>{
  const tag=(e.target.tagName||'').toLowerCase();const typing=['input','textarea','select'].includes(tag)||e.target.isContentEditable;
  if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openCmd();return}
  if(e.key==='Escape'){closeSheets();const os=$('.os.cp-open');if(os&&window.innerWidth<=900)os.classList.remove('cp-open');return}
  if(typing||e.metaKey||e.ctrlKey||e.altKey)return;
  if(e.key==='/'){e.preventDefault();openCmd();return}
  if(e.key==='?'){const k=$('#keys');if(k){k.showModal()}return}
  if(e.key==='.'){toggleCopilot();return}
  if(gWait){const a=$(`[data-g="${e.key.toLowerCase()}"]`);gWait=false;if(a){e.preventDefault();a.click()}return}
  if(e.key==='g'){gWait=true;clearTimeout(gT);gT=setTimeout(()=>gWait=false,1200);return}
  const t=$('[data-screen].on [data-jk]');
  if(t&&(e.key==='j'||e.key==='k')){const rows=$$('tbody tr:not(.hide)',t);if(!rows.length)return;let i=rows.findIndex(r=>r.classList.contains('sel'));i=e.key==='j'?Math.min(rows.length-1,i+1):Math.max(0,i-1);rows.forEach(r=>r.classList.remove('sel'));rows[i].classList.add('sel');rows[i].scrollIntoView({block:'nearest'});return}
  if(t&&e.key==='Enter'){const r=$('tbody tr.sel a',t);if(r)r.click()}
});

/* copilot */
function toggleCopilot(force){const os=$('.os');if(!os||!$('.copilot',os))return;const on=force!==undefined?force:!os.classList.contains('cp-open');os.classList.toggle('cp-open',on);$$('[data-copilot-toggle]').forEach(b=>b.setAttribute('aria-expanded',on));if(on){const f=$('.copilot textarea,.copilot input');f&&f.focus({preventScroll:true})}}
document.addEventListener('click',e=>{if(e.target.closest('[data-copilot-toggle]'))toggleCopilot();const x=e.target.closest('[data-explain]');if(x){const s=x.closest('.sug');const o=s.classList.toggle('open');x.setAttribute('aria-expanded',o)}});
$$('form[data-ask]').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const i=$('textarea,input',f);const q=i.value.trim();if(!q)return;const log=$('[data-log]');const m=document.createElement('div');m.className='msg me';m.textContent=q;log.appendChild(m);i.value='';setTimeout(()=>{const r=document.createElement('div');r.className='msg';r.innerHTML='<b>Copilot:</b> I can draft that and show my reasoning with page references. Nothing goes to a customer, contractor or sub until an admin approves it. <span class="chip gold">Draft · needs approval</span>';log.appendChild(r);log.scrollTop=log.scrollHeight},500)}));

/* status actions */
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-set]');if(b){const it=b.closest('[data-item]')||b.closest('[data-screen]');const [txt,cls]=b.dataset.set.split('|');const st=it&&$('[data-status]',it);if(st){st.hidden=false;st.textContent=txt;st.className='chip '+(cls||'')}if(b.dataset.disable!=='no'){b.disabled=true}if(it&&b.dataset.hide){$$(b.dataset.hide,it).forEach(x=>x.classList.add('hide'))}if(it&&b.dataset.reveal){$$(b.dataset.reveal,it).forEach(x=>x.classList.remove('hide'))}toast(b.dataset.toast||txt,'check');const ct=$(b.dataset.dec||'_none_');if(ct){ct.textContent=Math.max(0,(+ct.textContent||0)-1)}return}
  const t=e.target.closest('[data-toast]');if(t&&!t.closest('[data-set]'))toast(t.dataset.toast,t.dataset.ic||'info');
});

/* wizards */
$$('[data-wizard]').forEach(w=>{const steps=$$('[data-step]',w);let i=0;const bar=$('.wzbar',w),cnt=$('[data-count]',w),next=$('[data-next]',w),prev=$('[data-prev]',w);
  function go(n){i=Math.max(0,Math.min(steps.length-1,n));steps.forEach((s,k)=>s.classList.toggle('on',k===i));if(bar)$$('i',bar).forEach((x,k)=>x.classList.toggle('on',k<=i));if(cnt)cnt.textContent=`Step ${i+1} of ${steps.length}`;if(prev)prev.disabled=i===0;if(next){const lab=$('span',next);if(lab)lab.textContent=i===steps.length-1?(next.dataset.finish||'Finish'):'Continue'}}
  if(next)next.addEventListener('click',()=>{if(i===steps.length-1){if(w.dataset.done)location.hash=w.dataset.done;else toast(next.dataset.toast||'Done','check')}else go(i+1)});
  if(prev)prev.addEventListener('click',()=>go(i-1));go(0)});

/* view toggles & tabs */
document.addEventListener('click',e=>{const b=e.target.closest('[data-view]');if(b){const g=b.closest('[data-views]');const scope=g.closest('[data-screen]')||document;$$('[data-view]',g).forEach(x=>x.setAttribute('aria-pressed',x===b));$$('[data-pane]',scope).forEach(p=>p.classList.toggle('hide',p.dataset.pane!==b.dataset.view));return}
  const t=e.target.closest('[data-tab]');if(t){const g=t.closest('[role=tablist]');const scope=g.closest('[data-tabscope]')||g.closest('[data-screen]')||document;$$('[data-tab]',g).forEach(x=>x.setAttribute('aria-selected',x===t));$$('[data-tabpane]',scope).forEach(p=>p.classList.toggle('hide',p.dataset.tabpane!==t.dataset.tab))}});

/* filters */
document.addEventListener('click',e=>{const b=e.target.closest('[data-filter]');if(!b)return;const g=b.closest('[data-filter-group]');const tgt=$(g.dataset.target);$$('[data-filter]',g).forEach(x=>x.setAttribute('aria-pressed',x===b));const v=b.dataset.filter;$$('[data-st]',tgt).forEach(r=>r.classList.toggle('hide',v!=='all'&&!r.dataset.st.split(' ').includes(v)))});
$$('[data-filter-input]').forEach(i=>i.addEventListener('input',()=>{const q=i.value.toLowerCase();$$('[data-st],tbody tr',$(i.dataset.target)).forEach(r=>r.classList.toggle('hide',!r.textContent.toLowerCase().includes(q)))}));

/* emergency */
document.addEventListener('screen:show',e=>{const s=e.target;const sos=$('[data-sos]',s);if(!sos)return;const live=$('[data-sos-live]',s);const cd=$('[data-sos-count]',s);let n=5;sos.classList.remove('hide');live.classList.add('hide');const ring=$('.sosring',s);cd.textContent=n;ring.style.setProperty('--p',0);clearInterval(window.__sos);window.__sos=setInterval(()=>{n--;cd.textContent=Math.max(n,0);ring.style.setProperty('--p',(5-n)*20);if(n<=0){clearInterval(window.__sos);sos.classList.add('hide');live.classList.remove('hide');toast('Emergency alert sent to IVO on-call','siren')}},1000)});
document.addEventListener('click',e=>{if(e.target.closest('[data-sos-cancel]')){clearInterval(window.__sos);toast('Emergency alert cancelled. Nothing was sent.','x');location.hash='#home'}});

/* otp */
document.addEventListener('click',e=>{const b=e.target.closest('[data-fill-otp]');if(!b)return;const s=b.closest('[data-screen]');const code=(b.dataset.fillOtp||'204816').split('');$$('.otp input',s).forEach((x,i)=>x.value=code[i]||'');toast('Code verified','shield-check');setTimeout(()=>location.hash=b.dataset.go||'#home',600)});
$$('.otp').forEach(o=>{const ins=$$('input',o);ins.forEach((x,i)=>x.addEventListener('input',()=>{if(x.value&&ins[i+1])ins[i+1].focus()}))});

/* pricing calc */
$$('[data-calc]').forEach(c=>{const base=+c.dataset.base;const fmt=n=>'$'+Math.round(n).toLocaleString('en-US');function upd(){const m=+$('[data-markup]',c).value,k=+$('[data-cont]',c).value;const mk=base*m/100,ct=base*k/100;$$('[data-out=mpct]',c).forEach(x=>x.textContent=m+'%');$$('[data-out=cpct]',c).forEach(x=>x.textContent=k+'%');$$('[data-out=markup]',c).forEach(x=>x.textContent=fmt(mk));$$('[data-out=cont]',c).forEach(x=>x.textContent=fmt(ct));$$('[data-out=total]',c).forEach(x=>x.textContent=fmt(base+mk+ct));const w=$('[data-out=winp]',c);if(w){const p=Math.max(18,Math.min(82,Math.round(78-(m-8)*4.2-(k-3)*2)));w.textContent=p+'%';const b=$('[data-out=winbar]',c);if(b)b.style.width=p+'%'}}$$('input[type=range]',c).forEach(r=>r.addEventListener('input',upd));upd();const use=$('[data-use-rec]',c);if(use)use.addEventListener('click',()=>{const f=$('[data-final]',c);f.value=$('[data-out=total]',c).textContent;toast('Recommended price copied. You still set the final number.','check')})});

/* punch list on plans */
function selPunch(scope,n){$$('[data-pin]',scope).forEach(p=>p.classList.toggle('sel',p.dataset.pin===n));$$('[data-punch]',scope).forEach(p=>p.classList.toggle('sel',p.dataset.punch===n));const li=$(`[data-punch="${n}"]`,scope);li&&li.scrollIntoView({block:'nearest'})}
document.addEventListener('click',e=>{const p=e.target.closest('[data-pin]');if(p){selPunch(p.closest('[data-punchscope]'),p.dataset.pin);return}const l=e.target.closest('[data-punch]');if(l&&!e.target.closest('input'))selPunch(l.closest('[data-punchscope]'),l.dataset.punch)});
document.addEventListener('change',e=>{const c=e.target.closest('[data-punch] input[type=checkbox]');if(!c)return;const sc=c.closest('[data-punchscope]');const n=c.closest('[data-punch]').dataset.punch;const pin=$(`[data-pin="${n}"]`,sc);pin&&pin.classList.toggle('done',c.checked);const all=$$('[data-punch] input[type=checkbox]',sc);const d=all.filter(x=>x.checked).length;$$('[data-punch-count]',sc).forEach(x=>x.textContent=`${d} of ${all.length} done`);if(c.checked)toast('Punch item closed with photo','camera')});

/* closeout builder */
$$('[data-closeout]').forEach(c=>{const req=$$('input[data-req]',c);const all=$$('input[type=checkbox]',c);function upd(){const d=all.filter(x=>x.checked).length;const p=Math.round(d/all.length*100);$$('.ring',c).forEach(r=>{r.style.setProperty('--p',p);$('span',r).textContent=p+'%'});$$('[data-co-count]',c).forEach(x=>x.textContent=`${d} of ${all.length} items`);const ok=req.every(x=>x.checked);const g=$('[data-generate]',c);if(g){g.disabled=!ok;g.setAttribute('aria-disabled',!ok)}}all.forEach(x=>x.addEventListener('change',upd));upd();const g=$('[data-generate]',c);g&&g.addEventListener('click',()=>{if(g.disabled)return;toast('Closeout package assembled. Sending it to the customer waits for admin approval.','package-check');const st=$('[data-status]',c);if(st){st.hidden=false;st.textContent='Assembled · awaiting approval';st.className='chip gold'}})});

/* before/after */
$$('.ba input').forEach(i=>i.addEventListener('input',()=>i.closest('.ba').style.setProperty('--x',i.value+'%')));

/* dispatch drag & drop */
let dragJob=null;
document.addEventListener('dragstart',e=>{const c=e.target.closest('.dragcard');if(!c)return;dragJob=c;c.classList.add('dragging');e.dataTransfer.setData('text/plain',c.dataset.job)});
document.addEventListener('dragend',()=>{if(dragJob)dragJob.classList.remove('dragging');dragJob=null;$$('.trk.over').forEach(t=>t.classList.remove('over'))});
document.addEventListener('dragover',e=>{const t=e.target.closest('.trk[data-crew]');if(t&&dragJob){e.preventDefault();$$('.trk.over').forEach(x=>x!==t&&x.classList.remove('over'));t.classList.add('over')}});
document.addEventListener('drop',e=>{const t=e.target.closest('.trk[data-crew]');if(!t||!dragJob)return;e.preventDefault();assign(dragJob.dataset.job,t.dataset.crew,dragJob)});
function assign(job,crew,card){const t=$(`.trk[data-crew="${crew}"]`);if(t){t.classList.remove('over');const b=document.createElement('div');b.className='blk gold pending';b.style.left='62%';b.style.width='22%';b.innerHTML=`<svg class="i sm" aria-hidden="true"><use href="#i-clock"/></svg>${job}`;t.appendChild(b)}if(card)card.classList.add('hide');const s=$('[data-dispatch-status]');if(s){s.hidden=false;s.textContent=`${job} → ${crew}: drafted, waiting in Approvals`}toast(`${job} assigned to ${crew} as a draft. Notifying them waits for approval.`,'calendar-check')}
document.addEventListener('click',e=>{const b=e.target.closest('[data-assign]');if(!b)return;const [j,c]=b.dataset.assign.split('|');assign(j,c,$(`.dragcard[data-job="${j}"]`));b.disabled=true});

/* map tips */
document.addEventListener('mouseover',e=>tip(e.target.closest('.pin')));document.addEventListener('focusin',e=>tip(e.target.closest('.pin')));
function tip(p){$$('.mtip').forEach(t=>t.remove());if(!p||!p.dataset.tip)return;const m=p.closest('.mapbox');const t=document.createElement('div');t.className='mtip';t.textContent=p.dataset.tip;t.style.left=p.style.left;t.style.top=`calc(${p.style.top} + 22px)`;const l=parseFloat(p.style.left);if(l>60){t.style.transform='translateX(-100%)'}m.appendChild(t)}
document.addEventListener('mouseout',e=>{if(e.target.closest('.pin'))$$('.mtip').forEach(t=>t.remove())});

/* audit verify */
document.addEventListener('click',e=>{const b=e.target.closest('[data-verify]');if(!b)return;const o=$('[data-verify-out]');const N=+b.dataset.verify;let n=0;b.disabled=true;o.innerHTML='Verifying…';const iv=setInterval(()=>{n=Math.min(N,n+Math.ceil(N/18));o.textContent=`Checking hash chain · ${n.toLocaleString()} / ${N.toLocaleString()}`;if(n>=N){clearInterval(iv);o.innerHTML=`<span class="chainok"><svg class="i sm" aria-hidden="true"><use href="#i-shield-check"/></svg>Chain intact · ${N.toLocaleString()} entries · no edits or gaps</span>`;b.disabled=false}},60)});

/* countdowns & live ago */
$$('[data-countdown]').forEach(el=>{let s=+el.dataset.countdown;const f=()=>{const d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),x=s%60;el.textContent=d?`${d}d ${h}h`:(h?`${h}:${String(m).padStart(2,'0')}:${String(x).padStart(2,'0')}`:`${m}:${String(x).padStart(2,'0')}`);if(s>0)s--};f();setInterval(f,1000)});
$$('[data-ago]').forEach(el=>{let s=2;setInterval(()=>{s=(s+1)%9;el.textContent=s<1?'just now':s+'s ago'},1000)});

/* service worker for installable apps */
if(document.body.dataset.sw&&'serviceWorker' in navigator){navigator.serviceWorker.register('sw.js').catch(()=>{})}
})();
/* doc viewer page refs + approvals split view */
(()=>{const $$=(s,r=document)=>[...r.querySelectorAll(s)];
document.addEventListener('click',e=>{const r=e.target.closest('[data-page]');if(r){const sc=r.closest('[data-screen]')||document;$$('[data-docpage]',sc).forEach(p=>p.classList.toggle('on',p.dataset.docpage===r.dataset.page));const v=sc.querySelector('.doc');if(v&&window.innerWidth<1180)v.scrollIntoView({behavior:'smooth',block:'center'});return}
const a=e.target.closest('[data-ap]');if(a){const sc=a.closest('[data-screen]');$$('[data-ap]',sc).forEach(x=>x.setAttribute('aria-selected',x===a));$$('[data-appane]',sc).forEach(p=>p.classList.toggle('hide',p.dataset.appane!==a.dataset.ap));if(window.innerWidth<1000){const p=sc.querySelector(`[data-appane="${a.dataset.ap}"]`);p&&p.scrollIntoView({behavior:'smooth'})}}
const t=e.target.closest('.toggle:not(.locked)');if(t){t.classList.toggle('on');t.setAttribute('aria-label',t.classList.contains('on')?'On':'Off')}});})();
