<template>
    <div id="app">
        <img id="video_image" src="/video">

        <LogPanel id="log_panel" ref="log_panel"/>

        <StatusInfoTable id="status_info_table" ref="status_info_table"/>

        <input type="button" class="button_upper_corner" id="button_reboot" value="Reboot" @click="confirm_reboot"/>
        <input type="button" class="button_upper_corner" id="button_logout" value="Logout" @click="logout"/>

        <ArrowButtonSet id="movement_button_set" class="arrow_button_set"
                        label_up="Forward (&uarr;)"
                        label_left="Turn Left (&larr;)"
                        label_center="Beep (shift)"
                        label_right="Turn right (&rarr;)"
                        label_down="Backward (&darr;)"
                        @button-pressed="on_movement_button_pressed"
                        @button-released="on_movement_button_released"/>

        <ArrowButtonSet id="camera_button_set" class="arrow_button_set"
                        label_up="Tilt up (w)"
                        label_left="Pan left (a)"
                        label_center="Center (s)"
                        label_right="Pan right (d)"
                        label_down="Tilt down (x)"
                        @button-released="on_camera_button_released"/>

        <LedController id="led_controller"
                       @brightness-changed="on_led_brightness_change"
                       @color-changed="on_led_color_change"/>
    </div>
</template>

<script>
    import ArrowButtonSet from "./components/ArrowButtonSet.vue"
    import LedController from "./components/LedController.vue"
    import StatusInfoTable from "./components/StatusInfoTable";
    import LogPanel from "./components/LogPanel";

    export default {
        name: "App",
        data() {
            return {}
        },
        components: {
            LogPanel,
            StatusInfoTable,
            ArrowButtonSet,
            LedController,
            // VideoFrame,
        },
        methods: {
            write_log(entry_text) {
                this.$refs.log_panel.write_log(entry_text);
            },

            write_status_info(status_data) {
                this.$refs.status_info_table.write_status_info(status_data);
            },

            on_movement_button_pressed: function(direction) {
                this.send_hardware_command(hardware_commands.movement.pressed[direction]);
            },
            on_movement_button_released: function(direction) {
                this.send_hardware_command(hardware_commands.movement.released[direction]);
            },
            on_camera_button_released: function(direction) {
                this.send_hardware_command(hardware_commands.camera.released[direction]);
            },

            on_led_brightness_change: function(brightness) {
                this.send_hardware_command(form_hardware_command_led_brightness(brightness));
            },
            on_led_color_change: function(color) {
                this.send_hardware_command(form_hardware_command_led_color(color));
            },

            confirm_reboot() {
                if (confirm('Really reboot?')) {
                    this.send_hardware_command(hardware_commands.reboot);
                }
            },

            logout() {
                window.location.href = '/logout';
            },

            send_hardware_command(command) {
                command = JSON.stringify({'command': command});
                // this.write_log('Send: ' + command);
                if (this.websocket) {
                    this.websocket.send(command);
                }
                else {
                    this.write_log('Could not send command "' + command +
                                   '". No websocket connection available.');
                }
            },

            keyevent_listener(event_type, event) {
                let hardware_command = form_hardware_command_from_keyevent(event.key, event_type);
                if (hardware_command !== null) {
                    event.preventDefault();
                    this.send_hardware_command(hardware_command)
                }
            }
        },
        mounted() {
            const vm = this;

            // Setup websocket.
            this.websocket = setup_websocket(vm);

            // Setup keyboard shortcut functionality.
            document.addEventListener('keydown', this.keyevent_listener.bind(this, 'pressed'));
            document.addEventListener('keyup', this.keyevent_listener.bind(this, 'released'));
        },
        beforeDestroy() {
            // Remove the key listeners.
            document.removeEventListener('keydown', this.key_down_listener);
            document.removeEventListener('keyup', this.key_up_listener);
        }
    }


    /**
     * Create and setup a websocket connection.
     */
    function setup_websocket(vm) {
        // Determine websocket url depending on protocol.
        let ws_protocol = 'wss://';
        if (location.protocol !== 'https:') {
            ws_protocol = 'ws://';
        }
        let ws_url = ws_protocol + location.host + '/ws';

        // Create and configure the websocket connection.
        let socket = new WebSocket(ws_url);
        if (socket) {
            socket.onopen = function() {
                vm.write_log('Websocket connection opened: ' + ws_url);
            };
            socket.onmessage = function(msg) {
                let data = JSON.parse(msg.data);
                if ('status' in data) {
                    vm.write_status_info(data['status'])
                }
                else if ('log' in data) {
                    vm.write_log(data['log']);
                }
            };
            socket.onclose = function() {
                vm.write_log('Websocket connection closed.');
            };
        }
        else {
            vm.write_log('Failed to open a websocket connection.');
        }

        return socket;
    }

    const hardware_command_movement_stop = {motors: 'stop'};

    const hardware_commands = {
        movement: {
            pressed: {
                up: {motors: 'move_forward'},
                left: {motors: 'turn_left'},
                center: {buzzer: true},
                right: {motors: 'turn_right'},
                down: {motors: 'move_backward'},
            },
            released: {
                up: hardware_command_movement_stop,
                left: hardware_command_movement_stop,
                center: {buzzer: false},
                right: hardware_command_movement_stop,
                down: hardware_command_movement_stop,
            }
        },
        camera: {
            released: {
                up: {camera_tilt: 'up'},
                left: {camera_pan: 'left'},
                center: {camera_center: null},
                right: {camera_pan: 'right'},
                down: {camera_tilt: 'down'},
            }
        },
        reboot: {reboot: null},
    };

    const hardware_command_key_map = {
        w: ['movement', 'up'],
        a: ['movement', 'left'],
        Shift: ['movement', 'center'],
        d: ['movement', 'right'],
        s: ['movement', 'down'],

        ArrowUp: ['camera', 'up'],
        ArrowLeft: ['camera', 'left'],
        // Nothing for the center
        ArrowRight: ['camera', 'right'],
        ArrowDown: ['camera', 'down'],
    };

    function form_hardware_command_led_brightness(brightness) {
        return {led_brightness: brightness};
    }

    function form_hardware_command_led_color(color) {
        return {led_rgb: color};
    }

    function form_hardware_command_from_keyevent(key, event_type) {
        let command = null;
        if (key in hardware_command_key_map) {
            let [button_set, direction] = hardware_command_key_map[key];
            if (event_type in hardware_commands[button_set]) {
                command = hardware_commands[button_set][event_type][direction];
            }
        }
        return command;
    }
