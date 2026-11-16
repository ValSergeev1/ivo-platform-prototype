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

/* Field tools: property switcher, job feed, gallery, plan markup, voice notes. Sample data only. */
(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const toast=(msg,ic)=>window.IVO&&window.IVO.toast(msg,ic);

/* ---------- property chips + feed filters + unread ---------- */
const home=$('[data-places]');
if(home){
  const heros=$$('[data-phero]',home);
  const cards=$$('[data-place]',home);
  const happening=$('[data-place-block]',home);
  function showPlace(id){
    $$('.chip-btn',home).forEach(b=>b.setAttribute('aria-pressed',b.dataset.place===id?'true':'false'));
    const heroId=id==='all'?'cedar':id;
    heros.forEach(h=>h.classList.toggle('hide',h.dataset.phero!==heroId));
    const f=$('[data-feed-filter]',home);
    const kind=f?$$('[data-filter]',f).find(x=>x.getAttribute('aria-pressed')==='true')?.dataset.filter||'all':'all';
    cards.forEach(c=>{
      const placeOk=id==='all'||c.dataset.place===id;
      const kindOk=kind==='all'||(c.dataset.kind||'').split(' ').includes(kind);
      c.classList.toggle('hide',!(placeOk&&kindOk));
    });
    if(happening)happening.classList.toggle('hide',id==='harbor');
  }
  home.addEventListener('click',e=>{
    const b=e.target.closest('[data-place].chip-btn, .chip-btn[data-place]');
    if(b&&b.closest('[data-places]')){showPlace(b.dataset.place);return}
  });
  const fg=$('[data-feed-filter]',home);
  if(fg)fg.addEventListener('click',e=>{
    const b=e.target.closest('[data-filter]');if(!b)return;
    $$('[data-filter]',fg).forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
    const cur=$$('.chip-btn[aria-pressed="true"]',home)[0];
    showPlace(cur?cur.dataset.place:'cedar');
  });
  home.addEventListener('click',e=>{
    const link=e.target.closest('.fcard.fresh .fcard-link');
    if(!link)return;
    const card=link.closest('.fcard');
    card.classList.remove('fresh');
    const chip=$('.chip.fresh-chip, .chip.gold.fresh-mark, [data-new]',card);
    if(chip)chip.remove();
  });
  /* A clearly fake late update appears once on home so the unread mark can be tried. */
  const live=$('[data-feed-live]',home);
  if(live){
    let armed=false;
    function armLive(){
      if(armed)return;armed=true;
      setTimeout(()=>{
        const on=$('[data-screen="home"].on');if(!on)return;
        const list=$('.feed-list',home);if(!list||list.querySelector('[data-live-added]'))return;
        const node=live.content&&live.content.firstElementChild?live.content.firstElementChild.cloneNode(true):null;
        if(!node)return;
        node.setAttribute('data-live-added','');
        list.prepend(node);
        const a=$('[data-feed-announce]',home);
        if(a)a.textContent='1 new update';
        toast('New job update: crew left the site','map-pin');
      },7000);
    }
    if($('[data-screen="home"].on'))armLive();
    document.addEventListener('screen:show',e=>{if(e.target&&e.target.dataset.screen==='home')armLive()});
  }
}

/* Gallery: cover, pin, remove, local add — stays on this phone only. */
$$('[data-gallery]').forEach(g=>{
  g.addEventListener('click',e=>{
    const cover=e.target.closest('[data-cover]');
    if(cover){
      $$('figure',cover.closest('.gallery')||g).forEach(f=>f.classList.remove('cover'));
      cover.closest('figure').classList.add('cover');
      toast('Cover photo updated','star');return;
    }
    const pin=e.target.closest('[data-pin-photo]');
    if(pin){
      const src=pin.closest('figure');
      const mine=$('[data-mine]',g);
      if(mine&&src){
        const clone=src.cloneNode(true);
        const cap=$('figcaption',clone);
        if(cap)cap.innerHTML=`<span class="grow ell">Pinned just now</span><button type="button" class="btn ghost icon" data-cover aria-label="Make this the cover photo"><svg class="i sm" aria-hidden="true"><use href="#i-star"/></svg></button><button type="button" class="btn ghost icon" data-remove aria-label="Remove from gallery"><svg class="i sm" aria-hidden="true"><use href="#i-trash-2"/></svg></button>`;
        mine.appendChild(clone);
        src.remove();
        toast('Pinned to your photos','pin');
      }
      return;
    }
    const rm=e.target.closest('[data-remove]');
    if(rm){rm.closest('figure').remove();toast('Removed from the gallery','trash-2')}
  });
  const inp=$('[data-add-photos]',g);
  if(inp)inp.addEventListener('change',()=>{
    const mine=$('[data-mine]',g);if(!mine)return;
    [...inp.files||[]].forEach(f=>{
      if(!f.type.startsWith('image/'))return;
      const url=URL.createObjectURL(f);
      const fig=document.createElement('figure');
      fig.innerHTML=`<img src="${url}" alt="Photo added in this preview"><figcaption><span class="grow ell">Added in this preview</span><button type="button" class="btn ghost icon" data-cover aria-label="Make this the cover photo"><svg class="i sm" aria-hidden="true"><use href="#i-star"/></svg></button><button type="button" class="btn ghost icon" data-remove aria-label="Remove from gallery"><svg class="i sm" aria-hidden="true"><use href="#i-trash-2"/></svg></button></figcaption>`;
      mine.appendChild(fig);
    });
    inp.value='';
    toast('Photo added','image-plus');
  });
});

/* ---------- plan markup (finger/stylus drawing on a sample plan) ---------- */
const HEX={red:'#d62828',orange:'#e8590c',yellow:'#f5c400',green:'#2b9348',blue:'#1d6fd8',navy:'#061d2a',black:'#111111',white:'#ffffff'};
const SAMPLE_SHAPES=[
  {t:'arrow',color:'red',width:4,from:[0.42,0.28],to:[0.55,0.42]},
  {t:'rect',color:'orange',width:3,a:[0.30,0.20],b:[0.48,0.40]},
  {t:'text',color:'navy',size:18,at:[0.31,0.18],text:'Patch opening'},
  {t:'pin',at:[0.70,0.62],title:'Final paint after dry',n:'3'}
];
function clone(s){return JSON.parse(JSON.stringify(s))}
$$('[data-markup]').forEach(root=>{
  const stage=$('.mk-stage',root),sheet=$('.mk-sheet',root),canvas=$('canvas.mk-layer',root),hit=$('.mk-hit',root);
  if(!stage||!sheet||!canvas||!hit)return;
  const ctx=canvas.getContext('2d');
  let tool='pen',color='red',shapes=clone(SAMPLE_SHAPES),undo=[],redo=[],draft=null,pinN=6;
  const versions=[{id:'v1',name:'Version 1 · Ana Kim',when:'This morning (sample)',shapes:clone(SAMPLE_SHAPES)},{id:'v2',name:'Version 2 · Sam Rivera',when:'Saved 2 hours ago (sample)',shapes:clone(SAMPLE_SHAPES).concat([{t:'highlighter',color:'yellow',width:18,points:[[0.18,0.68],[0.28,0.72],[0.40,0.74]]}])}];
  let current='v1',dirty=false;
  const ask=$('.mk-ask',root),askKind=$('[data-ask-kind]',root),askInput=$('[data-ask-text]',root);
  let askAt=null,penSeen=0;

  function size(){
    const r=sheet.getBoundingClientRect();
    const d=Math.max(1,window.devicePixelRatio||1);
    canvas.width=Math.round(r.width*d);
    canvas.height=Math.round(r.height*d);
    canvas.style.width=r.width+'px';
    canvas.style.height=r.height+'px';
    hit.style.width=r.width+'px';
    hit.style.height=r.height+'px';
    draw();
  }
  function pt(e){
    const r=canvas.getBoundingClientRect();
    return [(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height];
  }
  function stroke(c,w){ctx.lineWidth=w*(canvas.width/400);ctx.strokeStyle=HEX[c]||c;ctx.fillStyle=HEX[c]||c;ctx.lineCap='round';ctx.lineJoin='round'}
  function px(p){return[p[0]*canvas.width,p[1]*canvas.height]}
  function drawArrow(from,to){
    const [x1,y1]=px(from),[x2,y2]=px(to);
    const a=Math.atan2(y2-y1,x2-x1),s=14*(canvas.width/400);
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
    ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-s*Math.cos(a-0.4),y2-s*Math.sin(a-0.4));ctx.lineTo(x2-s*Math.cos(a+0.4),y2-s*Math.sin(a+0.4));ctx.closePath();ctx.fill();
  }
  function drawShape(s){
    if(s.t==='pen'||s.t==='highlighter'){
      if(!s.points||s.points.length<1)return;
      ctx.save();
      if(s.t==='highlighter')ctx.globalAlpha=0.35;
      stroke(s.color,s.width||(s.t==='highlighter'?18:4));
      ctx.beginPath();
      s.points.forEach((p,i)=>{const [x,y]=px(p);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});
      ctx.stroke();ctx.restore();
    }else if(s.t==='arrow'){stroke(s.color,s.width||4);drawArrow(s.from,s.to)}
    else if(s.t==='rect'){
      const [x1,y1]=px(s.a),[x2,y2]=px(s.b);
      stroke(s.color,s.width||3);ctx.strokeRect(x1,y1,x2-x1,y2-y1);
    }else if(s.t==='ellipse'){
      const [x1,y1]=px(s.a),[x2,y2]=px(s.b);
      stroke(s.color,s.width||3);
      ctx.beginPath();ctx.ellipse((x1+x2)/2,(y1+y2)/2,Math.abs(x2-x1)/2,Math.abs(y2-y1)/2,0,0,Math.PI*2);ctx.stroke();
    }else if(s.t==='text'){
      const [x,y]=px(s.at),sz=(s.size||18)*(canvas.width/400);
      ctx.font=`650 ${sz}px Geist,system-ui,sans-serif`;
      ctx.lineWidth=Math.max(2,sz*0.08);
      ctx.strokeStyle=s.color==='white'?'#061d2a':'#fff';
      ctx.fillStyle=HEX[s.color];
      ctx.textBaseline='alphabetic';
      ctx.strokeText(s.text,x,y);ctx.fillText(s.text,x,y);
    }else if(s.t==='pin'){
      const [x,y]=px(s.at),r=13*(canvas.width/400);
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(x,y);
      ctx.bezierCurveTo(x+r*1.25,y-r*0.7,x+r*1.05,y-r*2.25,x,y-r*2.25);
      ctx.bezierCurveTo(x-r*1.05,y-r*2.25,x-r*1.25,y-r*0.7,x,y);
      ctx.closePath();
      ctx.fillStyle='#d62828';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=Math.max(2,r*0.15);ctx.stroke();
      ctx.fillStyle='#fff';ctx.font=`700 ${Math.round(r*0.95)}px Geist Mono,ui-monospace,monospace`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(s.n||'+',x,y-r*1.35);ctx.restore();
    }
  }
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    shapes.forEach(drawShape);
    if(draft)drawShape(draft);
  }
  function commit(next){
    undo.push(clone(shapes));if(undo.length>40)undo.shift();
    shapes=next;redo=[];dirty=true;draw();syncBtns();
  }
  function syncBtns(){
    const u=$('[data-mk-undo]',root),r=$('[data-mk-redo]',root);
    if(u)u.disabled=!undo.length;if(r)r.disabled=!redo.length;
    const lab=$('[data-mk-count]',root);
    if(lab)lab.textContent=shapes.length+' mark'+(shapes.length===1?'':'s')+' on this page';
    const cur=$('[data-version-current]',root);
    if(cur)cur.textContent=(versions.find(v=>v.id===current)||{}).name||'Unsaved';
  }
  function setTool(t){
    tool=t;
    $$('[data-mk-tool]',root).forEach(b=>b.setAttribute('aria-pressed',b.dataset.mkTool===t?'true':'false'));
    stage.classList.toggle('drawing',t!=='hand');
  }
  function setColor(c){
    color=c;
    $$('[data-mk-color]',root).forEach(b=>b.setAttribute('aria-pressed',b.dataset.mkColor===c?'true':'false'));
  }
  function openAsk(kind,at){
    askAt=at;if(!ask)return;
    ask.classList.remove('hide');
    if(askKind)askKind.textContent=kind==='pin'?'New punch item':'Text on the plan';
    if(askInput){askInput.value='';askInput.placeholder=kind==='pin'?'e.g. Seal penetration at riser':'e.g. Valve here';askInput.focus()}
    ask.dataset.mode=kind;
  }
  function closeAsk(){if(ask)ask.classList.add('hide');askAt=null}

  hit.addEventListener('pointerdown',e=>{
    if(e.pointerType==='pen')penSeen=Date.now();
    else if(e.pointerType==='touch'&&Date.now()-penSeen<1500)return;
    if(tool==='hand')return;
    e.preventDefault();
    hit.setPointerCapture(e.pointerId);
    const p=pt(e);
    if(tool==='pen'||tool==='highlighter'){
      draft={t:tool,color:tool==='highlighter'&&color==='red'?'yellow':color,width:tool==='highlighter'?18:4,points:[p]};
    }else if(tool==='arrow')draft={t:'arrow',color,width:4,from:p,to:p};
    else if(tool==='rect'||tool==='ellipse')draft={t:tool,color,width:3,a:p,b:p};
    else if(tool==='text'||tool==='pin'){openAsk(tool,p);draft=null;return}
    else if(tool==='eraser'){
      const hitI=shapes.findLastIndex(s=>{
        const pts=s.points||(s.from&&s.to?[s.from,s.to]:s.a&&s.b?[s.a,s.b]:s.at?[s.at]:[]);
        return pts.some(q=>Math.hypot(q[0]-p[0],q[1]-p[1])<0.04);
      });
      if(hitI>=0)commit(shapes.filter((_,i)=>i!==hitI));
      return;
    }
    draw();
  });
  hit.addEventListener('pointermove',e=>{
    if(!draft)return;
    const p=pt(e);
    if(draft.t==='pen'||draft.t==='highlighter')draft.points.push(p);
    else if(draft.t==='arrow')draft.to=p;
    else if(draft.t==='rect'||draft.t==='ellipse')draft.b=p;
    draw();
  });
  function endDraft(){
    if(!draft)return;
    const tooSmall=(draft.t==='arrow'&&Math.hypot(draft.to[0]-draft.from[0],draft.to[1]-draft.from[1])<0.01)
      ||((draft.t==='rect'||draft.t==='ellipse')&&Math.hypot(draft.b[0]-draft.a[0],draft.b[1]-draft.a[1])<0.01)
      ||((draft.t==='pen'||draft.t==='highlighter')&&draft.points.length<2);
    const keep=draft;draft=null;
    if(!tooSmall)commit(shapes.concat([keep]));else draw();
  }
  hit.addEventListener('pointerup',endDraft);
  hit.addEventListener('pointercancel',()=>{draft=null;draw()});

  root.addEventListener('click',e=>{
    const t=e.target.closest('[data-mk-tool]');if(t){setTool(t.dataset.mkTool);return}
    const c=e.target.closest('[data-mk-color]');if(c){setColor(c.dataset.mkColor);return}
    if(e.target.closest('[data-mk-undo]')){
      if(!undo.length)return;redo.push(clone(shapes));shapes=undo.pop();dirty=true;draw();syncBtns();return;
    }
    if(e.target.closest('[data-mk-redo]')){
      if(!redo.length)return;undo.push(clone(shapes));shapes=redo.pop();dirty=true;draw();syncBtns();return;
    }
    if(e.target.closest('[data-mk-versions-toggle]')){
      const p=$('.mk-versions',root);if(p)p.classList.toggle('hide');return;
    }
    const load=e.target.closest('[data-load-version]');
    if(load){
      const v=versions.find(x=>x.id===load.dataset.loadVersion);
      if(v){shapes=clone(v.shapes);current=v.id;undo=[];redo=[];dirty=false;draw();syncBtns();toast('Opened '+v.name,'layers')}
      const p=$('.mk-versions',root);if(p)p.classList.add('hide');
      return;
    }
    if(e.target.closest('[data-mk-save]')){
      const id='v'+(versions.length+1);
      const v={id,name:'Version '+(versions.length+1)+' · you',when:'Just now (this preview)',shapes:clone(shapes)};
      versions.push(v);current=id;dirty=false;
      renderVersions();syncBtns();
      toast('Saved as '+v.name+'. The original plan is unchanged.','save');
      return;
    }
    if(e.target.closest('[data-ask-cancel]')){closeAsk();return}
    if(e.target.closest('[data-ask-ok]')){
      const text=(askInput&&askInput.value||'').trim();
      if(ask&&ask.dataset.mode==='text'&&text&&askAt)commit(shapes.concat([{t:'text',color,size:18,at:askAt,text}]));
      if(ask&&ask.dataset.mode==='pin'&&askAt){
        const n=String(pinN++);
        commit(shapes.concat([{t:'pin',at:askAt,title:text||'Punch item',n}]));
        toast('Pin '+n+' will become a punch item when this version is saved','map-pin');
      }
      closeAsk();
    }
  });
  function renderVersions(){
    const box=$('[data-version-list]',root);if(!box)return;
    box.innerHTML=versions.map(v=>`<button class="mk-sheet-btn" type="button" data-load-version="${v.id}" aria-current="${v.id===current?'true':'false'}">
      <span class="mk-thumb" aria-hidden="true"></span>
      <span class="grow"><b>${v.name}</b><div class="small t3">${v.when}${v.id===current?' · showing':''}</div></span>
    </button>`).join('');
  }
  document.addEventListener('keydown',e=>{
    if(!root.closest('[data-screen].on'))return;
    const mod=e.metaKey||e.ctrlKey;
    if(mod&&e.key.toLowerCase()==='z'){
      e.preventDefault();
      if(e.shiftKey){if(redo.length){undo.push(clone(shapes));shapes=redo.pop();dirty=true;draw();syncBtns()}}
      else if(undo.length){redo.push(clone(shapes));shapes=undo.pop();dirty=true;draw();syncBtns()}
    }
  });
  root.addEventListener('screen:show',()=>{size();setTool(tool)});
  const ro=new ResizeObserver(size);
  ro.observe(sheet);
  setTool('pen');setColor('red');renderVersions();syncBtns();
  requestAnimationFrame(size);
});

