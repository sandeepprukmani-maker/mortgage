<template>
    <div class="card basic-data-table">
        <div class="card-header">
            <h5 class="card-title mb-0">Default Datatables</h5>
        </div>
        <div class="card">
            <div class="card-header d-flex flex-wrap align-items-center justify-content-between gap-3"
                style="border-bottom: none; padding-bottom: 0px;">

                <div class="d-flex flex-wrap align-items-center gap-3">
                    <div class="d-flex align-items-center gap-2">
                        <select class="form-select form-select-lr w-auto rounded-3 me-10" v-model="selectedShow"
                            style="border-radius: 10px; height: 2.4rem;">
                            <option value="10">10</option>
                            <option value="15">15</option>
                            <option value="20">20</option>
                        </select>
                        <span>entries per page</span>
                    </div>
                </div>

                <div class="icon-field d-flex align-items-center" style="padding-bottom: 5px;">
                    <span class="me-13">Search:</span>
                    <div class="position-relative" style="width: 100%; max-width: 226px;">
                        <input type="text" class="form-control form-control-sm w-100 px-3 pe-5" v-model="searchText"
                            style="border-radius: 10px; height: 2.5rem;" />
                        <span class="icon position-absolute end-0 top-50 translate-middle-y me-3 text-muted"
                            style="pointer-events: none;"></span>
                    </div>
                </div>
            </div>

            <!-- Table -->
            <div class="card-body">
                <table class="table bordered-table mb-0">
                    <thead>
                        <tr>
                            <th scope="col" @click="sortBy('id')" class="sortable">
                                <div class="form-check style-check d-flex align-items-center">
                                    <input class="form-check-input" type="checkbox" v-model="selectAll"
                                        @change="toggleSelectAll">
                                    <label class="form-check-label d-flex align-items-center">
                                        S.L
                                        <span v-if="sortKey === 'id'">
                                            <iconify-icon
                                                :icon="sortAsc ? 'mdi:arrow-up' : 'mdi:arrow-down'"></iconify-icon>
                                        </span>
                                    </label>
                                </div>
                            </th>
                            <th scope="col" @click="sortBy('invoice')" class="sortable">
                                Invoice
                                <span v-if="sortKey === 'invoice'">
                                    <iconify-icon :icon="sortAsc ? 'mdi:arrow-up' : 'mdi:arrow-down'"></iconify-icon>
                                </span>
                            </th>
                            <th scope="col" @click="sortBy('name')" class="sortable">
                                Name
                                <span v-if="sortKey === 'name'">
                                    <iconify-icon :icon="sortAsc ? 'mdi:arrow-up' : 'mdi:arrow-down'"></iconify-icon>
                                </span>
                            </th>
                            <th scope="col" @click="sortBy('issuedDate')" class="sortable">
                                Issued Date
                                <span v-if="sortKey === 'issuedDate'">
                                    <iconify-icon :icon="sortAsc ? 'mdi:arrow-up' : 'mdi:arrow-down'"></iconify-icon>
                                </span>
                            </th>
                            <th scope="col" @click="sortBy('amount')" class="sortable">
                                Amount
                                <span v-if="sortKey === 'amount'">
                                    <iconify-icon :icon="sortAsc ? 'mdi:arrow-up' : 'mdi:arrow-down'"></iconify-icon>
                                </span>
                            </th>
                            <th scope="col" @click="sortBy('status')" class="sortable">
                                Status
                                <span v-if="sortKey === 'status'">
                                    <iconify-icon :icon="sortAsc ? 'mdi:arrow-up' : 'mdi:arrow-down'"></iconify-icon>
                                </span>
                            </th>
                            <th scope="col">
                                Action
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(invoice, index) in paginatedInvoices" :key="invoice.id">
                            <td>
                                <div class="form-check style-check d-flex align-items-center">
                                    <input class="form-check-input" type="checkbox" v-model="selectedIds"
                                        :value="invoice.id">
                                    <label class="form-check-label">{{ invoice.id }}</label>
                                </div>
                            </td>
                            <td>
                                <a href="javascript:void(0)" class="text-primary-600">{{ invoice.invoice }}</a>
                            </td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <img :src="invoice.image" alt="" class="flex-shrink-0 me-12 radius-8" width="40"
                                        height="40">
                                    <h6 class="text-md mb-0 fw-medium flex-grow-1">{{ invoice.name }}</h6>
                                </div>
                            </td>
                            <td>{{ invoice.issuedDate }}</td>
                            <td>${{ invoice.amount }}.00 </td>
                            <td>
                                <span :class="statusClasses(invoice.status)"
                                    class="px-24 py-4 rounded-pill fw-medium text-sm">
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

                <!-- pagination -->
                <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mt-24">
                    <span>
                        Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ totalEntries }} entries
                    </span>
                    <ul class="pagination d-flex flex-wrap align-items-center gap-2 justify-content-center">
                        <li class="page-item">
                            <a class="page-link text-secondary-light fw-medium radius-4 border-0 px-10 py-10 d-flex align-items-center justify-content-center h-32-px w-32-px bg-base"
                                href="javascript:void(0)" @click="goToPage(currentPage - 1)"
                                :class="{ disabled: currentPage === 1 }">
                                <iconify-icon icon="ep:d-arrow-left" class="text-xl"></iconify-icon>
                            </a>
                        </li>
                        <li class="page-item">
                            <a class="page-link text-secondary-light fw-medium radius-4 border-0 px-10 py-10 d-flex align-items-center justify-content-center h-32-px w-32-px bg-base"
                                href="javascript:void(0)" @click="goToPage(currentPage - 1)"
                                :class="{ disabled: currentPage === 1 }">
                                <iconify-icon icon="ep:arrow-left"></iconify-icon>
                            </a>
                        </li>

                        <li v-for="page in totalPages" :key="page" class="page-item">
                            <a href="javascript:void(0)"
                                class="page-link fw-medium radius-4 border-0 px-10 py-10 d-flex align-items-center justify-content-center h-32-px w-32-px"
                                :class="{
                                    'bg-primary-600 text-white': currentPage === page,
                                    'bg-primary-50 text-secondary-light': currentPage !== page
                                }" @click="goToPage(page)">
                                {{ page }}
                            </a>
                        </li>

                        <li class="page-item">
                            <a class="page-link text-secondary-light fw-medium radius-4 border-0 px-10 py-10 d-flex align-items-center justify-content-center h-32-px w-32-px bg-base"
                                href="javascript:void(0)" @click="goToPage(currentPage + 1)"
                                :class="{ disabled: currentPage === totalPages }">
                                <iconify-icon icon="ep:arrow-right" class="text-xl"></iconify-icon>
                            </a>
                        </li>

                        <li class="page-item">
                            <a class="page-link text-secondary-light fw-medium radius-4 border-0 px-10 py-10 d-flex align-items-center justify-content-center h-32-px w-32-px bg-base"
                                href="javascript:void(0)" @click="goToPage(currentPage + 1)"
                                :class="{ disabled: currentPage === totalPages }">
                                <iconify-icon icon="ep:d-arrow-right" class="text-xl"></iconify-icon>
                            </a>
                        </li>
                    </ul>
                </div>

            </div>
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

