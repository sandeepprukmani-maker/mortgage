<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Typography" :breadcrumbs="[
            { name: 'Components / Typography' }
        ]" />

        <div class="row gy-4">
            <Heading />
            <DisplayHeading />
            <HeadingColors />
            <InineTextElements />
            <Text />
            <TextDecoration />
            <BlockquoteBgColorText />
            <BlockquoteBorderColor />
        </div>


    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Heading from '@/components/UiComponent/Typography/Heading.vue'
import DisplayHeading from '@/components/UiComponent/Typography/DisplayHeading.vue'
import HeadingColors from '@/components/UiComponent/Typography/HeadingColors.vue'
import InineTextElements from '@/components/UiComponent/Typography/InineTextElements.vue'
import Text from '@/components/UiComponent/Typography/Text.vue'
import TextDecoration from '@/components/UiComponent/Typography/TextDecoration.vue'
import BlockquoteBgColorText from '@/components/UiComponent/Typography/BlockquoteBgColorText.vue'
import BlockquoteBorderColor from '@/components/UiComponent/Typography/BlockquoteBorderColor.vue'

export default {
    name: "Typography",
    components: {
        Breadcrumb,
        Heading,
        DisplayHeading,
        HeadingColors,
        InineTextElements,
        Text,
        TextDecoration,
        BlockquoteBgColorText,
        BlockquoteBorderColor
    },
}
</script>