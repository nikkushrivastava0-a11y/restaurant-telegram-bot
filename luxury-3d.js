/* One honest interactive 3D sculpture per page.
   Uses Three.js as an optional enhancement; HTML/CSS fallback stays visible
   if WebGL or the module CDN is unavailable. No analytics or data collection. */
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js";

const prefersLess = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const mobile = window.matchMedia("(max-width: 680px)").matches;
const palette = {
  studio: {base:0xceb185,bright:0xf4deae,dark:0x6e624e},
  modern: {base:0xc89165,bright:0xf5ddac,dark:0x744333},
  bold: {base:0xe8a646,bright:0xf9db84,dark:0x8e3025},
  minimal: {base:0xd2d2c5,bright:0xf9f2de,dark:0x758877}
};

function finish(color, roughness=0.27, metalness=0.68) {
  return new THREE.MeshPhysicalMaterial({
    color, metalness, roughness, clearcoat:0.42,
    clearcoatRoughness:0.17, side:THREE.DoubleSide
  });
}
function ceramic(color, roughness=0.36) {
  return new THREE.MeshPhysicalMaterial({color,metalness:0.1,roughness,clearcoat:0.28,side:THREE.DoubleSide});
}
function add(group,geometry,material,pos,rot,scale){
  const obj=new THREE.Mesh(geometry,material);
  if(pos)obj.position.set(pos[0],pos[1],pos[2]);
  if(rot)obj.rotation.set(rot[0],rot[1],rot[2]);
  if(scale)obj.scale.set(scale[0],scale[1],scale[2]);
  group.add(obj);
  return obj;
}
function ring(group,radius,tube,color,pos,rot){
  return add(group,new THREE.TorusGeometry(radius,tube,24,124),finish(color,.21,.8),pos,rot);
}
function sphere(group,radius,material,pos,scale){
  return add(group,new THREE.SphereGeometry(radius,40,24),material,pos,null,scale);
}

