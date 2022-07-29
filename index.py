from threading import Thread
from reach_rpc import mk_rpc
import time
def main():
    rpc, rpc_callbacks = mk_rpc()

    starting_balance = rpc("/stdlib/parseCurrency", 6000)
    names = ['Alice', 'Bob']
    acc_alice = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob = rpc("/stdlib/newTestAccount",rpc("/stdlib/parseCurrency", 500) )

    

    def fmt(x):
        return rpc("/stdlib/formatCurrency", x, 4)

    def get_balance(w):
        return fmt(rpc("/stdlib/balanceOf", w))

    before_alice = get_balance(acc_alice)
    before_bob = get_balance(acc_bob)

    print("%s starting balance is %s algo" %(names[0],before_alice))
    print("%s starting balance is %s algo"%(names[1],before_bob))

    ctc_alice = rpc("/acc/contract", acc_alice)

    def play_alice():
        inheritance = int(input("How much are you willing to put in the inheritance fund Alice: "))
        def Inheritance():
            #print("Alice has deposited %s algo to the contract"%inheritance)
            return rpc("/stdlib/parseCurrency",inheritance)


        def presence():
            present = int(input("Are you present Alice: "))
            if (present == 0):
                print("i am not present ")
                return present
            elif(present == 1):
                print("i am still present")
                return present

        def deadline():
            deadline = int(input('input deadline for the contract Alice: '))
            return deadline
        def showdeadline(dl):
            print("%s the deadline is %s"%(names[0],rpc("/stdlib/bigNumberToNumber", dl)))

        rpc_callbacks(
            "/backend/Alice",
            ctc_alice,
            dict(
                Inheritance = Inheritance,presence = presence,deadline=deadline, showdeadline =showdeadline 
            )
        )
    alice = Thread(target=play_alice)
    alice.start()

    def play_bob():
        #time.sleep(5)
        wag = input("Do you accept this terms Bob: ")
        if wag == "yes" or wag == "y" or wag == "Y" or wag == "YES":

            def acceptinheritance(amt):
                print("%s accepts the terms of %s" % (names[1], fmt(amt)))

            def showdeadline(dl):
                print("%s the deadline is %s"%(names[1],rpc("/stdlib/bigNumberToNumber", dl)))

            ctc_bob = rpc("/acc/contract", acc_bob, rpc("/ctc/getInfo", ctc_alice))
            rpc_callbacks(
                "/backend/Bob",
                ctc_bob,
                dict(acceptinheritance=acceptinheritance, showdeadline = showdeadline),
            )
            rpc("/forget/ctc", ctc_bob)
        elif wag == "n" or wag == "no" or wag == "NO" or wag == "N":
            try:
                def acceptinheritance(amt):
                    print("%s accepts the terms of %s" % (names[1], fmt(amt)))

                def showdeadline(dl):
                    print("%s the deadline is %s"%(names[1],rpc("/stdlib/bigNumberToNumber", dl)))

                ctc_bob = rpc("/acc/contract", acc_bob, rpc("/ctc/getInfo", ctc_alice))
                rpc_callbacks(
                    "/backend/Bob",
                    ctc_bob,
                    dict(acceptinheritancess=acceptinheritance, showdeadlinesss = showdeadline),)
            except:
                print("Terms weren't agreed program ended")
                quit()
            

    bob = Thread(target=play_bob)
    bob.start()

    alice.join()
    bob.join()



    after_alice = get_balance(acc_alice)
    after_bob = get_balance(acc_bob)

    print("%s starting balance is %s algo" %(names[0],after_alice))
    print("%s starting balance is %s algo"%(names[1],after_bob))

    rpc("/forget/acc", acc_alice, acc_bob)
    rpc("/forget/ctc", ctc_alice)


if __name__ == "__main__":
    main()
