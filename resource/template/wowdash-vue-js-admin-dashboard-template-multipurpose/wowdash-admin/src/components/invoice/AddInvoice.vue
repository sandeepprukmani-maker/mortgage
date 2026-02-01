<template>
    <div class="card">
      <div class="card-header">
        <div class="d-flex flex-wrap align-items-center justify-content-end gap-2">
          <button type="button" class="btn btn-sm btn-primary-600 radius-8 d-inline-flex align-items-center gap-1">
            <iconify-icon icon="simple-line-icons:check" class="text-xl"></iconify-icon>
            Save
          </button>
        </div>
      </div>
      <div class="card-body py-40">
        <div class="row justify-content-center" id="invoice">
          <div class="col-lg-8">
            <div class="shadow-4 border radius-8">
              <div class="p-20 border-bottom">
                <div class="row justify-content-between g-3">
                  <div class="col-sm-4">
                    <h3 class="text-xl">Invoice #3492</h3>
                    <p class="mb-1 text-sm">
                      Date Issued:
                      <span v-if="!edit.dateIssued" @click="edit.dateIssued = true" class="editable text-decoration-underline">{{ fields.dateIssued }}</span>
                      <input v-else v-model="fields.dateIssued" @blur="edit.dateIssued = false" class="invoive-form-control" />
                      <span class="text-success-main"><iconify-icon icon="mage:edit"></iconify-icon></span>
                    </p>
                    <p class="mb-0 text-sm">
                      Date Due:
                      <span v-if="!edit.dateDue" @click="edit.dateDue = true" class="editable text-decoration-underline">{{ fields.dateDue }}</span>
                      <input v-else v-model="fields.dateDue" @blur="edit.dateDue = false" class="invoive-form-control" />
                      <span class="text-success-main"><iconify-icon icon="mage:edit"></iconify-icon></span>
                    </p>
                  </div>
                  <div class="col-sm-4">
                    <img src="@/assets/images/logo.png" alt="image" class="mb-8" />
                    <p class="mb-1 text-sm">4517 Washington Ave. Manchester, Kentucky 39495</p>
                    <p class="mb-0 text-sm">random@gmail.com, +1 543 2198</p>
                  </div>
                </div>
              </div>
  
              <div class="py-28 px-20">
                <div class="d-flex flex-wrap justify-content-between align-items-end gap-3">
                  <div>
                    <h6 class="text-md">Issus For:</h6>
                    <table class="text-sm text-secondary-light">
                      <tbody>
                        <tr>
                          <td>Name</td>
                          <td class="ps-8">
                            :
                            <span v-if="!edit.name" @click="edit.name = true" class="editable text-decoration-underline">{{ fields.name }}</span>
                            <input v-else v-model="fields.name" @blur="edit.name = false" class="invoive-form-control" />
                            <span class="text-success-main"><iconify-icon icon="mage:edit"></iconify-icon></span>
                          </td>
                        </tr>
                        <tr>
                          <td>Address</td>
                          <td class="ps-8">
                            :
                            <span v-if="!edit.address" @click="edit.address = true" class="editable text-decoration-underline">{{ fields.address }}</span>
                            <input v-else v-model="fields.address" @blur="edit.address = false" class="invoive-form-control" />
                            <span class="text-success-main"><iconify-icon icon="mage:edit"></iconify-icon></span>
                          </td>
                        </tr>
                        <tr>
                          <td>Phone number</td>
                          <td class="ps-8">
                            :
                            <span v-if="!edit.phone" @click="edit.phone = true" class="editable text-decoration-underline">{{ fields.phone }}</span>
                            <input v-else v-model="fields.phone" @blur="edit.phone = false" class="invoive-form-control" />
                            <span class="text-success-main"><iconify-icon icon="mage:edit"></iconify-icon></span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div>
                    <table class="text-sm text-secondary-light">
                      <tbody>
                        <tr>
                          <td>Issus Date</td>
                          <td class="ps-8">:25 Jan 2024</td>
                        </tr>
                        <tr>
                          <td>Order ID</td>
                          <td class="ps-8">:#653214</td>
                        </tr>
                        <tr>
                          <td>Shipment ID</td>
                          <td class="ps-8">:#965215</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
  
               <!-- Table -->
                  <div class="mt-24">
                    <div class="table-responsive scroll-sm">
                      <table class="table bordered-table text-sm" id="invoice-table">
                        <thead>
                          <tr>
                            <th class="text-sm">SL.</th><th class="text-sm">Items</th><th class="text-sm">Qty</th><th class="text-sm">Units</th><th class="text-sm">Unit Price</th><th class="text-sm">Price</th><th class="text-sm">Action</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(item, index) in invoiceItems" :key="index">
                            <td>{{ (index + 1).toString().padStart(2, '0') }}</td>
                            <td><input type="text" class="invoive-form-control" v-model="item.name" /></td>
                            <td><input type="number" class="invoive-form-control" v-model.number="item.qty" /></td>
                            <td><input type="text" class="invoive-form-control" v-model="item.unit" /></td>
                            <td><input type="number" step="0.01" class="invoive-form-control" v-model.number="item.unitPrice" /></td>
                            <td>{{ (item.qty * item.unitPrice).toFixed(2) }}</td>
                            <td class="text-center">
                              <button type="button" @click="removeItem(index)" class="remove-row">
                                <iconify-icon icon="ic:twotone-close" class="text-danger-main text-xl"></iconify-icon>
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
    
                    <div>
                      <button type="button" id="addRow" @click="addRow" class="btn btn-sm btn-primary-600 radius-8 d-inline-flex align-items-center gap-1">
                        <iconify-icon icon="simple-line-icons:plus" class="text-xl"></iconify-icon>
                        Add New
                      </button>
                    </div>
    
                    <!-- Totals -->
                    <div class="d-flex flex-wrap justify-content-between gap-3 mt-24">
                      <div>
                        <p class="text-sm mb-0"><span class="text-primary-light fw-semibold">Sales By:</span> Jammal</p>
                        <p class="text-sm mb-0">Thanks for your business</p>
                      </div>
                      <div>
                        <table class="text-sm">
                          <tbody>
                            <tr><td class="pe-64">Subtotal:</td><td class="pe-16"><span class="text-primary-light fw-semibold">${{ subtotal.toFixed(2) }}</span></td></tr>
                            <tr><td class="pe-64">Discount:</td><td class="pe-16"><span class="text-primary-light fw-semibold">${{ discount.toFixed(2) }}</span></td></tr>
                            <tr><td class="pe-64 border-bottom pb-4">Tax:</td><td class="pe-16 border-bottom pb-4"><span class="text-primary-light fw-semibold">{{ tax.toFixed(2) }}</span></td></tr>
                            <tr><td class="pe-64 pt-4"><span class="text-primary-light fw-semibold">Total:</span></td><td class="pe-16 pt-4"><span class="text-primary-light fw-semibold">${{ total.toFixed(2) }}</span></td></tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
    
                    <div class="mt-64">
                      <p class="text-center text-secondary-light text-sm fw-semibold">Thank you for your purchase!</p>
                    </div>
    
                    <div class="d-flex flex-wrap justify-content-between align-items-end mt-64">
                      <div class="text-sm border-top d-inline-block px-12">Signature of Customer</div>
                      <div class="text-sm border-top d-inline-block px-12">Signature of Authorized</div>
                    </div>
                  </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "InvoiceEditor",
    data() {
      return {
        fields: {
          dateIssued: "25/08/2020",
          dateDue: "29/08/2020",
          name: "Will Marthas",
          address: "4517 Washington Ave.USA",
          phone: "+1 543 2198",
        },
        edit: {
          dateIssued: false,
          dateDue: false,
          name: false,
          address: false,
          phone: false,
        },
        invoiceItems: [
          { name: "Apple's Shoes", qty: 5, unit: 'PC', unitPrice: 200 },
          { name: "Apple's Shoes", qty: 5, unit: 'PC', unitPrice: 200 },
          { name: "Apple's Shoes", qty: 5, unit: 'PC', unitPrice: 200 },
          { name: "Apple's Shoes", qty: 5, unit: 'PC', unitPrice: 200 },
        ],
        discount: 0,
        tax: 0,
      };
    },
      computed: {
      subtotal() {
        return this.invoiceItems.reduce((sum, item) => sum + item.qty * item.unitPrice, 0);
      },
      total() {
        return this.subtotal - this.discount + this.tax;
      },
    },
    methods: {
      addRow() {
        this.invoiceItems.push({ name: 'New Item', qty: 1, unit: 'PC', unitPrice: 0 });
      },
      removeItem(index) {
        this.invoiceItems.splice(index, 1);
      },
    },
  };
  </script>