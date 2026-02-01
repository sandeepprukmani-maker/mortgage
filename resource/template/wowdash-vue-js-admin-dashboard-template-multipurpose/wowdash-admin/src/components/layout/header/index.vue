<template>
  <aside class="sidebar" :class="{ 'sidebar-open': isMobileOpen }">
    <!-- Mobile Close -->
    <button type="button" class="sidebar-close-btn" @click="closeSidebar">
      <iconify-icon icon="radix-icons:cross-2" />
    </button>

    <!-- Logo -->
    <router-link to="/" class="sidebar-logo">
      <img src="@/assets/images/logo.png" alt="Logo" class="light-logo" />
      <img src="@/assets/images/logo-light.png" alt="Logo" class="dark-logo" />
      <img src="@/assets/images/logo-icon.png" alt="Logo" class="logo-icon" />
    </router-link>

    <!-- Menu -->
    <div class="sidebar-menu-area">
      <ul class="sidebar-menu">
        <li :class="{ dropdown: true, open: activeDropdown === 'dashboard' }">
          <a href="javascript:void(0)" @click="toggleDropdown('dashboard')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="solar:home-smile-angle-outline" class="menu-icon" />
            <span>Dashboard</span>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'dashboard' }"></span>
          </a>

          <!-- Transition wrapper -->
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'dashboard'" ref="dashboardMenu" class="sidebar-submenu">
              <li v-for="item in dashboardItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />
                  {{ item.label }}
                </router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Application Section -->
        <li class="sidebar-menu-group-title">Application</li>
        <li>
          <router-link to="/email" @click="() => goToRoute('/email')" :class="{ 'active-page': isActive('/email') }">
            <iconify-icon icon="mage:email" class="menu-icon"></iconify-icon>
            <span>Email</span>
          </router-link>
        </li>
        <li>
          <router-link to="/chat-message" @click="() => goToRoute('/chat-message')"
            :class="{ 'active-page': isActive('/chat-message') }">
            <iconify-icon icon="bi:chat-dots" class="menu-icon"></iconify-icon>
            <span>Chat</span>
          </router-link>
        </li>
        <li>
          <router-link to="/calendar-main" @click="() => goToRoute('/calendar-main')"
            :class="{ 'active-page': isActive('/calendar-main') }">
            <iconify-icon icon="solar:calendar-outline" class="menu-icon" />
            <span>Calendar</span>
          </router-link>
        </li>
        <li>
          <router-link to="/kanban" @click="() => goToRoute('/kanban')" :class="{ 'active-page': isActive('/kanban') }">
            <iconify-icon icon="material-symbols:map-outline" class="menu-icon" />
            <span>Kanban</span>
          </router-link>
        </li>

        <!-- Invoice Section Dropdown -->
        <li :class="{ dropdown: true, open: activeDropdown === 'invoice' }">
          <a href="javascript:void(0)" @click="toggleDropdown('invoice')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="hugeicons:invoice-03" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'invoice' }">Invoice</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'invoice'" ref="invoiceMenu" class="sidebar-submenu">
              <li v-for="item in invoiceItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Ai Applicartion... -->
        <li :class="{ dropdown: true, open: activeDropdown === 'ai' }">
          <a href="javascript:void(0)" @click="toggleDropdown('ai')" :class="{ active: isDashboardActive }">
            <i class="ri-robot-2-line text-xl me-14 d-flex w-auto"></i>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'ai' }">Ai Application</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'ai'" ref="aiMenu" class="sidebar-submenu">
              <li v-for="item in aiApplicationItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- crypto currency -->
        <li :class="{ dropdown: true, open: activeDropdown === 'crypto' }">
          <a href="javascript:void(0)" @click="toggleDropdown('crypto')" :class="{ active: isDashboardActive }">
            <i class="ri-btc-line text-xl me-14 d-flex w-auto"></i>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'crypto' }">Crypto Currency</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'crypto'" ref="cryptoMenu" class="sidebar-submenu">
              <li v-for="item in cryptoCurrencyItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- UI Element Section  -->
        <li class="sidebar-menu-group-title">UI Elements</li>

        <!-- Components -->
        <li :class="{ dropdown: true, open: activeDropdown === 'components' }">
          <a href="javascript:void(0)" @click="toggleDropdown('components')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="solar:document-text-outline" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'components' }">Components</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'components'" ref="cryptoMenu" class="sidebar-submenu">
              <li v-for="item in componentsItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Forms -->
        <li :class="{ dropdown: true, open: activeDropdown === 'forms' }">
          <a href="javascript:void(0)" @click="toggleDropdown('forms')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="heroicons:document" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'forms' }">Forms</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'forms'" ref="formsMenu" class="sidebar-submenu">
              <li v-for="item in formsItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Table -->
        <li :class="{ dropdown: true, open: activeDropdown === 'table' }">
          <a href="javascript:void(0)" @click="toggleDropdown('table')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="mingcute:storage-line" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'table' }">Table</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'table'" ref="tableMenu" class="sidebar-submenu">
              <li v-for="item in tableItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- charts -->
        <li :class="{ dropdown: true, open: activeDropdown === 'charts' }">
          <a href="javascript:void(0)" @click="toggleDropdown('charts')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="solar:pie-chart-outline" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'charts' }">Chart</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'charts'" ref="chartsMenu" class="sidebar-submenu">
              <li v-for="item in chartItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Widgets -->
        <li>
          <router-link to="/widgets" @click="() => goToRoute('/widgets')"
            :class="{ 'active-page': isActive('/widgets') }">
            <iconify-icon icon="fe:vector" class="menu-icon"></iconify-icon>
            <span>Widgets</span>
          </router-link>
        </li>

        <!-- Users -->
        <li :class="{ dropdown: true, open: activeDropdown === 'users' }">
          <a href="javascript:void(0)" @click="toggleDropdown('users')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="flowbite:users-group-outline" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'users' }">Users</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'users'" ref="usersMenu" class="sidebar-submenu">
              <li v-for="item in usersItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <li :class="{ dropdown: true, open: activeDropdown === 'role' }">
          <a href="javascript:void(0)" @click="toggleDropdown('role')" :class="{ active: isDashboardActive }">
            <i class="ri-user-settings-line text-xl me-14 d-flex w-auto"></i>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'role' }">Role & Access</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'role'" ref="roleMenu" class="sidebar-submenu">
              <li v-for="item in roleItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Application2 Section -->
        <li class="sidebar-menu-group-title">Application</li>

        <!-- authentication -->
        <li :class="{ dropdown: true, open: activeDropdown === 'authentication' }">
          <a href="javascript:void(0)" @click="toggleDropdown('authentication')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="simple-line-icons:vector" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'authentication' }">Authentication</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'authentication'" ref="authenticationMenu" class="sidebar-submenu">
              <li v-for="item in authenticationItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Gallery -->
        <li :class="{ dropdown: true, open: activeDropdown === 'gallery' }">
          <a href="javascript:void(0)" @click="toggleDropdown('gallery')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="solar:gallery-wide-linear" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'gallery' }">Gallery</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'gallery'" ref="galleryMenu" class="sidebar-submenu">
              <li v-for="item in galleryItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- pricing  -->
        <li>
          <router-link to="/pricing" @click="() => goToRoute('/pricing')"
            :class="{ 'active-page': isActive('/pricing') }">
            <iconify-icon icon="hugeicons:money-send-square" class="menu-icon"></iconify-icon>
            <span>Pricing</span>
          </router-link>
        </li>

        <!-- Blog -->
        <li :class="{ dropdown: true, open: activeDropdown === 'blog' }">
          <a href="javascript:void(0)" @click="toggleDropdown('blog')" :class="{ active: isDashboardActive }">
            <i class="ri-news-line text-xl me-14 d-flex w-auto"></i>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'blog' }">Blog</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'blog'" ref="blogMenu" class="sidebar-submenu">
              <li v-for="item in blogItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Testimonial -->
        <li>
          <router-link to="/testimonials" @click="() => goToRoute('/testimonials')"
            :class="{ 'active-page': isActive('/testimonials') }">
            <i class="ri-star-line text-xl me-14 d-flex w-auto"></i>
            <span>Testimonial</span>
          </router-link>
        </li>

        <!-- FAQs -->
        <li>
          <router-link to="/faq" @click="() => goToRoute('/faq')" :class="{ 'active-page': isActive('/faq') }">
            <iconify-icon icon="mage:message-question-mark-round" class="menu-icon"></iconify-icon>
            <span>FAQs</span>
          </router-link>
        </li>

        <!--  Error Page -->
        <li :class="{ dropdown: true, open: activeDropdown === 'error' }">
          <a href="javascript:void(0)" @click="toggleDropdown('error')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="streamline:straight-face" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'error' }">Error Pages</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'error'" ref="errorMenu" class="sidebar-submenu">
              <li v-for="item in errorItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

        <!-- Terms & Conditions -->
        <li>
          <router-link to="/terms-condition" @click="() => goToRoute('/terms-condition')"
            :class="{ 'active-page': isActive('/terms-condition') }">
            <iconify-icon icon="octicon:info-24" class="menu-icon"></iconify-icon>
            <span>Terms & Conditions</span>
          </router-link>
        </li>

        <!-- Coming Soon -->
        <li>
          <router-link to="/coming-soon" @click="() => goToRoute('/coming-soon')"
            :class="{ 'active-page': isActive('/coming-soon') }">
            <i class="ri-rocket-line text-xl me-14 d-flex w-auto"></i>
            <span>Coming Soon</span>
          </router-link>
        </li>

        <!-- Access Denied -->
        <li>
          <router-link to="/access-denied" @click="() => goToRoute('/coming-soon')"
            :class="{ 'active-page': isActive('/coming-soon') }">
            <i class="ri-folder-lock-line text-xl me-14 d-flex w-auto"></i>
            <span>Access Denied</span>
          </router-link>
        </li>

        <!-- Maintenance -->
        <li>
          <router-link to="/maintenance" @click="() => goToRoute('/maintenance')"
            :class="{ 'active-page': isActive('/maintenance') }">
            <i class="ri-hammer-line text-xl me-14 d-flex w-auto"></i>
            <span>Maintenance</span>
          </router-link>
        </li>

        <!-- Blank Page -->
        <li>
          <router-link to="/blank-page" @click="() => goToRoute('/blank-page')"
            :class="{ 'active-page': isActive('/blank-page') }">
            <i class="ri-checkbox-multiple-blank-line text-xl me-14 d-flex w-auto"></i>
            <span>Blank Page</span>
          </router-link>
        </li>

        <!-- Settings -->
        <li :class="{ dropdown: true, open: activeDropdown === 'setting' }">
          <a href="javascript:void(0)" @click="toggleDropdown('setting')" :class="{ active: isDashboardActive }">
            <iconify-icon icon="icon-park-outline:setting-two" class="menu-icon"></iconify-icon>
            <span class="dropdown-arrow" :class="{ rotated: activeDropdown === 'setting' }">Settings</span>
          </a>
          <transition @before-enter="beforeEnter" @enter="enter" @after-enter="afterEnter" @before-leave="beforeLeave"
            @leave="leave" @after-leave="afterLeave">
            <ul v-show="activeDropdown === 'setting'" ref="settingMenu" class="sidebar-submenu">
              <li v-for="item in settingItems" :key="item.path" :class="['nav-link', { 'active-page': isActive(item.path) }]">
                <router-link :to="item.path">
                  <i class="ri-circle-fill circle-icon" :class="item.colorClass" />{{ item.label }}</router-link>
              </li>
            </ul>
          </transition>
        </li>

      </ul>
    </div>
  </aside>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const activeDropdown = ref(null);
