# My developer journal
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
- 
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
