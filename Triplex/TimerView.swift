//
//  TimerView.swift
//  Triplex
//
//  Created by Laurent Vincent on 11/09/2025.
//

import SwiftUI

struct TimerView: View {
    @ObservedObject var gameBoard: GameBoardModel

    var body: some View {
        GeometryReader { geometry in
            ZStack (alignment: .leading){
                Capsule()
                    .frame(height:40)
                    .foregroundStyle(Color("BackPanelColor").gradient)
                
                Capsule(style:.continuous)
                    .frame(width: geometry.size.width * progress,
                           height:40)
                    .foregroundStyle(Color.accentColor.gradient)
            }
            .background(Color.accentColor)
                .overlay(alignment: .trailing){
                    Text("\(gameBoard.timeRemaining)s")
                        .font(.title)
                        .padding(.trailing, 20)
                        .foregroundStyle((1-progress)*geometry.size.width >= 80 ? Color.accentColor : Color.white)
                }
                .clipShape(.capsule)
        }
    }
    
    private var progress: CGFloat {
        guard gameBoard.timeRemaining < gameBoard.MAX_TIME else { return 1 }
        return CGFloat(gameBoard.timeRemaining) / CGFloat(gameBoard.MAX_TIME)
    }
}

#Preview {
    TimerView(gameBoard: GameBoardModel(nbAssets: 24))
}
