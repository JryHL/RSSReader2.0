<script setup>
import StoryCard from '@/components/StoryCard.vue';
import { getStories } from '@/api/api';
</script>

<template>
  <div>

    <main class="home-main">
      <div class="search-bar">
        <input type="text" placeholder="Search" v-if="!loading" v-model="searchQuery"/>
        <button @click="searchWithQuery" v-if="!loading"> <i class="bi bi-search"></i> Search </button>
      </div>
      <div v-for="(stories, index) in categories" :key="stories[0]?.id || -1">
        <StoryCard :stories="stories" :label="categoryLabels[index]"/>
      </div>
      <button class="loading-button" @click="fetchStoriesFromAPI" :disabled="loading" v-if="!noMoreStories"> {{ loading ? "Loading..." : "Load more"}} </button>
      <div class="msg-no-stories" v-if="categories.length == 0 && !loading">
        No stories found. Try checking your internet connection or adding new sources.
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categories: [],
      categoryLabels: [],
      pageNumber: 0,
      loading: false,
      noMoreStories: false,
      searchQuery: ""
    }
  },
  created() {
    this.fetchStoriesFromAPI(this.pageNumber);
  },
  methods: {
    async fetchStoriesFromAPI() {
      this.noMoreStories = false;
      this.loading = true;
      const result = await getStories(this.pageNumber, this.searchQuery);
      this.categories.push(...result.stories);
      this.categoryLabels.push(...result.labels);
      this.pageNumber += 1
      this.loading = false;
      if (!result.stories?.length) {
        this.noMoreStories = true;
      }
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
.home-main {
  margin-left: 1em;
  margin-right: 1em;
}

.search-bar {
  display: flex;
  gap: 0.5em;
  margin-top: 0.4em;
  margin-bottom: 0.75em;
}
</style>