export default {
    data() {
        return {
            selectedShow: 10,
            searchText: '',
            selectedStatus: '',
            selectAll: false,
            selectedIds: [],
            currentPage: 1,
            sortKey: '',
            sortAsc: true,
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
                { id: '13', invoice: '#256584', name: 'Ronald Richards', issuedDate: '10 Feb 2024', amount: '200', status: 'Paid', image: user3 },
                { id: '14', invoice: '#526587', name: 'Eleanor Pena', issuedDate: '10 Feb 2024', amount: '150', status: 'Paid', image: user4 },
                { id: '15', invoice: '#105986', name: 'Leslie Alexander', issuedDate: '15 March 2024', amount: '150', status: 'Pending', image: user5 },
                { id: '16', invoice: '#526589', name: 'Albert Flores', issuedDate: '15 March 2024', amount: '150', status: 'Paid', image: user6 },
                { id: '17', invoice: '#526520', name: 'Jacob Jones', issuedDate: '27 April 2024', amount: '250', status: 'Paid', image: user7 },
                { id: '18', invoice: '#256584', name: 'Jerome Bell', issuedDate: '27 April 2024', amount: '250', status: 'Pending', image: user8 },
                { id: '19', invoice: '#200257', name: 'Marvin McKinney', issuedDate: '30 April 2024', amount: '250', status: 'Paid', image: user9 },
                { id: '20', invoice: '#526525', name: 'Cameron Williamson', issuedDate: '30 April 2024', amount: '250', status: 'Paid', image: user10 },
            ]
        };
    },
    computed: {
        entriesPerPage() {
            return Number(this.selectedShow);
        },
        filteredInvoices() {
            let result = [...this.invoices];

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

            // Sorting
            if (this.sortKey) {
                result.sort((a, b) => {
                    let valA = a[this.sortKey];
                    let valB = b[this.sortKey];

                    if (this.sortKey === 'issuedDate') {
                        valA = new Date(valA);
                        valB = new Date(valB);
                    } else if (this.sortKey === 'amount') {
                        valA = Number(valA);
                        valB = Number(valB);
                    } else {
                        valA = String(valA).toLowerCase();
                        valB = String(valB).toLowerCase();
                    }

                    return this.sortAsc ? valA > valB ? 1 : -1 : valA < valB ? 1 : -1;
                });
            }

            return result;
        },
        paginatedInvoices() {
            return this.filteredInvoices.slice(this.startIndex, this.endIndex);
        },
        totalEntries() {
            return this.filteredInvoices.length;
        },
        totalPages() {
            return Math.ceil(this.totalEntries / this.entriesPerPage);
        },
        startIndex() {
            return (this.currentPage - 1) * this.entriesPerPage;
        },
        endIndex() {
            return Math.min(this.startIndex + this.entriesPerPage, this.totalEntries);
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
        sortBy(key) {
            if (this.sortKey === key) {
                this.sortAsc = !this.sortAsc;
            } else {
                this.sortKey = key;
                this.sortAsc = true;
            }
        },
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
        }
    }
};
</script>

<style>
.sortable {
    cursor: pointer;
    user-select: none;
}

.sortable:hover {
    text-decoration: underline;
}
</style>
