<script setup>
import StoryDisplay from '@/components/StoryDisplay.vue';
</script>

<template>
    <h2>{{ label }}</h2>
    <StoryDisplay v-for="(st, index) in stories.slice(0, 1)" :key="st.id" :story="st" :index="index"/>
    <div class="carousel">
        <StoryDisplay v-for="(st, index) in showMore ? stories.slice(1) : stories.slice(1,4)" :key="st.id" :story="st" :index="index + 1"/>
    </div>
    <button @click="showMore = !showMore"> {{ showMore ? "Collapse" : "Show more"}} </button>
</template>

<script>
export default {
    props: ["stories", "label"],
    data() {
        return {
            showMore: false
        }
    }
}
</script>

<style scoped>
.carousel {
  margin-bottom: 0.5em;
}
</style>