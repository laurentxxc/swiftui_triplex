//
//  ContentView.swift
//  Triplex
//
//  Created by Laurent Vincent on 08/09/2025.
//

import SwiftUI


enum PlayMode: String, CaseIterable, Identifiable {
    case single,dual
    var id: Self {self}
}

enum TimeMode: String, CaseIterable, Identifiable {
    case falling_clock,fast_100
    var id:Self {self}
}

struct StartView: View {
    @State private var playMode: PlayMode = .single
    @State private var timeMode: TimeMode = .falling_clock

    var body: some View {
        VStack {
            Text("Triplex © lvt")
                .font(.system(size: 30, weight: .bold))
            Spacer()
            
            Text("Player Mode")
            Picker("Player Mode",selection: $playMode){
                Text("Single").tag(PlayMode.single)
                Text("Dual").tag(PlayMode.dual)
            }
            .pickerStyle(.segmented)
            
            Text("Time Mode")
            Picker("Time Mode", selection: $timeMode){
                Text("Falling clock").tag(TimeMode.falling_clock)
                Text("Fast to 100").tag(TimeMode.fast_100)
            }
            .pickerStyle(.segmented)

            
            Spacer()
            Button( action: {
                // TBD
            },
                    label: {
                Text("Let's play!")
                    .frame(width:200, height: 50)
                    .background(.blue)
                    .font(.system(size:20,weight: .bold))
                    .foregroundColor(.white)
                    .clipShape(.capsule)
            })
        }
        .padding()
    }
}

#Preview {
    StartView()
}
