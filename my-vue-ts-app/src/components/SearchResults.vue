<template>
  <div class="results">
    <div v-if="results.length">
      <ul>
        <li v-for="item in results" :key="item.id">{{ item.name }}</li>
      </ul>
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">
          Anterior
        </button>
        <span>Página {{ currentPage }}</span>
        <button @click="nextPage" :disabled="!hasMoreResults">Próxima</button>
      </div>
    </div>
    <div v-else>
      <p>Nenhum resultado encontrado.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
  name: "SearchResults",
  props: {
    results: {
      type: Array as PropType<Array<{ id: number; name: string }>>,
      required: true,
    },
    currentPage: {
      type: Number,
      required: true,
    },
    hasMoreResults: {
      type: Boolean,
      required: true,
    },
    nextPage: {
      type: Function,
      required: true,
    },
    prevPage: {
      type: Function,
      required: true,
    },
  },
});
</script>

<style scoped>
.results {
  margin-top: 1rem;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #f5f7fa;
  margin: 0.5rem 0;
  padding: 0.75rem;
  border-radius: 5px;
}

.pagination {
  margin-top: 1rem;
}

button {
  margin: 0 5px;
  padding: 0.5rem 1rem;
  background-color: #3572f2;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #1a2e6c;
}
</style>
