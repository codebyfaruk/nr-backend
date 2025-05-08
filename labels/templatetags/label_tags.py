from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
    
@register.filter
def chunk_by(value, size):
    """Chunk list into sublists of given size."""
    size = int(size)
    return [value[i:i+size] for i in range(0, len(value), size)]

@register.filter
def chunk_by_2(value):
    """Split a flat iterable into chunks of 2."""
    return [value[i : i + 2] for i in range(0, len(value), 2)]


@register.filter
def shorten_name(name, max_length=18):
    words = name.split()

    def shorten(words_list):
        current = " ".join(words_list)
        if len(current) <= max_length:
            return current.title()

        # Try to abbreviate the next full-length word
        for i, word in enumerate(words_list):
            if len(word) > 2 and not word.endswith("."):
                words_list[i] = word[0]
                return shorten(words_list)

        # If all words are abbreviated and it's still long, truncate
        shortened = " ".join(words_list)
        if len(shortened) > max_length:
            return shortened[: max_length - 3].rstrip() + "..."
        return shortened.title()

    return shorten(words[:])

@register.filter
def has_small_height(value, threshold=30):
    """Returns True if the label height is less than threshold (default=30)."""
    try:
        return float(value) < threshold
    except (ValueError, TypeError):
        return False
    
@register.filter
def flatten_labels(products):
    """
    Create a flat list of product references, repeated by stock_quantity.
    E.g., [{product1}, {product1}, {product2}, ...]
    """
    flat = []
    for p in products:
        flat.extend([p] * p.stock_quantity)
    return flat
