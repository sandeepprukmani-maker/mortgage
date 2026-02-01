<template>
    <div class="card h-100 p-0 radius-12">
        <div
            class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
            <div class="d-flex align-items-center flex-wrap gap-3">
                <span class="text-md fw-medium text-secondary-light mb-0">Show</span>
                <select class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px" v-model="itemsPerPage">
                    <option v-for="n in 12" :key="n" :value="n">{{ n }}</option>
                </select>
                <form class="navbar-search">
                    <input type="text" class="bg-base h-40-px w-auto" v-model="searchQuery" placeholder="Search" />
                    <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
                </form>
            </div>
            <router-link to="/view-profile"
                class="btn btn-primary text-sm btn-sm px-12 py-12 radius-8 d-flex align-items-center gap-2">
                <iconify-icon icon="ic:baseline-plus" class="icon text-xl line-height-1"></iconify-icon>
                Add New User
            </router-link>
        </div>
        <div class="card-body p-24">
            <div class="row gy-4">
                <div v-for="(user, index) in filteredUsers.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)"
                    :key="user.id" class="col-xxl-3 col-md-6 user-grid-card">
                    <div class="position-relative border radius-16 overflow-hidden">
                        <img :src="user.bgImage" alt="" class="w-100 object-fit-cover" />
                        <div class="dropdown position-absolute top-0 end-0 me-16 mt-16">
                            <button type="button" data-bs-toggle="dropdown" aria-expanded="false"
                                class="bg-white-gradient-light w-32-px h-32-px radius-8 border border-light-white d-flex justify-content-center align-items-center text-white">
                                <iconify-icon icon="entypo:dots-three-vertical" class="icon"></iconify-icon>
                            </button>
                            <ul class="dropdown-menu p-12 border bg-base shadow">
                                <li>
                                    <a class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900 d-flex align-items-center gap-10"
                                        href="#">
                                        Edit
                                    </a>
                                </li>
                                <li>
                                    <button type="button"
                                        class="delete-btn dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-danger-100 text-hover-danger-600 d-flex align-items-center gap-10"
                                        @click="deleteUser(user.id)">
                                        Delete
                                    </button>
                                </li>
                            </ul>
                        </div>
                        <div class="ps-16 pb-16 pe-16 text-center mt--50">
                            <img :src="user.img" alt=""
                                class="border br-white border-width-2-px w-100-px h-100-px rounded-circle object-fit-cover" />
                            <h6 class="text-lg mb-0 mt-4">{{ user.name }}</h6>
                            <span class="text-secondary-light mb-16">{{ user.email }}</span>
                            <div
                                class="center-border position-relative bg-danger-gradient-light radius-8 p-12 d-flex align-items-center gap-4">
                                <div class="text-center w-50">
                                    <h6 class="text-md mb-0">Design</h6>
                                    <span class="text-secondary-light text-sm mb-0">Department</span>
                                </div>
                                <div class="text-center w-50">
                                    <h6 class="text-md mb-0">UI UX Designer</h6>
                                    <span class="text-secondary-light text-sm mb-0">Designation</span>
                                </div>
                            </div>
                            <router-link to="/view-profile"
                                class="bg-primary-50 text-primary-600 bg-hover-primary-600 hover-text-white p-10 text-sm btn-sm px-12 py-12 radius-8 d-flex align-items-center justify-content-center mt-16 fw-medium gap-2 w-100">
                                View Profile
                                <iconify-icon icon="solar:alt-arrow-right-linear"
                                    class="icon text-xl line-height-1"></iconify-icon>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Pagination -->
            <Pagination :currentPage="currentPage" :totalPages="totalPages" :startIndex="startIndex"
                :endIndex="endIndex" :totalItems="totalEntries" @page-changed="changePage" />
        </div>
    </div>
</template>

