<script setup>
import StoryDisplay from '@/components/StoryDisplay.vue';
</script>

<template>
    <h2>{{ label }}</h2>
    <StoryDisplay v-for="(st, index) in stories.slice(0, 1)" :key="st.id" :story="st" :index="index"/>
    <div class="carousel">
        <TransitionGroup name="more-stories">
            <StoryDisplay v-for="(st, index) in showMore ? stories.slice(1) : stories.slice(1,4)" :key="st.id" :story="st" :index="index + 1"/>
        </TransitionGroup>
    </div>
    <button v-if="stories.length > 4" @click="showMore = !showMore"> {{ showMore ? "Collapse" : "Show more"}} </button>
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

<style>
.carousel {
  margin-bottom: 0.5em;
}

.more-stories-enter-active, .more-stories-leave-active {
    transition: all 0.2s ease;
}

.more-stories-leave-to, .more-stories-enter-from {
    opacity: 0;
    transform: translateY(-30px);
}
</style>