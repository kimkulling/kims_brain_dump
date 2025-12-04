# What is the problem?

You want to use your own importer in your application. Unfortunately, you don’t know how. So let’s try to help you here a little bit.
How to solve it

At first you need to write your own importer. There is a base class for this:

```cpp
class NewLoader final : public BaseImporter{
public:
  NewLoader() : BaseImporter() {}
  bool CanRead(const std::string &pFile,  IOSystem *pIOHandler, bool checkSig) const override { ... }

protected:
  void InternReadFile(const std::string &pFile, 
      aiScene *pScene, 
      IOSystem *pIOHandler) override { ... }
};
```
This implementation shall fulfill all the requiements to get a scene out of the loader. It shall contain all the intermediate data which is needed to do this job. You can check our documentation for that.

Last but not least you need to register your own loader to the importer instance of the Asset-Importer-Lib:
```cpp
Importer myImporter;
myImporter.RegisterLoader(new NewLoader);
```
And that is all.
