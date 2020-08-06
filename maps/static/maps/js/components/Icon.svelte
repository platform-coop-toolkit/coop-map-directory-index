<script>
export let name;
export let size;
export let classOverride;
export let modifier = name;
export let ariaHidden = true;
export let viewBox = '0 0 20 20';
export let focusable = false;

let className = '';

if (classOverride) {
    className = classOverride;
} else {
    className = (size) ? `icon icon--${modifier} icon--${size}` : `icon icon--${modifier}`;
}
</script>

<svg class={className} aria-hidden={ariaHidden} viewBox={viewBox} focusable={focusable}>
    <use href="/static/maps/dist/images/{name}.svg#{name}" />
</svg>
