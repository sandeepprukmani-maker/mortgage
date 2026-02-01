<template>
    <div class="card h-100 p-0 radius-12">
        <div
            class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
            <div class="d-flex align-items-center flex-wrap gap-3">
                <span class="text-md fw-medium text-secondary-light mb-0">Show</span>
                <select v-model="entriesPerPage" class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px">
                    <option v-for="n in [5, 10, 15, 20]" :key="n" :value="n">{{ n }}</option>
                </select>

                <form class="navbar-search">
                    <input v-model="searchQuery" type="text" class="bg-base h-40-px w-auto" name="search"
                        placeholder="Search" />
                    <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
                </form>

                <select v-model="selectedStatus" class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px">
                    <option>Status</option>
                    <option>Active</option>
                    <option>Inactive</option>
                </select>
            </div>
            <router-link to="/add-user"
                class="btn btn-primary text-sm btn-sm px-12 py-12 radius-8 d-flex align-items-center gap-2">
                <iconify-icon icon="ic:baseline-plus" class="icon text-xl line-height-1"></iconify-icon>
                Add New User
            </router-link>
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
                                            v-model="selectAll" @change="toggleSelectAll" />
                                    </div>
                                    S.L
                                </div>
                            </th>
                            <th scope="col">Join Date</th>
                            <th scope="col">Name</th>
                            <th scope="col">Email</th>
                            <th scope="col">Department</th>
                            <th scope="col">Designation</th>
                            <th scope="col" class="text-center">Status</th>
                            <th scope="col" class="text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(user, index) in filteredUsers" :key="index">
                            <td>
                                <div class="d-flex align-items-center gap-10">
                                    <div class="form-check style-check d-flex align-items-center">
                                        <input class="form-check-input radius-4 border border-neutral-400"
                                            type="checkbox" :value="user" v-model="selectedUsers" />
                                    </div>
                                    {{ user.sl }}
                                </div>
                            </td>
                            <td>{{ user.joinDate }}</td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <img :src="user.avatar" alt=""
                                        class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                                    <div class="flex-grow-1">
                                        <span class="text-md mb-0 fw-normal text-secondary-light">{{ user.name }}</span>
                                    </div>
                                </div>
                            </td>
                            <td><span class="text-md mb-0 fw-normal text-secondary-light">{{ user.email }}</span></td>
                            <td>{{ user.department }}</td>
                            <td>{{ user.designation }}</td>
                            <td class="text-center">
                                <span :class="[
                                    'px-24 py-4 radius-4 fw-medium text-sm border',
                                    user.status === 'Active' ? 'bg-success-focus text-success-600 border-success-main' : 'bg-neutral-200 text-neutral-600 border-neutral-400'
                                ]">
                                    {{ user.status }}
                                </span>
                            </td>
                            <td class="text-center">
                                <div class="d-flex align-items-center gap-10 justify-content-center">
                                    <button type="button"
                                        class="bg-info-focus bg-hover-info-200 text-info-600 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle">
                                        <iconify-icon icon="majesticons:eye-line" class="icon text-xl"></iconify-icon>
                                    </button>
                                    <button type="button"
                                        class="bg-success-focus text-success-600 bg-hover-success-200 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle">
                                        <iconify-icon icon="lucide:edit" class="menu-icon"></iconify-icon>
                                    </button>
                                    <button type="button"
                                        class="remove-item-btn bg-danger-focus bg-hover-danger-200 text-danger-600 fw-medium w-40-px h-40-px d-flex justify-content-center align-items-center rounded-circle"
                                        @click="hideUser(user)">
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
                :endIndex="endIndex" :totalItems="totalEntries" @page-changed="changePage" />
        </div>
    </div>
</template>

<script>
import user1 from "@/assets/images/user-list/user-list1.png"
import user2 from "@/assets/images/user-list/user-list2.png"
import user3 from "@/assets/images/user-list/user-list3.png"
import user4 from "@/assets/images/user-list/user-list4.png"
import user5 from "@/assets/images/user-list/user-list5.png"
import user6 from "@/assets/images/user-list/user-list6.png"
import user7 from "@/assets/images/user-list/user-list7.png"
import user8 from "@/assets/images/user-list/user-list8.png"
import user10 from "@/assets/images/user-list/user-list10.png"

import Pagination from '@/components/pagination/index.vue'

