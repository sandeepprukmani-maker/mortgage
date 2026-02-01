<template>
    <div class="col-xxl-4">
      <div class="card h-100 radius-8 border-0">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Working Schedule</h6>
          <div class="">
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8" v-model="selectedMonth">
              <option>Jan 2025</option>
              <option>Feb 2025</option>
              <option>March 2025</option>
              <option>April 2025</option>
              <option>May 2025</option>
              <option>June 2025</option>
              <option>July 2025</option>
              <option>Aug 2025</option>
              <option>Sep 2025</option>
              <option>Oct 2025</option>
              <option>Nov 2025</option>
              <option>Dec 2025</option>
            </select>
          </div>
        </div>
        <div class="card-body p-24">
          <div class="d-flex align-items-center gap-16 justify-content-between flex-wrap">
            <div
              v-for="(day, index) in days"
              :key="index"
              :class="[
                'week-item text-center',
                day.isSelected ? 'bg-purple rounded-pill py-12 px-16' : '',
                !day.isSelected ? 'text-neutral-400' : ''
              ]"
              @click="selectDay(day)"
            >
              <span class="text-sm fw-medium" :class="day.isSelected ? 'text-white' : ''">{{ day.day }}</span>
              <h6 class="text-md mb-0" :class="day.isSelected ? 'text-white' : ''">{{ day.date }}</h6>
            </div>
          </div>
  
          <div class="mt-24 d-flex flex-column gap-20">
            <div v-for="(meeting, index) in meetings" :key="index" class="d-flex align-items-center justify-content-between gap-1 ps-10" :class="`border-inline-start border-start-width-3-px ${meeting.borderClass}`">
              <div>
                <div class="d-flex align-items-center gap-1">
                  <h6 class="text-lg mb-0">{{ meeting.time }}</h6>
                  <span class="text-xs text-secondary-light fw-medium">AM</span>
                </div>
                <p class="text-sm text-secondary-light fw-medium mb-1">{{ meeting.title }}</p>
                <p class="text-xs text-neutral-400 fw-medium mb-0">Lead by <span class="text-success-600">{{ meeting.lead }}</span></p>
              </div>
              <div>
                <a href="javascript:void(0)" class="btn btn-neutral-200 text-sm text-primary-light py-6 px-16">View</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedMonth: 'Jan 2025', // Default selected month
        days: [
          { day: 'Fr', date: '21', isSelected: false },
          { day: 'Sa', date: '22', isSelected: false },
          { day: 'Su', date: '23', isSelected: false },
          { day: 'Mo', date: '24', isSelected: false },
          { day: 'Tu', date: '25', isSelected: true },
          { day: 'We', date: '26', isSelected: false },
          { day: 'Th', date: '27', isSelected: false },
          { day: 'Fr', date: '28', isSelected: false },
          { day: 'Sa', date: '29', isSelected: false },
          { day: 'Su', date: '30', isSelected: false }
        ],
        meetings: [
          {
            time: '10:20 - 11:00',
            title: 'UI UX Dashboard Project Meeting',
            lead: 'Jane Cooper',
            borderClass: 'border-purple'
          },
          {
            time: '10:20 - 11:00',
            title: 'UI UX Dashboard Project Meeting',
            lead: 'Jane Cooper',
            borderClass: 'border-warning-600'
          },
          {
            time: '10:20 - 11:00',
            title: 'UI UX Dashboard Project Meeting',
            lead: 'Jane Cooper',
            borderClass: 'border-info-600'
          }
        ]
      };
    },
    methods: {
      selectDay(selectedDay) {
        // Deselect all days
        this.days.forEach(day => day.isSelected = false);
        // Select the clicked day
        selectedDay.isSelected = true;
      }
    }
  };
  </script>