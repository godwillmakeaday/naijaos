'use strict';
const form=document.getElementById('inquiry');
form.addEventListener('submit',event=>event.preventDefault());
const fields=[...form.querySelectorAll('input,textarea')];
const status=document.getElementById('status');
document.getElementById('actions').hidden=false;
function syncPrint(){fields.forEach(field=>{let copy=field.nextElementSibling;if(!copy||!copy.classList.contains('print-answer')){copy=document.createElement('div');copy.className='print-answer';field.after(copy);}copy.textContent=field.value||'________________________________________________';});}
form.addEventListener('input',syncPrint);
window.addEventListener('beforeprint',syncPrint);
syncPrint();
document.getElementById('print').addEventListener('click',()=>{syncPrint();window.print();});
document.getElementById('export').addEventListener('click',()=>{
const lines=['THE FOUNDATIONS OF PRACTICE INQUIRY','By Paul A. Magaji | NaijaOS','What must we understand, justify and build for a better practice to become possible?','Better for whom, by what standard, and how would we know?',''];
form.querySelectorAll('fieldset').forEach(group=>{lines.push(group.querySelector('legend').textContent,'');group.querySelectorAll('input,textarea').forEach(field=>{lines.push(form.querySelector('label[for="'+field.id+'"]').textContent,field.value||'[Unanswered]','');});});
const url=URL.createObjectURL(new Blob([lines.join('\n')],{type:'text/plain;charset=utf-8'}));
const link=document.createElement('a');link.href=url;link.download='foundations-of-practice-inquiry.txt';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='Text download requested. Check your browser downloads.';
});