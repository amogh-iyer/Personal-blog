console.log('Carmine is cool!');

function loadDoc(url, func) {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status != 200) {
            console.log("Error");
        } else {
            func(xhttp.response);
        }
    }
    xhttp.open("GET", url);
    xhttp.send();
}

function login() {
    let txtEmail = document.getElementById("txtEmail");
    let txtPassword = document.getElementById("txtPassword");

    if (txtEmail.value == '' || txtPassword.value == '') {
        alert("Email and password can not be blank.");
        return;
    }

    let URL = "/login?email=" + txtEmail.value + "&password=" + txtPassword.value;


    let chkRemember = document.getElementById("chkRemember");
    if(chkRemember.checked){
        URL +="&remember=yes";
    } else {
        URL += "&remember=no";
    }

      loadDoc(URL, login_response);
}


// function login_response(response) {
//     let data = JSON.parse(response);
//     let result = data["result"];
//     if (result != "OK") {
//         alert(result);
//     }
//     else {
//         window.location.replace("/account.html");
//     }

// }



function list_blog() {
    loadDoc('/list_blog', list_blog_response);
}

function list_blog_response(response) {
    let data = JSON.parse(response)
    let items = data["results"]

    let divResults = document.getElementById("divResults");

    let temp = "";
    for (let i = 0; i < items.length; i++) {

        temp +=  items[i]["title"] + '<br>' + items[i]["text"]  + "<br>" + items[i]["date"] + "<br>" + "<br>";
    }
    divResults.innerHTML = temp;
}

function list_blog_editor() {
    loadDoc('/list_blog', list_blog_editor_response);
}

function list_blog_editor_response(response) {
    let data = JSON.parse(response)
    let items = data["results"]

    let divResults = document.getElementById("divResults");

    let temp = "";
    for (let i = 0; i < items.length; i++) {

       temp += "<a href=\"/delete?id=" +  items[i]["uniqueID"] + "\">remove</a>"  + items[i]["date"]  + '<br>' + items[i]["title"] + "<br>" +  items[i]["text"]  + "<br><br>";

    }
    divResults.innerHTML = temp;
}


function add_blog(){
    let title = document.getElementById("title");
    let text = document.getElementById("text");


    if (text == '' || title == '') {
        alert("text and title can not be blank.");
        return;
    }

    let URL = "/add_blog?title=" + title.value + "&text=" + text.value;

    loadDoc(URL, add_blog_response);



}

function add_blog_response(response) {

        window.location.replace("/editor.html");


}



function login_response(response) {
    let data = JSON.parse(response);
    let result = data["result"];
    if (result != "OK") {
        alert(result);
    }
    else {
        window.location.replace("/editor.html");
    }

}


function course_search() {
    let txtSearch = document.getElementById("txtSearch");
    let url = "/catalog/" + txtSearch.value;
    loadDoc(url, course_search_results);
}

function course_search_results(response) {
    let data = JSON.parse(response);
    let result = data["result"];

    let temp = "";

    for (let i = 0; i < result.length; i++) {
        let course = result[i];

        temp += "<div class=\"course_container\">";
        temp += "<a href=\"/course/" + course["number"] + "\">" + course["number"] + "</a> :" + course["name"];
        temp += "</div>";
    }

    let divResults = document.getElementById("divResults");
    divResults.innerHTML = temp;
}


function list_files() {
    loadDoc('/listfiles', list_files_response);
}

function list_files_response(response) {
    let data = JSON.parse(response);
    let items = data["items"];
    let url = data["url"];
    let divResults = document.getElementById("divResults");

    let temp = "";
    for (let i = 0; i < items.length; i++) {
        temp += "<a href=\"" + url + "/" + items[i] + "\">" + items[i] + "</a><br>";
    }
    divResults.innerHTML = temp;
}

function list_images() {
    loadDoc('/listimages', list_images_response);
}

function list_images_response(response) {
    let data = JSON.parse(response)
    let items = data["results"]

    let divResults = document.getElementById("divResults");

    let temp = "";
    for (let i = 0; i < items.length; i++) {
        temp += '<img style="width:220px" src="https://ai55853n-web-public.s3.us-east-2.amazonaws.com/'+ items[i]["filename"] + '"><br>' + items[i]["caption"]  + "<br>";
    }
    divResults.innerHTML = temp;
}


function upload_file() {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status != 200) {
            console.log("Error");
        } else {
            upload_file_response(xhttp.response);
        }
    }

    xhttp.open('POST','/uploadfile',true);
    var formData = new FormData();
    formData.append("file", document.getElementById('file').files[0]);

// You can add other form elements here!
    let s = document.getElementById("caption");
    console.log(s.value);
    formData.append("caption", s.value);


    xhttp.send(formData);


}

function upload_file_response(response) {
    location.reload();
}





