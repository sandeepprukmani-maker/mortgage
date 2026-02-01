<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Wizard" :breadcrumbs="[
            { name: 'Wizard' }
        ]" />
        <div class="row gy-4">
            <NumberingWizard />
            <NumberingWizardLabel />
            <OrderFollowingStep />
            <WizardBesideLabel />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import NumberingWizard from '@/components/Forms/FormWizard/NumberingWizard.vue'
import NumberingWizardLabel from '@/components/Forms/FormWizard/NumberingWizardLabel.vue'
import OrderFollowingStep from '@/components/Forms/FormWizard/OrderFollowingStep.vue'
import WizardBesideLabel from '@/components/Forms/FormWizard/WizardBesideLabel.vue'

export default {
    name: "FormWizard",
    components: {
        Breadcrumb,
        NumberingWizard,
        NumberingWizardLabel,
        OrderFollowingStep,
        WizardBesideLabel,
    },
}
</script>