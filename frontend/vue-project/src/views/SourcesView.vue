<script setup>
import SourceDisplay from '@/components/SourceDisplay.vue';
import { getSources, addSource } from '@/api/api';
</script>
<template>
    <main class="add-source-main">
        <h2>Add source</h2>
        <div class="add-source-form">
            <input type="text" placeholder="Source name" v-model="addSourceName"/>
            <input type="url" placeholder="Source URL" v-model="addSourceURL"/>
            <button :disabled="loading" @click="addSourceToBackend" ><i class="bi bi-plus"></i>Add</button>
        </div>
        <h2>Your Sources</h2>
        <div>
            <SourceDisplay v-for="s in sources.slice().reverse()" :key="s.id" :source="s" @delete-source="refresh"/>
        </div>


    </main>
</template>

<script>

export default {
    data() {
        return {
            sources: [],
            addSourceURL: "",
            addSourceName: "",
            loading: false
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
            this.loading = true;
            let res = await addSource(this.addSourceName, this.addSourceURL);
            if (res) {
                this.fetchSourcesFromAPI();
                this.addSourceName = "";
                this.addSourceURL = "";
            }
            this.loading = false;
        }
    }

}
</script>

<style>

.add-source-main {
    margin-left: 1em;
    margin-right: 1em;
}
.add-source-form {
    display: flex;
    gap: 0.3em;
}
</style>