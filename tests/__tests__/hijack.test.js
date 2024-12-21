import 'global-jsdom/register'
import assert from 'node:assert'
import { afterEach, describe, mock, test } from 'node:test'
import * as hijack from '../../hijack/static/hijack/hijack.js'

afterEach(() => {
  mock.restoreAll()
})

describe('ready', () => {
  test('already', () => {
    const spy = mock.fn()
    assert(document.readyState === 'complete')

    hijack.ready(spy)
    assert(spy.mock.callCount())
  })

  test('ready', () => {
    const spy = mock.fn()
    Object.defineProperty(globalThis.document, 'readyState', {
      writable: true,
      value: 'loading'
    })
    assert(document.readyState === 'loading')

    hijack.ready(spy)
    assert(!spy.mock.callCount())

    document.dispatchEvent(new window.Event('DOMContentLoaded'))

    assert(spy.mock.callCount())
  })
})

describe('mount', () => {
  test('mount exists', () => {
    document.body.innerHTML = '<div class="foo"></div>'
    Object.defineProperty(globalThis.document, 'readyState', {
      writable: true,
      value: 'loading'
    })
    const spy = mock.fn()
    hijack.mount(spy, 'div.foo')
    document.dispatchEvent(new window.Event('DOMContentLoaded'))
    assert(
      spy.mock.calls[0].arguments[0] === document.querySelector('div.foo')
    )
  })

  test('mount does not exist', () => {
    Object.defineProperty(globalThis.document, 'readyState', {
      writable: true,
      value: 'loading'
    })
    const spy = mock.fn()
    document.body.innerHTML = '<div class="foo"></div>'
    hijack.mount(spy, 'div.does-not-exist')
    document.dispatchEvent(new window.Event('DOMContentLoaded'))
    console.warn(spy.mock.calls)
    assert(!spy.mock.callCount())
  })
})

describe('hijack', () => {
  test('hijack', () => {
    const event = {
      currentTarget: {
        dataset: {
          hijackUser: '1',
          hijackNext: '/',
          hijackUrl: '/hijack/'
        }
      }
    }
    document.body.innerHTML = '<input name="csrfmiddlewaretoken" value="token">'
    hijack.hijack(event)
    assert.equal(
      document.body.innerHTML,
      '<input name="csrfmiddlewaretoken" value="token"><form method="POST" style="display: none;" action="/hijack/"><input type="hidden" name="csrfmiddlewaretoken" value="token"><input type="hidden" name="user_pk" value="1"><input type="hidden" name="next" value="/"></form>')
  })
})
