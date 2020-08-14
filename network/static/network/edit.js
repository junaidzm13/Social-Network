// function editpost(id){
//   console.log(id)
//   fetch(`/posts/${id}`)
//   .then(response => response.json())
//   .then(post => {
//     console.log(id)
//     document.querySelector(`.c${id} #postcontent`).style.display = 'none';
//     document.querySelector(`.c${id} #editcontent`).style.display = 'block';
//
//     document.querySelector(`.c${id} #edit-content`).innerHTML = `${post.content}`;
//     document.querySelector('#edit-form').onsubmit = function() {
//       const content =  document.querySelector('#edit-content').value;
//       console.log(content)
//       document.querySelector(`.c${id} #postcontent`).innerHTML = `${content}`
//       document.querySelector(`.c${id} #postcontent`).style.display = 'block';
//       document.querySelector(`.c${id} #editcontent`).style.display = 'none';
//       fetch('/posts', {
//         method: 'POST',
//         body: JSON.stringify({
//         new_content: content,
//         id: id
//         })
//       })
//       .then(response => response.json())
//       .then(result => {
//           // Print result
//           console.log(result);
//           alert(result.message);
//         });
//     };
//
//   });
// }


document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('#postcontent').forEach(function(post) {
    post.style.display = 'block';
  })
  document.querySelectorAll('#editcontent').forEach(function(post) {
    post.style.display = 'none';
  })

  //edit
  document.querySelectorAll('#edit').forEach(function(button) {
    button.onclick = function() {
      id = button.dataset.postid;
      fetch(`/posts/${id}`)
      .then(response => response.json())
      .then(post => {
        console.log(id);
        document.querySelector(`.c${id} #postcontent`).style.display = 'none';
        document.querySelector(`.c${id} #editcontent`).style.display = 'block';

        document.querySelector(`.c${id} #edit-content`).innerHTML = post.content;
        document.querySelector('#save').onclick = function() {
          const content =  document.querySelector('#edit-content').value;
          console.log(content);
          document.querySelector(`.c${id} #postcontent`).style.display = 'block';
          document.querySelector(`.c${id} #editcontent`).style.display = 'none';
          document.querySelector(`.c${id} #postcontent`).innerHTML = content;
          fetch('/posts', {
            method: 'POST',
            body: JSON.stringify({
            new_content: content,
            id: id
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print result
              console.log(result);
              alert(result.message);
            });
        };
      });
    }
  });

  // likes
  document.querySelectorAll('#likes').forEach(function(heart) {
    heart.onclick = function() {
      id = heart.dataset.postid

      fetch(`/posts/${id}`)
      .then(response => response.json())
      .then(post => {
        let num_likes = `${post.likes}`;
        console.log(num_likes);

        if(heart.style.color === 'red') {
          heart.style.color = 'grey';
          document.querySelector(`.c${id} span`).innerHTML = post.likes - 1;
          fetch(`/posts/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              color: 'white',
              id: id
            })
          })
        }
        else {
          heart.style.color = 'red';
          document.querySelector(`.c${id} span`).innerHTML = post.likes + 1;
          fetch(`/posts/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              color: 'red',
              id: id
            })
          })
        }
    // const id = heart.dataset.postid;
    // fetch(`/posts/${id}`)
    // .then(response => response.json())
    // .then(post => {

  });
};

});
});
