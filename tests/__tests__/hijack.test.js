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
  test('hijack', async () => {
    const event = {
      currentTarget: {
        dataset: {
          hijackUser: '1',
          hijackNext: '/',
          hijackUrl: '/hijack/'
        }
      }
    }
    document.body.innerHTML =
      '<input name="csrfmiddlewaretoken" value="token">'
    globalThis.fetch = mock.fn()
    await hijack.hijack(event)
    const call = globalThis.fetch.mock.calls[0]
    assert(call.arguments[0] === '/hijack/')
    assert(call.arguments[1].method === 'POST')
    assert(call.arguments[1].credentials === 'same-origin')
    assert(call.arguments[1].body.get('csrfmiddlewaretoken') === 'token')
    assert(call.arguments[1].body.get('user_pk') === '1')
    assert(call.arguments[1].body.get('next') === '/')
  })
})
