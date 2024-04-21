"""The main Dashboard App."""

from rxconfig import config

import reflex as rx

from ice_sight.styles import BACKGROUND_COLOR, FONT_FAMILY, THEME, STYLESHEETS

from ice_sight.pages.index import index

# Create app instance and add index page.
app = rx.App(
    theme=THEME,
    stylesheets=STYLESHEETS,
)

app.add_page(index, route="/")
