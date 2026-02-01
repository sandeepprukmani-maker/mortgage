<template>
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Tables Border Colors</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table border-primary-table mb-0">
              <thead>
                <tr>
                  <th scope="col">
                    <div class="form-check style-check d-flex align-items-center">
                      <input class="form-check-input" type="checkbox" />
                      <label class="form-check-label"> S.L </label>
                    </div>
                  </th>
                  <th scope="col">Transaction ID</th>
                  <th scope="col">Date</th>
                  <th scope="col">Status</th>
                  <th scope="col">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in tableData" :key="index">
                  <td>
                    <div class="form-check style-check d-flex align-items-center">
                      <input class="form-check-input" type="checkbox" />
                      <label class="form-check-label">{{ row.serial }}</label>
                    </div>
                  </td>
                  <td>{{ row.transactionId }}</td>
                  <td>{{ row.date }}</td>
                  <td>
                    <span
                      :class="[
                        'px-32 py-4 rounded-pill fw-medium text-sm',
                        row.status === 'Pending'
                          ? 'bg-warning-focus text-warning-main'
                          : row.status === 'Rejected'
                          ? 'bg-danger-focus text-danger-main'
                          : 'bg-success-focus text-success-main'
                      ]"
                    >
                      {{ row.status }}
                    </span>
                  </td>
                  <td>{{ row.amount }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "TablesBorderColors",
    data() {
      return {
        tableData: [
          {
            serial: "01",
            transactionId: "5986124445445",
            date: "27 Mar 2024",
            status: "Pending",
            amount: "$20,000.00"
          },
          {
            serial: "02",
            transactionId: "5986124445445",
            date: "27 Mar 2024",
            status: "Rejected",
            amount: "$20,000.00"
          },
          {
            serial: "03",
            transactionId: "5986124445445",
            date: "27 Mar 2024",
            status: "Completed",
            amount: "$20,000.00"
          },
          {
            serial: "04",
            transactionId: "5986124445445",
            date: "27 Mar 2024",
            status: "Completed",
            amount: "$20,000.00"
          },
          {
            serial: "05",
            transactionId: "5986124445445",
            date: "27 Mar 2024",
            status: "Completed",
            amount: "$20,000.00"
          }
        ]
      };
    }
  };
  </script>
  