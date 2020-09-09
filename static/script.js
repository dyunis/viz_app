'use strict'

document.addEventListener('keyup', update)

function update (event) {
  if (event.keyCode == 85) {
    document.getElementsByTagName('button')[0].click()
  }
}
