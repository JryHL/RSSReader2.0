<script setup>
import StoryCard from '@/components/StoryCard.vue';
import { getStories } from '@/api/api';
</script>

<template>
  <main>
    <div v-for="(stories, index) in categories" :key="stories[0]?.id || -1">
      <StoryCard :stories="stories" :label="categoryLabels[index]"/>
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

