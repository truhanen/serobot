<template>
    <div id="led_control_div">
        <!--The image to be drawn on color_range_canvas-->
        <img id="color_picker_image" ref="color_picker_image"
             src="../assets/color_range.png" alt="Color range"
             style="display: none"/>
        <div id="color_picker_div" ref="color_picker_div">
            <canvas id="color_picker_canvas" ref="color_picker_canvas"
                    width="300px" height="300px" @click.prevent="color_range_clicked">
                Your browser does not support the HTML5 canvas element.
            </canvas>
            <img id="color_picker_pointer_image" ref="color_picker_pointer_image"
                 src="../assets/color_picker.png" alt="Color picker">
        </div>
        <input type="range" id="led_brightness_slider" ref="led_brightness_slider"
               @input="$emit('brightness-changed', Math.floor($event.target.value))">
    </div>
</template>

<script>
    export default {
        name: "LedController",
        methods: {
            draw_color_range() {
                const canvas = this.$refs.color_picker_canvas;
                const context = canvas.getContext("2d");
                const background = this.$refs.color_picker_image;
                background.onload = function() {
                    context.drawImage(background, 0, 0);
                };
            },
            color_range_clicked(click_event) {
                const color_picker_canvas = this.$refs.color_picker_canvas;
                const color_picker_context = color_picker_canvas.getContext("2d");
                const color_range_width = this.$refs.color_picker_div.clientWidth;
                const color_range_radius = color_range_width / 2;
                // Coordinates of the click
                let x = click_event.offsetX;
                let y = click_event.offsetY;
                // The coordinates transformed so that the origin is
                // at the center of color_picker_image.
                let x2 = x - color_range_radius;
                let y2 = y - color_range_radius;

                // Change color if the click was inside the radius.
                if (Math.sqrt(x2 * x2 + y2 * y2) < color_range_radius - 5) {
                    // Move the pointer.
                    const color_picker_image = this.$refs.color_picker_pointer_image;
                    color_picker_image.style.left = x + 'px';
                    color_picker_image.style.top = y + 'px';

                    // Transform the click coordinates to point to the respective pixel
                    // in the HTML canvas and its 2D context.
                    let x3 = (x / color_range_width) * color_picker_canvas.width;
                    let y3 = (y / color_range_width) * color_picker_canvas.width;
                    // Get the image data (RGBA value) of the pixel that was
                    // clicked (rectangle of size 1 x 1).
                    let rgba = color_picker_context.getImageData(
                        x3, y3, 1, 1).data;
                    let red = rgba['0'];
                    let green = rgba['1'];
                    let blue = rgba['2'];

                    // Send the RGB value to the server.
                    this.$emit("color-changed", {'red': red, 'green': green, 'blue': blue});
                }
            }
        },
        mounted() {
            this.draw_color_range();
            let led_brightness_slider = this.$refs.led_brightness_slider;
            led_brightness_slider.max = 100;
            led_brightness_slider.value = 0;
        }
    }
</script>

<style scoped>
    #color_picker_div {
        width: 100%;
        height: 20vmin;
        position: absolute;
        left: 0;
        top: 0;
    }

    #color_picker_canvas {
        width: 100%;
        height: 100%;
        position: absolute;
        left: 0;
        top: 0;
    }

    #color_picker_pointer_image {
        width: 10%;
        height: 10%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    #led_brightness_slider {
        width: 100%;
        height: 2vmin;
        position: absolute;
        left: 0;
        top: 100%;
        transform: translateY(-100%);
    }
</style>