<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Checkout</h1>
            </div>

            <div class="column is-12 box">
                <table id="customers" class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="order in order[0]?.cart.products"
                            v-bind:key="order.product.id"
                        >
                            <td>{{ order.product.name }}</td>
                            <td>{{ order.product.price }} ₺</td>
                            <td>{{ order.quantity }}</td>
                            <td>{{ getItemTotal(order).toFixed(2) }} ₺</td>
                        </tr>
                    </tbody>

                    <tfoot>
                        <tr>
                            <td colspan="2">Cart Total</td>
                            <td>{{ order[id]?.cart.get_cart_total }}</td>
                            <td>{{ order[id]?.get_cart_total }} ₺</td>
                        </tr>

                        <tr>
                            <td colspan="3">Shipping</td>
                            <td>{{ order[0]?.shipping }} ₺</td>
                        </tr>
                        <tr>
                            <td colspan="3">Tax</td>
                            <td>{{ order[0]?.get_tax_total }} ₺</td>
                        </tr>
                        <tr>
                            <td colspan="3">Total</td>
                            <td>{{ order[0]?.get_total }} ₺</td>
                        </tr>
                    </tfoot>
                </table>

<!--              <router-link to="/cart/success/"><button class="button is-dark">Give Order</button></router-link>-->
              <button class="button is-dark" @click="giveOrder">Give Order</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import OrderSummary from "../components/OrderSummary";

export default {
    name: 'Checkout',
    components: {
        OrderSummary
    },
    data() {
        return {
            order: {
              id: ''
            },
            orderID: '',
            isHidden: true,
            errors: []
        }
    },
    // beforeMount() {
    //   this.getMyOrders()
    // },
    mounted() {
        document.title = "Checkout | Let's Shop"
        // this.cart = this.$store.state.cart
        this.getMyOrders()
        console.log(this.order.cart)
        // console.log(this.orders.products)
        // console.log(this.cart.products)
        console.log("shipping")
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        completeCheckout() {
            axios
                .get('/checkout/')
                .then(response => {
                    this.order.id = response.data
                    orderID
                })
        },

        getMyOrders() {
            this.$store.commit('setIsLoading', true)
            axios
                .get('/checkout/')
                .then(response => {
                    console.log(response.data)
                    this.order = response.data //[response.data.length-1]
                    console.log(this.order)
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },

        async giveOrder() {
            let products = []
            let obj = {}

            for (let i = 0; i < this.order[0].cart.products.length; i++) {
                const item = this.order[0].cart.products[i]
                obj = {
                    product: item.product.id,
                    quantity: item.quantity,
                    price: item.product.price * item.quantity
                }
                products.push(obj)
            }
            console.log(obj)
            console.log(products)
            const data = {
                'products': products
            }

            await axios
                .post('/checkout/', data)
                .then(response => {
                    console.log(response.data.cart)
                    let items = response.data.cart.products
                    console.log(items)
                    // this.$store.commit('clearCart', item)
                    // let item = JSON.parse(localStorage.getItem('cart'))
                    console.log(items)
                    for (let i = 0; i < items.length; i++) {
                        let productID = items[i].id
                        console.log(productID)
                        console.log(items.id)
                        item.product.stock -= items.quantity
                        console.log(items.product.stock)
                        const temp_data = {
                          "stock": items.product.stock
                        }
                        axios.patch('product/' + productID + '/', temp_data)



                      // let temp = JSON.parse(this.order[0].cart.products[i])
                      // console.log(temp)
                      // this.order[0].cart.products = []

                      // item.product = {}
                      // item.quantity = 0
                    }
                  // item = JSON.stringify(item)
                  // localStorage.setItem('products', item)
                  // this.order[0].cart.products = []

                  // this.product.stock -= this.quantity
                  // console.log(this.product.stock)
                  // const temp_data = {
                  //   "stock": this.product.stock
                  // }
                  // console.log(this.product)
                  // console.log(productID)
                  // console.log(temp_data)
                  // return axios.patch('product/' + productID + '/', temp_data)

                  console.log(this.order[0])
                  this.$router.push('/cart/success')
                })
                .catch(error => {
                    this.errors.push('Something went wrong. Please try again')
                    console.log(error)
                })
                this.$store.commit('setIsLoading', false)
                // blablalll
        }
    },
    computed: {
        // cartTotalPrice() {
        //     return this.cart.products.reduce((acc, curVal) => {
        //         return acc += curVal.product.price * curVal.quantity
        //     }, 0)
        // },
        // cartTotalLength() {
        //     return this.cart.products.reduce((acc, curVal) => {
        //         return acc += curVal.quantity
        //     }, 0)
        // }
    }
}
</script>

<style>
#customers {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#customers td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#customers tr:nth-child(even){background-color: #f2f2f2;}

#customers tr:hover {background-color: #ddd;}

#customers th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #3e3737;
  color: white;
}
</style>