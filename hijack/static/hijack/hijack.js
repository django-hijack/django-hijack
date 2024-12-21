/**
 * Given function will be executed when DOM is ready.
 * If DOM is already ready, function will be executed immediately.
 * @param {Function} fn - Function to be executed.
 * @param {object} context - Context to be used when executing function.
 * @returns {void}
 */
export function ready (fn, context) {
  context = context || document
  // http://youmightnotneedjquery.com/#ready
  if (context.readyState !== 'loading') {
    fn()
  } else {
    context.addEventListener('DOMContentLoaded', fn)
  }
}

/**
 * Given function will be executed when DOM is ready and the element exists.
 * @param {Function} fn - Function to be executed.
 * @param {string} query - Query selector to find element.
 * @returns {void}
 */
export function mount (fn, query) {
  ready(() => {
    document.querySelectorAll(query).forEach((element) => fn(element))
  })
}

/**
 * Hijack user session.
 * @param {Event} event - Click event.
 * @returns {void}
 */
export function hijack (event) {
  const element = event.currentTarget
  const form = document.createElement('form')
  form.method = 'POST'
  form.style.display = 'none'
  form.action = element.dataset.hijackUrl
  const csrfTokenInput = document.createElement('input')
  csrfTokenInput.type = 'hidden'
  csrfTokenInput.name = 'csrfmiddlewaretoken'
  csrfTokenInput.value =
    document.querySelector('input[name=csrfmiddlewaretoken]').value
  form.appendChild(csrfTokenInput)
  const userPkInput = document.createElement('input')
  userPkInput.type = 'hidden'
  userPkInput.name = 'user_pk'
  userPkInput.value = element.dataset.hijackUser
  form.appendChild(userPkInput)
  if (element.dataset.hijackNext) {
    const nextInput = document.createElement('input')
    nextInput.type = 'hidden'
    nextInput.name = 'next'
    nextInput.value = element.dataset.hijackNext
    form.appendChild(nextInput)
  }
  document.body.appendChild(form)
  form.submit()
}

mount(function (element) {
  element.addEventListener('click', hijack)
}, '[data-hijack-user]')
