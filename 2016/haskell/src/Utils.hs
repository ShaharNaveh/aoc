module Utils ( 
    getInputFileName
    , readInputFile
    , split
    , splitString
    ) where

import Data.Char (isSpace)
import Data.List (dropWhileEnd)
import System.Environment (getArgs, getProgName)

getInputFileName :: IO String
getInputFileName = do
    args <- getArgs
    progName <- getProgName
    let baseName = case args of
            (x:_) -> x
            []    -> progName
    return $ "input/" ++ baseName ++ ".txt"


readInputFile :: IO String
readInputFile = dropWhileEnd isSpace <$> (getInputFileName >>= readFile)


split [] wordAcc wordsAcc _ = wordsAcc ++ [wordAcc]
split (x:xs) wordAcc wordsAcc sep
  | x == sep  = split xs [] (wordsAcc ++ [wordAcc]) sep
    | otherwise = split xs (wordAcc ++ [x]) wordsAcc sep

splitString :: Char -> [Char] -> [[Char]]
splitString _ [] = []
splitString sep str = 
    let (left, right) = break (==sep) str 
    in left : splitString sep (drop 1 right)
