  //GET search form and page links
  let searchForm = document.getElementById("searchForm");
  let pageLinks = document.getElementsByClassName("page-link");

  //ENsure search form exitst 
  if(searchForm){
      for(let i=0; pageLinks.length > i ; i++){
        pageLinks[i].addEventListener('click',function(e){
          e.preventDefault();
          //GET THE DATA ATTRIBUTE
          let page = this.dataset.page;
          
          //ADD HIDDEN search input
          searchForm.innerHTML += `<input value="${page}" name="page" hidden/>`;
          searchForm.submit();
        })
      }
  }
  
  
  document.onkeydown = function(evt){
      evt = evt || window.event;
      if (evt.keyCode == 27){
          backHref = document.getElementById('backButton')
          if(backHref){ 
            alert(`taking back to ${backHref}`);
            window.location = backHref.href;
          }
      }
  }
