<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Let's Shop</strong></router-link>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu}">
        <div class="navbar-end">

          <div class="navbar-item">
            <div class="buttons">

              <template v-if="$store.state.isAuthenticated">
                <router-link to="/user/get_user/" class="button is-light">My Account</router-link>
                <router-link to="/product/add" class="button is-light">Add Product</router-link>
              </template>

              <template v-else>
                <router-link to="/user/login/" class="button is-light">
                  <span class="icon"><i class="fas fa-sign-in-alt"></i></span>
                  <span>Log In</span>
                </router-link>
              </template>

              <router-link to="/cart/" class="button is-primary is-light">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                <span>Cart ({{ cart.products.get_cart_total }})</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </div>

  <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading}">
    <div class="lds-dual-ring"></div>
  </div>

  <section class="section">
    <router-view/>
  </section>

  <footer class="footer">
    <p class="has-text-centered">Copyright (c) 2021</p>
  </footer>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      showMobileMenu: false,
      cart: {
        products: []
      }
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token
    if (token) {
        axios.defaults.headers.common['Authorization'] = "Bearer " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.getMyCart()
    // this.cart = this.$store.state.cart
  },
  methods: {
      async getMyCart() {
          this.$store.commit('setIsLoading', true)
          await axios
              .get('/cart/')
              .then(response => {
                  this.cart.products = response.data
              })
              .catch(error => {
                  console.log(error)
              })
          this.$store.commit('setIsLoading', false)
      },
  },
  computed: {
    cartTotalLength() {
      let totalLength = 0

      for (let i = 0; i < this.cart.products.length; i++) {
        totalLength += this.cart.products[i].quantity
      }
      return totalLength
    }
  }
}
</script>

<style lang="scss">
@import "../node_modules/bulma";

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.is-loading-bar {
  height: 0;
  overflow: hidden;

  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}
</style>
