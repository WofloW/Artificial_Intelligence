import gameplay
from copy import deepcopy

def horizontal_vague_stable(board,i,j):
    j1=0
    j2=7
    stable1=True    #left elements are all board[i][j]
    stable2=True    #right elements are all board[i][j]
    filled=True     #this row is filled with elements
    while j1<j:
        if board[i][j1] != board[i][j]:
            stable1 = False
        if board[i][j1] == '.':
            filled = False
        j1+=1
    while j2>j:
        if board[i][j1] != board[i][j]:
            stable2 = False
        if board[i][j1] == '.':
            filled = False
        j2-=1
    return stable1 or stable2 or filled

def vertical_vague_stable(board,i,j):
    i1=0
    i2=7
    stable1=True    #up elements are all board[i][j]
    stable2=True    #down elements are all board[i][j]
    filled=True     #column is filled with elements
    while i1<i:
        if board[i1][j] != board[i][j]:
            stable1 = False
        if board[i1][j] == '.':
            filled = False
        i1+=1
    while i2>i:
        if board[i2][j] != board[i][j]:
            stable2 = False
        if board[i2][j] == '.':
            filled = False
        i2-=1
    return stable1 or stable2 or filled


# calculate num_point, weight_point,frontier_point, stable_point
def value(board,ori_color,search_depth,total_num):
    weight = [[99, -8, 8,  6,  6, 8, -8,99], [-8,-24,  -4,  -3,  -3,  -4,-24, -8], [8,  -4,  7,  4,  4,  7,  -4, 8], [6,  -3,  4,  0,  0,  4,  -3,  6], [6,  -3,  4,  0,  0,  4,  -3,  6], [8,  -4,  7,  4,  4,  7,  -4, 8],[-8,-24,  -4,  -3,  -3,  -4,-24, -8], [99, -8, 8,  6,  6, 8, -8,99]]
    value_point=0

    num_self=0      #total_num
    num_op=0
    num_point=0

    frontier_self=0      #element is on the frontier
    frontier_op=0
    frontier_point=0

    stable_self=0      #element is stable and the element is on the side
    stable_op=0
    stable_point=0

    border_x=[-1,0,1,-1,1,-1,0,1]
    border_y=[1,1,1,0,0,-1,-1,-1]
    for i in range(8):
        for j in range(8):
            #weight_point num_point
            if board[i][j] == ori_color:
                value_point+=weight[i][j]
                num_self+=1
            elif board[i][j] == gameplay.opponent(ori_color):
                value_point-=weight[i][j]
                num_op+=1
            #frontier_point
            if board[i][j] != '.':
                for k in range(8):
                    new_x=i+border_x[k]
                    new_y=j+border_y[k]
                    if gameplay.validPos(new_x,new_y) and board[new_x][new_y] == '.':
                        if board[i][j] == ori_color:
                            frontier_self+=1
                        else:
                            frontier_op+=1
                        break
            #stable_point- just vaguely caculate
            if total_num>=20:
                if (i==0 or i==7) and j!=0 and j!=7 and board[i][j] !='.':
                    if horizontal_vague_stable(board,i,j):
                        if board[i][j] == ori_color:
                            stable_self+=1
                        else:
                            stable_op+=1
                if (j==0 or j==7) and i!=0 and i!=7 and board[i][j] !='.':
                    if vertical_vague_stable(board,i,j):
                        if board[i][j] == ori_color:
                            stable_self+=1
                        else:
                            stable_op+=1

    if frontier_self>frontier_op:
        frontier_point=-100*frontier_self/(frontier_self+frontier_op)
    elif frontier_op>frontier_self:
        frontier_point=100*frontier_self/(frontier_self+frontier_op)

    if num_self> num_op:
        num_point=100*num_self/(num_self+num_op)
    elif num_op>num_self:
        num_point=-100*num_op/(num_self+num_op)
    else:
        num_point=0

    if stable_self> stable_op:
        stable_point=100*stable_self/(stable_self+stable_op)
    elif stable_op>stable_self:
        stable_point=-100*stable_op/(stable_self+stable_op)
    else:
        stable_point=0
    return num_point,value_point,frontier_point,stable_point


def movepoint(board,color):
    moves=[]
    for i in range(8):
        for j in range(8):
            if gameplay.valid(board, color, (i,j)):
                moves.append((i,j))
    return len(moves)


def mobility(board,ori_color):
    mp_self=movepoint(board,ori_color)
    mp_op=movepoint(board,gameplay.opponent(ori_color))
    if mp_self>mp_op:
        return 100*mp_self/(mp_self+mp_op)
    elif mp_op>mp_self:
        return -100*mp_op/(mp_self+mp_op)
    else:
        return 0

