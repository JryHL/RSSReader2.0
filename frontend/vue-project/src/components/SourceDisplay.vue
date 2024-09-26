
<template>
    <div class="source-card-wrap">
        <div>
        <h3>{{ source.name }}</h3>
        <div>{{ source.url }}</div>
        </div>
        <button class="button-delete-source" @click="deleteSource"> <i class="bi bi-trash"></i> Delete</button>
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

<style>
.source-card-wrap {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    border-width: 1px;
    border-color: var(--gray-color);
    border-style: solid;
    padding: 1em;
    margin-bottom: 0.75em;
    box-shadow: 0px 3px 5px var(--gray-color);
    h3 {
        margin: 0;
    }
}
.button-delete-source {
    height: 50%;
    align-self: center;
}
</style>