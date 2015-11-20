varying vec3 normal, light, eye;

void main() {
	vec4 ambient = gl_FrontMaterial.ambient * gl_LightSource[0].ambient;
	vec4 diffuse = gl_FrontMaterial.diffuse * max(0.0, dot(normalize(light), normalize(normal))) * gl_LightSource[0].diffuse;
	vec4 specular = gl_FrontMaterial.specular * pow(max(0.0, dot(reflect(-normalize(light), normalize(normal)), normalize(eye))), gl_FrontMaterial.shininess) * gl_LightSource[0].specular;
	gl_FragColor = ambient + diffuse + specular;
}
