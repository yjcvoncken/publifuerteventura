const menu=document.querySelector('.menu');
const navigation=document.querySelector('#main-navigation');
if(menu&&navigation){menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')==='true';menu.setAttribute('aria-expanded',String(!open));menu.setAttribute('aria-label',open?'Open menu':'Close menu');menu.textContent=open?'☰':'×';navigation.classList.toggle('open',!open)})}

const cookieBanner=document.querySelector('[data-cookie-banner]');
const analyticsConsent=document.querySelector('[data-analytics-consent]');
const cookieKey='publifuerte_cookie_choice';

function cookieChoice(){try{return localStorage.getItem(cookieKey)}catch(e){return null}}
function setConsentCookie(value){const secure=location.protocol==='https:'?'; Secure':'';document.cookie=`${cookieKey}=${value}; Path=/; Max-Age=31536000; SameSite=Lax${secure}`}
function analyticsSession(){try{let id=sessionStorage.getItem('publifuerte_analytics_session');if(!id){id=crypto.randomUUID?crypto.randomUUID():`${Date.now()}-${Math.random()}`;sessionStorage.setItem('publifuerte_analytics_session',id)}return id}catch(e){return''}}
function recordPageView(){const endpoint=document.body.dataset.analyticsUrl;if(!endpoint||cookieChoice()!=='accepted')return;fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:location.pathname,language:document.documentElement.lang,session:analyticsSession()}),keepalive:true}).catch(()=>{})}
function saveCookieChoice(value){try{localStorage.setItem(cookieKey,value)}catch(e){}setConsentCookie(value);if(cookieBanner)cookieBanner.hidden=true;if(value==='accepted')recordPageView()}
function openCookieSettings(){if(!cookieBanner)return;analyticsConsent.checked=cookieChoice()==='accepted';cookieBanner.hidden=false}

const existingChoice=cookieChoice();
if(existingChoice){setConsentCookie(existingChoice);if(existingChoice==='accepted')recordPageView()}else if(cookieBanner){cookieBanner.hidden=false}
document.querySelector('[data-cookie-save]')?.addEventListener('click',()=>saveCookieChoice(analyticsConsent?.checked?'accepted':'essential'));
document.querySelector('[data-cookie-reject]')?.addEventListener('click',()=>saveCookieChoice('essential'));
document.querySelector('[data-cookie-settings]')?.addEventListener('click',openCookieSettings);
