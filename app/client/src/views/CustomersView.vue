<template>
  <DashboardLayout page-title="Customers" max-width="7xl">
    <!-- Header -->
    <header class="mb-8">
      <h2 class="m-0 text-3xl text-neutral-800 font-semibold">Customers</h2>
      <p class="mt-2 text-neutral-500 text-lg">
        {{ customersList.total }} {{ customersList.total === 1 ? 'customer' : 'customers' }}
      </p>
    </header>

    <!-- Error Alert -->
    <BaseAlert v-if="error" variant="error" class="mb-6" @close="error = null">
      {{ error }}
    </BaseAlert>

    <!-- Success Alert -->
    <BaseAlert v-if="successMessage" variant="success" class="mb-6" @close="successMessage = null">
      {{ successMessage }}
    </BaseAlert>

    <!-- Customers Table -->
    <div class="bg-white rounded-lg shadow-card overflow-hidden">
      <CustomerTable
        :customers="customersWithPrices"
        :loading="isLoading"
        :loading-quotes="loadingQuotes"
        @quote-requested="handleQuoteRequest"
        @price-clicked="handlePriceClick"
      />
    </div>

    <!-- Pricing Modal -->
    <PricingModal
      :show="showModal"
      :best-price="selectedQuote?.best_price || 'N/A'"
      :full-response="selectedQuote?.full_response || {}"
      @close="closeModal"
    />
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import DashboardLayout from '../layouts/DashboardLayout.vue';
import BaseAlert from '../components/ui/BaseAlert.vue';
import CustomerTable from '../components/CustomerTable.vue';
import PricingModal from '../components/PricingModal.vue';
import { customerService } from '../services/customerService';
import { pricingService } from '../services/pricingService';

const customersList = ref({ customers: [], total: 0 });
const isLoading = ref(false);
const error = ref(null);
const successMessage = ref(null);
const loadingQuotes = ref({});
const customerQuotes = ref({});
const showModal = ref(false);
const selectedQuote = ref(null);
const uwmConfig = ref(null);

// Computed property to merge customers with their latest quotes
const customersWithPrices = computed(() => {
  return customersList.value.customers.map(customer => ({
    ...customer,
    bestPrice: customerQuotes.value[customer.id]?.best_price || null,
    quote: customerQuotes.value[customer.id] || null
  }));
});

const fetchCustomers = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    // Fetch customers and UWM config in parallel
    const [customersData, config] = await Promise.all([
      customerService.listCustomers(),
      pricingService.getConfig()
    ]);
    customersList.value = customersData;
    uwmConfig.value = config;
  } catch (err) {
    error.value = typeof err === 'string' ? err : 'Failed to load customers. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

const handleQuoteRequest = async (customer) => {
  loadingQuotes.value[customer.id] = true;
  error.value = null;
  successMessage.value = null;

  try {
    // Use UWM config from server
    if (!uwmConfig.value) {
      throw 'UWM config not loaded';
    }
    const quoteData = { ...uwmConfig.value };

    const quote = await pricingService.getQuote(customer.id, quoteData);

    // Store the quote for this customer
    customerQuotes.value[customer.id] = quote;

    successMessage.value = `Successfully retrieved pricing quote for ${customer.name}`;

    // Scroll to top to show success message
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (err) {
    error.value = typeof err === 'string' ? err : 'Failed to request pricing quote. Please try again.';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } finally {
    loadingQuotes.value[customer.id] = false;
  }
};

const handlePriceClick = (customer) => {
  if (customer.quote) {
    selectedQuote.value = customer.quote;
    showModal.value = true;
  }
};

const closeModal = () => {
  showModal.value = false;
  selectedQuote.value = null;
};

onMounted(() => {
  fetchCustomers();
});
</script>
