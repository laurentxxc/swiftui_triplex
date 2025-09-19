//
//  TriplexApp.swift
//  Triplex
//
//  Created by Laurent Vincent on 08/09/2025.
//

import SwiftUI

@main
struct TriplexApp: App {
    // UI scheme
    static let COLOR_BACK = Color.accentColor
    static let COLOR_FRONT = Color.orange.gradient
    static let COLOR_TEXT = Color.white
    
    var body: some Scene {
        let gb = GameBoardModel(nbAssets: 24)
        WindowGroup {
//            StartView()
            PlayView(gameBoard: gb).onAppear(){
                gb.startGame()
            }
        }
    }
}
