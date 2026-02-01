<template>
    <div class="dashboard-main-body">
      <Breadcrumb title="Calendar" :breadcrumbs="[{ name: 'Components / Calendar' }]" />
      <div class="row gy-4">
        <CalendarSidebar />
        <div class="col-xxl-9 col-lg-8">
          <div class="card h-100 p-0">
            <div class="card-body p-24">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="calendar-title">{{ currentTitle }}</h4>
                <div class="calendar-controls align-items-center d-flex gap-2">
                  <div class="view-buttons">
                    <button
                      class="fc-button"
                      :class="{ active: currentView === 'timeGridDay' }"
                      @click="changeView('timeGridDay')"
                    >
                      day
                    </button>
                    <button
                      class="fc-button"
                      :class="{ active: currentView === 'timeGridWeek' }"
                      @click="changeView('timeGridWeek')"
                    >
                      week
                    </button>
                    <button
                      class="fc-button"
                      :class="{ active: currentView === 'dayGridMonth' }"
                      @click="changeView('dayGridMonth')"
                    >
                      month
                    </button>
                  </div>
                  <div class="nav-buttons">
                    <button class="fc-button" @click="prev">‹</button>
                    <button class="fc-button" @click="next">›</button>
                  </div>
                  <button class="fc-button today-button" @click="today">today</button>
                </div>
              </div>
  
              <FullCalendar ref="fullCalendar" :options="calendarOptions" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
  import CalendarSidebar from '@/components/calendar/CalendarSidebar.vue';
  import FullCalendar from '@fullcalendar/vue3';
  import dayGridPlugin from '@fullcalendar/daygrid';
  import timeGridPlugin from '@fullcalendar/timegrid';
  import interactionPlugin from '@fullcalendar/interaction';
  
  export default {
    name: 'Calendar',
    components: {
      Breadcrumb,
      CalendarSidebar,
      FullCalendar,
    },
    data() {
      return {
        currentView: 'dayGridMonth',
        currentTitle: '',
        calendarOptions: {
          plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
          initialView: 'dayGridMonth',
          editable: true,
          selectable: true,
          droppable: true,
          nowIndicator: true,
          slotMinTime: '06:00:00',
          slotMaxTime: '20:00:00',
          allDaySlot: false,
          headerToolbar: false,
          events: [
            { title: 'Meeting', start: '2025-05-09T10:30:00', end: '2025-05-09T11:30:00', className: 'event-red' },
            { title: 'Lunch', start: '2025-05-09T12:00:00', end: '2025-05-09T14:00:00', className: 'event-yellow' },
            { title: 'Repeating Event', start: '2025-05-05T16:00:00', className: 'event-purple' },
          ],
          datesSet: this.updateTitle,
          firstDay: 1,
        },
      };
    },
    methods: {
      changeView(view) {
        this.currentView = view;
        this.$refs.fullCalendar.getApi().changeView(view);
        this.updateTitle();
      },
      prev() {
        this.$refs.fullCalendar.getApi().prev();
        this.updateTitle();
      },
      next() {
        this.$refs.fullCalendar.getApi().next();
        this.updateTitle();
      },
      today() {
        this.$refs.fullCalendar.getApi().today();
        this.updateTitle();
      },
      updateTitle() {
        this.currentTitle = this.$refs.fullCalendar.getApi().view.title;
      },
    },
    mounted() {
      this.updateTitle();
    },
  };
  </script>
  
  <style scoped>
  .calendar-title {
    font-size: 23px !important;
  font-weight: 700 !important;
  margin-bottom: 0 !important;
  }
  
  /* Control Layout */
  .calendar-controls {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  /* View Buttons Group */
  .view-buttons {
    display: flex;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    overflow: hidden;
    height: 32px;
  }
  
  .fc-button {
    color: #487fff;
    border: none;
    padding: 0 12px;
    font-size: 15px;
    font-weight: 500;
    height: 32px;
    line-height: 32px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  
  .fc-button:hover {
    background-color: rgb(225, 238, 255);
  }
  
  .fc-button.active {
    background-color: #487fff;
    color: white;
  }
  
  /* Navigation Buttons Group */
  .nav-buttons {
    display: flex;
    border: 1px solid #487fff;
    border-radius: 6px;
    overflow: hidden;
    height: 32px;
  }
  
  .nav-buttons .fc-button {
    padding: 0 10px;
    font-size: 16px;
  }
  
  /* Today Button */
  .today-button {
    background-color: #487fff;
    color: white;
    border-radius: 6px;
    border: none;
  }
  
  .today-button:hover {
    background-color: #2563eb;
  }
  
  /* Event styling */
  .fc-event {
    border: none;
    border-radius: 8px;
    padding: 2px 6px;
    font-size: 12px;
    font-weight: 500;
    opacity: 0.9;
  }
  
  .event-red {
    background-color: #fee2e2 !important;
    color: #dc2626 !important;
    border: 1px solid #fecaca;
  }
  
  .event-yellow {
    background-color: #fef9c3 !important;
    color: #b45309 !important;
    border: 1px solid #fde68a;
  }
  
  .event-purple {
    background-color: #ede9fe !important;
    color: #7c3aed !important;
    border: 1px solid #ddd6fe;
  }
  </style>
  