document.addEventListener('DOMContentLoaded', function() {
    const search_field = document.querySelector('#search_field');
    const search_button = document.querySelector('#search_button');
    const page_title = document.querySelector('.page_title');

    console.log(page_title.innerHTML);
    let baseSearchUrl;
    if (page_title.innerHTML === "Users") {
      baseSearchUrl = "/user_search/";
    } else if (page_title.innerHTML === "Accounts") {
      baseSearchUrl = "/account_search/";
    } else if (page_title.innerHTML === "Billings") {
      baseSearchUrl = "/billing_search/";
    }

    function isAlphaNumeric(str) {
      var code, i, len;

      for (i = 0, len = str.length; i < len; i++) {
        code = str.charCodeAt(i);
        if (!(code > 47 && code < 58) && // numeric (0-9)
            !(code > 64 && code < 91) && // upper alpha (A-Z)
            !(code > 96 && code < 123) &&// lower alpha (a-z)
            !(code == 45) && // hyphen
            !(code == 95)) { // underscore
          return false;
        }
      }
      return true;
    };

    function searchIt(data) {
      if (isAlphaNumeric(data)) {

        window.location = baseSearchUrl + data;
      } else {
        alert("Would be great if you type letters and numbers ;)");
      };
    }

    search_field.addEventListener("keydown", function(event) {
        if (event.key === 'Enter') {
          event.preventDefault();
          searchIt(search_field.value);
        };
      });

    search_button.addEventListener("click", function(event) {
      event.preventDefault();
      searchIt(search_field.value);
    });
  });