$(function() {
  var INDEX = 0; 
  $("#chat-submit").click(function(e) {
    e.preventDefault();
    var msg = $("#chat-input").val(); 
    if (msg.trim() == '') {
      return false;
    }
    generate_message(msg, 'self');

    setTimeout(function() {
      generate_messageoutput(msg, 'user');  
    }, 1000);
  });

  function generate_message(msg, type) {
    INDEX++;
    var str = "";
    str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
    str += "  <span class=\"msg-avatar\"></span>";
    str += "  <div class=\"cm-msg-text\">";
    str += msg;
    str += "  </div>";
    str += "</div>";
    $(".chat-logs").append(str);
    $("#cm-msg-"+INDEX).hide().fadeIn(300);
    if(type == 'self'){
      $("#chat-input").val(''); 
    }
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
  }

  $(document).delegate(".chat-btn", "click", function() {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, 'self');
  });

  $("#chat-circle").click(function() {    
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  });

  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  });
});

function generate_messageoutput(msg, type) {
  var INDEX = 0;
  INDEX++;
  var result = "ggggg";
  var str = "";
  str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
  str += "  <span class=\"msg-avatar\"></span>";
  str += "  <div class=\"cm-msg-text\">";
  fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    body: JSON.stringify({ 'message': msg }),
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(r => r.json())
    .then(r => {
      result = r.answer;
      str += result;
      str += "  </div>";
      str += "</div>";
      $(".chat-logs").append(str);
      $("#cm-msg-"+INDEX).hide().fadeIn(300);
      $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

 