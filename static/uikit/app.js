// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


let alertWrapper = document.getElementsByClassName('alert');
let alertClose = document.getElementsByClassName('alert__close');

if (alertWrapper){
  for(let i=0; i < alertClose.length; i++ ){
    alertClose[i].addEventListener('click',(e)=>{
      // alertWrapper.style.display='none'
      alertWrapper[i].remove();
    })
  }
}