function studioSculpture(root,colors){
  const g=new THREE.Group();root.add(g);
  g.rotation.set(0.23,-0.28,0.12);
  // Balanced bronze orbital sculpture, not a random dashboard orb.
  ring(g,2.28,.108,colors.base,[0,0,0],[0.84,0.09,-0.24]);
  ring(g,1.72,.13,colors.bright,[0.13,0.02,0],[1.58,0.51,0.48]);
  ring(g,2.04,.095,colors.dark,[-0.06,0,0],[-0.53,0.58,0.4]);
  add(g,new THREE.TorusKnotGeometry(1.16,.27,210,22,2,3),finish(colors.base,.18,.82),[0.05,0.02,0.2],[0.21,0.25,0.33]);
  sphere(g,.73,finish(colors.bright,.15,.71),[.08,0,.16]);
  sphere(g,.14,finish(colors.bright,.13,.76),[-2.3,-1.2,.4]);
  sphere(g,.1,finish(colors.bright,.13,.76),[1.84,1.76,-.28]);
  return g;
}
function modernSculpture(root,colors){
  const g=new THREE.Group();root.add(g);
  g.rotation.set(0.18,-0.43,0.1);
  const clay=ceramic(0xd5a06b,.39),warm=ceramic(0xe9c59b,.34),sage=finish(0x586b4d,.41,.12);
  const profile=[
    [0,0],[.6,.03],[1.3,.05],[1.64,.11],[1.83,.28],
    [1.92,.5],[2.04,.72],[2.0,.79],[1.88,.76],[1.73,.54],
    [1.41,.34],[.75,.27],[0,.24]
  ].map(p=>new THREE.Vector2(p[0],p[1]));
  const bowl=add(g,new THREE.LatheGeometry(profile,100),clay,[0,-.62,0],[.04,0,.12]);
  ring(g,1.94,.07,0xe9bb85,[0,.16,0],[Math.PI/2,0,0]);
  // Floating abstract spices and garnishes are deliberately illustrative,
  // never photographs or claims of actual menu items.
  sphere(g,.33,warm,[-.56,.38,.38],[1.25,.42,.81]);
  sphere(g,.37,ceramic(0x9a4c28,.53),[.34,.29,.16],[1.1,.33,1.28]);
  sphere(g,.31,ceramic(0xa57640,.52),[-.05,.52,-.49],[1.0,.5,1.2]);
  for(let i=0;i<6;i++){
    const a=i*2.4;
    sphere(g,.27,sage,[Math.sin(a)*.7,.54+(i%3)*.08,Math.cos(a)*.65],[.38,.15,1.5]).rotation.y=a;
  }
  ring(g,2.43,.022,colors.bright,[0,-.35,.0],[.2,.2,-.2]);
  return g;
}
function boldSculpture(root,colors){
  const g=new THREE.Group();root.add(g);
  g.rotation.set(0.2,-.39,-.05);
  const bun=ceramic(0xe9aa54,.36),patty=ceramic(0x503121,.8),
    cheese=ceramic(0xf9ce61,.54),green=ceramic(0x698348,.78);
  // A stylized exploded burger: real 3D primitives, not a flat fake mockup.
  sphere(g,1.55,bun,[0,1.05,0],[1.25,.47,1.12]);
  add(g,new THREE.CylinderGeometry(1.72,1.65,.22,68),bun,[0,-1.27,0]);
  add(g,new THREE.CylinderGeometry(1.68,1.7,.39,68),patty,[0,-.78,0]);
  add(g,new THREE.CylinderGeometry(1.7,1.7,.11,68),cheese,[0,-.38,0]);
  add(g,new THREE.TorusGeometry(1.56,.16,22,128),green,[0,-.06,0],[Math.PI/2,.2,0]);
  sphere(g,1.48,ceramic(0xc83e2e,.48),[0,.23,0],[1.06,.12,.96]);
  for(let i=0;i<13;i++){
    const t=i*2.399963;
    sphere(g,.075,ceramic(0xf7edca,.55),[Math.cos(t)*.9,1.62+Math.sin(t*.7)*.08,Math.sin(t)*.75],[.7,.5,1.45]);
  }
  ring(g,2.48,.035,colors.bright,[0,0,0],[.23,.8,.63]);
  ring(g,2.68,.025,0xffdf8b,[0,0,0],[1.24,.2,-.45]);
  return g;
}
function minimalSculpture(root,colors){
  const g=new THREE.Group();root.add(g);
  g.rotation.set(.22,-.33,.08);
  const bowlMat=ceramic(0xeee6d1,.23),shade=ceramic(0xb2b9a5,.3);
  const profile=[
    [0,-1.15],[.49,-1.15],[.65,-.91],[.72,-.57],[.84,-.24],
    [1.19,.13],[1.44,.42],[1.42,.52],[1.29,.52],[1.08,.34],
    [.70,.08],[.4,-.06],[0,-.06]
  ].map(p=>new THREE.Vector2(p[0],p[1]));
  add(g,new THREE.LatheGeometry(profile,110),bowlMat,[0,-.17,0]);
  ring(g,1.49,.044,0xe1d6b5,[0,.36,0],[Math.PI/2,0,0]);
  add(g,new THREE.CylinderGeometry(.18,.23,2.26,36),shade,[0,1.5,0],[.08,0,.02]);
  for(let i=0;i<5;i++){
    const a=i*2.399963;
    const leaf=sphere(g,.65,ceramic(0x788d76,.59),[
      Math.sin(a)*.55,1.16+(i%3)*.41,Math.cos(a)*.56],[.31,.72,.18]);
    leaf.rotation.set(Math.sin(a)*.5,0,-Math.cos(a)*.65);
  }
  ring(g,2.39,.035,colors.bright,[0,-.22,0],[.27,.45,.16]);
  return g;
}

