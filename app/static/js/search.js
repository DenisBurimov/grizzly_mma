document.addEventListener('DOMContentLoaded', function() {
    const search_field = document.querySelector('#search_field');
    const search_button = document.querySelector('#search_button');
    search_field.addEventListener("keydown", function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            search_button.click();
            console.log(window.location);
            window.location = "/search/" + search_field.value;
        };
      });
    });