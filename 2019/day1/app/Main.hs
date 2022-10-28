module Main where

import System.Environment
import Lib (moduleFuelCalc, moduleFuelFuelCalc)

main :: IO ()
main = do
    filename <- fmap head getArgs
    f <- readFile filename
    let ints = read <$> lines f :: [Int]
    print $ sum $ moduleFuelFuelCalc . moduleFuelCalc <$> ints 
