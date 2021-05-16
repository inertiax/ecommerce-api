import { createStore } from 'vuex'

export default createStore({
  state: {
    cart: {
        products: [],
    },
    order: {},
    isAuthenticated: false,
    token: '',
    isLoading: false
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('cart')) {
        state.cart = JSON.parse(localStorage.getItem('cart'))
      } else {
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }

      if (localStorage.getItem('token')) {
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
      } else {
          state.token = ''
          state.isAuthenticated = false
      }
    },
    addToCart(state, item) {
      console.log(state.cart.products)
      const exists = state.cart.products.filter(i => i.product.id === item.product.id)
      if (exists.length) {
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      } else {
        state.cart.products.push(item)
      }

      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
        state.token = token
        state.isAuthenticated = true
        console.log(state.order)
        console.log(state.cart)
    },
    removeToken(state) {
        state.token = ''
        state.isAuthenticated = false
    },
    clearCart(state, item) {
      console.log(state.order)
      console.log(state.cart)
      state.cart.products = item
      state.cart.products = []
      // const products = state.cart.products

      // for (let i = 0; i < state.cart.products.length; i++) {
      //   let item = state.cart.products[i]
      //   console.log(item)
      //   item.product = {}
      //   item.quantity = 0
      // }
      // state.cart = { products: [] }
      console.log(state.order)

      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
  },
  actions: {
  },
  modules: {
  }
})