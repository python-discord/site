# Image assets

The names of each directory correspond to the pages from which apps they are
used, except for the homepage, which uses `frontpage`, `waves`, `waves_dark`,
`sponsors`, and `sponsors_dark`.

Directories with the `_dark` suffix store alternate images to the ones in the
corresponding directory without the `_dark` suffix. When using these alternate
images, use the `light-image` class for the normal image and the `dark-image`
class for the image intended for dark mode.

The exception to this is the `waves_dark`, which is used in the homepage hero
section and the images are set by CSS using `[data-theme="light"]` and
`[data-theme="dark"]`.
