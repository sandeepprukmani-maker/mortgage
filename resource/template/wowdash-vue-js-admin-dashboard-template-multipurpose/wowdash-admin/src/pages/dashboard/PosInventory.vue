<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="POS & Inventory" :breadcrumbs="[
            { name: 'POS & Inventory' }
        ]" />

        <div class="row gy-4">
            <PosWidget />
            <IncomeExpense />
            <Users />
            <TopSuppliers />
            <TopCustomer />
            <OverallReport />
            <PurchaseSales />
            <RecentTransactions />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import PosWidget from "@/components/dashboard/POSinventory/PosWidget.vue"
import IncomeExpense from "@/components/dashboard/POSinventory/IncomeExpense.vue"
import Users from "@/components/dashboard/POSinventory/Users.vue"
import TopSuppliers from "@/components/dashboard/POSinventory/TopSuppliers.vue"
import TopCustomer from "@/components/dashboard/POSinventory/TopCustomer.vue"
import OverallReport from "@/components/dashboard/POSinventory/OverallReport.vue"
import PurchaseSales from "@/components/dashboard/POSinventory/PurchaseSales.vue"
import RecentTransactions from "@/components/dashboard/POSinventory/RecentTransactions.vue"

export default {
  name: "Lms",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    PosWidget,
    IncomeExpense,
    Users,
    TopSuppliers,
    TopCustomer,
    OverallReport,
    PurchaseSales,
    RecentTransactions
  },
};
</script>