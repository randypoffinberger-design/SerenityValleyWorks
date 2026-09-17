document.getElementById('year').textContent=new Date().getFullYear();
const menu=document.querySelector('.menu'),nav=document.querySelector('#nav');
menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false');}));
if(location.pathname.includes('/morethanmeasured/')){const l=document.createElement('link');l.rel='stylesheet';l.href=location.pathname.includes('/morethanmeasured/articles/')?'../mtm.css':'mtm.css';document.head.appendChild(l);}
