"use strict"
window.addEventListener("load", onLoad);

function onLoad(e) {
  
  $('.message-button').click(displyMessage);
  
  
  function displyMessage(e) {
    e.preventDefault();
    var text_box = $(e.target).parent().parent().children('div.item-message')
    if(text_box.is(':visible')) {
      text_box.slideToggle()
    } else {
      var spinner = $(e.target).parent().children('div.spinner')
      spinner.toggleClass('invisible')
      var url = $(e.target).parent().children('input.message-url').get(0).value
      
      $.ajax({
        dataType: "json",
        url: url,
        success: function(data) {
          
          var str = data['messages'].join("\n")
          str = str.replace(/(?:\r\n|\r|\n)/g, '<br />');
          if(str.length == 0) {
            str = "No errors, or warnings"
          }
          text_box.html(str)
          
          spinner.toggleClass('invisible')
          text_box.slideToggle()
        },
        error: function() {
          $('#compiling_spinner').hide();
          alert("could not get results")
          spinner.toggleClass('invisible')
        }
      });
    }
    
  }
}

