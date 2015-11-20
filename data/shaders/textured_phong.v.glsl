varying vec3 normal, light, eye;

void main() {
	normal = gl_NormalMatrix * gl_Normal;
	vec3 vVertex = vec3(gl_ModelViewMatrix * gl_Vertex);
	light = vec3(gl_LightSource[0].position.xyz - vVertex);
	eye = -vVertex;
	gl_Position = ftransform();
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
}
