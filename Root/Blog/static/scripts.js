function hide_ip() {
    let x = document.getElementById('ip').hidden;
    if (x==false){
        document.getElementById('ip').hidden = true;
        document.getElementById('ip-btn').className = "btn btn-secondary btn-sm m-1";

    }else{
        document.getElementById('ip').hidden = false;
        document.getElementById('ip-btn').className = "btn btn-light btn-sm m-1";
    }
}

function hide_geo() {
    let x = document.getElementById('geo').hidden;
    if (x==false){
        document.getElementById('geo').hidden = true;
        document.getElementById('geo-btn').className = "btn btn-secondary btn-sm m-1";

    }else{
        document.getElementById('geo').hidden = false;
        document.getElementById('geo-btn').className = "btn btn-light btn-sm m-1";

    }
}

function hide_count() {
    let x = document.getElementById('count').hidden;
    if (x==false){
        document.getElementById('count').hidden = true;
        document.getElementById('count-btn').className = "btn btn-secondary btn-sm m-1";

    }else{
        document.getElementById('count').hidden = false;
        document.getElementById('count-btn').className = "btn btn-light btn-sm m-1";

    }
}
function hide_devices() {
    let x = document.getElementById('devices').hidden;
    if (x==false){
        document.getElementById('devices').hidden = true;
        document.getElementById('dev-btn').className = "btn btn-secondary btn-sm m-1";

    }else{
        document.getElementById('devices').hidden = false;
        document.getElementById('dev-btn').className = "btn btn-light btn-sm m-1";

    }
}
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
      x.className += " w3-show";
    } else { 
      x.className = x.className.replace(" w3-show", "");
    }
  }