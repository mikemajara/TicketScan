# Ticket Scan App

[Trello Board](https://trello.com/b/aBXyLQaO/ticketscan)

## Naming convention

**BEGIN_TODO**
> _"I call them Container and Presentational components but I also heard Fat and Skinny, Smart and Dumb, Stateful and Pure, Screens and Components, etc"_

- `[Name][View?]Container` - for all _smart_ components (containers).
- `[Name]View` - for all _dumb_ components (components)

Prefer to set parents as containers, the rest as views (or pure components)
**END_TODO**

## Links 🔗 & Libraries 📚

- [react-native-vector-icons directory](https://oblador.github.io/react-native-vector-icons/)
- [Fonts From Mac OS X Included With iPhone](https://daringfireball.net/misc/2007/07/iphone-osx-fonts)

- 🖼 Pictures
  - [ascoders/react-native-image-viewer](https://github.com/ascoders/react-native-image-viewer#readme) <- considering.
    - Considering
    - Dependance on [ascoders/react-native-image-zoom](https://github.com/ascoders/react-native-image-zoom)
    - Try frist this one^^^ asuming its the base for the one above.
  - [ascoders/react-native-image-zoom](https://github.com/ascoders/react-native-image-zoom)
    - Not convincing.
    - Tension on borders not working well.
    - Need to check for fading on close of modal...
    - Designed for an image carousel (we just need one picture for the moment)
  - [antonKalinin/react-native-image-view](https://github.com/antonKalinin/react-native-image-view)
    - Sticking to this one
    - Simple enough
    - No extra Modal needed
    - Issues found
      - Image freezes depending on swipe from some corners
      - width/height breaks swipeToClose
        - When image's props specified swipe does not work
        - Somehow specifying different values... (those of device instead of pixels?) it works better.
      - To disable close button in controls, `close` must take `null` value instead of `false` (as `next` and `prev` do), which is counterintuitive.

### 🧩 Components

- [React Native Elements](https://github.com/react-native-training/react-native-elements) _Included_
- [react-native-typography](https://github.com/hectahertz/react-native-typography) _Included_
- [react-native-elements](https://react-native-training.github.io/react-native-elements/) _Included_

## Troubleshooting & Known issues


