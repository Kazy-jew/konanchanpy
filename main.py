from encapsulation import DL_Process, Print_Welcome

def konachan_main():
    Print_Welcome().konachan()
    while True:
        choice = input('select operation')
        if choice == '1':
            DL_Process().bulk_dl()
        elif choice == '2':
            DL_Process().chk_dl()
        elif choice == '3':
            pass
        elif choice == '4':
            exit('aborted')
        else:
            print('Invalid Input')


konachan_main()