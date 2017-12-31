"use strict"
window.addEventListener("load", onLoad);


function onLoad(e) {
  console.log("load")
  document.getElementById("fileUpload_form").addEventListener("submit", onSubmitForm);

  function onSubmitForm(e) {
    console.log("javascript interrutping submit");
    e.preventDefault();
    
    var file_input = document.getElementById("file_input");
    if(file_input.files.length < 1) {
      alert("no file")
      return;
    }
    var file = file_input.files[0]
    var formData = new FormData();
    formData.append('source.zip', file);
    //get the flags
    //formData.append('flags', jsonstring_of_flags)
    console.log(formData);
    $.ajax({
       url : '/api/v1/submit',
       type : 'PUT',
       data : formData,
       processData: false,
       contentType: false,
       enctype: 'multipart/form-data',
       success : function(data) {
           console.log(data);
           alert(data);
       }
    });
    
  }
}
