/* Spring Real Estate — lichte i18n laag (NL / EN / ES)
   Elementen met data-i18n="key" krijgen vertaalde tekst.
   NL is de basistaal (in de HTML geschreven); EN/ES uit de woordenlijst.
   Placeholders via data-i18n-ph. */
window.SPRING_I18N = {
  en: {
    "nav.diensten":"Services","nav.listings":"Listings","nav.about":"About","nav.agents":"Agents",
    "nav.resources":"Resources","nav.vacatures":"Careers","nav.contact":"Contact","cta.aanbod":"View listings",
    "nav.aanbod":"Listings","nav.koop":"For Sale","nav.koop.d":"Office and commercial space for sale",
    "nav.huur":"To Let","nav.huur.d":"Office and commercial space to let",
    "nav.cases":"Cases","nav.cases.d":"Results for our clients",
    "nav.transacties":"Transactions","nav.transacties.d":"Real estate deals and market data",
    "nav.algemeen":"General","nav.algemeen.d":"Analyses, trends and insights",
    "nav.team":"Team","nav.huidig.team":"Our team","nav.huidig.team.d":"100+ real estate specialists",
    "nav.join":"Join our team?","nav.join.d":"View vacancies",
    "nav.over.spring":"About Spring","nav.over.spring.d":"Who we are and what we do",
    "nav.locaties":"Our locations","nav.locaties.d":"Amsterdam, Utrecht &amp; Spain",
    "dd.gebruiker":"User","dd.gebruiker.d":"I'm looking for office space","dd.eigenaar":"Owner",
    "dd.eigenaar.d":"I want to sell or lease","dd.investeerder":"Investor","dd.investeerder.d":"I want to invest in real estate",
    "dd.ontwikkelaar":"Developer","dd.ontwikkelaar.d":"I want to develop or optimise",
    "search.lblloc":"Location or keyword","search.phloc":"E.g. Amsterdam Zuidas, office…",
    "search.lbltype":"Type","search.lblarea":"Floor area","search.btn":"Search",
    "search.t.huur":"Rent","search.t.koop":"Buy","search.t.invest":"Invest",
    "search.people":"Search a colleague by name or role…","search.articles":"Search articles…",
    "more.info":"More info","cta.contact":"Get in touch","search.term":"Search a term…",
    "form.firstname":"First name *","form.lastname":"Last name *","form.email":"Email address *","form.phone":"Phone number","form.company":"Company name","form.message":"Your message",
    "foot.doelgroepen":"Audiences","foot.navigatie":"Navigation","foot.locaties":"Locations",
    "foot.nieuwsbrief":"Newsletter","foot.nieuwsbrief.p":"Market insights & new listings in your inbox.",
    "foot.inschrijven":"Subscribe","foot.email":"Your email address","foot.tagline":"Powered by People. Backed by Tech. Your partner in commercial real estate in the Netherlands & Spain.",
    "foot.rights":"© 2026 Spring Real Estate. All rights reserved.",
    "talk.eyebrow":"Personal contact","talk.p":"Prefer to talk directly? Our specialists are happy to help — no obligation, in your language.","talk.plan":"Book a consultation"
  },
  es: {
    "nav.diensten":"Servicios","nav.listings":"Inmuebles","nav.about":"About","nav.agents":"Equipo",
    "nav.resources":"Recursos","nav.vacatures":"Empleo","nav.contact":"Contacto","cta.aanbod":"Ver inmuebles",
    "nav.aanbod":"Inmuebles","nav.koop":"En venta","nav.koop.d":"Oficina y local comercial en venta",
    "nav.huur":"En alquiler","nav.huur.d":"Oficina y local comercial en alquiler",
    "nav.cases":"Casos","nav.cases.d":"Resultados para nuestros clientes",
    "nav.transacties":"Transacciones","nav.transacties.d":"Operaciones inmobiliarias y datos de mercado",
    "nav.algemeen":"General","nav.algemeen.d":"Análisis, tendencias e insights",
    "nav.team":"Equipo","nav.huidig.team":"Nuestro equipo","nav.huidig.team.d":"100+ especialistas en inmuebles",
    "nav.join":"¿Te unes a nosotros?","nav.join.d":"Ver vacantes",
    "nav.over.spring":"Sobre Spring","nav.over.spring.d":"Quiénes somos y qué hacemos",
    "nav.locaties":"Nuestras ubicaciones","nav.locaties.d":"Ámsterdam, Utrecht y España",
    "dd.gebruiker":"Usuario","dd.gebruiker.d":"Busco espacio de oficina","dd.eigenaar":"Propietario",
    "dd.eigenaar.d":"Quiero vender o alquilar","dd.investeerder":"Inversor","dd.investeerder.d":"Quiero invertir en inmuebles",
    "dd.ontwikkelaar":"Promotor","dd.ontwikkelaar.d":"Quiero desarrollar u optimizar",
    "search.lblloc":"Ubicación o palabra clave","search.phloc":"Ej. Ámsterdam Zuidas, oficina…",
    "search.lbltype":"Tipo","search.lblarea":"Superficie","search.btn":"Buscar",
    "search.t.huur":"Alquilar","search.t.koop":"Comprar","search.t.invest":"Invertir",
    "search.people":"Busca un compañero por nombre o función…","search.articles":"Buscar artículos…",
    "more.info":"Más información","cta.contact":"Contáctanos","search.term":"Buscar un término…",
    "form.firstname":"Nombre *","form.lastname":"Apellidos *","form.email":"Correo electrónico *","form.phone":"Teléfono","form.company":"Empresa","form.message":"Tu mensaje",
    "foot.doelgroepen":"Públicos","foot.navigatie":"Navegación","foot.locaties":"Ubicaciones",
    "foot.nieuwsbrief":"Boletín","foot.nieuwsbrief.p":"Análisis de mercado y nuevos inmuebles en tu correo.",
    "foot.inschrijven":"Suscribirse","foot.email":"Tu correo electrónico","foot.tagline":"Powered by People. Backed by Tech. Tu socio en inmuebles comerciales en los Países Bajos y España.",
    "foot.rights":"© 2026 Spring Real Estate. Todos los derechos reservados.",
    "talk.eyebrow":"Contacto personal","talk.p":"¿Prefieres hablar directamente? Nuestros especialistas te ayudan con gusto, sin compromiso y en tu idioma.","talk.plan":"Reserva una consulta"
  }
};

