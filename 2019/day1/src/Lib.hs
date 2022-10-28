module Lib
    ( moduleFuelCalc,
      moduleFuelFuelCalc
    ) where

import Data.List

-- Fuel required to launch a given module is based on its mass. 
-- Specifically, to find the fuel required for a module, 
-- take its mass, divide by three, round down, and subtract 2.
moduleFuelCalc :: Int -> Int
moduleFuelCalc x =
    (x `div` 3) - 2

-- Fuel itself requires fuel just like a module
-- take its mass, divide by three, round down, and subtract 2. 
-- However, that fuel also requires fuel, and that fuel requires fuel, and so on.
-- Any mass that would require negative fuel should instead be treated as if it requires zero fuel; 
-- the remaining mass, if any, is instead handled by wishing really hard,
-- which has no mass and is outside the scope of this calculation.
moduleFuelFuelCalc :: Int -> Int
moduleFuelFuelCalc =
    sum . takeWhile (>0) . iterate (\x -> (x `div` 3) - 2)