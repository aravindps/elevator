# Simple Evlevator Simulation

import random
from draw import canvas

class Building:
    """ Structure of the Building """

    def __init__( self, customer, floor = 6 ):
        """ Intialisation """

        self.customer_list = customer
        self.num_of_floors = floor
        self.elevator = 1

    def run ( self ):
        c = canvas()
        c.paint(0, 3)
        sys.exit()     
        return

    def output ( self ):
        
        return


class Elevator:
    """ Status of the Elevator """

    def __init__( self, floor ):
        
        self.num_of_floors = floor
        self.__register_list = ()
        self.cur_floor = 0
        self.direction = 0 # 0 - Down; 1 - Up;

    def register_customer( self, customer ):
        if ( customer.finished == False and self.cur_floor == customer.cur_floor ):
            self.__register_list += ( customer, )
            customer.in_elevator = True            
        return

    def cancel_customer( self, customer ):
        if ( customer.finished == True ):
            print self.__register_list

        return

class Customer:
    """ Customer details """

    def __init__( self, floor ):

        self.ID = random.randrange( 1, 100, 1 )
        self.in_elevator = False
        self.finished = False
        self.cur_floor = random.randrange( 0, floor, 1 )
        self.dst_floor = random.randrange( 0, floor, 1 )
        if ( self.dst_floor == self.cur_floor ):
            self.finished = True
            

def main():

    

    """ Customer Creation """
    c = ( )
    for i in range(10):
        tmp = Customer(4)
        c += (tmp, )
        
    b = Building(c, 4)
    e =  Elevator(b.num_of_floors)
    
    for i in range ( len( b.customer_list ) ):
        """ Register customer """
        e.register_customer(b.customer_list[i])
        print b.customer_list[i].ID, b.customer_list[i].cur_floor, b.customer_list[i].dst_floor, b.customer_list[i].finished, "in_elevator=>", b.customer_list[i].in_elevator

    b.run()
    

if __name__ == "__main__":

    main()
