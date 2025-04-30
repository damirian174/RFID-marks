shader_type spatial;

// Gradient texture input
uniform sampler2D gradient_texture;
// Scroll speed (negative values scroll left, positive scroll right)
uniform float scroll_speed : hint_range(-10, 10) = 1.0;

void fragment() {
    // Create scrolling UV coordinates
    vec2 scrolled_uv = UV;
    scrolled_uv.x += TIME * -scroll_speed;
    
    // Sample gradient texture
    vec4 gradient_color = texture(gradient_texture, scrolled_uv);
    
    // Multiply RGB by object's alpha channel (from vertex colors or modulate)
    // Choose ONE of these versions based on your needs:
    
    // Version 1: Multiply RGB only by alpha
	EMISSION.rg = vec2(2.0, 2.0);
	
    ALPHA = gradient_color.r;
    // Version 2: Multiply RGBA by alpha (more transparent as object fades)
    // COLOR = gradient_color * COLOR.a;
}