import { createRouter, createWebHistory } from 'vue-router'

// DashBoard
import Ai from './pages/dashboard/ai.vue'
import Crm from './pages/dashboard/crm.vue'
import ECommerce from './pages/dashboard/eCommerce.vue'
import Cryptocurrency from './pages/dashboard/cryptocurrency.vue'
import Investment from './pages/dashboard/investment.vue'
import Lms from './pages/dashboard/lms.vue'
import NFTgaming from './pages/dashboard/NFTgaming.vue'
import Medical from './pages/dashboard/medical.vue'
import Analytics from './pages/dashboard/analytics.vue'
import PosInventory from './pages/dashboard/PosInventory.vue'
import FinanceBanking from './pages/dashboard/financeBanking.vue'
import BookingSystem from './pages/dashboard/bookingSystem.vue'
import HelpDesk from './pages/dashboard/helpDesk.vue'
import Podcast from './pages/dashboard/podcast.vue'
import ProjectManagement from './pages/dashboard/projectManagement.vue'

// Ui Component
import Typography from './pages/uiComponent/typography.vue'
import Colors from './pages/uiComponent/colors.vue'
import Button from './pages/uiComponent/button.vue'
import Dropdown from './pages/uiComponent/dropdown.vue'
import Alert from './pages/uiComponent/alert.vue'
import Badges from './pages/uiComponent/badges.vue'
import Card from './pages/uiComponent/card.vue'
import Carousel from './pages/uiComponent/carousel.vue'
import Avatar from './pages/uiComponent/avatar.vue'
import Progress from './pages/uiComponent/progress.vue'
import Tabs from './pages/uiComponent/tabs.vue'
import Pagination from './pages/uiComponent/pagination.vue'
import Tooltip from './pages/uiComponent/tooltip.vue'
import Videos from './pages/uiComponent/videos.vue'
import StarRating from './pages/uiComponent/star-rating.vue'
import Tags from './pages/uiComponent/tags.vue'
import List from './pages/uiComponent/list.vue'
import AppCalendar from './pages/uiComponent/calendar.vue'
import Radio from './pages/uiComponent/radio.vue'
import Switch from './pages/uiComponent/switch.vue'
import imageUpload from './pages/uiComponent/image-upload.vue'

// Form 
import Form from './pages/forms/form.vue'
import FormValidation from './pages/forms/form-validation.vue'
import FormWizard from './pages/forms/wizard.vue'
import FormLayout from './pages/forms/form-layout.vue'

// Table
import BasicTable from './pages/table/table-basic.vue'
import DataTable from './pages/table/table-data.vue'

// chart
import LineChart from './pages/Chart/line-chart.vue'
import ColumnChart from './pages/Chart/column-chart.vue'
import PieChart from './pages/Chart/pie-chart.vue'

// Widgets
import Widgets from './pages/widgets/widgets.vue'

// Users
import UserList from './pages/users/users-list.vue'
import ViewProfile from './pages/users/view-profile.vue'
import UserRolePermission from './pages/users/user-role-permission.vue'
import AddUser from './pages/users/add-user.vue'
import UsersGrid from './pages/users/users-grid.vue'

// Role and Permission
import AssignRole from './pages/roleAccess/assign-role.vue'
import RoleAccess from './pages/roleAccess/role-access.vue'

// authentication
import SignIn from './pages/authentication/sign-in.vue'
import SignUp from './pages/authentication/sign-up.vue'
import ForgotPassword from './pages/authentication/forgot-password.vue'


// Gallery
import Gallery from './pages/gallery/gallery.vue'
import GalleryGrid from './pages/gallery/gallery-grid.vue'
import GalleryMasonry from './pages/gallery/gallery-masonry.vue'
import GalleryHover from './pages/gallery/gallery-hover.vue'

// Pricing
import Pricing from './pages/pricing/pricing.vue'

// Blog
import Blog from './pages/blog/blog.vue'
import BlogDetails from './pages/blog/blog-details.vue'
import AddBlog from './pages/blog/add-blog.vue'

// Testimonial
import Testimonial from './pages/testimonial/testimonial.vue'

// FAQS
import FAQS from './pages/faq/faqs.vue'

