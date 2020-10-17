import numpy as np
from PIL import Image, ImageDraw

class SnakeGame:
    def __init__(self,grid_size=29):
        self.grid_size = grid_size

    def reset(self):
        self.snake = []
        self.x = int(self.grid_size // 2)
        self.y = int(self.grid_size // 2)
        self.snake.append({"x":self.x, "y":self.y})
        startx = self.x
        starty = self.y
        # spawn_choices = [
        #             [{"x":startx+1, "y":starty},{"x":startx+2, "y":starty},{"x":startx+3, "y":starty},{"x":startx+4, "y":starty}],
        #             [{"x":startx-1, "y":starty},{"x":startx-2, "y":starty},{"x":startx-3, "y":starty},{"x":startx-4, "y":starty}],
        #             [{"x":startx, "y":starty+1},{"x":startx, "y":starty+2},{"x":startx, "y":starty+3},{"x":startx, "y":starty+4}],
        #             [{"x":startx, "y":starty-1},{"x":startx, "y":starty-2},{"x":startx, "y":starty-3},{"x":startx, "y":starty-4}]
        #             ]
        spawn_choices = [
                    [{"x":startx+1, "y":starty}],
                    [{"x":startx-1, "y":starty}],
                    [{"x":startx, "y":starty+1}],
                    [{"x":startx, "y":starty-1}]
                    ]
        spawn_choice = spawn_choices[np.random.randint(4)]
        for choice in spawn_choice:
            self.snake.append(choice)
            self.food =  {"x":np.random.randint(0,self.grid_size), "y":np.random.randint(0,self.grid_size)}
            self.reward = 0
            self.game_over = False
            self.distance =  np.round( ((startx - self.food["x"])**2 + (starty - self.food["y"])**2) ** 0.5, 2)
            self.old_distance = self.distance

        observation = self.get_state()
        return observation
    
    def step(self,action):
        self.reward = 0
        old_pos = self.snake
        old_head = self.snake[0]
        #actions 0,1,2,3 -> U,D,R,L
        if action == 0:
            new_head = {"x":old_head["x"] , "y":old_head["y"] - 1}
        elif action == 1:
            new_head = {"x":old_head["x"] , "y":old_head["y"] + 1}
        elif action == 2:
            new_head = {"x":old_head["x"] + 1, "y":old_head["y"]}
        elif action == 3:
            new_head = {"x":old_head["x"] - 1, "y":old_head["y"] }
        else:
            print("wrong input. expected 0~4")
        
        if new_head["x"] == self.food["x"] and new_head["y"] == self.food["y"]:
            self.food =  {"x":np.random.randint(0,self.grid_size), "y":np.random.randint(0,self.grid_size)}
            self.reward += 10
        else:
            self.snake.pop()

        self.snake.insert(0,new_head)

        self.distance =np.round(( (new_head["x"] - self.food["x"])**2 + (new_head["y"] - self.food["y"])**2 ) **0.5, 2)
        if self.distance < self.old_distance:
            self.reward +=1
        if self.distance > self.old_distance:
            self.reward -= 1

        self.old_distance = self.distance

        if self.collision_self(new_head,self.snake) or self.collision_wall(new_head):
            self.reward -= 100
            self.game_over = True

        observation = self.get_state()
        return observation, self.reward, self.game_over

    def animate(self,ep,steps,score,snake_len):
        game_matrix = np.zeros((self.grid_size*10,self.grid_size*10,3),dtype=np.uint8)
        game_matrix[self.food["y"]* 10 : self.food["y"]*10 + 10 ,self.food["x"]* 10 : self.food["x"]*10 + 10] = [255,0,0]
        
        for pos in self.snake:
            game_matrix[pos["y"]* 10 :pos["y"]*10 + 10,pos["x"]* 10:pos["x"]*10 + 10] = [0,200,0]   
            if pos == self.snake[0]:
                game_matrix[pos["y"]* 10 :pos["y"]*10 + 10,pos["x"]* 10:pos["x"]*10 + 10] = [0,255,0]

        if self.game_over:
            edge = self.grid_size*10-1
            line_width = 4
            game_matrix[0:edge,0:line_width]=[200,0,0]
            game_matrix[0:edge,edge-line_width:edge]=[200,0,0]
            game_matrix[0:line_width,0:edge]=[200,0,0]
            game_matrix[edge-line_width:edge,0:edge]=[200,0,0]
        img = Image.fromarray(game_matrix, 'RGB')
        d = ImageDraw.Draw(img)
        d.text((10,10), f"ep:{ep}  steps:{steps}   score:{score}    length:{snake_len}", fill=(255,255,0))
        #d.multiline_text((10,10), f"{self.get_state()[0:4]} \n {self.get_state()[4:12]} \n {self.get_state()[12:]}", fill=(255,255,0))

        return img#, game_matrix

    def collision_self(self,newhead,snake):

        flag = False
        for i in range(1,len(snake)):
            if newhead["x"] == snake[i]["x"] and newhead["y"] == snake[i]["y"]:
                flag =  True
        return flag

    def collision_wall(self,newhead):
        if newhead["x"] < 0 or newhead["y"] < 0 or newhead["x"] > self.grid_size-1 or newhead["y"] > self.grid_size-1:
            return True
        else:
            return False

    def get_state(self):
        snake = self.snake
        grid_size = self.grid_size
        food = self.food
        head = snake[0]
        body = snake[1]
        #DIRECTIONS
        #   UL  U   UR      |   (x-1,y-1)      (x,y-1)      (x+1,y-1)    
        #                   |
        #   L   S   R       |   (x-1,y)         (x,y)       (x+1,y)           
        #                   |
        #   DL  D   DR      |   (x-1,y+1)      (x,y+1)      (x+1,y+1)           
        fd_d = 0.0
        fd_u = 0.0
        fd_r = 0.0
        fd_l = 0.0

        w_ul = 0.0  #(x-1,y-1) 
        w_u = 0.0   #(x,y-1)
        w_ur = 0.0  #(x+1,y-1)
        w_l = 0.0   #(x-1,y)
        w_r = 0.0   #(x+1,y) 
        w_dl = 0.0  #(x-1,y+1)
        w_d = 0.0   #(x,y+1)
        w_dr = 0.0  #(x+1,y+1)

        d_d = 0.0
        d_u = 0.0
        d_r = 0.0
        d_l = 0.0
        
        #Food is XX relative to the snake head
        if head["y"] < food["y"]:
            fd_d = 1.0
        elif head["y"] > food["y"]:
            fd_u = 1.0
        if head["x"] < food["x"]:
            fd_r = 1.0
        elif head["x"] > food["x"]:
            fd_l = 1.0
        #Wall is directly XX the snake
        if head["y"]+1 == grid_size:
            w_dl = 1.0
            w_d = 1.0
            w_dr = 1.0
        elif head["y"]-1 == -1:
            w_ul = 1.0
            w_u = 1.0
            w_ur = 1.0
        if head["x"]-1 == -1:
            w_ul = 1.0
            w_l = 1.0
            w_dl = 1.0
        elif head["x"]+1 == grid_size:
            w_ur = 1.0
            w_r = 1.0
            w_dr = 1.0
        #Body is directly XX the snake
        for s in snake:
            if head["x"]-1 == s["x"] and head["y"]-1 == s["y"]:
                w_ul = 1.0
            if head["x"] == s["x"] and head["y"]-1 == s["y"]:
                w_u = 1.0
            if head["x"]+1 == s["x"] and head["y"]-1 == s["y"]:
                w_ur = 1.0
            if head["x"]-1 == s["x"] and head["y"] == s["y"]:
                w_l = 1.0
            if head["x"]+1 == s["x"] and head["y"] == s["y"]:
                w_r = 1.0
            if head["x"]-1 == s["x"] and head["y"]+1 == s["y"]:
                w_dl = 1.0
            if head["x"] == s["x"] and head["y"]+1 == s["y"]:
                w_d = 1.0
            if head["x"]+1 == s["x"] and head["y"]+1 == s["y"]:
                w_dr = 1.0
        #Snake is currently headed in the XX direction
        if head["y"]+1 == body["y"]:
            d_u = 1.0
        elif head["y"]-1 == body["y"]:
            d_d = 1.0
        if head["x"]+1 == body["x"]:
            d_l = 1.0
        elif head["x"]-1 == body["x"]:
            d_r = 1.0

        

        return  [ fd_d, fd_u, fd_l, fd_r,  w_ul,w_u,w_ur,w_l,w_r,w_dl,w_d,w_dr ,d_d ,d_u,d_l ,d_r ]