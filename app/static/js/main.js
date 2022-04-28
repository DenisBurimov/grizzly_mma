// custom javascript
(function () {
    'use strict'

    feather.replace({ 'aria-hidden': 'true' })

  })()

const close_flash = document.querySelector('.close');
const flash_block = document.querySelector('.hit_flash');
if (flash_block) {
  close_flash.addEventListener('click', function() {
    flash_block.classList.add('invisible');
  });
}
