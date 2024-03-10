# Static CSS files

When styling components, oftentimes you can make good use of Bulma classes
rather than hardcoding CSS rules:

- [Bulma color helpers](https://bulma.io/documentation/helpers/color-helpers/):
  Classes that can be added to pretty much all Bulma components to give them a
  text or background color which are defined in [`BULMA_SETTINGS`](../settings.py).
- [Bulma typography helpers](https://bulma.io/documentation/helpers/typography-helpers/):
  Classes you can add to divs and text elements to adjust the text properties
  and alignment.
- [Bulma visibility helpers](https://bulma.io/documentation/helpers/visibility-helpers/):
  Rather than hardcoding screen width cutoffs just to adjust visibility, use
  these classes instead as they are more descriptive and provide more
  flexibility.

To adjust Bulma variables (including color, sizes, margins) for a Bulma class
everywhere, adjust the variables in [`BULMA_SETTINGS`](../../settings.py) where
applicable. The [Bulma
Variables](https://bulma.io/documentation/customize/variables/) page describes
the list of all variables and their default values.

That said, however, sometimes Bulma does not provide a good generalized
solution for a specific use case or for a specific element. In that case, use
CSS selectors to ensure that other elements that should not be styled are not
affected by the rule, and when working with colors, ensure both light and dark
modes are supported. Use `[data-theme="light"]` and `[data-theme="dark"]` to
style elements for specific themes.
