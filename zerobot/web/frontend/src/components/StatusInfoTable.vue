<template>
    <table id="status_info_table">
        <tr v-for="(status_entry, i) in status_entries" :key="i">
            <td class="status_label">{{status_entry.label}}</td>
            <td class="status_value">{{status_entry.value}}</td>
        </tr>
    </table>
</template>

<script>
    export default {
        name: "StatusInfoTable",
        data() {
            return {
                status_entries: []
            }
        },
        methods: {
            write_status_info(status_data) {
                for (const [name, value] of Object.entries(status_data)) {
                    let label = name;
                    if (label in hw_status_labels) {
                        label = hw_status_labels[label];
                    }

                    let existing_entry = null;
                    for (const status_entry of this.status_entries) {
                        if (status_entry.label === label) {
                            existing_entry = status_entry;
                            break;
                        }
                    }

                    if (existing_entry != null) {
                        existing_entry.value = value;
                    }
                    else {
                        const new_entry = {label: label, value: value};
                        this.status_entries.push(new_entry);
                    }
                }
            }
        }
    }

    // Displayed labels for ZeroBotStatus values
    const hw_status_labels = {
        cpu_load: 'CPU load, %',
        camera_exposure: 'Camera exposure, us',
        distance_sensor_value: 'Distance sensor, m',
        left_proximity_value: 'Left proximity',
        right_proximity_value: 'Right proximity',
        buzzer_on: 'Buzzer on',
        line_tracker_values: 'Line trackers',
        led_brightness: 'LED brightness',
    };
</script>

<style scoped>
    #status_info_table {
        vertical-align:text-top;
    }

    .status_label {
        font-family: 'Courier New', Courier, monospace;
        font-size: 10px;
        font-weight: bold;
        color: red;
    }

    .status_value {
        font-family: 'Courier New', Courier, monospace;
        font-size: 10px;
        color: red;
    }
</style>