/* ---------- voice notes (MediaRecorder, or a simulated recording) ---------- */
$$('[data-voice]').forEach(root=>{
  const MAX=180,list=$('[data-vn-list]',root),idle=$('[data-vn-idle]',root),live=$('[data-vn-live]',root),clockEl=$('[data-vn-clock]',root);
  let rec=null,stream=null,chunks=[],started=0,tick=null,simulated=false,elapsed=0;
  const fmt=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
  function setLive(on){
    if(idle)idle.classList.toggle('hide',on);
    if(live)live.classList.toggle('hide',!on);
    if(clockEl)clockEl.textContent=fmt(elapsed)+' / '+fmt(MAX);
  }
  function stopTick(){if(tick){clearInterval(tick);tick=null}}
  function addNote(opts){
    if(!list)return;
    const li=document.createElement('li');
    li.className='li vn';
    const audio=opts.url?`<audio class="vn-audio" controls preload="metadata" src="${opts.url}" aria-label="Voice note you just recorded, ${opts.len}"></audio>`:
      `<p class="xs t3">Demo recording — no microphone in this preview (${opts.len}).</p>`;
    li.innerHTML=`<div class="row gap6 wrap"><b class="grow">${opts.who||'You'}</b><span class="xs t3 mono">Just now · ${opts.len}</span></div>
      ${audio}
      ${opts.transcript?`<div class="vn-text"><p>${opts.transcript}</p></div>`:''}`;
    list.prepend(li);
  }
  async function startReal(){
    stream=await navigator.mediaDevices.getUserMedia({audio:true});
    const mime=['audio/webm;codecs=opus','audio/webm','audio/mp4'].find(m=>window.MediaRecorder&&MediaRecorder.isTypeSupported(m))||'';
    rec=new MediaRecorder(stream,mime?{mimeType:mime}:{});
    chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
    rec.onstop=()=>{
      stream&&stream.getTracks().forEach(t=>t.stop());
      const blob=new Blob(chunks,{type:(rec.mimeType||'audio/webm').split(';')[0]});
      const url=URL.createObjectURL(blob);
      addNote({url,len:fmt(elapsed),who:'You'});
      rec=null;stream=null;elapsed=0;setLive(false);
      toast('Voice note saved on this phone (preview only)','mic');
    };
    rec.start(1000);simulated=false;
  }
  function startSim(){
    simulated=true;rec={stop(){}};
  }
  async function start(){
    elapsed=0;started=Date.now();setLive(true);
    try{
      if(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia&&window.MediaRecorder)await startReal();
      else startSim();
    }catch(err){startSim()}
    stopTick();
    tick=setInterval(()=>{
      elapsed=Math.min(MAX,(Date.now()-started)/1000);
      if(clockEl)clockEl.textContent=fmt(elapsed)+' / '+fmt(MAX);
      if(elapsed>=MAX)stop();
    },200);
  }
  function stop(){
    stopTick();
    if(rec&&rec.state&&rec.state!=='inactive'&&!simulated){rec.stop();return}
    rec=null;stream&&stream.getTracks().forEach(t=>t.stop());stream=null;
    if(simulated){
      addNote({len:fmt(Math.max(1,elapsed)),who:'You',transcript:'(Sample) Ceiling opening is closed. Ready for texture — example transcript, not a real recording.'});
      toast('Sample note saved. Allow the microphone to record for real.','mic');
    }
    simulated=false;elapsed=0;setLive(false);
  }
  root.addEventListener('click',e=>{
    if(e.target.closest('[data-vn-start]')){start();return}
    if(e.target.closest('[data-vn-stop]')){stop();return}
  });
});
})();

