<template>
  <div class="card">
    <div class="card-header d-flex flex-wrap align-items-center justify-content-between gap-3">
      <div class="d-flex flex-wrap align-items-center gap-3">
        <div class="d-flex align-items-center gap-2">
          <span>Show</span>
          <select class="form-select form-select-sm w-auto" v-model="selectedShow">
            <option value="10">10</option>
            <option value="15">15</option>
            <option value="20">20</option>
          </select>
        </div>

        <div class="icon-field">
          <input type="text" class="form-control form-control-sm w-auto" v-model="searchText" placeholder="Search">
          <span class="icon">
            <iconify-icon icon="ion:search-outline"></iconify-icon>
          </span>
        </div>
      </div>

      <div class="d-flex flex-wrap align-items-center gap-3">
        <select class="form-select form-select-sm w-auto" v-model="selectedStatus">
          <option value="">Status</option>
          <option value="Paid">Paid</option>
          <option value="Pending">Pending</option>
        </select>

        <router-link to="/invoice-add" class="btn btn-sm btn-primary-600">
          <i class="ri-add-line"></i> Create Invoice
        </router-link>
      </div>
    </div>

    <!-- Table -->
    <div class="card-body">
      <table class="table bordered-table mb-0">
        <thead>
          <tr>
            <th scope="col">
              <div class="form-check style-check d-flex align-items-center">
                <input class="form-check-input" type="checkbox" v-model="selectAll" @change="toggleSelectAll">
                <label class="form-check-label">S.L</label>
              </div>
            </th>
            <th scope="col">Invoice</th>
            <th scope="col">Name</th>
            <th scope="col">Issued Date</th>
            <th scope="col">Amount</th>
            <th scope="col">Status</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(invoice, index) in filteredInvoices" :key="invoice.id">
            <td>
              <div class="form-check style-check d-flex align-items-center">
                <input class="form-check-input" type="checkbox" v-model="selectedIds" :value="invoice.id">
                <label class="form-check-label">{{ invoice.id }}</label>
              </div>
            </td>
            <td>
              <a href="javascript:void(0)" class="text-primary-600">{{ invoice.invoice }}</a>
            </td>
            <td>
              <div class="d-flex align-items-center">
                <img :src="invoice.image" alt="" class="flex-shrink-0 me-12 radius-8" width="40" height="40">
                <h6 class="text-md mb-0 fw-medium flex-grow-1">{{ invoice.name }}</h6>
              </div>
            </td>
            <td>{{ invoice.issuedDate }}</td>
            <td>${{ invoice.amount }}.00 </td>
            <td>
              <span :class="statusClasses(invoice.status)" class="px-24 py-4 rounded-pill fw-medium text-sm">
                {{ invoice.status }}
              </span>
            </td>
            <td class="d-flex gap-2">
              <a href="#"
                class="w-32-px h-32-px bg-primary-light text-primary-600 rounded-circle d-inline-flex align-items-center justify-content-center">
                <iconify-icon icon="iconamoon:eye-light"></iconify-icon>
              </a>
              <a href="#"
                class="w-32-px h-32-px bg-success-focus text-success-main rounded-circle d-inline-flex align-items-center justify-content-center">
                <iconify-icon icon="lucide:edit"></iconify-icon>
              </a>
              <a href="#"
                class="w-32-px h-32-px bg-danger-focus text-danger-main rounded-circle d-inline-flex align-items-center justify-content-center">
                <iconify-icon icon="mingcute:delete-2-line"></iconify-icon>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Pagination -->
      <Pagination :currentPage="currentPage" :totalPages="totalPages" :startIndex="startIndex" :endIndex="endIndex"
        :totalItems="totalEntries" @page-changed="changePage" />
    </div>
  </div>
</template>

<script>
import user1 from '@/assets/images/user-list/user-list1.png'
import user2 from '@/assets/images/user-list/user-list2.png'
import user3 from '@/assets/images/user-list/user-list3.png'
import user4 from '@/assets/images/user-list/user-list4.png'
import user5 from '@/assets/images/user-list/user-list5.png'
import user6 from '@/assets/images/user-list/user-list6.png'
import user7 from '@/assets/images/user-list/user-list7.png'
import user8 from '@/assets/images/user-list/user-list8.png'
import user9 from '@/assets/images/user-list/user-list9.png'
import user10 from '@/assets/images/user-list/user-list10.png'

