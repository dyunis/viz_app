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

async function update_paths () {
  let path_opts = Array.from(document.querySelector('#filename').selectedOptions)
  let paths = path_opts.map( (opt) => opt.value )
  let json = await fetch('/paths', {
    headers: {'Content-Type': 'application/json'},
    method: 'POST',
    body: JSON.stringify({
      'paths': paths
    })
  }).then( (response) => response.json(),
           () => console.log('failure on filename POST'))

  for (let path of json['rejected']){
    for (let opt of path_opts) {
      if (path == opt.value) {
        document.querySelector('[title="' + path + '"]').style.backgroundColor = 'rgba(255, 0, 0, 0.5)'
      }
    }
  }
}

async function update_plot () {

  // make a post here with selected items from ykeys, xkey
  let y_opts = Array.from(document.querySelector('#y').selectedOptions)
  let ykeys = y_opts.map( (opt) => opt.value )
  let xkey = document.querySelector('#x').selectedOptions[0].value

  let json = await fetch('/options', {
    headers: {'Content-Type': 'application/json'},
    method: 'POST',
    body: JSON.stringify({
      'xkey': xkey,
      'ykeys': ykeys,
      'xlog': document.querySelector('#xlog').checked,
      'ylog': document.querySelector('#ylog').checked
    })
  }).then( function success (response) {
    // force a refresh of iframe
    let iframe = document.querySelector('iframe')
    iframe.src = iframe.src
    return response.json()
  }, function failure () {
    console.log('error in POST')   
  })

  for (let ykey of json['rejected']){
    for (let opt of y_opts) {
      if (ykey == opt.value) {
        document.querySelector('[title="' + ykey + '"]').style.backgroundColor = 'rgba(255, 0, 0, 0.5)'
      }
    }
  }
}

function clear_selections (id) {
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
  $('#filename').select2({
    placeholder: 'Paths to load',
    tags: true,
    dropdownCssClass: 'hidden-dropdown'
  });

  $('#x').val('step').trigger('change')
})
