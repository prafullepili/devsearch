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

  let tags = document.getElementsByClassName('project-tag');
  for (let i = 0; tags.length > i ; i++){
      tags[i].addEventListener('dblclick',(e)=>{
          let tagId = e.target.dataset.tag;
          let projectId = e.target.dataset.project;
          console.log("CLick")
          fetch('http://127.0.0.1:8000/api/remove-tag/',{
              method:'DELETE',
              headers: {
                  'Content-Type':'application/json'
              },
              body : JSON.stringify({'project':projectId,'tag':tagId})
          })
          .then(response => response.json())
          .then(data => {
              e.target.remove()
          })
      })
  }
