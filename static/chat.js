$(function() {
  var INDEX = 0; 
  $("#chat-submit").click(function(e) {
    e.preventDefault();
    var msg = $("#chat-input").val(); 
    if(msg.trim() == ''){
      return false;
    }
    /////input
    generate_message(msg, 'self');

    setTimeout(function() {   
      //out   
      generate_messageoutput(msg, 'user');  
    }, 1000)
    
  })
  
  

  

  function generate_message(msg, type) {
    INDEX++;
    var result ;

    var str="";
    str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
    str += "          <span class=\"msg-avatar\">";
   // str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
    str += "          <\/span>";
    str += "          <div class=\"cm-msg-text\">";

 
       console.log('*msg**'+msg);
       str += msg;      
 
   
    str += "          <\/div>";
    str += "        <\/div>";
    $(".chat-logs").append(str);
    $("#cm-msg-"+INDEX).hide().fadeIn(300);
     
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000); 
 
  }  
  

  
  $(document).delegate(".chat-btn", "click", function() {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, 'self');
  })
  
  $("#chat-circle").click(function() {    
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
  
  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
  
})

/*function chatbot_response(msg) {   
  fetch('http://127.0.0.1:5000/predict',{
   method: 'POST',
   body: JSON.stringify({ 'message': msg }),
   mode: 'cors',
   headers: {
       'Content-Type': 'application/json'
   },
})
   .then(r => r.json())
   .then(r => {
    var str =r.answer;
    console.log('***'+str);

    console.log('*test**'+r.answer);
       return r.answer;
      

   })
   .catch((error) => {
       console.error('Error:', error);
       
   });
}*/



function generate_messageoutput(msg, type) {
var INDEX=0;
INDEX++;
var result = "ggggg";

var str="";
str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
str += "          <span class=\"msg-avatar\">";
// str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
str += "          <\/span>";
str += "          <div class=\"cm-msg-text\">";
fetch('http://127.0.0.1:5000/predict',{
  method: 'POST',
  body: JSON.stringify({ 'message': msg }),
  mode: 'cors',
  headers: {
      'Content-Type': 'application/json'
  },
})
  .then(r => r.json())
  .then(r => {
  console.log('*test2: **'+r.answer);
   result =r.answer;


   console.log("final"+result);
   str += "          <\/div>";
   str += "        <\/div>";
   console.log("result"+result);
   $(".chat-logs").append(result);
  // $(".chat-logs").append("kkkkkkkk");
 
 
   $("#cm-msg-"+INDEX).hide().fadeIn(300);
    
   $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000); 
   console.log('*strfinal**'+str);



   console.log('*str**'+result);
    //  return r.answer;
     

  })
  .catch((error) => {
      console.error('Error:', error);
      
  });


} 