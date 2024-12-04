# What is the problem?
Many assets come with a lot of textures. Depending on the format, the referenced textures are available as image files next to the format data, which are then referenced directly in the asset. If you as a user want to access this image data, it can get complicated. The data must be stored in an accessible manner together with the geometry data. It can get complicated, especially if you are working with the Asset Importer Lib on the web or on a mobile platform. You have to put together a package that contains all the necessary data. And then it can get complicated. I don't even want to start talking about incorrectly interpreted paths in the assets.

# How to solve it!
All data in the asset importer library is stored in the aiScene container. And textures can also be stored here. How does this work? It's quite simple:

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

1.) First we check whether we have textures in the scene.
2.) If so, we iterate over all the embedded textures.
3.) Now we can read out the meta data and the actual image data.

In the material definition of the Asset Importer Lib, an embedded texture is marked with the prefix "*".