const isMobileOpen = ref(false);

const toggleDropdown = (name) => {
  activeDropdown.value = activeDropdown.value === name ? null : name;
  localStorage.setItem('activeDropdown', activeDropdown.value || '');
};

onMounted(() => {
  const savedDropdown = localStorage.getItem('activeDropdown');
  if (savedDropdown) {
    activeDropdown.value = savedDropdown;
  }
});

const closeSidebar = () => {
  isMobileOpen.value = false;
  document.body.classList.remove('overlay-active');
  const asideEl = document.querySelector('aside.sidebar');
  if (asideEl) {
    asideEl.classList.remove('sidebar-open');
  }
};

const goToRoute = (path) => {
  activeDropdown.value = null;
  closeSidebar()
  localStorage.removeItem('activeDropdown');
  router.push(path);
};

const isActive = (path) => route.path === path;

const dashboardItems = [
  { path: '/', label: 'AI', colorClass: 'text-primary-600 w-auto' },
  { path: '/crm', label: 'CRM', colorClass: 'text-warning-main w-auto' },
  { path: '/eCommerce', label: 'eCommerce', colorClass: 'text-info-main w-auto' },
  { path: '/cryptocurrency', label: 'Cryptocurrency', colorClass: 'text-danger-main w-auto' },
  { path: '/investment', label: 'Investment', colorClass: 'text-success-main w-auto' },
  { path: '/lms', label: 'LMS', colorClass: 'text-purple w-auto' },
  { path: '/nft-gaming', label: 'NFT & Gaming', colorClass: 'text-info-main w-auto' },
  { path: '/medical', label: 'Medical', colorClass: 'text-danger-main w-auto' },
  { path: '/analytics', label: 'Analytics', colorClass: 'text-purple w-auto' },
  { path: '/pos-inventory', label: 'POS & Inventory', colorClass: 'text-warning-main w-auto' },
  { path: '/finance-banking', label: 'Finance & Banking', colorClass: 'text-success-main w-auto' },
  { path: '/booking-system', label: 'Booking System', colorClass: 'text-danger-main w-auto' },
  { path: '/help-desk', label: 'Help Desk', colorClass: 'text-info-main w-auto' },
  { path: '/podcast', label: 'Podcast', colorClass: 'text-warning-main w-auto' },
  { path: '/project-management', label: 'Project Management', colorClass: 'text-purple w-auto' },
];

