//
//  PlayView.swift
//  Triplex
//
//  Created by Laurent Vincent on 08/09/2025.
//

import SwiftUI

struct PlayView: View {
    // @StateObject to be used when view is creating GameBoardModel otherwise @ObservedObject must be used
    @ObservedObject var gameBoard : GameBoardModel
    
    // For representation of asset as a text tile
    /* asset.value(for: 0) */ private let SYMBOLS = ["⚑","♛","⚽︎"]
    /* asset.value(for: 1) */ private let ASSET_FONT_SIZES:[CGFloat] = [60, 40, 30]
    /* asset.value(for: 2) */ private let ASSET_BACK_STYLES = [Color("bg_1"), Color("bg_2"), Color("bg_3")]
    /* asset.value(for: 3) */ private let ASSET_FRONT_STYLES = [Color("fg_1"), Color("fg_2"), Color("fg_3")]
    
    var body: some View {
        VStack{
            HStack(){
                Capsule()
                    .frame(height:55)
                    .foregroundStyle(Color("BackPanelColor").gradient)
                    .overlay(alignment: .trailing){
                        Text("\(gameBoard.score)")
                            .font(.title)
                            .foregroundColor(Color.accentColor)
                            .padding([.top, .trailing], 10)
                        
                    }.overlay(alignment:.leading){
                        Text("Current")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(Color("AccentColor"))
                            .padding(.leading, 6.0)
                    }
                Image(systemName: "trophy.fill")
                    .foregroundStyle(Color.accentColor)
                    .font(.title)
                
                Capsule()
                    .frame(height:55)
                    .foregroundStyle(Color("BackPanelColor").gradient)
                    .overlay(alignment: .leading){
                        Text("\(gameBoard.bestScore)")
                            .font(.title)
                            .foregroundColor(Color.accentColor)
                            .padding([.top, .leading], 10)
                        
                    }.overlay(alignment: .trailing){
                        Text("Best")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(Color("AccentColor"))
                            .padding(.trailing, 6.0)
                    }
            }
            
            
            Spacer()
            
            HStack {
                TimerView(gameBoard: gameBoard)
                Image(systemName: "clock.fill")
                    .foregroundStyle(Color.accentColor.gradient)
                    .font(.title)
            }.frame(maxHeight:40)
            
            Spacer()
            
            let cols = Array(repeating: GridItem(.flexible()), count: 4)
            
            LazyVGrid(columns: cols, content: {
                ForEach(0..<24) { i in
                    let a = gameBoard.assets[i]
                    Button(action:{
                        guard gameBoard.gameState == .running else { return }
                        gameBoard.assetTap(pos: i)
                    }, label: {
                        //                            Image("\(gameBoard.valueAt(pos: i))")
                        //                                .resizable()
                        //                                .aspectRatio(contentMode: .fit)
                        
                        Text(convertText(asset:gameBoard.assets[i]))
                            .frame(width:80, height:80)
                            .background(ASSET_BACK_STYLES[a.value(for:3)-1].gradient)
                            .cornerRadius(10)
                            .font(.system(size: ASSET_FONT_SIZES[a.value(for: 1)-1]))
                            .foregroundColor(ASSET_FRONT_STYLES[a.value(for: 2)-1])
                            .colorInvertIf(gameBoard.lastMarkedAssets.keys.contains(i) && gameBoard.lastAssetPoints < 0)
                    })
                    .overlay(
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(Color.accentColor, lineWidth: gameBoard.isAssetMarked(pos: i) ||  gameBoard.lastMarkedAssets.keys.contains(i) ? 5 : 0)
                    )
                    .scaleEffect(gameBoard.lastMarkedAssets.keys.contains(i) && gameBoard.lastAssetPoints >= 0 ? 0.8 : 1)
                    .opacity(gameBoard.lastMarkedAssets.keys.contains(i) && gameBoard.lastAssetPoints >= 0 ? 0.10 : 1.0)
                    .overlay(alignment: .center) {
                        if (gameBoard.lastMarkedAssets.keys.contains(i) && gameBoard.lastAssetPoints >= 0) {
                            Text("+\(gameBoard.lastAssetPoints)")
                                .font(.title)
                                .fontWeight(.heavy)
                                .foregroundStyle(Color("AccentColor"))
                        }
                    }
                    .animation(.easeOut(duration: 0.2), value: gameBoard.lastMarkedAssets)
                }
            })
            .padding(10)
            .opacity(getOpacity(state: gameBoard.gameState))
            .overlay(alignment: .center) {
                if gameBoard.gameState == .paused {
                    Text("Your game is paused ")
                        .font(.title)
                        .fontWeight(.heavy)
                        .foregroundColor(Color("AccentColor"))
                } else if gameBoard.gameState == .not_started {
                    Text("Your score is \(gameBoard.score). \nTap to start a new game")
                        .font(.title)
                        .fontWeight(.heavy)
                        .foregroundColor(Color("AccentColor"))
                }
            }
            
            Spacer()
            
            Button(action: {
                switch gameBoard.gameState {
                case .not_started:
                    gameBoard.startGame()
                case .running:
                    gameBoard.pauseGame()
                case .paused:
                    gameBoard.resumeGame()
                }
                
            },label: {
                HStack{
                    Image(systemName: getButtonLogo(state: gameBoard.gameState))
                        .font(.title)
                        .foregroundStyle(Color.white)
                    Text(getButtonText(state: gameBoard.gameState))
                        .foregroundStyle(Color.white)
                        .font(.title)
                        .frame(width:200)
                    
                }.padding(10)
            }
            )
            .background(Color.accentColor.gradient)
            .cornerRadius(20)
        }
        .padding(20)
        .background(Color("BackPanelColor"))
    }
    
    private func getOpacity(state: GameState)-> Double{
        switch state {
        case .not_started:
            return 0.2
        case .paused:
            return 0
        case .running:
            return 1
        }
    }
    
    private func getButtonLogo(state: GameState) -> String{
        switch state {
        case .not_started:
            return "play.fill"
        case .running:
            return "pause.fill"
        case .paused:
            return "play.fill"
        }
    }
    
    private func getButtonText(state: GameState) -> String {
        switch state {
        case .not_started:
            return "Start"
        case .running:
            return "Pause"
        case .paused:
            return "Resume"
        }
    }
    
    func convertText(asset: Asset) -> String {
        var res = ""
        for _ in 1...asset.value(for:1) {res.append(SYMBOLS[asset.value(for: 0)-1]) }
        return res
    }
}


#Preview {
    let gb = GameBoardModel(nbAssets: 24, isTest: true)
    PlayView(gameBoard: gb).onAppear(){gb.startGame()}
//        .preferredColorScheme(.dark) // forces dark mode
}

extension View {
    @ViewBuilder
    func colorInvertIf(_ condition: Bool) -> some View {
        if condition {
            self.colorInvert()
        } else {
            self
        }
    }
}
