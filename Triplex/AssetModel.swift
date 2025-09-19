//
//  AssetModel.swift
//  Triplex
//
//  Created by Laurent Vincent on 08/09/2025.
//

import Foundation


class Asset: Hashable, CustomStringConvertible {
    private let values: [Int]
    
    // Initializer
    init(values: [Int]) {
        self.values = values
    }
    
    // Size
    var size: Int {
        return values.count
    }
    
    // Access by index
    func value(for position: Int) -> Int {
        return values[position]
    }
    
    // String representation
    var description: String {
        return values.map { String($0) }.joined(separator: "")
    }
    
    // Hashable
    func hash(into hasher: inout Hasher) {
        hasher.combine(description)
    }
    
    // Equatable
    static func == (lhs: Asset, rhs: Asset) -> Bool {
        return lhs.description == rhs.description
    }
}


struct AssetsFactory {
    
    static let shared = AssetsFactory()
    
    /*
     Exemple of criteria for a graphical representation of an asset:
        - color
        - form
        - quantity
        - drawing line
     */
    static let NB_CRITERIA_PER_ASSET: Int = 4
    
    /*
     Exemple of values for a previous criteria:
     - color => blue, red, green
     - form => duck, dog, elephant
     - quantity => 1, 2, 3)
     - drawing line => full, dashed1, dashed2

     Each criteria must have same number of possible values
     */
    static let NB_VALUES_PER_CRITERIA: Int = 3
    
    static let SUM1_3 = 6

    static let FACTO_3 = 6
    
    static let ROOT_3 = [0,1,8,27]
    
    /*
     Generate a asset matching with 2 assets
     */
    func generateMatchingAsset(first: Asset, second: Asset) -> Asset {
        var matchingAssetContent = Array<Int>(repeating: 0, count:AssetsFactory.NB_CRITERIA_PER_ASSET)
        
        for i in 0..<AssetsFactory.NB_CRITERIA_PER_ASSET {
            let v1 = first.value(for:i)
            let v2 = second.value(for:i)
            matchingAssetContent[i] = (v1 == v2 ? v1 : AssetsFactory.SUM1_3 - (v1 + v2))
        }
        return Asset(values:matchingAssetContent)
    }
    
    /*
     Generate a random asset
     */
    func generateRandomAsset() -> Asset {
        var randomContent: [Int] = []
        for _ in 0..<AssetsFactory.NB_CRITERIA_PER_ASSET {
            randomContent.append(Int.random(in: 1...AssetsFactory.NB_VALUES_PER_CRITERIA))
        }
        return Asset(values: randomContent)
    }
    
    
    /*
     Generate NB_VALUES_PER_CRITERIA matching assets with matchingLevel criteria in common
     */
    func generateMatchingAssets(matchingLevel: Int) -> [Asset] {
        guard ((matchingLevel >= 0) && (matchingLevel <= AssetsFactory.NB_CRITERIA_PER_ASSET)) else {
            fatalError("matchingLevel must be between 0 and \(AssetsFactory.NB_CRITERIA_PER_ASSET)")
        }

        let variantStartPosition = Int.random(in:0..<AssetsFactory.NB_CRITERIA_PER_ASSET)
        let variantIncPosition = Int.random(in:1..<(AssetsFactory.NB_CRITERIA_PER_ASSET-1))
        
        var tempAssetContent: [Int] = []
        for _ in 0..<AssetsFactory.NB_CRITERIA_PER_ASSET {
            tempAssetContent.append(Int.random(in: 1...AssetsFactory.NB_VALUES_PER_CRITERIA))
        }
        var result = [Asset(values:tempAssetContent)]

        for _ in 1...AssetsFactory.NB_VALUES_PER_CRITERIA {
            for j in 0..<(AssetsFactory.NB_CRITERIA_PER_ASSET-matchingLevel) {
                let pos = (variantStartPosition+j*variantIncPosition)%AssetsFactory.NB_CRITERIA_PER_ASSET
                tempAssetContent[pos] = (tempAssetContent[pos]+1)%AssetsFactory.NB_VALUES_PER_CRITERIA+1
            }
            result += [Asset(values:tempAssetContent)]
        }
        
        return result
    }

    /*
     Verify NB_VALUES_PER_CRITERIA assets are matching. Either each criteria value are identical or completly differents
     @return -1 if not match or n>0 if assets match, where n is the number of criteria with same value
     */
    func checkAssets(assets: [Asset]) -> Int {
        guard (assets.count == AssetsFactory.NB_VALUES_PER_CRITERIA) else { fatalError("checkAssets: wrong number of assets") }
        var matching_criteria=0
        
        for i in 0..<AssetsFactory.NB_CRITERIA_PER_ASSET {
            var prod:Int = 1
            for j in 0..<AssetsFactory.NB_VALUES_PER_CRITERIA {
                prod *= assets[j].value(for:i)
            }
            
            if (prod != AssetsFactory.FACTO_3) {
                if (prod == AssetsFactory.ROOT_3[assets[0].value(for: i)]){
                        matching_criteria += 1
                } else {
                    return -1
                }
            }
        }
        return matching_criteria
    }
}
