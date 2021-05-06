<template>
  <div class="page-product">
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
          <input type="text" class="input" v-model="category.title" required>
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

<!--      <div id="image-file-ex" class="file has-name">-->
<!--        <label class="file-label">-->
<!--          <input class="file-input" type="file" @change="onFileChange" name="image">-->
<!--          <span class="file-cta">-->
<!--            <span class="file-icon">-->
<!--              <i class="fas fa-upload"></i>-->
<!--            </span>-->
<!--            <span class="file-label">-->
<!--              Choose an image…-->
<!--            </span>-->
<!--          </span>-->
<!--          <span class="file-name">-->
<!--            No file uploaded-->
<!--          </span>-->
<!--        </label>-->
<!--      </div>-->
        <div id="app">
          <div v-if="!image">
            <h2>Select an image</h2>
            <input type="file" @change="onFileChange">
          </div>
          <div v-else>
            <img :src="image" />
            <button @click="removeImage">Remove image</button>
          </div>
        </div>

<!--      <div class="image-file">-->
<!--        <label for>Food picture</label>-->
<!--        <input type="file-input" name="file" @change="onFileChange">-->
<!--      </div>-->
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
      image: ''
    }
  },
  mounted() {
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
    // onFileChange(e) {
    //   let files = e.target.files || e.dataTransfer.files;
    //   if (!files.length) {
    //     return;
    //   }
    //   this.image = files[0];
    //   this.createImage(files[0]);
    // },
    // createImage(file) {
    //   // let image = new Image();
    //   let reader = new FileReader();
    //   let vm = this;
    //   reader.onload = e => {
    //     vm.preview = e.target.result;
    //   };
    //   reader.readAsDataURL(file);
    // },
    async addProduct() {
      const newProduct = {
        id: this.id,
        name: this.name,
        brand: this.brand,
        category: this.category.title,
        size: this.size,
        color: this.color,
        price: this.price,
        stock: this.stock,
        description: this.description,
        // image: this.image
      }
      // const fileInput = document.querySelector('#image-file-ex input[type=file]');
      // fileInput.onchange = () => {
      //   if (fileInput.files.length > 0) {
      //     const fileName = document.querySelector('#image-file-ex .file-name');
      //     fileName.textContent = fileInput.files[0].name;
      //   }
      // }
      this.$store.commit('setIsLoading', true)
      let formData = new FormData();
      formData.append("id", this.id)
      formData.append("name", this.name)
      formData.append("brand", this.brand)
      formData.append("category", this.category)
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
          // this.$router.push('/')
          this.$emit("fetchData")

          const toPath = this.$route.query.to || 'product/' + id + '/'
          this.$router.push(toPath)
          toast({
            message: 'Product added successfully',
            type: 'is-black',
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: 'top-center'
          })

          // document.title = this.product.name + " | Let's Shop"
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

#app {
  text-align: left;
}
img {
  width: 30%;
  margin: auto;
  display: block;
  margin-bottom: 10px;
}
button {

}
</style>