// error
import Error from './pages/error/error.vue'
import BadRequest from './pages/error/bad-request.vue'
import ServiceUnavailable from './pages/error/service-unavailable.vue'
import InternalServer from './pages/error/internal-server.vue'
import Forbidden from './pages/error/forbidden.vue'

import TermsCondition from './pages/termsCondition/terms-condition.vue'

import ComingSoon from './pages/comingSoon/coming-soon.vue'
import AccessDenied from './pages/accessDenied/accessDenied.vue'
import Maintenance from './pages/maintenance/maintenance.vue'
import BlankPage from './pages/blankPage/blank-page.vue'



// email
import Email from './pages/email/Email.vue'
import StarredEmail from './pages/email/StarredEmail.vue'
import VeiwDetails from './pages/email/VeiwDetails.vue'

// Chat
import ChatMessage from './pages/chat/chat-message.vue'
import ChatProfile from './pages/chat/chat-profile.vue'
import Component from 'vue-flatpickr-component'

// Calendar
import CalendarMain from './pages/calendar-main.vue'

// Kanban
import Kanban from './pages/kanban.vue'

// Invoice
import InvoiceList from './pages/invoice/invoice-list.vue'
import InvoicePreview from './pages/invoice/invoice-preview.vue'
import InvoiceAdd from './pages/invoice/invoice-add.vue'
import InvoiceEdit from './pages/invoice/invoice-edit.vue'

// Ai Application
import TextGenerator from './pages/ai-application/text-generator/text.vue'
import TextChat from './pages/ai-application/text-generator/new-chat.vue'
import CodeGenerator from './pages/ai-application/code-generator/code.vue'
import CodeNewPage from './pages/ai-application/code-generator/new-page.vue'
import ImageGenerator from './pages/ai-application/image-generator.vue'
import VoiceGenerator from './pages/ai-application/voice-generator.vue'
import VideoGenerator from './pages/ai-application/video-generator.vue'

// Crypto Currencies
import Wallet from './pages/crypto-currency/wallet.vue'
import Marketplace from './pages/crypto-currency/marketplace.vue'
import MarketplaceDetails from './pages/crypto-currency/marketplace-details.vue'
import Portfolio from './pages/crypto-currency/portfolio.vue'

// Settings
import Company from './pages/settings/company.vue'
import Notification from './pages/settings/notification.vue'
import NotificationAlert from './pages/settings/notification-alert.vue'
import Theme from './pages/settings/theme.vue'
import Currencies from './pages/settings/currencies.vue'
import Language from './pages/settings/language.vue'
import PaymentGateway from './pages/settings/payment-gateway.vue'


