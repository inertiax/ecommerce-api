<template>
  <div class="home">
    <section class="hero is-dark is-medium mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">Welcome</p>
        <p class="subtitle">Best Store Ever</p>
      </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-3 has-text-centered">Latest Products</h2>
      </div>

      <div class="column is-3" v-for="product in latestProducts" v-bind:key="product.id">
        <div class="box">
          <figure class="image mb-4">
            <img v-bind:src="product.image">
          </figure>

          <h3 class="is-size-4">{{ product.name }}</h3>
          <p class="is-size-6 has-text-grey-dark">{{ product.price }} ₺</p>

<!--          <router-link :to="product.id" class="button is-dark is-centered mt-4">View Details</router-link>-->
          <router-link :to="{name: 'Product', params: {id: product.id}}" class="button is-dark is-centered mt-4">View Details</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      latestProducts: []
    }
  },
  components: {

  },
  mounted () {
    this.getLatestProducts()

    document.title = "Home | Let's Shop"
  },
  methods: {
    async getLatestProducts() {
      this.$store.commit('setIsLoading', true)

      await axios
      .get('/product/')
      .then(response => {
        this.latestProducts = response.data
      })
      .catch(error => {
        console.log(error)
      })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>

<style>
  .image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
  }
</style>
