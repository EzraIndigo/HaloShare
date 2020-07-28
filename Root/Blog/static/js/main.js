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


