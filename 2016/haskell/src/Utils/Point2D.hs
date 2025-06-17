import Prelude hiding (sum)

data Point2D = Point2D { x :: Int, y:: Int }
    deriving (Eq, Read, Show)

instance Num Point2D where
    (Point2D x1 y1) + (Point2D x2 y2) = Point2D (x1 + x2) (y1 + y2)
    -- (Point2D x1 y1) - (Point2D x2 y2) = Point2D (x1 - x2) (y1 - y2)
    -- (Point2D x1 y1) * (Point2D x2 y2) = Point2D (x1 * x2) (y1 * y2)
