"use strict"
window.addEventListener("load", onLoad);

function onLoad(Event e) {
  getElementById("fileUpload-form").addEventListener("submit", onSubmitForm);

  function onSubmitForm(Event e) {
    alert("javascript interrutping submit");
    e.preventDefaults();
  }
}