
<template>
    <div :class="`storyCard ${smallClass}`">
        <a :href="story.url" target="_blank"><h2>{{ story.title }}</h2></a>
        <div class="emphasis">{{ story.source }}</div>
        <div>{{ story.date }}</div>
        <div class="summary">{{story.summary}}</div>
    </div>
</template>

<script>
    export default {
        props: ["story", "index"],
        computed: {
            smallClass() {
                if (this.index == 0) {
                    return ""
                } else {
                    return `small`
                }
            }   
        }
    }
</script>

<style scoped>
.storyCard {
    display: flex;
    flex-direction: column;
    border-width: 1px;
    border-color: var(--gray-color);
    border-style: solid;
    padding: 1em;
}


.summary {
    text-wrap:nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.small {
    background-color: var(--gray-color);
    font-size: 0.8em;
}

</style>