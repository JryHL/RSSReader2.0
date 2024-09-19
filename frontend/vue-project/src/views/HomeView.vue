<script setup>
import StoryCard from '@/components/StoryCard.vue';
import { getStories } from '@/api/api';
</script>

<template>
  <main>
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
      loading: false
    }
  },
  created() {
    this.fetchStoriesFromAPI(this.pageNumber);
  },
  methods: {
    async fetchStoriesFromAPI() {
      this.loading = true;
      const result = await getStories(this.pageNumber);
      this.categories.push(...result.stories);
      this.categoryLabels.push(...result.labels);
      this.pageNumber += 1
      this.loading = false;
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