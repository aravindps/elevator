"""
    # Simple Evlevator Simulation using Sprite package
"""

import random, os, sys, pygame

if not pygame.image: print 'Warning, image disabled'

log = open( "elevator_log.txt", "w" )

class Building( pygame.sprite.Sprite ):
    """ Structure of the Building """

    def __init__( self, floor = 6 ):
        """ Intialisation """

        pygame.sprite.Sprite.__init__( self )
        self.screen = pygame.display.get_surface()

        self.num_of_floors = floor
        self.customer_list = self.__generate_customer()

        self.black = (0, 0, 0)
        self.red = (255, 0, 0)

        self.floor_width = self.screen.get_width() * (0.25)                        ## 2/8
        self.floor_height = ( self.screen.get_height()-15 )/ self.num_of_floors     ## height/num_of_floors

        ##  lift margin
        self.hor_margin = self.floor_width * 0.3
        self.ver_margin = self.floor_height * 0.15

        self.leftwall = self.screen.get_width() * (0.375)                          ## 3/8
        self.ground = self.screen.get_height() - 10
        self.load_background()

    def screen_shot( self ):
        """ Screen shot """
        pygame.image.save( self.screen, "background.bmp" )
        return

    def load_background( self ):

        self.screen.fill( ( 255, 255, 255 ) )
        self.draw_building()
        self.screen_shot()
        current_dir = os.path.dirname( os.path.abspath(__file__) )
        background = os.path.join( current_dir, "background.bmp" )
        try:
            self.image = pygame.image.load( background ).convert()
        except pygame.error:
            print >> log, "Background can't be loaded"
        return

    def draw_building ( self ):
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

    def __generate_customer( self ):
        """ Initialiing customer list """

        c = ()
        for i in range( 0, 3 ):
            tmp = Customer( self.num_of_floors )
            tmp.cur_floor = 3
            tmp.dst_floor = 0
            tmp.update()
            c += ( tmp, )
        return c

class Customer( pygame.sprite.Sprite ):
    """ Customer details """

    def __init__( self, floor ):

        pygame.sprite.Sprite.__init__( self )
        self.ID = random.randrange( 1, 100, 1 )
        self.finished = False
        self.num_of_floors = floor
        self.cur_floor = random.randrange( 0, self.num_of_floors, 1 )
        self.dst_floor = random.randrange( 0, self.num_of_floors, 1 )
        self.direction = -1         # 0 - Down; 1 - Up;
        self.update()

    def update( self ):

        if ( self.dst_floor == self.cur_floor ):
            self.finished = True
            self.direction = -1
        elif ( self.cur_floor < self.dst_floor ):
            self.direction = 1
            self.finished = False
        else:
            self.direction = 0
            self.finished = False
        return

