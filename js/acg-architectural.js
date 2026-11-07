(()=>{
const d=document,reduced=matchMedia('(prefers-reduced-motion: reduce)');
const menu=d.querySelector('.menu-button'),navi=d.querySelector('#navigation'),nav=d.querySelector('.nav');
let closing=0;
// Menu enters from the Menu button and exits back to it (rules 10 to 12, 15).
function openMenu(){clearTimeout(closing);navi.hidden=false;navi.getBoundingClientRect();navi.classList.add('open');menu.setAttribute('aria-expanded','true');d.body.classList.add('menu-open');}
function closeMenu(){navi.classList.remove('open');menu.setAttribute('aria-expanded','false');d.body.classList.remove('menu-open');closing=setTimeout(()=>{navi.hidden=true;},reduced.matches?0:170);}
menu.addEventListener('click',()=>{if(navi.hidden||!navi.classList.contains('open'))openMenu();else closeMenu();});
navi.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
d.addEventListener('keydown',e=>{const open=!navi.hidden&&navi.classList.contains('open');if(e.key==='Escape'&&open){closeMenu();menu.focus();}if(e.key==='Tab'&&open){const items=[menu,...navi.querySelectorAll('a')],first=items[0],last=items[items.length-1];if(e.shiftKey&&d.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&d.activeElement===last){e.preventDefault();first.focus();}}});
// Header turns solid after 40px.
let scheduled=false;
function update(){scheduled=false;nav.classList.toggle('scrolled',scrollY>40);}
addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(update);}},{passive:true});
update();
// Reveal each section once (12px, 420ms, rows 30ms apart). Without JS or with reduced motion everything is simply visible.
if('IntersectionObserver'in window&&!reduced.matches){d.documentElement.classList.add('motion');const io=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('in');io.unobserve(entry.target);}}),{threshold:.12,rootMargin:'0px 0px -8% 0px'});d.querySelectorAll('[data-reveal]').forEach(s=>io.observe(s));}
// Systems: one row open at a time; the old row closes while the new one opens (rule 16).
d.querySelectorAll('.system-list details').forEach(detail=>detail.addEventListener('toggle',()=>{if(detail.open)d.querySelectorAll('.system-list details').forEach(other=>{if(other!==detail)other.open=false;});}));
})();
