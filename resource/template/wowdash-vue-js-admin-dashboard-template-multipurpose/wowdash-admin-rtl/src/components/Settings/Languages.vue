<template>
    <div class="card h-100 p-0 radius-12">
        <div
            class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
            <div class="d-flex align-items-center flex-wrap gap-3">
                <span class="text-md fw-medium text-secondary-light mb-0">Show</span>
                <select class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px" v-model="itemsToShow">
                    <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
                </select>

                <form class="navbar-search">
                    <input type="text" class="bg-base h-40-px w-auto" name="search" placeholder="Search"
                        v-model="searchQuery" />
                    <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
                </form>
            </div>

            <button type="button"
                class="btn btn-primary text-sm btn-sm px-12 py-12 radius-8 d-flex align-items-center gap-2"
                data-bs-toggle="modal" data-bs-target="#exampleModal">
                <iconify-icon icon="ic:baseline-plus" class="icon text-xl line-height-1"></iconify-icon>
                Add Languages
            </button>
        </div>

        <div class="card-body p-24">
            <div class="table-responsive scroll-sm">
                <table class="table bordered-table sm-table mb-0">
                    <thead>
                        <tr>
                            <th scope="col">S.L</th>
                            <th scope="col" class="text-center">Name</th>
                            <th scope="col" class="text-center">Status</th>
                            <th scope="col" class="text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(language, index) in paginatedLanguages" :key="startIndex + index">
                            <td>{{ startIndex + index + 1 }}</td>
                            <td class="text-center">{{ language.name }}</td>
                            <td>
                                <div
                                    class="form-switch switch-primary d-flex align-items-center justify-content-center">
                                    <input class="form-check-input" type="checkbox" role="switch"
                                        v-model="language.status" />
                                </div>
                            </td>
                            <td class="text-center">
                                <div class="d-flex align-items-center gap-10 justify-content-center">
                                    <button type="button"
                                        class="bg-success-100 text-success-600 bg-hover-success-200 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle"
                                        data-bs-toggle="modal" data-bs-target="#exampleModalEdit"
                                        @click="loadEditForm(language, index)">
                                        <iconify-icon icon="lucide:edit" class="menu-icon"></iconify-icon>
                                    </button>
                                    <button type="button"
                                        class="remove-item-button bg-danger-focus bg-hover-danger-200 text-danger-600 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle"
                                        @click="removeLanguage(index)">
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
                :endIndex="endIndex" :totalItems="filteredLanguages.length" @page-changed="changePage" />
        </div>
    </div>
    <!-- ADD LANGUAGE MODAL -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content radius-16 bg-base">
                <div class="modal-header py-16 px-24 border-bottom">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Add New Language</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-24">
                    <form @submit.prevent="addLanguage">
                        <div class="row">
                            <div class="col-6 mb-20">
                                <label for="name" class="form-label text-sm mb-8">Language Name</label>
                                <input type="text" class="form-control radius-8" id="name" placeholder="Enter Name"
                                    v-model="newLanguage.name" />
                            </div>
                            <div class="col-6 mb-20">
                                <label for="status" class="form-label text-sm mb-8">Status</label>
                                <select class="form-control radius-8 form-select" id="status"
                                    v-model="newLanguage.status">
                                    <option disabled value="">Select One</option>
                                    <option :value="true">ON</option>
                                    <option :value="false">OFF</option>
                                </select>
                            </div>
                            <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
                                <button type="reset"
                                    class="border border-danger-600 text-danger-600 px-50 py-11 radius-8"
                                    @click="resetNewLanguage">Reset</button>
                                <button type="submit" class="btn btn-primary px-50 py-12 radius-8">Save Change</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- EDIT LANGUAGE MODAL -->
    <div class="modal fade" id="exampleModalEdit" tabindex="-1" aria-labelledby="exampleModalEditLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content radius-16 bg-base">
                <div class="modal-header py-16 px-24 border-bottom">
                    <h1 class="modal-title fs-5" id="exampleModalEditLabel">Edit Language</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-24">
                    <form @submit.prevent="updateLanguage">
                        <div class="row">
                            <div class="col-6 mb-20">
                                <label for="editname" class="form-label text-sm mb-8">Language Name</label>
                                <input type="text" class="form-control radius-8" id="editname" placeholder="Enter Name"
                                    v-model="editForm.name" />
                            </div>
                            <div class="col-6 mb-20">
                                <label for="editstatus" class="form-label text-sm mb-8">Status</label>
                                <select class="form-control radius-8 form-select" id="editstatus"
                                    v-model="editForm.status">
                                    <option disabled value="">Select One</option>
                                    <option :value="true">ON</option>
                                    <option :value="false">OFF</option>
                                </select>
                            </div>
                            <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
                                <button type="reset"
                                    class="border border-danger-600 text-danger-600 px-50 py-11 radius-8"
                                    data-bs-dismiss="modal">Cancel</button>
                                <button type="submit" class="btn btn-primary px-50 py-12 radius-8">Update</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Pagination from "@/components/pagination/index.vue";

export default {
    components: { Pagination },
    data() {
        return {
            searchQuery: "",
            itemsToShow: 10,
            currentPage: 1,
            newLanguage: {
                name: "",
                status: "",
            },
            editForm: {
                name: "",
                status: "",
                index: null,
            },
            languages: [
                { name: "English(Default)", status: true },
                { name: "Bangla", status: false },
                { name: "Bangla", status: false },
                { name: "Bangla", status: false },
                { name: "German", status: false },
                { name: "German", status: false },
                { name: "German", status: false },
                { name: "Hindi", status: false },
                { name: "Hindi", status: false },
                { name: "Bangla", status: false },
                { name: "German", status: false },
            ],
        };
    },
    computed: {
        filteredLanguages() {
            const q = this.searchQuery.toLowerCase();
            return this.languages.filter((lang) =>
                lang.name.toLowerCase().includes(q)
            );
        },
        totalPages() {
            return Math.ceil(this.filteredLanguages.length / this.itemsToShow);
        },
        startIndex() {
            return (this.currentPage - 1) * this.itemsToShow;
        },
        endIndex() {
            return this.startIndex + this.itemsToShow;
        },
        paginatedLanguages() {
            return this.filteredLanguages.slice(this.startIndex, this.endIndex);
        },
    },
    methods: {
        changePage(page) {
            this.currentPage = page;
        },
        resetNewLanguage() {
            this.newLanguage = { name: "", status: "" };
        },
        addLanguage() {
            if (this.newLanguage.name && this.newLanguage.status !== "") {
                this.languages.push({ ...this.newLanguage });
                this.resetNewLanguage();
                // Close modal programmatically
                const modal = bootstrap.Modal.getInstance(document.getElementById("exampleModal"));
                modal.hide();
            }
        },
        loadEditForm(language, index) {
            this.editForm = {
                name: language.name,
                status: language.status,
                index: this.startIndex + index,
            };
        },
        updateLanguage() {
            if (this.editForm.name && this.editForm.status !== "") {
                const idx = this.editForm.index;
                this.languages.splice(idx, 1, {
                    name: this.editForm.name,
                    status: this.editForm.status,
                });
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById("exampleModalEdit"));
                modal.hide();
            }
        },
        removeLanguage(index) {
            this.languages.splice(this.startIndex + index, 1);
        },
    },
};
</script>