class Elevator( pygame.sprite.DirtySprite ):
    """ Status of the Elevator """

    def __init__( self, floor_num ):

        pygame.sprite.DirtySprite.__init__( self )
        self.screen = pygame.display.get_surface()

        self.num_of_floors = floor_num
        self.cur_floor = 0
        self.direction = 1          # 0 - Down; 1 - Up; -1 - rest;

        self.floor_width =  self.screen.get_width() * (0.25)                       # 2/8
        self.floor_height = ( self.screen.get_height()-15 )/ self.num_of_floors     # height/num_of_floors

        #  lift margin
        self.hor_margin = self.floor_width * 0.4
        self.ver_margin = self.floor_height * 0.09

        self.lift_width = int( self.floor_width * 0.6 )
        self.lift_height = int( self.floor_height * 0.7 )
        self.moving = False
        self.overload = False
        self.load = 10

        print >> log, "lift_width- ", self.lift_width, " lift_height- ",  self.lift_height

        self.leftwall = self.screen.get_width() * (0.375)                          # 3/8
        self.ground = self.screen.get_height() - 10

        self.allcustomer = pygame.sprite.Group(  )
        self.elevator_customer = pygame.sprite.Group(  )
        self.removed_customer = []

        """
        Preload customers!

        c = ()
        for i in range( 0, 15 ):
            c += ( Customer( self.num_of_floors ), )

        c[0].cur_floor = 0
        c[0].dst_floor = 3

        c[1].cur_floor = 0
        c[1].dst_floor = 4

        c[2].cur_floor = 0
        c[2].dst_floor = 1

        c[3].cur_floor = 3
        c[3].dst_floor = 0

        c[4].cur_floor = 5
        c[4].dst_floor = 0

        self.add_customer( c )
        self.allcustomer.update()
        self.register_customer( pygame.sprite.Group( c ) )
        """
        for customer in self.allcustomer:
            print >>log, customer.ID, customer.cur_floor, customer.dst_floor, customer.finished, " direction=> ", customer.direction

        self.cur_pixel = int (( self.num_of_floors - self.cur_floor -1 ) * self.floor_height + 10 + (self.ver_margin/2))
        self.next_floor = int()

        # Intializing floor Group list
        self.floor_initialize()

        # loads lift images
        self.load_lift_image()

        # Sets initial postiton of lift rect
        self.rect = self.image.get_rect().move( self.leftwall + self.hor_margin, self.cur_pixel )

    def floor_initialize( self ):
        """ Checks when new customer is added """

        self.floor_list = ()
        for floor_num in range( 0, self.num_of_floors ):

            floor_customer = ()

            for i in self.allcustomer:
                if( i.cur_floor == floor_num and i.finished == False and ( i not in self.elevator_customer ) ):
                    floor_customer += ( i, )
            floor = pygame.sprite.Group(floor_customer)
            self.floor_list += ( floor, )

        return

    def load_lift_image( self ):
        """ Loading lift image """

        current_dir = os.path.dirname( os.path.abspath("__file__") )

        lift_rest = os.path.join( current_dir, 'lift.png' )
        lift_up = os.path.join( current_dir, 'lift_upward.png' )
        lift_down = os.path.join( current_dir, 'lift_downward.png' )

        try:
            self.img_rest = pygame.image.load( lift_rest )
            rect = self.img_rest.get_rect()
            self.ratio = rect[3]/self.lift_height
            rect = [ i/self.ratio for i in rect ]
            self.img_rest = pygame.transform.scale( self.img_rest, ( int( rect[2] ), int( rect[3] ) ) )

            self.img_up = pygame.image.load( lift_up )
            rect = self.img_up.get_rect()
            self.ratio = rect[3]/self.lift_height
            rect = [ i/self.ratio for i in rect ]
            self.img_up = pygame.transform.scale( self.img_up, ( int( rect[2] ), int( rect[3] ) ) )

            self.img_down = pygame.image.load( lift_down )
            rect = self.img_down.get_rect()
            self.ratio = rect[3]/self.lift_height
            rect = [ i/self.ratio for i in rect ]
            self.img_down = pygame.transform.scale( self.img_down, ( int( rect[2] ), int( rect[3] ) ) )

        except pygame.error, message:
            print >> log, "Can't load image"
            raise SystemExit, message

        self.set_lift_image()

    def set_lift_image( self ):

        if ( self.direction == 0 ):
                self.image = self.img_down
        elif ( self.direction == 1 ):
                self.image = self.img_up
        elif ( self.direction == -1 ):
                self.image = self.img_rest

        return

    def move_one_step ( self, dst_floor ):
        """ Moves a floor in both upward and downward """

        count = 1

        if ( self.direction == 1 ):         # Uplift
            count = - abs( count )
        elif ( self.direction == 0 ):       # Lower
            count = abs( count )
        else:
            print >> log, "Rest"
            return

        # Current dst floor Pixel identification
        tmp =  self.num_of_floors - dst_floor - 1
        dst_floor_pixel = int( ( self.floor_height * tmp ) + 10 + (self.ver_margin/2) )

        if ( self.cur_pixel == dst_floor_pixel ):
            self.cur_floor =  dst_floor
            self.cancel_customer( self.floor_list[self.cur_floor] )
            self.cancel_customer( self.elevator_customer )

            if ( len(self.elevator_customer) > self.load ):
                self.overload = True
            else:
                self.overload = False

            self.register_customer( self.floor_list[self.cur_floor] )
            self.moving = False
##            print >> log, self.rect, " <--- Updated"
##            print >> log, "count -- ", count, " cur_pixel -- ", self.cur_pixel, " dst_floor_pixel -- ", dst_floor_pixel, " moving -- ", self.moving
            pygame.time.delay(1000)
            return

        self.rect = self.rect.move( 0, count )
        self.cur_pixel += count
        self.moving = True
        pygame.time.delay(1)

    def update( self ):

        if ( self.moving == False ):
            self.next_floor = self.next_stop()

            self.register_customer( self.floor_list[ self.cur_floor ] )

            if self.direction != -1:
                print >> log, "    # self.next_stop =>", self.next_floor, " direction => ", self.direction
                if ( self.cur_floor < self.next_floor ):
                    self.direction = 1
                elif ( self.cur_floor > self.next_floor ):
                    self.direction = 0

            if self.direction == -1:
                """"
                print >> log, "waiting"

                for customer in self.allcustomer:
                    print >> log, customer.ID, customer.cur_floor, customer.dst_floor, customer.finished, " direction=> ", customer.direction
                """

            else:
                self.move_one_step( self.next_floor )
        else:
            self.move_one_step( self.next_floor )
        self.set_lift_image()
        self.dirty = 1
        return

    def add_customer( self, customer_list ):

        for customer in customer_list:
            self.allcustomer.add( customer )
            print >> log, "<+>-- ", customer.ID, customer.cur_floor, customer.dst_floor, customer.finished, " direction=> ", customer.direction
        self.floor_initialize()

    def register_customer( self, customer_list ):

        load = len( self.elevator_customer )
        if ( self.overload == True ):
            return

        for customer in customer_list:
            if ( load > self.load ):
                self.overload = True
                return
            if ( customer.finished == False and self.cur_floor == customer.cur_floor\
             and self.direction == customer.direction ):
                self.elevator_customer.add( customer )
                customer_list.remove( customer )
                print >> log, customer.ID, " (+) Entered"
            load += 1

    def cancel_customer( self, customer_list ):

        self.removed_customer = []
        for customer in customer_list:
            if ( self.cur_floor == customer.dst_floor ):
                customer.finished = True
                customer.in_elevator = False
                customer.cur_floor = self.cur_floor
                customer.update()
                customer_list.remove( customer )
                print >> log, customer.ID, " (-) Reached"
                self.removed_customer.append( customer )
        return

    def next_stop( self ):

        floor_num = []
        up, down, same, other = self.is_waiting()

        if ( len( self.elevator_customer ) ):
            print >> log, "_____________elevator_customer len -", len(self.elevator_customer ), " cur_floor -", self.cur_floor
            for customer in self.elevator_customer:
                if customer.direction == self.direction:
                    floor_num.append( customer.dst_floor )
                print >> log, customer.ID,

