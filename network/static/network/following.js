document.addEventListener('DOMContentLoaded', function() {

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

  });
};

});
});
