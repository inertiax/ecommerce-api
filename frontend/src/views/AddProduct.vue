<template>
  <div class="content page-product">
    <div class="row">
      <div class="column is-9">
        <h1 class="title">Add New Product</h1>
      </div>
    </div>

    <form @submit.prevent="AddProduct">
      <div class="field">
        <label class="label">Name</label>
        <div class="control">
          <input type="text" class="input" v-model="name" required>
        </div>
      </div>

      <div class="field">
        <label class="label">Brand</label>
        <div class="control">
          <input type="text" class="input" v-model="brand" required>
        </div>
      </div>

      <div class="field">
        <label class="label">Category</label>
        <div class="control">
          <input type="text" class="input" v-model="category.title">
<!--          <select name="category" class="select" v-for="categories in category" v-bind:key="categories.title.id">-->
<!--            <option value="categories.title.id">{{ categories.title }}</option>-->
<!--          </select>-->
        </div>
      </div>

      <div class="field">
        <label class="label">Size</label>
        <div class="select">
          <select name="size" class="select" v-model="size">
            <option value="">None</option>
            <option value="S">S</option>
            <option value="M">M</option>
            <option value="L">L</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label class="label">Color</label>
        <div class="select">
          <select name="color" class="select" v-model="color">
            <option value="">None</option>
            <option value="BLACK">Black</option>
            <option value="BLUE">Blue</option>
            <option value="WHITE">White</option>
            <option value="GREEN">Green</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label class="label">Price</label>
        <div class="control">
          <input type="text" class="input" v-model="price">
        </div>
      </div>

      <div class="field">
        <label class="label">Stock</label>
        <div class="control">
          <input type="text" class="input" v-model="stock">
        </div>
      </div>

      <div class="field">
        <label class="label">Description</label>
        <div class="control">
          <input type="text" class="input" v-model="description">
        </div>
      </div>

      <div id="app">
        <div v-if="!image">
          <h3>Select an image</h3>
          <input type="file" @change="onFileChange">
        </div>

        <div v-else>
          <img :src="image" />
          <button @click="removeImage">Remove image</button>
        </div>
      </div>

      <br>
      <div class="notification is-danger" v-if="errors.length">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
      </div>

      <br>
      <div class="control">
        <a class="button is-dark" @click="addProduct">Add Product</a>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios"
import {toast} from "bulma-toast"

export default {
  name: "AddProduct",
  data() {
    return {
      name: '',
      brand: '',
      category: {
        title: ''
      },
      size: {},
      color: {},
      price: '',
      stock: '',
      description: '',
      image: '',
      errors: []
    }
  },
  mounted() {
    document.title = "Add Product | Let's Shop"
    console.log(this.category.title)
    if (!localStorage.getItem('token')) {
      this.$router.push({name : 'LogIn'});
    }
  },
  methods: {
    onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      this.imageFiles = files
      this.createImage(files[0]);
    },
    createImage(file) {
      var image = new Image();
      var reader = new FileReader();

      reader.onload = (e) => {
        this.image = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    removeImage: function (e) {
      this.image = '';
    },
    async addProduct() {
      this.errors = []
      if (this.name === '') {
          this.errors.push('You should add a name')
      }
      if (this.brand === '') {
          this.errors.push('You should add a brand')
      }
      if (this.category.title === '') {
          this.errors.push('You should add a category')
      }
      if (isNaN(this.size)) {
          this.errors.push('Select a size or select None.')
      }
      if (isNaN(this.color)) {
          this.errors.push('Select a color or select None.')
      }
      if (isNaN(this.price)) {
          this.errors.push('Price should be a number')
      }
      if (this.price < 0) {
          this.errors.push('Price should be a positive number')
      }
      if (this.price === '') {
          this.errors.push('You should enter a price')
      }
      if (isNaN(this.stock)) {
          this.errors.push('Stock should be a price number')
      }
      if (this.stock < 0) {
          this.errors.push('Stock should be a positive number or zero')
      }
      if (this.stock === '') {
          this.errors.push('You should enter a stock number')
      }
      if (this.description === '') {
          this.errors.push('You should enter a description')
      }
      if (this.image === '') {
          this.errors.push('You should select an image')
      }
      if (!this.errors.length) {
        let formData = new FormData();
        formData.append("id", this.id)
        formData.append("name", this.name)
        formData.append("brand", this.brand)
        formData.append("category", this.category.title)
        formData.append("size", this.size)
        formData.append("color", this.color)
        formData.append("price", this.price)
        formData.append("stock", this.stock)
        formData.append("description", this.description)
        formData.append("image", this.imageFiles[0]);


        await axios
          .post('product/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        })
          .then(response => {
            this.$router.push('/')
            this.$emit("fetchData")

            // const toPath = this.$route.query.to || 'product/' + id + '/'
            // this.$router.push(toPath)

            toast({
              message: 'Product added successfully',
              type: 'is-black',
              dismissible: true,
              pauseOnHover: true,
              duration: 3000,
              position: 'top-center'
            })

          })
          .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    this.errors.push(`${property}: ${error.response.data[property]}`)
                }
                console.log(JSON.stringify(error.response.data))
            } else if (error.message) {
                this.errors.push('Something went wrong. Please try again')

                console.log(JSON.stringify(error))
            }
          })
        // this.$store.commit('setIsLoading', false)
      }
    }
  }
}
</script>

<style>

.content {
  max-width: 800px;
  margin: auto;
}

#app {
  text-align: left;
}
.img {
  width: 30%;
  margin: auto;
  display: block;
  margin-bottom: 10px;
}
button {

}
</style>