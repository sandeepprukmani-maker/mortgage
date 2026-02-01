<template>
    <div class="card basic-data-table">
        <div class="card-body">
            <div class="table-toolbar d-flex flex-wrap align-items-center justify-content-between gap-3"
                style="border-bottom: none; padding-bottom: 8px; padding-top: 1px;">
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
                    </div>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="table bordered-table mb-0 mx-0">
                    <thead>
                        <tr>
                            <th @click="sortBy('name')">User</th>
                            <th @click="sortBy('status')">Status</th>
                            <th>Role</th>
                            <th>Permission Group</th>
                            <th @click="sortBy('location')">Location</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in paginatedUsers" :key="user.email">
                            <td>
                                <div class="d-flex align-items-center">
                                    <img :src="user.image" alt=""
                                        class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                                    <div class="flex-grow-1">
                                        <span class="text-md mb-0 fw-bolder text-primary-light d-block">{{ user.name
                                            }}</span>
                                        <span class="text-sm mb-0 fw-normal text-secondary-light d-block">{{ user.email
                                            }}</span>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <span :class="statusClass(user.status)" class="px-20 py-4 rounded fw-medium text-sm">{{
                                    user.status }}</span>
                            </td>
                            <td>
                                <select class="form-select form-select-sm rounded-3 me-2" v-model="user.role"
                                    style="border-radius: 10px; height: 2.4rem; font-size: 0.87rem; font-weight: 500; width: 112px;">
                                    <option v-for="role in roles" :key="role">{{ role }}</option>
                                </select>
                            </td>
                            <td>
                                <select class="form-select form-select-sm rounded-3 me-2" v-model="user.permission"
                                    style="border-radius: 10px; height: 2.4rem; font-size: 0.87rem; font-weight: 500; width: 135px;">
                                    <option v-for="group in permissionGroups" :key="group">{{ group }}</option>
                                </select>
                            </td>
                            <td>
                                <span class="text-sm mb-0 fw-normal text-secondary-light d-block">{{ user.location
                                    }}</span>
                            </td>
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <button type="button"
                                        class="btn rounded border text-neutral-500 border-neutral-500 radius px-4 py-6 bg-hover-neutral-500 text-hover-white flex-grow-1">
                                        {{ user.status === 'Inactive' || user.status === 'Pending' ? (user.status ===
                                            'Pending' ? 'Approve' : 'Activate') : 'Deactivate' }}
                                    </button>
                                    <button type="button"
                                        class="btn rounded border text-info-500 border-info-500 radius px-4 py-6 bg-hover-info-500 text-hover-white flex-grow-1">Edit</button>
                                    <button type="button"
                                        class="btn rounded border text-danger-500 border-danger-500 radius px-4 py-6 bg-hover-danger-500 text-hover-white flex-grow-1">Delete</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <!-- Pagination  -->
                <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mt-24">
                    <span>
                        Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ filteredUsers.length }} entries
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

<script setup>
import { ref, computed } from 'vue'

import user1 from '@/assets/images/user-list/user-list1.png'
import user2 from '@/assets/images/user-list/user-list2.png'
import user3 from '@/assets/images/user-list/user-list3.png'
import user4 from '@/assets/images/user-list/user-list4.png'
import user5 from '@/assets/images/user-list/user-list5.png'
import user6 from '@/assets/images/user-list/user-list6.png'
import user7 from '@/assets/images/user-list/user-list7.png'
import user8 from '@/assets/images/user-list/user-list8.png'

const roles = ['Manager', 'Admin', 'Employee', 'Owner', 'Staff', 'Host', 'Analyst']
const permissionGroups = ['Full Access', 'Hosts', 'View Only', 'Accounting', 'Management']

const users = ref([
    { name: 'Cameron Williamson', email: 'cameron.williamson@example.com', status: 'Pending', role: 'Owner', permission: 'Accounting', location: 'Chicago, USA', image: user1 },
    { name: 'Devon Lane', email: 'devon.lane@example.com', status: 'Inactive', role: 'Admin', permission: 'Hosts', location: 'Los Angeles, USA', image: user2 },
    { name: 'Eleanor Pena', email: 'eleanor.pena@example.com', status: 'Active', role: 'Employee', permission: 'Hosts', location: 'Miami, USA', image: user3 },
    { name: 'Kathryn Murphy', email: 'kathryn.murphy@example.com', status: 'Active', role: 'Employee', permission: 'Full Access', location: 'New York, USA', image: user4 },
    { name: 'Kathryn Murphy', email: 'kathrynmurphy@gmail.com', status: 'Active', role: 'Manager', permission: 'Full Access', location: 'Mikel Roads, Port Arnoldo, ID', image: user5 },
    { name: 'Kristin Watson', email: 'Leslie Alexander', status: 'Pending', role: 'Staff', permission: 'Accounting', location: 'Seattle, USA', image: user6 },
    { name: 'Leslie Alexander', email: 'leslie.alexander@example.com', status: 'Active', role: 'Employee', permission: 'View Only', location: 'New York, USA', image: user7 },
    { name: 'Robert Fox', email: 'robert.fox@example.com', status: 'Inactive', role: 'Manager', permission: 'Full Access', location: 'Dallas, USA', image: user8 },
    
])

const selectedShow = ref(10)
const currentPage = ref(1)
const searchText = ref('')
const sortedBy = ref('')
const sortAsc = ref(true)

const filteredUsers = computed(() => {
    const keyword = searchText.value.toLowerCase()
    return users.value.filter(user =>
        user.name.toLowerCase().includes(keyword) ||
        user.email.toLowerCase().includes(keyword) ||
        user.role.toLowerCase().includes(keyword) ||
        user.permission.toLowerCase().includes(keyword) ||
        user.status.toLowerCase().includes(keyword) ||
        user.location.toLowerCase().includes(keyword)
    )
})

const sortedUsers = computed(() => {
    if (!sortedBy.value) return filteredUsers.value
    return [...filteredUsers.value].sort((a, b) => {
        const valA = a[sortedBy.value]?.toLowerCase?.() || ''
        const valB = b[sortedBy.value]?.toLowerCase?.() || ''
        return (valA > valB ? 1 : -1) * (sortAsc.value ? 1 : -1)
    })
})

const totalPages = computed(() =>
    Math.ceil(sortedUsers.value.length / selectedShow.value)
)

const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * selectedShow.value
    return sortedUsers.value.slice(start, start + selectedShow.value)
})

const startIndex = computed(() => (currentPage.value - 1) * selectedShow.value)
const endIndex = computed(() =>
    Math.min(startIndex.value + selectedShow.value, filteredUsers.value.length)
)

function sortBy(key) {
    if (sortedBy.value === key) {
        sortAsc.value = !sortAsc.value
    } else {
        sortedBy.value = key
        sortAsc.value = true
    }
}

function goToPage(page) {
    if (page < 1 || page > totalPages.value) return
    currentPage.value = page
}

function statusClass(status) {
    switch (status) {
        case 'Active':
            return 'bg-success-focus text-success-main'
        case 'Inactive':
            return 'bg-danger-focus text-danger-main'
        case 'Pending':
            return 'bg-warning-focus text-warning-main'
        default:
            return ''
    }
}
</script>