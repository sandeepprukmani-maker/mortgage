<template>
    <div class="card h-100 p-0 radius-12">
        <div
            class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
            <div class="d-flex align-items-center flex-wrap gap-3">
                <span class="text-md fw-medium text-secondary-light mb-0">Show</span>
                <select v-model="rolesPerPage" @change="changePage(1)"
                    class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px">
                    <option v-for="n in 10" :key="n">{{ n }}</option>
                </select>
                <form class="navbar-search">
                    <input type="text" v-model="searchQuery" @input="changePage(1)" class="bg-base h-40-px w-auto"
                        placeholder="Search">
                    <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
                </form>
                <select v-model="statusFilter" @change="changePage(1)"
                    class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px">
                    <option>Status</option>
                    <option>Active</option>
                    <option>Inactive</option>
                </select>
            </div>
            <button type="button"
                class="btn btn-primary text-sm btn-sm px-12 py-12 radius-8 d-flex align-items-center gap-2"
                data-bs-toggle="modal" data-bs-target="#exampleModal">
                <iconify-icon icon="ic:baseline-plus" class="icon text-xl line-height-1"></iconify-icon>
                Add New Role
            </button>
        </div>

        <div class="card-body p-24">
            <div class="table-responsive scroll-sm">
                <table class="table bordered-table sm-table mb-0">
                    <thead>
                        <tr>
                            <th scope="col">
                                <div class="d-flex align-items-center gap-10">
                                    <div class="form-check style-check d-flex align-items-center">
                                        <input class="form-check-input radius-4 border input-form-dark" type="checkbox"
                                            name="checkbox" id="selectAll" v-model="selectAll"
                                            @change="toggleSelectAll">
                                    </div>
                                    S.L
                                </div>
                            </th>
                            <th scope="col">Create Date</th>
                            <th scope="col">Role</th>
                            <th scope="col">Description</th>
                            <th scope="col" class="text-center">Status</th>
                            <th scope="col" class="text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(role, index) in paginatedRoles" :key="index" v-show="role.isVisible">
                            <td>
                                <div class="d-flex align-items-center gap-10">
                                    <div class="form-check style-check d-flex align-items-center">
                                        <input class="form-check-input radius-4 border border-neutral-400"
                                            type="checkbox" v-model="selectedRoles" :value="role.id" />
                                    </div>
                                    {{ role.id }}
                                </div>
                            </td>
                            <td>{{ role.createDate }}</td>
                            <td>{{ role.name }}</td>
                            <td>
                                <p class="max-w-500-px">{{ role.description }}</p>
                            </td>
                            <td class="text-center">
                                <span
                                    :class="role.status === 'Active' ? 'bg-success-focus text-success-600 border border-success-main' : 'bg-danger-focus text-danger-600 border border-danger-main'"
                                    class="px-24 py-4 radius-4 fw-medium text-sm">
                                    {{ role.status }}
                                </span>
                            </td>
                            <td class="text-center">
                                <div class="d-flex align-items-center gap-10 justify-content-center">
                                    <button type="button"
                                        class="bg-success-focus text-success-600 bg-hover-success-200 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle">
                                        <iconify-icon icon="lucide:edit" class="menu-icon"></iconify-icon>
                                    </button>
                                    <button type="button"
                                        class="remove-item-btn bg-danger-focus bg-hover-danger-200 text-danger-600 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle"
                                        @click="removeRole(index)">
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
                :endIndex="endIndex" :totalItems="filteredRoles.length" @page-changed="changePage" />
        </div>
    </div>

    <!-- Modal for adding a new role -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content radius-16 bg-base">
                <div class="modal-header py-16 px-24 border border-top-0 border-start-0 border-end-0">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Add New Role</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-24">
                    <form action="#">
                        <div class="row">
                            <div class="col-12 mb-20">
                                <label class="form-label fw-semibold text-primary-light text-sm mb-8">Role Name</label>
                                <input type="text" v-model="newRole.name" class="form-control radius-8"
                                    placeholder="Enter Role Name">
                            </div>
                            <div class="col-12 mb-20">
                                <label for="desc"
                                    class="form-label fw-semibold text-primary-light text-sm mb-8">Description</label>
                                <textarea v-model="newRole.description" class="form-control" id="desc" rows="4"
                                    placeholder="Write some text"></textarea>
                            </div>

                            <div class="col-12 mb-20">
                                <label class="form-label fw-semibold text-primary-light text-sm mb-8">Status </label>
                                <div class="d-flex align-items-center flex-wrap gap-28">
                                    <div class="form-check checked-success d-flex align-items-center gap-2">
                                        <input class="form-check-input" type="radio" name="status" value="Active"
                                            v-model="newRole.status">
                                        <label
                                            class="form-check-label line-height-1 fw-medium text-secondary-light text-sm d-flex align-items-center gap-1">
                                            <span class="w-8-px h-8-px bg-success-600 rounded-circle"></span> Active
                                        </label>
                                    </div>
                                    <div class="form-check checked-danger d-flex align-items-center gap-2">
                                        <input class="form-check-input" type="radio" name="status" value="Inactive"
                                            v-model="newRole.status">
                                        <label
                                            class="form-check-label line-height-1 fw-medium text-secondary-light text-sm d-flex align-items-center gap-1">
                                            <span class="w-8-px h-8-px bg-danger-600 rounded-circle"></span> Inactive
                                        </label>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
                                <button type="reset"
                                    class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-40 py-11 radius-8">
                                    Cancel </button>
                                <button type="button" @click="saveNewRole"
                                    class="btn btn-primary border border-primary-600 text-md px-48 py-12 radius-8"> Save
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Pagination from '@/components/pagination/index.vue'
export default {
    name: 'Role',
    components: { Pagination },
    data() {
        return {
            selectAll: false,
            currentPage: 1,
            rolesPerPage: 10,
            searchQuery: "",
            statusFilter: "Status",
            roles: [
                { id: '01', createDate: "25 Jan 2024", name: "Test", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true },
                { id: '02', createDate: "25 Jan 2024", name: "Waiter", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Inactive", isVisible: true },
                { id: '03', createDate: "10 Feb 2024", name: "Manager", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true, },
                { id: '04', createDate: "10 Feb 2024", name: "Project Manager", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true, },
                { id: '05', createDate: "15 March 2024", name: "Game Developer", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Inactive", isVisible: true, },
                { id: '06', createDate: "15 March 2024", name: "Head", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true, },
                { id: '07', createDate: "27 April 2024", name: "Management", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true, },
                { id: '08', createDate: "27 April 2024", name: "Waiter", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Inactive", isVisible: true, },
                { id: '09', createDate: "30 April 2024", name: "Waiter", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true, },
                { id: 10, createDate: "30 April 2024", name: "Waiter", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true, },
                { id: 11, createDate: "10 Feb 2024", name: "Manager", description: "Lorem Ipsum is simply dummy text of the printing and typesetting", status: "Active", isVisible: true, },
            ],
            newRole: {
                name: "",
                description: "",
                status: "Active", // Default status
            },
            selectedRoles: [],
        };
    },
    computed: {
        filteredRoles() {
            return this.roles.filter(role => {
                return (this.statusFilter === 'Status' || role.status === this.statusFilter) &&
                    (role.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || role.description.toLowerCase().includes(this.searchQuery.toLowerCase()));
            });
        },
        totalPages() {
            return Math.ceil(this.filteredRoles.length / this.rolesPerPage);
        },
        startIndex() {
            return (this.currentPage - 1) * this.rolesPerPage;
        },
        endIndex() {
            return Math.min(this.startIndex + this.rolesPerPage, this.filteredRoles.length);
        },
        paginatedRoles() {
            return this.filteredRoles.slice(this.startIndex, this.endIndex);
        },
    },
    methods: {
        toggleSelectAll() {
            if (this.selectAll) {
                this.selectedRoles = this.paginatedRoles.map(role => role.id);
            } else {
                this.selectedRoles = [];
            }
        },
        removeRole(index) {
            this.roles[index].isVisible = false;
        },
        saveNewRole() {
            this.roles.push({
                ...this.newRole,
                id: this.roles.length + 1,
                createDate: new Date().toLocaleDateString(),
                isVisible: true,
            });
            this.newRole = { name: "", description: "", status: "Active" };
        },
        changePage(pageNumber) {
            this.currentPage = pageNumber;
        },
    },
};
</script>
