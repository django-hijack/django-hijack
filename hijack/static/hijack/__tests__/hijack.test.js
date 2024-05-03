import { jest } from '@jest/globals'
import * as hijack from '../hijack'

jest.useFakeTimers()

afterEach(() => {
  jest.clearAllMocks()

})

describe('ready', () => {
  test('already', () => {
    const spy = jest.fn()
    expect(document.readyState).toBe('complete')

    hijack.ready(spy)
    expect(spy).toHaveBeenCalled()
  })

  test('ready', () => {
    const spy = jest.fn()
    Object.defineProperty(global.document, 'readyState', {
      writable: true,
      value: 'loading'
    })
    expect(document.readyState).toBe('loading')

    hijack.ready(spy)
    expect(spy).not.toHaveBeenCalled()

    document.dispatchEvent(new Event('DOMContentLoaded'))

    expect(spy).toHaveBeenCalled()
  })
})

describe('mount', () => {
  test('mount exists', () => {
    document.body.innerHTML = '<div class="foo"></div>'
    Object.defineProperty(global.document, 'readyState', {
      writable: true,
      value: 'loading'
    })
    const spy = jest.fn()
    hijack.mount(spy, 'div.foo')
    document.dispatchEvent(new Event('DOMContentLoaded'))
    expect(spy).toHaveBeenLastCalledWith(document.querySelector('div.foo'))
  })

  test('mount does not exist', () => {
    Object.defineProperty(global.document, 'readyState', {
      writable: true,
      value: 'loading'
    })
    const spy = jest.fn()
    document.body.innerHTML = '<div class="foo"></div>'
    hijack.mount(spy, 'div.does-not-exist')
    document.dispatchEvent(new Event('DOMContentLoaded'))
    expect(spy).not.toHaveBeenCalled()
  })
})

describe('hijack', () => {
  test('hijack', async () => {
    const event = {
      target: {
        dataset: {
          hijackUser: '1',
          hijackNext: '/',
          hijackUrl: '/hijack/'
        }
      }
    }
    document.body.innerHTML = '<input name="csrfmiddlewaretoken" value="token">'
    global.fetch = jest.fn()
    await hijack.hijack(event)
    expect(global.fetch).toHaveBeenCalledWith('/hijack/', {
      method: 'POST',
      body: expect.any(FormData),
      credentials: 'same-origin'
    })
  })
})