const invoiceItems = [
  { path: '/invoice-list', label: 'List', colorClass: 'text-primary-600 w-auto' },
  { path: '/invoice-preview', label: 'Preview', colorClass: 'text-warning-main w-auto' },
  { path: '/invoice-add', label: 'Add new', colorClass: 'text-info-main w-auto' },
  { path: '/invoice-edit', label: 'Edit', colorClass: 'text-danger-main w-auto' },
]

const aiApplicationItems = [
  { path: '/text-generator', label: 'Text Generator', colorClass: 'text-primary-600 w-auto' },
  { path: '/code-generator', label: 'Code Generator', colorClass: 'text-warning-main w-auto' },
  { path: '/image-generator', label: 'Image Generator', colorClass: 'text-info-main w-auto' },
  { path: '/voice-generator', label: 'Voice Generator', colorClass: 'text-danger-main w-auto' },
  { path: '/video-generator', label: 'Video Generator', colorClass: 'text-success-main w-auto' },
]

const cryptoCurrencyItems = [
  { path: '/wallet', label: 'Wallet', colorClass: 'text-primary-600 w-auto' },
  { path: '/marketplace', label: 'Marketplace', colorClass: 'text-warning-main w-auto' },
  { path: '/marketplace-details', label: 'Marketplace Details', colorClass: 'text-warning-main w-auto' },
  { path: '/portfolio', label: 'Portfolios', colorClass: 'text-warning-main w-auto' }
]

