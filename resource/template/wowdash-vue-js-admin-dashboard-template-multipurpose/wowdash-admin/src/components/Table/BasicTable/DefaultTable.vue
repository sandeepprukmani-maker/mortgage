<template>
    <div class="col-lg-6">
      <div class="card h-100">
        <div class="card-header">
          <h5 class="card-title mb-0">Default Table</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table basic-table mb-0">
              <thead>
                <tr>
                  <th>S.L</th>
                  <th>Invoice</th>
                  <th>Name</th>
                  <th>Issued Date</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(entry, index) in tableData" :key="index">
                  <td>{{ entry.sl }}</td>
                  <td>
                    <a href="javascript:void(0)" class="text-primary-600">{{ entry.invoice }}</a>
                  </td>
                  <td>{{ entry.name }}</td>
                  <td>{{ entry.date }}</td>
                  <td>{{ entry.amount }}</td>
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
    name: "DefaultTable",
    data() {
      return {
        tableData: [
          { sl: "01", invoice: "#526534", name: "Kathryn Murphy", date: "25 Jan 2024", amount: "$200.00" },
          { sl: "02", invoice: "#696589", name: "Annette Black", date: "25 Jan 2024", amount: "$200.00" },
          { sl: "03", invoice: "#256584", name: "Ronald Richards", date: "10 Feb 2024", amount: "$200.00" },
          { sl: "04", invoice: "#526587", name: "Eleanor Pena", date: "10 Feb 2024", amount: "$150.00" },
          { sl: "05", invoice: "#105986", name: "Leslie Alexander", date: "15 Mar 2024", amount: "$150.00" }
        ]
      };
    }
  };
  </script>
  