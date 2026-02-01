<template>
    <div class="card h-100 p-0 radius-12">
        <!-- Header -->
        <div
            class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
            <div class="d-flex align-items-center flex-wrap gap-3">
                <span class="text-md fw-medium text-secondary-light mb-0">Show</span>
                <select class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px" v-model="itemsToShow">
                    <option v-for="n in 10" :key="n">{{ n }}</option>
                </select>
                <form class="navbar-search" @submit.prevent>
                    <input type="text" class="bg-base h-40-px w-auto" name="search" placeholder="Search"
                        v-model="searchQuery" />
                    <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
                </form>
            </div>

            <button type="button"
                class="btn btn-primary text-sm btn-sm px-12 py-12 radius-8 d-flex align-items-center gap-2"
                data-bs-toggle="modal" data-bs-target="#exampleModal">
                <iconify-icon icon="ic:baseline-plus" class="icon text-xl line-height-1"></iconify-icon>
                Add Currency
            </button>
        </div>

        <!-- Table -->
        <div class="card-body p-24">
            <div class="table-responsive scroll-sm">
                <table class="table bordered-table sm-table mb-0">
                    <thead>
                        <tr>
                            <th>S.L</th>
                            <th class="text-center">Name</th>
                            <th class="text-center">Symbol</th>
                            <th class="text-center">Code</th>
                            <th class="text-center">Is Cryptocurrency</th>
                            <th class="text-center">Status</th>
                            <th class="text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(currency, index) in paginatedCurrencies" :key="index">
                            <td>{{ ('0' + (startIndex + index + 1)).slice(-2) }}</td>
                            <td class="text-center">{{ currency.name }}</td>
                            <td class="text-center">{{ currency.symbol }}</td>
                            <td class="text-center">{{ currency.code }}</td>
                            <td class="text-center">{{ currency.isCrypto ? 'Yes' : 'No' }}</td>
                            <td>
                                <div
                                    class="form-switch switch-primary d-flex align-items-center justify-content-center">
                                    <input class="form-check-input" type="checkbox" v-model="currency.status" />
                                </div>
                            </td>
                            <td class="text-center">
                                <div class="d-flex align-items-center gap-10 justify-content-center">
                                    <button type="button"
                                        class="bg-success-100 text-success-600 bg-hover-success-200 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle"
                                        data-bs-toggle="modal" data-bs-target="#exampleModalEdit"
                                        @click="loadEditForm(currency, index)">
                                        <iconify-icon icon="lucide:edit" class="menu-icon"></iconify-icon>
                                    </button>
                                    <button type="button"
                                        class="remove-item-button bg-danger-focus bg-hover-danger-200 text-danger-600 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle"
                                        @click="removeCurrency(index)">
                                        <iconify-icon icon="fluent:delete-24-regular" class="menu-icon"></iconify-icon>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <Pagination :currentPage="currentPage" :totalPages="totalPages" :startIndex="startIndex"
                :endIndex="endIndex" :totalItems="filteredCurrencies.length" @page-changed="changePage" />
        </div>

        <!-- Add Currency Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content radius-16 bg-base">
                    <div class="modal-header py-16 px-24 border-bottom">
                        <h1 class="modal-title fs-5">Add New Currency</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body p-24">
                        <form @submit.prevent="submitAddForm" @reset="resetAddForm">
                            <div class="row">
                                <div class="col-6 mb-20">
                                    <label class="form-label fw-semibold text-primary-light text-sm mb-8">Name</label>
                                    <input type="text" class="form-control radius-8" v-model="addForm.name"
                                        placeholder="Enter Name" />
                                </div>
                                <div class="col-6 mb-20">
                                    <label
                                        class="form-label fw-semibold text-primary-light text-sm mb-8">Country</label>
                                    <select class="form-control radius-8 form-select" v-model="addForm.symbol">
                                        <option value="" disabled selected>Select symbol</option>
                                        <option>$</option>
                                        <option>৳</option>
                                        <option>₹</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label fw-semibold text-primary-light text-sm mb-8">Code</label>
                                    <select class="form-control radius-8 form-select" v-model="addForm.code">
                                        <option value="" disabled selected>Select Code</option>
                                        <option>15</option>
                                        <option>26</option>
                                        <option>64</option>
                                        <option>25</option>
                                        <option>92</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label fw-semibold text-primary-light text-sm mb-8">Is
                                        Cryptocurrency</label>
                                    <select class="form-control radius-8 form-select" v-model="addForm.isCrypto">
                                        <option value="" disabled selected>Select</option>
                                        <option :value="false">No</option>
                                        <option :value="true">Yes</option>
                                    </select>
                                </div>
                                <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
                                    <button type="reset"
                                        class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-40 py-11 radius-8">Reset</button>
                                    <button type="submit"
                                        class="btn btn-primary border border-primary-600 text-md px-24 py-12 radius-8">Save
                                        Change</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Edit Currency Modal -->
        <div class="modal fade" id="exampleModalEdit" tabindex="-1" aria-labelledby="exampleModalEditLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content radius-16 bg-base">
                    <div class="modal-header py-16 px-24 border-bottom">
                        <h1 class="modal-title fs-5">Edit Currency</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body p-24">
                        <form @submit.prevent="submitEditForm" @reset="resetEditForm">
                            <div class="row">
                                <div class="col-6 mb-20">
                                    <label class="form-label fw-semibold text-primary-light text-sm mb-8">Name</label>
                                    <input type="text" class="form-control radius-8" v-model="editForm.name" />
                                </div>
                                <div class="col-6 mb-20">
                                    <label
                                        class="form-label fw-semibold text-primary-light text-sm mb-8">Country</label>
                                    <select class="form-control radius-8 form-select" v-model="editForm.symbol">
                                        <option value="" disabled selected>Select symbol</option>
                                        <option>$</option>
                                        <option>৳</option>
                                        <option>₹</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label fw-semibold text-primary-light text-sm mb-8">Code</label>
                                    <select class="form-control radius-8 form-select" v-model="editForm.code">
                                        <option value="" disabled selected>Select Code</option>
                                        <option>15</option>
                                        <option>26</option>
                                        <option>64</option>
                                        <option>25</option>
                                        <option>92</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label fw-semibold text-primary-light text-sm mb-8">Is
                                        Cryptocurrency</label>
                                    <select class="form-control radius-8 form-select" v-model="editForm.isCrypto">
                                        <option value="" disabled selected>Select</option>
                                        <option :value="false">No</option>
                                        <option :value="true">Yes</option>
                                    </select>
                                </div>
                                <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
                                    <button type="reset"
                                        class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-50 py-11 radius-8">Cancel</button>
                                    <button type="submit"
                                        class="btn btn-primary border border-primary-600 text-md px-50 py-12 radius-8">Update</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Pagination from '@/components/pagination/index.vue'

