# WTF: C++ Initialization Is Driving Me Crazy
## What Happened?
I finally took the time to clean up the public headers of the Open-Asset-Importer-Lib. Specifically, 
I opened each header, tidied things up, added missing documentation, and "simplified" a few constructors
where it made sense. I thought I hadn’t changed anything fundamental. Or so I believed. Then I ran the 
unit tests. Six tests failed immediately. But why?

## Deep Dive
I had moved some constructors that were already declared as default from the implementation file into the 
header. That looked like this:

From:

```cpp
.h:
class Foo {
public:
    Foo(); // trivial
};

.cpp:
Foo::Foo() = default;
```

wurde

```cpp
.h:
class Foo {
public:
    Foo() = default; // trivial
};
```
This didn’t cause any failing unit tests. Thankfully. So I kept digging through my pull request. And I found
another change. In the LineSplitter class, I had tweaked a small detail in the constructor. 

It went from this:

```cpp
AI_FORCE_INLINE LineSplitter::LineSplitter(StreamReaderLE& stream, bool skip_empty_lines, bool trim ) :
        mIdx(0),
        mCur(),
        mEnd(nullptr),
        mStream(stream),
        mSwallow(),
        mSkip_empty_lines(skip_empty_lines),
        mTrim(trim) {
    mCur.reserve(1024);
    mEnd = mCur.c_str() + 1024;
    operator++();
    mIdx = 0;
}
```

to this:

```cpp
AI_FORCE_INLINE LineSplitter::LineSplitter(StreamReaderLE& stream, bool skip_empty_lines, bool trim ) :
        mIdx(0),
        mCur(),
        mEnd(nullptr),
        mStream(stream),
        mSkip_empty_lines(skip_empty_lines),
        mTrim(trim) {
    mCur.reserve(1024);
    mEnd = mCur.c_str() + 1024;
    operator++();
    mIdx = 0;
}
```

The attribute mSwallow, which was supposed to take the default value, was now implicitly initialized. I expected no 
change in behavior. Boy, was I wrong! Instead of the expected default (false), it was now true. A bit of background 
on the LineSplitter class: It splits a text file into individual lines. If there’s an error, it throws an exception. 
The mSwallow attribute suppresses that exception. Since the default changed from false to true, all parsing tests that 
expected the exception to be thrown failed. So, I explicitly initialized it to false, and all tests passed again.

## But  ...
Why did the default value change when I removed the explicit initialization from the constructor? I expected nothing 
to change, but I was wrong. Lesson learned: Always make implicit assumptions explicit and easy to understand. Otherwise, 
the world will burn.
This behavior was observed with MSVC, g++, and clang++. There’s probably a reason in the C++ spec, but I spared myself 
the trouble of looking it up.