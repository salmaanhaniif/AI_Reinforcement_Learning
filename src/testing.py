import environment as env
# Testing
game = env.Environment()
game.reset()
game.displayGrid()
game.step("moveForward") # Agen bergerak ke atas
game.displayGrid()


game.step("turnRight") # Agen berputar
game.displayGrid()

game.step("moveForward")
game.displayGrid()


game.step("turnLeft") # Agen berputar
game.displayGrid()

game.step("moveForward")
game.displayGrid()

game.step("grab")
game.displayGrid()

game.step("turnLeft")
game.displayGrid()

game.step("turnLeft")
game.displayGrid()

game.step("moveForward")
game.displayGrid()

game.step("moveForward")
game.displayGrid()

game.step("turnRight")
game.displayGrid()

game.step("moveForward")
game.displayGrid()

game.step("climb")
game.displayGrid()