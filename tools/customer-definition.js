(function(root){
'use strict';
const fields=[
['audience','Who are you serving?','Describe people in a recognisable situation. Include age or location only when it changes the need.','Women over 60 who feel uncomfortable in conventional gyms'],
['outcome','What do they want to accomplish?','Use their language. Describe a result, without promising an outcome you cannot establish.','Find approachable support for managing their weight'],
['trigger','Why does this matter now?','What event or change brings the need into focus?','They are reconsidering their daily routines after retirement'],
['barriers','What makes progress difficult?','Think about time, access, confidence, responsibilities and resources.','Unfamiliar gym environments and routines that feel difficult to maintain'],
['alternatives','What do they already do?','Include doing nothing, asking friends and free resources.','Watch general fitness videos and ask friends for suggestions'],
['gap','What remains unsatisfactory?','What do existing options fail to address?','They struggle to judge which information suits their circumstances'],
['roles','Who uses, chooses and pays?','Separate these roles. Do not assume interest means willingness to pay.','The woman uses and chooses; who pays still needs investigation'],
['reach','Where can you learn from them?','Name a specific setting or channel you can actually access.','Ask a local community group whether members want to discuss their experiences'],
['offer','What is the smallest useful response?','Start with a resource or service you can test before creating a brand.','A short guide to questions to ask a suitably qualified professional'],
['test','How will you test this understanding?','State who you will speak with, what behaviour you will examine and when.','Speak with five willing participants this month about their most recent attempt and existing spending'],
['decision','What would make you continue, change or stop?','Choose observable evidence in advance. A small test gives direction, not proof.','Continue if repeated unmet needs emerge and people choose to try the resource; revise if their priorities differ']
];
function derive(values){const get=k=>(values[k]?.answer||'').trim();const filled=fields.filter(([k])=>get(k)).length;const evidenced=fields.filter(([k])=>get(k)&&values[k]?.status==='evidence'&&(values[k]?.note||'').trim()).length;return {filled,evidenced,statement:`We serve ${get('audience')||'[people]'} who, when ${get('trigger')||'[circumstance]'}, want to ${get('outcome')||'[outcome]'}, but face ${get('barriers')||'[barriers]'}. They currently use ${get('alternatives')||'[alternatives]'}, which leave this gap: ${get('gap')||'[gap]'}. We will test ${get('offer')||'[response]'} through ${get('test')||'[experiment]'}.`,warnings:fields.filter(([k])=>get(k)&&values[k]?.status==='evidence'&&!(values[k]?.note||'').trim()).map(([,label])=>label+' needs an evidence note.')}};
function brief(v){const d=derive(v);return '# Customer Definition Brief\n\nWorking hypothesis — not a validated customer profile.\n\n'+d.statement+'\n\n'+fields.map(([k,label])=>'## '+label+'\n'+(v[k]?.answer||'[Unanswered]')+'\nBasis: '+(v[k]?.status||'assumption')+'\nEvidence / uncertainty: '+(v[k]?.note||'[Not recorded]')).join('\n\n')+'\n\n'+d.evidenced+' of '+fields.length+' answers marked as evidence with notes. Evidence quality has not been independently verified.\n';}
root.CustomerCanvas={fields,derive,brief};if(typeof module!=='undefined')module.exports=root.CustomerCanvas;
})(typeof window!=='undefined'?window:globalThis);
