<template>
    <div class="page-log-in">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Log in</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="text" class="input" v-model="email">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Log in</button>
                        </div>
                    </div>

                    <hr>

                    Or <router-link to="/user/signup/">click here</router-link> to sign up!
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from "bulma-toast"

export default {
    name: 'LogIn',
    data() {
        return {
            email: '',
            password: '',
            errors: []
        }
    },
    mounted() {
        document.title = "Log In | Let's Shop"
    },
    methods: {
        async submitForm() {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            const formData = {
                email: this.email,
                password: this.password
            }
            await axios
                .post("/user/login/", formData)
                .then(response => {
                    const token = response.data.access;
                    console.log(token)
                    this.$store.commit('setToken', token)

                    axios.defaults.headers.common["Authorization"] = "Bearer " + token
                    localStorage.setItem("token", token)
                    const toPath = this.$route.query.to || '/'
                    this.$router.push(toPath)

                    toast({
                      message: 'You have logged in!',
                      type: 'is-success is-light',
                      dismissible: true,
                      pauseOnHover: true,
                      duration: 2000,
                      position: 'top-center'
                    })
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else {
                        this.errors.push('Something went wrong. Please try again')

                        console.log(JSON.stringify(error))
                    }
                })
        },
        async talkToServer(email, password) {
          var data = JSON.stringify("FAILURE")
          await axios
            .post('/user/login/')
        }
    }
}
</script>