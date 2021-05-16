<template>
    <div class="page-cart">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Cart</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth" v-if="cart.items.get_cart_total">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        <CartItem
                            v-for="item in cart.items.products"
                            v-bind:key="item.product.id"
                            v-bind:initialItem="item"
                            v-on:removeFromCart="removeFromCart" />
                    </tbody>
                </table>

                <p v-else>You don't have any items in your cart...</p>
            </div>

            <div class="column is-12 box">
                <h2 class="subtitle">Summary</h2>

                <strong>Number of Items: </strong>{{ cart.items.get_cart_total }} items
                <br>
                <strong>Tax Total: </strong>{{ cart.items.get_tax_total }} ₺
                <br>
                <strong>Cart Total: </strong>{{ cart.items.get_total }} ₺
<!--              <hr>-->
<!--                <strong>{{ products.get_total }} ₺</strong>, {{ products.get_cart_total }} items-->

                <hr>

                <router-link to="/checkout/" class="button is-dark">Proceed to checkout</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import CartItem from '@/components/CartItem.vue'

export default {
    name: 'Cart',
    components: {
        CartItem
    },
    data() {
        return {
            cart: {
              items: []
            },
            // products: [],
            // get_total: '',
            // get_tax_total: '',
            // get_cart_total: ''
        }
    },
    mounted() {
        this.getMyCart()

    },
    methods: {
        async getMyCart() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/cart/')
                .then(response => {
                    this.cart.items = response.data
                    console.log(this.cart.items)
                    // console.log(this.products.products)
                    // console.log(this.products.get_total)
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        async removeFromCart(item) {
            // console.log(item)
            // console.log(item.id)
            await axios
                .delete('cart/' + item.id + '/')
                .then(response => {

                  this.cart.items.products = this.cart.items.products.filter(i => i.product.id !== item.product.id)
                })
                .catch(error => {
                  console.log(error)
                })
        }
    },
    computed: {
        cartTotalLength() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        cartTotalPrice() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.product.price * curVal.quantity
            }, 0)
        },
    }
}
</script>