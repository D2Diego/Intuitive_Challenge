<template>
  <div class="search-view">
    <h2>Pesquisa de Operadores</h2>
    <div class="search-box">
      <input
        v-model="query"
        @keyup.enter="fetchResults"
        placeholder="Digite para pesquisar"
      />
      <button @click="fetchResults">Buscar</button>
    </div>

    <SearchResults
      :results="results"
      :currentPage="currentPage"
      :hasMoreResults="hasMoreResults"
      :nextPage="nextPage"
      :prevPage="prevPage"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import axios from "axios";
import SearchResults from "@/components/SearchResults.vue";

export default defineComponent({
  name: "SearchView",
  components: { SearchResults },
  setup() {
    const query = ref<string>("");
    const results = ref<
      Array<{ id: number; nome_fantasia: string; razao_social: string }>
    >([]);
    const currentPage = ref<number>(1);
    const hasMoreResults = ref<boolean>(true);

    const fetchResults = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/operadoras/search?q=${query.value}&page=${currentPage.value}`
        );
        results.value = response.data.results;
        hasMoreResults.value =
          response.data.pagination.current_page <
          response.data.pagination.total_pages;
      } catch (error) {
        console.error("Erro ao buscar resultados:", error);
        results.value = [];
        hasMoreResults.value = false;
      }
    };

    const nextPage = () => {
      currentPage.value++;
      fetchResults();
    };

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
        fetchResults();
      }
    };

    return {
      query,
      results,
      currentPage,
      hasMoreResults,
      fetchResults,
      nextPage,
      prevPage,
    };
  },
});
</script>

<style scoped>
.search-view {
  max-width: 600px;
  margin: 2rem auto;
  text-align: center;
  color: #1a2e6c;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  font-weight: bold;
}

.search-box {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

input {
  padding: 0.5rem;
  border: 1px solid #1a2e6c;
  border-radius: 5px;
  width: 300px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #3572f2;
}

button {
  padding: 0.5rem 1rem;
  background-color: #3572f2;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #1a2e6c;
}
</style>