(function(){
  const dict = window.SPRING_I18N;
  function apply(lang){
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el=>{
      if(el.dataset.nl === undefined) el.dataset.nl = el.textContent;
      el.textContent = (lang!=='nl' && dict[lang] && dict[lang][el.dataset.i18n]) || el.dataset.nl;
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(el=>{
      if(el.dataset.nlPh === undefined) el.dataset.nlPh = el.getAttribute('placeholder')||'';
      el.setAttribute('placeholder',(lang!=='nl' && dict[lang] && dict[lang][el.dataset.i18nPh]) || el.dataset.nlPh);
    });
    // element-level body translations (data-tr + data-en / data-es, innerHTML)
    document.querySelectorAll('[data-tr]').forEach(el=>{
      if(el.dataset.nlHtml === undefined) el.dataset.nlHtml = el.innerHTML;
      el.innerHTML = (lang==='en' && el.dataset.en) ? el.dataset.en
                   : (lang==='es' && el.dataset.es) ? el.dataset.es
                   : el.dataset.nlHtml;
    });
    document.querySelectorAll('.lang button, .mm-lang button, .h-lang button').forEach(b=>{
      b.classList.toggle('active', b.dataset.lang===lang);
    });
    try{ localStorage.setItem('spring-lang', lang); }catch(_){}
  }
  window.SPRING_setLang = apply;
  document.addEventListener('click', e=>{
    const b = e.target.closest('.lang button, .mm-lang button, .h-lang button');
    if(b && b.dataset.lang) apply(b.dataset.lang);
  });
  let saved='nl';
  try{ saved = localStorage.getItem('spring-lang') || 'nl'; }catch(_){}
  document.addEventListener('DOMContentLoaded', ()=>apply(saved));
})();
