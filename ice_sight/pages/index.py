"""The main index page."""

import reflex as rx
from ice_sight.graphs import plot_component
from ice_sight.template import template

# import plot images method
from ice_sight.model.plotgen import generate_plot_images

import asyncio

####

class PlotSelector(rx.State):
    hour: int = 0
    max_counter: int = 10
    running: bool = False
    _n_tasks: int = 0

    # # moronic function
    # @rx.var
    # def get_hour(self) -> int:
    #     return self.hour

    @rx.background
    async def my_task(self):
        async with self:
            # The latest state values are always available inside the context
            if self._n_tasks > 0:
                # only allow 1 concurrent task
                return

            # State mutation is only allowed inside context block
            self._n_tasks += 1

        while True:
            async with self:
                # Check for stopping conditions inside context
                if self.hour >= self.max_counter:
                    self.running = False
                if not self.running:
                    self._n_tasks -= 1
                    return

                self.hour += 1

            # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(1)

    def toggle_running(self):
        self.running = not self.running
        if self.running:
            return PlotSelector.my_task

    def clear_counter(self):
        self.hour = 0


def plot_animation():
    return rx.vstack(
        rx.hstack(
            rx.button(
                rx.cond(~PlotSelector.running, "Start", "Stop"),
                on_click=PlotSelector.toggle_running,
            ),
            rx.button(
                "Reset",
                on_click=PlotSelector.clear_counter,
            ),
        )
        
    )


# cycle through the plots
def plot_component():
    # get plot images from the model
    images = generate_plot_images()
    button_html = '<button style="display: block; margin: 0 auto; border: 1px solid black;" onclick="animatePlots()">Animate Plots</button>'
    image_html = "".join(
        [
            f'<img src="{img}" style="display:none;" class="plot-image">'
            for img in images
        ]
    )
    script_html = """
    <script>
    function animatePlots() {
        let images = document.querySelectorAll('.plot-image');
        let index = 0;
        images[0].style.display = 'block';  // Show the first image
        setInterval(() => {
            if (index < images.length - 1) {
                images[index].style.display = 'none';
                index++;
                images[index].style.display = 'block';
            } else {
                clearInterval(this);
            }
        }, 1000);  // Change image every second
    }
    </script>
    """
    return rx.html(button_html + image_html + script_html)


def card(*children, **props):
    return rx.card(
        *children,
        box_shadow="rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;",
        **props,
    )


####


def page_content():
    return rx.vstack(
        rx.hstack(
            rx.image(src="\logo.png", width="70px"),
            rx.heading("Ice Sight", size="9"),
        ),
        plot_component(),
    )

@template
def index() -> rx.Component:
    return rx.box(
        rx.flex(
            page_content(),
            margin_top="calc(50px + 2em)",
            padding="2em",
            justify="center",
        ),
        # padding_left="250px",
    )
