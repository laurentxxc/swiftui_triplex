//
//  GameBoardModel.swift
//  Triplex
//
//  Created by Laurent Vincent on 09/09/2025.
//

import Foundation
import SwiftUI
import Combine // needed for Timer usage
import AVFoundation

enum GameState {
    case not_started
    case running
    case paused
}

class GameBoardModel: ObservableObject {
    private let nbAssets: Int
    private let isTest: Bool
    @Published var assets:[Asset] = []
    @Published var markedAssets:[Int:Asset] = [:]
    @Published var score:Int = 0
    @Published var bestScore:Int = 0
    @Published var gameState:GameState = .not_started
    @Published var lastMarkedAssets: [Int:Asset] = [:]
    @Published var lastAssetPoints: Int = 0
    
    private var timer: AnyCancellable?
    private var audioPlayer: AVAudioPlayer?
    
    @Published var timeRemaining:Int = 180
    
    let MAX_TIME = 180
    let SCORE_PENALTY = -1
    let SCORE_BONUS = 1
    let TIME_EXTRA = 10
    
    init (nbAssets: Int, isTest: Bool = false) {
        self.nbAssets = nbAssets
        self.isTest = isTest
        initBoardAssets()
    }
    
    func initBoardAssets() {
        guard isTest == false else {
            assets = Array(repeating: Asset(values: [1,1,1,1]), count: nbAssets)
            return
        }
        
        let nbMatchingAssets = nbAssets / 2
        var fillidx = 0
        
        // start filling with matchin asset
        while ( fillidx < nbMatchingAssets ) {
            assets += AssetsFactory.shared.generateMatchingAssets(matchingLevel: 3)
            fillidx += AssetsFactory.NB_VALUES_PER_CRITERIA
        }
        
        // complet with random asset
        while ( fillidx < nbAssets) {
            assets.append(AssetsFactory.shared.generateRandomAsset())
            fillidx += 1
        }
        
        assets.shuffle()
    }

    func valueAt(pos:Int) -> String {
        guard pos >= 0 && pos < nbAssets else {
            fatalError("Position \(pos) out of bounds")
        }
        return assets[pos].description
    }
    
    func assetTap(pos:Int) {
        guard (pos >= 0 && pos < nbAssets) else {
            fatalError( "Position \(pos) out of bounds" )
        }
        
        if !isAssetMarked(pos: pos) {
            markedAssets[pos] = assets[pos]
        } else {
            markedAssets.removeValue(forKey: pos)
        }
        
        if markedAssets.count == AssetsFactory.NB_VALUES_PER_CRITERIA {
            let matchinglevel = AssetsFactory.shared.checkAssets(assets: [Asset](markedAssets.values))
            // keeping last marked assets
            lastMarkedAssets = markedAssets
            
            if (matchinglevel<0) {
                // assets are not matching
                lastAssetPoints = SCORE_PENALTY
                addToScore(value:lastAssetPoints*3)
                
                // play wrong sound
                SoundManager.shared.playSound("wrong")
                
            } else {
                // assets are matching
                // won points = <base score> * <number of diff criteria on the match assets> * number of assets
                lastAssetPoints = SCORE_BONUS * (markedAssets.count + 1 - matchinglevel)
                addToScore(value: lastAssetPoints  * markedAssets.count)
                timeRemaining += TIME_EXTRA
                
                //play good sound
                SoundManager.shared.playSound("good")

                //replace marked assets with new ones
                // collect marked assets keys
                // capture which tiles matched so the view can animate them
                let indexes:[Int] = markedAssets.keys.shuffled()

                // generated random assets for each index except last one
                for i in 0..<(indexes.count-1) {
                    assets[indexes[i]] = AssetsFactory.shared.generateRandomAsset()
                }
                
                // for last one generate a matching asset with 2 others form the board randomly selected
                let i_a3:Int = indexes[indexes.count-1]
                var i_a1 = 0, i_a2 = 0
                
                repeat { i_a1 = Int.random(in: 0..<nbAssets)}
                while (i_a1 == i_a3)
                
                repeat { i_a2 = Int.random(in: 0..<nbAssets)}
                while (i_a2 == i_a3) && (i_a2 == i_a1)
                
                    assets[i_a3] = AssetsFactory.shared.generateMatchingAsset(first: assets[i_a1], second: assets[i_a2])
            }

            // clear after a short delay so the animation can play
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) { [weak self] in
                self?.lastMarkedAssets = [:]
                self?.lastAssetPoints = 0
            }
            
            //reset all mark
            markedAssets.removeAll()
        }
    }
    
    // updare score and best score also if needed
    private func addToScore(value:Int){
        score += value
        if score > bestScore {
            bestScore = score
        }
    }
    
    private func startTimer() {
        timer = Timer.publish(every: 1, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                guard let self = self else { return }
                self.timeRemaining += -1
                
                if self.timeRemaining <= 0 {
                    //game over
                    self.stopGame()
                    SoundManager.shared.playSound("end")
                }
            }
    }
    
    func startGame(){
        // kill timer if already exist
        timer?.cancel()
        timeRemaining = MAX_TIME
        score = 0
        gameState = .running
        markedAssets = [:]
        lastMarkedAssets = [:]
        lastAssetPoints = 0
        startTimer()
    }
    
    func pauseGame(){
        guard gameState == .running else { return }
        gameState = .paused
        timer?.cancel()
    }
    
    func stopGame(){
        gameState = .not_started
        timer?.cancel()
    }
 
    func resumeGame(){
        guard gameState == .paused else { return }
        gameState = .running
        startTimer()
    }
    
    func isAssetMarked(pos:Int) -> Bool {
        return markedAssets[pos] != nil
    }
    
}