const routes = [

  // DashBoard section Route
  { path: '/', component: Ai },
  { path: '/crm', component: Crm },
  { path: '/eCommerce', component: ECommerce },
  { path: '/cryptocurrency', component: Cryptocurrency },
  { path: '/investment', component: Investment },
  { path: '/lms', component: Lms },
  { path: '/nft-gaming', component: NFTgaming },
  { path: '/medical', component: Medical },
  { path: '/analytics', component: Analytics },
  { path: '/pos-inventory', component: PosInventory },
  { path: '/finance-banking', component: FinanceBanking },
  { path: '/booking-system', component: BookingSystem },
  { path: '/help-desk', component: HelpDesk },
  { path: '/podcast', component: Podcast },
  { path: '/project-management', component: ProjectManagement },

  // Email Section Route
  { path: '/email', component: Email },
  { path: '/starred-email', component: StarredEmail },
  { path: '/veiw-details', component: VeiwDetails },
  
  // Chat Section Route
  { path: '/chat-message', component: ChatMessage },
  { path: '/chat-profile', component: ChatProfile },



  // ui Component 
  { path: '/typography', component: Typography },
  { path: '/colors', component: Colors },
  { path: '/button', component: Button },
  { path: '/dropdown', component: Dropdown },
  { path: '/alert', component: Alert },
  { path: '/card', component: Card },
  { path: '/carousel', component: Carousel },
  { path: '/badges', component: Badges },
  { path: '/avatar', component: Avatar },
  { path: '/progress', component: Progress},
  { path: '/tabs', component: Tabs},
  { path: '/pagination', component: Pagination},
  { path: '/tooltip', component: Tooltip},
  { path: '/videos', component: Videos},
  { path: '/star-rating', component: StarRating},
  { path: '/tags', component: Tags},
  { path: '/list', component: List},
  { path: '/calendar', component: AppCalendar},
  { path: '/radio', component: Radio},
  { path: '/switch', component: Switch},
  { path: '/image-upload', component: imageUpload},

  // Form
  { path: '/form', component: Form },
  { path: '/form-validation', component : FormValidation },
  { path: '/wizard', component : FormWizard },
  { path: '/form-layout', component : FormLayout },


  // table
  { path: '/table-basic', component: BasicTable },
  { path: '/table-data', component: DataTable },

  // Chart
  { path: '/line-chart', component: LineChart },
  { path: '/column-chart', component: ColumnChart },
  { path: '/pie-chart', component: PieChart },

  // widgets
  { path: '/widgets', component: Widgets },

  // users
  { path: '/users-list', component: UserList },
  { path: '/view-profile', component: ViewProfile },
  { path: '/users-role-permission', component: UserRolePermission },
  { path: '/add-user', component: AddUser },
  { path: '/users-grid', component: UsersGrid },

  // Roles and permission
  { path: '/assign-role', component: AssignRole },
  { path: '/role-access', component: RoleAccess },


  // Authentication
  { path: '/sign-in', component: SignIn, meta: { layout: false } },
  { path: '/sign-up', component: SignUp, meta: { layout: false } },
  {  path: '/forgot-password', component: ForgotPassword, meta: { layout: false } },

  // Gallery
  { path: '/gallery', component: Gallery },
  { path: '/gallery-grid', component: GalleryGrid },
  { path: '/gallery-masonry', component: GalleryMasonry },
  { path: '/gallery-hover', component: GalleryHover },

  // Pricing
  { path: '/pricing', component: Pricing },

  // Blog
  { path: '/blog', component: Blog },
  { path: '/blog-details', component: BlogDetails },
  { path: '/add-blog', component: AddBlog },

  // Testimonial
  { path: '/testimonials', component: Testimonial },
  // FAQS
  { path: '/faq', component: FAQS },


  // error
  { path: '/error', component: Error },
  { path: '/bad-request', component: BadRequest },
  { path: '/service-unavailable', component: ServiceUnavailable},
  { path: '/internal-server', component: InternalServer },
  { path: '/forbidden', component: Forbidden },

  // Terms and condition
  { path: '/terms-condition', component: TermsCondition },
  { path: '/coming-soon', component: ComingSoon, meta: { layout: false }  },
  { path: '/access-denied', component: AccessDenied, meta: { layout: false }  },
  { path: '/maintenance', component: Maintenance, meta: { layout: false }  },
  { path: '/blank-page', component: BlankPage },


  // Calender Route
  { path: '/calendar-main', component: CalendarMain },

  // Khanban Route
  { path: '/kanban', component: Kanban },

  // Invoice Route
  { path: '/invoice-list', component: InvoiceList },
  { path: '/invoice-preview', component: InvoicePreview },
  { path: '/invoice-add', component: InvoiceAdd },
  { path: '/invoice-edit', component: InvoiceEdit },

  // Ai Application
  { path: '/text-generator', component: TextGenerator },
  { path: '/text-new-chat', component: TextChat },
  { path: '/code-generator', component: CodeGenerator },
  { path: '/code-generator-new', component: CodeNewPage },
  { path: '/image-generator', component: ImageGenerator },
  { path: '/voice-generator', component: VoiceGenerator },
  { path: '/video-generator', component: VideoGenerator },

  // Crypto Currency
  { path: '/wallet', component: Wallet },
  { path: '/marketplace', component: Marketplace },
  { path: '/marketplace-details', component: MarketplaceDetails },
  { path: '/portfolio', component: Portfolio },

  // Settings
  { path: '/company', component: Company },
  { path: '/notification', component: Notification },
  { path: '/notification-alert', component: NotificationAlert },
  { path: '/theme', component: Theme },
  { path: '/currencies', component: Currencies },
  { path: '/language', component: Language },
  { path: '/payment-gateway', component: PaymentGateway },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router