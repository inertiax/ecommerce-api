<template>
  <div class="page-product content">
    <div class="columns is-multiline">
      <div class="column is-9">
        <figure class="image mb-6">
          <img v-bind:src="product.image">
        </figure>

        <h1 class="title">{{ product.name }}</h1>
        <p><strong>Brand: </strong>{{ product.brand }}</p>
<!--        <p><strong>Category: </strong>{{ product.category.id }}</p>-->

        <p><strong>Description: </strong>{{ product.description }}</p>
        <p><strong>Stock: </strong>{{ product.stock }}</p>
      </div>

      <div class="column is-3">
        <h2 class="subtitle">Information</h2>

        <p><strong>Price: </strong>{{ product.price }} ₺</p>

        <div class="field has-addons mt-6">
          <div class="control">
            <input type="number" class="input" min="1" v-model="quantity">
          </div>

          <div class="control">
            <a class="button is-dark" @click="addToCart">Add to Cart</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import {toast} from "bulma-toast"

export default {
  name: "Product",
  // props: { id: String },
  data() {
    return {
      product: {},
      quantity: 1,
      product_id: 1
    }
  },
  mounted() {
    this.getProduct()
  },
  methods: {
    async getProduct() {
      this.$store.commit('setIsLoading', true)

      const productID = this.$route.params.id

      await axios
        .get('product/' + productID + '/')
        .then(response => {
          this.product = response.data

          document.title = this.product.name + " | Let's Shop"
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    },
    async addToCart() {

      const productID = this.$route.params.id

      if (this.product.stock !== 0) {
        if (isNaN(this.quantity) || this.quantity < 1) {
          this.quantity = 1
        }

        const product_id = this.product.id

        const item = {
          product_id: product_id,
          quantity: this.quantity
        }

        await axios
          .post('cart/', item)
          .then(response => {
            // this.$store.commit('addToCart', item)
            console.log(item)

            toast({
              message: 'Product was added to the cart',
              type: 'is-black',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'top-center'
            })
            this.product.stock -= this.quantity
            console.log(this.product.stock)
            const temp_data = {
              "stock": this.product.stock
            }
            console.log(this.product)
            console.log(productID)
            console.log(temp_data)
            return axios.patch('product/' + productID + '/', temp_data)
          })
          .catch(error => {
            console.log(error)
          })
      }
    }
  }
}
</script>

<style>
.content {
  width: 70%;
  margin: auto;
}
</style>