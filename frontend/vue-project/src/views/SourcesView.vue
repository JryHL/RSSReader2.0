<script setup>
import SourceDisplay from '@/components/SourceDisplay.vue';
import { getSources, addSource } from '@/api/api';
</script>
<template>
    <main>
        <h2>Your Sources</h2>
        <div>
            <SourceDisplay v-for="s in sources" :key="s.id" :source="s" @delete-source="refresh"/>
        </div>
        <h2>Add source</h2>

        <input type="text" placeholder="Source name" v-model="addSourceName"/>
        <input type="url" placeholder="Source URL" v-model="addSourceURL"/>
        <button @click="addSourceToBackend" >Add</button>

    </main>
</template>

<script>

export default {
    data() {
        return {
            sources: [],
            addSourceURL: "",
            addSourceName: ""
        }
    },
    created() {
        this.fetchSourcesFromAPI()
    },
    methods: {
        refresh() {
            this.fetchSourcesFromAPI();
        },
        async fetchSourcesFromAPI() {
            let res = await getSources();
            this.sources = res;

        },
        async addSourceToBackend() {
            let res = await addSource(this.addSourceName, this.addSourceURL);
            if (res) {
                this.fetchSourcesFromAPI();
                this.addSourceName = "";
                this.addSourceURL = "";
            }
        }
    }

}
</script>