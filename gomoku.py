#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五子棋游戏 (Gomoku Game)
一个简单的命令行五子棋游戏实现
"""

import os
import sys

class GomokuBoard:
    """五子棋棋盘类"""
    
    def __init__(self, size=15):
        """
        初始化棋盘
        :param size: 棋盘大小，默认15x15
        """
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1  # 1为黑棋，2为白棋
        self.move_history = []
        
    def display_board(self):
        """显示当前棋盘状态"""
        print("\n  ", end="")
        # 打印列号
        for i in range(self.size):
            print(f"{i:2d}", end=" ")
        print()
        
        # 打印棋盘
        for i in range(self.size):
            print(f"{i:2d} ", end="")
            for j in range(self.size):
                if self.board[i][j] == 0:
                    print(" ·", end=" ")
                elif self.board[i][j] == 1:
                    print(" ●", end=" ")  # 黑棋
                else:
                    print(" ○", end=" ")  # 白棋
            print()
        print()
    
    def is_valid_move(self, row, col):
        """
        检查下棋位置是否有效
        :param row: 行号
        :param col: 列号
        :return: 布尔值
        """
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.board[row][col] == 0)
    
    def make_move(self, row, col):
        """
        下棋
        :param row: 行号
        :param col: 列号
        :return: 是否成功下棋
        """
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.move_history.append((row, col, self.current_player))
            return True
        return False
    
    def check_winner(self, row, col):
        """
        检查是否有玩家获胜
        :param row: 最后一步的行号
        :param col: 最后一步的列号
        :return: 获胜玩家编号，0表示无人获胜
        """
        player = self.board[row][col]
        directions = [
            (0, 1),   # 水平
            (1, 0),   # 垂直
            (1, 1),   # 右斜线
            (1, -1)   # 左斜线
        ]
        
        for dx, dy in directions:
            count = 1  # 包含当前棋子
            
            # 向正方向检查
            r, c = row + dx, col + dy
            while (0 <= r < self.size and 0 <= c < self.size and 
                   self.board[r][c] == player):
                count += 1
                r, c = r + dx, c + dy
            
            # 向反方向检查
            r, c = row - dx, col - dy
            while (0 <= r < self.size and 0 <= c < self.size and 
                   self.board[r][c] == player):
                count += 1
                r, c = r - dx, c - dy
            
            # 如果连成5子则获胜
            if count >= 5:
                return player
        
        return 0
    
    def is_board_full(self):
        """检查棋盘是否已满"""
        for row in self.board:
            if 0 in row:
                return False
        return True
    
    def switch_player(self):
        """切换当前玩家"""
        self.current_player = 3 - self.current_player  # 1变2，2变1
    
    def get_current_player_name(self):
        """获取当前玩家名称"""
        return "黑棋" if self.current_player == 1 else "白棋"
    
    def get_player_symbol(self):
        """获取当前玩家符号"""
        return "●" if self.current_player == 1 else "○"


class GomokuGame:
    """五子棋游戏类"""
    
    def __init__(self, board_size=15):
        """
        初始化游戏
        :param board_size: 棋盘大小
        """
        self.board = GomokuBoard(board_size)
        self.winner = 0
        self.game_over = False
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_game_info(self):
        """显示游戏信息"""
        print("=" * 50)
        print("            五子棋游戏 (Gomoku)")
        print("=" * 50)
        print("游戏规则：")
        print("1. 黑棋先行，双方轮流下棋")
        print("2. 率先连成5子的一方获胜")
        print("3. 输入坐标格式：行号 列号 (例如：7 7)")
        print("4. 输入 'quit' 退出游戏")
        print("=" * 50)
    
    def get_move_input(self):
        """
        获取玩家输入
        :return: (row, col) 或 None (退出游戏)
        """
        while True:
            try:
                user_input = input(f"请输入 {self.board.get_current_player_name()}({self.board.get_player_symbol()}) 的下棋位置 (行 列): ").strip()
                
                if user_input.lower() == 'quit':
                    return None
                
                parts = user_input.split()
                if len(parts) != 2:
                    print("输入格式错误！请输入两个数字，用空格分隔。")
                    continue
                
                row, col = int(parts[0]), int(parts[1])
                
                if not self.board.is_valid_move(row, col):
                    if not (0 <= row < self.board.size and 0 <= col < self.board.size):
                        print(f"坐标超出范围！请输入 0-{self.board.size-1} 之间的数字。")
                    else:
                        print("该位置已有棋子！请选择其他位置。")
                    continue
                
                return row, col
                
            except ValueError:
                print("输入格式错误！请输入数字。")
            except KeyboardInterrupt:
                print("\n游戏被中断！")
                return None
    
    def play_turn(self):
        """执行一回合"""
        move = self.get_move_input()
        if move is None:
            self.game_over = True
            return
        
        row, col = move
        self.board.make_move(row, col)
        
        # 检查是否获胜
        winner = self.board.check_winner(row, col)
        if winner:
            self.winner = winner
            self.game_over = True
            return
        
        # 检查是否平局
        if self.board.is_board_full():
            self.game_over = True
            return
        
        # 切换玩家
        self.board.switch_player()
    
    def display_result(self):
        """显示游戏结果"""
        self.clear_screen()
        self.board.display_board()
        
        if self.winner:
            winner_name = "黑棋" if self.winner == 1 else "白棋"
            winner_symbol = "●" if self.winner == 1 else "○"
            print(f"🎉 恭喜！{winner_name}({winner_symbol}) 获胜！")
        else:
            print("游戏平局！")
        
        print("\n游戏结束。感谢游玩！")
    
    def run(self):
        """运行游戏主循环"""
        self.clear_screen()
        self.display_game_info()
        
        while not self.game_over:
            self.board.display_board()
            self.play_turn()
            
            if not self.game_over:
                # 可选：每步后清屏，使界面更清洁
                # self.clear_screen()
                pass
        
        self.display_result()


def main():
    """主函数"""
    try:
        print("欢迎来到五子棋游戏！")
        
        # 询问棋盘大小
        while True:
            try:
                size_input = input("请选择棋盘大小 (默认15，按回车使用默认值): ").strip()
                if not size_input:
                    board_size = 15
                    break
                
                board_size = int(size_input)
                if 10 <= board_size <= 20:
                    break
                else:
                    print("棋盘大小应在10-20之间！")
            except ValueError:
                print("请输入有效的数字！")
        
        # 创建并运行游戏
        game = GomokuGame(board_size)
        game.run()
        
    except KeyboardInterrupt:
        print("\n\n游戏被中断！再见！")
    except Exception as e:
        print(f"\n游戏出现错误：{e}")
        print("请重新启动游戏。")


if __name__ == "__main__":
    main()