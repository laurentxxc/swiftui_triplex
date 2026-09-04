# Triplex

**This project is now archived. See [Project Closure](#project-closure) section.**

A SwiftUI puzzle game for iOS, iPadOS, and macOS. Match sets of three tiles that either share all criteria or differ completely across multiple attributes.

## Gameplay

- The board displays 24 tiles, each defined by 4 criteria with 3 possible values
- Select tiles in groups of 3 and submit a match
- A valid match means the three tiles are either **all the same** or **all different** for every criterion
- Correct matches earn points and bonus time; incorrect matches incur a penalty
- A 180-second timer counts down — clear as many sets as you can before time runs out

## Platforms

- iOS 18.5+
- iPadOS 18.5+
- macOS 15.5+

## Requirements

- Xcode 16.4+
- Swift 5.0+

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/laurentxxc/swiftui_triplex.git
   ```
2. Open `Triplex.xcodeproj` in Xcode
3. Select a destination and run

## Features

- Pattern-matching puzzle with 4 criteria per tile
- Score tracking with local best-score persistence
- Optional iCloud sync for best scores
- Sound effects for matches, mismatches, and game over
- Localized in English and French

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Project Closure

I originally created this game to experience how good Xcode and SwiftUI are for development.
Both are great and provide a very nice developer experience, however I found the following limitations I was not fully satisfied with:
* Without paying for an Apple Developer license, I can only deploy the game for a few weeks on my iPhone.
* Obviously you can't target Android devices with this (so forget sharing this app with friends not using iPhone/iPad/Mac).

A few weeks after the first working releases, I decided to look for another language/workbench/deployment environment to pursue my development where I would be able to:
* Get a similar developer experience (nice language, nice workbench)
* Target both Android and iOS devices
* Implement a nice CI/CD workflow (e.g. with one commit I can trigger tests + code building + app deployment)

I finally decided to rewrite this project using Flutter/Dart + VS Code + Vercel in order to deploy Triplex as an HTML application. This new project is on the [flutter_triplex](https://github.com/laurentxxc/flutter_triplex) repo.

[swiftui_triplex](https://github.com/laurentxxc/swiftui_triplex) is now archived. It can still be accessed in read-only but I won't work on it.
