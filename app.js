async function logout(event){event.preventDefault();await fetch("/logout",{method:"POST"});location.href="/login";}
function showRecommendations(box,data){
  box.innerHTML=`<div class="card result"><h2>AI Recommendations</h2><p>${escapeHtml(data.summary||"")}</p>${(data.recommendations||[]).map(r=>`<div class="rec"><h3>${escapeHtml(r.name||"Recommendation")}</h3><p><strong>Platform:</strong> ${escapeHtml(r.platform||"")}</p><p><strong>Estimated price:</strong> ₹${Number(r.estimated_price||0).toLocaleString("en-IN")}</p><p>${escapeHtml(r.reason||"")}</p></div>`).join("")}<p><small>Source: ${escapeHtml(data.source||"AI")}. Prices are estimates and should be verified before purchase.</small></p></div>`;
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));}
async function submitPlanner(form, url, isFormData=false){
  const box=document.getElementById("result"); box.innerHTML="<p>Generating recommendations...</p>";
  try{
    const options={method:"POST",body:isFormData?new FormData(form):JSON.stringify(Object.fromEntries(new FormData(form)))};
    if(!isFormData) options.headers={"Content-Type":"application/json"};
    const r=await fetch(url,options); const data=await r.json();
    if(!r.ok) throw new Error(data.detail||"Request failed");
    showRecommendations(box,data);
  }catch(e){box.innerHTML=`<div class="card message">${escapeHtml(e.message)}</div>`;}
}
document.addEventListener("DOMContentLoaded",()=>{
 const home=document.getElementById("homeForm"); if(home) home.addEventListener("submit",e=>{e.preventDefault();submitPlanner(home,"/generate-home");});
 const party=document.getElementById("partyForm"); if(party) party.addEventListener("submit",e=>{e.preventDefault();submitPlanner(party,"/generate-party");});
 const jewelry=document.getElementById("jewelryForm"); if(jewelry) jewelry.addEventListener("submit",e=>{e.preventDefault();submitPlanner(jewelry,"/generate-jewelry",true);});
});