/* Full-bleed join / sign-up stepper */
(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const C=["role","company","property","request","finish"];
const K=["role","invite","code","firm","trades","area","docs","availability","done"];
$$('[data-join]').forEach(root=>{
  let role=root.dataset.defaultRole||"customer";
  let step="role";
  const path=()=>role==="customer"?C:K;
  function show(id){
    const list=path();
    if(!list.includes(id))id=list[0];
    step=id;
    $$('[data-join-step]',root).forEach(s=>{
      const roles=(s.dataset.joinRoles||"").split(/\s+/);
      s.classList.toggle("on",roles.includes(role)&&s.dataset.joinStep===id);
    });
    $$('[data-join-rail]',root).forEach(r=>{
      const on=r.dataset.joinRail===role;
      r.hidden=!on;
      if(!on)return;
      $$('[data-join-goto]',r).forEach(b=>{
        const sid=b.dataset.joinGoto;
        const i=list.indexOf(sid),cur=list.indexOf(id);
        b.classList.toggle("current",sid===id);
        b.classList.toggle("done",i>=0&&i<cur);
      });
    });
    $$('[data-join-role]',root).forEach(b=>b.setAttribute("aria-pressed",b.dataset.joinRole===role?"true":"false"));
    const i=list.indexOf(id);
    const prev=$('[data-join-prev]',root),next=$('[data-join-next]',root);
    if(prev)prev.disabled=i<=0;
    if(next){
      const last=i===list.length-1;
      next.disabled=false;
      const lab=$('span',next);
      if(last){
        if(lab)lab.textContent=role==="customer"?"See the customer app":"Open the contractor app";
        next.dataset.finishHref=role==="customer"?"../customer/index.html#invite":"../contractor/index.html#today";
      }else{
        if(lab)lab.textContent="Continue";
        delete next.dataset.finishHref;
      }
      next.classList.remove("hide");
    }
    if(location.hash.slice(1)!==id)history.replaceState(null,"","#"+id);
    const sc=$('.join-main',root);if(sc)sc.scrollTop=0;
    window.scrollTo({top:0});
  }
  function fromHash(){
    const h=location.hash.slice(1);
    if(C.includes(h)&&h!=="role")role="customer";
    if(K.includes(h)&&h!=="role")role="contractor";
    show(h||"role");
  }
  root.addEventListener("click",e=>{
    const roleBtn=e.target.closest("[data-join-role]");
    if(roleBtn){role=roleBtn.dataset.joinRole;show("role");return}
    if(e.target.closest("[data-join-next]")){
      const next=$("[data-join-next]",root);
      if(next&&next.dataset.finishHref){location.href=next.dataset.finishHref;return}
      const list=path();const i=list.indexOf(step);
      if(i<list.length-1)show(list[i+1]);
      return;
    }
    if(e.target.closest("[data-join-prev]")){
      const list=path();const i=list.indexOf(step);
      if(i>0)show(list[i-1]);
      return;
    }
    const go=e.target.closest("[data-join-goto]");
    if(go){show(go.dataset.joinGoto);return}
    const pick=e.target.closest(".pick-card");
    if(pick){
      const group=pick.parentElement;
      if(group&&group.getAttribute("aria-label")==="Availability"){
        $$(".pick-card",group).forEach(x=>x.setAttribute("aria-pressed",x===pick?"true":"false"));
      }else{
        pick.setAttribute("aria-pressed",pick.getAttribute("aria-pressed")==="true"?"false":"true");
      }
      return;
    }
    const urg=e.target.closest(".join-step .seg button");
    if(urg){$$(".seg button",urg.closest(".seg")).forEach(x=>x.setAttribute("aria-pressed",x===urg?"true":"false"));return}
  });
  window.addEventListener("hashchange",fromHash);
  fromHash();
});
})();