export default {
    name: "UserTable",
    components: { Pagination },
    data() {
        return {
            users: [
                {
                    sl: "01",
                    joinDate: "25 Jan 2024",
                    name: "Kathryn Murphy",
                    email: "osgoodwy@gmail.com",
                    department: "HR",
                    designation: "Manager",
                    status: "Active",
                    avatar: user1,
                    hidden: false,
                },
                {
                    sl: "02",
                    joinDate: "25 Jan 2024",
                    name: "Annette Black",
                    email: "redaniel@gmail.com",
                    department: "Design",
                    designation: "UI UX Designer",
                    status: "Inactive",
                    avatar: user2,
                    hidden: false,
                },
                {
                    sl: "03",
                    joinDate: "10 Feb 2024",
                    name: "Ronald Richards",
                    email: "seannand@mail.ru",
                    department: "Design",
                    designation: "UI UX Designer",
                    status: "Active",
                    avatar: user3,
                    hidden: false,
                },
                {
                    sl: "04",
                    joinDate: "10 Feb 2024",
                    name: "Eleanor Pena",
                    email: "miyokoto@mail.ru",
                    department: "Design",
                    designation: "UI UX Designer",
                    status: "Active",
                    avatar: user4,
                    hidden: false,
                },
                {
                    sl: "05",
                    joinDate: "15 March 2024",
                    name: "Leslie Alexander",
                    email: "icadahli@gmail.com",
                    department: "Design",
                    designation: "UI UX Designer",
                    status: "Inactive",
                    avatar: user5,
                    hidden: false,
                },
                {
                    sl: "06",
                    joinDate: "15 March 2024",
                    name: "Albert Flores",
                    email: "warn@mail.ru",
                    department: "Design",
                    designation: "UI UX Designer",
                    status: "Active",
                    avatar: user6,
                    hidden: false,
                },
                {
                    sl: "07",
                    joinDate: "27 April 2024",
                    name: "Jacob Jones",
                    email: "zitka@mail.ru",
                    department: "Development",
                    designation: "Frontend developer",
                    status: "Active",
                    avatar: user7,
                    hidden: false,
                },
                {
                    sl: "08",
                    joinDate: "25 Jan 2024",
                    name: "Jerome Bell",
                    email: "igerrin@gmail.com",
                    department: "Development",
                    designation: "Frontend developer",
                    status: "Inactive",
                    avatar: user8,
                    hidden: false,
                },
                {
                    sl: "09",
                    joinDate: "30 April 2024",
                    name: "Marvin McKinney",
                    email: "maka@yandex.ru",
                    department: "Development",
                    designation: "Frontend developer",
                    status: "Active",
                    avatar: user2,
                    hidden: false,
                },
                {
                    sl: "10",
                    joinDate: "30 April 2024",
                    name: "Cameron Williamson",
                    email: "danten@mail.ru",
                    department: "Development",
                    designation: "Frontend developer",
                    status: "Active",
                    avatar: user10,
                    hidden: false,
                },
                {
                    sl: "11",
                    joinDate: "30 April 2024",
                    name: "Marvin McKinney",
                    email: "maka@yandex.ru",
                    department: "Development",
                    designation: "Frontend developer",
                    status: "Active",
                    avatar: user2,
                    hidden: false,
                },
            ],
            selectedUsers: [],
            searchQuery: '',
            selectedStatus: 'Status',
            entriesPerPage: 10,
            currentPage: 1,
        };
    },
    computed: {
        selectAll: {
            get() {
                return this.filteredUsers.length > 0 &&
                    this.selectedUsers.length === this.filteredUsers.length;
            },
            set(value) {
                if (value) {
                    this.selectedUsers = [...this.filteredUsers];
                } else {
                    this.selectedUsers = [];
                }
            }
        },
        filteredUsers() {
            let filtered = this.users.filter(user => {
                const matchesSearch = user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    user.email.toLowerCase().includes(this.searchQuery.toLowerCase());
                const matchesStatus = this.selectedStatus === 'Status' || user.status === this.selectedStatus;
                return matchesSearch && matchesStatus && !user.hidden;
            });

            this.totalFiltered = filtered.length;
            const start = (this.currentPage - 1) * this.entriesPerPage;
            return filtered.slice(start, start + this.entriesPerPage);
        },
        totalEntries() {
            return this.users.filter(user => {
                const matchesSearch = user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    user.email.toLowerCase().includes(this.searchQuery.toLowerCase());
                const matchesStatus = this.selectedStatus === 'Status' || user.status === this.selectedStatus;
                return matchesSearch && matchesStatus && !user.hidden;
            }).length;
        },
        totalPages() {
            return Math.ceil(this.totalEntries / this.entriesPerPage);
        },
        startIndex() {
            return (this.currentPage - 1) * this.entriesPerPage + 1;
        },
        endIndex() {
            return Math.min(this.startIndex + this.entriesPerPage - 1, this.totalEntries);
        }
    },
    watch: {
        searchQuery() {
            this.currentPage = 1;
        },
        selectedStatus() {
            this.currentPage = 1;
        },
        entriesPerPage() {
            this.currentPage = 1;
        },
    },
    methods: {
        toggleSelectAll() {
            if (this.selectAll) {
                this.selectedUsers = [...this.filteredUsers];
            } else {
                this.selectedUsers = [];
            }
        },
        hideUser(user) {
            user.hidden = true;
        },
        prevPage() {
            if (this.currentPage > 1) this.currentPage--;
        },
        nextPage() {
            if (this.currentPage < this.totalPages) this.currentPage++;
        },
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        }
    }
};
</script>