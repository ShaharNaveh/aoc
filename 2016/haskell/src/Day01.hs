import Utils ( readInputFile, split )

--import Data.List.Split


main :: IO ()
main = do
    input <- readInputFile
    print $ split ", " input
    --print $ splitOn ", " input
    --print $ p1 input

{-
p1 :: [String] -> Int
p1 input =
    return (splitOn ", " input)
-}
    
	
