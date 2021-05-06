<!--<template>-->
<!--  <div class="page-category">-->
<!--    <div class="columns is-multiline">-->
<!--      <div class="column is-12">-->
<!--        <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>-->
<!--      </div>-->

<!--      <div class="column is-3" v-for="category in category.products" v-bind:key="product.id">-->
<!--        <div class="box">-->
<!--          <figure class="image mb-4">-->
<!--            <img v-bind:src="product.thumbnail">-->
<!--          </figure>-->

<!--          <h3 class="is-size-4">{{ product.name }}</h3>-->
<!--          <p class="is-size-6 has-text-grey-dark">{{ product.price }} ₺</p>-->

<!--&lt;!&ndash;          <router-link :to="product.id" class="button is-dark is-centered mt-4">View Details</router-link>&ndash;&gt;-->
<!--          <router-link :to="{name: 'Product', params: {id: product.id}}" class="button is-dark is-centered mt-4">View Details</router-link>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import axios from "axios"-->
<!--import { toast } from "bulma-toast"-->


<!--export default {-->
<!--  name: "Category",-->
<!--  data() {-->
<!--    return {-->
<!--      category: {-->
<!--        products: []-->
<!--      }-->
<!--    }-->
<!--  },-->
<!--  mounted() {-->
<!--    this.getCategory()-->
<!--  },-->
<!--  methods: {-->
<!--    async getCategory() {-->
<!--      this.$store.commit('setIsLoading', true)-->

<!--      const categoryID = this.$route.params.id-->

<!--      axios-->
<!--        .get('category/' + categoryID + '/')-->
<!--        .then(response => {-->
<!--          this.category = response.data-->

<!--          document.title = this.category.name + " | Let's Shop"-->
<!--        })-->
<!--        .catch(error => {-->
<!--          console.log(error)-->

<!--          toast({-->
<!--            message: 'Something went wrong. Try again.',-->
<!--            type: 'is-danger',-->
<!--            dismissible: true,-->
<!--            pauseOnHover: true,-->
<!--            duration: 2000,-->
<!--            position: 'top-center'-->
<!--          })-->
<!--        })-->

<!--      this.$store.commit('setIsLoading', false)-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style scoped>-->

<!--</style>-->

<template>
    <div class="page-category">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>
            </div>

            <ProductBox
                v-for="product in category.products"
                v-bind:key="product.id"
                v-bind:product="product" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import ProductBox from '@/components/ProductBox'
export default {
    name: 'Category',
    components: {
        ProductBox
    },
    data() {
        return {
            category: {
                products: []
            }
        }
    },
    mounted() {
        this.getCategory()
    },
    watch: {
        $route(to, from) {
            if (to.name === 'Category') {
                this.getCategory()
            }
        }
    },
    methods: {
        async getCategory() {
            const categorySlug = this.$route.params.category_slug
            this.$store.commit('setIsLoading', true)
            axios
                .get('/products/' + categorySlug + '/')
                .then(response => {
                    this.category = response.data
                    document.title = this.category.name + " | Let's Shop"
                })
                .catch(error => {
                    console.log(error)
                    toast({
                        message: 'Something went wrong. Please try again.',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                })
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>