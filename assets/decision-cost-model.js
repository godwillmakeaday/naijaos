/* NaijaOS Decision Lab: no network requests, storage or tracking */
(function(root){"use strict";
function estimateCosts(input,months=24,contingency=10){
 if(!Number.isInteger(months)||months<1||months>120)throw Error("Months must be 1–120.");
 if(!Number.isFinite(contingency)||contingency<0||contingency>50)throw Error("Contingency must be 0–50%.");
 const v={};
 for(const key of ["setup","migration","hosting","tools","supportHours","supportRate"]){
  if(typeof input[key]!=="number"||!Number.isFinite(input[key])||input[key]<0)throw Error("Enter a non-negative figure for "+key+".");
  v[key]=input[key];
 }
 const monthly=v.hosting+v.tools+v.supportHours*v.supportRate;
 const oneTime=v.setup+v.migration;
 const recurring=monthly*months;
 const subtotal=oneTime+recurring;
 const reserve=subtotal*contingency/100;
 return {oneTime,monthly,recurring,subtotal,reserve,total:subtotal+reserve};
}
const api={estimateCosts};if(typeof module==="object"&&module.exports)module.exports=api;root.NaijaOSCostModel=api;
})(typeof globalThis!=="undefined"?globalThis:this);
