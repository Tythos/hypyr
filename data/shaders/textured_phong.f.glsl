varying vec3 normal, light, eye;
uniform sampler2D tex[1];

void main() {
	vec4 texColor = texture2D(tex[0], gl_TexCoord[0].st);
	vec4 ambient = texColor * gl_LightSource[0].ambient;
	vec4 diffuse = texColor * max(0.0, dot(normalize(light), normalize(normal))) * gl_LightSource[0].diffuse;
	vec4 specular = texColor * pow(max(0.0, dot(reflect(-normalize(light), normalize(normal)), normalize(eye))), gl_FrontMaterial.shininess) * gl_LightSource[0].specular;
	gl_FragColor = ambient + diffuse + specular;
}
