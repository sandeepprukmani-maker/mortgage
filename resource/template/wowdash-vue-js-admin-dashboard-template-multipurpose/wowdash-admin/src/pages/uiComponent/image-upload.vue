<template>
  <div class="dashboard-main-body">


    <Breadcrumb title="Upload" :breadcrumbs="[
      { name: 'Components / Upload' }
    ]" />

    <ImageUpload />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ImageUpload from '@/components/UiComponent/ImageUpload.vue'

export default {
  name: "Upload",
  components: {
    Breadcrumb,
    ImageUpload,
  },
}
</script>