function mount(canvas) {
  const name=canvas.dataset.scene;
  const colors=palette[name];
  if(!colors)return;
  const parent=canvas.parentElement;
  let renderer;
  try{
    renderer=new THREE.WebGLRenderer({
      canvas,alpha:true,antialias:!mobile,powerPreference:"low-power"
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,mobile?1.3:1.55));
  }catch(error){
    console.warn("WebGL unavailable; leaving crafted CSS sculpture visible.");
    return;
  }
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure=1.25;
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(mobile?41:35,1,.1,80);
  camera.position.set(0,.35,mobile?9.2:8.6);
  scene.add(new THREE.AmbientLight(0xffffff,1.55));
  const key=new THREE.DirectionalLight(0xfff0d1,4.1);
  key.position.set(4,7,6);scene.add(key);
  const fill=new THREE.PointLight(0xf0c58e,54,16,1.55);
  fill.position.set(-5,-1,4);scene.add(fill);
  const rim=new THREE.PointLight(0xd6e9d9,38,20,1.5);
  rim.position.set(3,-5,-2);scene.add(rim);
  const root=new THREE.Group();scene.add(root);
  const builders={studio:studioSculpture,modern:modernSculpture,bold:boldSculpture,minimal:minimalSculpture};
  const sculpture=builders[name](root,colors);
  function resize(){
    const bounds=parent.getBoundingClientRect();
    const width=Math.max(260,bounds.width),height=Math.max(260,bounds.height);
    renderer.setSize(width,height,false);
    camera.aspect=width/height;
    camera.position.z=(width<500?9.45:8.65);
    camera.updateProjectionMatrix();
    if(prefersLess)renderer.render(scene,camera);
  }
  resize();
  if("ResizeObserver" in window){
    const ro=new ResizeObserver(resize);ro.observe(parent);
  }else window.addEventListener("resize",resize,{passive:true});
  let targetX=0,targetY=0,curX=0,curY=0,onscreen=true,frame=0;
  parent.addEventListener("pointermove",function(e){
    if(prefersLess||e.pointerType==="touch")return;
    const b=parent.getBoundingClientRect();
    targetX=((e.clientX-b.left)/b.width-.5)*.27;
    targetY=((e.clientY-b.top)/b.height-.5)*.20;
  },{passive:true});
  parent.addEventListener("pointerleave",function(){targetX=0;targetY=0;},{passive:true});
  if("IntersectionObserver" in window){
    const visible=new IntersectionObserver(function(entries){
      onscreen=entries[0].isIntersecting;
      if(onscreen&&!prefersLess&&frame===0)frame=requestAnimationFrame(tick);
    },{threshold:0.01});
    visible.observe(parent);
  }
  let then=0;
  function tick(ts){
    frame=0;
    if(document.hidden||!onscreen)return;
    const dt=Math.min(0.055,(ts-then)/1000||0.016);then=ts;
    curX+=(targetX-curX)*Math.min(1,dt*1.8);
    curY+=(targetY-curY)*Math.min(1,dt*1.8);
    sculpture.rotation.y+=dt*.095;
    root.rotation.y=curX;
    root.rotation.x=curY;
    root.position.y=Math.sin(ts*.00045)*.075;
    renderer.render(scene,camera);
    frame=requestAnimationFrame(tick);
  }
  canvas.addEventListener("webglcontextlost",function(e){
    e.preventDefault();
    parent.classList.remove("is-ready");
    if(frame)cancelAnimationFrame(frame);
    frame=0;
  });
  renderer.render(scene,camera);
  parent.classList.add("is-ready");
  if(!prefersLess)frame=requestAnimationFrame(tick);
  document.addEventListener("visibilitychange",function(){
    if(!document.hidden&&frame===0&&!prefersLess&&onscreen)frame=requestAnimationFrame(tick);
  });
}
document.querySelectorAll("canvas[data-scene]").forEach(mount);
