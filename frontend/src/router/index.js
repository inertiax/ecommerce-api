import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import Home from '../views/Home.vue'
import Product from "../views/Product.vue";
import Category from "../views/Category.vue";
import Cart from "../views/Cart.vue"
import OrderSuccess from "../views/OrderSuccess.vue"
import Checkout from "../views/Checkout.vue"
import LogIn from "../views/LogIn.vue"
import SignUp from "../views/SignUp.vue"
import Account from "../views/Account.vue"
import AddProduct from "../views/AddProduct.vue";


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/product/:id',
    name: 'Product',
    component: Product
  },
  {
    path: '/product/add',
    name: 'AddProduct',
    component: AddProduct
  },
  {
    path: '/category/',
    name: 'Category',
    component: Category
  },
  {
    path: '/cart/',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/cart/success',
    name: 'OrderSuccess',
    component: OrderSuccess
  },
  {
    path: '/checkout/',
    name: 'Checkout',
    component: Checkout,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/user/login/',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/user/signup/',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/user/get_user/',
    name: 'Account',
    component: Account,
    meta: {
      requireLogin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
