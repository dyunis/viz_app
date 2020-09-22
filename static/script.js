'use strict'

function update_plot () {

  // make a post here with selected items from ykeys, xkey
  let y_options = Array.from(document.getElementById('y').selectedOptions)
  let ykeys = y_options.map( (opt) => opt.value )
  let xkey = document.getElementById('x').selectedOptions[0].value

  fetch('/options', {
    headers: {'Content-Type': 'application/json'},
    method: 'POST',
    body: JSON.stringify({
      'xkey': xkey,
      'ykeys': ykeys,
      'xlog': document.getElementById('xlog').checked,
      'ylog': document.getElementById('ylog').checked
    })
  }).then( function success () {
    // force a refresh of iframe
    let iframe = document.getElementsByTagName('iframe')[0]
    iframe.src = iframe.src
  }, function failure () {
    console.log('error in POST')   
  })
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
})
