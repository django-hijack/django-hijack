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
    document.querySelectorAll(query).forEach(element => fn(element))
  })
}

/**
 * Hijack user session.
 * @param {Event} event - Click event.
 * @return {Promise<void>}
 */
export async function hijack (event) {
  const element = event.target
  const form = new FormData()
  form.append('csrfmiddlewaretoken', document.querySelector('input[name=csrfmiddlewaretoken]').value)
  form.append('user_pk', element.dataset.hijackUser)
  if (element.dataset.hijackNext) {
    form.append('next', element.dataset.hijackNext)
  }
  await fetch(element.dataset.hijackUrl, {
    method: 'POST',
    body: form,
    credentials: 'same-origin'
  })
  window.location.href = element.dataset.hijackNext
}

mount(function (element) { element.addEventListener('click', hijack) }, '[data-hijack-user]')
