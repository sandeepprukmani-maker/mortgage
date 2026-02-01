<template>
    <div class="col-xxl-3">
      <div class="card h-100">
        <div class="card-body">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Transactions</h6>
            <div class="">
              <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option>This Month</option>
                <option>Last Month</option>
              </select>
            </div>
          </div>
  
          <div class="mt-32">
            <div v-for="(transaction, index) in transactions" :key="index" class="d-flex align-items-center justify-content-between gap-3 " :class="{'mb-32': index !== transactions.length - 1, 'mb-0': index === transactions.length -1 }">
              <div class="d-flex align-items-center gap-2">
                <img :src="transaction.image" alt="" class="w-40-px h-40-px radius-8 flex-shrink-0">
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0 fw-normal">{{ transaction.method }}</h6>
                  <span class="text-sm text-secondary-light fw-normal">{{ transaction.description }}</span>
                </div>
              </div>
              <span :class="transaction.amountClass" class="text-md fw-medium">{{ transaction.amount }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import payment1 from "@/assets/images/payment/payment1.png"
  import payment2 from "@/assets/images/payment/payment2.png"
  import payment3 from "@/assets/images/payment/payment3.png"
  import payment4 from "@/assets/images/payment/payment4.png"
  export default {
    name: "Transactions",
    data() {
      return {
        transactions: [
          {
            image: payment1,
            method: "Paytm",
            description: "Starbucks",
            amount: "-$20",
            amountClass: "text-danger text-md",
          },
          {
            image: payment2,
            method: "PayPal",
            description: "Client Payment",
            amount: "+$800",
            amountClass: "text-success-main text-md",
          },
          {
            image: payment3,
            method: "Stripe",
            description: "Ordered iPhone 14",
            amount: "-$300",
            amountClass: "text-danger-main text-md",
          },
          {
            image: payment4,
            method: "Razorpay",
            description: "Refund",
            amount: "+$500",
            amountClass: "text-success-main text-md",
          },
          {
            image: payment1,
            method: "Paytm",
            description: "Starbucks",
            amount: "-$1500",
            amountClass: "text-danger-main text-md",
          },
          {
            image: payment3,
            method: "Stripe",
            description: "Ordered iPhone 14",
            amount: "+$800",
            amountClass: "text-success-main text-md",
          },
        ],
      };
    },
  };
  </script>
  