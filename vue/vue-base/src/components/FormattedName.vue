<template>
    <!-- Display the formatted name and short description -->
    <div class="formatted-name-container">
      <!-- Formatted name with birth and death years -->
      <span>{{ formattedName }}</span>
      <!-- Short description with capitalized words -->
      <p v-if="capitalizedShortDescription">{{ capitalizedShortDescription }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "FormattedName",
    props: {
      given_names: {
        type: String,
        required: true,
      },
      family_name: {
        type: String,
        required: true,
      },
      birth_year: {
        type: [String, Number],
        required: false,
      },
      death_year: {
        type: [String, Number],
        required: false,
      },
      short_description: {
        type: String,
        required: false,
      },
    },
    computed: {
      formattedName() {
        const { given_names, family_name, birth_year, death_year } = this;
        // Construct the formatted name with years
        const years =
          birth_year && death_year ? ` (${birth_year}-${death_year})` : "";
        return `${given_names} ${family_name}${years}`;
      },
      capitalizedShortDescription() {
        if (!this.short_description) return '';
        
        // Capitalize the first letter of each word
        return this.short_description
          .toLowerCase()
          .replace(/\b\w/g, (char) => char.toUpperCase());
      },
    },
  };
  </script>
  
  <style scoped>
  .formatted-name-container {
    margin-bottom: 10px;
  }
  
  span {
    font-family: Iowan Old Style;
    color: black;
    font-weight: bold;
    font-size: 32px;
    display: block; /* Makes the name appear on its own line */
    margin-bottom: 5px;
  }
  
  p {
    font-family: Iowan Old Style;
    font-size: 26px;
    margin: 0;
    color: black;
  }
  </style>
  