<script>
import user1 from "@/assets/images/user-grid/user-grid-img1.png"
import user2 from "@/assets/images/user-grid/user-grid-img2.png"
import user3 from "@/assets/images/user-grid/user-grid-img3.png"
import user4 from "@/assets/images/user-grid/user-grid-img4.png"
import user5 from "@/assets/images/user-grid/user-grid-img5.png"
import user6 from "@/assets/images/user-grid/user-grid-img6.png"
import user7 from "@/assets/images/user-grid/user-grid-img7.png"
import user8 from "@/assets/images/user-grid/user-grid-img8.png"
import user9 from "@/assets/images/user-grid/user-grid-img9.png"
import user10 from "@/assets/images/user-grid/user-grid-img10.png"
import user11 from "@/assets/images/user-grid/user-grid-img11.png"
import user12 from "@/assets/images/user-grid/user-grid-img12.png"

import userBg1 from "@/assets/images/user-grid/user-grid-bg1.png"
import userBg2 from "@/assets/images/user-grid/user-grid-bg2.png"
import userBg3 from "@/assets/images/user-grid/user-grid-bg3.png"
import userBg4 from "@/assets/images/user-grid/user-grid-bg4.png"
import userBg5 from "@/assets/images/user-grid/user-grid-bg5.png"
import userBg6 from "@/assets/images/user-grid/user-grid-bg6.png"
import userBg7 from "@/assets/images/user-grid/user-grid-bg7.png"
import userBg8 from "@/assets/images/user-grid/user-grid-bg8.png"
import userBg9 from "@/assets/images/user-grid/user-grid-bg9.png"
import userBg10 from "@/assets/images/user-grid/user-grid-bg10.png"
import userBg11 from "@/assets/images/user-grid/user-grid-bg11.png"
import userBg12 from "@/assets/images/user-grid/user-grid-bg12.png"

import Pagination from '@/components/pagination/index.vue'

export default {
    name: "UserGrid",
    components: { Pagination },
    data() {
        return {
            users: [
                { id: 1, name: "Jacob Jones", email: "ifrandom@gmail.com", img: user1, bgImage: userBg1 },
                { id: 2, name: "Darrell Steward", email: "ifrandom@gmail.com", img: user2, bgImage: userBg2 },
                { id: 3, name: "Jerome Bell", email: "ifrandom@gmail.com", img: user3, bgImage: userBg3 },
                { id: 4, name: "Eleanor Pena", email: "ifrandom@gmail.com", img: user4, bgImage: userBg4 },
                { id: 5, name: "Ralph Edwards", email: "ifrandom@gmail.com", img: user5, bgImage: userBg5 },
                { id: 6, name: "Annette Black", email: "ifrandom@gmail.com", img: user6, bgImage: userBg6 },
                { id: 7, name: "Robert Fox", email: "ifrandom@gmail.com", img: user7, bgImage: userBg7 },
                { id: 8, name: "Albert Flores", email: "ifrandom@gmail.com", img: user8, bgImage: userBg8 },
                { id: 9, name: "Dianne Russell", email: "ifrandom@gmail.com", img: user9, bgImage: userBg9 },
                { id: 10, name: "Esther Howard", email: "ifrandom@gmail.com", img: user10, bgImage: userBg10 },
                { id: 11, name: "Marvin McKinney", email: "ifrandom@gmail.com", img: user11, bgImage: userBg11 },
                { id: 12, name: "Guy Hawkins", email: "ifrandom@gmail.com", img: user12, bgImage: userBg12 },
                { id: 13, name: "Annette Black", email: "ifrandom@gmail.com", img: user6, bgImage: userBg6 },
            ],
            searchQuery: "",
            itemsPerPage: 12,
            currentPage: 1
        };
    },
    computed: {
        filteredUsers() {
            return this.users.filter(user => {
                return user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || user.email.toLowerCase().includes(this.searchQuery.toLowerCase());
            });
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
            return Math.ceil(this.filteredUsers.length / this.itemsPerPage);
        },
        startIndex() {
            return (this.currentPage - 1) * this.itemsPerPage + 1;
        },
        endIndex() {
            return Math.min(this.currentPage * this.itemsPerPage, this.filteredUsers.length);
        }
    },
    methods: {
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },
        deleteUser(userId) {
            this.users = this.users.filter(user => user.id !== userId);
        }
    }
};
</script>