export default {
    name: 'CurrencyTable',
    components: { Pagination },
    data() {
        return {
            currentPage: 1,
            itemsToShow: 10,
            searchQuery: '',
            currencies: [
                { name: 'Dollars(Default)', symbol: '$', code: 'USD', isCrypto: false, status: true },
                { name: 'Taka', symbol: '৳', code: 'BDT', isCrypto: false, status: false },
                { name: 'Rupee', symbol: '₹', code: 'INR', isCrypto: false, status: false },
                { name: 'Dollars', symbol: '$', code: 'USD', isCrypto: false, status: false },
                { name: 'Taka', symbol: '৳', code: 'BDT', isCrypto: false, status: false },
                { name: 'Dollars', symbol: '$', code: 'USD', isCrypto: false, status: false },
                { name: 'Rupee', symbol: '₹', code: 'INR', isCrypto: false, status: false },
                { name: 'Dollars', symbol: '$', code: 'USD', isCrypto: false, status: false },
                { name: 'Taka', symbol: '৳', code: 'BDT', isCrypto: false, status: false },
                { name: 'Rupee', symbol: '₹', code: 'INR', isCrypto: false, status: false },
                { name: 'Dollars', symbol: '$', code: 'USD', isCrypto: false, status: false },
            ],
            addForm: { name: '', symbol: '', code: '', isCrypto: '' },
            editForm: { name: '', symbol: '', code: '', isCrypto: '' },
            editIndex: null
        };
    },
    computed: {
        filteredCurrencies() {
            const query = this.searchQuery.toLowerCase();
            return this.currencies.filter(c => c.name.toLowerCase().includes(query) || c.code.toLowerCase().includes(query));
        },
        totalPages() {
            return Math.ceil(this.filteredCurrencies.length / this.itemsToShow);
        },
        startIndex() {
            return (this.currentPage - 1) * this.itemsToShow;
        },
        endIndex() {
            return this.startIndex + this.itemsToShow;
        },
        paginatedCurrencies() {
            return this.filteredCurrencies.slice(this.startIndex, this.endIndex);
        }
    },
    methods: {
        changePage(page) {
            this.currentPage = page;
        },
        submitAddForm() {
            this.currencies.push({ ...this.addForm, status: true });
            this.resetAddForm();
        },
        resetAddForm() {
            this.addForm = { name: '', symbol: '', code: '', isCrypto: '' };
        },
        loadEditForm(currency, index) {
            this.editIndex = index + this.startIndex;
            this.editForm = { ...currency };
        },
        submitEditForm() {
            this.currencies.splice(this.editIndex, 1, { ...this.editForm, status: this.currencies[this.editIndex].status });
        },
        resetEditForm() {
            this.editForm = { name: '', symbol: '', code: '', isCrypto: '' };
        },
        removeCurrency(index) {
            this.currencies.splice(this.startIndex + index, 1);
        }
    }
};
</script>