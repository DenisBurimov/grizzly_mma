document.addEventListener('DOMContentLoaded', function() {
    const search_field = document.querySelector('#search_field');
    const search_button = document.querySelector('#search_button');

    function isAlphaNumeric(str) {
      var code, i, len;

      for (i = 0, len = str.length; i < len; i++) {
        code = str.charCodeAt(i);
        if (!(code > 47 && code < 58) && // numeric (0-9)
            !(code > 64 && code < 91) && // upper alpha (A-Z)
            !(code > 96 && code < 123)) { // lower alpha (a-z)
          return false;
        }
      }
      return true;
    };

    search_field.addEventListener("keydown", function(event) {
        if (event.key === 'Enter') {
          if (isAlphaNumeric(search_field.value)) {
            event.preventDefault();
            search_button.click();
            window.location = "/search/" + search_field.value;
          } else {
            alert("Would be great if you type letters and numbers ;)");
          };
        };
      });
    });