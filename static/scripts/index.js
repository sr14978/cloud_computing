"use strict"
window.addEventListener("load", onLoad);

var file_id

function onLoad(e) {
  console.log("load")
  var language = "cpp";
  document.getElementById("fileUpload_form").addEventListener("submit", onSubmitForm);
  document.getElementById("download_button").addEventListener("click", download);
  document.getElementById("standard-c").style.visibility = "hidden";
  document.getElementById("language-c").addEventListener("click", onChangeLanguage("c"));
  document.getElementById("language-cpp").addEventListener("click", onChangeLanguage("cpp"));

  var standards =
  {
    "c" : ["", " -std=c89", " -std=c99", " -std=c11"],
    "cpp" : ["", " -std=c++11", " -std=c++14", " -std=c++17"]
  };

  var opt_lvls = ["", " -O", " -O2", " -O3", " -Ofast"];

  function onSubmitForm(e) {
    console.log("javascript interrupting submit");
    e.preventDefault();

    var file_input = document.getElementById("file_input");
    var linker_flags = document.getElementById("linker_flags").value;
    var standard = standards[language][document.getElementById("standard-" + language).selectedIndex];
    var opt_lvl = opt_lvls[document.getElementById("opt-level").selectedIndex];
    var compiler_flags = document.getElementById("compiler_flags").value + opt_lvl + standard;
    //console.log(compiler_flags);
    //console.log(linker_flags);
    if(file_input.files.length < 1) {
      alert("no file")
      return;
    }

    var file = file_input.files[0]
    var formData = new FormData();
    formData.append('source.zip', file);
    //get the flags
    formData.append('compiler', language == "c" ? "gcc" : "g++");
    formData.append('compiler-flags', compiler_flags);
    formData.append('linker-flags', linker_flags);
    console.log(formData);
    startUploadingAnimation()
    $.ajax({
       url : '/api/v1/submit',
       type : 'PUT',
       data : formData,
       processData: false,
       contentType: false,
       enctype: 'multipart/form-data',
       success : function(data) {
          startCompilingAnimation()
          console.log("id = " + data)
          file_id = data
          setTimeout(checkFinishedCompiling, 500)
       },
       error : function(data) {
          $('#uploading_spinner').hide()
          alert("There was an error in the request");
       }
    });
  }

  // This doesn't quite work :\ oh well, gets the job done! :)
  function onChangeLanguage(to)
  {
    return (e) =>
    {
      console.log("Target language has been changed to " + to + ", updating dropdown menu");
      if (to == "cpp")
      {
        document.getElementById("standard-c").style.visibility = "hidden";
        document.getElementById("standard-cpp").style.visibility = "visible";
      }
      else
      {
        document.getElementById("standard-cpp").style.visibility = "hidden";
        document.getElementById("standard-c").style.visibility = "visible";
      }
      language = to;
    }
  }
}

function download() {
  var a = document.createElement('a');
  a.href = '/api/v1/executable/' + file_id; 
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
}

function checkFinishedCompiling() {
  $.ajax({
       url : '/api/v1/ready/' + file_id,
       type : 'GET',
       success : function(data) {
         if(data == "True") {
           stopCompilingAnimation()
         } else if(data == "False") {
           setTimeout(checkFinishedCompiling, 500)
         } else {
           alert("error")
         }
       },
       error : function(data) {
          alert("some thing has gone wrong")
       }
    });
}

function startUploadingAnimation() {
  $('#uploading_spinner').toggleClass("invisible")
}

function startCompilingAnimation() {
  $('#uploading_spinner').hide()
  $('#waiting_step').slideDown()
}
  
function stopCompilingAnimation() {
  $('#compiling_spinner').hide();
  $(".trigger").toggleClass("drawn");
  $('#download_step').slideDown();
}