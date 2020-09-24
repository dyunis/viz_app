'use strict'

function run_on_keycodes (func, ...codes) {
  let pressed = new Set()

  document.addEventListener('keydown', function (event) {
    pressed.add(event.keyCode)
    //clear the set so they have to be pressed quickly
    setTimeout(() => pressed.clear(), 100)

    for (let code of codes) {
      if (!pressed.has(code)) {
        return
      }
    }

    pressed.clear()

    func()
  })

  document.addEventListener('keyup', function (event) {
    pressed.delete(event.key)
  })
}

// ctrl-r to refresh plot
run_on_keycodes(update_plot, 17, 82)

function update_plot () {

  // make a post here with selected items from ykeys, xkey
  let y_options = Array.from(document.querySelector('#y').selectedOptions)
  let ykeys = y_options.map( (opt) => opt.value )
  let xkey = document.querySelector('#x').selectedOptions[0].value

  fetch('/options', {
    headers: {'Content-Type': 'application/json'},
    method: 'POST',
    body: JSON.stringify({
      'xkey': xkey,
      'ykeys': ykeys,
      'xlog': document.querySelector('#xlog').checked,
      'ylog': document.querySelector('#ylog').checked
    })
  }).then( function success () {
    // force a refresh of iframe
    let iframe = document.querySelector('iframe')
    iframe.src = iframe.src
  }, function failure () {
    console.log('error in POST')   
  })
}

function clear_selections (axis) {
  let id = axis === 'y' ? '#y' : '#x'
  $(id).val(null).trigger('change')
}


$(document).ready(function() {
  $('.js-example-placeholder-single').select2();
  $('.js-example-placeholder-multiple').select2();

  $('#x').select2({placeholder: 'X axis'});
  $('#y').select2({
    placeholder: 'Y axis',
    tags: true,
    createTag: function (params) {
      if (! RegExp(`^r'.+'$`).test(params.term)) {
        return null;
      }

      return {id: params.term, text: params.term}
    }
  });

  $('#x').val('step').trigger('change')
})
