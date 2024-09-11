
<template>
    <div :class="`storyCard ${smallClass}`">
        <a :href="story.url" target="_blank"  class="story-title"><h2>{{ story.title }}</h2></a>
        <div class="details">
            <div class="emphasis">{{ story.source }}</div>
            <div>{{ story.date }}</div>
            <div class="summary">{{story.summary}}</div>
        </div>
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

    .story-title {
        color: var(--dark-color);
        text-decoration: none;
    }

    .story-title:hover {
        color: var(--dark-gray-color);
    }
}


.summary {
    text-wrap:nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.small {
    font-size: 0.8em;
    padding-bottom: 0em;
    padding-top: 0em;
    border-style: none;


    .summary {
        display: none;
    }
    .details {
        display: flex;
        column-gap: 0.5em;
    }

    .story-title h2 {
        margin-top: 0.4em;
        margin-bottom: 0.2em;
    }
}

</style>