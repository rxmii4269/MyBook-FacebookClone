let button = document.getElementById("follow"); // add friend button

let addFriend = function () {
  // api post request to add friend
  fetch("/api/add", {
    method: "POST",
    body: JSON.stringify(button.value), //create a json object with the value of the follow button
    headers: {
      // headers to pass into the post request.
      "Content-Type": "application/json", //signifies the type of content being sent
      "X-CSRFToken": token, //csrf token to prevent xss attacks. ie. validation
    },
    credentials: "same-origin", //pass the same session id of the current session ..enforces CORS
  })
    .then(function (response) {
      //on response from the server change button to added
      button.innerHTML = "Added";
      return response.json();
    })
    .catch(function (error) {
      //log error to console.. debugging purposes
      console.log(error);
    });
};

if (document.getElementsByClassName("username").item(0)) {
  // change webpage title to include username
  title = document.getElementsByClassName("username").item(0).textContent;
  if (document.title != title) {
    document.title = ` ${title} | ${document.title} `;
  } else {
    document.title = document.title;
  }
} else {
}

let edit = $(".edit"); //jQuery object for the edit profile button
$("#photo").attr("aria-describedby", "upload"); // jQuery object for the photo field on the edit profile page
$("#datepicker").attr("data-provide", "datepicker-inline"); //jQuery object for the date field on the register page
$(".datepicker").attr("data-provide", "datepicker-inline"); // jQuery object for the date field on the edit profile page

$("#datepicker").datepicker({
  format: "yyyy/mm/dd",
  autoclose: true,
  clearBtn: true,
  keyBoardNavigation: true,
});

$(".datepicker").datepicker({
  format: "yyyy/mm/dd",
  autoclose: true,
  clearBtn: true,
  keyBoardNavigation: true,
});

$(".photo-btn").click(() => {
  $(".post-form").replaceWith($(".photo-form"));
  $(".photo-form").removeAttr("hidden");
  $(".photo-btn").hide();
  $("#photo").val();
});


$(".comment-btn").click(function(){
    let comment_btn = $(this).attr('value');
    let comment = $(this).closest('div').prev('input').val()
    package = JSON.stringify({comment_btn,comment})
    // console.log($button.attr('value'),input)
    if (comment.length===0){

    }else{
      fetch('/api/comment',{
        method : 'POST',
        body: package,
        headers: {
          // headers to pass into the post request.
          "Content-Type": "application/json", //signifies the type of content being sent
          "X-CSRFToken": token, //csrf token to prevent xss attacks. ie. validation
        },
        credentials: "same-origin",
      });
    }
    location.reload()
});


$(".photo_comment-btn").click(function(){
  let comment_btn = $(this).attr('value');
  let comment = $(this).closest('div').prev('input').val()
  package = JSON.stringify({comment_btn,comment})
  // console.log($button.attr('value'),input)
  if (comment.length===0){

  }else{
    fetch('/api/comment/photo',{
      method : 'POST',
      body: package,
      headers: {
        // headers to pass into the post request.
        "Content-Type": "application/json",
        "X-CSRFToken": token, //signifies the type of content being sent
      },
      credentials: "same-origin",
    });
  }
  // location.reload()
});
$(".content-editor").click(function(){
  let group_btn = $(this).attr('value');
  let group_id = $(".groupname").attr('id')
 
  package = JSON.stringify({group_btn,group_id})
  
  fetch('/api/add/group',{
    method: 'POST',
    body: package,
    headers: {
      "Content-Type": "application/json", //signifies the type of content being sent
      "X-CSRFToken": token, //csrf token to prevent xss attacks. ie. validation
    },
    credentials: "same-origin",  
    
  });
})