const componentsItems = [
  { path: '/typography', label: 'Typography', colorClass: 'text-primary-600 w-auto' },
  { path: '/colors', label: 'Colors', colorClass: 'text-warning-main w-auto' },
  { path: '/button', label: 'Button', colorClass: 'text-success-main w-auto' },
  { path: '/dropdown', label: 'Dropdown', colorClass: 'text-lilac-600 w-auto' },
  { path: '/alert', label: 'Alerts', colorClass: 'text-warning-600 w-auto' },
  { path: '/card', label: 'Card', colorClass: 'text-danger-main w-auto' },
  { path: '/carousel', label: 'Carousel', colorClass: 'text-info-main w-auto' },
  { path: '/avatar', label: 'Avatars', colorClass: 'text-success-main w-auto' },
  { path: '/progress', label: 'Progress bar', colorClass: 'text-primary-600 w-auto' },
  { path: '/tabs', label: 'Tab & Accordion', colorClass: 'text-warning-main w-auto' },
  { path: '/pagination', label: 'Pagination', colorClass: 'text-danger-main w-auto' },
  { path: '/badges', label: 'Badges', colorClass: 'text-info-main w-auto' },
  { path: '/tooltip', label: 'Tooltip & Popover', colorClass: 'text-lilac-600 w-auto' },
  { path: '/videos', label: 'Videos', colorClass: 'text-cyan w-auto' },
  { path: '/star-rating', label: 'Star Ratings', colorClass: 'text-indigo w-auto' },
  { path: '/tags', label: 'Tags', colorClass: 'text-purple w-auto' },
  { path: '/list', label: 'List', colorClass: 'text-red w-auto' },
  { path: '/calendar', label: 'Calendar', colorClass: 'text-yellow w-auto' },
  { path: '/radio', label: 'Radio', colorClass: 'text-orange w-auto' },
  { path: '/switch', label: 'Switch', colorClass: 'text-pink w-auto' },
  { path: '/image-upload', label: 'Upload', colorClass: 'text-primary-600 w-auto' },
]

const formsItems = [
  { path: '/form', label: 'Input Forms', colorClass: 'text-primary-600 w-auto' },
  { path: '/form-layout', label: 'Input Layout', colorClass: 'text-warning-main w-auto' },
  { path: '/form-validation', label: 'Form Validation', colorClass: 'text-success-main w-auto' },
  { path: '/wizard', label: 'Form Wizard', colorClass: 'text-danger-main w-auto' },
]

const tableItems = [
  { path: '/table-basic', label: 'Basic Table', colorClass: 'text-primary-600 w-auto' },
  { path: '/table-data', label: 'Data Table', colorClass: 'text-warning-main w-auto' },
]

