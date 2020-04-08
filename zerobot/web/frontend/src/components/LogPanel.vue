<template>
    <div id="log_panel" ref="log_panel">
        <span v-for="(entry, i) in log_entries" :key="i">{{entry}}<br /></span>
    </div>
</template>

<script>
    export default {
        name: "LogPanel",
        data() {
            return {
                log_entries: []
            }
        },
        methods: {
            write_log(entry) {
                this.log_entries.push(entry);
            }
        },
        updated() {
            // Keep the log view scolled to bottom.
            let log_panel = this.$refs.log_panel;
            log_panel.scrollTop = log_panel.scrollHeight;
        }
    }
</script>

<style scoped>
    #log_panel {
        overflow: auto;
        border: 1px solid red;
        font-family: 'Courier New', Courier, monospace;
        font-size: 10px;
        color: red;
    }
</style>