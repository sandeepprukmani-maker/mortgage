<template>
    <div class="col-md-6">
      <div class="card radius-16">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Payment History</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body">
          <div
            v-for="(item, index) in payments"
            :key="index"
            :class="[
              'd-flex align-items-center justify-content-between',
              'pb-10 mb-10',
              index !== payments.length - 1 ? 'border-bottom border-neutral-200' : ''
            ]"
            
          >
            <div>
              <h6 class="text-md mb-0">{{ item.title }}</h6>
              <span class="text-xs text-secondary-light fw-medium">{{ item.date }}</span>
            </div>
            <div>
              <h6 class="text-sm mb-1">{{ item.amount }}</h6>
              <span
                :class="[
                  'text-xs fw-medium rounded-pill px-3',
                  statusClasses[item.status].text,
                  statusClasses[item.status].bg
                ]"
              >
                {{ item.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "PaymentHistory",
    data() {
      return {
        payments: [
          {
            title: "Digital Assets",
            date: "18 Nov 2024",
            amount: "$450.00",
            status: "Paid"
          },
          {
            title: "Electricity",
            date: "18 Nov 2024",
            amount: "$150.00",
            status: "Due"
          },
          {
            title: "Internet Bill",
            date: "18 Nov 2024",
            amount: "$450.00",
            status: "Cancel"
          },
          {
            title: "House rent",
            date: "18 Nov 2024",
            amount: "$450.00",
            status: "Paid"
          },
          {
            title: "Office rent",
            date: "18 Nov 2024",
            amount: "$450.00",
            status: "Paid"
          }
        ],
        statusClasses: {
          Paid: {
            text: "text-success-600",
            bg: "bg-success-100"
          },
          Due: {
            text: "text-warning-600",
            bg: "bg-warning-100"
          },
          Cancel: {
            text: "text-danger-600",
            bg: "bg-danger-100"
          }
        }
      };
    }
  };
  </script>
  