<template>
    <div class="col-xxl-9 col-lg-8">
      <div class="card h-100 p-0">
        <div class="card-body p-24">
          <div id="external-events" style="margin-bottom: 10px;">
            <p><strong>Draggable Events</strong></p>
            <div class="fc-event" v-for="(event, i) in externalEvents" :key="i" :class="event.className"
              style="margin: 5px; padding: 5px; cursor: pointer; background: #eee; border: 1px solid #ccc;"
              ref="draggable" :data-event='JSON.stringify({ title: event.title, className: event.className })'>
              {{ event.title }}
            </div>
            <div>
              <input type="checkbox" id="drop-remove" v-model="removeAfterDrop" />
              <label for="drop-remove">Remove after drop</label>
            </div>
          </div>
  
          <FullCalendar :options="calendarOptions" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import FullCalendar from '@fullcalendar/vue3'
  import dayGridPlugin from '@fullcalendar/daygrid'
  import interactionPlugin from '@fullcalendar/interaction'
  
  export default {
    components: { FullCalendar },
    data() {
      return {
        removeAfterDrop: false,
        externalEvents: [
          { title: 'External Event 1', className: 'bg-primary text-white' },
          { title: 'External Event 2', className: 'bg-success text-white' },
        ],
        calendarOptions: {
          plugins: [dayGridPlugin, interactionPlugin],
          initialView: 'dayGridMonth',
          editable: true,
          droppable: true,
          selectable: true,
          events: [{ title: 'Launch', date: '2025-05-12' }],
          drop: this.handleDrop,
        },
      }
    },
    mounted() {
      // Make external events draggable
      new Draggable(this.$refs.draggable[0].parentNode, {
        itemSelector: '.fc-event',
        eventData(el) {
          return JSON.parse(el.getAttribute('data-event'))
        },
      })
    },
    methods: {
      handleDrop(info) {
        if (this.removeAfterDrop && info.draggedEl.parentNode) {
          info.draggedEl.parentNode.removeChild(info.draggedEl)
        }
      },
    },
  }
  </script>
  