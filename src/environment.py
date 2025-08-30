class Environment:
    def __init__(self):
        # Arah dan Action yang mungkin diambil Agent
        self.direction = ('Utara', 'Timur', 'Selatan', 'Barat')
        
        # Board
        self.board = [[set() for _ in range(4)] for _ in range(4)]
        self.agentPos = [3, 0] # untuk posisi agen saat bergerak nantinya
        self.agentDirection = self.direction[0] # arah agen menuju (untuk move forward)

        # Kebutuhan Game
        self.poin = 0
        self.isEndGame = False
        self.isGrabGold = False
        self.agentClimbOut = False

        # Kebutuhan Sistem (Menampilkan semua urutan langkah yang diambil)
        self.stack = []

    def reset(self):
        # Reset semua status ke keadaan awal
        self.poin = 0
        self.isEndGame = False
        self.isGrabGold = False
        self.agentClimbOut = False
        self.stack = []

        self.board = [[set() for _ in range(4)] for _ in range(4)]
        self.agentPos = [3, 0]
        self.agentDirection = self.direction[0]
        
        # Element lain di Board sesuai Map
        self.board[3][0].add('A')
        self.board[1][1].add('G')
        self.board[1][0].add('W')
        self.board[0][3].add('P')
        self.board[1][2].add('P')
        self.board[3][2].add('P')
        
        # Stench
        self.board[2][0].add('S')
        self.board[0][0].add('S')
        self.board[1][1].add('S')
        
        # Breeze
        self.board[1][1].add('B')
        self.board[3][1].add('B')
        self.board[2][2].add('B')
        self.board[0][2].add('B')
        self.board[1][3].add('B')
        self.board[3][3].add('B')

        # Kembalikan state awal
        return self.getState(), 0, self.isEndGame
    
    def turnLeft(self):
        self.poin -= 1
        currIdx = self.direction.index(self.agentDirection)
        newIdx = (currIdx - 1) % 4
        self.agentDirection = self.direction[newIdx]
        
        self.checkEndGame()
    
    def turnRight(self):
        self.poin -= 1
        currIdx = self.direction.index(self.agentDirection)
        newIdx = (currIdx + 1) % 4
        self.agentDirection = self.direction[newIdx]

        self.checkEndGame()

    def moveForward(self):
        self.poin -= 1
        r, c = self.agentPos
        dr, dc = 0, 0
        
        if self.agentDirection == 'Utara':
            dr, dc = -1, 0
        elif self.agentDirection == 'Timur':
            dr, dc = 0, 1
        elif self.agentDirection == 'Selatan':
            dr, dc = 1, 0
        elif self.agentDirection == 'Barat':
            dr, dc = 0, -1
        
        newR, newC = r + dr, c + dc
        
        if 0 <= newR < 4 and 0 <= newC < 4:
            self.board[r][c].remove('A')
            self.agentPos = [newR, newC]
            self.board[newR][newC].add('A')

        self.checkEndGame()
    
    def grab(self):
        r, c = self.agentPos
        
        if not self.isGrabGold and 'G' in self.board[r][c]:
            self.isGrabGold = True
            self.board[r][c].remove('G')
            self.poin += 1000
            self.poin -= 1
        else:
            self.poin -= 2
            
        self.checkEndGame()

    def climb(self):
        r, c = self.agentPos
        
        if r == 3 and c == 0 & self.isGrabGold:
            self.isEndGame = True
            self.agentClimbOut = True
            self.poin -= 1
        else:
            self.poin -= 2
        
        self.checkEndGame()

    def getKnowledge(self):
        r, c = self.agentPos
        knowledge = set()
        if 'B' in self.board[r][c]:
            knowledge.add('Breeze')
        if 'S' in self.board[r][c]:
            knowledge.add('Stench')
        if 'G' in self.board[r][c]:
            knowledge.add('Glitter')
        return sorted(knowledge)

    def checkEndGame(self):
        r, c = self.agentPos
        
        if 'P' in self.board[r][c] or 'W' in self.board[r][c]:
            self.isEndGame = True
            self.poin -= 1000

    def getState(self):
        r, c = self.agentPos
        knowledge = self.getKnowledge()
        return (r, c, self.agentDirection, tuple(knowledge), self.isGrabGold)

    def step(self, action):
        old_poin = self.poin
        
        if action == "turnLeft":
            self.turnLeft()
        elif action == "turnRight":
            self.turnRight()
        elif action == "moveForward":
            self.moveForward()
        elif action == "grab":
            self.grab()
        elif action == "climb":
            self.climb()
        else:
            raise ValueError(f"Aksi tidak valid: {action}")
        
        # Tambahkan aksi ke stack
        self.stack.append(action)
        
        # Hitung reward
        reward = self.poin - old_poin
        
        # Ambil state baru
        nextState = self.getState()
        
        return nextState, reward, self.isEndGame

    def displayGrid(self):
        if self.stack:
            print(f"\n--- Aksi : {self.stack[-1]} ---")

        cell_width = 15
        
        def printDivider():
            print("+" + ("-" * (cell_width + 2) + "+") * 4)
        
        printDivider()
        
        for i in range(4):
            row_content = []
            for j in range(4):
                content = ', '.join((self.board[i][j]))
                if not content:
                    content = ' '
                row_content.append(f"| {content.center(cell_width)} ")
            
            print("".join(row_content) + "|")
            printDivider()
        
        print(f"Arah agen: {self.agentDirection}")
        print(f"Poin saat ini: {self.poin}")
        print(f"Emas sudah diambil: {self.isGrabGold}")
        print(f"Game berakhir: {self.isEndGame}")
        if self.isEndGame:
            if self.agentClimbOut and self.isGrabGold:
                print("Selamat! Anda berhasil menemukan emas dan keluar.")
            elif self.agentClimbOut and not self.isGrabGold:
                print("Game berakhir: Agen keluar sebelum mendapat emas")
            else:
                print("Game berakhir: Agen mati.")