def corner_point(board,ori_color):
    cp_self=0
    cp_op=0
    corner=[0,7]
    for i in corner:
        for j in corner:
            if board[i][j]==ori_color:
                cp_self+=1
            elif board[i][j]==gameplay.opponent(ori_color):
                cp_op=+1
    return cp_self-cp_op


def near_corner(board,ori_color):
    nc_self=0
    nc_op=0
    side=[[0,1],[1,1],[1,0],[0,6],[1,6],[1,7],[6,0],[6,1],[7,1],[7,6],[6,7],[6,6]]
    for k in side:
        if board[k[0]][k[1]]== ori_color:
            nc_self+=1
        elif board[k[0]][k[1]]==gameplay.opponent(ori_color):
            nc_op+=1
    return -(nc_self-nc_op)


def calculate(board,search_depth,ori_color):
    total_num=gameplay.score(board)[0]+gameplay.score(board)[1]
    npp,vp,fpp,spp=value(board,ori_color,search_depth,total_num)
    cp=corner_point(board,ori_color)
    nc=near_corner(board,ori_color)
    mpp=mobility(board,ori_color)
    #total_num>=20 start calculating stable_point
    if total_num<20:
#npp:num_point cp:corner_point nc:near_corner mpp:mobility_point fpp:frontier_point vp:value_point spp:stablity_point
        return 20*npp+12000*cp+3000*nc+50*mpp+30*fpp+60*vp
    else:
        # return 10*npp+25*801.724*cp+382.026*12.5*nc+78.922*mpp+74.396*fpp+100*vp
        # print 'npp:',20*npp,'cp:',12000*cp,'nc:', 3000*nc,'mpp:', 30*mpp,'fpp:', 30*fpp,'vp:', 50*vp,'sp:', 20*spp
        return 20*npp+12000*cp+3000*nc+30*mpp+30*fpp+50*vp+20*spp





def nextMoveR(board, color, time):
    return nextMove(board, color, time, True)
    
def nextMove(board, color, time, reversed = False):
    moves = []
    for i in range(8):
        for j in range(8):
            if gameplay.valid(board, color, (i,j)):
                moves.append((i,j))
    if len(moves) > 9:
        deepest = 7
    else:
        deepest = 8
    search_depth = 0
    alpha = -float('inf')
    beta = float('inf')
    ori_color=color
    if not reversed:
        v,bestmove = maxvalue(board,color,ori_color,deepest,search_depth,alpha,beta)
    else:
        v,bestmove = minvalue(board,color,ori_color,deepest,search_depth,alpha,beta)
    return bestmove




def maxvalue(board,color,ori_color,deepest,search_depth,alpha,beta):
    search_depth=search_depth+1
    if search_depth == deepest or gameplay.gameOver(board):
        return calculate(board,search_depth,ori_color)
    moves=[]
    bestmove="pass"
    for i in range(8):
        for j in range(8):
            if gameplay.valid(board, color, (i,j)):
                moves.append((i,j))
    v=-float('inf')
    if len(moves) == 0:
        if search_depth==1:
            return float('inf'),"pass"
        else:
            return float('inf')
    # print 'max',search_depth
    # print moves
    for move in moves:
        newBoard = deepcopy(board)
        gameplay.doMove(newBoard,color,move)
        min_value=minvalue(newBoard,gameplay.opponent(color),ori_color,deepest,search_depth,alpha,beta)
        if min_value>v:
            # if search_depth==1:
            #     print "v=",v,"min_value=",min_value
            v=min_value
            if search_depth==1:
                bestmove=move
        if v>=beta:
            if search_depth==1:
                return v,bestmove
            else:
                return v
        alpha=max(alpha,v)
    if search_depth==1:
        return v,bestmove
    else:
        return v


def minvalue(board,color,ori_color,deepest,search_depth,alpha,beta):
    search_depth=search_depth+1
    if search_depth == deepest or gameplay.gameOver(board):
        return calculate(board,search_depth,ori_color)
    moves=[]
    bestmove="pass"
    for i in range(8):
        for j in range(8):
            if gameplay.valid(board, color, (i,j)):
                moves.append((i,j))
    v=float('inf')
    if len(moves) == 0:
        if search_depth==1:
            return -float('inf'),"pass"
        else:
            return -float('inf')
    # print 'min',search_depth
    # print moves
    for move in moves:
        newBoard = deepcopy(board)
        gameplay.doMove(newBoard,color,move)
        max_value=maxvalue(newBoard,gameplay.opponent(color),ori_color,deepest,search_depth,alpha,beta)
        if max_value<v:
            v=max_value
            if search_depth==1:
                bestmove=move
        if v<=alpha:
            if search_depth==1:
                return v,bestmove
            else:
                return v
        alpha=min(beta,v)
    if search_depth==1:
        return v,bestmove
    else:
        return v