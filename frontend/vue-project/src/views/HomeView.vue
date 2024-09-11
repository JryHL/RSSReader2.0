<script setup>
import StoryDisplay from '@/components/StoryDisplay.vue';
import { getStories } from '@/api/api';
</script>

<template>
  <main>
    <div v-for="(stories, index) in categories" :key="stories[0]?.id || -1">
      <h2>{{ categoryLabels[index] }}</h2>
      <StoryDisplay v-for="(st, index) in stories.slice(0, 1)" :key="st.id" :story="st" :index="index"/>
      <div class="carousel">
        <StoryDisplay v-for="(st, index) in stories.slice(1)" :key="st.id" :story="st" :index="index + 1"/>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {
      categories: [],
      categoryLabels: []
    }
  },
  created() {
    this.fetchStoriesFromAPI();
  },
  methods: {
    async fetchStoriesFromAPI() {
      const result = await getStories();
      this.categories = result.stories;
      this.categoryLabels = result.labels;
    }
  }
}
</script>

<style scoped>
.carousel {
  display: grid;
  grid-template-columns: repeat(auto-fill, 20em);
  gap: 0.5em;
  overflow: auto;
  height: 300px;
  margin-bottom: 0.5em;
}
</style>