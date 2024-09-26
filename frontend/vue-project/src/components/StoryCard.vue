<script setup>
import StoryDisplay from '@/components/StoryDisplay.vue';
</script>

<template>
    <div class="story-card-wrap">
        <h2>{{ label }}</h2>
        <StoryDisplay v-for="(st, index) in stories.slice(0, 1)" :key="st.id" :story="st" :index="index"/>
        <hr class="top-story-separator" v-if="stories.length > 1">
        <div class="carousel">
            <TransitionGroup name="more-stories">
                <StoryDisplay v-for="(st, index) in showMore ? stories.slice(1) : stories.slice(1,4)" :key="st.id" :story="st" :index="index + 1"/>
            </TransitionGroup>
        </div>
        <button class="show-more-btn" v-if="stories.length > 4" @click="showMore = !showMore">
            <i class="bi bi-chevron-down" v-if="!showMore"></i>
            <i class="bi bi-chevron-up" v-else></i> 
            {{ showMore ? "Collapse" : "Show more"}} 
        </button>
    </div>
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
  margin-bottom: 1em;
}

.more-stories-enter-active, .more-stories-leave-active {
    transition: all 0.2s ease;
}

.more-stories-leave-to, .more-stories-enter-from {
    opacity: 0;
    transform: translateY(-30px);
}

.story-card-wrap {
    display: flex;
    flex-direction: column;
    border-width: 1px;
    border-color: var(--gray-color);
    border-style: solid;
    padding: 1em;
    margin-bottom: 0.75em;
    box-shadow: 0px 3px 5px var(--gray-color);
}
.show-more-btn {
    align-self:center;
}

.top-story-separator {
    width: 100%;
    border-color: var(--gray-color);
}
</style>