import Pagination from '@/components/pagination/index.vue'

export default {
  components: { Pagination },
  data() {
    return {
      selectedShow: 10,
      searchText: '',
      selectedStatus: '',
      selectAll: false,
      selectedIds: [],
      currentPage: 1,
      invoices: [
        { id: '01', invoice: '#526534', name: 'Kathryn Murphy', issuedDate: '25 Jan 2024', amount: '200', status: 'Paid', image: user1 },
        { id: '02', invoice: '#696589', name: 'Annette Black', issuedDate: '25 Jan 2024', amount: '200', status: 'Paid', image: user2 },
        { id: '03', invoice: '#256584', name: 'Ronald Richards', issuedDate: '10 Feb 2024', amount: '200', status: 'Paid', image: user3 },
        { id: '04', invoice: '#526587', name: 'Eleanor Pena', issuedDate: '10 Feb 2024', amount: '150', status: 'Paid', image: user4 },
        { id: '05', invoice: '#105986', name: 'Leslie Alexander', issuedDate: '15 March 2024', amount: '150', status: 'Pending', image: user5 },
        { id: '06', invoice: '#526589', name: 'Albert Flores', issuedDate: '15 March 2024', amount: '150', status: 'Paid', image: user6 },
        { id: '07', invoice: '#526520', name: 'Jacob Jones', issuedDate: '27 April 2024', amount: '250', status: 'Paid', image: user7 },
        { id: '08', invoice: '#256584', name: 'Jerome Bell', issuedDate: '27 April 2024', amount: '250', status: 'Pending', image: user8 },
        { id: '09', invoice: '#200257', name: 'Marvin McKinney', issuedDate: '30 April 2024', amount: '250', status: 'Paid', image: user9 },
        { id: '10', invoice: '#526525', name: 'Cameron Williamson', issuedDate: '30 April 2024', amount: '250', status: 'Paid', image: user10 },
        { id: '11', invoice: '#526534', name: 'Kathryn Murphy', issuedDate: '25 Jan 2024', amount: '200', status: 'Paid', image: user1 },
        { id: '12', invoice: '#696589', name: 'Annette Black', issuedDate: '25 Jan 2024', amount: '200', status: 'Paid', image: user2 },


      ]
    };
  },
  computed: {
    entriesPerPage() {
      return Number(this.selectedShow);
    },
    filteredData() {
      let result = this.invoices;

      if (this.searchText) {
        const search = this.searchText.toLowerCase();
        result = result.filter(inv =>
          inv.name.toLowerCase().includes(search) ||
          inv.invoice.toLowerCase().includes(search)
        );
      }

      if (this.selectedStatus) {
        result = result.filter(inv => inv.status === this.selectedStatus);
      }

      return result;
    },
    totalEntries() {
      return this.filteredData.length;
    },
    totalPages() {
      return Math.ceil(this.totalEntries / this.entriesPerPage);
    },
    startIndex() {
      return (this.currentPage - 1) * this.entriesPerPage;
    },
    endIndex() {
      return Math.min(this.startIndex + this.entriesPerPage, this.totalEntries);
    },
    filteredInvoices() {
      return this.filteredData.slice(this.startIndex, this.endIndex);
    }
  },
  watch: {
    selectedShow() {
      this.currentPage = 1;
    },
    searchText() {
      this.currentPage = 1;
    },
    selectedStatus() {
      this.currentPage = 1;
    }
  },
  methods: {
    toggleSelectAll() {
      if (this.selectAll) {
        this.selectedIds = this.filteredInvoices.map(inv => inv.id);
      } else {
        this.selectedIds = [];
      }
    },
    statusClasses(status) {
      return {
        'bg-success-focus text-success-main': status === 'Paid',
        'bg-warning-focus text-warning-main': status === 'Pending'
      };
    },
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    changePage(page) {
      this.goToPage(page);
    }
  }
};
</script>