##        print >> log, "floor: ", floor_num, " customer waiting floor list: ", "up->", up, "down->", down,"same->", same,"other->", other

        if( self.direction == 1 ):              # Upward
            if not self.overload:
                floor_num.extend( up )
            if len( floor_num ):
                return min( floor_num )

        elif( self.direction == 0 ):            # Downward
            if not self.overload:
                floor_num.extend( down )
            if len( floor_num ):
                return max( floor_num )

        if len( up ) or len( down ):
            print >> log, "floor: ", floor_num, " customer waiting floor list: ", "up->", up, "down->", down,"same->", same,"other->", other
            print >> log, "!_-' Elevator empty '-_!"
            if self.direction == 1:
                if len( up ):
                    return min( up )
                elif len( down ):
                    self.direction = 0
                    print >> log, "(!) Direction changed: ", self.direction
                    return max( down )
            elif self.direction == 0:
                if len( down ):
                    return max( down )
                elif len( up ):
                    self.direction = 1
                    print >> log, "(!) Direction changed: ", self.direction
                    return min( up )
            elif self.direction == -1:
                self.direction = 1
                return next_stop()
        if len( same ) or len( other ):
            print >> log, "floor: ", floor_num, " customer waiting floor list: ", "up->", up, "down->", down,"same->", same,"other->", other
            if self.direction == 0:     self.direction = 1
            elif self.direction == 1:   self.direction = 0
            elif self.direction == -1:  self.direction = 1

            print >> log, "(!) Direction changed: ", self.direction
            self.register_customer( self.floor_list[ self.cur_floor ] )
            return self.next_stop()

        else:
            self.direction = -1

    def is_waiting( self ):
        """
            Check for waiting customer in each floor based on direction the customer wants to go
        """

        up = []
        down = []
        same = []
        other = []
        for i in range( len( self.floor_list ) ):
            if len( self.floor_list[i].sprites() ):
                for customer in self.floor_list[i]:
                    if( self.cur_floor < customer.cur_floor and self.direction == customer.direction ):
                        up.append( i )
                    elif( self.cur_floor > customer.cur_floor and self.direction == customer.direction ):
                        down.append( i )
                    elif self.cur_floor == customer.cur_floor:
                        same.append( i )
                    else:
                        other.append( i )
        return up, down, same, other


def main():
    """ Customer Creation """

    current_dir = os.path.dirname( os.path.abspath("__file__") )

    pygame.init()
    screen = pygame.display.set_mode ( ( 640, 480 ) )
    pygame.mouse.set_visible( 1 )
    pygame.display.set_caption( "Elevator using Sprite package" )

    total_floors = 6

    building = Building( total_floors )
    elevator = Elevator( total_floors )
    lift = pygame.sprite.LayeredDirty( elevator )

    background = building.image          # Surface

    # Display status text
    font = pygame.font.Font( None, 20 )
    text = font.render( " Click to add customer ", 1, (0,0,0) )
    textpos = text.get_rect( topleft = (10,10) )
    background.blit( text, textpos )

    lift.clear( screen, background )
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                customer = Customer( total_floors )
                print "[+>> {0} waiting in {1} --> {2} direction=> {3}".format( customer.ID, customer.cur_floor, customer.dst_floor, customer.direction )
                if customer.finished == False:
                    val = "[+>> {0} waiting in {1} --> {2} direction=> {3}".format( customer.ID, customer.cur_floor, customer.dst_floor, customer.direction )
                    text = font.render( val , 1, (0,255,0) )
                    textpos = text.get_rect( topleft = (10,25) )
                elevator.add_customer( ( customer, ) )

        screen.blit( background, (0,0) )
        add_text_rect = screen.blit( text, textpos )

        lift.update()
        rect_to_update = lift.draw( screen )

        rect_to_update.append( add_text_rect )

        for customer in elevator.removed_customer:
            line = 1
            val = "<<-] Customer %d Reached %d"%( customer.ID, customer.dst_floor )
            print val
            text = font.render( val , 1, (255,0,0) )
            textpos = text.get_rect( topleft = (10,25 + line*25 ) )
            rect_to_update.append( screen.blit( text, textpos ) )
            line += 1
        elevator.removed_customer = []

        pygame.display.update( rect_to_update )

    pygame.quit()

if __name__ == "__main__":    main()
