<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Inine Text Elements</h6>
        </div>
        <div class="card-body py-16 px-24">
          <p class="mb-16 text-secondary-light fw-normal">
            You can use the mark tag to
            <span class="text-warning-main bg-warning-focus px-4">highlight</span>
            text
          </p>
          <p class="mb-16 text-secondary-light fw-normal text-decoration-line-through">
            This is a paragraph. it stands out from regular Delete text
          </p>
          <p class="mb-16 text-secondary-light fw-normal text-decoration-line-through">
            This line of text is meant to be treated as no longer accurate.
          </p>
          <p class="mb-16 text-secondary-light fw-normal text-decoration-underline">
            This line of text will render as underlined
          </p>
          <p class="mb-16 text-secondary-light fw-normal text-decoration-underline">
            This line of text is meant to be treated as an addition to the document.
          </p>
          <p class="mb-16 text-secondary-light fw-normal">
            This is a paragraph. it stands out from regular text.
          </p>
          <p class="mb-16 text-secondary-light fw-semibold">
            This line rendered as bold text.
          </p>
          <p class="mb-16 text-secondary-light fst-italic">
            This line rendered as italicized text.
          </p>
          <p class="text-secondary-light fst-italic">
            This line rendered as italicized text.
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InlineTextElementsCard'
  }
  </script>
  