<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Calendar" :breadcrumbs="[{ name: 'Components / Calendar' }]" />
        <div class="row gy-4">
            <CalendarSidebar />
            <div class="col-xxl-9 col-lg-8">
                <div class="card h-100 p-0">
                    <div class="card-body p-24">
                        <div id="external-events" style="margin-bottom: 10px;">
                            <div class="fc-event" v-for="(event, i) in externalEvents" :key="i" :class="event.className"
                                style="margin: 5px; padding: 5px; cursor: pointer; background: #eee; border: 1px solid #ccc;"
                                ref="draggable"
                                :data-event='JSON.stringify({ title: event.title, className: event.className })'>
                                {{ event.title }}
                            </div>
                        </div>

                        <FullCalendar :options="calendarOptions" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import { Icon } from "@iconify/vue";
import CalendarSidebar from "@/components/calendar/CalendarSidebar.vue"
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
    name: "Calendar",
    components: {
        Breadcrumb,
        Icon,
        CalendarSidebar,
        FullCalendar,
    },
    data() {
        return {
            removeAfterDrop: false,
            calendarOptions: {
                plugins: [dayGridPlugin, interactionPlugin],
                initialView: 'dayGridMonth',
                editable: true,
                droppable: true,
                selectable: true,
                events: [{ title: 'Launch', date: '2025-05-12' }],
                drop: this.handleDrop,
                headerToolbar: {
                    left: 'title',
                    center: 'dayGridDay,dayGridWeek,dayGridMonth',
                    right: 'prev,next today',
                },
                customButtons: {
                    yearViewButton: {
                        text: 'Year',
                        click: () => {
                            const calendarApi = this.$refs.fullCalendar.getApi();
                            const yearStart = new Date(new Date().getFullYear(), 0, 1);
                            calendarApi.gotoDate(yearStart);
                        },
                    },
                },
                buttonText: {
                    day: 'Day',
                    week: 'Week',
                    month: 'Month',
                    today: 'Today',
                },
                eventDidMount: (info) => {
                    const headerTitle = document.querySelector('.fc-header-title');
                    if (headerTitle) {
                        headerTitle.classList.add('fc-header-title'); // Add the class explicitly
                    }
                }
            },
        }
    },
    methods: {
        gotoDate(year, month, dateOfMonth) {
            const calendarApi = this.$refs.fullCalendar.getApi();
            const targetDate = new Date(year, month - 1, dateOfMonth); // Month is 0-indexed
            calendarApi.gotoDate(targetDate); // 👈 Go to that date
        },
        handleDrop(info) {
            // Handle event drop here
            console.log('Event dropped', info);
        }
    }
};
</script>
<style>
.fc-toolbar-title {
    font-size: 24px !important;
    font-weight: 600;
}

.fc .fc-button-primary:disabled {
    border-color: var(--primary-50) !important;
    background-color: var(--primary-50) !important;
    color: var(--primary-600) !important;
}

.fc .fc-button-primary {
    background-color: transparent;
    border-color: var(--primary-50) !important;
    color: var(--primary-600) !important;

}

.fc .fc-button-primary:not(:disabled).fc-button-active, .fc .fc-button-primary:not(:disabled):active  {
    color: #fff !important;
    background-color: var(--primary-600) !important;
}
.fc .fc-button-primary:hover {
    background-color: var(--primary-600) !important;
    color: #fff !important;

}
.fc .fc-button-primary:focus{
    box-shadow: none !important;
}
</style>
