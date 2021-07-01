'use strict'

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-hijack-user]').forEach(function (element) {
    element.addEventListener('click', (event) => {
      const data = new FormData()
      data.append('csrfmiddlewaretoken', document.querySelector('input[name=csrfmiddlewaretoken]').value)
      data.append('user_pk', element.dataset.hijackUser)
      if (element.dataset.hijackNext) {
        data.append('next', element.dataset.hijackNext)
      }
      fetch(element.dataset.hijackUrl, {
        method: 'POST',
        body: data,
        credentials: 'same-origin'
      }).then(function (response) {
        window.location.href = element.dataset.hijackNext
      })
    })
  })
})
