<template>
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Bordered Tables</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table basic-border-table mb-0">
              <thead>
                <tr>
                  <th>Invoice</th>
                  <th>Name</th>
                  <th>Issued Date</th>
                  <th>Amount</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(entry, index) in tableData" :key="index">
                  <td>
                    <a href="javascript:void(0)" class="text-primary-600">{{ entry.invoice }}</a>
                  </td>
                  <td>{{ entry.name }}</td>
                  <td>{{ entry.date }}</td>
                  <td>{{ entry.amount }}</td>
                  <td>
                    <a href="javascript:void(0)" class="text-primary-600">View More ></a>
                  </td>
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
    name: "BorderedTable",
    data() {
      return {
        tableData: [
          { invoice: "#526534", name: "Kathryn Murphy", date: "25 Jan 2024", amount: "$200.00" },
          { invoice: "#696589", name: "Annette Black", date: "25 Jan 2024", amount: "$200.00" },
          { invoice: "#256584", name: "256584", date: "10 Feb 2024", amount: "$200.00" },
          { invoice: "#526587", name: "Eleanor Pena", date: "10 Feb 2024", amount: "$150.00" },
          { invoice: "#105986", name: "Leslie Alexander", date: "15 Mar 2024", amount: "$150.00" }
        ]
      };
    }
  };
  </script>
  