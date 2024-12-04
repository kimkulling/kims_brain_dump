# Wo liegt das Problem?

Viele Assets bringen einen Haufen Texturen mit sich. Je nach Format liegen die referenzerten Texturen als 
Image-Dateien neben den Formatdaten vor, die dann im Asset direct referenziert werden. Will man nun als 
Anwender auf diese Image-Daten zugreifen, kann es kompliziert werden. Die Daten müssen zusammen mit den 
Geometrie-Daten zugreifbar hinterlegt werden. Gerade wenn man im Web oder auf einer Mobile-PLattform mit
der Asset-Importer Lib arbeitet, kann es kompliziert werden. So muss man ein Packet schnüren, welches alle 
notwendigen Daten enthält. Und dann kann es kompliziert werden. Von falsch interpretierten Pfaden in den
Assets möchte ich gar nicht erst anfangen.

# Lösung
Alle Daten in der Asset-Importer-Lib werden in dem Container aiScene hinterlegt. Und hier können auch 
Texturen hinterlegt werden. Wie geht das vonstatten? Das ist recht einfach:

void LoadGLTextures(const aiScene* scene, const string& pModelPath)
{
	// Check if scene has textures.
	if(scene->HasTextures())
	{
		textureIds = new GLuint[scene->mNumTextures];
		glGenTextures(scene->mNumTextures, textureIds);// generate GL-textures ID's
		// upload textures
		for(size_t ti = 0; ti < scene->mNumTextures; ti++)
		{
			glBindTexture(GL_TEXTURE_2D, textureIds[ti]);// Binding of texture name
			//
			//redefine standard texture values
			//
			// We will use linear interpolation for magnification filter
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
			// tiling mode
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, (scene->mTextures[ti]->achFormatHint[0] & 0x01) ? GL_REPEAT : GL_CLAMP);
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, (scene->mTextures[ti]->achFormatHint[0] & 0x01) ? GL_REPEAT : GL_CLAMP);
			// Texture specification
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, scene->mTextures[ti]->mWidth, scene->mTextures[ti]->mHeight, 0, GL_BGRA, GL_UNSIGNED_BYTE,
							scene->mTextures[ti]->pcData);
		}
	}
}

