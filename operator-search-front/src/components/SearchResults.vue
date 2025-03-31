<template>
  <div class="results">
    <div v-if="results.length">
      <div class="results-grid">
        <div v-for="item in results" :key="item.id" class="result-card">
          <h3>{{ item.nome_fantasia }}</h3>
          <div class="result-details">
            <p><strong>Razão Social:</strong> {{ item.razao_social }}</p>
            <p><strong>Registro ANS:</strong> {{ item.registro_ans }}</p>
            <p><strong>CNPJ:</strong> {{ formatCNPJ(item.cnpj) }}</p>
            <p><strong>Modalidade:</strong> {{ item.modalidade }}</p>
            <p><strong>Localização:</strong> {{ item.cidade }}/{{ item.uf }}</p>
            <p v-if="item.telefone">
              <strong>Telefone:</strong> {{ formatTelefone(item.telefone) }}
            </p>
          </div>
        </div>
      </div>
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

interface Operadora {
  id: number;
  nome_fantasia: string;
  razao_social: string;
  registro_ans: number;
  cnpj: number;
  modalidade: string;
  cidade: string;
  uf: string;
  telefone: number;
}

export default defineComponent({
  name: "SearchResults",
  props: {
    results: {
      type: Array as PropType<Operadora[]>,
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
  methods: {
    formatCNPJ(cnpj: number | null) {
      if (!cnpj) return "";
      const cnpjStr = cnpj.toString().padStart(14, "0");
      return cnpjStr.replace(
        /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
        "$1.$2.$3/$4-$5"
      );
    },
    formatTelefone(telefone: number | null) {
      if (!telefone) return "";
      const telStr = telefone.toString().padStart(10, "0");
      return telStr.replace(/^(\d{2})(\d{4,5})(\d{4})$/, "($1) $2-$3");
    },
  },
});
</script>

<style scoped>
.results {
  margin-top: 1rem;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.result-card {
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-card h3 {
  color: #1a2e6c;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.result-details p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #444;
}

.result-details strong {
  color: #1a2e6c;
}

.pagination {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

button {
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
