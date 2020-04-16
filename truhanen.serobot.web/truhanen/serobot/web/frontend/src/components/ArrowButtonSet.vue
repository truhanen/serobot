<template>
    <div class="arrow_button_set">
        <input type="button" class="arrow_button_up" :value="label_up" v-on="handlers_up"/>
        <input type="button" class="arrow_button_left" :value="label_left" v-on="handlers_left"/>
        <input type="button" class="arrow_button_center" :value="label_center" v-on="handlers_center"/>
        <input type="button" class="arrow_button_right" :value="label_right" v-on="handlers_right"/>
        <input type="button" class="arrow_button_down" :value="label_down" v-on="handlers_down"/>
    </div>
</template>

<script>
    export default {
        name: "ArrowButtonSet",
        props: [
            "label_up",
            "label_left",
            "label_center",
            "label_right",
            "label_down"
        ],
        data() {
            const vm = this;
            return {
                handlers_up: create_button_handlers(vm, 'up'),
                handlers_left: create_button_handlers(vm, 'left'),
                handlers_center: create_button_handlers(vm, 'center'),
                handlers_right: create_button_handlers(vm, 'right'),
                handlers_down: create_button_handlers(vm, 'down'),
            }
        },
        methods: {
            button_pressed(direction) {
                this.$emit('button-pressed', direction);
            },
            button_released(direction) {
                this.$emit('button-released', direction);
            }
        }
    }

    function create_button_handlers(vm, direction) {
        let button_pressed = function() {
            vm.button_pressed(direction)
        };
        let button_released = function() {
            vm.button_released(direction)
        };
        return {
            mousedown: button_pressed,
            touchstart: button_pressed,
            mouseup: button_released,
            touchend: button_released
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .arrow_button_up,
    .arrow_button_down,
    .arrow_button_left,
    .arrow_button_right,
    .arrow_button_center {
        width: 33.333%;
        height: 33.333%;
        position: absolute
    }

    .arrow_button_up {
        left: 33.333%;
        top: 0;
    }
    .arrow_button_down {
        left: 33.333%;
        top: 66.667%;
    }
    .arrow_button_left {
        left: 0;
        top: 33.333%;
    }
    .arrow_button_right {
        left: 66.667%;
        top: 33.333%;
    }
    .arrow_button_center {
        left: 33.333%;
        top: 33.333%;
    }
</style>