const chartItems = [
  { path: '/line-chart', label: 'Line Chart', colorClass: 'text-danger-main w-auto' },
  { path: '/column-chart', label: 'Column Chart', colorClass: 'text-warning-main w-auto' },
  { path: '/pie-chart', label: 'Pie Chart', colorClass: 'text-success-main w-auto' },
]

const usersItems = [
  { path: '/users-list', label: 'Users List', colorClass: 'text-primary-600 w-auto' },
  { path: '/users-grid', label: 'Users Grid', colorClass: 'text-warning-main w-auto' },
  { path: '/add-user', label: 'Add user', colorClass: 'text-info-main w-auto' },
  { path: '/view-profile', label: 'View Profile', colorClass: 'text-danger-main w-auto' },
  { path: '/users-role-permission', label: 'User Role & Permission', colorClass: 'text-info-main w-auto' },
]

const roleItems = [
  { path: '/role-access', label: 'Role & Access', colorClass: 'text-primary-600 w-auto' },
  { path: '/assign-role', label: ' Assign Role', colorClass: 'text-warning-main w-auto' },
]

const authenticationItems = [
  { path: '/sign-in', label: 'Sign In', colorClass: 'text-primary-600 w-auto' },
  { path: '/sign-up', label: 'Sign Up', colorClass: 'text-warning-main w-auto' },
  { path: '/forgot-password', label: 'Forgot Password', colorClass: 'text-info-main w-auto' },
]

const galleryItems = [
  { path: '/gallery-grid', label: 'Gallery Grid', colorClass: 'text-primary-600 w-auto' },
  { path: '/gallery', label: 'Gallery Grid Desc', colorClass: 'text-danger-600 w-auto' },
  { path: '/gallery-masonry', label: 'Gallery Masonry', colorClass: 'text-info-main w-auto' },
  { path: '/gallery-hover', label: 'Gallery Hover Effect', colorClass: 'text-info-main w-auto' },
]

const blogItems = [
  { path: '/blog', label: 'Blog', colorClass: 'text-primary-600 w-auto' },
  { path: '/blog-details', label: 'Blog Details', colorClass: 'text-warning-main w-auto' },
  { path: '/add-blog', label: 'Add Blog', colorClass: 'text-info-main w-auto' },
]

const errorItems = [
  { path: '/bad-request', label: 'Bad Request', colorClass: 'text-danger-600 w-auto' },
  { path: '/forbidden', label: 'Forbidden', colorClass: 'text-info-main w-auto' },
  { path: '/error', label: '404 Page', colorClass: 'text-warning-600 w-auto' },
  { path: '/internal-server', label: 'Internal Server', colorClass: 'text-primary-main w-auto' },
  { path: '/service-unavailable', label: 'Service Unavailable', colorClass: 'text-danger-main w-auto' },
]

const settingItems = [
  { path: '/company', label: 'Company', colorClass: 'text-primary-600 w-auto' },
  { path: '/notification', label: 'Notification', colorClass: 'text-warning-main w-auto' },
  { path: '/notification-alert', label: 'Notification Alert', colorClass: 'text-info-main w-auto' },
  { path: '/theme', label: 'Theme', colorClass: 'text-danger-main w-auto' },
  { path: '/currencies', label: 'Currencies', colorClass: 'text-danger-main w-auto' },
  { path: '/language', label: 'Languages', colorClass: 'text-danger-main w-auto' },
  { path: '/payment-gateway', label: 'Payment Gateway', colorClass: 'text-danger-main w-auto' },
]

const isDashboardActive = computed(() =>
  dashboardItems.some((item) => isActive(item.path))
);

function beforeEnter(el) {
  el.style.height = '0px';
  el.style.opacity = '0';
  el.style.overflow = 'hidden';
}

function enter(el) {
  el.style.transition = 'height 0.7s ease';
  el.style.height = el.scrollHeight + 'px';
  el.style.opacity = '1';
}

function afterEnter(el) {
  el.style.height = 'auto';
  el.style.overflow = '';
  el.style.transition = '';
}

function beforeLeave(el) {
  el.style.height = el.scrollHeight + 'px';
  el.style.opacity = '1';
  el.style.overflow = 'hidden';
}

function leave(el) {
  el.style.transition = 'height 0.7s ease';
  requestAnimationFrame(() => {
    el.style.height = '0px';
    el.style.opacity = '0';
  });
}

function afterLeave(el) {
  el.style.height = '';
  el.style.opacity = '';
  el.style.transition = '';
  el.style.overflow = '';
}
</script>
