
<template>
    <div>
        <h3>{{ source.name }}</h3>
        <div>{{ source.url }}</div>
        <button @click="deleteSource">Delete</button>
    </div>
</template>

<script>
    import { delSource } from '@/api/api';
    export default {
        props: ["source"],
        methods: {
            async deleteSource() {
                if (confirm(`Are you sure you wish to delete ${this.source.name}?`)) {
                    await delSource(this.source.id)
                    this.$emit("delete-source")
                }
            }
        }
    }
</script>