void main() {
	mat4 mvm = gl_ModelViewMatrix;
	mvm[0][0] = 0.0;
	mvm[0][1] = 0.0;
	mvm[0][2] = 1.0;
	mvm[1][0] = 1.0;
	mvm[1][1] = 0.0;
	mvm[1][2] = 0.0;
	mvm[2][0] = 0.0;
	mvm[2][1] = 1.0;
	mvm[2][2] = 0.0;
	gl_Position = gl_ProjectionMatrix * mvm * gl_Vertex;
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
}
