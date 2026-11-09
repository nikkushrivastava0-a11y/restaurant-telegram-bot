/* Progressive enhancement only. Navigation, enquiries and reveal states
   work with keyboard and reduced-motion settings. */
(function(){
  "use strict";
  document.documentElement.classList.add("js-on");
  var menu=document.querySelector(".menu-toggle");
  var nav=document.getElementById("site-menu");
  function closeMenu(){
    if(!menu||!nav)return;
    menu.setAttribute("aria-expanded","false");
    menu.setAttribute("aria-label","Open menu");
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
  }
  if(menu&&nav){
    menu.addEventListener("click",function(){
      var expanded=menu.getAttribute("aria-expanded")==="true";
      menu.setAttribute("aria-expanded",expanded?"false":"true");
      menu.setAttribute("aria-label",expanded?"Open menu":"Close menu");
      nav.classList.toggle("is-open",!expanded);
      document.body.classList.toggle("nav-open",!expanded);
    });
    nav.querySelectorAll("a").forEach(function(link){link.addEventListener("click",closeMenu);});
    document.addEventListener("keydown",function(event){
      if(event.key==="Escape"&&menu.getAttribute("aria-expanded")==="true"){
        closeMenu();menu.focus();
      }
    });
    window.addEventListener("resize",function(){if(window.innerWidth>800)closeMenu();},{passive:true});
  }

  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals=Array.from(document.querySelectorAll(".reveal"));
  if(reduce||!("IntersectionObserver" in window)){
    reveals.forEach(function(el){el.classList.add("is-inview");});
  } else {
    var observer=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add("is-inview");
          observer.unobserve(entry.target);
        }
      });
    },{threshold:0.1,rootMargin:"0px 0px 45px 0px"});
    reveals.forEach(function(el){observer.observe(el);});
  }

  var form=document.getElementById("luxury-enquiry");
  if(form){
    var feedback=document.getElementById("form-feedback");
    var wanted=new URLSearchParams(window.location.search).get("package");
    if(["Starter","Growth","Premium"].includes(wanted)){
      var matching=form.querySelector('input[name="package"][value="'+wanted+'"]');
      if(matching)matching.checked=true;
    }
    form.addEventListener("submit",function(event){
      event.preventDefault();
      if(!form.reportValidity()){
        feedback.textContent="Please complete the required details before continuing.";
        return;
      }
      var email=(form.getAttribute("data-email")||"").trim();
      if(!email){feedback.textContent="Our enquiry email is unavailable at the moment.";return;}
      var value=function(id){return (form.querySelector("#"+id).value||"").trim();};
      var plan=form.querySelector('input[name="package"]:checked');
      var selected=plan?plan.value:"Starter";
      var subject="Restaurant Website Enquiry — "+value("business");
      var message=[
        "Hello Noida Restaurant Web Studio,",
        "",
        "I would like a written website quote.",
        "",
        "Restaurant: "+value("business"),
        "Contact: "+value("owner"),
        "Phone: "+value("phone"),
        "Area: "+value("area"),
        "Package: "+selected,
        "Notes: "+(value("notes")||"Not specified"),
        "",
        "I am requesting contact about this enquiry.",
        "",
        "Thank you"
      ].join("\n");
      var link="mailto:"+encodeURIComponent(email)+"?subject="+encodeURIComponent(subject)+"&body="+encodeURIComponent(message);
      feedback.textContent="Your email app is opening. Please press Send there to complete your enquiry.";
      window.location.href=link;
    });
  }
})();