</script>

<style>
    body {
        background-color: black;
    }

    /* Set size and position of components. */

    /* Video image */
    #video_image {
        position: absolute;
        left: 50%;
        top: 0;
        transform: translateX(-50%);
    }
    @media (min-aspect-ratio: 4/3) {
        #video_image {
            /* Limit by viewport height */
            min-height: 100vh;
            max-height: 100vh;
        }
    }
    @media (max-aspect-ratio: 4/3) {
        #video_image {
            /* Limit by viewport width */
            min-width: 100vw;
            max-width: 100vw;
        }
    }

    /* LogPanel */
    #log_panel {
        width: 320px;
        height: 20vmin;
        position: fixed;
        left: 5px;
        top: 5px;
    }

    /* StatusInfoTable */
    #status_info_table {
        position: fixed;
        left: 5px;
        top: calc(5px + 20vmin + 5px);
    }

    /* ArrowButtonSet size */
    .arrow_button_set {
        width: 30vmin;
        height: 30vmin;
        position: fixed;
    }

    /* Movement buttons */
    #movement_button_set {
        top: calc(100% - 5px - 30vmin);
        left: 5px;
    }

    /* Camera buttons */
    #camera_button_set {
        top: calc(100% - 5px - 30vmin);
        left: calc(100% - 5px - 30vmin);
    }

    /* Buttons in the upper corner */
    .button_upper_corner {
        width: 15vmin;
        height: 6vmin;
        position: fixed;
        left: calc(100% - 5px - 15vmin);
    }

    /* Reboot button */
    #button_reboot {
        top: 5px;
    }

    /* Logout button */
    #button_logout {
        top: calc(10px + 6vmin);
    }

    /* LedController */
    #led_controller {
        width: 20vmin;
        height: 22vmin;
        position: fixed;
    }
    @media (min-aspect-ratio: 4/3) {
        #led_controller {
            /* Above the camera buttons */
            left: calc(100% - 5px - 20vmin);
            top: calc(100% - 5px - 30vmin - 5vmin - 22vmin);
        }
    }
    @media (max-aspect-ratio: 4/3) {
        #led_controller {
            /* Left of the camera buttons */
            left: calc(100% - 5px - 30vmin - 20vmin - 2vmin);
            top: calc(100% - 5px - 22vmin - 2vmin);
        }
    }
</style>
