# Pygame sample

import sys, pygame
pygame.init()

class canvas:

    def __init__( self ):
        self.size = width, height = 320, 240
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
    
        self.screen = pygame.display.set_mode( self.size )
        self.floor_num = 5
        self.floor_width = self.screen.get_width() * (0.125)                    ## 2/16
        self.floor_height = ( self.screen.get_height()-10 )/ self.floor_num      ## height/num_of_floors

        ##  lift margin
        self.hor_margin = 45
        self.ver_margin = 10

        self.leftwall = self.screen.get_width() * (0.4375)            ## 7/16
        self.ground = self.screen.get_height() - 5
        self.count = self.floor_height
        
    def draw_building( self ):
        """ Draws the whole building """

        ## drawing leftwall
        pygame.draw.line( self.screen, self.black, ( self.leftwall , 10 ) , ( self.leftwall , self.ground) , 2 )
        
        ## drawing rightwall
        pygame.draw.line( self.screen, self.black, ( self.leftwall + self.floor_width ,10 ) , ( self.leftwall + self.floor_width, self.ground) , 2 )
        
        ## drawing building floors
        for i in range ( 10, self.screen.get_height() , self.floor_height):
            pygame.draw.line( self.screen, self.black, ( self.leftwall, i ) ,( self.leftwall + self.floor_width, i) , 2 )
            
        ## Ground line
        pygame.draw.line( self.screen, self.black, ( 10, self.ground ) , ( self.screen.get_width() - 10 , self.ground ) , 4 )
        
        return

    def draw_lift( self, offset = 0 ):
        """ draws the lift based on offset """

        lift = ( self.leftwall + self.hor_margin, self.ver_margin + offset ,    
                             self.floor_width - 2*self.hor_margin, self.floor_height - 2*self.ver_margin )  ## ( x, y, width, height )
        pygame.draw.rect( self.screen, self.red, lift, 3 )
        return

    def paint( self, cur_floor, dst_floor  ):
        """ Draws the whole image """
        print "paint() method called"
        self.total_floor = 5
        self.cur_floor = cur_floor
    
        j = ( self.total_floor - self.cur_floor -1  ) * self.floor_height + 10  ## Current floor
        move = False
        dst_floor =  self.total_floor - dst_floor - 1
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            dst = ( self.floor_height * dst_floor ) + 10
            
            if ( j == dst ):        ## Stay where you are
                move = False
                self.screen.fill( ( 255, 255, 255 ) )
                self.draw_building()
                self.draw_lift(j)
                pygame.display.update()
            elif ( j > dst ):       ## Uplift
                self.count = - abs( self.count )
                move = True
            elif ( j < dst ):       ## Lower
                self.count = abs( self.count )
                move = True
                
            while move:

                self.screen.fill( ( 255, 255, 255 ) )
                self.draw_building()
                self.draw_lift(j)
                pygame.display.update()
                
                print "j-> %d" % j, " count-> %d" % self.count, " dst-> %d" % dst
                if ( j == dst ):
                    print (" Reached dst ")
                    move = False
                    break
                    
                j += self.count
                
                pygame.time.delay( 1000 )
            
        return


if __name__ == "__main__":

    c = canvas()
    c.paint(3, 0)
    sys.exit()
