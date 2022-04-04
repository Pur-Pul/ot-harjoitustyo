```mermaid
  classDiagram
        Game "1" --> "2" Dice
        Game "1" --> "1" Board
        Game "1" --> "2..8" Player
        Board "1" --> "40" Square
        Square "1" --> "1" Square
        Player "1" --> "1" PlayerPiece
        PlayerPiece "*" --> "1" Square
```
