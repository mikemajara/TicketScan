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
- 🔋 Loaders
  - [danilowoz/react-content-loader](https://github.com/danilowoz/react-content-loader). Contetn Loader for ticket list in future.
  - [joinspontaneous/react-native-loading-spinner-overlay](https://github.com/joinspontaneous/react-native-loading-spinner-overlay)
    - Too bad that they have to recommend an [implementation](https://github.com/joinspontaneous/react-native-loading-spinner-overlay#recommended-implementation) Probably buggy. Discarded
  - This [code snippet](https://medium.com/@kelleyannerose/react-native-activityindicator-for-a-quick-easy-loading-animation-593c06c044dc) did the trick. [Kelly Rose](https://medium.com/@kelleyannerose) might have some more stuff to show 😏. For the moment taking a basic component as loader in the project (as of Saturday, 05 Oct 2019 18:18)
  - [oblador/react-native-progress](https://github.com/oblador/react-native-progress) **Not checked** but might be useful for the future.

- Typescript
  - ♻️ Generics in Typescript
    - [ErickWendel/generic-repository-nodejs-typescript-article](https://github.com/ErickWendel/generic-repository-nodejs-typescript-article)
  - [Stop Manually Assigning TypeScript Constructor Parameters](https://www.stevefenton.co.uk/2013/04/stop-manually-assigning-typescript-constructor-parameters/)
  - [Constructor overload in Typescript](https://stackoverflow.com/questions/12702548/constructor-overload-in-typescript)

- Hooks
  - `useState` is asynchronous, for callback use `useEffect`. Check [here](https://www.robinwieruch.de/react-usestate-callback) for an example.
  - Re-rendering works better if we touch the least part of the code. So less frames are dropped if we use separate `useState` for two different parts of a same object. (No precise measure here, but could be benchmarked).
  Find an example below:
    ```
    const [ticket, setTicket] = useState(props.navigation.getParam('ticket', null));
    const [lines, setlines] = useState(ticket.lines);
    ```

### 🧩 Used Components

- [react-native-typography](https://github.com/hectahertz/react-native-typography)
- [react-native-elements](https://react-native-training.github.io/react-native-elements/)
- [antonKalinin/react-native-image-view](https://github.com/antonKalinin/react-native-image-view)
  - Excluded. Broken from upgrade to 0.61.2

## Troubleshooting & Known issues

- After upgrade of react native (0.60.x -> 0.61.2) a lot of things went wrong.
Some were fixed using parts of the new templates for a new project which can be found here (all under `<project-directory>/node_modules/react-native/template`)
  - `_flowconfig`
  - `_gitignore`
  - `android/app/build.gradle`
  - `android/app/src/main/java/com/helloworld/MainActivity.java`
  - `android/app/src/main/java/com/helloworld/MainApplication.java`
  - `android/build.gradle`
  - `android/gradle/wrapper/gradle-wrapper.properties`
  - `ios/HelloWorld/Images.xcassets/AppIcon.appiconset/Contents.json`
  - `ios/HelloWorld/Info.plist`
  - `ios/HelloWorld.xcodeproj/project.pbxproj`
  - `ios/HelloWorldTests/HelloWorldTests.m`
  - `ios/Podfile`
  - `package.json`

