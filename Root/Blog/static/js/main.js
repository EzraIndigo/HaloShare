// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
      x.className += " w3-show";
    } else { 
      x.className = x.className.replace(" w3-show", "");
    }
  }




function getSetBio() {
  let currentBio = document.getElementById("getBio").dataset.geocode;
  console.log(currentBio)

  let formTextArea = document.getElementById("about");
  formTextArea.value = currentBio;
}


function HandleImgError(source) {
  source.src = "../static/img/placeholder.jpeg";
  source.onerror = "";
  return true;
}


function HandleUploadImgError(source) {
  source.src = "../static/img/upload_placeholder.jpg";
  source.onerror = "";
  return true;
}


function hide_alert() {
  let x = document.getElementById('form_alert').hidden;
  if (x==false){
      document.getElementById('form_alert').hidden = true;
      //document.getElementById('form_alert-btn').className = "btn btn-secondary btn-sm m-1";

  }else{
      document.getElementById('form_alert').hidden = false;
      //document.getElementById('form_alert-btn').className = "btn btn-light btn-sm m-1";

  }
}

function hide_alert_all() {
  let x = document.getElementById('nav_alert').hidden;
  if (x==false){
      document.getElementById('nav_alert').hidden = true;
      //document.getElementById('nav_alert-btn').className = "btn btn-secondary btn-sm m-1";

  }else{
      document.getElementById('nav_alert').hidden = false;
      //document.getElementById('nav_alert-btn').className = "btn btn-light btn-sm m-1";

  }
}
/*
function alert_view(){
  setTimeout(function () {
    document.getElementById('form_alert').remove();
  }, 20000);
}
*/

asd
