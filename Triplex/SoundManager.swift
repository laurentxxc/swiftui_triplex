//
//  SoundManager.swift
//  Triplex
//
//  Created by Laurent Vincent on 14/09/2025.
//

import AVFoundation

class SoundManager {
    static let shared = SoundManager()   // singleton
    private var player: AVAudioPlayer?
    
    private init() {}
    
    func playSound(_ name: String, withExtension ext: String = "mp3") {
        guard let url = Bundle.main.url(forResource: name, withExtension: ext) else {
            print("Sound file \(name).\(ext) not found")
            return
        }
        
        do {
            player = try AVAudioPlayer(contentsOf: url)
            player?.prepareToPlay()
            player?.play()
        } catch {
            print("Error playing sound: \(error.localizedDescription)")
        }
    }
    
    func stop() {
        player?.stop()
    }
}
