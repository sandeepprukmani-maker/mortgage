<template>
  <div class="dashboard-main-body">

    <Breadcrumb title="Faq" :breadcrumbs="[
      { name: 'Faq' }
    ]" />

    <FrequentlyQuestion />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import FrequentlyQuestion from '@/components/FAQs/FrequentlyQuestion.vue'
export default {
    name: "FAQs",
    components: {
        Breadcrumb,
        FrequentlyQuestion,
    },
}
</script>