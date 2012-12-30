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
        self.lift = Elevator( self.num_of_floors )
        self.display = canvas( self.num_of_floors )
        self.display.paint()

    def run ( self ):

        """ Customer getting into lift in ground floor """
        for customer in self.customer_list:
            self.lift.register_customer( customer )

##        print self.lift.register_list

        for i in range( 0, self.num_of_floors, 1 ):
            """ Upward movement """
            print "upward ", i
            self.lift.cur_floor = i
            if( i != self.num_of_floors - 1):
                self.display.paint( i, i+1)

            for i in range ( len( self.lift.register_list ) ):
                if ( self.lift.cancel_customer( self.lift.register_list[i] ) ):
                    print "Reached dst_floor => ", self.lift.register_list[i].ID
            for customer in self.customer_list:
                self.lift.register_customer( customer )

        for i in range( self.num_of_floors - 2, -1 , -1 ):
            """ Downward movement """
            print "downward ", i
            self.lift.cur_floor = i
##            if ( i != self.num_of_floors -1 ):
            self.display.paint( i+1, i )

            for i in range ( len( self.lift.register_list ) ):
                if ( self.lift.cancel_customer( self.lift.register_list[i] ) ):
                    print "Reached dst_floor => ", self.lift.register_list[i].ID
            for customer in self.customer_list:
                self.lift.register_customer( customer )

##        for customer in self.customer_list:
##            print ( customer.ID )
        print "__Still waiting for the lift__"
        flag = 0
        for customer in self.customer_list:
            if ( customer.finished == False ):
##                print ( customer.ID )
                flag = 1
        if ( flag == 0 ):
            print "All safe"
        else:
            self.run()

        return

    def output ( self ):

        return


class Elevator:
    """ Status of the Elevator """

    def __init__( self, floor ):

        self.num_of_floors = floor
        self.register_list = ()
        self.cur_floor = 0
        self.direction = 0          # 0 - Down; 1 - Up;

    def register_customer( self, customer ):
        if ( customer.finished == False and self.cur_floor == customer.cur_floor ):
            self.register_list += ( customer, )
            customer.in_elevator = True

        return

    def cancel_customer( self, customer ):
        done = False
        if ( customer.in_elevator == True and self.cur_floor == customer.dst_floor ):
            customer.finished = True
            customer.cur_floor = self.cur_floor
            customer.in_elevator = False
            done = True
        return done

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

    total_floors = 10
    c = ( )
    for i in range( 0, 100 ):
        tmp = Customer( total_floors )
        c += (tmp, )

    b = Building( c, total_floors )

##    for i in range ( len( b.customer_list ) ):
##        print b.customer_list[i].ID, b.customer_list[i].cur_floor, b.customer_list[i].dst_floor, b.customer_list[i].finished

    b.run()

if __name__ == "__main__":

    main()
