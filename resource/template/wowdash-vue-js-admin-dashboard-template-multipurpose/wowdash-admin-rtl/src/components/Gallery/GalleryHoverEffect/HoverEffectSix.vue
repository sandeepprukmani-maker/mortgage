<template>
  <div class="mt-24 card h-100 p-0 radius-12 overflow-hidden gallery-scale">
    <div class="card-header">
      <h6 class="mb-0">Hover Effect 6</h6>
    </div>
    <div class="card-body p-24">
      <div class="row gy-4">
        <div class="col-xxl-3 col-md-4 col-sm-6" v-for="(img, index) in images" :key="index">
          <div class="hover-scale-img style-six border radius-16 overflow-hidden p-8">
            <a href="javascript:void(0)" class="popup-img w-100 h-100 d-flex radius-12 overflow-hidden"
              @click.prevent="openModal(img, index)">
              <img :src="img.src" :alt="img.alt" class="hover-scale-img__img w-100 h-100 object-fit-cover" />
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <span class="close" @click="closeModal">&times;</span>
      <span class="modal-nav prev" @click.stop="prevImage">&#10094;</span>
      <img class="modal-content" :src="modalImgSrc" :alt="modalImgAlt" />
      <span class="modal-nav next" @click.stop="nextImage">&#10095;</span>
      <div id="caption">{{ currentIndex + 1 }} of {{ images.length }}</div>
    </div>
  </div>
</template>

<script>
import galleryImg9 from '@/assets/images/gallery/gallery-img9.png'
import galleryImg10 from '@/assets/images/gallery/gallery-img10.png'
import galleryImg11 from '@/assets/images/gallery/gallery-img11.png'
import galleryImg12 from '@/assets/images/gallery/gallery-img12.png'

export default {
  data() {
    return {
      showModal: false,
      modalImgSrc: '',
      modalImgAlt: '',
      currentIndex: 0,
      images: [
        { src: galleryImg9, alt: 'Image 9' },
        { src: galleryImg10, alt: 'Image 10' },
        { src: galleryImg11, alt: 'Image 11' },
        { src: galleryImg12, alt: 'Image 12' }
      ]
    }
  },
  methods: {
    openModal(img, index) {
      this.modalImgSrc = img.src
      this.modalImgAlt = img.alt
      this.currentIndex = index
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
    },
    nextImage() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length
      this.updateModalImage()
    },
    prevImage() {
      this.currentIndex =
        (this.currentIndex - 1 + this.images.length) % this.images.length
      this.updateModalImage()
    },
    updateModalImage() {
      const img = this.images[this.currentIndex]
      this.modalImgSrc = img.src
      this.modalImgAlt = img.alt
    }
  }
}
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  z-index: 1050;
  padding-top: 225px;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.849);
}

.modal-content {
  margin: auto;
  display: block;
  width: 80%;
  max-width: 700px;
}

#caption {
  margin: auto;
  display: block;
  width: 80%;
  max-width: 700px;
  text-align: center;
  color: #ccc;
  padding: 10px 0;
  height: 100px;
  font-size: 22px;
}

.modal-content,
#caption {
  animation-name: zoom;
  animation-duration: 0.6s;
}

@keyframes zoom {
  from {
    transform: scale(0);
  }

  to {
    transform: scale(1);
  }
}

.close {
  position: absolute;
  top: 15px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: #bbb;
  text-decoration: none;
}

.modal-nav {
  cursor: pointer;
  position: absolute;
  top: 45%;
  color: white;
  font-size: 40px;
  font-weight: bold;
  padding: 16px;
  user-select: none;
  transition: 0.3s;
  z-index: 1060;
}

.modal-nav:hover {
  color: #bbb;
}

.modal-nav.prev {
  left: 20px;
}

.modal-nav.next {
  right: 20px;
}

@media only screen and (max-width: 700px) {
  .modal-content {
    width: 100%;
  }
}
</style>