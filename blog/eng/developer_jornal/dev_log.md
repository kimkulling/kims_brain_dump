# My developer journal
## 07-05-2025
- Using vcpkg, SDL2 and Vulkan is more complicated than expected. I tried to load all the needed vulkan-libs and render a simple triangle. To optimize
  the way to set it up I installes SDL2 and volk by using vcpkg. unfortunately, nothing worked. The SLS2-stuff told me that the co9nfiguration of the
  Vulkan loading was not successful. Volks initialization calls told me: We are fine. My impacient told me to kill them all. But I didn't listening to them.
## 07-04-2025
- I took a look onto my old fe-solver for beam structures. I want to have it in a working state again.
## 07-01-2025
- The new concept for strings in my cppcore library (see https://github.com/kimkulling/cppcore) is ready for merging. IN this moment the features are not
  too bad:
  - Small string representation on the stack to avoid allocations during construction
  - Fast string comparison by hash checks instead of deep checks
  - I have introduced a string view class
- The assimp library is now part of the bazel registry: https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/assimp
## 06-27-2025
- I searched for good ways to structurized a new vulkan renderer. In special I was interested how to run it: in the main thread or in a separate
  render thread. I am still investigating this question. I guess toing this decision is not so easy, because there are a lot of between thread
  concepts I haven't evaluated until now. And I want to avoid to do the same mistaakes as I did in my OSRE.
## ß6-25-2025
- I worked on a PR (thanks to https://github.com/HandsomeXi) fixing memory leaks in the texture transform post-processing step. I tried to optimize
  his solution and I failed. He just used a copy-constructed unique-ptr from the STL. I tried the make_unique and failed to deduct the currect type.
- Always try to make things better can make things much buggier.

## 06-24-2025
- I optimized the GeometricTools. I have avoided some possible crashes.
- Maybe I should try to used SIMD stuff on the assimp vector arithmetics.
  
## 06-20-2025
- Sometimes it makes sense to rethink all the stuff you have done in the past. Currently I am rethinking the way my old renderer in the OSRE works.
  My plan was to have a separate renderthread and push all the new stuff from the main thread to the new one. So far so good. But with the time I
  recognized that when creating a renderer in a separate thread you need to set it up from your main thread. Getting it up means creating an
  interface on the main thread side and push all the data to the backend side. After the years this has basicly doubled all
  interfaces - in both threads.

## 06-19-2025
- I fixed some minor things in my cppcore lib. Mostly upper/lowercase issues
- The way I wrote the string class seems to be wrong because I never used it.
  
## 06-12-2025
- I took a deeper look inside the initial allocations in the OSRE. Most of them are done by Constant Strings using a std::string.
  I guess I should replace them by a null-terminated constexpr char array. And all the shader code are stored in static
  std::strings. Not the best idea for buildin shaders.
  
## 06-11-2025
- I played a little bit with the debug renderer in the OSRE. As usual I was not able to concentrate on a
  dedicated fix ... in the beginning. At the end I recognized: I introduced a render path interface, I
  used it to implement the Canvas-renderer. But I missed the point when any kind of instance or service
  iterates through all the different renderpaths to ensure that their rendering gets performed during the frame update.
  I guess I need to add this.

## 06-10-2025
- The documentation for the **Asset-Importer-Doc** got an update to **v6.0.2**
  
## 06-09-2025
- I prepared the installer for the **Asset-Importer-SDK**. it is now available on itchi.io.

## 06-08-2025
- The **Asset-Importer-Lib v6.0.2** is out. And I adapted all my homes in the internet.

## 06-07-2025
- I tried to fix the update of the pugixml dependency in assimp. If you want to do the same some findings from me:
  - They have added a cpp file, add this to you build environment. The old way will not work anymore.
  - You need to enable the export for dlls on windows manually, but you need to take case if you are using windows or not.
    Check the config header for this:

```cpp
#ifdef _WIN32
#   define PUGIXML_API __declspec(dllexport) // to export all public symbols from DLL
#else
#  define PUGIXML_API __attribute__((visibility("default")))
#endif // _WIN32
```

- I started to integrate the freetype lib as a workaroud in my OSRE renderer. I want to be able to provide a simple UI for
  importing assets. Unfortunately putting an image or a text onto my button stiil does not work
- I installed Unreal-Engine for the first time. It is such a biiiiiig project ...

## 06-06-2025
- I closed the rework on the Canvas-elements - it broke the 2D rendering and I was too excausted to start debugging - maybe not the best decision
- I start to fix the Debug-Renderer in the OSRE

## 06-04-2025
- I made some refactorings in the CanvasRenderer in the OSRE-Repo
- The main page of the Open-Collective page got an update
  
## 06-03-2025
- I wrote my first Scratch allocator, which can be used for all kind of classes by using implplacement new / deletes.
- Today I tried the google library benchmark to play with performance tests in assimp.

## 06-02-2025
- I fixed the version issue in the Asset-Importer-Lib
  
## 05-31-2025
- I released 6.0.0 of the Asset-Importer-Lib and I have forgotten to increase the versions ... again.

## 05-27-2025
- Today I need to deal with fixing a lot of approval documentation for my day job. This takes time and is not always fun.
- I try to move the Uri implementation of my playground engine OSRE to use enums instead of strings. Make the whole code more verbose.
