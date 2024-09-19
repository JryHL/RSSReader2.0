<script setup>
import StoryCard from '@/components/StoryCard.vue';
import { getStories } from '@/api/api';
</script>

<template>
  <main>
    <input type="text" placeholder="Search" v-if="!loading" v-model="searchQuery"/>
    <button @click="searchWithQuery" v-if="!loading"> Search </button>
    <div v-for="(stories, index) in categories" :key="stories[0]?.id || -1">
      <StoryCard :stories="stories" :label="categoryLabels[index]"/>
    </div>
    <button class="loading-button" @click="fetchStoriesFromAPI" :disabled="loading"> {{ loading ? "Loading..." : "Load more"}} </button>
  </main>
</template>

<script>
export default {
  data() {
    return {
      categories: [],
      categoryLabels: [],
      pageNumber: 0,
      loading: false,
      searchQuery: ""
    }
  },
  created() {
    this.fetchStoriesFromAPI(this.pageNumber);
  },
  methods: {
    async fetchStoriesFromAPI() {
      this.loading = true;
      const result = await getStories(this.pageNumber, this.searchQuery);
      this.categories.push(...result.stories);
      this.categoryLabels.push(...result.labels);
      this.pageNumber += 1
      this.loading = false;
    },
    searchWithQuery() {
      // Reset page number, categories due to new search
      this.pageNumber = 0;
      this.categories = [];
      this.categoryLabels = [];
      this.fetchStoriesFromAPI();
    }
  }
}
</script>

<style>
.loading-button {
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 1em;
}
</style>