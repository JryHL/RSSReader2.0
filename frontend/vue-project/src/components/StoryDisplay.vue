
<template>
    <div :class="`story-box ${smallClass}`">
        <a :href="story.url" target="_blank"  class="story-title"><h3>{{ story.title }}</h3></a>
        <div class="details">
            <img class="story-favicon" :src="`https://www.google.com/s2/favicons?domain=${story?.base_domain}`"/>
            <div class="emphasis">{{ story.source }}</div>
            <div>{{ story.date }}</div>
            <div class="summary">{{story.summary}}</div>
        </div>
        <div class="alt-viewers">
            <a :href="`https://archive.today/latest/${story.url}`" target="_blank">View archived</a>
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

<style>
.story-box {
    display: flex;
    flex-direction: column;
    padding: 1em;


    .story-title {
        color: var(--dark-color);
        text-decoration: none;
    }

    .story-title h3 {
        font-size: 1.6em;
        margin-top: 0.4em;
        margin-bottom: 0.2em;
    }
    .story-favicon {
        width: 1em;
        height: 1em;
    }

    .story-title:hover {
        color: var(--dark-gray-color);
    }

    .details {
        display: flex;
        column-gap: 0.5em;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }

}


.summary {
    text-wrap:nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.small {
    padding-bottom: 0em;
    padding-top: 0em;
    border-style: none;


    .summary {
        display: none;
    }


    .story-title h3 {

        font-size: 1.1em;
    }
}

</style>