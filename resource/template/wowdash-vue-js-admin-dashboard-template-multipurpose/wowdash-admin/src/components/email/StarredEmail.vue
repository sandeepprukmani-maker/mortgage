<template>
    <div class="col-xxl-9">
      <div class="card h-100 p-0 email-card">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <div class="d-flex flex-wrap align-items-center justify-content-between gap-4">
            <div class="d-flex align-items-center gap-3">
              <div class="form-check style-check d-flex align-items-center">
                <input
                  class="form-check-input radius-4 border input-form-dark"
                  type="checkbox"
                  id="selectAll"
                  v-model="selectAll"
                  @change="toggleSelectAll"
                />
                <div class="dropdown line-height-1">
                  <button type="button" data-bs-toggle="dropdown" aria-expanded="false" class="line-height-1 d-flex">
                    <iconify-icon icon="typcn:arrow-sorted-down" class="icon line-height-1"></iconify-icon>
                  </button>
                  <ul class="dropdown-menu p-12 border bg-base shadow">
                    <li><button type="button" class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" data-bs-toggle="modal" data-bs-target="#exampleModalView">All</button></li>
                    <li><button type="button" class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" data-bs-toggle="modal" data-bs-target="#exampleModalEdit">None</button></li>
                    <li><button type="button" class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" data-bs-toggle="modal" data-bs-target="#exampleModalEdit">Read</button></li>
                    <li><button type="button" class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" data-bs-toggle="modal" data-bs-target="#exampleModalEdit">Unread</button></li>
                    <li><button type="button" class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" data-bs-toggle="modal" data-bs-target="#exampleModalEdit">Starred</button></li>
                    <li><button type="button" class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" data-bs-toggle="modal" data-bs-target="#exampleModalEdit">Unstarred</button></li>
                  </ul>
                </div>
              </div>
  
              <button type="button" class="delete-button text-secondary-light text-xl d-flex" :class="{ 'd-none': selectedCount === 0 }" @click="deleteSelected">
                <iconify-icon icon="material-symbols:delete-outline" class="icon line-height-1"></iconify-icon>
              </button>
  
              <button type="button" class="reload-button text-secondary-light text-xl d-flex" @click="reloadPage">
                <iconify-icon icon="tabler:reload" class="icon"></iconify-icon>
              </button>
  
              <div class="dropdown">
                <button type="button" data-bs-toggle="dropdown" aria-expanded="false" class=" d-flex">
                  <iconify-icon icon="entypo:dots-three-vertical" class="icon text-secondary-light"></iconify-icon>
                </button>
                <ul class="dropdown-menu dropdown-menu-lg p-12 border bg-base shadow">
                  <li>
                    <button type="button" class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900 d-flex align-items-center gap-10" data-bs-toggle="modal" data-bs-target="#exampleModalView">
                      <iconify-icon icon="gravity-ui:envelope-open" class="icon text-lg line-height-1"></iconify-icon>
                      Mark all as read
                    </button>
                  </li>
                  <li><p class="ms-40 mt-8 text-secondary-light mb-0">Select messages to see more actions</p></li>
                </ul>
              </div>
  
              <form class="navbar-search d-lg-block d-none">
                <input type="text" class="bg-base h-40-px w-auto" name="search" placeholder="Search" />
                <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
              </form>
            </div>
  
            <div class="d-flex align-items-center gap-3">
              <span class="text-secondary-light line-height-1">1-12 of 1,253</span>
              <nav aria-label="Page navigation example">
                <ul class="pagination">
                  <li class="page-item">
                    <a class="page-link d-flex bg-base border text-secondary-light text-xl" href="javascript:void(0)">
                      <iconify-icon icon="iconamoon:arrow-left-2" class="icon"></iconify-icon>
                    </a>
                  </li>
                  <li class="page-item">
                    <a class="page-link d-flex bg-base border text-secondary-light text-xl" href="javascript:void(0)">
                      <iconify-icon icon="iconamoon:arrow-right-2" class="icon"></iconify-icon>
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
  
        <div class="card-body p-0">
          <ul class="overflow-x-auto">
            <li
              v-for="(email, index) in emails"
              :key="index"
              class="email-item px-24 py-16 d-flex gap-4 align-items-center border-bottom cursor-pointer bg-hover-neutral-200 min-w-max-content"
              :class="{ active: email.checked }"
            >
              <div class="form-check style-check d-flex align-items-center">
                <input
                  class="form-check-input radius-4 border border-neutral-400"
                  type="checkbox"
                  v-model="email.checked"
                  @change="updateSelection"
                />
              </div>
              <button
                type="button"
                class="starred-button icon text-xl text-secondary-light line-height-1 d-flex"
                :class="{ active: email.starred }"
                @click="email.starred = !email.starred"
              >
                <iconify-icon icon="ph:star" class="icon-outline line-height-1"></iconify-icon>
                <iconify-icon icon="ph:star-fill" class="icon-fill line-height-1 text-warning-600"></iconify-icon>
              </button>
              <router-link
              to="/veiw-details" class="text-primary-light fw-medium text-md text-line-1 w-190-px">{{ email.sender }}</router-link>
              <router-link
              to="/veiw-details" class="text-primary-light fw-medium mb-0 text-line-1 max-w-740-px">{{ email.message }}</router-link>
              <span class="text-primary-light fw-medium min-w-max-content ms-auto">{{ email.time }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectAll: false,
        emails: [
           {
            sender: 'Jerome Bell',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Kristin Watson',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Cody Fisher',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Dianne Russell',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Floyd Miles',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Devon Lane',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Dianne Russell',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Annette Black',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Bessie Cooper',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Courtney Henry',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
          {
            sender: 'Wade Warren',
            message:
              'Aliquam pulvinar vestibulum blandit. Donec sed nisl libero. Fusce dignissim luctus sem eu dapibus.',
            time: '6:07 AM',
            checked: false,
            starred: true,
          },
        ],
      };
    },
    computed: {
      selectedCount() {
        return this.emails.filter((email) => email.checked).length;
      },
    },
    methods: {
      toggleSelectAll() {
        this.emails.forEach((email) => {
          email.checked = this.selectAll;
        });
      },
      updateSelection() {
        this.selectAll = this.emails.every((email) => email.checked);
      },
      deleteSelected() {
        this.emails = this.emails.filter((email) => !email.checked);
      },
      reloadPage() {
        location.reload();
      },
    },
  };
  </script>
  