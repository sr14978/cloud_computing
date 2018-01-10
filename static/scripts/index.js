"use strict"
window.addEventListener("load", onLoad);

var file_id

function onLoad(e) {
  console.log("load")
  var language = "cpp";
  document.getElementById("fileUpload_form").addEventListener("submit", upload);
  document.getElementById("download_button").addEventListener("click", download);
  document.getElementById("language-c").addEventListener("click", onChangeLanguage("c"));
  document.getElementById("language-cpp").addEventListener("click", onChangeLanguage("cpp"));

  var standards =
  {
    "c" : [
      {
        'display':'No Standard',
        'val':''
      },
      {
        'display':'C89',
        'val':' -std=c89'
      },
      {
        'display':'GNU C89',
        'val':' -std=gnu90'
      },
      {
        'display':'C99',
        'val':' -std=c99'
      },
      {
        'display':'GNU C99',
        'val':' -std=gnu99'
      },
      {
        'display':'C11',
        'val':' -std=c11'
      },
      {
        'display':'GNU C11',
        'val':' -std=gnu11'
      }
    ],
    "cpp" : [
      {
        'display':'No Standard',
        'val':''
      },
      {
        'display':'C++ 98',
        'val':' -std=c++98'
      },
      {
        'display':'GNU C++ 98',
        'val':' -std=gnu++98'
      },
      {
        'display':'C++ 11',
        'val':' -std=c++11'
      },
      {
        'display':'GNU C++ 11',
        'val':' -std=gnu++11'
      },
      {
        'display':'C++ 14',
        'val':' -std=c++14'
      }
    ]
  };
  onChangeLanguage("cpp")();
  var opt_lvls = ["", " -O", " -O2", " -O3", " -Ofast"];

  function upload(e) {
    
    
    
    document.getElementById("submit_button").disabled = true;
    console.log("javascript interrupting submit");
    e.preventDefault();

    var file_input = document.getElementById("file_input");
    var linker_flags = document.getElementById("linker_flags").value;
    var standard = standards[language][document.getElementById("standard").selectedIndex]['val'];
    var opt_lvl = opt_lvls[document.getElementById("opt-level").selectedIndex];
    var compiler_flags = document.getElementById("compiler_flags").value + opt_lvl + standard;
    //console.log(compiler_flags);
    //console.log(linker_flags);
    if(file_input.files.length < 1) {
      alert("no file")
      document.getElementById("submit_button").disabled = false;
      return;
    }

    var file = file_input.files[0]
    console.log(file);
    if( ! (file.type == "application/x-zip-compressed" ||  file.type == "application/zip"
          || (file.type == "" && file.name.substring(file.name.lastIndexOf('.')) == "zip")) ) {
      alert("please upload zip file")
      document.getElementById("submit_button").disabled = false;
      return;
    }  
    var formData = new FormData();
    formData.append('source.zip', file);
    //get the flags
    formData.append('compiler', language == "c" ? "gcc" : "g++");
    formData.append('compiler-flags', compiler_flags);
    formData.append('linker-flags', linker_flags);
    
    /*
    var params = getAllUrlParams()
    
    if(!('user_id' in params)) {
        alert("user_id not set")
        return
    }
    formData.append('user_id', params['user_id']);
    */
    
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
          document.getElementById("submit_button").disabled = false;
          setTimeout(function() {alert("There was an error in the request")}, 0);
       }
    });
  }

  function onChangeLanguage(to)
  {
    return (e) =>
    {
      console.log("Target language has been changed to " + to + ", updating dropdown menu");
      var selector = document.getElementById("standard")
      selector.options.length = 0;
      for(var index in standards[to]) {
        selector.options[selector.options.length] = new Option(standards[to][index]['display']);
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

           getResults();

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

function getResults() {

  $.ajax({
    dataType: "json",
    url: '/api/v1/results/' + file_id,
    success: function(data) {

      if(data['success']) {
        document.getElementById('results_title').innerHTML = "Finished";
      } else {
        document.getElementById('results_title').innerHTML = "Could not compile";
        document.getElementById('download_button_container').style.display = 'none'
      }

      var str = data['messages'].join("\n")
      str = str.replace(/(?:\r\n|\r|\n)/g, '<br />');
      document.getElementById('results_text').innerHTML = str

      stopCompilingAnimation(data['success'])
    },
    error: function() {
      $('#compiling_spinner').hide();
      alert("could not get results")
      location.reload();
    }
  });

}

function makeCross() {
  $('.tick').css('display', "none");
  $('.cross__circle').toggleClass("go")
  $('.cross__path').toggleClass("go")
}

function startUploadingAnimation() {
  $('#uploading_spinner').toggleClass("invisible")
}

function startCompilingAnimation() {
  $('#uploading_spinner').hide()
  $('#waiting_step').slideDown()
}

function stopCompilingAnimation(success) {
  $('#compiling_spinner').hide();
  if(success) {
    $(".tick-trigger").toggleClass("drawn");
  } else {
    makeCross();
  }
  $('#download_step').slideDown();
}

function getAllUrlParams() {

  // get query string from url (optional) or window
  var queryString = window.location.search.slice(1);

  // we'll store the parameters here
  var obj = {};

  // if query string exists
  if (queryString) {

    // stuff after # is not part of query string, so get rid of it
    queryString = queryString.split('#')[0];

    // split our query string into its component parts
    var arr = queryString.split('&');

    for (var i=0; i<arr.length; i++) {
      // separate the keys and the values
      var a = arr[i].split('=');

      // in case params look like: list[]=thing1&list[]=thing2
      var paramNum = undefined;
      var paramName = a[0].replace(/\[\d*\]/, function(v) {
        paramNum = v.slice(1,-1);
        return '';
      });

      // set parameter value (use 'true' if empty)
      var paramValue = typeof(a[1])==='undefined' ? true : a[1];

      // (optional) keep case consistent
      paramName = paramName.toLowerCase();
      paramValue = paramValue.toLowerCase();

      // if parameter name already exists
      if (obj[paramName]) {
        // convert value to array (if still string)
        if (typeof obj[paramName] === 'string') {
          obj[paramName] = [obj[paramName]];
        }
        // if no array index number specified...
        if (typeof paramNum === 'undefined') {
          // put the value on the end of the array
          obj[paramName].push(paramValue);
        }
        // if array index number specified...
        else {
          // put the value at that index number
          obj[paramName][paramNum] = paramValue;
        }
      }
      // if param name doesn't exist yet, set it
      else {
        obj[paramName] = paramValue;
      }
    }
  }

  return obj;
}