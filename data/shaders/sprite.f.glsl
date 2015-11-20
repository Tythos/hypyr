uniform sampler2D tex[1];

void main() {
	float tex = texture2D(tex[0], gl_TexCoord[0].st).r;
	gl_FragColor = vec4(gl_FrontMaterial.ambient.rgb,tex);
}
