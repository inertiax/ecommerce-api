<template>
    <tr>
        <td><router-link :to="{name: 'Product', params: {id: item.product.id}}">{{ item.product.name }}</router-link></td>
        <td>{{ item.product.price }} ₺</td>
        <td>
            {{ item.quantity }}
            <a @click="decrementQuantity(item)"><i class="fas fa-caret-down"></i></a>
            <a @click="incrementQuantity(item)"><i class="fas fa-caret-up"></i></a>
        </td>
        <td>{{ getItemTotal(item).toFixed(2) }} ₺</td>
        <td><button class="delete" @click="removeFromCart(item)"></button></td>
    </tr>
</template>

<script>
import axios from "axios";
import {toast} from "bulma-toast";

export default {
    name: 'CartItem',
    props: {
        initialItem: Object
    },
    data() {
        return {
            item: this.initialItem
        }
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        decrementQuantity(item) {
            item.quantity -= 1

            if (item.quantity === 0) {
                this.$emit('removeFromCart', item)
            }

            const decr_item = {
              product_id: item.product.id,
              quantity: item.quantity
            }

            axios
              .post('cart/', decr_item)
              .then(response => {
                // this.item = response.data
                this.$store.commit('addToCart', decr_item)
              })
              .catch(error => {
                console.log(error)
              })

            this.updateCart()
        },
        incrementQuantity(item) {

          item.quantity += 1

          const incr_item = {
            product_id: item.product.id,
            quantity: item.quantity
          }

          axios
            .post('cart/', incr_item)
            .then(response => {
              // this.item = response.data
              this.$store.commit('addToCart', incr_item)
            })
            .catch(error => {
              console.log(error)
            })

            this.updateCart()
        },
        updateCart() {
            localStorage.setItem('cart', JSON.stringify(this.$store.state.cart))
        },
        removeFromCart(item) {
            this.$emit('removeFromCart', item)
            this.updateCart()
        },
    },
}
</script>