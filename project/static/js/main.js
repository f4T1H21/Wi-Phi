/*
ﺏ
Copyright [2022] Şefik Efe Altınoluk

This file is a part of project Wi-Phi©
For more details, see https://github.com/f4T1H21/Wi-Phi

Licensed under the GNU GENERAL PUBLIC LICENSE Version 3.0 (the "License")
You may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.gnu.org/licenses/gpl-3.0.html
*/

function validate() {
    var email = document.getElementById("e");
    var emailval = email.value;
    var emailre = /^[ ]*[a-zA-Z0-9](\.?[a-zA-Z0-9]){5,}@gmail\.com[ ]*$/;

    if (emailre.test(emailval)) {

        var passwd = document.getElementById("p");
        var passwdval = passwd.value;
        var passwdre = /.{8}.*/;

        if (passwdre.test(passwdval)) {
            return true;
        }

        else {
            passwd.style.border = "solid 3px #d31f1f";
            alert("Şifre hatalı!");
            setTimeout(function() {passwd.style.border = "solid 1px #c2c4c6"}, 2000);
            event.preventDefault();
            returnToPreviousPage();
            return false;
        }
    }

    else {
        email.style.border = "solid 3px #d31f1f";
        alert("E-posta adresi hatalı!");
        setTimeout(function() {email.style.border = "solid 1px #c2c4c6"}, 2000);
        event.preventDefault();
        returnToPreviousPage();
        return false;
    }
}

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

function toggle() {
    var x = document.getElementById("p");
    if (x.type === "password") {
        x.type = "text";
    } 
    else {
        x.type = "password";
    }
}